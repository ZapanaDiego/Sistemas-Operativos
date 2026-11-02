"""Rover de contexto."""

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
        vertices=16, radius=radius, depth=depth, location=location, rotation=rotation
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def build_rover(
    collection: bpy.types.Collection,
    location: tuple[float, float] = (-4.0, -1.0),
) -> list[bpy.types.Object]:
    x, y = location
    z = terrain_height(x, y)
    metal = materials.make_principled(
        "MAT_RoverMetal", "#C0C0C0", roughness=0.4, metallic=0.7
    )
    dark = materials.make_principled(
        "MAT_RoverDark", "#3A3F46", roughness=0.6, metallic=0.5
    )
    panel = materials.make_principled(
        "MAT_RoverPanel",
        "#16233B",
        roughness=0.35,
        metallic=0.35,
        emission_color="#0A84FF",
        emission_strength=0.6,
    )

    objects: list[bpy.types.Object] = []
    objects.append(_cube("ROVER_Body", (x, y, z + 0.32), (0.75, 0.55, 0.3), metal, collection))
    objects.append(_cube("ROVER_Panel", (x, y, z + 0.53), (0.85, 0.6, 0.045), panel, collection))
    objects.append(_cube("ROVER_Head", (x + 0.05, y - 0.18, z + 0.72), (0.22, 0.22, 0.2), metal, collection))
    objects.append(
        _cylinder(
            "ROVER_Mast",
            (x + 0.05, y - 0.18, z + 0.9),
            0.022,
            0.35,
            metal,
            collection,
        )
    )
    for index, (dx, dy) in enumerate(
        ((-0.28, -0.3), (-0.28, 0.3), (0.0, -0.3), (0.0, 0.3), (0.28, -0.3), (0.28, 0.3))
    ):
        objects.append(
            _cylinder(
                f"ROVER_Wheel_{index}",
                (x + dx, y + dy, z + 0.1),
                0.13,
                0.08,
                dark,
                collection,
                rotation=(0.0, math.pi / 2.0, 0.0),
            )
        )
    return objects
