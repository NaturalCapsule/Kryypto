import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from PyQt6.QtGui import  QFont, QSurfaceFormat, QCloseEvent, QPixmap
from PyQt6.QtCore import Qt
from shortcuts import *
from get_style import get_css_style

class IDE(QMainWindow):
    def __init__(self, clipboard):
        super().__init__()
        self.clipboard = clipboard
        self.setupUI()
        self.setupWidgets()
        # self.

    def setupUI(self):
        import widgets
        self.setWindowTitle("IDE")
        self.setGeometry(100, 100, 800, 600)
        self.setCentralWidget(widgets.central_widget)
        self.setObjectName("MainWindow")
        self.setStyleSheet(get_css_style())

    def setupWidgets(self):
        import widgets

        self.git_panel = widgets.GitDock(self)
        # widgets.layout.addWidget(self.git_panel)

        self.welcome_page = widgets.WelcomeWidget()
        self.list_shortcuts = widgets.ListShortCuts()

        widgets.layout.addWidget(self.welcome_page)

        self.terminal = widgets.TerminalDock(self)
        main_text = widgets.MainText(widgets.layout, self.clipboard)
        self.tab_bar = widgets.ShowOpenedFile(main_text, widgets.layout, widgets.error_label, self, self.welcome_page)

        widgets.layout.addWidget(main_text)

        self.editor_shortcuts = MainTextShortcuts(main_text, main_text.completer, self.tab_bar, widgets.error_label, self.clipboard, widgets.layout, self.terminal, self, self.tab_bar, widgets.file_description, self.list_shortcuts)
        main_text.setFont(QFont("Maple Mono", self.editor_shortcuts.font_size))

        self.show_files = widgets.ShowDirectory(self, main_text, self.tab_bar)
        FileDockShortcut(self, self.show_files, self.show_files.file_viewer, main_text, widgets.file_description, self.tab_bar)

        widgets.layout.addWidget(self.list_shortcuts)

        self.welcome_page.setFocus()

    def closeEvent(self, event: QCloseEvent):
        def pop_messagebox():
                box = QMessageBox(self)

                box.setWindowFlag(Qt.WindowType.FramelessWindowHint)

                box.setText('Hey!\nIt looks like you are trying to close IDE without saving your progress\nDo you really your work go in vain?')

                box.setObjectName('MessageBox')
                box.setStyleSheet(get_css_style())

                save_file = QPushButton(box)
                save_file.setText('Save File')

                save_file.setObjectName('MessageBoxSave')
                save_file.setStyleSheet(get_css_style())

                dont_save = QPushButton(box)
                dont_save.setText("Don't Save")

                dont_save.setObjectName('MessageBoxSaveNot')
                dont_save.setStyleSheet(get_css_style())

                cancel = QPushButton(box)
                cancel.setText('Cancel')

                cancel.setObjectName('MessageBoxCancel')
                cancel.setStyleSheet(get_css_style())

                pixmap = QPixmap('icons/messagebox/warning.png')
                pixmap.size()

                scaled_pixmap = pixmap.scaled(98, 98, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
                box.setIconPixmap(scaled_pixmap)


                box.addButton(save_file, QMessageBox.ButtonRole.YesRole)
                box.addButton(dont_save, QMessageBox.ButtonRole.NoRole)
                box.addButton(cancel, QMessageBox.ButtonRole.RejectRole)

                box.exec()

                if box.clickedButton() == save_file:
                    self.tab_bar.save_current_file()
                    event.accept()
                elif box.clickedButton() == dont_save:
                    event.accept()
                else:
                    event.ignore()

        if self.tab_bar.is_save_file_needed():
            pop_messagebox()



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