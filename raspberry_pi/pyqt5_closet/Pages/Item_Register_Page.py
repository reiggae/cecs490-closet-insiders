from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *

class Item_Register_Page(QWidget):
    def __init__(self, parent=None):
        self.image_number = 0
        self.image_taken = False
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        #
        self.title = QLabel("NEW ITEM DETAILS")
        self.title.setFont(QFont("Sans Serif",32))

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID Number (scan to auto fill)")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        self.image_preview = QLabel()
        self.image_preview.setPixmap(QPixmap('Item_Images/placeholder_shirt.png'))
        self.image_preview.setScaledContents(True)
        self.image_preview.setMaximumSize(100,100)

        self.camera_button = QPushButton("Open Camera")

        self.tag_input = QPlainTextEdit()
        self.tag_input.setPlaceholderText("Tag1\nTag2\n...")
#        self.tag_input.setMaximumHeight(50)

        self.confirm_button = QPushButton("Confirm New Item")
        self.exit_button = QPushButton("Exit")

        self.layout.addWidget(self.title, alignment = Qt.AlignTop|Qt.AlignCenter)
        self.layout.addWidget(self.id_input)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.image_preview, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.camera_button)
        self.layout.addWidget(self.tag_input)
        self.layout.addWidget(self.confirm_button)
        self.layout.addWidget(self.exit_button)

