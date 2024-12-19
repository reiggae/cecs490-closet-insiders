from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *

class Outfit_Main_Page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Initialize main page widgets
        self.inventory_label = QLabel("OUTFITS")
        self.inventory_label.setFont(QFont("Sans Serif",32))

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Bar")

        self.search_button = QPushButton("Search")

        self.main_scroll = QScrollArea()
        self.scroll_area_contents = QWidget()
        self.main_scroll_layout = QGridLayout()
        self.main_scroll_layout.setSizeConstraint(QLayout.SetFixedSize)

        #TEMP
#        row = 0
#        col = 0
#        for row in range(0,20):
#            for col in range(0,3):
#                object = QPushButton(str(row))
#                object.setMinimumSize(100,100)
#                object.setMaximumSize(100,100)
#                self.main_scroll_layout.addWidget(object,row,col)

        self.scroll_area_contents.setLayout(self.main_scroll_layout)
        QScroller.grabGesture(self.main_scroll.viewport(), QScroller.LeftMouseButtonGesture)
        self.main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_scroll.setWidgetResizable(False)
        self.main_scroll.setWidget(self.scroll_area_contents)

        self.led_off_button = QPushButton("Turn Off All Lights")
        self.register_button = QPushButton("Register New Outfit")
        self.clothes_button = QPushButton("CLOTHES")

        # Initialize main page layout
        self.layout.addWidget(self.inventory_label, alignment = Qt.AlignTop|Qt.AlignCenter)
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.main_scroll)
        self.layout.addWidget(self.led_off_button)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.clothes_button)
