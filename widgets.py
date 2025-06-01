from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QTextCursor, QKeyEvent
from PyQt6.QtWidgets import QApplication, QPlainTextEdit, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

central_widget = QWidget()

layout = QVBoxLayout(central_widget)

class MainText(QPlainTextEdit):
    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        text = event.text()
        pairs = {'"': '"', "'": "'", '(': ')', '[': ']', '{': '}'}

        if text in pairs:
            cursor = self.textCursor()
            closing_char = pairs[text]

            cursor.insertText(text + closing_char)

            cursor.movePosition(QTextCursor.MoveOperation.Left)
            self.setTextCursor(cursor)
        else:
            super().keyPressEvent(event)
