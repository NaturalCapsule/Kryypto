import sys
import os
import shutil
import time
import platform
if getattr(sys, 'frozen', False):
    src = r'src\config'
else:
    src = r'config'

if platform.system() == 'Windows':
    dst = fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto'
elif platform.system() == 'Linux':
    dst = os.path.expanduser('~/.config/KryyptoConfig')
else:
    print("Unknown OS detected, exiting now...")
    sys.exit()

did_transfer = False
if os.path.exists(src) and not os.path.exists(dst):
    os.makedirs(dst, exist_ok=True)
    shutil.move(src, dst)

    new_path = os.path.join(dst, 'config')
    for _ in range(50):
        if os.path.exists(new_path):
            did_transfer = True
            break
        time.sleep(0.1)
    else:
        raise FileNotFoundError(f"Move failed, {new_path} not found")

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QMainWindow, QHBoxLayout
from PyQt6.QtGui import  QSurfaceFormat, QCloseEvent, QIcon, QPixmap
from titlebar import CustomTitleBar
from PyQt6.QtCore import Qt, QPoint, QRect, QCoreApplication

from multiprocessing import freeze_support, active_children
from pathlib import Path


if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    plugin_path = os.path.join(base_path, "PyQt6", "Qt6", "plugins")
    QCoreApplication.addLibraryPath(plugin_path)



from settings import Setting
from shortcuts import *
from heavy import *

from config import setCustomTitleBar
from get_style import get_css_style
from config import get_fontSize
from check_version import checkUpdate

class Kryypto(QMainWindow):
    def __init__(self, clipboard):
        super().__init__()
        from pygit import open_file_dialog

        from widgets import MessageBox

        if did_transfer:
            if platform.system() == 'Windows':
                MessageBox(fr"Configuration files have been moved to 'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto'.\nIf not, please move the 'config' folder manually to 'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto'.")

            elif platform.system() == 'Linux':
                MessageBox(fr"Configuration files have been moved to '~/.config/KryyptoConfig/config'.\nIf not, please move the 'config' folder manually to '~/.config/KryyptoConfig'.")



        self.clipboard = clipboard
        self.settings = Setting()
        self.opened_directory = open_file_dialog(self, True)
        self.font_size = 12
        self.new_user_count = 0

        self.settings.setValue('Font Size', get_fontSize())



        self.settingUP_settings()

        self.resize_margin = 20
        self.resize_mode = None
        self.resize_start_pos = QPoint()
        self.resize_start_geometry = QRect()

        self.setupUI()
        self.setupWidgets()
        self.addDocks()
        self.open_files()

    def addDocks(self):
        from pygit import is_gitInstalled

        self.inner_window.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.inner_window.setDockOptions(QMainWindow.DockOption.AnimatedDocks|
            QMainWindow.DockOption.AllowTabbedDocks |
            QMainWindow.DockOption.AllowNestedDocks)

        show_files_area = self.inner_window.dockWidgetArea(self.show_files)
        git_panel_area = self.inner_window.dockWidgetArea(self.git_panel)
        terminal_area = self.inner_window.dockWidgetArea(self.terminal)

        if self.settings.value('FileDockWidgetPosition') == 'Left':
            self.inner_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.show_files)

        elif self.settings.value('FileDockWidgetPosition') == 'Right':
            self.inner_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.show_files)

        elif self.settings.value('FileDockWidgetPosition') == 'Bottom':
            self.inner_window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.show_files)

        elif self.settings.value('FileDockWidgetPosition') == 'Top':
            self.inner_window.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.show_files)


        elif show_files_area == Qt.DockWidgetArea.NoDockWidgetArea:
            self.inner_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.show_files)
            self.settings.setValue('FileDockWidgetPosition', "Left")

        # elif self.settings.value('FileDockWidgetPosition') == 'Left':
        #     self.inner_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.show_files)

        # elif self.settings.value('FileDockWidgetPosition') == 'Right':
        #     self.inner_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.show_files)

        # elif self.settings.value('FileDockWidgetPosition') == 'Bottom':
        #     self.inner_window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.show_files)

        # elif self.settings.value('FileDockWidgetPosition') == 'Top':
        #     self.inner_window.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.show_files)


        if is_gitInstalled():

            if self.settings.value('GitDockWidgetPosition') == 'Left':
                self.inner_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.git_panel)

            elif self.settings.value('GitDockWidgetPosition') == 'Right':
                self.inner_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.git_panel)

            elif self.settings.value('GitDockWidgetPosition') == 'Bottom':
                self.inner_window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.git_panel)

            elif self.settings.value('GitDockWidgetPosition') == 'Top':
                self.inner_window.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.git_panel)


            elif git_panel_area == Qt.DockWidgetArea.NoDockWidgetArea:
                self.inner_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.git_panel)
                self.settings.setValue('GitDockWidgetPosition', "Left")


        if self.settings.value('TerminalDockWidgetPosition') == 'Left':
            self.inner_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.terminal)

        elif self.settings.value('TerminalDockWidgetPosition') == 'Right':
            self.inner_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.terminal)

        elif self.settings.value('TerminalDockWidgetPosition') == 'Bottom':
            self.inner_window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal)

        elif self.settings.value('TerminalDockWidgetPosition') == 'Top':
            self.inner_window.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.terminal)


        elif terminal_area == Qt.DockWidgetArea.NoDockWidgetArea:
            self.inner_window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal)
            self.settings.setValue('TerminalDockWidgetPosition', "Bottom")


        # if is_gitInstalled():
            # self.inner_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.git_panel)
        # self.inner_window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal)
        # self.inner_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.show_files)


    def setupUI(self):
        self.setWindowTitle("Kryypto")
        if getattr(sys, 'frozen', False):
            pixmap = QPixmap('icons/app/icon.ico')
        else:
            pixmap = QPixmap('src/icons/app/icon.ico')


        pixmap = pixmap.scaled(256, 256)
        self.setWindowIcon(QIcon(pixmap))

        self.setMouseTracking(True)
        self.setObjectName("MainWindow")
        self.setStyleSheet(get_css_style())
        
        if setCustomTitleBar():
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def settingUP_settings(self):
        import widgets
        try:
            self.resize(self.settings.value('Window Size'))
            self.move(self.settings.value('Window Position'))
            self.font_size = self.settings.value('Font Size')

        except:
            self.setGeometry(100, 100, 400, 800)
            self.font_size = 12

        try:
           widgets.file_description = self.settings.value('opened_files')
        except Exception:
            self.settings.setValue('opened_files', {})


    def open_files(self):
        from pygit import folder_path_
        from widgets import file_description
        parent_folder = Path(folder_path_)

        if self.settings.value('opened_files'):
            for path, file_name in self.settings.value('opened_files').items():
                sub_folder_file = Path(path)
                if (os.path.exists(path)) and (sub_folder_file.is_relative_to(parent_folder)):
                    with open(path, 'r', encoding = 'utf-8') as opened_file:
                        opened_file_ = opened_file.read()
                        self.tab_bar.add_file(path = path, file_name = file_name)
                        self.main_text.setPlainText(opened_file_)
                else:
                    file_description.pop(path)

            try:
                self.tab_bar.setCurrentIndex(self.settings.value('CurrentFileIndex'))
            except Exception:
                self.settings.setValue('CurrentFileIndex', 0)
                self.tab_bar.setCurrentIndex(0)
        else:
            self.settings.setValue('opened_files', {})


    def setupWidgets(self):
        import widgets
        
        is_update = checkUpdate()

        if is_update:
            widgets.MessageBox(
                f"An update for "
                f"<a href='{is_update}'>Kryypto</a>"
                " has been released go download it!",
                link=is_update

            )

        central_widget = QWidget()



        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)


        if setCustomTitleBar():
            self.title_bar = CustomTitleBar(self)
            main_layout.addWidget(self.title_bar)
            central_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            central_widget.setMouseTracking(True)

        content_area = QWidget()
        content_area.setMouseTracking(True)
        content_area.setObjectName('MainWindow')
        content_area.setStyleSheet(get_css_style())

        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.editor_containter = QWidget()
        self.editor_layout = QVBoxLayout(self.editor_containter)

        self.main_text = widgets.MainText(self.editor_layout, self.clipboard, self.font_size, self)

        self.welcome_page = widgets.WelcomeWidget()
        self.inner_window = QMainWindow()

        self.tab_bar = widgets.ShowOpenedFile(
            self.main_text, content_layout, widgets.error_label, 
            self.inner_window, self.welcome_page, self.editor_containter, 
            self.editor_layout, widgets.nameErrorlabel
        )
        
        content_layout.addWidget(self.tab_bar)
        content_layout.addWidget(self.inner_window)

        self.editor_layout.addWidget(self.tab_bar)
        self.editor_layout.addWidget(self.main_text)

        self.inner_window.setCentralWidget(self.welcome_page)
        self.inner_window.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.inner_window.setMouseTracking(True)

        if is_gitInstalled():
            self.git_panel = widgets.GitDock(self.inner_window)

        else:
            self.git_panel = None

        self.list_shortcuts = widgets.ListShortCuts()
        self.terminal = widgets.TerminalDock(self)
        self.show_files = widgets.ShowDirectory(self.main_text, self.tab_bar)

        self.editor_shortcuts = MainTextShortcuts(
            self.main_text, self.main_text.completer, self.tab_bar, 
            widgets.error_label, self.clipboard, self.editor_layout, 
            self.terminal, self, self.tab_bar, widgets.file_description, 

            self.list_shortcuts, self.git_panel, self.font_size, self.main_text.line_number_area, self.show_files

        )



        FileDockShortcut(
            self.inner_window, self.show_files, self.show_files.file_viewer, 
            self.main_text, widgets.file_description, self.tab_bar, self
        )

        main_layout.addWidget(content_area)

        self.setCentralWidget(central_widget)

        content_layout.addWidget(self.list_shortcuts)

        self.welcome_page.setFocus()


    def get_resize_mode(self, pos):
        rect = self.rect()
        margin = self.resize_margin
        
        left = pos.x() <= margin
        right = pos.x() >= rect.width() - margin
        top = pos.y() <= margin
        bottom = pos.y() >= rect.height() - margin
        
        if top and left:
            return 'top-left'
        elif top and right:
            return 'top-right'
        elif bottom and left:
            return 'bottom-left'
        elif bottom and right:
            return 'bottom-right'
        elif top:
            return 'top'
        elif bottom:
            return 'bottom'
        elif left:
            return 'left'
        elif right:
            return 'right'
        else:
            return None

    def update_cursor(self, mode):
        cursor_map = {
            'top': Qt.CursorShape.SizeVerCursor,
            'bottom': Qt.CursorShape.SizeVerCursor,
            'left': Qt.CursorShape.SizeHorCursor,
            'right': Qt.CursorShape.SizeHorCursor,
            'top-left': Qt.CursorShape.SizeFDiagCursor,
            'bottom-right': Qt.CursorShape.SizeFDiagCursor,
            'top-right': Qt.CursorShape.SizeBDiagCursor,
            'bottom-left': Qt.CursorShape.SizeBDiagCursor,
        }
        
        if mode in cursor_map:
            self.setCursor(cursor_map[mode])
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)


    if setCustomTitleBar():
        def mousePressEvent(self, event):
            if event.button() == Qt.MouseButton.LeftButton:
                self.resize_mode = self.get_resize_mode(event.position().toPoint())
                if self.resize_mode:
                    self.resize_start_pos = event.globalPosition().toPoint()
                    self.resize_start_geometry = self.geometry()
                    event.accept()
                    return
            super().mousePressEvent(event)

        def mouseMoveEvent(self, event):
            if not self.resize_mode:
                mode = self.get_resize_mode(event.position().toPoint())
                self.update_cursor(mode)
            else:
                current_pos = event.globalPosition().toPoint()
                diff = current_pos - self.resize_start_pos
                
                new_geo = QRect(self.resize_start_geometry)
                
                if 'left' in self.resize_mode:
                    new_geo.setLeft(new_geo.left() + diff.x())
                if 'right' in self.resize_mode:
                    new_geo.setRight(new_geo.right() + diff.x())
                if 'top' in self.resize_mode:
                    new_geo.setTop(new_geo.top() + diff.y())
                if 'bottom' in self.resize_mode:
                    new_geo.setBottom(new_geo.bottom() + diff.y())
                
                min_width, min_height = 800, 600
                if new_geo.width() < min_width:
                    if 'left' in self.resize_mode:
                        new_geo.setLeft(new_geo.right() - min_width)
                    else:
                        new_geo.setRight(new_geo.left() + min_width)
                
                if new_geo.height() < min_height:
                    if 'top' in self.resize_mode:
                        new_geo.setTop(new_geo.bottom() - min_height)
                    else:
                        new_geo.setBottom(new_geo.top() + min_height)
                
                self.setGeometry(new_geo)
                event.accept()
                return

            super().mouseMoveEvent(event)


        def enterEvent(self, event):
            self.setMouseTracking(True)
            super().enterEvent(event)

        def mouseReleaseEvent(self, event):
            if event.button() == Qt.MouseButton.LeftButton:
                self.resize_mode = None
                self.setCursor(Qt.CursorShape.ArrowCursor)
            super().mouseReleaseEvent(event)

        def leaveEvent(self, event):
            if not self.resize_mode:
                self.setCursor(Qt.CursorShape.ArrowCursor)
            super().leaveEvent(event)

    def closeEvent(self, event: QCloseEvent):
        from widgets import pop_messagebox, file_description
        from pygit import folder_path_

        self.font_size = self.editor_shortcuts.font_size
        self.settings.setValue('Font Size', get_fontSize())
        self.settings.setValue('Window Size', self.size())
        self.settings.setValue('Window Position', self.pos())
        self.settings.setValue('Opened Directory', folder_path_)

        if (hasattr(self.tab_bar, 'show_error') and hasattr(self.tab_bar.show_error, 'code_queue')):
            self.tab_bar.show_error._code_queue.put('__EXIT__')
            self.main_text.code_queue_.put('__EXIT__')
            self.main_text.code_queue.put('__EXIT__')

        for p in active_children():
            if p.is_alive():
                p.terminate()

        if self.tab_bar.is_save_file_needed():
            pop_messagebox(self, event, self.tab_bar, True)

        self.main_text.discord_presence.disconnect()

        self.settings.setValue('opened_files', file_description)
        self.settings.setValue('CurrentFileIndex', self.tab_bar.currentIndex())

        show_files_area = self.inner_window.dockWidgetArea(self.show_files)
        git_panel_area = self.inner_window.dockWidgetArea(self.git_panel)
        terminal_area = self.inner_window.dockWidgetArea(self.terminal)

        if show_files_area == Qt.DockWidgetArea.LeftDockWidgetArea:
            self.settings.setValue('FileDockWidgetPosition', "Left")
        elif show_files_area == Qt.DockWidgetArea.RightDockWidgetArea:
            self.settings.setValue('FileDockWidgetPosition', "Right")
        elif show_files_area == Qt.DockWidgetArea.TopDockWidgetArea:
            self.settings.setValue('FileDockWidgetPosition', "Top")
        elif show_files_area == Qt.DockWidgetArea.BottomDockWidgetArea:
            self.settings.setValue('FileDockWidgetPosition', "Bottom")

        if git_panel_area == Qt.DockWidgetArea.LeftDockWidgetArea:
            self.settings.setValue('GitDockWidgetPosition', "Left")
        elif git_panel_area == Qt.DockWidgetArea.RightDockWidgetArea:
            self.settings.setValue('GitDockWidgetPosition', "Right")
        elif git_panel_area == Qt.DockWidgetArea.TopDockWidgetArea:
            self.settings.setValue('GitDockWidgetPosition', "Top")
        elif git_panel_area == Qt.DockWidgetArea.BottomDockWidgetArea:
            self.settings.setValue('GitDockWidgetPosition', "Bottom")

        if terminal_area == Qt.DockWidgetArea.LeftDockWidgetArea:
            self.settings.setValue('TerminalDockWidgetPosition', "Left")
        elif terminal_area == Qt.DockWidgetArea.RightDockWidgetArea:
            self.settings.setValue('TerminalDockWidgetPosition', "Right")
        elif terminal_area == Qt.DockWidgetArea.TopDockWidgetArea:
            self.settings.setValue('TerminalDockWidgetPosition', "Top")
        elif terminal_area == Qt.DockWidgetArea.BottomDockWidgetArea:
            self.settings.setValue('TerminalDockWidgetPosition', "Bottom")

        if self.tab_bar.doc_panelstring:
            docstring_area = self.inner_window.dockWidgetArea(self.tab_bar.doc_panelstring)

            if docstring_area == Qt.DockWidgetArea.LeftDockWidgetArea:
                self.settings.setValue('DocStringDockWidgetPosition', "Left")
            elif docstring_area == Qt.DockWidgetArea.RightDockWidgetArea:
                self.settings.setValue('DocStringDockWidgetPosition', "Right")
            elif docstring_area == Qt.DockWidgetArea.TopDockWidgetArea:
                self.settings.setValue('DocStringDockWidgetPosition', "Top")
            elif docstring_area == Qt.DockWidgetArea.BottomDockWidgetArea:
                self.settings.setValue('DocStringDockWidgetPosition', "Bottom")


if __name__ == "__main__":
    freeze_support()
    format = QSurfaceFormat()
    format.setRenderableType(QSurfaceFormat.RenderableType.OpenGL)
    format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    format.setVersion(3, 3)
    format.setSwapBehavior(QSurfaceFormat.SwapBehavior.DoubleBuffer)
    format.setDepthBufferSize(144)
    QSurfaceFormat.setDefaultFormat(format)
    app = QApplication(sys.argv)

    window = Kryypto(app.clipboard())
    window.show()
    sys.exit(app.exec())