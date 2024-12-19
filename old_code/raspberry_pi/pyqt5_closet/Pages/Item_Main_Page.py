from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *

class Item_Main_Page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Initialize main page widgets
        self.inventory_label = QLabel("INVENTORY")
        self.inventory_label.setFont(QFont("Sans Serif",32))

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Bar")

        self.search_button = QPushButton("Search")

        self.sort_select = QComboBox()
        self.sort_select.addItem("Sort By Color")
        self.sort_select.addItem("Sort By Alphabet")
        self.sort_select.addItem("Sort By Type")
        self.sort_select.addItem("No Sort")

        self.main_scroll = QScrollArea()
        self.scroll_area_contents = QWidget()
        self.main_scroll_layout = QGridLayout()
        self.main_scroll_layout.setSizeConstraint(QLayout.SetFixedSize)

#        #TEMP
#        row = 0
#        col = 0
#        for row in range(0,20):
#            for col in range(0,3):
#                object = QPushButton(str(row))
#                object.setMinimumSize(170,170)
#                object.setMaximumSize(170,170)
#                self.main_scroll_layout.addWidget(object,row,col)

        self.scroll_area_contents.setLayout(self.main_scroll_layout)
        QScroller.grabGesture(self.main_scroll.viewport(), QScroller.LeftMouseButtonGesture)
        self.main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_scroll.setWidgetResizable(False)
        self.main_scroll.setWidget(self.scroll_area_contents)

        self.led_off_button = QPushButton("Turn Off All Lights")
        self.register_button = QPushButton("Register New Item")
        self.outfits_button = QPushButton("OUTFITS")

        # Add widgets to layout
        self.layout.addWidget(self.inventory_label, alignment = Qt.AlignTop|Qt.AlignCenter)
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.sort_select)
        self.layout.addWidget(self.main_scroll)
        self.layout.addWidget(self.led_off_button)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.outfits_button)

        # Connect buttons to functions
#        self.register_button.clicked.connect(go_register_page)
#        self.search_button.clicked.connect(generate_item_buttons)
#        self.outfits_button.clicked.connect(go_outfit_main_page)

#        self.debug_button = QPushButton("DEBUG")
#        self.debug_button.clicked.connect(debug_function)
#        self.layout.addWidget(self.debug_button)

#        self.load_button = QPushButton("Load")
#        self.load_button.clicked.connect(load_function)
#        self.layout.addWidget(self.load_button)

#        self.save_button = QPushButton("Save")
#        self.save_button.clicked.connect(save_function)
#        self.layout.addWidget(self.save_button)
