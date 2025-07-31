import sys
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QApplication, QMainWindow, QMessageBox, QPushButton, QFileDialog
from PyQt6.QtGui import  QFont, QSurfaceFormat, QCloseEvent, QPixmap
from titlebar import CustomTitleBar
from PyQt6.QtCore import Qt
from shortcuts import *
from get_style import get_css_style
from pygit import open_file_dialog

class IDE(QMainWindow):
    def __init__(self, clipboard):
        super().__init__()
        self.clipboard = clipboard
        self.opened_directory = open_file_dialog(self)


        self.setupUI()
        self.setupWidgets()
        self.addDocks()


    def addDocks(self):
        self.inner_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.git_panel)
        self.inner_window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal)
        self.inner_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.show_files)
        self.setDockOptions(QMainWindow.DockOption.AnimatedDocks|
    QMainWindow.DockOption.AllowTabbedDocks |
    QMainWindow.DockOption.AllowNestedDocks)

    def setupUI(self):
        self.setWindowTitle("IDE")
        self.setGeometry(100, 100, 2000, 1400)
        self.setObjectName("MainWindow")
        self.setStyleSheet(get_css_style())
        # print(self.geometry()) get current geometry


    def setupWidgets(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        import widgets

        self.editor_containter = QWidget()
        self.editor_layout = QVBoxLayout(self.editor_containter)


        self.central_layout = QVBoxLayout(widgets.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        # self.main_text = widgets.MainText(self.central_layout, self.clipboard)
        self.main_text = widgets.MainText(self.editor_layout, self.clipboard)



        self.title_bar = CustomTitleBar(self)
        self.central_layout.addWidget(self.title_bar)
        self.setCentralWidget(widgets.central_widget)

        self.welcome_page = widgets.WelcomeWidget()
        self.inner_window = QMainWindow()
        self.tab_bar = widgets.ShowOpenedFile(self.main_text, self.central_layout, widgets.error_label, self.inner_window, self.welcome_page, self.editor_containter, self.editor_layout)
        self.central_layout.addWidget(self.tab_bar)
        self.central_layout.addWidget(self.inner_window)



        self.editor_layout.addWidget(self.tab_bar)
        self.editor_layout.addWidget(self.main_text)

        self.inner_window.setCentralWidget(self.welcome_page)
        self.inner_window.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.inner_window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


        self.git_panel = widgets.GitDock(self.inner_window)

        self.list_shortcuts = widgets.ListShortCuts()

        self.terminal = widgets.TerminalDock(self)

        self.editor_shortcuts = MainTextShortcuts(self.main_text, self.main_text.completer, self.tab_bar, widgets.error_label, self.clipboard, self.editor_layout, self.terminal, self, self.tab_bar, widgets.file_description, self.list_shortcuts, self.git_panel)


        self.main_text.setFont(QFont("Maple Mono", self.editor_shortcuts.font_size))

        self.show_files = widgets.ShowDirectory(self.main_text, self.tab_bar)

        FileDockShortcut(self.inner_window, self.show_files, self.show_files.file_viewer, self.main_text, widgets.file_description, self.tab_bar)


        self.welcome_page.setFocus()

    def closeEvent(self, event: QCloseEvent):
        from widgets import pop_messagebox

        if self.tab_bar.is_save_file_needed():
            pop_messagebox(self, event, self.tab_bar)



if __name__ == '__main__':
    format = QSurfaceFormat()
    format.setRenderableType(QSurfaceFormat.RenderableType.OpenGL)
    format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    format.setVersion(3, 3)
    format.setSwapBehavior(QSurfaceFormat.SwapBehavior.DoubleBuffer)
    format.setDepthBufferSize(144)
    QSurfaceFormat.setDefaultFormat(format)
    app = QApplication(sys.argv)
    window = IDE(app.clipboard())
    window.show()
    sys.exit(app.exec())