from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont, QFontMetrics
from get_style import get_css_style

class ShowLines(QWidget):
    def __init__(self, editor, font_size):
        super().__init__(editor)
        self.editor = editor

        self.setObjectName("NumberLines")
        self.setStyleSheet(get_css_style())
        font_ = QFont("Maple Mono", font_size)

        self.setFont(font_)

        self.font_metrics = QFontMetrics(font_)

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(self.font_metrics), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event, self.font_metrics)
