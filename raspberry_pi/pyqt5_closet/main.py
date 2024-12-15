from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *

from enum import IntEnum

from Pages.Item_Main_Page import *
from Pages.Item_Register_Page import *
from Pages.Item_Edit_Page import *
from Pages.Camera_Page import *
from Pages.Outfit_Main_Page import *
from Pages.Outfit_Register_Page import *
from Pages.Outfit_Edit_Page import *
from Keyboard.Keyboard import *
from Inventory_System.closet_inventory import *
from Inventory_System.RFIDReader import *

import sys
import time
import board
import neopixel_spi as neopixel

import subprocess

from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2

#TEMP
save_file = "ReiTest.txt"

# Enumerating page numbers
class Page(IntEnum):
    ITEM_MAIN = 0
    ITEM_REGISTER = 1
    ITEM_EDIT = 2
    CAMERA = 3
    OUTFIT_MAIN = 4
    OUTFIT_REGISTER = 5
    OUTFIT_EDIT = 6

closet = []

class Main_Stack(QStackedWidget):
    # Clothing button on item page, shows image and name of item
    class clothing_button(QPushButton):
        def __init__(self, closet_index, parent=None):
            super().__init__(parent)

            # Initialize layout
            self.setLayout(QVBoxLayout())

            # Initialize image
            self.image = QLabel()
            self.image.setPixmap(QPixmap(f"{closet[closet_index].image_name}"))
            self.image.setScaledContents(True)
            self.image.setMaximumSize(150,150)

            # Initialize name
            self.label = QLabel(closet[closet_index].name)

            self.layout().addWidget(self.label,alignment=Qt.AlignTop|Qt.AlignCenter)
            self.layout().addWidget(self.image,alignment=Qt.AlignTop|Qt.AlignCenter)

    #        self.setStyleSheet("border-image : url({});".format(closet[closet_index].image_name))
            self.setMinimumSize(170,190)
            self.setMaximumSize(170,190)

    class outfit_button(QPushButton):
        def __init__(self, outfit_index, parent=None):
            super().__init__(parent)

            self.setLayout(QVBoxLayout())

            # ANDREWTODO4 i havent tested it out so prob wait for me, but this is what making outfit button should look like
            self.top_image = QLabel()
            self.top_image.setPixmap(QPixmap(f"{outfit[outfit_index].top_piece.image_name}"))
            self.top_image.setScaledContents(True)
            self.top_image.setMaximumSize(150,150)

            self.bottom_image = QLabel()
            self.bottom_image.setPixmap(QPixmap(f"{outfit[outfit_index].bottom_piece.image_name}"))
            self.bottom_image.setScaledContents(True)
            self.bottom_image.setMaximumSize(150,150)

            self.shoe_image = QLabel()
            self.shoe_image.setPixmap(QPixmap(f"{outfit[outfit_index].shoe_piece.image_name}"))
            self.shoe_image.setScaledContents(True)
            self.shoe_image.setMaximumSize(150,150)

            # Initialize name
            self.label = QLabel(closet[closet_index].name)

            self.layout().addWidget(self.label,alignment=Qt.AlignTop|Qt.AlignCenter)
            self.layout().addWidget(self.top_image,alignment=Qt.AlignTop|Qt.AlignCenter)
            self.layout().addWidget(self.bottom_image,alignment=Qt.AlignTop|Qt.AlignCenter)
            self.layout().addWidget(self.shoe_image,alignment=Qt.AlignTop|Qt.AlignCenter)

            self.setMinimumSize(500,190)
            self.setMaximumSize(500,190) #maybe 470

    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup keyboard
        self.keyboard = Keyboard()

        # Setup RFID
        self.rfid_reader = RFIDReader("/dev/ttyACM0", 115200)
        self.rfid_reader.rfid_detected.connect(self.on_rfid_detected)
        self.rfid_reader.start()

        # Construct pages
        self.item_main_page = Item_Main_Page()
        self.item_register_page = Item_Register_Page()
        self.item_edit_page = Item_Edit_Page()
        self.camera_page = Camera_Page()
        self.outfit_main_page = Outfit_Main_Page()
        self.outfit_register_page = Outfit_Register_Page()

        # Give pages parent functions
        # FLAG
        self.item_main_page.register_button.clicked.connect(self.go_item_register_page)
        self.item_main_page.outfits_button.clicked.connect(self.go_outfit_main_page)
        self.item_main_page.search_button.clicked.connect(self.generate_item_buttons)
        self.item_main_page.search_bar.installEventFilter(self)
        self.item_register_page.exit_button.clicked.connect(self.go_item_main_page)
        self.item_register_page.camera_button.clicked.connect(self.go_camera_register_page)
        self.item_register_page.confirm_button.clicked.connect(self.register_clothing)
        self.item_register_page.id_input.installEventFilter(self)
        self.item_register_page.name_input.installEventFilter(self)
        self.item_register_page.tag_input.viewport().installEventFilter(self)
        self.item_edit_page.camera_button.clicked.connect(self.go_camera_edit_page)
        self.item_edit_page.confirm_button.clicked.connect(self.edit_clothing)
        self.item_edit_page.delete_button.clicked.connect(self.delete_clothing)
        self.item_edit_page.exit_button.clicked.connect(self.go_item_main_page)
        self.camera_page.camera_button.clicked.connect(self.take_photo)
        self.camera_page.back_button.clicked.connect(self.go_previous_page)
        self.camera_page.qpicamera2.done_signal.connect(self.capture_done)
        self.outfit_main_page.register_button.clicked.connect(self.go_outfit_register_page)
        self.outfit_main_page.search_button.clicked.connect(self.generate_outfit_buttons)
        self.outfit_main_page.clothes_button.clicked.connect(self.go_item_main_page)
        #outfit search button
        #outfit
        #self.outfit_register_page.exit_button.clicked.connect(self.go_outfit_main_page)

        # Connect pages to stacked widget
        self.addWidget(self.item_main_page)
        self.addWidget(self.item_register_page)
        self.addWidget(self.item_edit_page)
        self.addWidget(self.camera_page)
        self.addWidget(self.outfit_main_page)
        self.addWidget(self.outfit_register_page)

    # ITEM MAIN PAGE FUNCTIONS
    def generate_item_buttons(self):
        value_count = 0

        # Deletes existing item buttons
        for i in reversed(range(self.item_main_page.main_scroll_layout.count())):
            self.item_main_page.main_scroll_layout.itemAt(i).widget().setParent(None)

        search_term = self.item_main_page.search_bar.text()

        for i in range(len(closet)):
            if closet[i].contains(search_term):
                newButton = self.clothing_button(i)
                newButton.clicked.connect(lambda state, item_index = i: self.setup_item_edit_page(item_index))
                self.item_main_page.main_scroll_layout.addWidget(newButton, value_count//3, value_count%3, alignment=Qt.AlignTop|Qt.AlignCenter)
                value_count += 1

        self.item_main_page.main_scroll.updateGeometry()

    # ITEM REGISTER PAGE FUNCTIONS
    def register_clothing(self):
        id = self.item_register_page.id_input.text()
        name = self.item_register_page.name_input.text()
        tags = self.item_register_page.tag_input.toPlainText().split('\n') # this looks like "red\nshirt\n"
        tags = [tag.strip() for tag in tags if tag.strip()]

        if Clothing.check_existing_id(closet, id) == False:   # True flag is temp
            image = f"image_{self.item_register_page.image_number}.jpg"
            self.item_register_page.image_number += 1
            input_clothing(closet, id, name, image, tags)

            self.item_register_page.confirm_button.setText("Confirm")

            self.sort_closet(closet)
            self.reset_item_register_page()
            self.go_item_main_page()
        else:

            self.confirm_button.setText("Confirm (Error: ID already taken)")
    def reset_item_register_page(self):
        self.item_register_page.id_input.setText("")
        self.item_register_page.name_input.setText("")
        self.item_register_page.image_preview.setPixmap(QPixmap('Item_Images/placeholder_shirt.png'))
        self.item_register_page.tag_input.setPlainText("")

    def sort_closet(self,closet):
        sort_by_color(closet)
        assign_led(closet)

    def on_rfid_detected(self, rfid_data):
        print(rfid_data)

        curr_index = self.currentIndex()
        if  curr_index == Page.ITEM_MAIN or curr_index == Page.ITEM_REGISTER:
            self.item_register_page.id_input.setText(rfid_data)
            self.go_item_register_page()

    # ITEM EDIT PAGE FUNCTIONS
    def setup_item_edit_page(self, item_index):
        item = closet[item_index]
        self.item_edit_page.closet_index = item_index

        self.item_edit_page.id_input.setText(item.ID)
        self.item_edit_page.name_input.setText(item.name)
        self.item_edit_page.image_preview.setPixmap(QPixmap(f"{item.image_name}"))
        self.item_edit_page.image_preview.setScaledContents(True)
        self.item_edit_page.image_preview.setMaximumSize(100,100)

        tag_input_text = ""
        for tag in item.details:
            tag_input_text += f"{tag}\n"

        self.item_edit_page.tag_input.setPlainText(tag_input_text)

        self.go_item_edit_page()

    def edit_clothing(self):

        id = self.item_edit_page.id_input.text()
        name = self.item_edit_page.name_input.text()
        tags = self.item_edit_page.tag_input.toPlainText().split('\n') # this looks like "red\nshirt\n"
        tags = [tag.strip() for tag in tags if tag.strip()]
        image = f"image_{self.item_register_page.image_number}.jpg"

        update_clothes(closet, id, name, image, tags)
        """
        #ANDREW4 TODO, update based on given index, not ID, sorry i forgot to put it here

        closet_index = self.item_edit_page.closet_index
        update_clothes(closet, closet_index, id, name, image, tags)
        """

        self.item_edit_page.confirm_button.setText("Confirm")

        self.sort_closet(closet)
        self.reset_item_register_page()
        self.go_item_main_page()

    def delete_clothing(self):
        """
        #ANDREW4 TODO
        closet_index = self.item_edit_page.closet_index
        delete_clothing(closet, closet_index) <- idk if this is right, maybe it is
        """

    # CAMERA PAGE FUNCTIONS
    def take_photo(self):
#       qpicamera2.show()
        self.camera_page.camera_button.setEnabled(False)
        self.camera_page.cfg = self.camera_page.picam2.create_still_configuration()

        if(self.camera_page.new_image):
            self.camera_page.picam2.switch_mode_and_capture_file(self.camera_page.cfg, f"image_{self.item_register_page.image_number}.jpg", signal_function=self.camera_page.qpicamera2.signal_done)
        else:
            self.camera_page.picam2.switch_mode_and_capture_file(self.camera_page.cfg, f"{closet[self.item_edit_page.closet_index].image_name}", signal_function=self.camera_page.qpicamera2.signal_done)

    def capture_done(self,job):
        self.camera_page.result = self.camera_page.picam2.wait(job)
        self.camera_page.camera_button.setEnabled(True)

        if(self.camera_page.new_image):
            self.item_register_page.image_preview.setPixmap(QPixmap(f"image_{self.item_register_page.image_number}.jpg"))
            self.go_item_register_page()
        else:
            self.item_edit_page.image_preview.setPixmap(QPixmap(f"closet[self.item_edit_page.closet_index].image_name"))
            self.go_item_edit_page()

    def go_previous_page(self):
        if(self.camera_page.new_image):
            self.go_item_register_page()
        else:
            self.go_item_edit_page()

    # OUTFIT MAIN PAGE FUNCTIONS
    def generate_outfit_buttons(self):
        value_count = 0

        # Deletes existing item buttons
        for i in reversed(range(self.item_outfit_page.main_scroll_layout.count())):
            self.outfit_main_page.main_scroll_layout.itemAt(i).widget().setParent(None)

        search_term = self.outfit_main_page.search_bar.text()

        for i in range(len(closet)):
            if outfit[i].contains(search_term): #ANDREW4 TODO outfit[] currently nothing
                newButton = self.clothing_button(i)
                newButton.clicked.connect(lambda state, item_index = i: self.setup_outfit_edit_page(item_index))
                self.outfit_main_page.main_scroll_layout.addWidget(newButton, value_count//3, value_count%3, alignment=Qt.AlignTop|Qt.AlignCenter)
                value_count += 1

        self.outfit_main_page.main_scroll.updateGeometry()

    # OUTFIT REGISTER PAGE FUNCTIONS
    def generate_outfit_selection_buttons(self):
        #ANDREW4 TODO, set up this code, generates when launching outfit register page

        #iterate through clothing, im using 1 for hardcoded example
        i = 1

        # if clothing item has "top"

        newButton = self.clothing_button(i)
        newButton.clicked.connect(lambda state, item_index = i: self.set_as_top(item_index))
        self.outfit_register_page.top_piece_bar.piece_scroll_layout.addWidget(newButton)
        # else if clothing item has "bottom"
        newButton = self.clothing_button(i)
        newButton.clicked.connect(lambda state, item_index = i: self.set_as_bottom(item_index))
        self.outfit_register_page.bottom_piece_bar.piece_scroll_layout.addWidget(newButton)
        # else if clothing item has "shoe"
        newButton = self.clothing_button(i)
        newButton.clicked.connect(lambda state, item_index = i: self.set_as_shoe(item_index))
        self.outfit_register_page.shoe_piece_bar.piece_scroll_layout.addWidget(newButton)

    def set_as_top(self, item_index):
        self.outfit_register_page.top_piece_bar.piece_image.setPixmap(QPixmap(f"{closet[item_index].image_name}"))
        self.outfit_register_page.top_piece_bar.piece_image.setScaledContents(True)
        self.outfit_register_page.top_piece_bar.piece_image.setMaximumSize(100,100)
        self.outfit_register_page.selected_top = item_index

    def set_as_bottom(self, item_index):
        self.outfit_register_page.bottom_piece_bar.piece_image.setPixmap(QPixmap(f"{closet[item_index].image_name}"))
        self.outfit_register_page.bottom_piece_bar.piece_image.setScaledContents(True)
        self.outfit_register_page.bottom_piece_bar.piece_image.setMaximumSize(100,100)
        self.outfit_register_page.selected_bottom = item_index

    def set_as_shoe(self, item_index):
        self.outfit_register_page.shoe_piece_bar.piece_image.setPixmap(QPixmap(f"{closet[item_index].image_name}"))
        self.outfit_register_page.shoe_piece_bar.piece_image.setScaledContents(True)
        self.outfit_register_page.shoe_piece_bar.piece_image.setMaximumSize(100,100)
        self.outfit_register_page.selected_shoe = item_index

    # OUTFIT EDIT PAGE FUNCTIONS

    # Stacked widget traversing functions
    def go_item_main_page(self):
        self.keyboard.KB_Off()
        self.generate_item_buttons()
        self.setCurrentIndex(Page.ITEM_MAIN)

    def go_item_register_page(self):
        self.keyboard.KB_Off()
        self.setCurrentIndex(Page.ITEM_REGISTER)

    def go_item_edit_page(self):
        self.keyboard.KB_Off()
        self.setCurrentIndex(Page.ITEM_EDIT)

    def go_camera_register_page(self):
        self.keyboard.KB_Off()
        self.camera_page.new_image = True
        self.setCurrentIndex(Page.CAMERA)

    def go_camera_edit_page(self):
        self.keyboard.KB_Off()
        self.setCurrentIndex(Page.CAMERA)

    def go_outfit_main_page(self):
        self.keyboard.KB_Off()
        self.setCurrentIndex(Page.OUTFIT_MAIN)

    def go_outfit_register_page(self):
        self.keyboard.KB_Off()
        self.generate_outfit_selection_buttons()
        self.setCurrentIndex(Page.OUTFIT_REGISTER)

    def go_outfit_edit_page(self):
        self.keyboard.KB_Off()
        self.setCurrentIndex(Page.OUTFIT_EDIT)



    # This function runs when a lineEdit is clicked
    def eventFilter(self,obj, event):
        #Turns on KB
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton and self.keyboard.KB_Active == False:
            self.keyboard.KB_On()
            return True
        #Turns off KB
        elif event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton and self.keyboard.KB_Active == True:
            self.keyboard.KB_Off()
            return True

        return super().eventFilter(obj, event)

    # This function runs when the window is closed
    def closeEvent(self, event):
        self.keyboard.KB_Off() # Turn off keyboard
        save_closet(closet, save_file)

#ANDREW4 TODO debug button on outfit main if u need it
def debug_function():
    print("hi")

if __name__ == "__main__":
    app = QApplication([])

    stacked_widget = Main_Stack()
    load_closet(closet, save_file)
    stacked_widget.go_item_main_page()

    stacked_widget.show()
    stacked_widget.showMaximized()


    debug_button = QPushButton("DEBUG")
    debug_button.clicked.connect(debug_function)
    stacked_widget.outfit_main_page.layout.addWidget(debug_button)

    app.exec()



'''
def light_LED():
    pixels[0] = 0xFF0000
    pixels.show()

### SPI STUFF
spi = board.SPI()
pixels = neopixel.NeoPixel_SPI(spi, 60, pixel_order=neopixel.GRB, auto_write=False)
pixels.fill(0x000000)
pixels.show()
'''
