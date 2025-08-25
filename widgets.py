import re
import subprocess
import os
import webbrowser
from datetime import datetime
from PyQt6.QtCore import QThreadPool, QRectF, QTimer, Qt, QRect, QFileInfo, pyqtSignal, QProcess
from PyQt6.QtGui import QPainter, QPainterPath, QPixmap, QTextCursor, QKeyEvent, QPainter, QColor, QFont, QTextCursor, QColor, QFileSystemModel, QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QMessageBox, QFrame, QComboBox, QLabel, QPushButton, QHBoxLayout, QLineEdit, QPlainTextEdit, QVBoxLayout, QWidget, QCompleter, QDockWidget, QTextEdit, QTreeView, QFileIconProvider, QTabBar
from lines import ShowLines
from multiprocessing import Process, Queue

from get_style import get_css_style

from heavy import *
from animations import *
from config import *
from highlighter import *
from show_errors import *
from pygit import *


central_widget = QWidget()
central_widget.setObjectName('MainWindow')
central_widget.setStyleSheet(get_css_style())

error_label = QLabel("Ready")
error_label.setObjectName("SyntaxChecker")
error_label.setStyleSheet(get_css_style())

nameErrorlabel = QLabel('Ready')
nameErrorlabel.setObjectName('NameErrorChecker')
nameErrorlabel.setStyleSheet(get_css_style())

file_description = {}

commenting = ''
current_file_path = ''

# layout = QVBoxLayout(central_widget)



class MainText(QPlainTextEdit):
    def __init__(self, parent, window, font_size, window_):
        super().__init__()
        print(sys.executable)
        self.font_size = font_size
        global commenting
        self.clipboard = window
        self.window = window_
        self.setCursorWidth(0)
        if showDocstringpanel():
            self.jediBridge()


        self.code_queue_ = Queue()
        self.result_queue_ = Queue()

        self.jediCompletetion_process = Process(target=jedi_completion, args=(self.code_queue_, self.result_queue_, current_file_path))
        self.jediCompletetion_process.start()

        bridge_ = JediBridgeCompletion(self.code_queue_, self.result_queue_)
        self.jedi_completion_bridge = bridge_
        self.jedi_completion_bridge.result_ready.connect(self.on_autocomplete_results)


        self.font__ = QFont(get_fontFamily(), get_fontSize())
        self.font__.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.font__.setPixelSize(self.font_size)
        self.setFont(self.font__)

        self.selected_line = None
        self.selected_text = None
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.doc_panel = None

        self.docstring_timer = QTimer()
        self.docstring_timer.setSingleShot(True)

        self._docstring_cache = {}


        self.finder = findingText(parent, self)

        self.cursor_visible = True
        r, g, b = get_cursorColor()
        # self.cursor_color = QColor("#f38ba8")
        self.cursor_color = QColor(r, g, b)

        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.toggle_cursor)
        self.blink_timer.start(get_cursorBlinkingRate())



        self.line_number_area = ShowLines(self, self.font_size)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        if showDocstringpanel():
            self.cursorPositionChanged.connect(self.on_text_change)
            self.jedi_bridge.result_ready.connect(self.on_docstring_result)

        self.update_line_number_area_width(0)
        
        self.setObjectName('Editor')
        self.setStyleSheet(get_css_style())
        self.show_completer = False

        self.completer = QCompleter()
        popup = self.completer.popup()
        popup.setObjectName('AutoCompleter')
        popup.setFont(self.font__)
        popup.setStyleSheet(get_css_style())
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.activated.connect(self.insert_completion)
        self.hide()




        self._last_docstring_position = -1
        self._last_docstring = ""

    def cursor_to_line_column(self, pos):
        text = self.toPlainText()
        lines = text[:pos].splitlines()
        line = len(lines) if lines else 1
        column = len(lines[-1]) if lines else 0
        return line, column


    def jediBridge(self):
        self.code_queue = Queue()
        self.result_queue = Queue()

        p = Process(target=jedi_worker, args=(self.code_queue, self.result_queue))
        p.start()

        bridge = JediBridge(self.code_queue, self.result_queue)
        self.jedi_bridge = bridge

    def on_text_change(self):
        code = self.toPlainText()
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.positionInBlock()
        self.jedi_bridge.request_docstring((code, line, column))


    def parse_docstring(self, doc: str):
        lines = doc.strip().splitlines()
        formatted = []
        for line in lines:
            line = line.strip()
            if line in ('---', '***', '___'):
                formatted.append('<hr>')
            elif line.endswith(':') and not line.startswith(' '):
                formatted.append(f'<b style="font-size:30px;">{line}</b>')

            elif re.match(r'^\*{3,}$', line):
                formatted.append('<hr>')
            else:
                formatted.append(line)
        return "<br>".join(formatted)

    def line_number_area_width(self, font_metrics):
        digits = len(str(self.blockCount()))
        return 3 + font_metrics.horizontalAdvance('9') * digits

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(self.line_number_area.font_metrics), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)


    def toggle_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.viewport().update()


    def paintEvent(self, event):
        super().paintEvent(event)
        if showIndentLine():
            self.paint_indent_guides(event)
        self.paint_cursor(event) 


    def paint_indent_guides(self, event):
        painter = QPainter(self.viewport())
        r, g, b = get_IndentlineColor()
        painter.setPen(QColor(r, g, b))


        block = self.firstVisibleBlock()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        line_height = self.fontMetrics().height()
        space_width = self.fontMetrics().horizontalAdvance(' ')

        while block.isValid():
            text = block.text()
            leading_spaces = len(text) - len(text.lstrip(' '))

            for col in range(4, leading_spaces + 1, 4):
                if col <= len(text) and text[col - 1] == ' ':
                    x = space_width * col
                    painter.drawLine(x, top, x, top + line_height)

            block = block.next()
            top += line_height

        painter.end()


    def paint_cursor(self, event):
        if self.cursor_visible and self.hasFocus():
            painter = QPainter(self.viewport())
            painter.setPen(self.cursor_color)
            rect = self.cursorRect()
            r, g, b = get_cursorColor()
            painter.fillRect(rect.left(), rect.top(), get_cursorWidth(), rect.height(), QColor(r, g, b))
            painter.end()

    def insert_completion(self, completion):
        cursor = self.textCursor()
        cursor.beginEditBlock()

        cursor.select(cursor.SelectionType.WordUnderCursor)
        cursor.removeSelectedText()
        cursor.insertText(completion)
        self.setTextCursor(cursor)
        cursor.endEditBlock()



    def schedule_docstring_update(self):
        if not self.textCursor().hasSelection():
            self.docstring_timer.start(150)

    def on_docstring_result(self, doc):
        self._last_docstring_position = self.textCursor().position()
        self._last_docstring = doc
        if self.doc_panel:
            if doc == "":
                animatePanel(self.doc_panel.dock, self.window, False)
                # self.doc_panel.hide()
                if self.doc_panel.custom_title:
                #     self.doc_panel.custom_title.hide()
                #     self.doc_panel.dock.hide()
                    animatePanel(self.doc_panel.custom_title, self.window, False)
                    animatePanel(self.doc_panel, self.window, False)

            else:
                self.doc_viewer = self.parse_docstring(doc)
                self.doc_panel.setHtml(self.doc_viewer or "")
                animatePanel(self.doc_panel.dock, self.window, True)
                # self.doc_panel.dock.show()
                # self.doc_panel.custom_title.show()
                # self.doc_panel.show()
                animatePanel(self.doc_panel.custom_title, self.window, True)
                animatePanel(self.doc_panel, self.window, True)


    def keyPressEvent(self, event: QKeyEvent):
        global current_file_path
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
            cursor.beginEditBlock()
            closing_char = pairs[text]
            cursor.insertText(text + closing_char)
            cursor.movePosition(QTextCursor.MoveOperation.Left)
            self.setTextCursor(cursor)
            cursor.endEditBlock()
            return

        if key == Qt.Key.Key_Tab:
            cursor = self.textCursor()
            cursor.beginEditBlock()
            cursor.insertText(" " * 4)
            cursor.endEditBlock()
            return

        if key == Qt.Key.Key_Slash and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.toggle_comments()
            return

        if key == Qt.Key.Key_X and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.cut_text()
            return

        if key == Qt.Key.Key_C and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.copy_text()
            return

        if key == Qt.Key.Key_V and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.paste_text()
            return

        if key == Qt.Key.Key_F and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if self.finder.maximumHeight() == 0:
                animatePanel(self.finder, self.window, show=True)
                self.finder.setFocus()
            else:
                animatePanel(self.finder, self.window, show=False)
        #     if self.finder.isVisible():
        #         self.finder.hide()
                self.setFocus()
        #     else:
        #         self.finder.show()
        #     return

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.handle_enter()
            return

        super().keyPressEvent(event)

        if not (Qt.Key.Key_A <= key <= Qt.Key.Key_Z or 
                Qt.Key.Key_0 <= key <= Qt.Key.Key_9 or 
                key in (Qt.Key.Key_Period, Qt.Key.Key_Underscore)):
            return

        if self.show_completer and showCompleter():
            self.handle_autocomplete()

    def toggle_comments(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        
        if not cursor.hasSelection():
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        start_block = cursor.blockNumber()

        cursor.setPosition(end)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        end_block = cursor.blockNumber()

        for block_num in range(start_block, end_block + 1):
            block = self.document().findBlockByNumber(block_num)
            text = block.text()

            leading_spaces = len(text) - len(text.lstrip())
            indent = text[:leading_spaces]
            content = text[leading_spaces:]

            cursor.setPosition(block.position())
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

            if content.startswith(commenting) and not content.startswith('/*') and not content.startswith('<!--'):
                content = content[len(commenting):].lstrip()
            elif content.startswith('/*'):
                content = content[1:-2].lstrip()
                content = content[len(commenting):].lstrip()
            elif content.startswith('<!--'):
                content = content[4:-3].lstrip()
            else:
                if commenting == '/*':
                    content += '*/'
                elif commenting == '<!--':
                    content += '-->'
                content = f"{commenting} {content}"

            cursor.insertText(indent + content)

        cursor.endEditBlock()

    def cut_text(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()

        if cursor.selectedText() == '':
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
            text = cursor.selectedText()
            self.selected_line = text
            self.selected_text = None
            self.clipboard.setText(self.selected_line)
            cursor.removeSelectedText()
            cursor.deleteChar()
        else:
            self.selected_text = cursor.selectedText()
            self.selected_line = None
            self.clipboard.setText(self.selected_text)
            cursor.removeSelectedText()
            cursor.deleteChar()

        self.completer.popup().hide()
        cursor.endEditBlock()

    def copy_text(self):
        cursor = self.textCursor()
        
        if cursor.selectedText() == '':
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
            text = cursor.selectedText()
            self.selected_line = text
            self.clipboard.setText(self.selected_line)
            self.selected_text = None
        else:
            self.selected_text = cursor.selectedText()
            self.selected_line = None
            self.clipboard.setText(self.selected_text)

    def paste_text(self):
        if self.clipboard.text() != '' and self.selected_line is None:
            cursor = self.textCursor()
            cursor.beginEditBlock()
            cursor.insertText(self.clipboard.text())
            cursor.endEditBlock()
            self.selected_line = None

        if self.selected_line is not None:
            cursor = self.textCursor()
            cursor.beginEditBlock()
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
            self.setTextCursor(cursor)
            cursor.insertText("\n" + self.selected_line)
            self.selected_text = None
            cursor.endEditBlock()

    def handle_enter(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()

        block_text = cursor.block().text()
        indent_match = re.match(r'^(\s*)', block_text)
        current_indent = indent_match.group(1) if indent_match else ""

        if block_text.strip().endswith(":"):
            new_indent = current_indent + " " * 4
        else:
            new_indent = current_indent

        cursor.insertText("\n" + new_indent)
        cursor.endEditBlock()

    def handle_autocomplete(self):
        code = self.toPlainText()
        cursor = self.textCursor()
        pos = cursor.position()
        line, column = self.cursor_to_line_column(pos)

        if cursor.hasSelection():
            return

        self.code_queue_.put((code, line, column))
        # worker = AutocompleteRunnable(self, code, line, column, 1)
        # worker.signals.results.connect(self.on_autocomplete_results)
        # worker.signals.error.connect(self.on_autocomplete_error)

        # QThreadPool.globalInstance().start(worker)



    def on_autocomplete_results(self, payload):
        model = QStandardItemModel()

        for item_data in payload:
            item = QStandardItem()
            item.setText(item_data["name"])

            if item_data["type"] == 'statement':
                item.setIcon(QIcon('icons/autocompleterIcons/variable.svg'))
            elif item_data["type"] in ('class', 'module'):
                item.setIcon(QIcon('icons/autocompleterIcons/class.svg'))
            elif item_data["type"] == 'function':
                item.setIcon(QIcon('icons/autocompleterIcons/function.svg'))
            elif item_data["type"] == 'keyword':
                item.setIcon(QIcon('icons/autocompleterIcons/keyword.svg'))

            model.appendRow(item)

        cursor = self.textCursor()
        cursor.select(cursor.SelectionType.WordUnderCursor)
        prefix = cursor.selectedText()

        self.completer.setModel(model)
        self.completer.setCompletionPrefix(prefix)
        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) + 10)
        self.completer.complete(cr)

    def on_autocomplete_error(self, e):
        print("Autocomplete error:", e)

    def line_number_area_width(self, font_metrics):
        digits = len(str(self.blockCount()))
        return 3 + font_metrics.horizontalAdvance('9') * digits

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(self.line_number_area.font_metrics), 0, 0, 0)

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
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(self.line_number_area.font_metrics), cr.height()))

    def line_number_area_paint_event(self, event, font_metrics):
        painter = QPainter(self.line_number_area)
        # painter.fillRect(event.rect(), QColor(30, 30, 46))

        r, g, b = get_lineareacolor()

        painter.fillRect(event.rect(), QColor(r, g, b))

        font = QFont(get_fontFamily(), get_fontSize())
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        font.setPixelSize(get_fontSize())

        painter.setFont(font)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                # painter.setPen(QColor(160, 160, 160))
                r, g, b = get_linenumbercolor()
                painter.setPen(QColor(r, g, b))

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
        self.custom_title = QLabel("Doc")
        self.custom_title.setObjectName('DockTitles')
        self.custom_title.setStyleSheet(get_css_style())

        self.setTitleBarWidget(self.custom_title)


        if use:
            self.clearFocus()
            self.doc_panel = QTextEdit()
            self.doc_panel.dock = self
            self.doc_panel.custom_title = self.custom_title
            self.doc_panel.setReadOnly(True)
            # self.doc_panel.setMinimumHeight(120)
            self.doc_panel.clearFocus()

            self.doc_panel.setObjectName("DocStrings")
            self.setWindowTitle('Doc String')
            self.doc_panel.setStyleSheet(get_css_style())

            font = QFont(get_fontFamily(), get_fontSize())
            font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
            font.setPixelSize(get_fontSize())

            self.doc_panel.setFont(font)
            self.setWidget(self.doc_panel)

            self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
            parent.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self)
            self.setObjectName("Docks")

            self.setStyleSheet(get_css_style())
            self.setMaximumHeight(0)

class ShowDirectory(QDockWidget):
    def __init__(self, main_text, opened_tabs):
        from pygit import folder_path_

        super().__init__()

        self.main_text = main_text

        self.custom_title = QLabel("Directory Viewer")
        self.custom_title.setObjectName('DockTitles')
        self.custom_title.setStyleSheet(get_css_style())

        self.setTitleBarWidget(self.custom_title)
        self.setWindowTitle('Directory Viewer')

        self.opened_tabs = opened_tabs

        global file_description

        self.container = QWidget()

        # self.hbox = QHBoxLayout(container)
        self.hbox = QVBoxLayout(self.container)

        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)

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

        font = QFont(get_fontFamily(), get_fontSize())

        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        font.setPixelSize(get_fontSize())

        self.file_viewer.setFont(font)
        self.setFont(font)

        # self.file_viewer.hide()
        # self.file_viewer.clearFocus()


        self.hide()
        self.setMaximumHeight(0)


        self.hbox.addWidget(self.new_file_input)
        self.hbox.addWidget(self.new_folder_input)
        self.hbox.addWidget(self.file_viewer)

        self.dir_model = QFileSystemModel()
        # self.dir_model = QFileSystemModel(parent)
        self.dir_model.setRootPath(folder_path_)

        self.dir_model.setIconProvider(CustomIcons())

        self.file_viewer.setModel(self.dir_model)
        # self.file_viewer.setRootIndex(self.dir_model.index(QDir.currentPath()))
        self.file_viewer.setRootIndex(self.dir_model.index(folder_path_))


        self.file_viewer.setHeaderHidden(True)
        self.file_viewer.setAnimated(True)
        self.file_viewer.setColumnHidden(1, True)
        self.file_viewer.setColumnHidden(2, True)
        self.file_viewer.setColumnHidden(3, True)


        self.setObjectName('Docks')
        self.file_viewer.setStyleSheet(get_css_style())


        # self.setWidget(self.file_viewer)
        self.setWidget(self.container)

        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)

        self.setStyleSheet(get_css_style())
        self.file_viewer.clicked.connect(self.set_file)


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
                cursor = self.main_text.textCursor()
                cursor.beginEditBlock()
                self.main_text.setUpdatesEnabled(False)
                self.main_text.blockSignals(True)
                self.main_text.setPlainText(file.read())
                cursor.endEditBlock()
                self.main_text.setUpdatesEnabled(True)
                self.main_text.blockSignals(False)


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
                    # self.main_text.setPlainText(file.read())

                    cursor = self.main_text.textCursor()
                    cursor.beginEditBlock()
                    # self.main_text.setUpdatesEnabled(False)
                    # self.main_text.blockSignals(True)
                    self.main_text.setPlainText(file.read())
                    cursor.endEditBlock()
                    # self.main_text.setUpdatesEnabled(True)
                    # self.main_text.blockSignals(False)

            except Exception as e:
                pass


        ############ ADD THIS TO LISTSHORTCUTS

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
        ############ ADD THIS TO LISTSHORTCUTS


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
                with open (f"{folder_path_}/{self.new_file_input.text()}", 'w') as file:
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
    def icon(self, info: QFileInfo):
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
        elif info.suffix().lower() == 'json' or info.suffix().lower() == 'jsonc':
            return QIcon("icons/fileIcons/json.svg")
        elif info.suffix().lower() == 'ini' or info.suffix().lower() == 'cfg' or info.suffix().lower() == 'settings' or info.suffix().lower() == 'conf' or info.suffix().lower() == 'config':
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
    def __init__(self, editor, layout, error_label, parent, welcome_page, editor_containter, editor_layout, nameError):
    # def __init__(self, editor, layout, error_label, parent):

        super().__init__()
        global file_description
        global commenting
        self.is_panel = True
        self.tab_paths = {}
        self.previous_index = -1
        self.welcome_page = welcome_page
        self.editor_layout = editor_layout
        self.editor_containter = editor_containter


        self.editor = editor
        self.layout_ = layout
        self.error_label = error_label
        self.nameErrorlabel = nameError
        self.parent_ = parent
        self.setObjectName('OpenedFiles')
        self.currentChanged.connect(self.track_tabs)

        self.setStyleSheet(get_css_style())

        if showDocstringpanel():
            self.doc_panelstring = DocStringDock(self.parent_, False)

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

        elif self.tabText(index).endswith('json') or self.tabText(index).endswith('jsonc'):
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

        elif self.tabText(index).lower().endswith('ini') or self.tabText(index).lower().endswith('settings') or self.tabText(index).lower().endswith('conf') or self.tabText(index).lower().endswith('config') or self.tabText(index).lower().endswith('cfg'):
            self.setTabIcon(index, QIcon('icons/fileIcons/settings.svg'))


    def remove_tab(self, index):
        current_file = self.tabText(index)

        for path, file in list(file_description.items()):
            if file == current_file:
                file_description.pop(path)
                break

        self.removeTab(index)

        if self.count() > 0:
            self.track_tabs(self.currentIndex())
            # self.editor.show()
        else:

            cursor = self.editor.textCursor()
            cursor.beginEditBlock()
            self.editor.setPlainText("")
            # self.editor.hide()
            cursor.endEditBlock()


            self.previous_path = None
            file_description.clear()


    def add_file(self, path, file_name):
        file_index = self.addTab(str(file_name))
        self.tabSizeHint(file_index)

        close_button = QPushButton('X')
        close_button.setFixedSize(16, 16)
        close_button.setObjectName("CloseTabButton")
        close_button.setStyleSheet(get_css_style())

        def handle_close():
            for i in range(self.count()):
                if self.tabButton(i, self.ButtonPosition.RightSide) == self.sender():
                    self.remove_tab(i)
                    break

        close_button.clicked.connect(handle_close)

        self.put_tab_icons(file_index)
        self.setCurrentIndex(file_index)
        self.setTabButton(file_index, self.ButtonPosition.RightSide, close_button)
        if not self.editor.isVisible():
            self.welcome_page.hide()
            # self.parent_.setCentralWidget(self.editor)
            self.parent_.setCentralWidget(self.editor_containter)
            self.editor.show()

    def track_tabs(self, index):
        global commenting, current_file_path

        if hasattr(self, 'previous_path') and self.previous_path:
            with open(self.previous_path, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())

        if self.count() == 0:
            cursor = self.editor.textCursor()
            cursor.beginEditBlock()

            self.editor.setPlainText("")

            cursor.endEditBlock()


            file_description.clear()
            self.previous_path = None
            return


        current_index = self.currentIndex()
        tab_text = self.tabText(current_index)
        self.previous_path = None


        for path, file_name in file_description.items():
            if file_name == tab_text:
                self.previous_path = path
                current_file_path = path

                try:
                    with open(path, 'r', encoding = 'utf-8') as file:
                        cursor = self.editor.textCursor()
                        cursor.beginEditBlock()

                        self.editor.setPlainText(file.read())

                        cursor.endEditBlock()

                except FileNotFoundError:
                    self.remove_tab(self.currentIndex())
                    return


                if file_name.lower().endswith('.py') or file_name.lower().endswith('.pyi'):
                    current_file_path = path
                    self.highlighter = PythonSyntaxHighlighter(use_highlighter = True, parent=self.editor.document())


                    self.show_error = ShowErrors(self.editor, self.highlighter)


                    self.editor.show_completer = True
                    self.show_error.error_label = self.error_label
                    self.show_error.nameErrorlabel = self.nameErrorlabel

                    self.layout_.addWidget(self.error_label)
                    self.layout_.addWidget(self.nameErrorlabel)
                    self.editor_layout.addWidget(self.error_label)
                    self.editor_layout.addWidget(self.nameErrorlabel)

                    self.error_label.show()
                    self.nameErrorlabel.show()

                    if self.is_panel and showDocstringpanel():
                        self.doc_panelstring = DocStringDock(self.parent_, True)
                        self.editor.doc_panel = self.doc_panelstring.doc_panel
                    self.is_panel = False

                    commenting = '#'


                elif file_name.lower().endswith('.json') or file_name.lower().endswith('.jsonc'):
                    self.highlighter = PythonSyntaxHighlighter(False, self.editor.document())
                    self.highlighter.deleteLater()
                    self.highlighter = JsonSyntaxHighlighter(True, self.editor.document())

                    try:
                        if self.show_error:
                            if hasattr(self.show_error, 'cleanup'):
                                self.show_error.cleanup()
                            self.show_error.error_label = None
                            self.show_error = None
                    except Exception as e:
                        pass

                    if self.error_label:
                        self.error_label.hide()
                    if self.nameErrorlabel:
                        self.nameErrorlabel.hide()
                    try:

                        if self.doc_panelstring:
                            self.parent_.removeDockWidget(self.doc_panelstring)
                            self.doc_panelstring.deleteLater()

                    except Exception:
                        pass
                    self.doc_panelstring = None
                    self.editor.doc_panel = None
                    self.editor.show_completer = False
                    self.editor.completer.setCompletionPrefix("")
                    commenting = '//'
                    self.is_panel = True

                    if file_name.lower().endswith('.jsonc'):
                        self.show_error = ShowJsonErrors(self.editor, self.highlighter, path, True)

                    elif file_name.lower().endswith('.json'):
                        self.show_error = ShowJsonErrors(self.editor, self.highlighter, path, False)
                    self.show_error.error_label = self.error_label
                    # self.layout_.addWidget(self.error_label)
                    self.editor_layout.addWidget(self.error_label)

                    self.error_label.show()

                elif file_name.lower().endswith('.css'):
                    self.highlighter = PythonSyntaxHighlighter(False, self.editor.document())
                    self.highlighter.deleteLater()
                    self.highlighter = CssSyntaxHighlighter(True, self.editor.document())

                    try:
                        if self.show_error:
                            if hasattr(self.show_error, 'cleanup'):
                                self.show_error.cleanup()
                            self.show_error.error_label = None
                            self.show_error = None
                    except Exception as e:
                        pass

                    if self.error_label:
                        self.error_label.hide()
                    if self.nameErrorlabel:
                        self.nameErrorlabel.hide()

                    try:

                        if self.doc_panelstring:
                            self.parent_.removeDockWidget(self.doc_panelstring)
                            self.doc_panelstring.deleteLater()

                    except Exception:
                        pass
                    self.doc_panelstring = None
                    self.editor.doc_panel = None
                    self.editor.show_completer = False
                    self.editor.completer.setCompletionPrefix("")
                    commenting = '/*'
                    self.is_panel = True

                    self.show_error = ShowCssErrors(self.editor, self.highlighter)

                    self.show_error.error_label = self.error_label
                    # self.layout_.addWidget(self.error_label)
                    self.editor_layout.addWidget(self.error_label)
                    self.error_label.show()


                elif file_name.lower().endswith('.ini') or file_name.lower().endswith('.settings') or file_name.lower().endswith('.conf') or file_name.lower().endswith('.cfg') or file_name.lower().endswith('.config'):
                    self.highlighter = PythonSyntaxHighlighter(False, self.editor.document())
                    self.highlighter.deleteLater()
                    self.highlighter = ConfigSyntaxHighlighter(True, self.editor.document())

                    try:
                        if self.show_error:
                            if hasattr(self.show_error, 'cleanup'):
                                self.show_error.cleanup()
                            self.show_error.error_label = None
                            self.show_error = None
                    except Exception as e:
                        pass

                    if self.error_label:
                        self.error_label.hide()

                    if self.nameErrorlabel:
                        self.nameErrorlabel.hide()

                    try:

                        if self.doc_panelstring:
                            self.parent_.removeDockWidget(self.doc_panelstring)
                            self.doc_panelstring.deleteLater()

                    except Exception:
                        pass
                    self.doc_panelstring = None
                    self.editor.doc_panel = None
                    self.editor.show_completer = False
                    self.editor.completer.setCompletionPrefix("")
                    commenting = ';'
                    self.is_panel = True


                elif file_name.lower().endswith('md') or file_name.lower().endswith('markdown'):
                    self.highlighter = PythonSyntaxHighlighter(False, self.editor.document())
                    self.highlighter.deleteLater()
                    self.highlighter = MarkdownSyntaxHighlighter(True, self.editor.document())

                    try:
                        if self.show_error:
                            self.show_error.error_label = None
                            self.show_error = None
                    except Exception as e:
                        pass

                    if self.error_label:
                        self.error_label.hide()
                    try:

                        if self.doc_panelstring:
                            self.parent_.removeDockWidget(self.doc_panelstring)
                            self.doc_panelstring.deleteLater()

                    except Exception:
                        pass
                    self.doc_panelstring = None
                    self.editor.doc_panel = None
                    self.editor.show_completer = False
                    self.editor.completer.setCompletionPrefix("")
                    commenting = '<!--'
                    self.is_panel = True


                else:
                    try:
                        if self.show_error:
                            self.show_error.error_label = None
                            self.highlighter = None

                            self.show_error = None
                    except Exception as e:
                        pass

                    if self.error_label:
                        self.error_label.hide()
                    if self.nameErrorlabel:
                        self.nameErrorlabel.hide()

                    try:
                        if self.doc_panelstring:
                            self.parent_.removeDockWidget(self.doc_panelstring)
                            self.doc_panelstring.deleteLater()
                    except Exception:
                        pass

                    self.doc_panelstring = None
                    self.editor.doc_panel = None
                    self.editor.show_completer = False
                    self.editor.completer.setCompletionPrefix("")
                    commenting = ''
                    self.is_panel = True


            else:
                file_description[path] = file_name


    def is_save_file_needed(self):
        current_index = self.currentIndex()
        current_file = self.tabText(current_index)

        for path, file in file_description.items():
            if file == current_file:
                with open(path, 'r', encoding = 'utf-8') as file:
                    if self.editor.toPlainText() != file.read():
                        return True
                    else:
                        return False

    def save_current_file(self):
        current_index = self.currentIndex()
        current_file = self.tabText(current_index)

        for path, file in file_description.items():
            if file == current_file:
                with open(path, 'w', encoding = 'utf-8') as file:
                    file.write(self.editor.toPlainText())


class TerminalEmulator(QWidget):
    command_input = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setObjectName('Terminal')
        self.setStyleSheet(get_css_style())

        self.setup_selector()

        self.terminal = QPlainTextEdit(self)
        self.terminal.setFont(QFont(get_fontFamily(), get_fontSize()))
        self.terminal.setObjectName('Terminal')
        self.terminal.setStyleSheet((get_css_style()))

        self.terminal.clearFocus()
        self.terminal.hide()


        self.terminal.keyPressEvent = self.terminal_key_press_event

        self.layout.addWidget(self.terminal)

        self.processes = []
        self.current_process_index = -1

        self.command_history = []
        self.history_index = 0

        self.current_command = ""
        self.prompt = "> "

        self.startSession()

    def setup_selector(self):
        self.terminal_selector = QComboBox()
        # self.terminal_selector.setStyleSheet("QComboBox { min-width: 150px; }")

    def startSession(self):
        process = QProcess(self)
        process.readyReadStandardOutput.connect(self.handle_stdout)
        process.readyReadStandardError.connect(self.handle_stderr)
        self.processes.append(process)
        self.terminal_selector.setCurrentIndex(0)

        # self.start_powershell(0, project_path=current_file_path)
        self.start_powershell(0, project_path=folder_path_)

        # self.start_powershell(0, project_path='')

        # self.run_command('cls')

    def start_powershell(self, index, project_path=None):
        powershell_path = self.find_powershell_core()
        if project_path == "":
            project_path = os.getcwd()

        self.processes[index].setWorkingDirectory(project_path)

        if powershell_path:
            self.processes[index].start(powershell_path)
            self.terminal.appendPlainText(
                f"Your current working directory {project_path}.\n"
            )
        else:
            self.processes[index].start("powershell.exe")
            self.terminal.appendPlainText(
                f"Your current working directory {project_path}.\n"
            )

        self.display_prompt()

    def find_powershell_core(self):
        paths_maybe = [
            r"C:\Program Files\PowerShell\7\pwsh.exe",
            r"C:\Program Files (x86)\PowerShell\7\pwsh.exe",
            "/usr/local/bin/pwsh",
            "/usr/bin/pwsh",
        ]

        for path in paths_maybe:
            if os.path.exists(path):
                return path
        try:
            result = subprocess.run(
                ["where", "pwsh"] if os.name == "nt" else ["which", "pwsh"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def handle_stdout(self):

        stream = self.processes[self.current_process_index]
        data = stream.readAllStandardOutput().data() 

        # data = (
        #     self.processes[self.current_process_index]
        #     .readAllStandardOutput()
        #     .data()
        #     .decode()
        # )

        decoded_data = data.decode('utf-8', errors='replace')


        # Enter the decoded text into the terminal
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)
        self.insert_colored_text(decoded_data)
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)
        if not decoded_data.endswith("\n"):
            self.terminal.insertPlainText("\n")
        self.display_prompt()


    def handle_stderr(self):
        stream = self.processes[self.current_process_index]
        data = stream.readAllStandardOutput().data() 

        decoded_data = data.decode('utf-8', errors='replace')

        self.terminal.moveCursor(QTextCursor.MoveOperation.End)
        self.insert_colored_text(decoded_data, QColor(255, 0, 0))  # Red color for errors
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)
        if not decoded_data.endswith("\n"):
            self.terminal.insertPlainText("\n")
        self.display_prompt()

    def display_prompt(self):
        self.terminal.appendPlainText(self.prompt)
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)

    def insert_colored_text(self, text, default_color=QColor(255, 255, 255)):
        cursor = self.terminal.textCursor()

        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        segments = ansi_escape.split(text)
        codes = ansi_escape.findall(text)

        current_color = default_color
        for i, segment in enumerate(segments):
            if segment:
                format = cursor.charFormat()
                format.setForeground(current_color)
                cursor.setCharFormat(format)
                cursor.insertText(segment)

            if i < len(codes):
                code = codes[i]
                if code == "\x1B[0m":
                    current_color = default_color
                elif code.startswith("\x1B[38;2;"):
                    rgb = code[7:-1].split(";")
                    if len(rgb) == 3:
                        current_color = QColor(int(rgb[0]), int(rgb[1]), int(rgb[2]))

        self.terminal.setTextCursor(cursor)

    def keyPressEvent(self, event: QKeyEvent):
        if event is not None:
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                self.execute_command()
            elif event.key() == Qt.Key.Key_Up:
                self.show_previous_command()
            elif event.key() == Qt.Key.Key_Down:
                self.show_next_command()
            else:
                super().keyPressEvent(event)

    def terminal_key_press_event(self, event: QKeyEvent):
        cursor = self.terminal.textCursor()

        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.execute_command()
        elif event.key() == Qt.Key.Key_Backspace:
            if len(self.current_command) > 0:
                self.current_command = self.current_command[:-1]
                cursor.deletePreviousChar()
        elif event.key() == Qt.Key.Key_Up:
            self.show_previous_command()
        elif event.key() == Qt.Key.Key_Down:
            self.show_next_command()
        elif event.key() == Qt.Key.Key_Left:
            if cursor.positionInBlock() > len(self.prompt):
                cursor.movePosition(QTextCursor.MoveOperation.Left)
        elif event.key() == Qt.Key.Key_Home:
            cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
            cursor.movePosition(
                QTextCursor.MoveOperation.Right,
                QTextCursor.MoveMode.MoveAnchor,
                len(self.prompt),
            )
        else:
            if cursor.positionInBlock() >= len(self.prompt):
                self.current_command += event.text()
                QPlainTextEdit.keyPressEvent(self.terminal, event)

    def execute_command(self):
        self.terminal.appendPlainText("")
        self.processes[self.current_process_index].write(
            self.current_command.encode() + b"\n"
        )
        self.command_history.append(self.current_command)
        self.history_index = len(self.command_history)
        self.command_input.emit(self.current_command)
        self.current_command = ""

    def show_previous_command(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.show_command_from_history()

    def show_next_command(self):
        if self.history_index < len(self.command_history):
            self.history_index += 1
            self.show_command_from_history()

    def show_command_from_history(self):
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        cursor.movePosition(
            QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.KeepAnchor
        )
        cursor.removeSelectedText()

        if self.history_index < len(self.command_history):
            self.current_command = self.command_history[self.history_index]
        else:
            self.current_command = ""

        cursor.insertText(f"{self.prompt}{self.current_command}")

    def run_command(self, command):
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)
        self.terminal.insertPlainText(f"{self.prompt}{command}\n")
        self.processes[self.current_process_index].write(command.encode() + b"\n")

    # def run_file(self, file_path):
    #     file_name = os.path.basename(file_path)
    #     self.run_command(file_name)

    # def change_directory(self, new_path):
    #     self.run_command(f"cd '{new_path}'")

    # def parse_ansi_codes(self, text):
    #     ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    #     return ansi_escape.sub("", text)

class TerminalDock(QDockWidget):
    # def __init__(self, parent):
    def __init__(self, parent):

        super().__init__()
        self.setObjectName('Docks')
        self.setStyleSheet(get_css_style())
        self.clearFocus()
        self.setMaximumHeight(0)
        self.hide()

        self.termEmulator = TerminalEmulator(self)
        self.setWidget(self.termEmulator)
        self.termEmulator.show()
        self.custom_title = QLabel("Terminal")
        self.custom_title.setStyleSheet("background-color: transparent; color: white; padding: 4px; border-radius: 10px; margin: 4px")
        self.setTitleBarWidget(self.custom_title)

        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)


class findingText(QLineEdit):
    def __init__(self, bawky_parent, main_text):
        super().__init__()
        self.main_text = main_text
        self.setObjectName('Finder')


        self.setStyleSheet(get_css_style())
        bawky_parent.addWidget(self)
        self.setPlaceholderText("Find...🔎")
        self.setFixedWidth(250)

        self.hide()
        self.setMaximumHeight(0)

        self.textChanged.connect(lambda: self.changed(main_text))
        self.returnPressed.connect(lambda: self.find_next(main_text))



    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Escape:
            # self.hide()
            animatePanel(self, self.main_text.window, show=False)
            self.main_text.setFocus()


        super().keyPressEvent(event)

    def find_next(self, main_text):
        if not main_text.find(self.text().lower()):
            main_text.moveCursor(QTextCursor.MoveOperation.Start)
            main_text.find(self.text().lower())

    def changed(self, main_text):
        main_text.moveCursor(QTextCursor.MoveOperation.Start)
        main_text.find(self.text().lower())


class GotoBlock(QLineEdit):
    def __init__(self, main_text):
        super().__init__(main_text)
        self.main_text = main_text
        self.setObjectName('GoLine')
        self.setStyleSheet(get_css_style())
        self.setPlaceholderText("Go to Line...")
        self.textChanged.connect(lambda: self.goto_line(main_text))
        self.cursor_ = main_text.textCursor()
        self.setFocus()
        self.setFixedWidth(150)

        self.top_right_in_editor()

        self.raise_()
        self.show()

    def top_right_in_editor(self):
        editor = self.main_text.viewport()
        editor_rect = editor.geometry()
        x = editor_rect.width() - self.width() - 5
        y = 15
        self.move(x, y)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            # animatePanel(self, self.main_text.window, False)
            self.deleteLater()
            self.main_text.setFocus()
        else:
            super().keyPressEvent(event)

    def goto_line(self, main_text):
        if self.text().isdigit():
            line_number = int(self.text())
            block = main_text.document().findBlockByLineNumber(line_number - 1)
            if block.isValid():
                self.cursor_.setPosition(block.position())
                main_text.setTextCursor(self.cursor_)


class WelcomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QVBoxLayout(self)

        self.full_text = f"Welcome, {os.getlogin()}!"
        self.current_index = 0

        self.welcome_user = QLabel("", self)
        self.welcome_user.setObjectName('Greeting')
        self.welcome_user.setStyleSheet(get_css_style())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(120)

        self.setStyleSheet(get_css_style())
        now = datetime.now()
        date = now.strftime('%A, %B %d')
        current_date = QLabel(date)
        current_date.setAlignment(Qt.AlignmentFlag.AlignCenter)

        current_date.setObjectName('Date')
        current_date.setStyleSheet(get_css_style())

        shortcut_1 = QLabel(f'Press <span style="font-family: monospace; background-color: #2d2d2d; padding: 2px 4px; border: 1px; border-radius: 15px;">{Hide_Show_viewer()}</span> to open Directory Viewer and start working!')
        shortcut_1.setAlignment(Qt.AlignmentFlag.AlignCenter)


        shortcut_1.setObjectName('ShortCutTexts')
        shortcut_1.setStyleSheet(get_css_style())

        shortcut_2 = QLabel(f'Press <span style="font-family: monospace; background-color: #2d2d2d; padding: 2px 4px; border: 1px; border-radius: 15px;">{Show_Hide_Shortcuts()}</span> to open Shorcut List')
        shortcut_2.setAlignment(Qt.AlignmentFlag.AlignCenter)


        shortcut_2.setObjectName('ShortCutTexts')
        shortcut_2.setStyleSheet(get_css_style())

        shortcut_3 = QLabel(f'Press <span style="font-family: monospace; background-color: #2d2d2d; padding: 2px 4px; border: 1px; border-radius: 15px;">{OpenStyleFile()}</span> to open CSS file')
        shortcut_3.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)


        shortcut_3.setObjectName('ShortCutTexts')
        shortcut_3.setStyleSheet(get_css_style())


        shortcut_4 = QLabel(f'Press <span style="font-family: monospace; background-color: #2d2d2d; padding: 2px 4px; border: 1px; border-radius: 15px;">{OpenConfigFile()}</span> to open Configuration file')
        shortcut_4.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)


        shortcut_4.setObjectName('ShortCutTexts')
        shortcut_4.setStyleSheet(get_css_style())


        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet(get_css_style())

        line.setObjectName("horizontalLines")



        self.setLayout(self._layout)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addStretch(1)
        self._layout.addWidget(self.welcome_user, alignment = Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(current_date, alignment = Qt.AlignmentFlag.AlignHCenter)
        line.setStyleSheet("background-color: #888;")
        line.setFixedHeight(2)
        line.setFixedWidth(500)
        self._layout.addWidget(line, alignment = Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(shortcut_1, alignment = Qt.AlignmentFlag.AlignHCenter)

        self._layout.setSpacing(10)
        self._layout.addStretch(1)
        self._layout.addWidget(shortcut_2, alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self._layout.addWidget(shortcut_3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self._layout.addWidget(shortcut_4, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.setFocus()
        # self.show()

    def update_text(self):
        if self.current_index <= len(self.full_text):
            self.welcome_user.setText(self.full_text[:self.current_index])
            self.current_index += 1
        else:
            self.timer.stop()


class ListShortCuts(QWidget):
    def __init__(self):
        super().__init__()

        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet(get_css_style())

        line.setObjectName("horizontalLines")


        self.layout_.addWidget(line)

        shortcut_1 = QLabel(f'Save Current File: <span style="background-color: #2d2d2d">{SaveCurrentFile()}</span>')
        shortcut_2 = QLabel(f'Show/Hide Directory Viewer: <span style="background-color: #2d2d2d">{Hide_Show_viewer()}</span>')
        shortcut_3 = QLabel(f'Run current python file: <span style="background-color: #2d2d2d">{RunCurrentPythonFile()}</span>')
        shortcut_4 = QLabel(f'Kill Terminal: <span style="background-color: #2d2d2d">{KillTerminalSession()}</span>')
        shortcut_5 = QLabel(f'Show/Hide Terminal: <span style="background-color: #2d2d2d">{Hide_Show_term()}</span>')
        shortcut_6 = QLabel(f'Go to line: <span style="background-color: #2d2d2d">{GotoBlock_()}</span>')
        shortcut_7 = QLabel(f'Find text: <span style="background-color: #2d2d2d">Ctrl + F</span>')
        # shortcut_8 = QLabel(f'Get Error: <span style="background-color: #2d2d2d">Ctrl + Shift + C</span>')
        shortcut_8 = QLabel(f'Open CSS file: <span style="background-color: #2d2d2d">{OpenStyleFile()}</span>')


        shortcut_9 = QLabel(f'Move Tab to left: <span style="background-color: #2d2d2d">{MoveTabLeft()}</span>')
        shortcut_10 = QLabel(f'Move tab to right: <span style="background-color: #2d2d2d">{MoveTabRight()}</span>')
        shortcut_11 = QLabel(f'Remove current tab: <span style="background-color: #2d2d2d">{RemoveCurrentTab()}</span>')
        shortcut_12 = QLabel(f'Remove line indent: <span style="background-color: #2d2d2d">{removeIndentCurrent()}</span>')
        shortcut_13 = QLabel(f'Indet line: <span style="background-color: #2d2d2d">{IndentCurrentLine()}</span>')
        shortcut_14 = QLabel(f'Increase font size: <span style="background-color: #2d2d2d">{IncreaseFont()}</span>')
        shortcut_15 = QLabel(f'Reduce font size: <span style="background-color: #2d2d2d">{DecreaseFont()}</span>')
        shortcut_16 = QLabel(f'Go to new line: <span style="background-color: #2d2d2d">{newLine()}</span>')
        shortcut_17 = QLabel(f'Remove current line: <span style="background-color: #2d2d2d">{DeleteLine()}</span>')
        shortcut_18 = QLabel(f'Open Configuration file: <span style="background-color: #2d2d2d">{OpenConfigFile()}</span>')
        shortcut_19 = QLabel(f'Show/Hide Git Panel: <span style="background-color: #2d2d2d">{Hide_Show_gitpanel()}</span>')
        shortcut_20 = QLabel(f'Select Folder: <span style="background-color: #2d2d2d">{SelectFolder()}</span>')

        shortcut_21 = QLabel(f'Close: <span style="background-color: #2d2d2d">{Close()}</span>')
        shortcut_22 = QLabel(f'Minimize: <span style="background-color: #2d2d2d">{Minimize()}</span>')
        shortcut_23 = QLabel(f'Restart: <span style="background-color: #2d2d2d">{Reboot()}</span> Not available on binary file format.')
        shortcut_24 = QLabel(f'Maximize: <span style="background-color: #2d2d2d">{Maximize()}</span>')

        shortcut_25 = QLabel(f'Make New File: <span style="background-color: #2d2d2d">Ctrl + F</span>')
        shortcut_26 = QLabel(f'Make New Folder: <span style="background-color: #2d2d2d">Ctrl + D</span>')
        shortcut_27 = QLabel(f'Remove Hovered File: <span style="background-color: #2d2d2d">Ctrl + K</span>')
        shortcut_28 = QLabel(f'Remove Hovered Folder: <span style="background-color: #2d2d2d">Ctrl + J</span>')

        self.left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()
        self.left_column.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.right_column.setAlignment(Qt.AlignmentFlag.AlignTop)

        # for shortcut in [shortcut_1, shortcut_2, shortcut_3, shortcut_4, shortcut_5, shortcut_6, shortcut_7, shortcut_8, shortcut_9, shortcut_19, shortcut_21, shortcut_23]:
        # for shortcut in [shortcut_1, shortcut_2, shortcut_3, shortcut_4, shortcut_5, shortcut_6, shortcut_25, shortcut_28 ,shortcut_7, shortcut_8, shortcut_9, shortcut_19, shortcut_21, shortcut_23]:
        for shortcut in [shortcut_1, shortcut_3, shortcut_20, shortcut_6, shortcut_7, shortcut_2, shortcut_19, shortcut_5, shortcut_4, shortcut_9, shortcut_10, shortcut_11, shortcut_21, shortcut_23]:


            shortcut.setObjectName('ShortCutTexts')
            shortcut.setStyleSheet(get_css_style())
            self.left_column.addWidget(shortcut)


        # dway 7
        # for shortcut in [shortcut_10, shortcut_11, shortcut_12, shortcut_13, shortcut_14, shortcut_15, shortcut_16, shortcut_17, shortcut_18, shortcut_20, shortcut_22, shortcut_24]:
        # for shortcut in [shortcut_10, shortcut_11, shortcut_12, shortcut_13, shortcut_14, shortcut_15, shortcut_26, shortcut_27 ,shortcut_16, shortcut_17, shortcut_18, shortcut_20, shortcut_22, shortcut_24]:
        for shortcut in [shortcut_25, shortcut_26, shortcut_27, shortcut_28, shortcut_12, shortcut_13, shortcut_14, shortcut_15 ,shortcut_16, shortcut_17, shortcut_8, shortcut_18, shortcut_22, shortcut_24]:


            shortcut.setObjectName('ShortCutTexts')
            shortcut.setStyleSheet(get_css_style())
            self.right_column.addWidget(shortcut)

        self.h_layout = QHBoxLayout()
        self.h_layout.addLayout(self.left_column)
        self.h_layout.setSpacing(10)
        self.h_layout.addStretch()
        self.h_layout.addLayout(self.right_column)

        self.layout_.addLayout(self.h_layout)

        self.hide()
        self.setMaximumHeight(0)

class GitDock(QDockWidget):
    def __init__(self, parent):

        super().__init__()
        # Only call git functions if git is installed
        if is_gitInstalled():
            is_downloaded(MessageBox)
        self.thread_pool = QThreadPool()
        self.setObjectName('Docks')
        self.setStyleSheet(get_css_style())
        self.clearFocus()
        self.setWindowTitle('Git Panel')
        content_widget = QWidget()
        self.layout_ = QVBoxLayout()
        content_widget.setObjectName('GitPanel')
        content_widget.setStyleSheet(get_css_style())
        self.gitTimers()

        self.labels()
        self._layout()

        self.setWidget(content_widget)
        content_widget.setLayout(self.layout_)

        self.setTitleBarWidget(self.custom_title)

        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        # parent.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self)

        self.hide()
        self.setMaximumHeight(0)

        self.checking()


    def _layout(self):
        self.layout_.addWidget(self.users_profile)
        self.layout_.addWidget(self.user_username)
        self.layout_.addStretch()

        self.layout_.addWidget(self.commit_info)
        self.layout_.addWidget(self.latest_commit)
        self.layout_.addWidget(self.commit)
        self.layout_.addWidget(self.last_commit)
        self.layout_.setSpacing(10)
        self.layout_.addWidget(self.untracked_header)
        self.layout_.setSpacing(10)
        self.layout_.addWidget(self.untracked_files)
        self.layout_.addWidget(self.header_changes)
        self.layout_.addWidget(self.show_changes)
        # self.layout_.addStretch()
        # self.layout_.addStretch()
        self.layout_.addStretch()

        self.layout_.addWidget(self.repo_info)
        self.layout_.addWidget(self.repo_name)
        self.layout_.addWidget(self.remote_url)
        self.layout_.addWidget(self.active_branch_name)
        self.layout_.addStretch()


    def labels(self):
        self.commit = QLabel()
        self.commit.setObjectName('TotalCommits')
        self.commit.setStyleSheet(get_css_style())

        self.insertions = QLabel()
        self.deletion = QLabel()

        self.active_branch_name = QLabel()
        self.active_branch_name.setObjectName('ActiveBranch')
        self.active_branch_name.setStyleSheet(get_css_style())

        # Only call git functions if git is installed
        if is_gitInstalled():
            self.remote_url = QLabel(get_github_remote_url(MessageBox))
        else:
            self.remote_url = QLabel("Git not installed")
        # self.remote_url.setOpenExternalLinks(True)
        # self.remote_url.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.remote_url.setObjectName('RemoteURL')
        self.remote_url.setStyleSheet(get_css_style())

        pixmap = QPixmap('icons/github/user_profile/users_profile.png')
        circular_profile = self.rounded_pixmap(pixmap, 96)


        self.users_profile = QLabel()
        self.users_profile.setPixmap(circular_profile)
        self.users_profile.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.users_profile.setObjectName('UserProfile')
        self.users_profile.setStyleSheet(get_css_style())

        # Only call git functions if git is installed
        if is_gitInstalled():
            self.user_username = QLabel(get_github_username())
        else:
            self.user_username = QLabel("Git not installed")
        self.user_username.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_username.setObjectName('Username')
        self.user_username.setStyleSheet(get_css_style())

        self.show_changes = QLabel()
        self.show_changes.setObjectName('fileChanges')
        self.show_changes.setStyleSheet(get_css_style())

        self.header_changes = QLabel('File Changes:')
        self.header_changes.setObjectName('fileChanges')
        self.header_changes.setStyleSheet(get_css_style())

        self.commit_info = QLabel("Commit Info:")

        self.commit_info.setObjectName('CommitInfo')
        self.commit_info.setStyleSheet(get_css_style())

        self.latest_commit = QLabel()
        self.latest_commit.setObjectName('CommitTime')
        self.latest_commit.setStyleSheet(get_css_style())

        self.last_commit = QLabel()
        self.last_commit.setObjectName('CommitMessage')
        self.last_commit.setStyleSheet(get_css_style())


        self.repo_info = QLabel("Repository Info:")
        self.repo_info.setObjectName('RepoInfo')
        self.repo_info.setStyleSheet(get_css_style())

        self.untracked_files = QLabel()
        self.untracked_files.setObjectName('UntrackedFiles')
        self.untracked_files.setStyleSheet(get_css_style())

        self.untracked_header = QLabel("Untracked Files:")
        self.untracked_header.setObjectName('UntrackedFiles')
        self.untracked_header.setStyleSheet(get_css_style())


        # Only call git functions if git is installed
        if is_gitInstalled():
            self.repo_name = QLabel(f"Repository name {get_reopName()}")
        else:
            self.repo_name = QLabel("Repository name: Git not installed")
        self.repo_name.setObjectName('RepoName')
        self.repo_name.setStyleSheet(get_css_style())

        self.no_repo_img = QLabel()
        self.no_repo_img.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.no_repo_img.setObjectName('RepoNotFound')
        self.no_repo_img.setStyleSheet(get_css_style())

        self.no_repo_text = QLabel("No repository in current directory")
        self.no_repo_text.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.no_repo_text.setObjectName('RepoNotFound')
        self.no_repo_text.setStyleSheet(get_css_style())

        pixmap = QPixmap('icons/github/github.png')
        scaled = pixmap.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.no_repo_img.setPixmap(scaled)

        self.image_container = QWidget()
        image_layout = QVBoxLayout(self.image_container)

        image_layout.addStretch()
        image_layout.addWidget(self.no_repo_img, alignment=Qt.AlignmentFlag.AlignHCenter)
        image_layout.addWidget(self.no_repo_text, alignment=Qt.AlignmentFlag.AlignHCenter)
        image_layout.addStretch()

        image_layout.setContentsMargins(0, 0, 0, 0)
        self.image_container.setLayout(image_layout)

        # self.layout_.addWidget(self.image_container, alignment = Qt.AlignmentFlag.AlignHCenter)

        self.custom_title = QLabel("Git Panel")
        self.custom_title.setObjectName('DockTitles')
        self.custom_title.setStyleSheet(get_css_style())
        # self.custom_title.setStyleSheet("background-color: transparent; color: white; padding: 4px; border-radius: 10px; margin: 4px")
        self.remote_url.hide()
        self.active_branch_name.hide()
        self.user_username.hide()
        self.users_profile.hide()
        self.repo_info.hide()
        self.repo_name.hide()
        self.commit.hide()
        self.commit_info.hide()
        self.last_commit.hide()
        self.latest_commit.hide()
        self.untracked_files.hide()
        self.untracked_header.hide()
        self.show_changes.hide()
        self.header_changes.hide()

    def rounded_pixmap(self, pixmap: QPixmap, radius: int = 128) -> QPixmap:
        size = min(pixmap.width(), pixmap.height())
        rounded = QPixmap(radius * 2, radius * 2)
        rounded.fill(Qt.GlobalColor.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, radius * 2, radius * 2)
        painter.setClipPath(path)

        scaled = pixmap.scaled(radius * 2, radius * 2, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        source_rect = QRectF((scaled.width() - radius * 2) / 2, (scaled.height() - radius * 2) / 2, radius * 2, radius * 2)
        painter.drawPixmap(QRectF(0, 0, radius * 2, radius * 2), scaled, source_rect)
        painter.end()

        return rounded

    def changes(self, file_changes: dict):
        text = ""
        for file, info in file_changes.items():
            if info['insertions'] != 0 or info['deletions'] != 0:
                text += f"""    &nbsp;&nbsp;&nbsp;&nbsp;<b>{file}({info['change_type']})</b>: 
                <span style="color: green;">+{info['insertions']} insertions</span> 
                <span style="color: red;">-{info['deletions']} deletions</span><br><br>"""


        self.show_changes.setTextFormat(Qt.TextFormat.RichText)
        self.show_changes.setText(text)

    def update_git_info(self):
        # Only update git info if git is installed
        if is_gitInstalled():
            worker = GitWorker()
            worker.signals.dataReady.connect(self.update_ui)
            self.thread_pool.start(worker)

    def update_ui(self, commit_msg, branch, total, get_latest_commit_time, file_changes, untracked_files):
        # if self.isVisible() and is_init():
        if self.maximumHeight() != 0 and is_init():

            # if not is_init():


                # if self.users_profile.isVisible():
                #     self.layout_.addWidget(self.image_container, alignment = Qt.AlignmentFlag.AlignHCenter)
                #     # self.layout_.removeWidget(self.image_container)

                #     self.no_repo_img.show()
                #     self.no_repo_text.show()
                #     self.repo_name.hide()
                #     self.commit.hide()
                #     self.remote_url.hide()
                #     self.user_username.hide()
                #     self.latest_commit.hide()
                #     self.last_commit.hide()
                #     self.commit_info.hide()
                #     self.active_branch_name.hide()
                #     self.untracked_files.hide()
                #     self.untracked_header.hide()
                #     self.header_changes.hide()
                #     self.show_changes.hide()
                #     self.users_profile.hide()
                #     self.repo_info.hide()


            # else:
            if not self.users_profile.isVisible():
                self.layout_.removeWidget(self.image_container)
                self.no_repo_img.hide()
                self.no_repo_text.hide()
                self.repo_name.show()
                self.commit.show()
                self.active_branch_name.show()
                self.remote_url.show()
                self.repo_info.show()
                self.latest_commit.show()
                self.user_username.show()
                self.last_commit.show()
                self.commit_info.show()
                self.active_branch_name.show()
                self.untracked_files.show()
                self.untracked_header.show()
                self.header_changes.show()
                self.show_changes.show()
                self.users_profile.show()

            self.changes(file_changes)

            self.untracked_files.setText(f"   {untracked_files}")

            self.latest_commit.setText(f"↳ Message: {commit_msg}")
            self.active_branch_name.setText(f"Branch: <code>{branch}</code>")
            self.commit.setText(f"↳ Total Commits: {str(total)}")
            self.last_commit.setText(f"↳ Last Committed: {get_latest_commit_time}")

        elif not is_init():
            if self.users_profile.isVisible():
                self.layout_.addWidget(self.image_container, alignment = Qt.AlignmentFlag.AlignHCenter)

                self.no_repo_img.show()
                self.no_repo_text.show()
                self.repo_name.hide()
                self.commit.hide()
                self.remote_url.hide()
                self.user_username.hide()
                self.latest_commit.hide()
                self.last_commit.hide()
                self.commit_info.hide()
                self.active_branch_name.hide()
                self.untracked_files.hide()
                self.untracked_header.hide()
                self.header_changes.hide()
                self.show_changes.hide()
                self.users_profile.hide()
                self.repo_info.hide()


    def checking(self):
        if not is_init():
            if self.users_profile.isVisible():
                self.layout_.addWidget(self.image_container, alignment = Qt.AlignmentFlag.AlignHCenter)


                self.no_repo_img.show()
                self.no_repo_text.show()
                self.repo_name.hide()
                self.commit.hide()
                self.remote_url.hide()
                self.user_username.hide()
                self.latest_commit.hide()
                self.last_commit.hide()
                self.commit_info.hide()
                self.active_branch_name.hide()
                self.untracked_files.hide()
                self.untracked_header.hide()
                self.header_changes.hide()
                self.show_changes.hide()
                self.users_profile.hide()


        else:
            if not self.users_profile.isVisible():
                self.layout_.removeWidget(self.image_container)
                self.no_repo_img.hide()
                self.no_repo_text.hide()
                self.repo_name.show()
                self.commit.show()
                self.active_branch_name.show()
                self.remote_url.show()
                self.repo_info.show()
                self.latest_commit.show()
                self.user_username.show()
                self.last_commit.show()
                self.commit_info.show()
                self.active_branch_name.show()
                self.untracked_files.show()
                self.untracked_header.show()
                self.header_changes.show()
                self.show_changes.show()
                self.users_profile.show()

    def gitTimers(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_git_info)
        # Only start the timer if git is installed
        if is_gitInstalled():
            self.timer.start(1500)


class MessageBox(QMessageBox):
    def __init__(self, text, link = None, add_buttons = False):
        super().__init__()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setText(text)
        if link:
            self.setTextFormat(Qt.TextFormat.RichText)
            self.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

            label = self.findChild(QLabel)
            if label:
                label.setOpenExternalLinks(False)
                label.linkActivated.connect(self.open_link)

        self.setObjectName('MessageBox')
        self.setStyleSheet(get_css_style())

        ok_button = QPushButton(self)
        ok_button.setText('Ok')

        ok_button.setObjectName('MessageBoxSave')
        ok_button.setStyleSheet(get_css_style())

        cancel = QPushButton(self)
        cancel.setText('Cancel')

        cancel.setObjectName('MessageBoxCancel')
        cancel.setStyleSheet(get_css_style())

        pixmap = QPixmap('icons/messagebox/warning.png')
        pixmap.size()
        scaled_pixmap = pixmap.scaled(98, 98, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.setIconPixmap(scaled_pixmap)


        self.addButton(ok_button, QMessageBox.ButtonRole.YesRole)
        self.addButton(cancel, QMessageBox.ButtonRole.RejectRole)
        if add_buttons:
            to_kurdish = QPushButton(self)
            to_kurdish.setObjectName('MessageBoxSaveNot')
            to_kurdish.setText('کوردی')
            to_kurdish.setStyleSheet(get_css_style())
            self.addButton(to_kurdish, QMessageBox.ButtonRole.AcceptRole)
            to_kurdish.clicked.disconnect()  
            to_kurdish.clicked.connect(lambda: self.change(to_kurdish))


        self.exec()


        if link:
            if self.clickedButton() == ok_button:
                webbrowser.open(link)

    def change(self, button: QPushButton):
        if button.text() == 'کوردی':
            self.setText("بەخێر بێت بۆ Kryypto!\n\n"
f"پێش ئەوەی دەست پێ بکەیت configuration file بکەوە بە بەکارهێنانی {OpenConfigFile()}\n"
"وە برۆ بۆ بەشی [Python] بۆ pythoninterpreter\n"
"وە لەوێ شوێنی python.exe دانێ.\n"
"ئەگەر نازانی شۆێنی، دەتوانیت CMD کەیتەوەو بنوسیت: where python"
"بەوە شوێنەکەت پیشان ئەیات.")
            button.setText('English')

        else:
            button.setText('کوردی')
            self.setText(f'Welcome to Kryypto!\n\nbefore you get started please open the configuration file by pressing {OpenConfigFile()} after this Message Box, go to [Python]\npythoninterpreter\nand put your python.exe.\n\nIf you dont know where it is you can open CMD and type: where python\nthis will give you the python interpreter path!')

    def open_link(self, url):
        webbrowser.open(url.toString())

def pop_messagebox(parent, event, tab_bar, use_events):
    box = QMessageBox(parent)

    box.setWindowFlag(Qt.WindowType.FramelessWindowHint)

    box.setText('Hey!\nIt looks like you are trying to close IDE without saving your progress\nDo you really want your work go in vain?')

    box.setObjectName('MessageBox')
    box.setStyleSheet(get_css_style())

    save_file = QPushButton(box)
    save_file.setText('Save File')

    save_file.setObjectName('MessageBoxSave')
    save_file.setStyleSheet(get_css_style())

    dont_save = QPushButton(box)
    dont_save.setText("Don't Save")

    dont_save.setObjectName('MessageBoxSaveNot')
    dont_save.setStyleSheet(get_css_style())

    cancel = QPushButton(box)
    cancel.setText('Cancel')

    cancel.setObjectName('MessageBoxCancel')
    cancel.setStyleSheet(get_css_style())

    pixmap = QPixmap('icons/messagebox/warning.png')
    pixmap.size()

    scaled_pixmap = pixmap.scaled(98, 98, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
    box.setIconPixmap(scaled_pixmap)


    box.addButton(save_file, QMessageBox.ButtonRole.YesRole)
    box.addButton(dont_save, QMessageBox.ButtonRole.NoRole)
    box.addButton(cancel, QMessageBox.ButtonRole.RejectRole)

    box.exec()


    if use_events:
        if box.clickedButton() == save_file:
            tab_bar.save_current_file()

            event.accept()
        elif box.clickedButton() == dont_save:
            event.accept()
        else:
            event.ignore()