"""Paleta y materiales base del film.

Los colores son los del contrato §5.1. Las funciones devuelven materiales
nuevos o reutilizan uno existente con el mismo nombre para que la escena sea
idempotente.
"""

from __future__ import annotations

import bpy

PALETTE = {
    "bc_sched": "#FFFFFF",
    "bc_dist": "#FF3B30",
    "med": "#FF9500",
    "asi_met": "#0A84FF",
    "mutex": "#FFB300",
    "deadline": "#FF3B30",
    "deadline_ok": "#34C759",
    "pip": "#34C759",
    "mars_dark": "#8B3A1E",
    "mars_mid": "#C1440E",
    "mars_light": "#E27D60",
    "metal": "#B0B0B0",
    "blanket": "#D4A017",
    "terminal_bg": "#0B0F14",
    "terminal_amber": "#FFB000",
    "terminal_green": "#33FF77",
}


def srgb_to_linear(value: float) -> float:
    if value <= 0.04045:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> tuple[float, float, float, float]:
    value = hex_color.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"color hex inválido: {hex_color}")
    rgb = [int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return (
        srgb_to_linear(rgb[0]),
        srgb_to_linear(rgb[1]),
        srgb_to_linear(rgb[2]),
        alpha,
    )


def make_principled(
    name: str,
    base_color: str,
    *,
    roughness: float = 0.6,
    metallic: float = 0.0,
    emission_color: str | None = None,
    emission_strength: float = 0.0,
) -> bpy.types.Material:
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    shader = nodes.new("ShaderNodeBsdfPrincipled")
    shader.inputs["Base Color"].default_value = hex_to_rgba(base_color)
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Metallic"].default_value = metallic
    if emission_color is not None:
        shader.inputs["Emission Color"].default_value = hex_to_rgba(emission_color)
        shader.inputs["Emission Strength"].default_value = emission_strength
    material.node_tree.links.new(shader.outputs["BSDF"], output.inputs["Surface"])
    return material


def make_emission(
    name: str,
    color: str,
    *,
    strength: float = 4.0,
) -> bpy.types.Material:
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = hex_to_rgba(color)
    emission.inputs["Strength"].default_value = strength
    material.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return material
