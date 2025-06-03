import sys
import jedi
from PyQt6.QtWidgets import QApplication, QPlainTextEdit, QCompleter, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QStringListModel

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.completer = QCompleter()
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

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        code = self.toPlainText()
        cursor = self.textCursor()
        pos = cursor.position()

        try:
            line, column = self.cursor_to_line_column(pos)
            script = jedi.Script(code=code, path="example.py")
            completions = script.complete(line, column)
            words = [c.name for c in completions]

            if words:
                cursor.select(cursor.SelectionType.WordUnderCursor)
                prefix = cursor.selectedText()
                model = QStringListModel(words)
                self.completer.setModel(model)
                self.completer.setCompletionPrefix(prefix)
                cr = self.cursorRect()
                cr.setWidth(self.completer.popup().sizeHintForColumn(0) + 10)
                self.completer.complete(cr)
        except Exception as e:
            print("Autocomplete error:", e)

    def cursor_to_line_column(self, pos):
        text = self.toPlainText()
        lines = text[:pos].splitlines()
        line = len(lines) if lines else 1
        column = len(lines[-1]) if lines else 0
        return line, column

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.editor = CodeEditor()
        layout.addWidget(self.editor)
        self.setLayout(layout)
        self.setWindowTitle("Python IDE with Jedi Autocompletion")

app = QApplication(sys.argv)
window = MainWindow()
window.resize(800, 600)
window.show()
sys.exit(app.exec())
