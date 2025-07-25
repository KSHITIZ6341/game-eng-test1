
from __future__ import annotations
from typing import Any, Dict

class NodeBase:
    def __init__(self, node_id: str, params: Dict[str, Any]) -> None:
        self.id = node_id
        self.params = params

    def process(self, ctx: Dict[str, Any]) -> None:  # ctx = blackboard / world
        raise NotImplementedError
