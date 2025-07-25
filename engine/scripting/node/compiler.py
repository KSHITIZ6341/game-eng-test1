
from __future__ import annotations
import json, importlib
from pathlib import Path
from typing import Dict, List

from jsonschema import validate
from engine.scripting.node.schema import GRAPH_SCHEMA
from engine.scripting.node.base import NodeBase

class CompiledGraph:
    def __init__(self, nodes: List[NodeBase], links: Dict[str, List[str]]) -> None:
        self.nodes = nodes
        self.links = links  # not used in MVP, but ready for dataflow

    def step(self, ctx) -> None:
        for node in self.nodes:
            node.process(ctx)


def compile_graph(path: Path) -> CompiledGraph:
    raw = json.loads(path.read_text())
    validate(instance=raw, schema=GRAPH_SCHEMA)

    nodes = []
    for n in raw["nodes"]:
        mod_path = f"engine.scripting.node.nodes.utility.rotate_y" if n["type"] == "RotateY" else n["type"]
        cls = importlib.import_module(mod_path).RotateY  # noqa: E402
        nodes.append(cls(n["id"], n["params"]))

    links = {l["src"]: l["dst"] for l in raw.get("links", [])}
    return CompiledGraph(nodes, links)
