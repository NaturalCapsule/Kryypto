from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QSize
from get_style import get_css_style
class ShowLines(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

        self.setObjectName("NumberLines")
        self.setStyleSheet(get_css_style())

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

