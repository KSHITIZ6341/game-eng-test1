from __future__ import annotations
import pyrr
from engine.scripting.node.base import NodeBase

class RotateY(NodeBase):
    """Spin entity around Y; speed modulated by incoming factor or speed input."""

    def __init__(self, node_id: str, params):
        super().__init__(node_id, params)
        self._angle = 0.0

    def process(self, inputs, ctx):
        dt = ctx["dt"]
        base_speed = self.params.get("speed", 6.2832)  # default = 1 rev / sec
        factor = inputs.get("factor", 1.0)              # 0‑to‑1 from Timer/PingPong
        speed_in = inputs.get("speed")                  # direct override, optional

        speed = speed_in if speed_in is not None else base_speed * factor
        self._angle += speed * dt
        ctx["entity"].transform.rotation = pyrr.Quaternion.from_y_rotation(self._angle)  # type: ignore[attr-defined]
        return {}
