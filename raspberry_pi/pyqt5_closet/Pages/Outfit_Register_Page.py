from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *

class Outfit_Register_Page(QWidget):
    class clothing_piece_bar(QWidget):
        def __init__(self, piece_name, parent=None):
            super().__init__(parent)

            self.piece_scroll = QScrollArea()
            self.piece_scroll_area_contents = QWidget()
            self.piece_scroll_layout = QHBoxLayout()

            self.piece_scroll_area_contents.setLayout(self.piece_scroll_layout)
            QScroller.grabGesture(self.piece_scroll.viewport(), QScroller.LeftMouseButtonGesture)
            self.piece_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.piece_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.piece_scroll.setWidgetResizable(False)
            self.piece_scroll_layout.setSizeConstraint(QLayout.SetFixedSize)
            self.piece_scroll.setWidget(self.piece_scroll_area_contents)
            self.piece_scroll.setMinimumHeight(140)

            self.piece_image = QLabel(piece_name)
            self.parent_layout = QHBoxLayout()
            self.setLayout(self.parent_layout)
            self.parent_layout.addWidget(self.piece_image)
            self.parent_layout.addWidget(self.piece_scroll)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_top = 0
        self.selected_bottom = 0
        self.selected_shoe = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("NEW OUTFIT DETAILS")
        self.title.setFont(QFont("Sans Serif",32))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Outfit Name")

        self.top_piece_bar = self.clothing_piece_bar("None")
        self.bottom_piece_bar = self.clothing_piece_bar("None")
        self.shoe_piece_bar = self.clothing_piece_bar("None")

        self.tag_input = QPlainTextEdit()
        self.tag_input.setPlaceholderText("Tag1\nTag2\n...")
#        self.tag_input.setMaximumHeight(50)

        self.confirm_button = QPushButton("Confirm New Outfit")
        self.exit_button = QPushButton("Exit")

        self.layout.addWidget(self.title, alignment = Qt.AlignTop|Qt.AlignCenter)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.top_piece_bar)
        self.layout.addWidget(self.bottom_piece_bar)
        self.layout.addWidget(self.shoe_piece_bar)
        self.layout.addWidget(self.tag_input)
        self.layout.addWidget(self.confirm_button)
        self.layout.addWidget(self.exit_button)

#        self.confirm_button.clicked.connect(self.register_clothing)
#        self.exit_button.clicked.connect(self.debug)

