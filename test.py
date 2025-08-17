from PyQt6.QtWidgets import QDockWidget, QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
import sys

class AnimatedPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.button = QPushButton("Toggle Panel")
        layout.addWidget(self.button)

        # This will act like our dock widget
        self.panel = QDockWidget("Panel Content")
        # self.panel = QTextEdit("Panel Content")

        layout.addWidget(self.panel)

        self.panel.setMaximumHeight(0)

        self.button.clicked.connect(self.togglePanel)
        self.anim = None

    def togglePanel(self):
        if self.panel.maximumHeight() == 0:
            self.animatePanel(show=True)
        else:
            self.animatePanel(show=False)

    def animatePanel(self, show=True):
        start_height = self.panel.maximumHeight()
        end_height = 150 if show else 0

        self.anim = QPropertyAnimation(self.panel, b"maximumHeight")
        self.anim.setDuration(300)
        self.anim.setStartValue(start_height)
        self.anim.setEndValue(end_height)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AnimatedPanel()
    w.resize(400, 300)
    w.show()
    sys.exit(app.exec())