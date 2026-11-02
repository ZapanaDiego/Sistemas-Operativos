"""Terreno, rocas y cielo de Marte."""

from __future__ import annotations

import math
import random

import bpy
from mathutils import noise

from modules import materials


def terrain_height(x: float, y: float) -> float:
    return (
        1.8 * noise.noise((x * 0.018, y * 0.018, 0.0))
        + 0.7 * noise.noise((x * 0.08, y * 0.08, 2.0))
        + 0.25 * noise.noise((x * 0.3, y * 0.3, 4.0))
    )


def _ground_material() -> bpy.types.Material:
    material = bpy.data.materials.get("MAT_Mars")
    if material is None:
        material = bpy.data.materials.new("MAT_Mars")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    shader = nodes.new("ShaderNodeBsdfPrincipled")
    shader.inputs["Roughness"].default_value = 0.95

    texture = nodes.new("ShaderNodeTexNoise")
    texture.inputs["Scale"].default_value = 0.045
    texture.inputs["Detail"].default_value = 6.0
    texture.inputs["Roughness"].default_value = 0.65

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.25
    ramp.color_ramp.elements[0].color = materials.hex_to_rgba("#6E2A16")
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = materials.hex_to_rgba("#C1440E")

    links = material.node_tree.links
    links.new(texture.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], shader.inputs["Base Color"])
    links.new(shader.outputs["BSDF"], output.inputs["Surface"])
    return material


def build_terrain(collection: bpy.types.Collection, subdivisions: int = 140) -> bpy.types.Object:
    size = 220.0
    step = size / subdivisions
    start = -size / 2.0
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
            faces.append((a, a + 1, a + row + 1, a + row))

    mesh = bpy.data.meshes.new("ENV_Terrain")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    terrain = bpy.data.objects.new("ENV_Terrain", mesh)
    collection.objects.link(terrain)
    terrain.data.materials.append(_ground_material())
    for polygon in terrain.data.polygons:
        polygon.use_smooth = True
    return terrain


def build_rocks(collection: bpy.types.Collection, count: int = 90) -> list[bpy.types.Object]:
    rng = random.Random(42)
    material = materials.make_principled("MAT_Rock", "#4A2318", roughness=0.92)
    rocks: list[bpy.types.Object] = []
    for index in range(count):
        x = rng.uniform(-95.0, 95.0)
        y = rng.uniform(-75.0, 100.0)
        if math.hypot(x + 12.0, y - 8.0) < 8.0:
            continue
        radius = rng.uniform(0.25, 1.9)
        z = terrain_height(x, y)
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=1, radius=radius, location=(x, y, z)
        )
        rock = bpy.context.object
        rock.name = f"ENV_Rock_{index:02d}"
        rock.scale = (1.0, rng.uniform(0.7, 1.3), rng.uniform(0.5, 1.0))
        rock.rotation_euler = (0.0, 0.0, rng.uniform(0.0, math.tau))
        rock.data.materials.append(material)
        for current in list(rock.users_collection):
            current.objects.unlink(rock)
        collection.objects.link(rock)
        rocks.append(rock)
    return rocks


def build_sun_disk(collection: bpy.types.Collection) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=3.2, segments=32, ring_count=16, location=(-58.0, 62.0, 17.0)
    )
    disk = bpy.context.object
    disk.name = "ENV_SunDisk"
    disk.data.materials.append(
        materials.make_emission("MAT_SunDisk", "#FFD9A0", strength=3.0)
    )
    for current in list(disk.users_collection):
        current.objects.unlink(disk)
    collection.objects.link(disk)
    return disk


def build_sky(scene: bpy.types.Scene) -> None:
    world = bpy.data.worlds.get("WORLD_Mars")
    if world is None:
        world = bpy.data.worlds.new("WORLD_Mars")
    background = world.node_tree.nodes.get("Background")
    if background is not None:
        background.inputs["Color"].default_value = (0.16, 0.045, 0.02, 1.0)
        background.inputs["Strength"].default_value = 0.9
    scene.world = world
