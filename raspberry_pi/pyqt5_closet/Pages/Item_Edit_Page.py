from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *

class Item_Edit_Page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.closet_index = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("EDITING")
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

        self.confirm_button = QPushButton("Confirm Changes")
        self.exit_button = QPushButton("Exit Without Changes")

        self.locate_button = QPushButton("Locate")
        self.delete_button = QPushButton("Delete Item")

        self.layout.addWidget(self.title, alignment = Qt.AlignTop|Qt.AlignCenter)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.id_input)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.image_preview, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.camera_button)
        self.layout.addWidget(self.tag_input)
        self.layout.addWidget(self.locate_button)
        self.layout.addWidget(self.confirm_button)
        self.layout.addWidget(self.exit_button)


#        self.camera_button.clicked.connect(go_edit_camera_page)
#        self.confirm_button.clicked.connect(self.edit_clothing)
#        self.exit_button.clicked.connect(go_main_page)


