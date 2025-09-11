import re
import sys
import os

from PyQt6.QtGui import QFont, QShortcut, QKeySequence, QTextCursor, QFontMetrics
from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtCore import QProcess, QCoreApplication

from config import get_fontFamily, write_config
from pygit import open_file_dialog_again, is_gitInstalled

from animations import *
from config import *

def reboot():
    if getattr(sys, 'frozen', False):

        # exe = sys.executable  
        # args = sys.argv[1:]
        # DETACHED_PROCESS = 0x00000008
        # subprocess.Popen(
        #     [exe] + args,
        #     creationflags=DETACHED_PROCESS
        # )

        # time.sleep(0.2)

        # os._exit(0)

        print("Error")

    else:
        python = sys.executable
        script = os.path.abspath(sys.argv[0])
        QProcess.startDetached(python, [script] + sys.argv[1:])
    
        QCoreApplication.quit()

class MainTextShortcuts:
    def __init__(self, parent, completer, tab, error_label, clipboard, bawky_parent, term, bawky_parent_, opened_tabs, file_desc, list_shortcuts, git_panel, font_size, lines, show_files):
        
        self.font_size = font_size
        self.terminal = term
        self.lines = lines
        self.show_files = show_files
        self.index = 0


        delete_line = QShortcut(QKeySequence(DeleteLine()), parent)
        delete_line.activated.connect(lambda: self.remove_current_line(parent))

        new_line = QShortcut(QKeySequence(newLine()), parent)
        new_line.activated.connect(lambda: self.goto_next_block(parent))

        increase_font = QShortcut(QKeySequence(IncreaseFont()), parent)
        increase_font.activated.connect(lambda: self.increase_font(parent, opened_tabs))

        reduce_font = QShortcut(QKeySequence(DecreaseFont()), parent)
        reduce_font.activated.connect(lambda: self.reduce_font(parent, opened_tabs))

        show_completer = QShortcut(QKeySequence("Ctrl+Space"), parent)
        show_completer.activated.connect(lambda: self.pressed(completer))

        indent_line = QShortcut(QKeySequence(IndentCurrentLine()), parent)
        indent_line.activated.connect(lambda: self.add_indentation(parent))

        remove_indent = QShortcut(QKeySequence(removeIndentCurrent()), parent)
        remove_indent.activated.connect(lambda: self.remove_indentation(parent))

        remove_current_tab = QShortcut(QKeySequence(RemoveCurrentTab()), parent)
        remove_current_tab.activated.connect(lambda: self.remove_tab_(tab, file_desc))


        move_tab_right = QShortcut(QKeySequence(MoveTabRight()), parent)
        move_tab_right.activated.connect(lambda: self.move_tab_right(tab))

        move_tab_left = QShortcut(QKeySequence(MoveTabLeft()), parent)
        move_tab_left.activated.connect(lambda: self.move_tab_left(tab))

        get_error_text = QShortcut(QKeySequence("Ctrl+Shift+C"), parent)
        get_error_text.activated.connect(lambda: self.get_text(error_label, clipboard))


        goto_block = QShortcut(QKeySequence(GotoBlock_()), parent)
        goto_block.activated.connect(lambda: self.goto_block_(parent, bawky_parent))


        hide_show_term = QShortcut(QKeySequence(Hide_Show_term()), bawky_parent_)
        hide_show_term.activated.connect(lambda: self.hide_show_terminal(bawky_parent_, parent))

        kill_term = QShortcut(QKeySequence(KillTerminalSession()), parent)
        kill_term.activated.connect(self.kill_terminal)

        run_file = QShortcut(QKeySequence(RunCurrentPythonFile()), parent)
        run_file.activated.connect(lambda: self.run_current_file(opened_tabs, file_desc, bawky_parent_, parent))

        open_css_file = QShortcut(QKeySequence(OpenStyleFile()), bawky_parent_)
        open_css_file.activated.connect(lambda: self.open_css(opened_tabs, file_desc, bawky_parent_, parent))

        open_config_file = QShortcut(QKeySequence(OpenConfigFile()), bawky_parent_)
        open_config_file.activated.connect(lambda: self.open_config(opened_tabs, file_desc, bawky_parent_, parent))

        open_markdown_file = QShortcut(QKeySequence(OpenMarkDownFile()), bawky_parent_)
        open_markdown_file.activated.connect(lambda: self.open_markdown(opened_tabs, file_desc, bawky_parent_, parent))


        hide_show_shortcuts = QShortcut(QKeySequence(Show_Hide_Shortcuts()), bawky_parent_)
        hide_show_shortcuts.activated.connect(lambda: self.hide_show_shortcuts(bawky_parent_, list_shortcuts))

        if is_gitInstalled():
            hide_show_gitpanel = QShortcut(QKeySequence(Hide_Show_gitpanel()), bawky_parent_)
            hide_show_gitpanel.activated.connect(lambda: self.hide_show_gitpanel(git_panel, parent, bawky_parent_))

        select_folder = QShortcut(QKeySequence(SelectFolder()), bawky_parent_)
        select_folder.activated.connect(lambda: self.show_folderGUI(bawky_parent_))


        move_block_above = QShortcut(QKeySequence(MoveBlockUp()), parent)
        move_block_above.activated.connect(lambda: self.moveBlock_above(parent))

        move_block_below = QShortcut(QKeySequence(MoveBlockDown()), parent)
        move_block_below.activated.connect(lambda: self.moveBlock_below(parent))

        goto_bookrmarked_block = QShortcut(QKeySequence("Ctrl+R"), parent)
        goto_bookrmarked_block.activated.connect(lambda: self.goto_bookrmarked_block(parent))

        bookmark_line = QShortcut(QKeySequence("Ctrl+O"), parent)
        bookmark_line.activated.connect(lambda: self.bookmark_line(parent))

        pop_bookmark_line = QShortcut(QKeySequence("Ctrl+E"), parent)
        # pop_bookmark_line = QShortcut(QKeySequence("Ctrl+Alt+R"), parent)
        pop_bookmark_line.activated.connect(lambda: self.pop_bookmarked_line(parent))


        maximize = QShortcut(QKeySequence(Maximize()), bawky_parent_)
        maximize.activated.connect(lambda: self.max_(bawky_parent_))

        minimize = QShortcut(QKeySequence(Minimize()), bawky_parent_)
        minimize.activated.connect(lambda: self.min_(bawky_parent_))



        close = QShortcut(QKeySequence(Close()), bawky_parent_)
        close.activated.connect(self.Close_)

        reboot_ = QShortcut(QKeySequence(Reboot()), bawky_parent_)
        reboot_.activated.connect(reboot)

    def Close_(self):
        QCoreApplication.quit()

    def max_(self, parent):
        if parent.isMaximized():
            parent.showNormal()
        else:
            parent.showMaximized()

    def min_(self, parent):
        parent.showMinimized()

    def goto_bookrmarked_block(self, text_edit: QPlainTextEdit):
        if text_edit.bookmarked_blocks:
            cursor = text_edit.textCursor()
            try:
                block = text_edit.document().findBlockByNumber(text_edit.bookmarked_blocks[self.index])
                cursor.setPosition(block.position())

            except IndexError:
                self.index = 0
                block = text_edit.document().findBlockByNumber(text_edit.bookmarked_blocks[self.index])
                cursor.setPosition(block.position())


            self.index += 1
            text_edit.setTextCursor(cursor)

    def bookmark_line(self, text_edit: QPlainTextEdit):
        cursor = text_edit.textCursor()
        current_block = cursor.block().blockNumber()
        if current_block not in text_edit.bookmarked_blocks:
            text_edit.bookmarked_blocks.append(current_block)

    def pop_bookmarked_line(self, text_edit):
        try:
            text_edit.bookmarked_blocks.pop()
        except IndexError:
            pass

    def show_folderGUI(self, parent):
        open_file_dialog_again(parent)
        reboot()

    def hide_show_shortcuts(self, parent, list_shortcuts):
        if list_shortcuts.maximumHeight() == 0:
            animatePanel(list_shortcuts, parent, show=True)
        else:
            animatePanel(list_shortcuts, parent, show=False)



    def open_config(self, tab, file_desc, bawky_parent, parent):
        # path = "config/configuration.cfg"
        if platform.system() == 'Windows':
            path = fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\configuration.cfg'
        elif platform.system() == "Linux":
            path = f'~/.config/KryyptoConfig/config/configuration.cfg'
        with open(path, 'r', encoding = 'utf-8') as css_file:
            if path not in file_desc.keys() and 'configuration.cfg' not in file_desc.values():
                file_desc[path] = 'configuration.cfg'
                tab.add_file(path, 'configuration.cfg')
                parent.setPlainText(css_file.read())
                parent.setFocus()

    def open_markdown(self, tab, file_desc, bawky_parent, parent):
        # path = "config/configuration.cfg"
        # if platform.system() == 'Windows':
        #     path = fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\configuration.cfg'
        # elif platform.system() == "Linux":
        #     path = f'~/.config/KryyptoConfig/config/configuration.cfg'
        path = get_markdownpreview_file()
        with open(path, 'r', encoding = 'utf-8') as markdown_file:
            if path not in file_desc.keys() and 'markdown.txt' not in file_desc.values():
                file_desc[path] = 'markdown.txt'
                tab.add_file(path, 'markdown.txt')
                parent.setPlainText(markdown_file.read())
                parent.setFocus()

    def open_css(self, tab, file_desc, bawky_parent, parent):
        path = get_stylefile()

        if platform.system() == 'Windows':
            file_name = path.split('\\')[-1]

        elif platform.system() == 'Linux':
            file_name = path.split('/')[-1]
            path = os.path.expanduser(path)

        with open(path, 'r', encoding = 'utf-8') as css_file:
            if path not in file_desc.keys() and file_name not in file_desc.values():
                file_desc[path] = file_name
                tab.add_file(path, file_name)
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
                    # self.terminal.termEmulator.run_command(fr"{sys.executable} {path}")
                    if ' ' in path:
                        self.terminal.termEmulator.run_command(fr"{getInterpreter()} '{path}'")
                    else:
                        self.terminal.termEmulator.run_command(fr"{getInterpreter()} {path}")

                else:
                    from widgets import TerminalDock

                    self.terminal = TerminalDock(bawky_parent)
                    self.terminal.show()
                    self.terminal.termEmulator.terminal.setFocus()

                    if ' ' in path:
                        self.terminal.termEmulator.run_command(fr"{getInterpreter()} '{path}'")
                    else:
                        self.terminal.termEmulator.run_command(fr"{getInterpreter()} {path}")
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
            if cursor.block().text() == '':
                cursor.deleteChar()
            else:
                cursor.movePosition(QTextCursor.MoveOperation.Down)


        text_edit.setTextCursor(cursor)
        cursor.endEditBlock()


    def moveBlock_below(self, text_edit):
        cursor = text_edit.textCursor()
        cursor.beginEditBlock()

        cursor_pos = cursor.block()
        next_block = cursor_pos.next()


        if not cursor.hasSelection():
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        start_block = cursor.blockNumber()

        cursor.setPosition(end)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        end_block = cursor.blockNumber()

        if next_block.isValid() and next_block.next().isValid():
            for block_num in reversed(range(start_block, end_block + 1)):
                block = text_edit.document().findBlockByNumber(block_num)
                cursor.setPosition(block.position())

                cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
                cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

                line_text = cursor.block().text()


                cursor.removeSelectedText()
                cursor.deleteChar()

                next_position = cursor.block().next().position()

                # cursor.setPosition(next_position, QTextCursor.MoveMode.KeepAnchor)
                cursor.setPosition(next_position)

                cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
                cursor.insertText(f'{line_text}\n')
                cursor.setPosition(next_position)



            text_edit.setTextCursor(cursor)

            new_cursor = text_edit.textCursor()
            block_start = text_edit.document().findBlockByNumber(start_block + 1).position()
            block_end = text_edit.document().findBlockByNumber(end_block + 1).position()
            new_cursor.setPosition(block_start, QTextCursor.MoveMode.MoveAnchor)
            new_cursor.setPosition(block_end, QTextCursor.MoveMode.KeepAnchor)
            text_edit.setTextCursor(new_cursor)

        cursor.endEditBlock()


    def moveBlock_above(self, text_edit):
        # cursor = text_edit.textCursor()
        # cursor.beginEditBlock()

        # if not cursor.hasSelection():
        #     cursor.select(QTextCursor.SelectionType.LineUnderCursor)

        # start = cursor.selectionStart()
        # end = cursor.selectionEnd()

        # cursor.setPosition(start)
        # cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        # start_block = cursor.blockNumber()

        # cursor.setPosition(end)
        # cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        # end_block = cursor.blockNumber()


        # cursor_pos = cursor.block()
        # prev_block = cursor_pos.previous()
        # prev_position = prev_block.position()


        # if prev_block.isValid():
        #     for block_num in reversed(range(start_block, end_block + 1)):
        #         block = text_edit.document().findBlockByNumber(block_num)
        #         cursor.setPosition(block.position())

        #         cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        #         cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

        #         line_text = cursor.selectedText()
        #         cursor.removeSelectedText()
        #         cursor.deleteChar()


        #         cursor.setPosition(prev_position)
        #         cursor.insertText(f'{line_text}\n')
        #         cursor.setPosition(prev_position)

        #     text_edit.setTextCursor(cursor)

        # cursor.endEditBlock()


        cursor = text_edit.textCursor()
        cursor.beginEditBlock()

        cursor_pos = cursor.block()
        prev_block = cursor_pos.previous()


        if not cursor.hasSelection():
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        start_block = cursor.blockNumber()

        cursor.setPosition(end)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        end_block = cursor.blockNumber()


        if prev_block.isValid():
            for block_num in range(start_block, end_block + 1):
                block = text_edit.document().findBlockByNumber(block_num)
                cursor.setPosition(block.position())

                cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
                cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

                line_text = cursor.block().text()

                cursor.removeSelectedText()
                cursor.deleteChar()

                prev_position = cursor.block().previous().position()


                cursor.setPosition(prev_position)
                cursor.insertText(f'{line_text}\n')
                cursor.setPosition(prev_position)


            text_edit.setTextCursor(cursor)


            new_cursor = text_edit.textCursor()
            block_start = text_edit.document().findBlockByNumber(start_block - 1).position()
            block_end = text_edit.document().findBlockByNumber(end_block - 1).position()
            new_cursor.setPosition(block_start, QTextCursor.MoveMode.MoveAnchor)
            new_cursor.setPosition(block_end, QTextCursor.MoveMode.KeepAnchor)
            text_edit.setTextCursor(new_cursor)


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

            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

            line_text = cursor.selectedText()

            new_line = "    " + line_text

            cursor.insertText(new_line)

        cursor.endEditBlock()


        # cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        # cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

        # line_text = cursor.selectedText()

        # new_line = "    " + line_text

        # cursor.insertText(new_line)

        # cursor.endEditBlock()

    def remove_indentation(self, text_edit):
        # cursor = text_edit.textCursor()
        # cursor.beginEditBlock()


        # cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        # cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

        # line_text = cursor.selectedText()

        # stripped_line = line_text[4:] if line_text.startswith("    ") else line_text.lstrip()

        # cursor.insertText(stripped_line)
        # cursor.endEditBlock()

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

            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)

            line_text = cursor.selectedText()

            stripped_line = line_text[4:] if line_text.startswith("    ") else line_text.lstrip()


            cursor.insertText(stripped_line)

        cursor.endEditBlock()



    def increase_font(self, text_edit, tab_bar):
        
        self.font_size += 1
        font = QFont(get_fontFamily(), self.font_size)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        font.setPixelSize(self.font_size)
        text_edit.setFont(font)

        text_edit.completer.popup().setFont(font)

        # self.terminal.termEmulator.terminal.setFont(QFont(get_fontFamily(), self.font_size))
        self.terminal.termEmulator.terminal.setFont(font)

        text_edit.line_number_area.update()
        # font = QFont('Maple Mono', self.font_size)

        self.lines.setFont(font)
        self.lines.font_metrics = QFontMetrics(font)
        # self.show_files.file_viewer.setFont(QFont(get_fontFamily(), self.font_size))
        self.show_files.file_viewer.setFont(font)



        try:
            if tab_bar.doc_panelstring.doc_panel is not None and text_edit.doc_panel is not None:
                tab_bar.doc_panelstring.doc_panel.setFont(font)
        except AttributeError:
            pass


        write_config(self.font_size, 'Appearance', 'fontsize')


    def reduce_font(self, text_edit, tab_bar):
        self.font_size -= 1
        if self.font_size <= 1:
            self.font_size = 1
        font = QFont(get_fontFamily(), self.font_size)
        font.setPixelSize(self.font_size)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        # text_edit.setFont(QFont(get_fontFamily(), self.font_size))
        text_edit.setFont(font)
        text_edit.completer.popup().setFont(font)

        # self.terminal.termEmulator.terminal.setFont(QFont(get_fontFamily(), self.font_size))
        self.terminal.termEmulator.terminal.setFont(font)


        self.lines.setFont(font)
        self.lines.font_metrics = QFontMetrics(font)
        # self.show_files.file_viewer.setFont(QFont(get_fontFamily(), self.font_size))
        self.show_files.file_viewer.setFont(font)


        try:
            if tab_bar.doc_panelstring.doc_panel is not None and text_edit.doc_panel is not None:
                tab_bar.doc_panelstring.doc_panel.setFont(font)
        except AttributeError:
            pass


        write_config(self.font_size, 'Appearance', 'fontsize')


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

    def hide_show_gitpanel(self, git_panel, parent, window):
        if git_panel.maximumHeight() == 0:
            animatePanel(git_panel, window, show=True, sub_widget = [git_panel.commit, git_panel.active_branch_name, git_panel.remote_url, git_panel.users_profile, git_panel.user_username, git_panel.show_changes, git_panel.header_changes, git_panel.commit_info, git_panel.latest_commit, git_panel.last_commit, git_panel.repo_info, git_panel.untracked_files, git_panel.untracked_header, git_panel.repo_name])
        else:
            # animatePanel(git_panel, window, show=False)
            animatePanel(git_panel, window, show=False, sub_widget = [git_panel.commit, git_panel.insertions, git_panel.deletion, git_panel.active_branch_name, git_panel.remote_url, git_panel.users_profile, git_panel.user_username, git_panel.show_changes, git_panel.header_changes, git_panel.commit_info, git_panel.latest_commit, git_panel.last_commit, git_panel.repo_info, git_panel.untracked_files, git_panel.untracked_header, git_panel.repo_name])



    def hide_show_terminal(self, bawky_parent, main_text):
        if self.terminal:
            if self.terminal.maximumHeight() == 0:
                animatePanel(self.terminal, bawky_parent, show=True, sub_widget = [self.terminal.termEmulator.terminal])
                self.terminal.termEmulator.terminal.setFocus()

            else:
                animatePanel(self.terminal, bawky_parent, show=False)
                main_text.setFocus()

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
    def __init__(self, parent, file_dock, file_view, main_text, file_description, opened_tabs, window):

        self.file_view = file_view
        self.main_text = main_text
        self.file_description = file_description
        self.opened_tabs = opened_tabs

        show_hide_file_dock = QShortcut(QKeySequence(Hide_Show_viewer()), parent)
        show_hide_file_dock.activated.connect(lambda: self.showHideFile(file_dock, window))
    
        save_file = QShortcut(QKeySequence(SaveCurrentFile()), parent)
        save_file.activated.connect(self.save_file)

    def showHideFile(self, file_dock, window):
        if file_dock.maximumHeight() == 0:
            animatePanel(file_dock, window, show=True)
            self.file_view.setFocus()
        else:
            animatePanel(file_dock, window, show=False)
            self.main_text.setFocus()


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