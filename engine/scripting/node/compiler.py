from __future__ import annotations
import importlib, json
from pathlib import Path
from typing import Dict, List, Tuple
from jsonschema import validate
from engine.scripting.node.schema import GRAPH_SCHEMA
from engine.scripting.node.base import NodeBase

def _topo_sort(nodes: List[str], edges: List[Tuple[str, str]]) -> List[str]:
    from collections import defaultdict, deque
    adj = defaultdict(list); indeg = {n: 0 for n in nodes}
    for a, b in edges:
        adj[a].append(b); indeg[b] += 1
    q = deque([n for n in nodes if indeg[n] == 0]); out = []
    while q:
        n = q.popleft(); out.append(n)
        for m in adj[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                q.append(m)
    if len(out) != len(nodes):
        raise ValueError("Cycle detected in node graph")
    return out

class CompiledGraph:
    def __init__(self, ordered_nodes: List[NodeBase], links_map: Dict[str, List[str]]):
        self._nodes = ordered_nodes
        self._links = links_map  # srcPin -> [dstPin]

    def step(self, ctx):
        pin_values: Dict[str, any] = {}
        for node in self._nodes:
            # collect inputs
            inputs = {
                pin.split(".")[1]: pin_values.get(src_pin)
                for src_pin, dsts in self._links.items()
                for dst_pin in dsts
                if dst_pin.startswith(f"{node.id}.") and (pin := dst_pin).split(".")[1]
            }
            outs = node.process(inputs, ctx)
            for pin, val in outs.items():
                pin_values[f"{node.id}.{pin}"] = val

def compile_graph(path: Path) -> CompiledGraph:
    raw = json.loads(path.read_text())
    validate(instance=raw, schema=GRAPH_SCHEMA)

    # instantiate nodes
    node_lookup: Dict[str, NodeBase] = {}
    for nd in raw["nodes"]:
        mod = nd["type"]
        if mod == "RotateY":
            modpath = "engine.scripting.node.nodes.utility.rotate_y"
            cls = importlib.import_module(modpath).RotateY
        elif mod == "Timer":
            modpath = "engine.scripting.node.nodes.utility.timer"
            cls = importlib.import_module(modpath).Timer
        elif mod == "PingPong":
            modpath = "engine.scripting.node.nodes.utility.pingpong"
            cls = importlib.import_module(modpath).PingPong
        else:
            raise ValueError(f"Unknown node type {mod}")
        node_lookup[nd["id"]] = cls(nd["id"], nd["params"])

    # edges for topo sort (src node -> dst node)
    edges = [(l["src"].split(".")[0], l["dst"].split(".")[0]) for l in raw["links"]]
    order = _topo_sort(list(node_lookup.keys()), edges)
    ordered_nodes = [node_lookup[nid] for nid in order]

    # map srcPin -> [dstPin]
    link_map: Dict[str, List[str]] = {}
    for l in raw["links"]:
        link_map.setdefault(l["src"], []).append(l["dst"])

    return CompiledGraph(ordered_nodes, link_map)
