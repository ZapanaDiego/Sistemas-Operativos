#!/usr/bin/env python3
"""Genera las texturas de código y terminal desde el demo real.

No inventa líneas: lee `../entornoRTOS/src/`, `include/` y `out/`, y captura
la salida por consola del binario. Los fragmentos se identifican con su archivo
y número de línea; `...` marca una omisión.

Uso:
    python3 assets/code/make_textures.py
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SIM = HERE.parents[1]
REPO = HERE.parents[2]
RTOS = REPO / "entornoRTOS"
FONT_REGULAR = SIM / "assets" / "fonts" / "DejaVuSansMono.ttf"
FONT_BOLD = SIM / "assets" / "fonts" / "DejaVuSansMono-Bold.ttf"

WIDTH, HEIGHT = 1920, 1080
BG = (11, 15, 20)
TEXT = (216, 222, 233)
DIM = (92, 103, 115)
AMBER = (255, 176, 0)
GREEN = (51, 255, 119)
RED = (255, 59, 48)


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.exists():
        raise FileNotFoundError(f"falta la fuente: {path}")
    return ImageFont.truetype(str(path), size)


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def run_console(scenario: str) -> list[str]:
    binary = RTOS / "entornoRTOS"
    if not binary.exists():
        raise FileNotFoundError(
            f"falta {binary}; ejecuta `make` en {RTOS} antes de generar texturas"
        )
    result = subprocess.run(
        [str(binary), "--scenario", scenario],
        cwd=RTOS,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().splitlines()


def trace_window(path: Path, start: float, end: float, tokens: tuple[str, ...]) -> list[str]:
    selected: list[str] = []
    pattern = re.compile(r"\[\s*([0-9.]+)\]")
    for line in read_lines(path):
        match = pattern.match(line)
        if not match:
            continue
        moment = float(match.group(1))
        if start <= moment <= end and any(token in line for token in tokens):
            selected.append(line)
    return selected


def scanlines(image: Image.Image) -> Image.Image:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(0, image.height, 4):
        draw.line((0, y, image.width, y), fill=(0, 0, 0, 18))
    return Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")


def frame(image: Image.Image, color: tuple[int, int, int] = AMBER) -> None:
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (18, 18, WIDTH - 18, HEIGHT - 18),
        radius=18,
        outline=(*color, 90),
        width=2,
    )


def code_panel() -> tuple[Image.Image, str]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    header_font = font(FONT_BOLD, 29)
    code_font = font(FONT_REGULAR, 26)
    line_number_font = font(FONT_REGULAR, 22)

    sections = [
        (
            "src/pipe.c",
            [65, 66, 67, None, 72, 73, 74, 76, 77, None, 95],
            {72: (*AMBER, 45), 95: (*AMBER, 45)},
        ),
        (
            "src/scenario.c",
            [43, 44, 45, 46, 47, 48, 49, 50],
            {44: (*RED, 45)},
        ),
        (
            "include/vxworks_like.h",
            [15, 16, 17],
            {16: (*GREEN, 45)},
        ),
    ]

    x_number = 74
    x_code = 138
    y = 52
    text_lines: list[str] = []
    first_section = True

    for relative, numbers, highlights in sections:
        if not first_section:
            y += 12
        first_section = False
        draw.text((x_number, y), relative, font=header_font, fill=AMBER)
        text_lines.append(f"### {relative}")
        y += 40

        source = read_lines(RTOS / relative)
        for number in numbers:
            if number is None:
                draw.text((x_code, y), "...", font=code_font, fill=DIM)
                text_lines.append("    ...")
                y += 50
                continue

            text = source[number - 1]
            background = highlights.get(number)
            if background is not None:
                draw.rounded_rectangle(
                    (58, y - 3, WIDTH - 58, y + 31),
                    radius=5,
                    fill=background,
                )
            draw.text(
                (x_number, y + 2),
                f"{number:4d}",
                font=line_number_font,
                fill=DIM,
            )
            draw.text((x_code, y), text, font=code_font, fill=TEXT)
            text_lines.append(f"{number:4d}  {text}")
            y += 33

    frame(image)
    return scanlines(image), "\n".join(text_lines) + "\n"


def terminal_panel(
    scenario: str,
    target: str,
    trace_path: Path,
    start: float,
    end: float,
    tokens: tuple[str, ...],
) -> tuple[Image.Image, str]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    mono = font(FONT_REGULAR, 31)
    mono_bold = font(FONT_BOLD, 31)

    draw.rounded_rectangle((40, 34, WIDTH - 40, 96), radius=12, fill=(18, 24, 32))
    for index, color in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        cx = 72 + index * 30
        draw.ellipse((cx, 55, cx + 14, 69), fill=color)
    draw.line((40, 96, WIDTH - 40, 96), fill=(42, 52, 65), width=1)

    console = run_console(scenario)
    trace = trace_window(trace_path, start, end, tokens)
    lines = [f"$ make {target}", *console, "", *trace]
    summary = next(
        (line for line in read_lines(trace_path) if line.startswith("# SUMMARY")),
        "",
    )
    if summary:
        lines.append(summary)

    y = 150
    for line in lines:
        color = TEXT
        if line.startswith("$"):
            color = AMBER
        elif "WATCHDOG: RESET" in line or "MISS" in line or "RESET" in line:
            color = RED
        elif line.strip() == "OK" or "INHERIT" in line or "UNLOCK" in line:
            color = GREEN
        elif "LOCK" in line or "WAIT" in line:
            color = AMBER
        elif line.startswith("# SUMMARY"):
            color = DIM

        active_font = mono_bold if line.startswith("$") or line.strip() == "OK" else mono
        draw.text((92, y), line, font=active_font, fill=color)
        y += 44

    draw.rectangle((92, y + 2, 106, y + 30), fill=AMBER)
    frame(image)
    return scanlines(image), "\n".join(lines) + "\n"


def main() -> None:
    code_image, code_text = code_panel()
    code_image.save(HERE / "code_panel.png")
    (HERE / "code_panel.txt").write_text(code_text, encoding="utf-8")

    off_image, off_text = terminal_panel(
        "s1",
        "run-pip-off",
        RTOS / "out" / "s1_pip_off.txt",
        0.499,
        0.625,
        ("LOCK", "PREEMPT", "WAIT", "BURST", "MISS", "RESET"),
    )
    off_image.save(HERE / "terminal_off.png")
    (HERE / "terminal_off.txt").write_text(off_text, encoding="utf-8")

    on_image, on_text = terminal_panel(
        "s2",
        "run-pip-on",
        RTOS / "out" / "s2_pip_on.txt",
        0.499,
        0.506,
        ("LOCK", "WAIT", "INHERIT", "UNLOCK"),
    )
    on_image.save(HERE / "terminal_on.png")
    (HERE / "terminal_on.txt").write_text(on_text, encoding="utf-8")

    print("TEXTURES_OK")
    for name in ("code_panel.png", "terminal_off.png", "terminal_on.png"):
        print(f"  {HERE / name}")


if __name__ == "__main__":
    main()
