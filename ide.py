import sys
from PyQt6.QtWidgets import QFileDialog, QLabel, QApplication, QMainWindow, QDockWidget, QTextEdit
from PyQt6.QtGui import QFont, QSurfaceFormat, QAction
from PyQt6.QtCore import Qt
from highlighter import PythonSyntaxHighlighter
from shortcuts import *
from show_errors import ShowErrors
import os

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        import widgets

        self.setWindowTitle("IDE")
        self.setGeometry(100, 100, 800, 600)
        self.setCentralWidget(widgets.central_widget)

        self.doc_panel = QTextEdit()
        self.doc_panel.setReadOnly(True)
        self.doc_panel.setMinimumHeight(120)
        # self.doc_panel.setMinimumWidth(900)
        # self.doc_panel.setFixedWidth(900)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
                selection-background-color: #007acc;
                padding: 2px;
                margin: 2px;
            }

    """)


        main_text = widgets.MainText(self.doc_panel)

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



        with open('show_errors.py', 'r', encoding='utf-8') as f:
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

        save_file = QAction('Save File', self)
        save_file.setShortcut("Ctrl+S")
        save_file.setStatusTip("Save File")

        save_file.triggered.connect(lambda: self.save_file(main_text))


        dock = QDockWidget("Docstring", self)
        dock.setWidget(self.doc_panel)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        dock.setStyleSheet("""
            QDockWidget {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                color: #ffffff;
            }

            QTextEdit {
                background-color: #252526;
                color: #d4d4d4;
                font-family: Consolas, monospace;
                font-size: 19px;
                padding: 5px;
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


    def save_file(self, main_text):
        name = QFileDialog.getSaveFileName(self, 'Save File')

        with open(name, 'w') as f:
            save_file = f.write(main_text.toPlainText())
            save_file.close()

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