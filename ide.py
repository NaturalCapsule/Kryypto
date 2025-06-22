import sys
from PyQt6.QtWidgets import QLabel, QApplication, QMainWindow, QTabBar
from PyQt6.QtGui import  QFont, QSurfaceFormat
from highlighter import PythonSyntaxHighlighter
from show_errors import ShowErrors
from shortcuts import *
from get_style import get_css_style

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        import widgets

        self.doc_string_dock = widgets.DocStringDock(self)

        main_text = widgets.MainText(self.doc_string_dock.doc_panel)

        self.tab_bar = widgets.ShowOpenedFile(main_text)

        self.setWindowTitle("IDE")
        self.setGeometry(100, 100, 800, 600)
        self.setCentralWidget(widgets.central_widget)

        self.setObjectName("MainWindow")
        self.setStyleSheet(get_css_style())



        with open('lines.py', 'r', encoding='utf-8') as f:
            main_text.setPlainText(f.read())

        widgets.layout.addWidget(main_text)

        self.highlighter = PythonSyntaxHighlighter(main_text.document())
        self.remove_line = MainTextShortcuts(main_text, main_text.completer, self.tab_bar)
        self.show_error = ShowErrors(main_text, self.highlighter)
        main_text.setFont(QFont("Maple Mono", self.remove_line.font_size))


        self.error_label = QLabel("Ready")

        self.error_label.setObjectName("SyntaxChecker")
        self.error_label.setStyleSheet(get_css_style())

        self.show_error.error_label = self.error_label
        widgets.layout.addWidget(self.error_label)
        self.show_files = widgets.ShowFiles(self, main_text, self.tab_bar)
        # self.terminal = widgets.Terminal(self)
        FileDockShortcut(self, self.show_files, self.show_files.file_viewer, self.doc_string_dock, self.doc_string_dock.doc_panel, main_text)

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
    window = IDE()
    window.show()
    sys.exit(app.exec())