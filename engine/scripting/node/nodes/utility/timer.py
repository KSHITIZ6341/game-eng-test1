from __future__ import annotations
from engine.scripting.node.base import NodeBase

class Timer(NodeBase):
    """Outputs a ramp from 0 to period then resets."""
    def __init__(self, node_id, params):
        super().__init__(node_id, params)
        self._t = 0.0

    def process(self, inputs, ctx):
        dt = ctx["dt"]
        period = self.params.get("period", 2.0)
        self._t = (self._t + dt) % period
        return {"elapsed": self._t / period}
