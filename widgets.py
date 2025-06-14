import jedi
import re
import os
from PyQt6.QtCore import Qt, QStringListModel, QRect, Qt, QDir
from PyQt6.QtGui import QTextCursor, QKeyEvent, QPainter, QColor, QFont, QFontMetrics, QTextCursor, QColor, QFileSystemModel
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QInputDialog, QPlainTextEdit, QVBoxLayout, QWidget, QCompleter, QDockWidget, QTextEdit, QTreeView

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


        # self.show_erros = ShowErrors(self)
        self.line_number_area = ShowLines(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width(0)

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

        if key == Qt.Key.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText(" " * 3)

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor = self.textCursor()
            block_text = cursor.block().text()

            indent_match = re.match(r'^(\s*)', block_text)
            current_indent = indent_match.group(1) if indent_match else ""

            if block_text.strip().endswith(":"):
                new_indent = current_indent + " " * 4
            else:
                new_indent = current_indent

            cursor.insertText("\n" + new_indent)
            return

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
            # inferred = script.infer(line, column)
            pass

            # if inferred:
                # print("--------------------------------")
                # print(inferred[0].name)
                # print(inferred[0].type)
                # print("--------------------------------")
                # if inferred[0].type == 'class' or inferred[0].type == 'function':
                #     self.class_or_function[inferred[0].name] = inferred[0].type
                #     print(self.class_or_function)
                
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



class DocStringDock(QDockWidget):
    def __init__(self, parent):
        super().__init__()

        self.clearFocus()

        self.doc_panel = QTextEdit()
        self.doc_panel.setReadOnly(True)
        self.doc_panel.setMinimumHeight(120)
        self.doc_panel.clearFocus()

        self.setWidget(self.doc_panel)

        # dock = QDockWidget("Docstring", self)
        # dock.setWidget(self.doc_panel)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        parent.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self)
        self.setStyleSheet("""
            QDockWidget {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                color: #ffffff;
            }

            QTextEdit {
                background-color: #252526;
                color: #d4d4d4;
                font-family: Consolas, monospace;
                font-size: 19px;
                padding: 5px;
            }

            QScrollBar:vertical {
                background: #2d2d2d;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical {
                background: #5a5a5a;
                min-height: 20px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)



class ShowFiles(QDockWidget):
    def __init__(self, parent, main_text):
        super().__init__(parent)
        self.main_text = main_text
        self.hbox = QHBoxLayout()

        self.new_file_input = QLineEdit(self)
        self.new_file_input.setPlaceholderText('Name new file')

        self.new_file_input.hide()

        self.new_folder_input = QLineEdit(self)
        self.new_folder_input.setPlaceholderText('Name new folder')

        self.new_folder_input.hide()

        self.file_viewer = QTreeView(self)

        self.hbox.addWidget(self.new_file_input)
        self.hbox.addWidget(self.new_folder_input)
        self.hbox.addWidget(self.file_viewer)

        self.dir_model = QFileSystemModel(parent)
        self.dir_model.setRootPath(QDir.currentPath())
        self.file_viewer.setModel(self.dir_model)
        self.file_viewer.setRootIndex(self.dir_model.index(QDir.currentPath()))

        self.file_viewer.setHeaderHidden(True)
        self.file_viewer.setAnimated(True)
        self.file_viewer.setColumnHidden(1, True)
        self.file_viewer.setColumnHidden(2, True)
        self.file_viewer.setColumnHidden(3, True)

        self.file_viewer.setStyleSheet("""

            QTreeView {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                color: #ffffff;
            }

            QScrollBar:vertical {
                background: #2d2d2d;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical {
                background: #5a5a5a;
                min-height: 20px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar:horizontal {
                background: #2d2d2d;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:horizontal {
                background: #5a5a5a;
                min-height: 20px;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                height: 0px;
            }

""")

        self.setWidget(self.file_viewer)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        parent.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self)
        self.setStyleSheet("""
            QDockWidget {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                color: #ffffff;
            }

            QScrollBar:vertical {
                background: #2d2d2d;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical {
                background: #5a5a5a;
                min-height: 20px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        self.file_viewer.clicked.connect(self.set_file)

    def set_file(self, index):
        try:
            path = self.sender().model().filePath(index)

            with open (path, 'r', encoding = 'utf-8') as file:
                self.main_text.setPlainText(file.read())
        except Exception as e:
            pass


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Return:
            model = self.file_viewer.model()
            index = self.file_viewer.currentIndex()
            path = model.filePath(index)
            try:
                with open (path, 'r', encoding = 'utf-8') as file:
                    self.main_text.setPlainText(file.read())
            except Exception as e:
                pass
        
        if key == Qt.Key.Key_F and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.new_file_input.show()
            self.new_file_input.setFocus()
            self.new_file_input.returnPressed.connect(self.create_file)

        if key == Qt.Key.Key_D and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.new_folder_input.show()
            self.new_folder_input.setFocus()
            self.new_folder_input.returnPressed.connect(self.create_folder)      

        if key == Qt.Key.Key_K and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.remove_file()

        if key == Qt.Key.Key_J and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.remove_dir()

        if key == Qt.Key.Key_Escape:
            self.new_file_input.hide()
            self.new_folder_input.hide()

        super().keyPressEvent(event)

    def remove_file(self):
        model = self.file_viewer.model()
        index = self.file_viewer.currentIndex()
        path = model.filePath(index)

        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass
        else:
            print("There is no", path)

    def remove_dir(self):
        model = self.file_viewer.model()
        index = self.file_viewer.currentIndex()
        path = model.filePath(index)

        if os.path.exists(path):
            try:
                os.rmdir(path)
            except Exception as e:
                pass
        else:
            print("There is no", path)

    def create_file(self):
        model = self.file_viewer.model()
        index = self.file_viewer.currentIndex()
        path = model.filePath(index)

        strin_path = str(path)

        new_string_path = strin_path.split('/')
        if '.' in new_string_path[-1]:
            path = '/'.join(new_string_path[:-1])

        if self.new_file_input.text():
            try:
                with open (f"{path}/{self.new_file_input.text()}", 'w') as file:
                    file.write('')
                    file.close()
            except Exception:
                with open (f"{QDir.currentPath()}/{self.new_file_input.text()}", 'w') as file:
                    file.write('')
                    file.close()


        self.new_file_input.clearFocus()
        self.new_file_input.setText('')
        self.new_file_input.hide()
        self.file_viewer.setFocus()

    def create_folder(self):
        model = self.file_viewer.model()
        index = self.file_viewer.currentIndex()
        path = model.filePath(index)

        strin_path = str(path)

        new_string_path = strin_path.split('/')
        if strin_path.endswith('.py'):
            path = '/'.join(new_string_path[:-1])

        if self.new_folder_input.text():
            os.mkdir(f"{path}/{self.new_folder_input.text()}")
        self.new_folder_input.clearFocus()
        self.new_folder_input.setText('')
        self.new_folder_input.hide()
        self.file_viewer.setFocus()