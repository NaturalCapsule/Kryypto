from PyQt6.QtGui import QShortcut, QKeySequence, QTextCursor
from PyQt6.QtGui import QFont


class MainTextShortcuts:
    def __init__(self, parent, completer):
        self.font_size = 19

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

    def remove_current_line(self, text_edit):
        cursor = text_edit.textCursor()
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)
        cursor.removeSelectedText()
        if not cursor.atEnd():
            cursor.deleteChar()
        text_edit.setTextCursor(cursor)
    
    def goto_next_block(self, text_edit):
        cursor = text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        cursor.insertBlock()
        text_edit.setTextCursor(cursor)

    def increase_font(self, text_edit):
        self.font_size += 1
        text_edit.setFont(QFont("Maple Mono", self.font_size))

    def reduce_font(self, text_edit):
        self.font_size -= 1

        if self.font_size <= 1:
            self.font_size = 1
        text_edit.setFont(QFont("Maple Mono", self.font_size))
    
    def pressed(self, completer):
        # print("Ctrl + Space has been pressed")
        completer.popup().show()
