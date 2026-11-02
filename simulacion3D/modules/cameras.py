"""Cámaras y luces con orientación declarativa."""

from __future__ import annotations

import math

import bpy


def _link(obj: bpy.types.Object, collection: bpy.types.Collection) -> None:
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)


def add_target(
    name: str,
    location: tuple[float, float, float],
    collection: bpy.types.Collection,
) -> bpy.types.Object:
    target = bpy.data.objects.new(name, None)
    target.location = location
    target.empty_display_size = 0.2
    collection.objects.link(target)
    return target


def add_camera(
    name: str,
    location: tuple[float, float, float],
    target: tuple[float, float, float],
    collection: bpy.types.Collection,
    *,
    lens: float = 35.0,
) -> bpy.types.Object:
    camera_data = bpy.data.cameras.new(name)
    camera_data.lens = lens
    camera_data.clip_start = 0.01
    camera_data.clip_end = 1000.0
    camera = bpy.data.objects.new(name, camera_data)
    collection.objects.link(camera)
    camera.location = location

    target_object = add_target(f"{name}_TARGET", target, collection)
    constraint = camera.constraints.new(type="TRACK_TO")
    constraint.target = target_object
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"
    return camera


def add_area_light(
    name: str,
    location: tuple[float, float, float],
    target: tuple[float, float, float],
    collection: bpy.types.Collection,
    *,
    energy: float = 200.0,
    size: float = 5.0,
    color: tuple[float, float, float] = (0.55, 0.7, 1.0),
) -> bpy.types.Object:
    light_data = bpy.data.lights.new(name, type="AREA")
    light_data.energy = energy
    light_data.shape = "DISK"
    light_data.size = size
    light_data.color = color
    light = bpy.data.objects.new(name, light_data)
    collection.objects.link(light)
    light.location = location

    target_object = add_target(f"{name}_TARGET", target, collection)
    constraint = light.constraints.new(type="TRACK_TO")
    constraint.target = target_object
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"
    return light


def add_sun(
    name: str,
    collection: bpy.types.Collection,
    *,
    energy: float = 3.0,
    angle_deg: float = 3.0,
    rotation_deg: tuple[float, float, float] = (55.0, 0.0, 35.0),
    color: tuple[float, float, float] = (1.0, 0.92, 0.82),
) -> bpy.types.Object:
    light_data = bpy.data.lights.new(name, type="SUN")
    light_data.energy = energy
    light_data.angle = math.radians(angle_deg)
    light_data.color = color
    light = bpy.data.objects.new(name, light_data)
    collection.objects.link(light)
    light.rotation_euler = tuple(math.radians(value) for value in rotation_deg)
    return light
