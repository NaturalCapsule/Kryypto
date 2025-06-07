import ast
from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat, QTextCursor, QColor
from PyQt6.QtCore import QTimer

class ShowErrors:
    def __init__(self, parent):
        # self.textChanged.connect(self.schedule_check)
        parent.textChanged.connect(self.schedule_check)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.check_syntax)
        self.error_label = None
        self.parent = parent

    def schedule_check(self):
            self.timer.start(500)

    def check_syntax(self):
        # code = self.toPlainText()
        code = self.parent.toPlainText()

        self.clear_error_highlighting()
        try:
            ast.parse(code)
            if self.error_label:
                self.error_label.setText("✅ No syntax errors")
        except SyntaxError as e:
            if self.error_label:
                self.error_label.setText(f"❌ Line {e.lineno}: {e.msg}")
            self.underline_error(e.lineno, e.offset)

    def clear_error_highlighting(self):
        # cursor = self.textCursor()
        cursor = self.parent.textCursor()

        cursor.select(QTextCursor.SelectionType.Document)
        fmt = QTextCharFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
        cursor.setCharFormat(fmt)

    def underline_error(self, line, column):
        # cursor = self.textCursor()
        cursor = self.parent.textCursor()

        cursor.movePosition(QTextCursor.MoveOperation.Start)
        for _ in range(line - 1):
            cursor.movePosition(QTextCursor.MoveOperation.Down)

        cursor.movePosition(QTextCursor.MoveOperation.Right, n=column - 1)
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)

        fmt = QTextCharFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
        fmt.setUnderlineColor(QColor("red"))
        cursor.setCharFormat(fmt)