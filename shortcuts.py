import re
import sys
from PyQt6.QtGui import QFont, QShortcut, QKeySequence, QTextCursor


class MainTextShortcuts:
    def __init__(self, parent, completer, tab, error_label, clipboard, bawky_parent, term, bawky_parent_, opened_tabs, file_desc, list_shortcuts, git_panel):
        self.font_size = 19
        self.terminal = term


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

        remove_current_tab = QShortcut(QKeySequence("Ctrl+Shift+R"), parent)
        remove_current_tab.activated.connect(lambda: self.remove_tab_(tab, file_desc))

        move_tab_right = QShortcut(QKeySequence("Ctrl+Shift+T"), parent)
        move_tab_right.activated.connect(lambda: self.move_tab_right(tab))

        move_tab_left = QShortcut(QKeySequence("Ctrl+Shift+E"), parent)
        move_tab_left.activated.connect(lambda: self.move_tab_left(tab))

        get_error_text = QShortcut(QKeySequence("Ctrl+Shift+C"), parent)
        get_error_text.activated.connect(lambda: self.get_text(error_label, clipboard))



        goto_block = QShortcut(QKeySequence("Ctrl+Shift+H"), parent)
        goto_block.activated.connect(lambda: self.goto_block_(parent, bawky_parent))


        # hide_show_term = QShortcut(QKeySequence("Ctrl+T"), parent)
        hide_show_term = QShortcut(QKeySequence("Ctrl+T"), bawky_parent_)

        hide_show_term.activated.connect(lambda: self.hide_show_terminal(bawky_parent_, parent))

        kill_term = QShortcut(QKeySequence("Ctrl+Shift+G"), parent)
        kill_term.activated.connect(self.kill_terminal)

        run_file = QShortcut(QKeySequence("Ctrl+N"), parent)
        run_file.activated.connect(lambda: self.run_current_file(opened_tabs, file_desc, bawky_parent_, parent))

        open_css_file = QShortcut(QKeySequence("Ctrl+Shift+S"), bawky_parent_)
        open_css_file.activated.connect(lambda: self.open_css(opened_tabs, file_desc, bawky_parent_, parent))

        open_config_file = QShortcut(QKeySequence("Ctrl+Shift+O"), bawky_parent_)
        open_config_file.activated.connect(lambda: self.open_config(opened_tabs, file_desc, bawky_parent_, parent))


        hide_show_shortcuts = QShortcut(QKeySequence("Ctrl+L"), bawky_parent_)
        hide_show_shortcuts.activated.connect(lambda: self.hide_show_shortcuts(bawky_parent_, list_shortcuts))

        hide_show_gitpanel = QShortcut(QKeySequence("Ctrl+G"), bawky_parent_)
        hide_show_gitpanel.activated.connect(lambda: self.hide_show_gitpanel(git_panel, parent))

    def hide_show_shortcuts(self, parent, list_shortcuts):
        if list_shortcuts.isVisible():
            list_shortcuts.hide()
        else:
            list_shortcuts.show()


    def open_config(self, tab, file_desc, bawky_parent, parent):
        path = "config/configuration.cfg"
        with open(path, 'r', encoding = 'utf-8') as css_file:
            if path not in file_desc.keys() and 'configuration.cfg' not in file_desc.values():
                file_desc[path] = 'configuration.cfg'
                tab.add_file(path, 'configuration.cfg')
                parent.setPlainText(css_file.read())
                parent.setFocus()


    def open_css(self, tab, file_desc, bawky_parent, parent):
        path = "config/style.css"
        with open(path, 'r', encoding = 'utf-8') as css_file:
            if path not in file_desc.keys() and 'style.css' not in file_desc.values():
                file_desc[path] = 'style.css'
                tab.add_file(path, 'style.css')
                parent.setPlainText(css_file.read())
                parent.setFocus()


    def run_current_file(self, opened_tabs, file_desc, bawky_parent, main_text):
        current_index = opened_tabs.currentIndex()
        current_file = opened_tabs.tabText(current_index)
        for path, file_name in file_desc.items():
            if current_file == file_name:
                if not current_file.lower().endswith('.py'):
                    break
                with open(path, 'w', encoding = 'utf-8') as file:
                    file.write(main_text.toPlainText())

                if self.terminal:
                    self.terminal.show()
                    self.terminal.termEmulator.terminal.show()
                    self.terminal.termEmulator.terminal.setFocus()
                    self.terminal.termEmulator.run_command(fr"{sys.executable} {path}")



                else:
                    from widgets import TerminalDock

                    self.terminal = TerminalDock(bawky_parent)
                    self.terminal.show()
                    self.terminal.termEmulator.terminal.setFocus()
                    self.terminal.termEmulator.run_command(fr"{sys.executable} {path}")

                break


    def goto_block_(self, parent, bawky_parent):
        from widgets import GotoBlock
        self.goto_block = GotoBlock(main_text = parent)


    def get_text(self, error_label, clipboard):
        if error_label:
            text = error_label.text()
            if text != '✔️ No syntax errors':
                splitting = text.split(' ')
                if splitting[1] == 'Line':
                    text = splitting[3:]
                    text = ' '.join(text)
                clipboard.setText(text)

    def remove_current_line(self, text_edit):
        cursor = text_edit.textCursor()
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



        for block_num in reversed(range(start_block, end_block + 1)):
            block = text_edit.document().findBlockByNumber(block_num)
            cursor.setPosition(block.position())
            cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()

        text_edit.setTextCursor(cursor)
        cursor.endEditBlock()


    def goto_next_block(self, text_edit):
        cursor = text_edit.textCursor()
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
        self.terminal.termEmulator.terminal.setFont(QFont("Maple Mono", self.font_size))


    def reduce_font(self, text_edit):
        self.font_size -= 1

        if self.font_size <= 1:
            self.font_size = 1
        text_edit.setFont(QFont("Maple Mono", self.font_size))
        self.terminal.termEmulator.terminal.setFont(QFont("Maple Mono", self.font_size))



    def pressed(self, completer):
        completer.popup().show()

    def comment(self, text_edit):
        cursor = text_edit.textCursor()
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

    def remove_tab_(self, tab, file_desc):
        current_index = tab.currentIndex()
        tab.remove_tab(current_index)

    def move_tab_right(self, tab):
        current_index = tab.currentIndex() + 1
        tab.setCurrentIndex(current_index)

    def move_tab_left(self, tab):
        if tab.currentIndex() <= 0:
            tab.setCurrentIndex(0)
        else:
            current_index = tab.currentIndex() - 1
            tab.setCurrentIndex(current_index)

    def hide_show_gitpanel(self, git_panel, parent):
        if git_panel.isVisible():
            git_panel.hide()
            parent.setFocus()
        else:
            git_panel.show()

    def hide_show_terminal(self, bawky_parent, main_text):
        if self.terminal:
            if self.terminal.isVisible():
                self.terminal.hide()
                main_text.setFocus()
            else:
                self.terminal.show()
                self.terminal.termEmulator.terminal.show()
                self.terminal.termEmulator.terminal.setFocus()

        else:
            from widgets import TerminalDock

            self.terminal = TerminalDock(bawky_parent)

    def kill_terminal(self):
        if self.terminal:
            self.terminal.deleteLater()
            self.terminal.termEmulator.deleteLater()
            self.terminal.custom_title.deleteLater()
            self.terminal = None
            self.terminal = None

class FileDockShortcut:
    def __init__(self, parent, file_dock, file_view, main_text, file_description, opened_tabs):

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


    def find_next(self, main_text):
        if not main_text.find(self.text()):
            main_text.moveCursor(QTextCursor.MoveOperation.Start)
            main_text.find(self.text())


    def changed(self, main_text):
        main_text.moveCursor(QTextCursor.MoveOperation.Start)
        main_text.find(self.text())



# not necessary
# class GitPanelShortcuts:
#     def __init__(self, parent):
#         init_git = QShortcut(QKeySequence('Ctrl+I'), parent)
#         init_git.activated.connect(self.init_git_dir)

#     def init_git_dir(self):
#         try:
#             from pygit import folder_path_

#             repo = git.Repo(folder_path_, search_parent_directories = True)
        
#         except git.InvalidGitRepositoryError:
#             repo = git.Repo.init(folder_path_)
#             print(repo)