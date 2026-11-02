"""Ciudad de tareas, cerrojo, anillos y paneles de código/terminal."""

from __future__ import annotations

import math
from pathlib import Path

import bpy

from modules import materials

ROOT = Path(__file__).resolve().parent.parent
CODE_TEXTURE = ROOT / "assets" / "code" / "code_panel.png"
TERMINAL_OFF = ROOT / "assets" / "code" / "terminal_off.png"
TERMINAL_ON = ROOT / "assets" / "code" / "terminal_on.png"

CITY_X = 0.0
CITY_Y = 22.0
CITY_Z = 9.0


def _cylinder(
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
        vertices=24, radius=radius, depth=depth, location=location, rotation=rotation
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def _torus(
    name: str,
    location: tuple[float, float, float],
    major: float,
    minor: float,
    material: bpy.types.Material,
    collection: bpy.types.Collection,
    *,
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=minor,
        location=location,
        rotation=rotation,
        major_segments=48,
        minor_segments=12,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def _sphere(
    name: str,
    location: tuple[float, float, float],
    radius: float,
    material: bpy.types.Material,
    collection: bpy.types.Collection,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius, segments=24, ring_count=12, location=location
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def _plane_with_texture(
    name: str,
    location: tuple[float, float, float],
    size: tuple[float, float],
    image_path: Path,
    collection: bpy.types.Collection,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_plane_add(
        size=1.0, location=location, rotation=(math.pi / 2.0, 0.0, 0.0)
    )
    plane = bpy.context.object
    plane.name = name
    plane.scale = (size[0], size[1], 1.0)

    material = bpy.data.materials.new(f"MAT_{name}")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    texture = nodes.new("ShaderNodeTexImage")
    image = bpy.data.images.load(str(image_path), check_existing=True)
    image.colorspace_settings.name = "sRGB"
    texture.image = image
    texture.interpolation = "Linear"
    emission.inputs["Strength"].default_value = 1.2
    material.node_tree.links.new(texture.outputs["Color"], emission.inputs["Color"])
    material.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    plane.data.materials.append(material)
    for current in list(plane.users_collection):
        current.objects.unlink(plane)
    collection.objects.link(plane)
    return plane


def _add_frame(
    name: str,
    center: tuple[float, float, float],
    size: tuple[float, float],
    material: bpy.types.Material,
    collection: bpy.types.Collection,
) -> list[bpy.types.Object]:
    x, y, z = center
    width, height = size
    thickness = 0.035
    bars = [
        (x, y - 0.01, z + height / 2.0, width, thickness, thickness),
        (x, y - 0.01, z - height / 2.0, width, thickness, thickness),
        (x - width / 2.0, y - 0.01, z, thickness, thickness, height),
        (x + width / 2.0, y - 0.01, z, thickness, thickness, height),
    ]
    objects = []
    for index, (bx, by, bz, sx, sy, sz) in enumerate(bars):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, bz))
        bar = bpy.context.object
        bar.name = f"{name}_{index}"
        bar.scale = (sx, sy, sz)
        bar.data.materials.append(material)
        for current in list(bar.users_collection):
            current.objects.unlink(bar)
        collection.objects.link(bar)
        objects.append(bar)
    return objects


def build_city(collection: bpy.types.Collection) -> dict[str, object]:
    platform = _cylinder(
        "TASK_Platform",
        (CITY_X, CITY_Y, CITY_Z - 0.12),
        7.0,
        0.24,
        materials.make_principled("MAT_CityBase", "#0B1118", roughness=0.45, metallic=0.5),
        collection,
    )
    platform.scale = (1.0, 0.65, 1.0)
    platform_rim = _torus(
        "TASK_PlatformRim",
        (CITY_X, CITY_Y, CITY_Z - 0.12),
        7.0,
        0.04,
        materials.make_emission("MAT_PlatformRim", "#FFB300", strength=1.5),
        collection,
    )
    platform_rim.scale = (1.0, 0.65, 1.0)

    definitions = (
        ("bc_sched", -5.0, 12.0, "#FFFFFF", 5.0),
        ("bc_dist", -2.5, 7.0, "#FF3B30", 5.5),
        ("med_1", 0.0, 4.5, "#FF9500", 4.0),
        ("med_2", 1.8, 4.5, "#FF9500", 4.0),
        ("med_3", 3.6, 4.5, "#FF9500", 4.0),
        ("asi_met", 5.5, 2.5, "#0A84FF", 5.0),
    )
    threads: dict[str, bpy.types.Object] = {}
    orbs: dict[str, bpy.types.Object] = {}
    for role, x, height, color, strength in definitions:
        material = materials.make_emission(f"MAT_{role}", color, strength=strength)
        thread = _cylinder(
            f"TASK_{role.upper()}",
            (CITY_X + x, CITY_Y, CITY_Z + height / 2.0),
            0.12,
            height,
            material,
            collection,
        )
        threads[role] = thread
        orbs[role] = _sphere(
            f"TASK_{role.upper()}_Orb",
            (CITY_X + x, CITY_Y, CITY_Z + height),
            0.18,
            material,
            collection,
        )

    lock = _torus(
        "FX_Lock",
        (CITY_X + 2.2, CITY_Y - 2.0, CITY_Z + 1.2),
        0.8,
        0.12,
        materials.make_emission("MAT_Lock", "#FFB300", strength=6.0),
        collection,
    )
    lock_eye = _sphere(
        "FX_LockEye",
        (CITY_X + 2.2, CITY_Y - 2.0, CITY_Z + 1.2),
        0.22,
        materials.make_emission("MAT_LockEye", "#FFD36A", strength=5.0),
        collection,
    )

    deadline = _torus(
        "FX_Deadline",
        (CITY_X - 2.5, CITY_Y, CITY_Z + 4.8),
        1.05,
        0.07,
        materials.make_emission("MAT_Deadline", "#FF3B30", strength=4.0),
        collection,
    )
    watchdog = _torus(
        "FX_Watchdog",
        (CITY_X - 5.0, CITY_Y, CITY_Z + 12.4),
        0.95,
        0.07,
        materials.make_emission("MAT_Watchdog", "#FFFFFF", strength=4.5),
        collection,
    )

    bus = _cylinder(
        "TASK_Bus1553",
        (CITY_X, CITY_Y + 2.4, CITY_Z + 0.25),
        0.06,
        16.0,
        materials.make_emission("MAT_CityBus", "#FFB000", strength=3.0),
        collection,
        rotation=(0.0, math.pi / 2.0, 0.0),
    )
    packets: list[bpy.types.Object] = []
    packet_material = materials.make_emission("MAT_CityPacket", "#FFE08A", strength=6.0)
    for index in range(9):
        packets.append(
            _sphere(
                f"FX_CityPacket_{index}",
                (CITY_X - 8.0 + index * 2.0, CITY_Y + 2.4, CITY_Z + 0.25),
                0.07,
                packet_material,
                collection,
            )
        )

    return {
        "platform": platform,
        "platform_rim": platform_rim,
        "threads": threads,
        "orbs": orbs,
        "lock": lock,
        "lock_eye": lock_eye,
        "deadline": deadline,
        "watchdog": watchdog,
        "bus": bus,
        "packets": packets,
        "location": (CITY_X, CITY_Y, CITY_Z),
    }


def build_panels(collection: bpy.types.Collection) -> dict[str, object]:
    center = (0.0, 300.0, 0.0)
    code = _plane_with_texture(
        "FX_CodePanel", center, (8.0, 4.5), CODE_TEXTURE, collection
    )
    terminal_off = _plane_with_texture(
        "FX_TerminalOff", (0.0, 300.02, 0.0), (8.0, 4.5), TERMINAL_OFF, collection
    )
    terminal_on = _plane_with_texture(
        "FX_TerminalOn", (0.0, 300.04, 0.0), (8.0, 4.5), TERMINAL_ON, collection
    )
    backdrop = _plane_with_texture(
        "FX_CodeBackdrop",
        (0.0, 303.0, 0.0),
        (26.0, 15.0),
        CODE_TEXTURE,
        collection,
    )
    backdrop.data.materials.clear()
    backdrop.data.materials.append(
        materials.make_emission("MAT_CodeBackdrop", "#05070A", strength=0.0)
    )
    frame_material = materials.make_emission("MAT_CodeFrame", "#FFB000", strength=3.0)
    frame = _add_frame("FX_CodeFrame", center, (8.2, 4.7), frame_material, collection)
    return {
        "code": code,
        "terminal_off": terminal_off,
        "terminal_on": terminal_on,
        "backdrop": backdrop,
        "frame": frame,
        "center": center,
    }
