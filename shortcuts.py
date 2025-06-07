from PyQt6.QtGui import QShortcut, QKeySequence, QTextCursor
from PyQt6.QtGui import QFont


class MainTextShortcuts:
    def __init__(self, parent, completer):
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

    def remove_current_line(self, text_edit):

    
        cursor = text_edit.textCursor()
        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)  # capture newline

        cursor.removeSelectedText()

        cursor.endEditBlock()
        text_edit.setTextCursor(cursor)

    def goto_next_block(self, text_edit):
        cursor = text_edit.textCursor()

        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        cursor.insertBlock()
        text_edit.setTextCursor(cursor)


    def add_indentation(self, text_edit):
        cursor = text_edit.textCursor()
        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

        line_text = cursor.selectedText()

        new_line = "    " + line_text

        cursor.insertText(new_line)
        cursor.endEditBlock()

    def remove_indentation(self, text_edit):
        cursor = text_edit.textCursor()
        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

        line_text = cursor.selectedText()

        stripped_line = line_text[4:] if line_text.startswith("    ") else line_text.lstrip()

        cursor.insertText(stripped_line)
        cursor.endEditBlock()

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
