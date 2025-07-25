from __future__ import annotations

from PySide6 import QtGui, QtWidgets, QtCore
from engine.rendering.backend.wgpu import Renderer


class ViewportWidget(QtWidgets.QWidget):
    """Dockable editor viewport."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_NativeWindow)
        self._renderer = Renderer()

    def showEvent(self, event: QtGui.QShowEvent) -> None:  # noqa: D401
        super().showEvent(event)
        if not hasattr(self, "_started"):
            from engine.core.time import Clock
            from engine.core.ecs import World

            clock, world = Clock(), World()
            self._started = True
            self._renderer.render_loop(clock.tick, world.step)
