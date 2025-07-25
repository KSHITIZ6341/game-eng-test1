
from __future__ import annotations

import sys
from PySide6 import QtWidgets
from engine.editor.viewport.opengl_view import ViewportWidget


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    viewport = ViewportWidget()
    viewport.resize(1280, 720)
    viewport.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
