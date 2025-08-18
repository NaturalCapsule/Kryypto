from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QHBoxLayout, QGraphicsBlurEffect
)
# from BlurWindow.blurWindow import blur
from PyQt6.QtCore import Qt, QPoint, QTimer
from get_style import get_css_style
from PyQt6.QtGui import QMouseEvent

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setObjectName('TitleBarBG')
        self.setStyleSheet(get_css_style())

        self.bg = QWidget(self)
        self.bg.setStyleSheet(get_css_style())
        self.bg.setObjectName('TitleBarBG')

        self.bg.setGeometry(0, 0, self.width(), self.height())
        self.bg.lower()
        # blur(self.bg.winId(), Dark = True, Acrylic = True)
        # blur(self.winId(), Dark = True, Acrylic = True)


        layout = QHBoxLayout(self)

        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(0)
        
        self.title_label = QLabel("Kryypto")
        self.title_label.setObjectName('TitleBarName')
        self.title_label.setStyleSheet(get_css_style())
        layout.addWidget(self.title_label)
        layout.addStretch()

        self.min_button = QPushButton("—")
        self.min_button.setObjectName('TitleBarMin')

        self.max_button = QPushButton('□')
        self.max_button.setObjectName('TitleBarMax')
        self.max_button.setToolTip('No need to hover over it, you know what this does.')

        self.close_button = QPushButton("X")
        self.close_button.setObjectName('TitleBarClose')
        self.close_button.setToolTip('you gonna close or we gon have a problem?')


        if parent:
            self.min_button.clicked.connect(parent.showMinimized)
            self.max_button.clicked.connect(self.toggle_maximize)
            self.close_button.clicked.connect(parent.close)
        
        for btn in (self.min_button, self.max_button, self.close_button):
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(get_css_style())


        layout.addWidget(self.min_button)
        layout.addWidget(self.max_button)
        layout.addWidget(self.close_button)

        self.start = QPoint(0, 0)
        self.pressing = False

        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_fullscreen)
        self.check_timer.start(100)

        # self.check_fullscreen()

    def check_fullscreen(self):
        if self.parent.isMaximized():
            self.max_button.setText('❐')
        else:
            self.max_button.setText('□')



    def toggle_maximize(self):
        if self.parent:
            if self.parent.isMaximized():
                self.max_button.setText('□')
                self.parent.showNormal()
            else:
                self.parent.showMaximized()
                self.max_button.setText('❐')

    def resizeEvent(self, event):
        self.bg.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start = self.mapToGlobal(event.position().toPoint())
            self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing and self.parent:
            end = self.mapToGlobal(event.position().toPoint())
            movement = end - self.start
            self.parent.move(self.parent.pos() + movement)
            self.start = end

    def mouseReleaseEvent(self, event):
        self.pressing = False


    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.parent:
                if self.parent.isMaximized():
                    self.max_button.setText('□')
                    self.parent.showNormal()
                else:
                    self.parent.showMaximized()
                    self.max_button.setText('❐')

        super().mouseDoubleClickEvent(event)