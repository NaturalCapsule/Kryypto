import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import  QFont, QSurfaceFormat
from shortcuts import *
from get_style import get_css_style

class IDE(QMainWindow):
    def __init__(self, clipboard):
        super().__init__()
        self.clipboard = clipboard
        self.setupUI()
        self.setupWidgets()

    def setupUI(self):
        import widgets
        self.setWindowTitle("IDE")
        self.setGeometry(100, 100, 800, 600)
        self.setCentralWidget(widgets.central_widget)
        self.setObjectName("MainWindow")
        self.setStyleSheet(get_css_style())

    def setupWidgets(self):
        import widgets


        self.welcome_page = widgets.WelcomeWidget()
        widgets.layout.addWidget(self.welcome_page)
        self.terminal = widgets.TerminalDock(self)
        main_text = widgets.MainText(widgets.layout, self.clipboard)
        self.tab_bar = widgets.ShowOpenedFile(main_text, widgets.layout, widgets.error_label, self, self.welcome_page)
        widgets.layout.addWidget(main_text)
        self.editor_shortcuts = MainTextShortcuts(main_text, main_text.completer, self.tab_bar, widgets.error_label, self.clipboard, widgets.layout, self.terminal, self, self.tab_bar, widgets.file_description)
        main_text.setFont(QFont("Maple Mono", self.editor_shortcuts.font_size))

        self.show_files = widgets.ShowDirectory(self, main_text, self.tab_bar)
        FileDockShortcut(self, self.show_files, self.show_files.file_viewer, main_text, widgets.file_description, self.tab_bar)


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