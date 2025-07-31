from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QHBoxLayout, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QPoint
import sys
from get_style import get_css_style

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.parent = parent

        self.bg = QWidget(self)
        # self.bg.setStyleSheet("background-color: rgba(30, 30, 30, 200); border-radius: 0px;")
        self.bg.setStyleSheet(get_css_style())
        self.bg.setObjectName('TitleBarBG')

        self.bg.setGeometry(0, 0, self.width(), self.height())
        self.bg.lower()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(0)

        self.title_label = QLabel("My App")
        self.title_label.setStyleSheet(get_css_style())
        self.title_label.setObjectName('TitleBarName')
        layout.addWidget(self.title_label)
        layout.addStretch()

        self.min_button = QPushButton("—")
        self.min_button.setStyleSheet(get_css_style())
        self.min_button.clicked.connect(self.toggle_minimize)

        self.min_button.setObjectName('TitleBarMin')

        self.max_button = QPushButton("□")
        self.max_button.clicked.connect(self.toggle_maximize)
        self.max_button.setStyleSheet(get_css_style())
        self.max_button.setObjectName('TitleBarMax')


        self.close_button = QPushButton("X")
        self.close_button.clicked.connect(self.exit_)
        self.close_button.setStyleSheet(get_css_style())
        self.close_button.setObjectName('TitleBarClose')

        for btn in (self.min_button, self.max_button, self.close_button):
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("color: white; background-color: transparent; border: none;")

        layout.addWidget(self.min_button)
        layout.addWidget(self.max_button)
        layout.addWidget(self.close_button)

        self.start = QPoint(0, 0)
        self.pressing = False


    def exit_(self):
        sys.exit()

    def resizeEvent(self, event):
        self.bg.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)


    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def toggle_minimize(self):
        self.parent.showMinimized()

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.position().toPoint())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.position().toPoint())
            self.movement = self.end - self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                  self.mapToGlobal(self.movement).y(),
                                  self.parent.width(),
                                  self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, event):
        self.pressing = False