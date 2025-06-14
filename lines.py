from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QSize

class ShowLines(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

        self.setStyleSheet("""
            QWidget {
                font-family: "Maple-Mono"
            }

""")

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

