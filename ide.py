import sys
from PyQt6.QtWidgets import QTreeView, QFileDialog, QLabel, QApplication, QMainWindow, QDockWidget, QTextEdit
from PyQt6.QtGui import  QFont, QSurfaceFormat, QAction, QFileSystemModel
from PyQt6.QtCore import Qt, QDir
from highlighter import PythonSyntaxHighlighter
from shortcuts import *
from show_errors import ShowErrors

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        import widgets

        self.setWindowTitle("IDE")
        self.setGeometry(100, 100, 800, 600)
        self.setCentralWidget(widgets.central_widget)


        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
                selection-background-color: #007acc;
                padding: 2px;
                margin: 2px;
            }

    """)

        self.doc_string_dock = widgets.DocStringDock(self)

        main_text = widgets.MainText(self.doc_string_dock.doc_panel)

        main_text.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                selection-background-color: #007acc;
                padding: 2px;
                margin: 2px;
            }
                                

                                
            QScrollBar:vertical {
                background: #2d2d2d;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical {
                background: #5a5a5a;
                min-height: 20px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

        """)



        with open('highlighter.py', 'r', encoding='utf-8') as f:
            main_text.setPlainText(f.read())



        widgets.layout.addWidget(main_text)

        self.highlighter = PythonSyntaxHighlighter(main_text.document())
        self.remove_line = MainTextShortcuts(main_text, main_text.completer)
        self.show_error = ShowErrors(main_text, self.highlighter)
        main_text.setFont(QFont("Maple Mono", self.remove_line.font_size))


        self.error_label = QLabel("Ready")

        self.error_label.setStyleSheet("""
                QLabel {
                    color: white;
                }
""")

        self.show_error.error_label = self.error_label
        widgets.layout.addWidget(self.error_label)
        self.show_files = widgets.ShowFiles(self, main_text)
        FileDockShortcut(self, self.show_files, self.show_files.file_viewer, self.doc_string_dock, self.doc_string_dock.doc_panel, main_text)


if __name__ == '__main__':
    format = QSurfaceFormat()
    format.setRenderableType(QSurfaceFormat.RenderableType.OpenGL)
    format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    format.setVersion(3, 3)
    format.setSwapBehavior(QSurfaceFormat.SwapBehavior.DoubleBuffer)
    format.setDepthBufferSize(24)
    QSurfaceFormat.setDefaultFormat(format)
    app = QApplication(sys.argv)
    window = IDE()
    window.show()
    sys.exit(app.exec())