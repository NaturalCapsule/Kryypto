import ast
import jedi
import re
from PyQt6.QtCore import Qt, QStringListModel, QRect, QSize, Qt, QTimer
from PyQt6.QtGui import QTextCursor, QKeyEvent, QPainter, QTextFormat, QColor, QFont, QFontMetrics, QTextCharFormat, QTextCursor, QColor
from PyQt6.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget, QCompleter

from show_errors import ShowErrors
from lines import ShowLines

central_widget = QWidget()

layout = QVBoxLayout(central_widget)

class MainText(QPlainTextEdit):
    def __init__(self, doc_panel):
        super().__init__()
        self.completer = QCompleter()
        self.doc_panel = doc_panel
        self.class_or_function = {}
        self.cursorPositionChanged.connect(self.update_docstring)

        self.show_erros = ShowErrors(self)
        # self.num_lines_font = None
        # self.painter = QP


        self.line_number_area = ShowLines(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width(0)
        # print(self.painter)
        # self.painter = QPainter(self.line_number_area)
        # self.painter.

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

    def update_docstring(self):
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.positionInBlock()
        code = self.toPlainText()

        doc = self.get_definition_docstring(code, line, column)
        doc = doc or ""
        if doc == "":
            self.doc_panel.hide()
        else:
            self.doc_panel.setPlainText(doc or "")
            self.doc_panel.show()

    def get_definition_docstring(self, code, line, column):
        try:
            script = jedi.Script(code=code, path="example.py")
            definitions = script.help(line, column)
            self.cursorPositionChanged.connect(lambda: self.class_or_func(script, line, column))

            if definitions:
                return definitions[0].docstring()
        except Exception as e:
            return f"Error: {e}"
        return ""

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        text = event.text()
        pairs = {'"': '"', "'": "'", '(': ')', '[': ']', '{': '}'}

        if self.completer.popup().isVisible():
            if key in (Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Tab):
                event.ignore()
                self.insert_completion(self.completer.currentCompletion())
                self.completer.popup().hide()
                return
            elif key == Qt.Key.Key_Escape:
                self.completer.popup().hide()
                return
            
        if text in pairs:
            cursor = self.textCursor()
            closing_char = pairs[text]
            cursor.insertText(text + closing_char)
            cursor.movePosition(QTextCursor.MoveOperation.Left)
            self.setTextCursor(cursor)
            return
        

        # if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
        #     cursor = self.textCursor()
        #     cursor.select(cursor.SelectionType.BlockUnderCursor)
        #     previous_line = cursor.selectedText()

        #     indent_match = re.match(r'^(\s*)', previous_line)
        #     current_indent = indent_match.group(1) if indent_match else ""


        #     if previous_line.strip().endswith(":"):
        #         new_indent = current_indent + " " * 4
        #     else:
        #         new_indent = current_indent

        #     self.insertPlainText(new_indent)

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor = self.textCursor()
            block_text = cursor.block().text()

            # Get current indentation
            indent_match = re.match(r'^(\s*)', block_text)
            current_indent = indent_match.group(1) if indent_match else ""

            if block_text.strip().endswith(":"):
                new_indent = current_indent + " " * 4
            else:
                new_indent = current_indent

            cursor.insertText("\n" + new_indent)
            return  # Skip super()

        super().keyPressEvent(event)





        if not (Qt.Key.Key_A <= key <= Qt.Key.Key_Z or 
                Qt.Key.Key_0 <= key <= Qt.Key.Key_9 or 
                key in (Qt.Key.Key_Period, Qt.Key.Key_Underscore)):
            self.completer.popup().hide()
            return

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

    def class_or_func(self, script, line, column):
        try:
            inferred = script.infer(line, column)

            if inferred:
                # print("--------------------------------")
                # print(inferred[0].name)
                # print(inferred[0].type)
                # print("--------------------------------")
                self.class_or_function[inferred[0].name] = inferred[0].type
                
        except ValueError:
            pass
    
    def cursor_to_line_column(self, pos):
        text = self.toPlainText()
        lines = text[:pos].splitlines()
        line = len(lines) if lines else 1
        column = len(lines[-1]) if lines else 0
        return line, column


    def line_number_area_width(self):
        font_metrics = QFontMetrics(QFont("Maple Mono", 19))
        digits = len(str(self.blockCount()))
        return 3 + font_metrics.horizontalAdvance('9') * digits

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(30, 30, 30))
        
        num_lines_font = QFont("Maple Mono", 19)
        painter.setFont(num_lines_font)
        font_metrics = QFontMetrics(num_lines_font)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(160, 160, 160))
                painter.drawText(
                    0, top, self.line_number_area.width() - 5, font_metrics.height(),
                    Qt.AlignmentFlag.AlignRight, number
                )
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1


    # def schedule_check(self):
    #     self.timer.start(500)

    # def check_syntax(self):
    #     code = self.toPlainText()
    #     self.clear_error_highlighting()
    #     try:
    #         ast.parse(code)
    #         if self.error_label:
    #             self.error_label.setText("✅ No syntax errors")
    #     except SyntaxError as e:
    #         if self.error_label:
    #             self.error_label.setText(f"❌ Line {e.lineno}: {e.msg}")
    #         self.underline_error(e.lineno, e.offset)

    # def clear_error_highlighting(self):
    #     cursor = self.textCursor()
    #     cursor.select(QTextCursor.SelectionType.Document)
    #     fmt = QTextCharFormat()
    #     fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
    #     cursor.setCharFormat(fmt)

    # def underline_error(self, line, column):
    #     cursor = self.textCursor()
    #     cursor.movePosition(QTextCursor.MoveOperation.Start)
    #     for _ in range(line - 1):
    #         cursor.movePosition(QTextCursor.MoveOperation.Down)

    #     cursor.movePosition(QTextCursor.MoveOperation.Right, n=column - 1)
    #     cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)

    #     fmt = QTextCharFormat()
    #     fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
    #     fmt.setUnderlineColor(QColor("red"))
    #     cursor.setCharFormat(fmt)