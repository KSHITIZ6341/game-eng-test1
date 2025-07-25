# engine/scripting/node/nodes/utility/pingpong.py
from __future__ import annotations
from engine.scripting.node.base import NodeBase

class PingPong(NodeBase):
    """Outputs ramp 0→1→0 with period seconds."""
    def __init__(self, node_id, params):
        super().__init__(node_id, params)
        self._t = 0.0
        self._dir = 1.0  # 1 = up, -1 = down

    def process(self, inputs, ctx):
        dt = ctx["dt"]
        period = self.params.get("period", 4.0)
        step = dt / (period / 2)  # half‑period up, half down

        self._t += step * self._dir
        if self._t >= 1.0:
            self._t = 1.0
            self._dir = -1.0
        elif self._t <= 0.0:
            self._t = 0.0
            self._dir = 1.0

        return {"factor": self._t}
