from __future__ import annotations
from typing import Dict, Any

class NodeBase:
    """Abstract data‑flow node."""
    def __init__(self, node_id: str, params: Dict[str, Any]) -> None:
        self.id = node_id
        self.params = params

    def process(self, inputs: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
        """Return a dict of output pin → value."""
        raise NotImplementedError
