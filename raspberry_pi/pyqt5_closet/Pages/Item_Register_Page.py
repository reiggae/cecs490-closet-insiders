from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *

color_list = ["red","orange","yellow","green","blue","purple","black","white","gray","brown"]

class Item_Register_Page(QWidget):
    class Color_Tags_Bar(QWidget):
        class Tag_Button(QPushButton):
            def __init__(self, input_color, parent=None):
                self.tag = input_color

                super().__init__(parent)

                self.setMinimumSize(50,50)
                self.setMaximumSize(50,50)
                self.setCheckable(True)

                self.layout = QVBoxLayout()
                self.setLayout(self.layout)
                self.color_box = QWidget()
                self.color_box.setStyleSheet(f"background-color: {input_color}")
                self.layout.addWidget(self.color_box)

        def __init__(self, parent=None):
            super().__init__(parent)

            self.layout = QHBoxLayout()
            self.setLayout(self.layout)
            self.color_buttons = []

            for color in color_list:
                self.new_button = self.Tag_Button(color)
                self.color_buttons.append(self.new_button)
                self.layout.addWidget(self.new_button)

    class Other_Tags_Bar(QWidget):
        class Tag_Button(QPushButton):
            def __init__(self, input_tag, parent=None):
                self.tag = input_tag

                super().__init__(parent)

                self.setMinimumSize(100,100)
                self.setMaximumSize(100,100)
                self.setCheckable(True)

                self.layout = QVBoxLayout()
                self.setLayout(self.layout)
                self.image = QLabel()
                self.image.setScaledContents(True)
                self.layout.addWidget(self.image)

        def __init__(self, parent=None):
            super().__init__(parent)

            self.layout = QHBoxLayout()
            self.setLayout(self.layout)

            self.top_button = self.Tag_Button("top")
            self.top_button.image.setPixmap(QPixmap('Item_Images/placeholder_shirt.png'))
            self.bottom_button = self.Tag_Button("bottom")
            self.bottom_button.image.setPixmap(QPixmap('Item_Images/placeholder_pants.png'))
            self.shoe_button = self.Tag_Button("shoe")
            self.shoe_button.image.setPixmap(QPixmap('Item_Images/placeholder_shoes.png'))
            self.hanger_button = self.Tag_Button("hanger")
            self.hanger_button.image.setPixmap(QPixmap('Item_Images/hanger.png'))

            self.layout.addWidget(self.top_button)
            self.layout.addWidget(self.bottom_button)
            self.layout.addWidget(self.shoe_button)
            self.layout.addWidget(self.hanger_button)

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

        self.color_tags_bar = self.Color_Tags_Bar()
        self.other_tags_bar = self.Other_Tags_Bar()


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
        self.layout.addWidget(self.color_tags_bar)
        self.layout.addWidget(self.other_tags_bar)
        self.layout.addWidget(self.tag_input)
        self.layout.addWidget(self.confirm_button)
        self.layout.addWidget(self.exit_button)

