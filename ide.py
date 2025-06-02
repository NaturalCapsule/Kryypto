import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QFont
from highlighter import PythonSyntaxHighlighter
from shortcuts import *

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        import widgets

        self.setWindowTitle("IDE")
        self.setGeometry(100, 100, 800, 600)
        self.setCentralWidget(widgets.central_widget)
        
        main_text = widgets.MainText()
        
        widgets.layout.addWidget(main_text)

        self.highlighter = PythonSyntaxHighlighter(main_text.document())
        self.remove_line = MainTextShortcuts(main_text)
        main_text.setFont(QFont("JetBrains Mono", self.remove_line.font_size))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IDE()
    window.show()
    sys.exit(app.exec())