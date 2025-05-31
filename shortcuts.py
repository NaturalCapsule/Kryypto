from PyQt6.QtGui import QShortcut, QKeySequence, QTextCursor


class RemoveLine:
    def __init__(self, parent):
        shortcut = QShortcut(QKeySequence("Ctrl+Shift+K"), parent)
        shortcut.activated.connect(lambda: self.remove_current_line(parent))

    def remove_current_line(self, text_edit):
        cursor = text_edit.textCursor()
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)
        cursor.removeSelectedText()
        if not cursor.atEnd():
            cursor.deleteChar()
        text_edit.setTextCursor(cursor)