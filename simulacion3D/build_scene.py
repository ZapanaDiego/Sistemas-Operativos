#!/usr/bin/env python3
"""Construye la escena base del film y permite un frame de prueba.

Uso:
    blender -b --factory-startup --python build_scene.py -- --save
    blender -b --factory-startup --python build_scene.py -- --test-frame --draft

La escena de esta iteración es un banco de pruebas de EEVEE y del compositor:
terreno plano, marcadores emisivos de las tareas, un cerrojo de prueba y una
cámara. Los módulos de terreno, lander, rover y ciudad de tareas se añaden en
las iteraciones siguientes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules import cameras, materials, render

BLEND_PATH = ROOT / "blender" / "pathfinder_failure.blend"
SPIKE_PATH = ROOT / "out" / "spike" / "frame_0001_1080p.png"
SPIKE_DRAFT_PATH = ROOT / "out" / "spike" / "frame_0001_720p.png"

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
    parser = argparse.ArgumentParser(description="Construye la escena del film")
    parser.add_argument("--save", action="store_true", help="guardar el .blend")
    parser.add_argument("--test-frame", action="store_true", help="renderizar un frame")
    parser.add_argument("--draft", action="store_true", help="720p y pocas muestras")
    parser.add_argument("--samples", type=int, default=None, help="muestras de EEVEE")
    return parser.parse_args(argv)


def reset_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def ensure_collections() -> dict[str, bpy.types.Collection]:
    scene = bpy.context.scene
    result: dict[str, bpy.types.Collection] = {}
    for name in COLLECTIONS:
        collection = bpy.data.collections.get(name)
        if collection is None:
            collection = bpy.data.collections.new(name)
        if scene.collection.children.get(name) is None:
            scene.collection.children.link(collection)
        result[name] = collection
    return result


def move_to(obj: bpy.types.Object, collection: bpy.types.Collection) -> None:
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)


def add_ground(collections: dict[str, bpy.types.Collection]) -> None:
    bpy.ops.mesh.primitive_plane_add(size=200.0, location=(0.0, 0.0, 0.0))
    ground = bpy.context.object
    ground.name = "ENV_Terrain_Test"
    material = materials.make_principled(
        "MAT_TestGround", "#3B2A22", roughness=0.95
    )
    ground.data.materials.append(material)
    move_to(ground, collections["00_ENV"])


def add_task_markers(collections: dict[str, bpy.types.Collection]) -> None:
    markers = (
        ("asi_met", (0.0, 0.0, 0.9), "#0A84FF", 5.0),
        ("med", (1.8, -0.4, 0.9), "#FF9500", 4.0),
        ("bc_dist", (-1.8, -0.4, 0.9), "#FF3B30", 5.0),
    )
    for role, location, color, strength in markers:
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.32, segments=32, ring_count=16, location=location
        )
        sphere = bpy.context.object
        sphere.name = f"FX_Test_{role}"
        sphere.data.materials.append(
            materials.make_emission(f"MAT_Test_{role}", color, strength=strength)
        )
        move_to(sphere, collections["04_FX"])

    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.55,
        minor_radius=0.10,
        location=(0.0, 0.0, 1.7),
    )
    lock = bpy.context.object
    lock.name = "FX_Test_Lock"
    lock.data.materials.append(
        materials.make_emission("MAT_Test_Lock", "#FFB300", strength=6.0)
    )
    move_to(lock, collections["03_TASKS"])


def add_lander_placeholder(collections: dict[str, bpy.types.Collection]) -> None:
    bpy.ops.mesh.primitive_cube_add(size=1.2, location=(-3.6, 1.2, 0.6))
    cube = bpy.context.object
    cube.name = "LANDER_TestBody"
    cube.data.materials.append(
        materials.make_principled("MAT_TestMetal", "#B0B0B0", roughness=0.35, metallic=0.8)
    )
    move_to(cube, collections["01_LANDER"])


def add_world() -> None:
    scene = bpy.context.scene
    world = bpy.data.worlds.get("WORLD_Test")
    if world is None:
        world = bpy.data.worlds.new("WORLD_Test")
    background = world.node_tree.nodes.get("Background")
    if background is not None:
        background.inputs["Color"].default_value = (0.012, 0.016, 0.028, 1.0)
        background.inputs["Strength"].default_value = 0.35
    scene.world = world


def add_lights(collections: dict[str, bpy.types.Collection]) -> None:
    cameras.add_sun("LIGHT_Sun", collections["06_LIGHTS"], energy=4.0)
    cameras.add_area_light(
        "LIGHT_Fill",
        (-5.0, -4.0, 5.0),
        (0.0, 0.0, 1.0),
        collections["06_LIGHTS"],
        energy=250.0,
        size=6.0,
    )


def add_camera(collections: dict[str, bpy.types.Collection]) -> None:
    scene = bpy.context.scene
    camera = cameras.add_camera(
        "CAM_Test",
        (7.0, -9.0, 4.5),
        (0.0, 0.0, 1.0),
        collections["05_CAMERAS"],
        lens=35.0,
    )
    scene.camera = camera


def build() -> None:
    reset_scene()
    collections = ensure_collections()
    add_world()
    add_ground(collections)
    add_task_markers(collections)
    add_lander_placeholder(collections)
    add_lights(collections)
    add_camera(collections)
    scene = bpy.context.scene
    print(
        "SCENE_READY"
        f" objects={len(bpy.data.objects)}"
        f" materials={len(bpy.data.materials)}"
        f" collections={len(bpy.data.collections)}"
        f" engine={scene.render.engine}"
    )


def main() -> None:
    args = parse_args()
    build()
    scene = bpy.context.scene
    render.setup_render(scene, draft=args.draft, samples=args.samples)

    if args.save:
        render.save_blend(scene, BLEND_PATH)
        print(f"BLEND_SAVED path={BLEND_PATH}")

    if args.test_frame:
        path = SPIKE_DRAFT_PATH if args.draft else SPIKE_PATH
        elapsed = render.render_still(scene, path)
        print(f"SPIKE_DONE seconds={elapsed:.2f} path={path}")


if __name__ == "__main__":
    main()
