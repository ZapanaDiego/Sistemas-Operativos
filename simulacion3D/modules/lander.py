"""Lander exterior, chasis VME, CPU y bus 1553."""

from __future__ import annotations

import math

import bpy

from modules import materials
from modules.terrain import terrain_height


def _cube(
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
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


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
        vertices=20,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def build_lander(collection: bpy.types.Collection) -> dict[str, object]:
    x, y = -12.0, 8.0
    z = terrain_height(x, y)
    metal = materials.make_principled(
        "MAT_Metal", "#B0B0B0", roughness=0.35, metallic=0.75
    )
    dark_metal = materials.make_principled(
        "MAT_DarkMetal", "#4A4F57", roughness=0.5, metallic=0.6
    )
    panel = materials.make_principled(
        "MAT_Panel",
        "#16233B",
        roughness=0.35,
        metallic=0.35,
        emission_color="#0A84FF",
        emission_strength=0.5,
    )
    blanket = materials.make_principled(
        "MAT_Blanket", "#D4A017", roughness=0.65, metallic=0.25
    )

    exterior: list[bpy.types.Object] = []
    exterior.append(
        _cube("LANDER_Body", (x, y, z + 0.8), (3.0, 2.0, 1.2), metal, collection)
    )
    exterior.append(
        _cube("LANDER_Blanket", (x, y - 1.01, z + 0.8), (2.6, 0.04, 1.0), blanket, collection)
    )
    for side, dx in (("L", -2.55), ("R", 2.55)):
        exterior.append(
            _cube(
                f"LANDER_Panel_{side}",
                (x + dx, y, z + 1.28),
                (2.2, 1.7, 0.06),
                panel,
                collection,
            )
        )
    exterior.append(
        _cylinder("LANDER_Mast", (x - 0.9, y, z + 2.5), 0.06, 2.8, metal, collection)
    )
    exterior.append(
        _cube("LANDER_Camera", (x - 0.9, y, z + 3.9), (0.22, 0.22, 0.22), metal, collection)
    )
    exterior.append(
        _cylinder(
            "LANDER_Antenna",
            (x + 1.35, y, z + 2.4),
            0.035,
            1.7,
            metal,
            collection,
            rotation=(0.15, 0.0, 0.0),
        )
    )
    for index, (dx, dy) in enumerate(((-1.1, -0.7), (-1.1, 0.7), (1.1, -0.7), (1.1, 0.7))):
        exterior.append(
            _cylinder(
                f"LANDER_Leg_{index}",
                (x + dx, y + dy, z + 0.25),
                0.05,
                0.6,
                dark_metal,
                collection,
                rotation=(math.radians(10.0), 0.0, 0.0),
            )
        )

    interior: list[bpy.types.Object] = []
    chassis = _cube(
        "LANDER_Chassis",
        (x, y, z + 1.1),
        (3.3, 2.2, 1.7),
        materials.make_principled(
            "MAT_ChassisFrame",
            "#2A6B8A",
            roughness=0.4,
            metallic=0.4,
            emission_color="#0A84FF",
            emission_strength=0.7,
        ),
        collection,
    )
    wireframe = chassis.modifiers.new("Wireframe", "WIREFRAME")
    wireframe.thickness = 0.035
    wireframe.use_replace = True
    interior.append(chassis)
    interior.append(
        _cube("LANDER_Backplane", (x, y, z + 1.1), (2.9, 0.12, 1.4), dark_metal, collection)
    )
    board_material = materials.make_principled(
        "MAT_Board",
        "#0E3B2E",
        roughness=0.4,
        metallic=0.3,
        emission_color="#33FF77",
        emission_strength=0.25,
    )
    for index, dx in enumerate((-1.0, 0.0, 1.0)):
        interior.append(
            _cube(
                f"LANDER_Board_{index}",
                (x + dx, y, z + 1.15),
                (0.08, 1.65, 0.95),
                board_material,
                collection,
            )
        )
    cpu = _cube(
        "LANDER_CPU",
        (x, y - 0.25, z + 1.55),
        (0.55, 0.55, 0.14),
        materials.make_principled(
            "MAT_CPU",
            "#1A1A1A",
            roughness=0.3,
            metallic=0.8,
            emission_color="#FFB300",
            emission_strength=2.0,
        ),
        collection,
    )
    interior.append(cpu)
    bus = _cylinder(
        "LANDER_Bus1553",
        (x, y - 0.2, z + 1.95),
        0.035,
        2.7,
        materials.make_emission("MAT_Bus1553", "#FFB000", strength=4.0),
        collection,
        rotation=(0.0, math.pi / 2.0, 0.0),
    )
    interior.append(bus)

    packets: list[bpy.types.Object] = []
    packet_material = materials.make_emission("MAT_BusPacket", "#FFD36A", strength=6.0)
    for index in range(7):
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.055, segments=12, ring_count=8, location=(x - 1.3 + index * 0.4, y - 0.2, z + 1.95)
        )
        packet = bpy.context.object
        packet.name = f"FX_BusPacket_{index}"
        packet.data.materials.append(packet_material)
        for current in list(packet.users_collection):
            current.objects.unlink(packet)
        collection.objects.link(packet)
        packets.append(packet)

    return {
        "exterior": exterior,
        "interior": interior,
        "cpu": cpu,
        "bus": bus,
        "packets": packets,
        "location": (x, y, z),
    }
