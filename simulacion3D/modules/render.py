"""Ajustes de render, guardado y medición de tiempos.

Blender 5.2.3 LTS identifica el motor EEVEE como ``BLENDER_EEVEE``.
El bloom de versiones anteriores ya no es una propiedad de EEVEE; se
reconstruye con un nodo Glare del compositor para conservar el lenguaje
visual del contrato (§7.8).
"""

from __future__ import annotations

import time
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent.parent
FPS = 24
FRAME_START = 1
FRAME_END = 4320
RESOLUTION_FINAL = (1920, 1080)
RESOLUTION_DRAFT = (1280, 720)


def setup_render(
    scene: bpy.types.Scene,
    *,
    draft: bool = False,
    samples: int | None = None,
    bloom: bool = True,
) -> None:
    """Configura EEVEE, resolución, fps y salida PNG del contrato."""
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x, scene.render.resolution_y = (
        RESOLUTION_DRAFT if draft else RESOLUTION_FINAL
    )
    scene.render.resolution_percentage = 100
    scene.render.fps = FPS
    scene.render.fps_base = 1.0
    scene.render.film_transparent = False
    scene.render.use_motion_blur = True
    scene.render.motion_blur_shutter = 0.5
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.color_depth = "8"
    scene.render.image_settings.compression = 15
    scene.eevee.taa_render_samples = samples or (16 if draft else 32)
    scene.eevee.use_shadows = True
    scene.eevee.use_raytracing = False
    scene.view_settings.view_transform = "AgX"
    scene.frame_start = FRAME_START
    scene.frame_end = FRAME_END
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    if bloom:
        setup_compositor(scene)


def setup_compositor(scene: bpy.types.Scene) -> None:
    """Añade un Glare suave para sustituir el bloom de EEVEE Legacy.

    Blender 5.2 usa un *compositing node group* en lugar de ``scene.node_tree``
    y el nodo Glare expone sus parámetros como entradas, no como propiedades.
    """
    scene.use_nodes = True
    tree = scene.compositing_node_group
    if tree is None:
        tree = bpy.data.node_groups.new("COMP_Film", "CompositorNodeTree")
        scene.compositing_node_group = tree
        tree.interface.new_socket(
            name="Image", in_out="OUTPUT", socket_type="NodeSocketColor"
        )

    tree.nodes.clear()
    render_layers = tree.nodes.new("CompositorNodeRLayers")
    glare = tree.nodes.new("CompositorNodeGlare")
    glare.inputs["Type"].default_value = "Fog Glow"
    glare.inputs["Quality"].default_value = "High"
    glare.inputs["Threshold"].default_value = 1.0
    glare.inputs["Size"].default_value = 0.6
    glare.inputs["Strength"].default_value = 0.35
    output = tree.nodes.new("NodeGroupOutput")

    tree.links.new(render_layers.outputs["Image"], glare.inputs["Image"])
    tree.links.new(glare.outputs["Image"], output.inputs["Image"])


def save_blend(scene: bpy.types.Scene, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(path))


def render_still(scene: bpy.types.Scene, path: Path, frame: int = 1) -> float:
    """Renderiza un frame y devuelve el tiempo de pared en segundos."""
    path.parent.mkdir(parents=True, exist_ok=True)
    scene.frame_set(frame)
    scene.render.filepath = str(path)
    started = time.perf_counter()
    bpy.ops.render.render(write_still=True)
    elapsed = time.perf_counter() - started
    print(f"RENDER_OK path={path} frame={frame} seconds={elapsed:.2f}")
    return elapsed
