## TO-DO: make the auto completer work only for .py files.

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import  QFont, QSurfaceFormat
from highlighter import PythonSyntaxHighlighter
from show_errors import ShowErrors
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
        # self.doc_string_dock = widgets.DocStringDock(self)

        # main_text = widgets.MainText(self.doc_string_dock.doc_panel, widgets.layout, self.clipboard)
        main_text = widgets.MainText(widgets.layout, self.clipboard)

        # main_text.doc_panel = self.doc_string_dock.doc_panel

        self.tab_bar = widgets.ShowOpenedFile(main_text, widgets.layout, widgets.error_label, self)
        # self.tab_bar.commenting
        # self.removeDockWidget()
        widgets.layout.addWidget(main_text)
        # widgets.layout.removeWidget()
        # main_text.find()
        # with open('lines.py', 'r', encoding='utf-8') as f:
        #     main_text.setPlainText(f.read())

        # self.highlighter = PythonSyntaxHighlighter(main_text.document())
        self.editor_shortcuts = MainTextShortcuts(main_text, main_text.completer, self.tab_bar, widgets.layout)
        # self.show_error = ShowErrors(main_text, self.highlighter)
        main_text.setFont(QFont("Maple Mono", self.editor_shortcuts.font_size))

        # self.show_error.error_label = widgets.error_label
        # widgets.layout.addWidget(widgets.error_label)
        self.show_files = widgets.ShowFiles(self, main_text, self.tab_bar)
        # self.terminal = widgets.Terminal(self)
        FileDockShortcut(self, self.show_files, self.show_files.file_viewer, main_text, widgets.file_description, self.tab_bar)
        # FileDockShortcut(self, self.show_files, self.show_files.file_viewer, self.doc_string_dock, self.doc_string_dock.doc_panel, main_text, widgets.file_description, self.tab_bar)



if __name__ == '__main__':
    format = QSurfaceFormat()
    format.setRenderableType(QSurfaceFormat.RenderableType.OpenGL)
    format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    format.setVersion(3, 3)
    format.setSwapBehavior(QSurfaceFormat.SwapBehavior.DoubleBuffer)
    format.setDepthBufferSize(144)
    QSurfaceFormat.setDefaultFormat(format)
    app = QApplication(sys.argv)
    # app.setCursorFlashTime(1500)
    window = IDE(app.clipboard())
    window.show()
    sys.exit(app.exec())