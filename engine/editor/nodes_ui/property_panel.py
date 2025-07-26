from __future__ import annotations
from PySide6 import QtWidgets, QtCore


def _inputs(node):
    if hasattr(node, "input_sockets"):
        return node.input_sockets()
    return node.input_ports()


class PropertyPanel(QtWidgets.QDockWidget):
    """Inspector showing a spin‑box + slider for numeric inputs."""

    def __init__(self, parent=None):
        super().__init__("Node Properties", parent)
        self._form = QtWidgets.QFormLayout()
        wrap = QtWidgets.QWidget(); wrap.setLayout(self._form)
        self.setWidget(wrap); self.setMinimumWidth(220)
        self._node = None

    def _row(self, name: str, getter, setter, rng=(-1000.0, 1000.0)):
        lo = QtWidgets.QHBoxLayout()
        spin = QtWidgets.QDoubleSpinBox(); spin.setDecimals(3)
        spin.setRange(*rng); spin.setValue(getter()); lo.addWidget(spin)

        sld = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sld.setRange(int(rng[0]*100), int(rng[1]*100))
        sld.setValue(int(getter()*100)); lo.addWidget(sld)

        # sync
        spin.valueChanged.connect(lambda v: (sld.setValue(int(v*100)), setter(v)))
        sld.valueChanged.connect(lambda iv: (spin.setValue(iv/100),   setter(iv/100)))

        w = QtWidgets.QWidget(); w.setLayout(lo)
        self._form.addRow(name, w)

    def inspect(self, node):
        self._node = node
        while self._form.rowCount():
            self._form.removeRow(0)

        if not node:
            return

        for sock in _inputs(node):
            if sock.name() in ("speed", "period", "value"):
                getter = lambda n=node, nm=sock.name(): float(getattr(n, nm, 0.0))
                setter = lambda v, n=node, nm=sock.name(): setattr(n, nm, v)
                self._row(sock.name(), getter, setter)


def _input_iter():
    return None