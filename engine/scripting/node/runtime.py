
from __future__ import annotations
from pathlib import Path
import time

from engine.scripting.node.compiler import compile_graph, CompiledGraph

class GraphRuntime:
    def __init__(self, graph_file: Path) -> None:
        self._file = graph_file
        self._mtime = 0.0
        self._graph: CompiledGraph | None = None
        self._load()

    def _load(self) -> None:
        self._graph = compile_graph(self._file)
        self._mtime = self._file.stat().st_mtime

    def step(self, ctx) -> None:
        if self._file.stat().st_mtime > self._mtime:
            self._load()
        if self._graph:
            self._graph.step(ctx)

