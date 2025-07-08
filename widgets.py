## TO-DO: make the auto completer work only for .py files.

import jedi
import re
import os
from PyQt6.QtCore import QTimer, Qt, QRect, Qt, QDir, QFileInfo
from PyQt6.QtGui import QTextCursor, QKeyEvent, QPainter, QColor, QFont, QFontMetrics, QTextCursor, QColor, QFileSystemModel, QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QLineEdit, QPlainTextEdit, QVBoxLayout, QWidget, QCompleter, QDockWidget, QTextEdit, QTreeView, QFileIconProvider, QTabBar

from lines import ShowLines

from get_style import get_css_style

from highlighter import PythonSyntaxHighlighter
from show_errors import ShowErrors

central_widget = QWidget()

error_label = QLabel("Ready")
error_label.setObjectName("SyntaxChecker")
error_label.setStyleSheet(get_css_style())


file_description = {}

layout = QVBoxLayout(central_widget)

class MainText(QPlainTextEdit):
    def __init__(self, parent, window):
    # def __init__(self, parent):
        super().__init__()
        self.clipboard = window
        self.setCursorWidth(0)
        self.selected_line = None
        self.selected_text = None

        # self.doc_panel = doc_panel
        self.doc_panel = None
        self.cursorPositionChanged.connect(self.update_docstring)

        self.finder = findingText(parent, self)

        self.cursor_visible = True
        self.cursor_color = QColor("#f38ba8")  # Custom cursor color

        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.toggle_cursor)
        self.blink_timer.start(10)  # Blink rate (ms)

        self.line_number_area = ShowLines(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width(0)
        self.setObjectName('Editor')

        self.setStyleSheet(get_css_style())

        self.completer = QCompleter()
        popup = self.completer.popup()
        popup.setObjectName('AutoCompleter')
        popup.setStyleSheet(get_css_style())


        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.activated.connect(self.insert_completion)

    def toggle_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.viewport().update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.cursor_visible and self.hasFocus():
            painter = QPainter(self.viewport())
            painter.setPen(self.cursor_color)
            rect = self.cursorRect()
            painter.fillRect(rect.left(), rect.top(), 3, rect.height(), QColor("#f38ba8"))



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
        if self.doc_panel:
            if doc == "":

                self.doc_panel.hide()
            else:
                self.doc_panel.setPlainText(doc or "")
                self.doc_panel.show()

    def get_definition_docstring(self, code, line, column):
        try:
            script = jedi.Script(code=code, path="example.py")
            definitions = script.help(line, column)

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
            cursor.insertText(" " * 4)
            return



        if key == Qt.Key.Key_C and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            cursor = self.textCursor()

            if cursor.selectedText() == '':
                self.setUpdatesEnabled(False)
                self.blockSignals(True)
                cursor.beginEditBlock()

                cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
                cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
                text = cursor.selectedText()
                self.selected_line = text

                cursor.endEditBlock()
                self.setUpdatesEnabled(True)
                self.blockSignals(False)
                # pyperclip.copy(self.selected_line)
                self.clipboard.setText(self.selected_line)

                self.selected_text = None

            else:
                self.selected_text = cursor.selectedText()
                self.selected_line = None
                # pyperclip.copy(self.selected_text)
                self.clipboard.setText(self.selected_text)

            return

        if key == Qt.Key.Key_V and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if self.selected_text is not None:
                cursor = self.textCursor()
                self.setUpdatesEnabled(False)
                self.blockSignals(True)
                cursor.beginEditBlock()

                # cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
                self.setTextCursor(cursor)

                cursor.insertText(self.selected_text)
                cursor.endEditBlock()
                self.setUpdatesEnabled(True)
                self.blockSignals(False)
                self.selected_line = None

            if self.selected_line is not None:
                cursor = self.textCursor()
                self.setUpdatesEnabled(False)
                self.blockSignals(True)
                cursor.beginEditBlock()

                cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
                self.setTextCursor(cursor)

                cursor.insertText("\n" + self.selected_line)
                print(self.selected_line)
                cursor.endEditBlock()
                self.setUpdatesEnabled(True)
                self.blockSignals(False)
                self.selected_text = None
            return

        if key == Qt.Key.Key_F and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if self.finder.isVisible():
                self.finder.hide()
                self.setFocus()
            else:
                self.finder.show()
                self.finder.setFocus()
            return

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
            
            
            model = QStandardItemModel()

            words = []
            for c in completions[:30]:
                words.append(c.name)
                item = QStandardItem()
                item.setText(c.name)
                if c.type == 'statement':
                    item.setIcon(QIcon('icons/autocompleterIcons/variable.svg'))
                elif c.type == 'class' or c.type == 'module':
                    item.setIcon(QIcon('icons/autocompleterIcons/class.svg'))
                elif c.type == 'function':
                    item.setIcon(QIcon('icons/autocompleterIcons/function.svg'))
                elif c.type == 'keyword':
                    item.setIcon(QIcon('icons/autocompleterIcons/keyword.svg'))

                model.appendRow(item)

            if words:
                cursor.select(cursor.SelectionType.WordUnderCursor)
                prefix = cursor.selectedText()
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
        painter.fillRect(event.rect(), QColor(30, 30, 46))

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
    def __init__(self, parent, use):
        super().__init__()

        if use:

            self.clearFocus()

            self.doc_panel = QTextEdit()
            self.doc_panel.setReadOnly(True)
            self.doc_panel.setMinimumHeight(120)
            self.doc_panel.clearFocus()

            self.doc_panel.setObjectName("DocStrings")
            self.doc_panel.setStyleSheet(get_css_style())

            self.setWidget(self.doc_panel)

            self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
            parent.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self)
            self.setObjectName("Docks")

            self.setStyleSheet(get_css_style())

class ShowFiles(QDockWidget):
    def __init__(self, parent, main_text, opened_tabs):
        super().__init__(parent)
        self.main_text = main_text

        self.opened_tabs = opened_tabs

        global file_description
        self.hbox = QHBoxLayout()


        self.new_file_input = QLineEdit(self)
        self.new_file_input.setPlaceholderText('Name new file')

        self.new_file_input.hide()

        self.new_folder_input = QLineEdit(self)
        self.new_folder_input.setPlaceholderText('Name new folder')
        self.new_folder_input.setObjectName('FolderMaker')

        self.new_file_input.setObjectName('FileMaker')

        self.new_file_input.setStyleSheet(get_css_style())


        self.new_folder_input.setStyleSheet(get_css_style())


        self.new_folder_input.hide()

        self.file_viewer = QTreeView(self)

        self.file_viewer.setObjectName("DirectoryViewer")

        self.hbox.addWidget(self.new_file_input)
        self.hbox.addWidget(self.new_folder_input)
        self.hbox.addWidget(self.file_viewer)

        self.dir_model = QFileSystemModel(parent)
        self.dir_model.setRootPath(QDir.currentPath())
        self.dir_model.setIconProvider(CustomIcons())

        self.file_viewer.setModel(self.dir_model)
        self.file_viewer.setRootIndex(self.dir_model.index(QDir.currentPath()))

        self.file_viewer.setHeaderHidden(True)
        self.file_viewer.setAnimated(True)
        self.file_viewer.setColumnHidden(1, True)
        self.file_viewer.setColumnHidden(2, True)
        self.file_viewer.setColumnHidden(3, True)

        
        self.setObjectName('Docks')
        self.file_viewer.setStyleSheet(get_css_style())

        # self.opened_tabs.currentChanged.connect(self.set_text)

        self.setWidget(self.file_viewer)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        parent.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self)
        self.setStyleSheet(get_css_style())
        self.file_viewer.clicked.connect(self.set_file)

    # def set_text(self, index):
        # if self.opened_tabs.currentIndex() == -1:
        #     self.main_text.setPlainText("")
        #     file_description.clear()

        # # model = self.file_viewer.model()
        # # index = self.file_viewer.currentIndex()
        # # path = model.filePath(index)
        # # str_path = str(path)
        # # file_name = str_path.split('/')[-1]

        # current_index = self.opened_tabs.currentIndex()

        # tab_text = self.opened_tabs.tabText(current_index)

        # for path, file_name_ in file_description.items():
        #     if file_name_ == tab_text:
        #         # print(path, file_name)
        #         with open(path, 'r', encoding = 'utf-8') as file:
        #             self.main_text.setPlainText(file.read())

    def set_file(self, index):
        try:
            path = self.sender().model().filePath(index)
            str_path = str(path)
            file_name = str_path.split('/')[-1]
            if '.' in file_name:
                if path not in file_description.keys() and file_name not in file_description.values():

                    file_description[path] = file_name
                    self.opened_tabs.add_file(path, file_name)

                else:
                    all_tabs = self.opened_tabs.count()
                    for tab in range(all_tabs):
                        if self.opened_tabs.tabText(tab) == file_name:
                            self.opened_tabs.setCurrentIndex(tab)
                            break

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
            str_path = str(path)
            file_name = str_path.split('/')[-1]
            if '.' in file_name:

                if path not in file_description.keys() and file_name not in file_description.values():
                        file_description[path] = file_name
                        self.opened_tabs.add_file(path, file_name)

                else:
                    all_tabs = self.opened_tabs.count()
                    for tab in range(all_tabs):
                        if self.opened_tabs.tabText(tab) == file_name:
                            self.opened_tabs.setCurrentIndex(tab)
                            break

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

class CustomIcons(QFileIconProvider):
    def icon(self, info: QFileInfo) -> QIcon:
        image_formats = [
            "jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp", "heif", "heic",
            "eps", "pdf", "ai", "raw", "cr2", "nef", "arw", "orf", "dng",
            "ico", "psd", "xcf", "dds"
        ]

        # if info.isDir() and info.suffix().lower() == 'test':
        if info.isDir():
            return QIcon("icons/fileIcons/folder.webp")
        elif info.suffix().lower() == "py" or info.suffix().lower() == 'pyi':
            return QIcon("icons/fileIcons/python.svg")
        elif info.suffix().lower() == 'json':
            return QIcon("icons/fileIcons/json.svg")
        elif info.suffix().lower() == 'ini' or info.suffix() == 'cfg' or info.suffix() == 'settings' or info.suffix() == 'conf' or info.suffix() == 'config':
            return QIcon("icons/fileIcons/settings.svg")
        elif info.suffix().lower() in image_formats:
            return QIcon("icons/fileIcons/image.svg")
        elif info.suffix().lower() == 'svg':
            return QIcon('icons/fileIcons/svg.svg')
        elif info.suffix().lower() == 'pyc':
            return QIcon('icons/fileIcons/python-misc.svg')
        elif info.suffix().lower() == 'css':
            return QIcon('icons/fileIcons/css.png')
        elif info.suffix().lower() == 'html':
                return QIcon('icons/fileIcons/html.svg')
        elif info.suffix().lower() == 'txt':
            return QIcon('icons/fileIcons/txt.png')
        elif info.suffix().lower() == 'md' or info.suffix().lower() == 'markdown':
            return QIcon('icons/fileIcons/markdown.svg')

        else:
            return super().icon(info)


class ShowOpenedFile(QTabBar):
    def __init__(self, editor, layout, error_label, parent):
        super().__init__()
        global file_description
        self.editor = editor
        self.layout_ = layout
        self.error_label = error_label
        self.parent_ = parent
        self.setObjectName('OpenedFiles')
        self.currentChanged.connect(self.track_tabs)

        # self.doc_panelstring = DocStringDock(self.parent_, True)
        # self.editor.doc_panel = self.doc_panelstring.doc_panel


        self.setStyleSheet(get_css_style())


        layout.addWidget(self)


    def put_tab_icons(self, index):
        image_formats = (
            "jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp", "heif", "heic",
            "eps", "pdf", "ai", "raw", "cr2", "nef", "arw", "orf", "dng",
            "ico", "psd", "xcf", "dds"
        )

        if self.tabText(index).endswith('py') or self.tabText(index).endswith('pyi'):
            self.setTabIcon(index, QIcon('icons/fileIcons/python.svg'))

        elif self.tabText(index).endswith('txt'):
            self.setTabIcon(index, QIcon('icons/fileIcons/txt.png'))

        elif self.tabText(index).endswith('json'):
            self.setTabIcon(index, QIcon('icons/fileIcons/json.svg'))

        elif self.tabText(index).endswith('svg'):
            self.setTabIcon(index, QIcon('icons/fileIcons/svg.svg'))

        elif self.tabText(index).endswith('html'):
            self.setTabIcon(index, QIcon('icons/fileIcons/html.svg'))

        elif self.tabText(index).endswith('css'):
            self.setTabIcon(index, QIcon('icons/fileIcons/css.png'))

        elif self.tabText(index).endswith('pyc'):
            self.setTabIcon(index, QIcon('icons/fileIcons/python-misc.svg'))

        elif self.tabText(index).endswith(image_formats):
            self.setTabIcon(index, QIcon('icons/fileIcons/image.svg'))

        elif self.tabText(index).endswith('md') or self.tabText(index).endswith('markdown'):
            self.setTabIcon(index, QIcon('icons/fileIcons/markdown.svg'))

    def remove_tab(self, index):
        self.removeTab(index)

    def add_file(self, path, file_name):
        file_index = self.addTab(str(file_name))
        self.tabSizeHint(file_index)
        close_button = QPushButton('X')
        close_button.setFixedSize(16, 16)
        close_button.setObjectName("CloseTabButton")
        close_button.setStyleSheet(get_css_style())

        close_button.clicked.connect(lambda _, index_=file_index: self.remove_tab(index_))
        self.put_tab_icons(file_index)
        self.setCurrentIndex(file_index)
        self.setTabButton(file_index, self.ButtonPosition.RightSide, close_button)


    def track_tabs(self):
        if self.currentIndex() == -1:
            self.editor.setPlainText("")
            file_description.clear()

        current_index = self.currentIndex()
        tab_text = self.tabText(current_index)

        for path, file_name in file_description.items():
            if file_name == tab_text:
                if file_name.endswith('.py') or file_name.endswith('.pyi'):
                    self.highlighter = PythonSyntaxHighlighter(use_highlighter = True, parent=self.editor.document())
                    self.show_error = ShowErrors(self.editor, self.highlighter)
                    self.show_error.error_label = self.error_label
                    self.layout_.addWidget(self.error_label)
                    self.error_label.show()
                    self.doc_panelstring = DocStringDock(self.parent_, True)
                    self.editor.doc_panel = self.doc_panelstring.doc_panel
                    # self.editor.completer.setWidget(self.editor)

                else:
                    if self.error_label:
                        self.error_label.hide()
                    self.doc_panelstring = DocStringDock(self.parent_, False)
                    self.parent_.removeDockWidget(self.doc_panelstring)
                    self.doc_panelstring = None
                    self.editor.doc_panel = None
                    # self.editor.completer.setWidget(None)

                    self.highlighter = PythonSyntaxHighlighter(False, self.editor.document())

                with open(path, 'r', encoding = 'utf-8') as file:
                    self.editor.setPlainText(file.read())

# class Terminal(QDockWidget):
#     def __init__(self, parent):
#         super().__init__()
#         self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
#         parent.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self)

#         self.terminal_editor = QPlainTextEdit(self)
#         self.setWidget(self.terminal_editor)

#         self.process = QProcess(self.terminal_editor)
#         self.process.start('powershell')
#         self.process.readyReadStandardOutput.connect(self.handle_stdout_output)
        # process.kill()

    # def handle_stdout_output(self):
        # Read all available data from standard output
        # output_bytes = self.process.readAllStandardOutput().data()
        # # Decode the bytes to a string (e.g., using UTF-8)
        # output_string = output_bytes.decode('utf-8')
        # # Process the output_string (e.g., print it, display in a widget)
        # print("Standard Output:", output_string)
        # output = self.process.readAllStandardOutput().data().decode('utf-8')
        # self.terminal_editor.appendPlainText(output)


class findingText(QLineEdit):
    def __init__(self, bawky_parent, main_text):
        super().__init__()
        self.main_text = main_text
        self.setObjectName('Finder')
        self.hide()
        self.setStyleSheet(get_css_style())
        bawky_parent.addWidget(self)
        self.setPlaceholderText("Find...🔎")
        self.textChanged.connect(lambda: self.changed(main_text))
        self.returnPressed.connect(lambda: self.find_next(main_text))



    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Escape:
            self.hide()
            self.main_text.setFocus()
        super().keyPressEvent(event)

    def find_next(self, main_text):
        if not main_text.find(self.text()):
            main_text.moveCursor(QTextCursor.MoveOperation.Start)
            main_text.find(self.text())


    def changed(self, main_text):
        main_text.moveCursor(QTextCursor.MoveOperation.Start)
        main_text.find(self.text())