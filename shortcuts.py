import re
from PyQt6.QtGui import QShortcut, QKeySequence, QTextCursor
from PyQt6.QtGui import QFont


class MainTextShortcuts:
    def __init__(self, parent, completer, tab):
        self.font_size = 19
        # self.num_lines = num_lines

        delete_line = QShortcut(QKeySequence("Ctrl+Shift+K"), parent)
        delete_line.activated.connect(lambda: self.remove_current_line(parent))

        new_line = QShortcut(QKeySequence("Ctrl+Return"), parent)
        new_line.activated.connect(lambda: self.goto_next_block(parent))

        increase_font = QShortcut(QKeySequence("Ctrl+="), parent)
        increase_font.activated.connect(lambda: self.increase_font(parent))

        reduce_font = QShortcut(QKeySequence("Ctrl+-"), parent)
        reduce_font.activated.connect(lambda: self.reduce_font(parent))

        show_completer = QShortcut(QKeySequence("Ctrl+Space"), parent)
        show_completer.activated.connect(lambda: self.pressed(completer))

        indent_line = QShortcut(QKeySequence("Ctrl+]"), parent)
        indent_line.activated.connect(lambda: self.add_indentation(parent))


        remove_indent = QShortcut(QKeySequence("Ctrl+["), parent)
        remove_indent.activated.connect(lambda: self.remove_indentation(parent))

        comment = QShortcut(QKeySequence("Ctrl+/"), parent)
        comment.activated.connect(lambda: self.comment(parent))

        remove_current_tab = QShortcut(QKeySequence("Ctrl+Shift+R"), parent)
        remove_current_tab.activated.connect(lambda: self.remove_tab_(tab))

        # save_file = QShortcut(QKeySequence("Ctrl+S"), parent)
        # save_file.activated.connect(lambda: self.save_file(parent))



    def remove_current_line(self, text_edit):
        cursor = text_edit.textCursor()

        text_edit.setUpdatesEnabled(False)
        text_edit.blockSignals(True)
        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)

        cursor.removeSelectedText()

        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)

        cursor.endEditBlock()
        text_edit.setTextCursor(cursor)
        text_edit.setUpdatesEnabled(True)
        text_edit.blockSignals(False)

    def goto_next_block(self, text_edit):
        cursor = text_edit.textCursor()
        text_edit.setUpdatesEnabled(False)
        text_edit.blockSignals(True)
        cursor.beginEditBlock()
        
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        text_edit.setTextCursor(cursor)

        block_text = cursor.block().text()
        indent_match = re.match(r'^(\s*)', block_text)
        current_indent = indent_match.group(1) if indent_match else ""
        if block_text.strip().endswith(":"):
            new_indent = current_indent + " " * 4
        else:
            new_indent = current_indent
        cursor.insertText("\n" + new_indent)

        cursor.endEditBlock()
        text_edit.setUpdatesEnabled(True)
        text_edit.blockSignals(False)

    def add_indentation(self, text_edit):
        cursor = text_edit.textCursor()
        text_edit.setUpdatesEnabled(False)
        text_edit.blockSignals(True)
        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

        line_text = cursor.selectedText()

        new_line = "    " + line_text

        cursor.insertText(new_line)

        cursor.endEditBlock()
        text_edit.setUpdatesEnabled(True)
        text_edit.blockSignals(False)

    def remove_indentation(self, text_edit):
        cursor = text_edit.textCursor()
        text_edit.setUpdatesEnabled(False)
        text_edit.blockSignals(True)

        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

        line_text = cursor.selectedText()

        stripped_line = line_text[4:] if line_text.startswith("    ") else line_text.lstrip()

        cursor.insertText(stripped_line)
        cursor.endEditBlock()

        text_edit.setUpdatesEnabled(True)
        text_edit.blockSignals(False)


    def increase_font(self, text_edit):
        self.font_size += 1
        text_edit.setFont(QFont("Maple Mono", self.font_size))
        # self.num_lines = QFont('Maple Mono'), self.font_size


    def reduce_font(self, text_edit):
        self.font_size -= 1

        if self.font_size <= 1:
            self.font_size = 1
        text_edit.setFont(QFont("Maple Mono", self.font_size))
    
    def pressed(self, completer):
        completer.popup().show()

    def comment(self, text_edit):
        cursor = text_edit.textCursor()
        text_edit.setUpdatesEnabled(False)
        text_edit.blockSignals(True)
        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

        line_text = cursor.selectedText()

        leading_spaces = len(line_text) - len(line_text.lstrip())
        indent = line_text[:leading_spaces]
        content = line_text[leading_spaces:]

        if content.startswith("#"):
            new_line = indent + content[1:].lstrip()
        else:
            new_line = indent + "# " + content

        cursor.insertText(new_line)

        cursor.endEditBlock()
        text_edit.setUpdatesEnabled(True)
        text_edit.blockSignals(False)

    # def save_file(self, text_edit):
    #     code = text_edit.toPlainText()
    #     with open ('test.txt', 'w') as f:
    #         f.write(code)
    #         f.close()

    def remove_tab_(self, tab):
        current_index = tab.currentIndex()
        tab.removeTab(current_index)


class FileDockShortcut:
    def __init__(self, parent, file_dock, file_view, doc_string, doc_panel, main_text):
        self.file_view = file_view
        self.doc_string = doc_string
        self.doc_panel = doc_panel
        self.main_text = main_text


        show_hide_file_dock = QShortcut(QKeySequence('Ctrl+B'), parent)
        show_hide_file_dock.activated.connect(lambda: self.showHideFile(file_dock))
    
    def showHideFile(self, file_dock):
        if file_dock.isVisible():
            file_dock.hide()
            self.file_view.clearFocus()
            self.doc_string.clearFocus()
            self.doc_panel.clearFocus()
            self.main_text.setFocus()

        else:
            file_dock.show()
            self.file_view.setFocus()

