from PyQt6.QtCore import QSize, Qt, QStringListModel, QObject, QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor, QKeyEvent
from PyQt6.QtWidgets import QPlainTextEdit, QPushButton, QLabel, QVBoxLayout, QWidget, QCompleter
import jedi

central_widget = QWidget()

layout = QVBoxLayout(central_widget)

class MainText(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.completer = QCompleter()
        popup = self.completer.popup()
        popup.setStyleSheet("""
            QListView {
                background-color: #1e1e1e;
                color: #ffffff;
                font-size: 14px;
                selection-background-color: #007acc;
                selection-color: white;
                border: 1px solid #444;
                padding: 2px;
            }
        """)

        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.activated.connect(self.insert_completion)

    def insert_completion(self, completion):
        cursor = self.textCursor()
        cursor.select(cursor.SelectionType.WordUnderCursor)
        cursor.removeSelectedText()
        cursor.insertText(completion)
        self.setTextCursor(cursor)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        text = event.text()
        pairs = {'"': '"', "'": "'", '(': ')', '[': ']', '{': '}'}

        # Handle autocompletion commit
        if self.completer.popup().isVisible() and key in (
            Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Tab
        ):
            self.insert_completion(self.completer.currentCompletion())
            self.completer.popup().hide()
            return

        # Handle auto-pairing of brackets/quotes
        if text in pairs:
            cursor = self.textCursor()
            closing_char = pairs[text]
            cursor.insertText(text + closing_char)
            cursor.movePosition(QTextCursor.MoveOperation.Left)
            self.setTextCursor(cursor)
            return

        super().keyPressEvent(event)

        typing_keys = (
            Qt.Key.Key_A, Qt.Key.Key_Z,
            Qt.Key.Key_0, Qt.Key.Key_9,
            Qt.Key.Key_Period, Qt.Key.Key_Underscore,
        )
        if not (Qt.Key.Key_A <= key <= Qt.Key.Key_Z or 
                Qt.Key.Key_0 <= key <= Qt.Key.Key_9 or 
                key in (Qt.Key.Key_Period, Qt.Key.Key_Underscore)):
            self.completer.popup().hide()
            return

        # Autocompletion logic
        code = self.toPlainText()
        cursor = self.textCursor()
        pos = cursor.position()

        try:
            line, column = self.cursor_to_line_column(pos)
            script = jedi.Script(code=code, path="example.py")
            completions = script.complete(line, column)
            words = [c.name for c in completions][:30]

            if words:
                cursor.select(cursor.SelectionType.WordUnderCursor)
                prefix = cursor.selectedText()
                model = QStringListModel(words)
                self.completer.setModel(model)
                self.completer.setCompletionPrefix(prefix)
                cr = self.cursorRect()
                cr.setWidth(self.completer.popup().sizeHintForColumn(0) + 10)
                self.completer.complete(cr)
            else:
                self.completer.popup().hide()
        except Exception as e:
            print("Autocomplete error:", e)
            self.completer.popup().hide()

    # def keyPressEvent(self, event: QKeyEvent):
    #     key = event.key()
    #     text = event.text()
    #     pairs = {'"': '"', "'": "'", '(': ')', '[': ']', '{': '}'}

    #     if self.completer.popup().isVisible() and key in (
    #         Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Tab
    #     ):
    #         event.ignore()
    #         return

    #     if text in pairs:
    #         cursor = self.textCursor()
    #         closing_char = pairs[text]
    #         cursor.insertText(text + closing_char)
    #         cursor.movePosition(QTextCursor.MoveOperation.Left)
    #         self.setTextCursor(cursor)
    #         return

    #     super().keyPressEvent(event)

    #     code = self.toPlainText()
    #     cursor = self.textCursor()
    #     pos = cursor.position()

    #     try:
    #         line, column = self.cursor_to_line_column(pos)
    #         script = jedi.Script(code=code, path="example.py")
    #         completions = script.complete(line, column)
    #         words = [c.name for c in completions][:30]

    #         if words:
    #             cursor.select(cursor.SelectionType.WordUnderCursor)
    #             prefix = cursor.selectedText()
    #             model = QStringListModel(words)
    #             self.completer.setModel(model)
    #             self.completer.setCompletionPrefix(prefix)
    #             cr = self.cursorRect()
    #             cr.setWidth(self.completer.popup().sizeHintForColumn(0) + 10)
    #             self.completer.complete(cr)
    #     except Exception as e:
    #         print("Autocomplete error:", e)


    def cursor_to_line_column(self, pos):
        text = self.toPlainText()
        lines = text[:pos].splitlines()
        line = len(lines) if lines else 1
        column = len(lines[-1]) if lines else 0
        return line, column