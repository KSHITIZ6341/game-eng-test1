

from __future__ import annotations

import json
from pathlib import Path

from NodeGraphQt import BaseNode, NodeGraph
from PySide6 import QtGui, QtWidgets

GRAPH_PATH = Path("assets/graphs/editing.json")  # runtime watches this


# ---------- node definitions ---------------------------------------------

class RotateYNode(BaseNode):
    __identifier__ = "Utility"
    NODE_NAME = "RotateY"

    def __init__(self):
        super().__init__()
        self.add_input("factor")            # modulates speed
        self.add_output("out")
        self.add_double_input("speed", value=6.2832)

    def params_dict(self) -> dict:
        return {"speed": self.input(1).value()}


class PingPongNode(BaseNode):
    __identifier__ = "Utility"
    NODE_NAME = "PingPong"

    def __init__(self):
        super().__init__()
        self.add_output("factor")
        self.add_double_input("period", value=4.0)

    def params_dict(self) -> dict:
        return {"period": self.input(0).value()}


class TimerNode(BaseNode):
    __identifier__ = "Utility"
    NODE_NAME = "Timer"

    def __init__(self):
        super().__init__()
        self.add_output("elapsed")
        self.add_double_input("period", value=2.0)

    def params_dict(self) -> dict:
        return {"period": self.input(0).value()}


# ---------- editor window -------------------------------------------------

class GraphEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reaper Engine – Graph Editor")
        self._graph = NodeGraph()
        self._register_nodes()
        self.setCentralWidget(self._graph.widget)
        self._install_shortcut()           # add Ctrl+S handler
        self._load()                       # load existing session

    def _register_nodes(self):
        self._graph.register_node(RotateYNode)
        self._graph.register_node(PingPongNode)
        self._graph.register_node(TimerNode)

    # ---- persistence -----------------------------------------------------

    def _save(self):
        data = {"version": "1.0", "nodes": [], "links": []}
        for n in self._graph.all_nodes():
            data["nodes"].append(
                {
                    "id": n.id,
                    "type": n.NODE_NAME,
                    "params": n.params_dict(),
                    "inputs": [s.name() for s in n.input_sockets()],
                    "outputs": [s.name() for s in n.output_sockets()],
                }
            )
        for c in self._graph.connections():
            src = f"{c['out_socket'].node().id}.{c['out_socket'].name()}"
            dst = f"{c['in_socket'].node().id}.{c['in_socket'].name()}"
            data["links"].append({"src": src, "dst": dst})

        GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
        GRAPH_PATH.write_text(json.dumps(data, indent=2))

    def _load(self):
        if GRAPH_PATH.exists():
            try:
                self._graph.clear_session()
                self._graph.load_session(GRAPH_PATH.as_posix())
            except Exception:
                pass  # ignore bad or old file

    # ---- key handling ----------------------------------------------------

    def _install_shortcut(self):
        orig = self._graph.widget.keyPressEvent

        def handler(event: QtGui.QKeyEvent):
            if event.modifiers() & QtGui.Qt.ControlModifier and event.key() == QtGui.Qt.Key_S:
                self._save()
            else:
                orig(event)

        self._graph.widget.keyPressEvent = handler  # type: ignore[method-assign]


# ---------- entry point ---------------------------------------------------

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = GraphEditor()
    win.resize(960, 640)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
