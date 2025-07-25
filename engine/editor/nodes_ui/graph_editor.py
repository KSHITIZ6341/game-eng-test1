# engine/editor/nodes_ui/graph_editor.py
# Qt graph editor that saves with NodeGraphQt.save_session().

from __future__ import annotations
from pathlib import Path
from NodeGraphQt import BaseNode, NodeGraph
from PySide6 import QtGui, QtWidgets

GRAPH_PATH = Path("assets/graphs/editing.json")

# ----- nodes -------------------------------------------------------------

class RotateYNode(BaseNode):
    __identifier__ = "Utility"
    NODE_NAME = "RotateY"

    def __init__(self):
        super().__init__()
        self.add_input("factor")
        self.add_output("out")
        self.add_double_input("speed", value=6.2832)


class PingPongNode(BaseNode):
    __identifier__ = "Utility"
    NODE_NAME = "PingPong"

    def __init__(self):
        super().__init__()
        self.add_output("factor")
        self.add_double_input("period", value=4.0)


class TimerNode(BaseNode):
    __identifier__ = "Utility"
    NODE_NAME = "Timer"

    def __init__(self):
        super().__init__()
        self.add_output("elapsed")
        self.add_double_input("period", value=2.0)


# ----- editor ------------------------------------------------------------

class GraphEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reaper Engine – Graph Editor")
        self._graph = NodeGraph()
        self._graph.register_node(RotateYNode)
        self._graph.register_node(PingPongNode)
        self._graph.register_node(TimerNode)
        self.setCentralWidget(self._graph.widget)

        for seq in ("Ctrl+S", "Meta+S"):            # Meta = ⌘ on macOS
            QtGui.QShortcut(QtGui.QKeySequence(seq), self).activated.connect(self._save)

        self._load()

    # persistence using built‑ins ----------------------------------------
    def _save(self):
        GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._graph.save_session(GRAPH_PATH.as_posix())

    def _load(self):
        if GRAPH_PATH.exists():
            try:
                self._graph.load_session(GRAPH_PATH.as_posix())
            except Exception:
                pass  # ignore old/corrupt sessions


# ----- entry point -------------------------------------------------------

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = GraphEditor()
    w.resize(960, 640)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
