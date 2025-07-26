# fallback‑aware palette helper
from __future__ import annotations
from NodeGraphQt import NodeGraph

def create_palette(graph: NodeGraph, title: str = "Node Palette"):
    """Return a QDockWidget with the node palette, or None if not supported."""
    try:
        # modern NodeGraphQt
        from NodeGraphQt.widgets.nodes_tree import NodeTreeWidget
        from PySide6.QtWidgets import QDockWidget

        tree = NodeTreeWidget(graph)
        dock = QDockWidget(title)
        dock.setWidget(tree)
        return dock

    except ImportError:
        # very old NodeGraphQt build – no palette available
        return None
