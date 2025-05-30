import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QFont
from highlighter import PythonSyntaxHighlighter


class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        import widgets
        self.setWindowTitle("IDE")

        self.setGeometry(100, 100, 800, 600)
        
        self.setCentralWidget(widgets.central_widget)
        

        widgets.main_text.setFont(QFont("JetBrains Mono", 19))
        widgets.layout.addWidget(widgets.main_text)
        
        self.highlighter = PythonSyntaxHighlighter(widgets.main_text.document())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IDE()
    window.show()
    sys.exit(app.exec())