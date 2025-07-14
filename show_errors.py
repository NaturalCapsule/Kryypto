import ast
from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat, QTextCursor, QColor
from PyQt6.QtCore import QTimer

from func_classes import list_classes_functions
import json, commentjson
from lark.exceptions import UnexpectedCharacters, UnexpectedToken
from threading import Thread

class ShowErrors:
    def __init__(self, parent, highlighter):
        parent.textChanged.connect(self.schedule_check)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.check_syntax)
        self.error_label = None
        self.parent = parent
        self.highlighter = highlighter

    def schedule_check(self):
            self.timer.start(500)

    def check_syntax(self):
        code = self.parent.toPlainText()


        self.clear_error_highlighting()
        try:
            ast.parse(code)
            if self.error_label:
                self.error_label.setText("✅ No syntax errors")

            # self.analyze_code(self.parent)
            Thread(target = lambda: self.analyze_code(self.parent), daemon = False).start()


        except (SyntaxError, NameError) as e:
            if self.error_label:
                self.error_label.setText(f"❌ Line {e.lineno}: {e.msg}")

            self.underline_error(e.lineno, e.offset)

    def clear_error_highlighting(self):
        cursor = self.parent.textCursor()

        cursor.select(QTextCursor.SelectionType.Document)
        fmt = QTextCharFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
        cursor.setCharFormat(fmt)

    def underline_error(self, line, column):
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

    def analyze_code(self, main_text):
        code = main_text.toPlainText()
        self.highlighter.set_code(code)

        instances = list_classes_functions(code)
        self.highlighter.get_calls(instances)

        self.highlighter.rehighlight()


class ShowJsonErrors:
    def __init__(self, parent, highlighter, file_path, use_jsonc):
        parent.textChanged.connect(self.schedule_check)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.check_syntax)
        self.error_label = None
        self.parent = parent
        self.highlighter = highlighter
        self.file_path = file_path
        self.use_jsonc = use_jsonc
        self.count_json = 0
        self.count_jsonc = 0

    def schedule_check(self):
            self.timer.start(500)

    def check_syntax(self):
        self.clear_error_highlighting()
        if not self.use_jsonc:
            try:
                with open(fr'{self.file_path}', 'r', encoding = 'utf-8') as file:
                    self.count_json += 1
                    if self.count_json == 1:
                            if len(file.read()) == 0:
                                self.parent.setPlainText('{\n    \n}')
                    json.load(file)
                    self.old_file = file.read()
                if self.error_label:
                    self.error_label.setText("✅ No syntax errors")

                file.close()

                Thread(target = lambda: self.analyze_code(self.parent), daemon = False).start()


            except json.JSONDecodeError as e:
                if self.error_label:
                    self.error_label.setText(f"❌ Line {e.lineno}: {e.msg}")

                self.underline_error(e.lineno, e.colno)
        else:
            try:
                with open(fr'{self.file_path}', 'r', encoding='utf-8') as file:
                    self.count_jsonc += 1
                    content = file.read()
                    if self.count_json == 1:
                        if len(content) == 0:
                            self.parent.setPlainText("{    \n}")
                    
                    data = commentjson.loads(content)

                if self.error_label:
                    self.error_label.setText("✅ No syntax errors")

                Thread(target=lambda: self.analyze_code(self.parent), daemon=False).start()

            except (UnexpectedToken, ValueError) as e:
                if self.error_label:
                    self.error_label.setText(f"❌ Error: {str(e)}")


    def clear_error_highlighting(self):
        cursor = self.parent.textCursor()

        cursor.select(QTextCursor.SelectionType.Document)
        fmt = QTextCharFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
        cursor.setCharFormat(fmt)

    def underline_error(self, line, column):

        cursor = self.parent.textCursor()

        cursor.movePosition(QTextCursor.MoveOperation.Start)
        if line <=3:
            for _ in range(line - 1):
                cursor.movePosition(QTextCursor.MoveOperation.Down)

        elif line <= 11 and line >=3:         
            for _ in range(line + 3):
                cursor.movePosition(QTextCursor.MoveOperation.Down)


        else:

            for _ in range(line + 5):
                cursor.movePosition(QTextCursor.MoveOperation.Down)

        cursor.movePosition(QTextCursor.MoveOperation.Right, n=column - 1)

        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)

        fmt = QTextCharFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
        fmt.setUnderlineColor(QColor("red"))
        cursor.setCharFormat(fmt)

    def analyze_code(self, main_text):
        self.highlighter.rehighlight()