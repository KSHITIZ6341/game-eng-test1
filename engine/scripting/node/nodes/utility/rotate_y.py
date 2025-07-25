from __future__ import annotations

import pyrr
from engine.scripting.node.base import NodeBase


class RotateY(NodeBase):

    def __init__(self, node_id: str, params):
        super().__init__(node_id, params)
        self._angle = 0.0  # accumulated radians

    def process(self, ctx):
        dt = ctx["dt"]
        ent = ctx["entity"]
        speed = self.params.get("speed", 1.5708)  # default = π/2 rad/s
        self._angle += speed * dt
        ent.transform.rotation = pyrr.Quaternion.from_y_rotation(self._angle)  # type: ignore[attr-defined]
