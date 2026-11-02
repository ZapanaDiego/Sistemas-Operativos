#!/usr/bin/env python3
"""Construye la escena completa del film de Mars Pathfinder.

Un solo escena maestra contiene los 15 planos. Los marcadores de la línea de
tiempo cambian de cámara al inicio de cada plano; la visibilidad de los mundos
(Marte, interior, ciudad, código) se anima con ``hide_render``.

Uso:
    blender -b --factory-startup --python build_scene.py -- --save
    blender -b --factory-startup --python build_scene.py -- --test-frame --frame 1
    blender -b --factory-startup --python build_scene.py -- --preview
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules import cameras, lander, materials, render, rover, tasks, terrain

BLEND_PATH = ROOT / "blender" / "pathfinder_failure.blend"
FRAMES_DIR = ROOT / "out" / "frames" / "film"
PREVIEW_DIR = ROOT / "out" / "preview"
TEST_PATH = ROOT / "out" / "spike" / "film_test.png"

FPS = 24
SHOTS = (
    ("shot_01", 1, 288),
    ("shot_02", 289, 600),
    ("shot_03", 601, 912),
    ("shot_04", 913, 1248),
    ("shot_05", 1249, 1560),
    ("shot_06", 1561, 1872),
    ("shot_07", 1873, 2208),
    ("shot_08", 2209, 2520),
    ("shot_09", 2521, 2832),
    ("shot_10", 2833, 3072),
    ("shot_11", 3073, 3360),
    ("shot_12", 3361, 3600),
    ("shot_13", 3601, 3840),
    ("shot_14", 3841, 4080),
    ("shot_15", 4081, 4320),
)

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
    parser = argparse.ArgumentParser(description="Escena completa del film")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--test-frame", action="store_true")
    parser.add_argument("--frame", type=int, default=1)
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--samples", type=int, default=None)
    parser.add_argument("--no-motion-blur", action="store_true")
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


def add_lights(collections: dict[str, bpy.types.Collection]) -> list[bpy.types.Object]:
    lights: list[bpy.types.Object] = []
    lights.append(
        cameras.add_sun(
            "LIGHT_Sun",
            collections["06_LIGHTS"],
            energy=4.5,
            angle_deg=2.0,
            rotation_deg=(62.0, 0.0, 25.0),
            color=(1.0, 0.88, 0.74),
        )
    )
    lights.append(
        cameras.add_area_light(
            "LIGHT_Fill",
            (-26.0, -30.0, 22.0),
            (-12.0, 8.0, 2.0),
            collections["06_LIGHTS"],
            energy=900.0,
            size=18.0,
            color=(0.45, 0.62, 1.0),
        )
    )

    interior = bpy.data.lights.new("LIGHT_Interior", type="AREA")
    interior.energy = 90.0
    interior.shape = "DISK"
    interior.size = 2.0
    interior.color = (0.55, 0.8, 1.0)
    interior_obj = bpy.data.objects.new("LIGHT_Interior", interior)
    collections["06_LIGHTS"].objects.link(interior_obj)
    interior_obj.location = (-12.0, 6.0, 3.2)
    target = bpy.data.objects.new("LIGHT_Interior_TARGET", None)
    collections["06_LIGHTS"].objects.link(target)
    target.location = (-12.0, 8.0, 1.5)
    constraint = interior_obj.constraints.new(type="TRACK_TO")
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"
    lights.append(interior_obj)

    city = bpy.data.lights.new("LIGHT_City", type="POINT")
    city.energy = 500.0
    city.shadow_soft_size = 4.0
    city.color = (1.0, 0.55, 0.25)
    city_obj = bpy.data.objects.new("LIGHT_City", city)
    collections["06_LIGHTS"].objects.link(city_obj)
    city_obj.location = (0.0, 22.0, 11.0)
    lights.append(city_obj)
    return lights


def add_camera(
    name: str,
    keys: list[tuple[int, tuple[float, float, float], tuple[float, float, float], float]],
    collection: bpy.types.Collection,
) -> bpy.types.Object:
    _, location, target_location, lens = keys[0]
    camera = cameras.add_camera(name, location, target_location, collection, lens=lens)
    target = bpy.data.objects[f"{name}_TARGET"]
    for frame, loc, target_loc, focal in keys:
        camera.location = loc
        camera.data.lens = focal
        target.location = target_loc
        camera.keyframe_insert(data_path="location", frame=frame)
        camera.data.keyframe_insert(data_path="lens", frame=frame)
        target.keyframe_insert(data_path="location", frame=frame)
    return camera


def add_cameras(collections: dict[str, bpy.types.Collection]) -> dict[str, bpy.types.Object]:
    definitions = {
        "shot_01": [
            (1, (0.0, -16.0, 6.0), (-12.0, 8.0, 2.5), 35.0),
            (288, (8.0, -13.0, 5.0), (-12.0, 8.0, 2.5), 35.0),
        ],
        "shot_02": [
            (289, (-10.0, 4.4, 3.6), (-12.9, 8.0, 3.2), 60.0),
            (600, (-10.6, 5.1, 3.8), (-12.9, 8.0, 3.4), 70.0),
        ],
        "shot_03": [
            (601, (2.0, -14.0, 6.0), (-12.0, 8.0, 2.0), 35.0),
            (912, (-16.0, -2.0, 4.5), (-12.0, 8.0, 2.0), 35.0),
        ],
        "shot_04": [
            (913, (-4.0, 0.0, 4.0), (-12.0, 8.0, 1.2), 40.0),
            (1248, (-6.0, 12.0, 4.0), (-12.0, 8.0, 1.2), 45.0),
        ],
        "shot_05": [
            (1249, (-10.0, 0.0, 5.0), (-12.0, 8.0, 3.0), 35.0),
            (1560, (0.0, -2.0, 13.0), (0.0, 22.0, 12.0), 35.0),
        ],
        "shot_06": [
            (1561, (2.2, 10.5, 12.5), (2.2, 20.0, 10.2), 45.0),
            (1872, (2.2, 12.5, 12.0), (2.2, 20.0, 10.2), 50.0),
        ],
        "shot_07": [
            (1873, (0.0, 5.0, 10.0), (2.0, 22.0, 10.0), 35.0),
            (2208, (4.0, 5.0, 10.0), (2.0, 22.0, 10.0), 35.0),
        ],
        "shot_08": [
            (2209, (0.0, 10.0, 8.0), (0.0, 20.0, 9.2), 50.0),
            (2520, (2.0, 12.0, 8.5), (2.0, 20.0, 9.2), 50.0),
        ],
        "shot_09": [
            (2521, (-2.5, 14.0, 12.0), (-2.5, 22.0, 13.8), 85.0),
            (2832, (-2.5, 2.0, 12.0), (-2.5, 22.0, 13.8), 50.0),
        ],
        "shot_10": [
            (2833, (0.0, -8.0, 14.0), (0.0, 22.0, 12.0), 24.0),
            (3072, (0.0, -8.0, 14.0), (0.0, 22.0, 12.0), 24.0),
        ],
        "shot_11": [
            (3073, (0.0, 291.0, 0.0), (0.0, 300.0, 0.0), 35.0),
            (3360, (0.0, 294.0, 0.0), (0.0, 300.0, 0.0), 40.0),
        ],
        "shot_12": [
            (3361, (0.0, 292.0, 0.0), (0.0, 300.0, 0.0), 35.0),
            (3600, (0.0, 293.0, 0.0), (0.0, 300.0, 0.0), 35.0),
        ],
        "shot_13": [
            (3601, (0.0, 2.0, 11.0), (2.0, 22.0, 10.0), 35.0),
            (3840, (4.0, 2.0, 11.0), (2.0, 22.0, 10.0), 40.0),
        ],
        "shot_14": [
            (3841, (0.0, -5.0, 13.0), (0.0, 22.0, 10.0), 30.0),
            (4080, (0.0, -15.0, 14.0), (0.0, 22.0, 10.0), 24.0),
        ],
        "shot_15": [
            (4081, (0.0, -16.0, 6.0), (-12.0, 8.0, 2.0), 35.0),
            (4320, (6.0, -20.0, 10.0), (-12.0, 8.0, 2.0), 28.0),
        ],
    }
    result: dict[str, bpy.types.Object] = {}
    for name, keys in definitions.items():
        result[name] = add_camera(f"CAM_{name}", keys, collections["05_CAMERAS"])
    return result


def set_visibility(objects: list[bpy.types.Object], ranges: list[tuple[int, int]]) -> None:
    for obj in objects:
        if not ranges:
            obj.hide_render = True
            obj.keyframe_insert(data_path="hide_render", frame=1)
            continue
        for start, end in ranges:
            if start > 1:
                obj.hide_render = True
                obj.keyframe_insert(data_path="hide_render", frame=start - 1)
            obj.hide_render = False
            obj.keyframe_insert(data_path="hide_render", frame=start)
            obj.hide_render = True
            obj.keyframe_insert(data_path="hide_render", frame=end + 1)


def add_markers(
    scene: bpy.types.Scene, cameras_map: dict[str, bpy.types.Object]
) -> None:
    scene.timeline_markers.clear()
    for name, start, _ in SHOTS:
        marker = scene.timeline_markers.new(name, frame=start)
        marker.camera = cameras_map[name]
    scene.camera = cameras_map["shot_01"]


def animate_data_pulses(collections: dict[str, bpy.types.Collection]) -> list[bpy.types.Object]:
    material = materials.make_emission("MAT_DataPulse", "#0A84FF", strength=7.0)
    pulses: list[bpy.types.Object] = []
    z0 = terrain.terrain_height(-12.9, 8.0)
    for index in range(6):
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.08, segments=16, ring_count=8, location=(-12.9, 8.0, z0 + 3.8)
        )
        pulse = bpy.context.object
        pulse.name = f"FX_DataPulse_{index}"
        pulse.data.materials.append(material)
        for current in list(pulse.users_collection):
            current.objects.unlink(pulse)
        collections["04_FX"].objects.link(pulse)
        start = 289 + index * 42
        pulse.location = (-12.9, 8.0, z0 + 3.8)
        pulse.keyframe_insert(data_path="location", frame=start)
        pulse.location = (-12.1, 8.0, z0 + 1.1)
        pulse.keyframe_insert(data_path="location", frame=start + 48)
        pulses.append(pulse)
    return pulses


def animate_bus_packets(lander_data: dict[str, object]) -> None:
    packets = lander_data["packets"]
    for index, packet in enumerate(packets):
        start_x = -13.3 + index * 0.1
        phase = index * 7
        for frame in range(913 + phase, 1561, 49):
            packet.location.x = start_x
            packet.keyframe_insert(data_path="location", frame=frame)
            packet.location.x = -10.7
            packet.keyframe_insert(data_path="location", frame=frame + 24)


def animate_city_packets(city: dict[str, object]) -> None:
    packets = city["packets"]
    for index, packet in enumerate(packets):
        phase = index * 6
        for frame in range(1300 + phase, 4081, 61):
            packet.location.x = -8.0
            packet.keyframe_insert(data_path="location", frame=frame)
            packet.location.x = 8.0
            packet.keyframe_insert(data_path="location", frame=frame + 36)


def _emission_input(obj: bpy.types.Object):
    material = obj.data.materials[0]
    for node in material.node_tree.nodes:
        if node.type == "EMISSION":
            return node.inputs["Color"], node.inputs["Strength"]
    return None, None


def animate_threads(city: dict[str, object]) -> None:
    threads = city["threads"]
    orbs = city["orbs"]
    blue = threads["asi_met"]
    blue_orb = orbs["asi_met"]
    blue_color, blue_strength = _emission_input(blue)
    base_blue_z = blue.location.z
    base_orb_z = blue_orb.location.z

    # La tarea azul es empujada hacia abajo en el plano 7.
    blue.location.z = base_blue_z
    blue.keyframe_insert(data_path="location", frame=1873)
    blue.location.z = base_blue_z - 1.1
    blue.keyframe_insert(data_path="location", frame=2208)
    blue_orb.location.z = base_orb_z
    blue_orb.keyframe_insert(data_path="location", frame=1873)
    blue_orb.location.z = base_orb_z - 1.4
    blue_orb.keyframe_insert(data_path="location", frame=2208)

    # En el plano 13 hereda la prioridad: sube por encima de las naranjas.
    blue.location.z = base_blue_z - 1.1
    blue.keyframe_insert(data_path="location", frame=3601)
    blue.location.z = base_blue_z + 2.8
    blue.keyframe_insert(data_path="location", frame=3660)
    blue.keyframe_insert(data_path="location", frame=3840)
    blue_orb.location.z = base_orb_z - 1.4
    blue_orb.keyframe_insert(data_path="location", frame=3601)
    blue_orb.location.z = base_orb_z + 5.6
    blue_orb.keyframe_insert(data_path="location", frame=3660)
    blue_orb.keyframe_insert(data_path="location", frame=3840)
    if blue_color is not None:
        blue_color.default_value = materials.hex_to_rgba("#0A84FF")
        blue_color.keyframe_insert(data_path="default_value", frame=3601)
        blue_color.default_value = materials.hex_to_rgba("#34C759")
        blue_color.keyframe_insert(data_path="default_value", frame=3660)
    if blue_strength is not None:
        blue_strength.default_value = 5.0
        blue_strength.keyframe_insert(data_path="default_value", frame=3601)
        blue_strength.default_value = 8.0
        blue_strength.keyframe_insert(data_path="default_value", frame=3660)

    # Las tareas medias suben en el plano 7 y se estabilizan.
    for role in ("med_1", "med_2", "med_3"):
        thread = threads[role]
        orb = orbs[role]
        base_z = thread.location.z
        base_orb = orb.location.z
        thread.location.z = base_z
        thread.keyframe_insert(data_path="location", frame=1873)
        thread.location.z = base_z + 0.7
        thread.keyframe_insert(data_path="location", frame=2208)
        orb.location.z = base_orb
        orb.keyframe_insert(data_path="location", frame=1873)
        orb.location.z = base_orb + 0.9
        orb.keyframe_insert(data_path="location", frame=2208)

    # El rojo baja al cerrojo en el plano 8.
    red = threads["bc_dist"]
    red_orb = orbs["bc_dist"]
    red_base = red.location.z
    red_orb_base = red_orb.location.z
    red.location.z = red_base
    red.keyframe_insert(data_path="location", frame=2209)
    red.location.z = red_base - 1.5
    red.keyframe_insert(data_path="location", frame=2400)
    red_orb.location.z = red_orb_base
    red_orb.keyframe_insert(data_path="location", frame=2209)
    red_orb.location.z = red_orb_base - 1.5
    red_orb.keyframe_insert(data_path="location", frame=2400)


def animate_lock_and_rings(city: dict[str, object]) -> None:
    lock = city["lock"]
    lock_eye = city["lock_eye"]
    deadline = city["deadline"]
    watchdog = city["watchdog"]

    # Cerrojo: se cierra en el plano 6 y se abre en el 13.
    lock.scale = (1.0, 1.0, 1.0)
    lock.keyframe_insert(data_path="scale", frame=1561)
    lock.scale = (1.12, 1.12, 1.12)
    lock.keyframe_insert(data_path="scale", frame=1872)
    lock.scale = (1.22, 1.22, 1.22)
    lock.keyframe_insert(data_path="scale", frame=2209)
    lock.scale = (1.22, 1.22, 1.22)
    lock.keyframe_insert(data_path="scale", frame=3601)
    lock.scale = (0.62, 0.62, 0.62)
    lock.keyframe_insert(data_path="scale", frame=3660)
    lock.rotation_euler.z = 0.0
    lock.keyframe_insert(data_path="rotation_euler", frame=3601)
    lock.rotation_euler.z = math.pi
    lock.keyframe_insert(data_path="rotation_euler", frame=3660)
    lock_eye.scale = (1.0, 1.0, 1.0)
    lock_eye.keyframe_insert(data_path="scale", frame=3601)
    lock_eye.scale = (0.3, 0.3, 0.3)
    lock_eye.keyframe_insert(data_path="scale", frame=3660)

    # Deadline: se llena en el plano 9 y se vuelve verde en el 14.
    deadline.scale = (1.0, 1.0, 1.0)
    deadline.keyframe_insert(data_path="scale", frame=2521)
    deadline.scale = (1.28, 1.28, 1.28)
    deadline.keyframe_insert(data_path="scale", frame=2832)
    deadline_color, deadline_strength = _emission_input(deadline)
    if deadline_color is not None:
        deadline_color.default_value = materials.hex_to_rgba("#FF3B30")
        deadline_color.keyframe_insert(data_path="default_value", frame=3841)
        deadline_color.default_value = materials.hex_to_rgba("#34C759")
        deadline_color.keyframe_insert(data_path="default_value", frame=3900)
    if deadline_strength is not None:
        deadline_strength.default_value = 4.0
        deadline_strength.keyframe_insert(data_path="default_value", frame=3841)
        deadline_strength.default_value = 6.5
        deadline_strength.keyframe_insert(data_path="default_value", frame=3900)

    # Watchdog: pulsa y se pone rojo en el plano 10.
    watchdog_color, watchdog_strength = _emission_input(watchdog)
    watchdog.scale = (1.0, 1.0, 1.0)
    watchdog.keyframe_insert(data_path="scale", frame=2833)
    watchdog.scale = (1.35, 1.35, 1.35)
    watchdog.keyframe_insert(data_path="scale", frame=2900)
    watchdog.scale = (1.0, 1.0, 1.0)
    watchdog.keyframe_insert(data_path="scale", frame=2960)
    watchdog.scale = (1.35, 1.35, 1.35)
    watchdog.keyframe_insert(data_path="scale", frame=3020)
    if watchdog_color is not None:
        watchdog_color.default_value = materials.hex_to_rgba("#FFFFFF")
        watchdog_color.keyframe_insert(data_path="default_value", frame=2833)
        watchdog_color.default_value = materials.hex_to_rgba("#FF3B30")
        watchdog_color.keyframe_insert(data_path="default_value", frame=2880)
        watchdog_color.default_value = materials.hex_to_rgba("#FFFFFF")
        watchdog_color.keyframe_insert(data_path="default_value", frame=2920)
        watchdog_color.default_value = materials.hex_to_rgba("#FF3B30")
        watchdog_color.keyframe_insert(data_path="default_value", frame=3000)
        watchdog_color.default_value = materials.hex_to_rgba("#FFFFFF")
        watchdog_color.keyframe_insert(data_path="default_value", frame=3841)
        watchdog_color.default_value = materials.hex_to_rgba("#34C759")
        watchdog_color.keyframe_insert(data_path="default_value", frame=3900)
    watchdog.scale = (1.0, 1.0, 1.0)
    watchdog.keyframe_insert(data_path="scale", frame=3841)


def add_shockwaves(collections: dict[str, bpy.types.Collection]) -> list[bpy.types.Object]:
    material = materials.make_emission("MAT_Shockwave", "#FFFFFF", strength=4.0)
    waves: list[bpy.types.Object] = []
    for index, start in enumerate((2860, 2940, 3020)):
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.5,
            minor_radius=0.05,
            location=(0.0, 22.0, 10.0),
            major_segments=64,
            minor_segments=8,
        )
        wave = bpy.context.object
        wave.name = f"FX_Shockwave_{index}"
        wave.data.materials.append(material)
        for current in list(wave.users_collection):
            current.objects.unlink(wave)
        collections["04_FX"].objects.link(wave)
        wave.scale = (0.1, 0.1, 0.1)
        wave.keyframe_insert(data_path="scale", frame=start)
        wave.scale = (16.0, 16.0, 1.0)
        wave.keyframe_insert(data_path="scale", frame=start + 30)
        waves.append(wave)
    return waves


def add_scanline(collections: dict[str, bpy.types.Collection]) -> bpy.types.Object:
    material = materials.make_emission("MAT_Scanline", "#FFB000", strength=5.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 299.9, 0.0))
    line = bpy.context.object
    line.name = "FX_CodeScanline"
    line.scale = (8.0, 0.02, 0.04)
    line.data.materials.append(material)
    for current in list(line.users_collection):
        current.objects.unlink(line)
    collections["04_FX"].objects.link(line)
    line.location.z = -2.2
    line.keyframe_insert(data_path="location", frame=3073)
    line.location.z = 2.2
    line.keyframe_insert(data_path="location", frame=3360)
    return line


def add_camera_shake(camera: bpy.types.Object) -> None:
    base = (0.0, -8.0, 14.0)
    offsets = (
        (2860, (0.12, 0.05, 0.10)),
        (2880, (-0.15, -0.04, -0.08)),
        (2900, (0.10, 0.06, 0.12)),
        (2920, (-0.08, 0.03, -0.10)),
        (2940, (0.16, -0.05, 0.06)),
        (2960, (-0.12, 0.04, 0.09)),
        (2980, (0.09, -0.03, -0.07)),
        (3000, (-0.14, 0.05, 0.11)),
        (3020, (0.11, -0.04, -0.09)),
        (3040, (-0.07, 0.03, 0.06)),
    )
    for frame, (dx, dy, dz) in offsets:
        camera.location = (base[0] + dx, base[1] + dy, base[2] + dz)
        camera.keyframe_insert(data_path="location", frame=frame)


def build() -> dict[str, object]:
    reset_scene()
    collections = ensure_collections()
    scene = bpy.context.scene
    terrain.build_sky(scene)

    env: list[bpy.types.Object] = []
    env.append(terrain.build_terrain(collections["00_ENV"]))
    env.extend(terrain.build_rocks(collections["00_ENV"]))
    env.append(terrain.build_sun_disk(collections["00_ENV"]))

    lander_data = lander.build_lander(collections["01_LANDER"])
    for obj in [*lander_data["interior"], *lander_data["packets"]]:
        obj.location.z += 0.3
    rover_objects = rover.build_rover(collections["02_ROVER"])
    city = tasks.build_city(collections["03_TASKS"])
    panels = tasks.build_panels(collections["04_FX"])

    lights = add_lights(collections)
    cameras_map = add_cameras(collections)
    add_markers(scene, cameras_map)

    data_pulses = animate_data_pulses(collections)
    animate_bus_packets(lander_data)
    animate_city_packets(city)
    animate_threads(city)
    animate_lock_and_rings(city)
    shockwaves = add_shockwaves(collections)
    scanline = add_scanline(collections)
    add_camera_shake(cameras_map["shot_10"])

    # Visibilidad de los mundos.
    set_visibility(env, [(1, 912), (4081, 4320)])
    set_visibility(rover_objects, [(1, 912), (4081, 4320)])
    set_visibility(list(lander_data["exterior"]), [(1, 759), (4081, 4320)])
    set_visibility(list(lander_data["interior"]), [(760, 1560)])
    set_visibility([lander_data["cpu"]], [(760, 1560)])
    set_visibility([lander_data["bus"]], [(760, 1560)])
    set_visibility(list(lander_data["packets"]), [(913, 1560)])
    set_visibility(data_pulses, [(289, 600)])
    set_visibility(
        [
            city["platform"],
            city["platform_rim"],
            city["lock"],
            city["lock_eye"],
            city["deadline"],
            city["watchdog"],
            city["bus"],
            *city["threads"].values(),
            *city["orbs"].values(),
            *city["packets"],
        ],
        [(1300, 3072), (3601, 4080)],
    )
    set_visibility([panels["code"], *panels["frame"]], [(3073, 3360)])
    set_visibility([panels["terminal_off"]], [(3361, 3500)])
    set_visibility([panels["terminal_on"]], [(3501, 3600)])
    set_visibility([panels["backdrop"]], [(3073, 3600)])
    set_visibility([scanline], [(3073, 3360)])
    set_visibility(shockwaves, [(2833, 3072)])
    set_visibility([lights[2]], [(760, 1560)])
    set_visibility([lights[3]], [(1300, 3072), (3601, 4080)])

    scene.frame_start = 1
    scene.frame_end = 4320
    scene.render.fps = FPS
    scene.render.fps_base = 1.0
    scene.render.filepath = str(FRAMES_DIR / "frame_")

    return {
        "collections": collections,
        "cameras": cameras_map,
        "lander": lander_data,
        "city": city,
        "panels": panels,
        "lights": lights,
        "env": env,
        "rover": rover_objects,
        "data_pulses": data_pulses,
        "shockwaves": shockwaves,
    }


PREVIEW_FRAMES = (1, 289, 601, 760, 913, 1249, 1561, 1873, 2209, 2521, 2833, 3073, 3361, 3501, 3601, 3841, 4081, 4320)


def preview(scene: bpy.types.Scene) -> None:
    scene.render.resolution_percentage = 100
    scene.render.resolution_x = 480
    scene.render.resolution_y = 270
    scene.eevee.taa_render_samples = 4
    scene.render.use_motion_blur = False
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for frame in PREVIEW_FRAMES:
        scene.frame_set(frame)
        scene.render.filepath = str(PREVIEW_DIR / f"frame_{frame:04d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"PREVIEW_FRAME {frame}")


def main() -> None:
    args = parse_args()
    build()
    scene = bpy.context.scene
    render.setup_render(
        scene,
        draft=args.draft,
        samples=args.samples,
        motion_blur=not args.no_motion_blur,
    )
    scene.frame_start = 1
    scene.frame_end = 4320
    scene.render.fps = FPS
    scene.render.fps_base = 1.0
    scene.render.filepath = str(FRAMES_DIR / "frame_")

    if args.save:
        render.save_blend(scene, BLEND_PATH)
        print(f"BLEND_SAVED path={BLEND_PATH}")
    if args.preview:
        preview(scene)
        print(f"PREVIEW_DONE path={PREVIEW_DIR}")
    if args.test_frame:
        scene.frame_set(args.frame)
        scene.render.filepath = str(TEST_PATH)
        bpy.ops.render.render(write_still=True)
        print(f"TEST_FRAME frame={args.frame} path={TEST_PATH}")


if __name__ == "__main__":
    main()
