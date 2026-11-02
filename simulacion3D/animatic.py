#!/usr/bin/env python3
"""Animatic de 18 s para validar el lenguaje visual del film.

No es la escena final: usa primitivas y una ciudad de tareas esquemática para
comprobar escala, cámara, paleta y transición terreno → lander → ciudad.

Uso:
    blender -b --factory-startup --python animatic.py -- --save
    blender -b --factory-startup --python animatic.py -- --test-frame
    blender -b --factory-startup --python animatic.py -- --render
"""

from __future__ import annotations

import argparse
import math
import random
import subprocess
import sys
from pathlib import Path

import bpy
from mathutils import noise

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules import cameras, materials, render

FPS = 24
DURATION_S = 18
FRAME_COUNT = FPS * DURATION_S
ANIM_BLEND = ROOT / "blender" / "animatic.blend"
FRAMES_DIR = ROOT / "out" / "animatic" / "frames"
TEST_FRAME = ROOT / "out" / "animatic" / "test_frame.png"
ANIM_MP4 = ROOT / "out" / "animatic.mp4"

COLLECTIONS = (
    "00_ENV",
    "01_LANDER",
    "02_ROVER",
    "03_TASKS",
    "04_FX",
    "05_CAMERAS",
    "06_LIGHTS",
)


def parse_args() -> argparse.Namespace:
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser(description="Animatic del film")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--test-frame", action="store_true")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--frame", type=int, default=216)
    parser.add_argument("--samples", type=int, default=12)
    return parser.parse_args(argv)


def reset_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def ensure_collections() -> dict[str, bpy.types.Collection]:
    scene = bpy.context.scene
    result: dict[str, bpy.types.Collection] = {}
    for name in COLLECTIONS:
        collection = bpy.data.collections.get(name) or bpy.data.collections.new(name)
        if scene.collection.children.get(name) is None:
            scene.collection.children.link(collection)
        result[name] = collection
    return result


def move_to(obj: bpy.types.Object, collection: bpy.types.Collection) -> None:
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)


def terrain_height(x: float, y: float) -> float:
    return (
        1.8 * noise.noise((x * 0.018, y * 0.018, 0.0))
        + 0.7 * noise.noise((x * 0.08, y * 0.08, 2.0))
        + 0.25 * noise.noise((x * 0.3, y * 0.3, 4.0))
    )


def add_terrain(collections: dict[str, bpy.types.Collection]) -> None:
    subdivisions = 100
    size = 200.0
    step = size / subdivisions
    start = -size / 2
    vertices: list[tuple[float, float, float]] = []
    for iy in range(subdivisions + 1):
        y = start + iy * step
        for ix in range(subdivisions + 1):
            x = start + ix * step
            vertices.append((x, y, terrain_height(x, y)))

    faces: list[tuple[int, int, int, int]] = []
    row = subdivisions + 1
    for iy in range(subdivisions):
        for ix in range(subdivisions):
            a = iy * row + ix
            b = a + 1
            c = a + row + 1
            d = a + row
            faces.append((a, b, c, d))

    mesh = bpy.data.meshes.new("ENV_Terrain")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    terrain = bpy.data.objects.new("ENV_Terrain", mesh)
    collections["00_ENV"].objects.link(terrain)
    terrain.data.materials.append(
        materials.make_principled("MAT_Mars", "#8B3A1E", roughness=0.95)
    )
    for polygon in terrain.data.polygons:
        polygon.use_smooth = True


def add_rocks(collections: dict[str, bpy.types.Collection]) -> None:
    rng = random.Random(42)
    rock_material = materials.make_principled(
        "MAT_Rock", "#5A2A1A", roughness=0.9
    )
    for index in range(70):
        x = rng.uniform(-85.0, 85.0)
        y = rng.uniform(-70.0, 85.0)
        if math.hypot(x + 12.0, y - 8.0) < 7.0:
            continue
        radius = rng.uniform(0.25, 1.7)
        z = terrain_height(x, y)
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=1, radius=radius, location=(x, y, z)
        )
        rock = bpy.context.object
        rock.name = f"ENV_Rock_{index:02d}"
        rock.scale = (1.0, rng.uniform(0.7, 1.3), rng.uniform(0.5, 1.0))
        rock.rotation_euler = (0.0, 0.0, rng.uniform(0.0, math.tau))
        rock.data.materials.append(rock_material)
        move_to(rock, collections["00_ENV"])


def add_cube(
    name: str,
    location: tuple[float, float, float],
    scale: tuple[float, float, float],
    material: bpy.types.Material,
    collection: bpy.types.Collection,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(material)
    move_to(obj, collection)
    return obj


def add_cylinder(
    name: str,
    location: tuple[float, float, float],
    radius: float,
    depth: float,
    material: bpy.types.Material,
    collection: bpy.types.Collection,
    *,
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    move_to(obj, collection)
    return obj


def add_lander(collections: dict[str, bpy.types.Collection]) -> None:
    base_x, base_y = -12.0, 8.0
    base_z = terrain_height(base_x, base_y)
    metal = materials.make_principled(
        "MAT_Metal", "#B0B0B0", roughness=0.35, metallic=0.8
    )
    panel = materials.make_principled(
        "MAT_Panel",
        "#1B2A4A",
        roughness=0.4,
        metallic=0.3,
        emission_color="#0A84FF",
        emission_strength=0.35,
    )
    add_cube(
        "LANDER_Body",
        (base_x, base_y, base_z + 0.75),
        (3.0, 2.0, 1.2),
        metal,
        collections["01_LANDER"],
    )
    add_cube(
        "LANDER_Panel_L",
        (base_x - 2.6, base_y, base_z + 1.25),
        (2.2, 1.6, 0.06),
        panel,
        collections["01_LANDER"],
    )
    add_cube(
        "LANDER_Panel_R",
        (base_x + 2.6, base_y, base_z + 1.25),
        (2.2, 1.6, 0.06),
        panel,
        collections["01_LANDER"],
    )
    add_cylinder(
        "LANDER_Mast",
        (base_x - 0.9, base_y, base_z + 2.4),
        0.06,
        2.6,
        metal,
        collections["01_LANDER"],
    )
    add_cube(
        "LANDER_Camera",
        (base_x - 0.9, base_y, base_z + 3.7),
        (0.22, 0.22, 0.22),
        metal,
        collections["01_LANDER"],
    )
    add_cylinder(
        "LANDER_Antenna",
        (base_x + 1.3, base_y, base_z + 2.3),
        0.035,
        1.6,
        metal,
        collections["01_LANDER"],
        rotation=(0.15, 0.0, 0.0),
    )


def add_rover(collections: dict[str, bpy.types.Collection]) -> None:
    x, y = -4.0, -1.0
    z = terrain_height(x, y)
    metal = materials.make_principled(
        "MAT_RoverMetal", "#C0C0C0", roughness=0.4, metallic=0.7
    )
    panel = materials.make_principled(
        "MAT_RoverPanel",
        "#1B2A4A",
        roughness=0.4,
        metallic=0.3,
        emission_color="#0A84FF",
        emission_strength=0.4,
    )
    add_cube("ROVER_Body", (x, y, z + 0.3), (0.7, 0.5, 0.28), metal, collections["02_ROVER"])
    add_cube("ROVER_Panel", (x, y, z + 0.5), (0.8, 0.55, 0.04), panel, collections["02_ROVER"])
    for index, (dx, dy) in enumerate(((-0.25, -0.25), (-0.25, 0.25), (0.25, -0.25), (0.25, 0.25))):
        add_cylinder(
            f"ROVER_Wheel_{index}",
            (x + dx, y + dy, z + 0.08),
            0.13,
            0.08,
            metal,
            collections["02_ROVER"],
            rotation=(0.0, math.pi / 2.0, 0.0),
        )


def add_city(collections: dict[str, bpy.types.Collection]) -> None:
    base_y = 22.0
    base_z = terrain_height(0.0, base_y) + 7.0
    platform = add_cylinder(
        "TASK_Platform",
        (0.0, base_y, base_z - 0.15),
        6.0,
        0.2,
        materials.make_principled("MAT_CityBase", "#101820", roughness=0.5, metallic=0.4),
        collections["03_TASKS"],
    )
    platform.scale = (1.0, 0.6, 1.0)

    threads = (
        ("TASK_BC_SCHED", -4.0, 10.0, "#FFFFFF", 5.0),
        ("TASK_BC_DIST", -2.0, 6.5, "#FF3B30", 5.0),
        ("TASK_MED_01", 0.0, 4.0, "#FF9500", 4.0),
        ("TASK_MED_02", 1.5, 4.0, "#FF9500", 4.0),
        ("TASK_MED_03", 3.0, 4.0, "#FF9500", 4.0),
        ("TASK_ASI_MET", 4.8, 2.0, "#0A84FF", 5.0),
    )
    for name, x, height, color, strength in threads:
        add_cylinder(
            name,
            (x, base_y, base_z + height / 2.0),
            0.09,
            height,
            materials.make_emission(f"MAT_{name}", color, strength=strength),
            collections["03_TASKS"],
        )

    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.8,
        minor_radius=0.12,
        location=(0.0, base_y - 2.0, base_z + 1.1),
    )
    lock = bpy.context.object
    lock.name = "FX_Lock"
    lock.data.materials.append(
        materials.make_emission("MAT_Lock", "#FFB300", strength=6.0)
    )
    move_to(lock, collections["03_TASKS"])

    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.9,
        minor_radius=0.08,
        location=(-2.0, base_y, base_z + 4.0),
        rotation=(math.pi / 2.0, 0.0, 0.0),
    )
    deadline = bpy.context.object
    deadline.name = "FX_Deadline"
    deadline.data.materials.append(
        materials.make_emission("MAT_Deadline", "#FF3B30", strength=4.0)
    )
    move_to(deadline, collections["03_TASKS"])

    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.8,
        minor_radius=0.07,
        location=(-4.0, base_y, base_z + 10.5),
        rotation=(math.pi / 2.0, 0.0, 0.0),
    )
    watchdog = bpy.context.object
    watchdog.name = "FX_Watchdog"
    watchdog.data.materials.append(
        materials.make_emission("MAT_Watchdog", "#FFFFFF", strength=4.0)
    )
    move_to(watchdog, collections["03_TASKS"])


def animate_city_visibility(collections: dict[str, bpy.types.Collection]) -> None:
    """Oculta la ciudad hasta que la cámara termina el acercamiento al lander."""
    for obj in collections["03_TASKS"].objects:
        obj.hide_render = True
        obj.keyframe_insert(data_path="hide_render", frame=1)
        obj.hide_render = False
        obj.keyframe_insert(data_path="hide_render", frame=230)


def add_world() -> None:
    scene = bpy.context.scene
    world = bpy.data.worlds.get("WORLD_Mars")
    if world is None:
        world = bpy.data.worlds.new("WORLD_Mars")
    background = world.node_tree.nodes.get("Background")
    if background is not None:
        background.inputs["Color"].default_value = (0.18, 0.055, 0.025, 1.0)
        background.inputs["Strength"].default_value = 0.8
    scene.world = world


def add_lights(collections: dict[str, bpy.types.Collection]) -> None:
    cameras.add_sun(
        "LIGHT_Sun",
        collections["06_LIGHTS"],
        energy=4.5,
        angle_deg=2.0,
        rotation_deg=(62.0, 0.0, 25.0),
        color=(1.0, 0.88, 0.74),
    )
    cameras.add_area_light(
        "LIGHT_Fill",
        (-25.0, -30.0, 22.0),
        (-12.0, 8.0, 2.0),
        collections["06_LIGHTS"],
        energy=900.0,
        size=18.0,
        color=(0.45, 0.62, 1.0),
    )


def add_camera_animation(collections: dict[str, bpy.types.Collection]) -> None:
    scene = bpy.context.scene
    camera = cameras.add_camera(
        "CAM_Animatic",
        (2.0, -20.0, 7.0),
        (-12.0, 8.0, 2.0),
        collections["05_CAMERAS"],
        lens=35.0,
    )
    scene.camera = camera
    target = bpy.data.objects["CAM_Animatic_TARGET"]

    keys = (
        (1, (2.0, -20.0, 7.0), (-12.0, 8.0, 2.0), 35.0),
        (144, (0.0, -8.0, 5.0), (-12.0, 8.0, 2.2), 40.0),
        (288, (0.0, 6.0, 10.0), (0.0, 22.0, 11.0), 35.0),
        (432, (0.0, 13.0, 10.0), (0.0, 20.0, 9.0), 50.0),
    )
    for frame, location, target_location, lens in keys:
        camera.location = location
        camera.data.lens = lens
        camera.keyframe_insert(data_path="location", frame=frame)
        camera.data.keyframe_insert(data_path="lens", frame=frame)
        target.location = target_location
        target.keyframe_insert(data_path="location", frame=frame)

    # La interpolación por defecto de Blender es Bezier; no se toca la acción
    # porque Blender 5.2 usa acciones por capas y `action.fcurves` ya no existe.


def build() -> None:
    reset_scene()
    collections = ensure_collections()
    add_world()
    add_terrain(collections)
    add_rocks(collections)
    add_lander(collections)
    add_rover(collections)
    add_city(collections)
    animate_city_visibility(collections)
    add_lights(collections)
    add_camera_animation(collections)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = FRAME_COUNT
    scene.render.fps = FPS
    print(
        "ANIMATIC_READY"
        f" objects={len(bpy.data.objects)}"
        f" frames={FRAME_COUNT}"
        f" engine={scene.render.engine}"
    )


def render_frame(scene: bpy.types.Scene, frame: int, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    scene.frame_set(frame)
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def encode() -> None:
    command = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(FPS),
        "-i",
        str(FRAMES_DIR / "frame_%04d.png"),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-crf",
        "20",
        str(ANIM_MP4),
    ]
    subprocess.run(command, check=True)
    print(f"ANIMATIC_MP4 path={ANIM_MP4}")


def main() -> None:
    args = parse_args()
    build()
    scene = bpy.context.scene
    render.setup_render(scene, draft=True, samples=args.samples)
    scene.frame_start = 1
    scene.frame_end = FRAME_COUNT
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720

    if args.save:
        render.save_blend(scene, ANIM_BLEND)
        print(f"BLEND_SAVED path={ANIM_BLEND}")

    if args.test_frame:
        render_frame(scene, args.frame, TEST_FRAME)
        print(f"TEST_FRAME frame={args.frame} path={TEST_FRAME}")

    if args.render:
        for frame in range(1, FRAME_COUNT + 1):
            render_frame(scene, frame, FRAMES_DIR / f"frame_{frame:04d}.png")
            if frame % 24 == 0 or frame == FRAME_COUNT:
                print(f"RENDER_PROGRESS frame={frame}/{FRAME_COUNT}")
        encode()


if __name__ == "__main__":
    main()
