import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QMainWindow
from PyQt6.QtGui import  QSurfaceFormat, QCloseEvent
from titlebar import CustomTitleBar
from PyQt6.QtCore import Qt, QPoint, QRect
# from multiprocessing import Process, Queue


from settings import Setting
from shortcuts import *
from heavy import *

from config import setCustomTitleBar
from get_style import get_css_style
from pygit import open_file_dialog, folder_path_
from config import get_fontSize

class Kryypto(QMainWindow):
    def __init__(self, clipboard):
        super().__init__()
        self.clipboard = clipboard
        self.settings = Setting()
        self.opened_directory = open_file_dialog(self, True)
        self.font_size = 12
        self.settings.setValue('Font Size', get_fontSize())
        self.settingUP_settings()

        self.resize_margin = 20
        self.resize_mode = None
        self.resize_start_pos = QPoint()
        self.resize_start_geometry = QRect()

        self.setupUI()
        self.setupWidgets()
        self.addDocks()

    def addDocks(self):
        self.inner_window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.inner_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.git_panel)
        self.inner_window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal)
        self.inner_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.show_files)
        self.inner_window.setDockOptions(QMainWindow.DockOption.AnimatedDocks|
            QMainWindow.DockOption.AllowTabbedDocks |
            QMainWindow.DockOption.AllowNestedDocks)

    def setupUI(self):
        self.setWindowTitle("Kryypto")
        self.setMouseTracking(True)
        self.setObjectName("MainWindow")
        self.setStyleSheet(get_css_style())
        
        if setCustomTitleBar():
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def settingUP_settings(self):
        try:
            self.resize(self.settings.value('Window Size'))
            self.move(self.settings.value('Window Position'))
            self.font_size = self.settings.value('Font Size')

        except:
            self.setGeometry(100, 100, 400, 800)
            self.font_size = 12

    def setupWidgets(self):
        import widgets
        
        
        central_widget = QWidget()


        # if setCustomTitleBar():
        #     self.title_bar = CustomTitleBar(self)
        #     main_layout.addWidget(self.title_bar)
        #     central_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        #     central_widget.setMouseTracking(True)


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

        self.git_panel = widgets.GitDock(self.inner_window)
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
        from widgets import pop_messagebox
        from pygit import folder_path_

        self.font_size = self.editor_shortcuts.font_size
        self.settings.setValue('Font Size', get_fontSize())
        self.settings.setValue('Window Size', self.size())
        self.settings.setValue('Window Position', self.pos())
        self.settings.setValue('Opened Directory', folder_path_)

        if (hasattr(self.tab_bar, 'show_error') and hasattr(self.tab_bar.show_error, 'code_queue')):
            # self.tab_bar.show_error.cleanup()
            self.tab_bar.show_error._code_queue.put('__EXIT__')
            self.main_text.code_queue_.put('__EXIT__')
            self.main_text.code_queue.put('__EXIT__')

        if self.tab_bar.is_save_file_needed():
            pop_messagebox(self, event, self.tab_bar, True)

if __name__ == '__main__':

    # code_queue = Queue()
    # result_queue = Queue()

    # Start Jedi worker in another process
    # p = Process(target=jedi_worker, args=(code_queue, result_queue))
    # p.start()

    format = QSurfaceFormat()
    format.setRenderableType(QSurfaceFormat.RenderableType.OpenGL)
    format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    format.setVersion(3, 3)
    format.setSwapBehavior(QSurfaceFormat.SwapBehavior.DoubleBuffer)
    format.setDepthBufferSize(144)
    QSurfaceFormat.setDefaultFormat(format)
    app = QApplication(sys.argv)
    # bridge = JediBridge(code_queue, result_queue)

    window = Kryypto(app.clipboard())
    window.show()
    sys.exit(app.exec())