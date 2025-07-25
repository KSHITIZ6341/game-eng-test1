"""Simple scene graph with local/global transform propagation."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
import pyrr


@dataclass(slots=True)
class Transform:
    position: pyrr.Vector3 = field(default_factory=lambda: pyrr.Vector3([0, 0, 0]))
    rotation: pyrr.Quaternion = field(default_factory=lambda: pyrr.Quaternion())
    scale: pyrr.Vector3 = field(default_factory=lambda: pyrr.Vector3([1, 1, 1]))

    def matrix(self) -> pyrr.Matrix44:
        m = pyrr.matrix44.create_from_scale(self.scale)
        m = pyrr.matrix44.multiply(m, self.rotation.matrix44)
        m = pyrr.matrix44.multiply(m, pyrr.matrix44.create_from_translation(self.position))
        return m


class Node:
    __slots__ = ("name", "transform", "children", "drawable")

    def __init__(self, name: str, transform: Transform | None = None) -> None:
        self.name = name
        self.transform = transform or Transform()
        self.children: List["Node"] = []
        self.drawable = None  # Mesh | Light | Camera

    def add(self, child: "Node") -> None:
        self.children.append(child)

    def traverse(self, parent_m: pyrr.Matrix44 | None = None):
        model_m = (
            pyrr.matrix44.multiply(self.transform.matrix(), parent_m)
            if parent_m is not None
            else self.transform.matrix()
        )
        if self.drawable:
            yield self, model_m
        for c in self.children:
            yield from c.traverse(model_m)
