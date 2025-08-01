from PyQt6.QtCore import QSettings

class Setting(QSettings):
    def __init__(self):
        super().__init__('Kryypto', 'Saves')