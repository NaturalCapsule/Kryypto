import re
from PyQt6.QtGui import QFont, QShortcut, QKeySequence, QTextCursor

class MainTextShortcuts:
    def __init__(self, parent, completer, tab, error_label, clipboard):
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

        # comment = QShortcut(QKeySequence("Ctrl+/"), parent)
        # comment.activated.connect(lambda: self.comment(parent))

        remove_current_tab = QShortcut(QKeySequence("Ctrl+Shift+R"), parent)
        remove_current_tab.activated.connect(lambda: self.remove_tab_(tab))

        move_tab_right = QShortcut(QKeySequence("Ctrl+Shift+T"), parent)
        move_tab_right.activated.connect(lambda: self.move_tab_right(tab))

        move_tab_left = QShortcut(QKeySequence("Ctrl+Shift+E"), parent)
        move_tab_left.activated.connect(lambda: self.move_tab_left(tab))

        get_error_text = QShortcut(QKeySequence("Ctrl+Shift+C"), parent)
        get_error_text.activated.connect(lambda: self.get_text(error_label, clipboard))

    def get_text(self, error_label, clipboard):
        if error_label:
            text = error_label.text()
            if text != '✅ No syntax errors':
                splitting = text.split(' ')
                if splitting[1] == 'Line':
                    text = splitting[3:]
                    text = ' '.join(text)
                clipboard.setText(text)

        # find_text = QShortcut(QKeySequence('Ctrl+F'), parent)
        # find_text.activated.connect(lambda: findingText(bawky_parent, parent))

    # class findingText(QLineEdit):
    #     def __init__(self, bawky_parent, main_text):
    #         super().__init__()
    #         self = QLineEdit()
    #         self.setObjectName('Finder')
    #         self.setStyleSheet(get_css_style())
    #         bawky_parent.addWidget(self)
    #         self.setFocus()
    #         self.setPlaceholderText("Search...")
    #         self.textChanged.connect(lambda: self.changed(self, main_text))
    #         self.returnPressed.connect(lambda: self.find_next(self, main_text))


    # # def find_text(self, bawky_parent, main_text):
    #     # find_text = QLineEdit()
    #     # find_text.setObjectName('Finder')
    #     # find_text.setStyleSheet(get_css_style())
    #     # bawky_parent.addWidget(find_text)
    #     # find_text.setFocus()
    #     # find_text.setPlaceholderText("Search...")
    #     # find_text.textChanged.connect(lambda: self.changed(find_text, main_text))
    #     # find_text.returnPressed.connect(lambda: self.find_next(find_text, main_text))


    #     # def find_next(self, find_text, main_text):
    #     #     if not main_text.find(find_text.text()):
    #     #         main_text.moveCursor(QTextCursor.MoveOperation.Start)
    #     #         main_text.find(find_text.text())


    #     # def changed(self, find_text, main_text):
    #     #     main_text.moveCursor(QTextCursor.MoveOperation.Start)
    #     #     main_text.find(find_text.text())


    #     def find_next(self, main_text):
    #         if not main_text.find(self.text()):
    #             main_text.moveCursor(QTextCursor.MoveOperation.Start)
    #             main_text.find(self.text())


    #     def changed(self, main_text):
    #         main_text.moveCursor(QTextCursor.MoveOperation.Start)
    #         main_text.find(self.text())


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

        if content.startswith(self.commenting):
            new_line = indent + content[1:].lstrip()
        else:
            new_line = indent + f"{self.commenting} " + content

        cursor.insertText(new_line)

        cursor.endEditBlock()
        text_edit.setUpdatesEnabled(True)
        text_edit.blockSignals(False)


    def remove_tab_(self, tab):
        current_index = tab.currentIndex()
        tab.removeTab(current_index)

    def move_tab_right(self, tab):
        current_index = tab.currentIndex() + 1
        tab.setCurrentIndex(current_index)

    def move_tab_left(self, tab):
        if tab.currentIndex() <= 0:
            tab.setCurrentIndex(0)
        else:
            current_index = tab.currentIndex() - 1
            tab.setCurrentIndex(current_index)

class FileDockShortcut:
    def __init__(self, parent, file_dock, file_view, main_text, file_description, opened_tabs):
    # def __init__(self, parent, file_dock, file_view, doc_string, doc_panel, main_text, file_description, opened_tabs):

        self.file_view = file_view
        self.main_text = main_text
        self.file_description = file_description
        self.opened_tabs = opened_tabs

        show_hide_file_dock = QShortcut(QKeySequence('Ctrl+B'), parent)
        show_hide_file_dock.activated.connect(lambda: self.showHideFile(file_dock))
    
        save_file = QShortcut(QKeySequence('Ctrl+S'), parent)
        save_file.activated.connect(self.save_file)

    def showHideFile(self, file_dock):
        if file_dock.isVisible():
            file_dock.hide()
            # self.file_view.clearFocus()
            # self.doc_string.clearFocus()
            # self.doc_panel.clearFocus()
            self.main_text.setFocus()

        else:
            file_dock.show()
            self.file_view.setFocus()


    def save_file(self):
        opened_tab = self.opened_tabs.currentIndex()
        for path, file_name in self.file_description.items():
            opened_tab = self.opened_tabs.currentIndex()
            current_tab_name = self.opened_tabs.tabText(opened_tab)

            if file_name == current_tab_name:
                with open(path, 'w', encoding = 'utf-8') as file:
                    file.write(self.main_text.toPlainText())



# class findingText(QLineEdit):
#     def __init__(self, bawky_parent, main_text):
#         super().__init__()
#         self.main_text = main_text
#         # self = QLineEdit()
#         self.setObjectName('Finder')

#         self.setStyleSheet(get_css_style())
#         bawky_parent.addWidget(self)
#         self.setFocus()
#         self.setPlaceholderText("Search...")
#         self.textChanged.connect(lambda: self.changed(main_text))
#         self.returnPressed.connect(lambda: self.find_next(main_text))



#     def keyPressEvent(self, event):
#         key = event.key()


#         if key == Qt.Key.Key_Escape:
#             self.destroy()
#             self.hide()
#             self.main_text.setFocus()
#             # return

#         super().keyPressEvent(event)

# def find_text(self, bawky_parent, main_text):
    # find_text = QLineEdit()
    # find_text.setObjectName('Finder')
    # find_text.setStyleSheet(get_css_style())
    # bawky_parent.addWidget(find_text)
    # find_text.setFocus()
    # find_text.setPlaceholderText("Search...")
    # find_text.textChanged.connect(lambda: self.changed(find_text, main_text))
    # find_text.returnPressed.connect(lambda: self.find_next(find_text, main_text))


    # def find_next(self, find_text, main_text):
    #     if not main_text.find(find_text.text()):
    #         main_text.moveCursor(QTextCursor.MoveOperation.Start)
    #         main_text.find(find_text.text())


    # def changed(self, find_text, main_text):
    #     main_text.moveCursor(QTextCursor.MoveOperation.Start)
    #     main_text.find(find_text.text())


    def find_next(self, main_text):
        if not main_text.find(self.text()):
            main_text.moveCursor(QTextCursor.MoveOperation.Start)
            main_text.find(self.text())


    def changed(self, main_text):
        main_text.moveCursor(QTextCursor.MoveOperation.Start)
        main_text.find(self.text())