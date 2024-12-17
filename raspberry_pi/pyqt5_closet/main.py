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
from Inventory_System.outfit import *

import sys
import time
import board
import neopixel_spi as neopixel
import shutil

from picamera2 import Picamera2, Preview
import cv2
import numpy as np
from rembg import remove
from PIL import Image
import os

import random

import subprocess

from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2

#TEMP ANDRE5 rename this if u want to do new save file
save_file = "ITC_Closet_Save.txt"
save_file_2 = "ITC_Outfit_Save.txt"
led_count = 10
# Enumerating page numbers
class Page(IntEnum):
    ITEM_MAIN = 0
    ITEM_REGISTER = 1
    ITEM_EDIT = 2
    CAMERA = 3
    OUTFIT_MAIN = 4
    OUTFIT_REGISTER = 5
    OUTFIT_EDIT = 6

class LED_Color(IntEnum):
    RED = 0xFF0000
    GREEN = 0x00FF00
    BLUE = 0x0000FF
    WHITE = 0xFFFFFF
    CLEAR = 0x000000

color_list = ["red","orange","yellow","green","blue","purple","black","white","gray","brown"]

closet = []
outfits = []

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

            self.setMinimumSize(170,190)
            self.setMaximumSize(170,190)

    class outfit_button(QPushButton):
        def __init__(self, outfit_index, parent=None):
            super().__init__(parent)

            self.setLayout(QVBoxLayout())

            self.extra_image = QLabel()
            if outfits[outfit_index].extra != None:
                self.extra_image.setPixmap(QPixmap(f"{outfits[outfit_index].extra.image_name}"))
            self.extra_image.setScaledContents(True)
            self.extra_image.setMaximumSize(150,150)

            self.top_image = QLabel()
            if outfits[outfit_index].top != None:
                self.top_image.setPixmap(QPixmap(f"{outfits[outfit_index].top.image_name}"))
            self.top_image.setScaledContents(True)
            self.top_image.setMaximumSize(150,150)

            self.bottom_image = QLabel()
            if outfits[outfit_index].bottom != None:
                self.bottom_image.setPixmap(QPixmap(f"{outfits[outfit_index].bottom.image_name}"))
            self.bottom_image.setScaledContents(True)
            self.bottom_image.setMaximumSize(150,150)

            self.shoe_image = QLabel()
            if outfits[outfit_index].shoe != None:
                self.shoe_image.setPixmap(QPixmap(f"{outfits[outfit_index].shoe.image_name}"))
            self.shoe_image.setScaledContents(True)
            self.shoe_image.setMaximumSize(150,150)

            # Initialize name
            self.label = QLabel(outfits[outfit_index].name)

            self.layout().addWidget(self.label,alignment=Qt.AlignTop|Qt.AlignCenter)
            self.layout().addWidget(self.extra_image,alignment=Qt.AlignTop|Qt.AlignCenter)
            self.layout().addWidget(self.top_image,alignment=Qt.AlignTop|Qt.AlignCenter)
            self.layout().addWidget(self.bottom_image,alignment=Qt.AlignTop|Qt.AlignCenter)
            self.layout().addWidget(self.shoe_image,alignment=Qt.AlignTop|Qt.AlignCenter)

            self.setMinimumSize(170,650)
            self.setMaximumSize(170,650) #maybe 470

    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup keyboard
        self.keyboard = Keyboard()

        # Setup RFID
        self.rfid_reader = RFIDReader("/dev/ttyACM0", 115200)
        self.rfid_reader.rfid_detected.connect(self.on_rfid_detected)
        self.rfid_reader.start()

        # Setup SPI/LED Strip
        self.spi = board.SPI()
        self.pixels = neopixel.NeoPixel_SPI(self.spi, 60, pixel_order=neopixel.GRB, auto_write=False)
        self.pixels.fill(LED_Color.CLEAR)
        self.pixels.show()

        # Construct pages
        self.item_main_page = Item_Main_Page()
        self.item_register_page = Item_Register_Page()
        self.item_edit_page = Item_Edit_Page()
        self.camera_page = Camera_Page()
        self.outfit_main_page = Outfit_Main_Page()
        self.outfit_register_page = Outfit_Register_Page()
        self.outfit_edit_page = Outfit_Edit_Page()

        # Give pages parent functions
        # FLAG
        self.item_main_page.register_button.clicked.connect(self.go_item_register_page)
        self.item_main_page.outfits_button.clicked.connect(self.go_outfit_main_page)
        self.item_main_page.led_off_button.clicked.connect(self.turn_leds_off)
        self.item_main_page.search_button.clicked.connect(self.generate_item_buttons)
        self.item_main_page.sort_select.activated.connect(self.generate_item_buttons)
        self.item_main_page.search_bar.installEventFilter(self)
        self.item_register_page.exit_button.clicked.connect(self.go_item_main_page)
        self.item_register_page.camera_button.clicked.connect(self.go_camera_register_page)
        self.item_register_page.confirm_button.clicked.connect(self.register_clothing)
        self.item_register_page.id_input.installEventFilter(self)
        self.item_register_page.name_input.installEventFilter(self)
        self.item_register_page.tag_input.viewport().installEventFilter(self)
        self.item_edit_page.camera_button.clicked.connect(self.go_camera_edit_page)
        self.item_edit_page.confirm_button.clicked.connect(self.edit_clothing)
        self.item_edit_page.locate_button.clicked.connect(self.locate_item)
        self.item_edit_page.delete_button.clicked.connect(self.delete_clothing)
        self.item_edit_page.exit_button.clicked.connect(self.go_item_main_page)
        self.item_edit_page.id_input.installEventFilter(self)
        self.item_edit_page.name_input.installEventFilter(self)
        self.item_edit_page.tag_input.viewport().installEventFilter(self)
        self.camera_page.camera_button.clicked.connect(self.take_photo)
        self.camera_page.back_button.clicked.connect(self.go_previous_page)
        self.camera_page.qpicamera2.done_signal.connect(self.capture_done)
        self.outfit_main_page.register_button.clicked.connect(self.go_outfit_register_page)
        self.outfit_main_page.led_off_button.clicked.connect(self.turn_leds_off)
        self.outfit_main_page.search_button.clicked.connect(self.generate_outfit_buttons)
        self.outfit_main_page.clothes_button.clicked.connect(self.go_item_main_page)
        self.outfit_main_page.search_bar.installEventFilter(self)
        self.outfit_register_page.random_button.clicked.connect(self.randomize_selection)
        self.outfit_register_page.exit_button.clicked.connect(self.go_outfit_main_page)
        self.outfit_register_page.confirm_button.clicked.connect(self.register_outfit)
        self.outfit_register_page.name_input.installEventFilter(self)
        self.outfit_register_page.tag_input.viewport().installEventFilter(self)
        self.outfit_edit_page.exit_button.clicked.connect(self.go_outfit_main_page)
        self.outfit_edit_page.confirm_button.clicked.connect(self.edit_outfit)
        self.outfit_edit_page.locate_button.clicked.connect(self.locate_outfit)
        self.outfit_edit_page.delete_button.clicked.connect(self.delete_outfit)
        self.outfit_edit_page.name_input.installEventFilter(self)
        self.outfit_edit_page.tag_input.viewport().installEventFilter(self)
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
        self.addWidget(self.outfit_edit_page)

    # ITEM MAIN PAGE FUNCTIONS
    def generate_item_buttons(self):
        sort_option = self.item_main_page.sort_select.currentText()
        self.sort_closet(closet, sort_option)


        value_count = 0

        # Deletes existing item buttons
        for i in reversed(range(self.item_main_page.main_scroll_layout.count())):
            self.item_main_page.main_scroll_layout.itemAt(i).widget().setParent(None)

        search_term = self.item_main_page.search_bar.text()

        for i in range(len(closet)):
            if closet[i].contains(search_term):
                newButton = self.clothing_button(i)
                newButton.clicked.connect(lambda state, item_index = i: self.setup_item_edit_page(item_index))

                if closet[i].is_checked_in:
                    newButton.setStyleSheet("")
                else:
                    newButton.setStyleSheet("border: 1px dashed black;")


                self.item_main_page.main_scroll_layout.addWidget(newButton, value_count//3, value_count%3, alignment=Qt.AlignTop|Qt.AlignCenter)
                value_count += 1

        self.item_main_page.main_scroll.updateGeometry()

    def turn_leds_off(self):
        self.pixels.fill(LED_Color.CLEAR) # Turn off LEDs
        self.pixels.show()

    # ITEM REGISTER PAGE FUNCTIONS
    def register_clothing(self):

        id = self.item_register_page.id_input.text()
        name = self.item_register_page.name_input.text()
        tags = self.item_register_page.tag_input.toPlainText().split('\n') # this looks like "red\nshirt\n"
        tags = [tag.strip() for tag in tags if tag.strip()]

        if self.item_register_page.other_tags_bar.top_button.isChecked():
            tags.append("top")
        if self.item_register_page.other_tags_bar.bottom_button.isChecked():
            tags.append("bottom")
        if self.item_register_page.other_tags_bar.shoe_button.isChecked():
            tags.append("shoe")
        if self.item_register_page.other_tags_bar.hanger_button.isChecked():
            tags.append("hanger")

        for color in self.item_register_page.color_tags_bar.color_buttons:
            if color.isChecked():
                tags.append(color.tag)

        if Clothing.check_existing_id(closet, id) == False:
            if(self.item_register_page.image_taken == False):
                shutil.copy('Item_Images/placeholder_shirt.png', f"Item_Images/image_{self.item_register_page.image_number}.png")
            image = f"Item_Images/image_{self.item_register_page.image_number}.png"



            self.item_register_page.image_number += 1
            input_clothing(closet, id, name, image, tags)

            self.item_register_page.confirm_button.setText("Confirm")

#            self.sort_closet(closet)
            self.reset_item_register_page()
            self.go_item_main_page()
        else:

            self.confirm_button.setText("Confirm (Error: ID already taken)")

    def randomize_selection(self):
        extra_list = []
        top_list = []
        bottom_list = []
        shoe_list = []

        for i, item in enumerate(closet):
            if item.contains("top"):
                top_list.append(i)
            elif item.contains("bottom"):
                bottom_list.append(i)
            elif item.contains("shoe"):
                shoe_list.append(i)
            else:
                extra_list.append(i)

        self.set_as_extra(random.choice(extra_list))
        self.set_as_top(random.choice(top_list))
        self.set_as_bottom(random.choice(bottom_list))
        self.set_as_shoe(random.choice(shoe_list))

    def reset_item_register_page(self):
        self.item_register_page.id_input.setText("")
        self.item_register_page.name_input.setText("")
        self.item_register_page.image_preview.setPixmap(QPixmap('Item_Images/placeholder_shirt.png'))
        self.item_register_page.tag_input.setPlainText("")

        for color in self.item_register_page.color_tags_bar.color_buttons:
            color.setChecked(False)

        self.item_register_page.image_taken = False

    def sort_closet(self,closet, option):
        if option == "Sort By Color":
            sort_by_color(closet)
        elif option == "Sort By Alphabet":
            pass #ANDREW7 TODO
        elif option == "Sort By Type":
            pass

        map_closet_to_leds(closet, num_leds = led_count)

    def on_rfid_detected(self, rfid_data):
        print(rfid_data)

        for i, clothing in enumerate(closet):
            if rfid_data == clothing.ID:
                if clothing.is_checked_in:
                    clothing.is_checked_in = False
                else:
                    clothing.is_checked_in = True


                self.setup_item_edit_page(i)
                self.go_item_edit_page()

                return

        curr_index = self.currentIndex()
        if  curr_index == Page.ITEM_MAIN or curr_index == Page.ITEM_REGISTER:
            self.go_item_register_page()
            self.item_register_page.id_input.setText(rfid_data)


    # ITEM EDIT PAGE FUNCTIONS
    def setup_item_edit_page(self, item_index):
        item = closet[item_index]
        self.item_edit_page.closet_index = item_index

        self.item_edit_page.id_input.setText(item.ID)
        self.item_edit_page.name_input.setText(item.name)
        self.item_edit_page.image_preview.setPixmap(QPixmap(f"{item.image_name}"))

        if item.contains("top"):
            self.item_edit_page.locate_button.setStyleSheet("background-color: red")
        elif item.contains("bottom"):
            self.item_edit_page.locate_button.setStyleSheet("background-color: blue")
        elif item.contains("shoe"):
            self.item_edit_page.locate_button.setStyleSheet("background-color: green")
        else:
            self.item_edit_page.locate_button.setStyleSheet("background-color: white")

        if item.is_checked_in:
            self.item_edit_page.image_preview.setStyleSheet("")
        else:
            self.item_edit_page.image_preview.setStyleSheet("border: 1px dashed black;")

        tag_input_text = ""

        if "top" in item.details:
            self.item_edit_page.other_tags_bar.top_button.setChecked(True)
        else:
            self.item_edit_page.other_tags_bar.top_button.setChecked(False)

        if "bottom" in item.details:
            self.item_edit_page.other_tags_bar.bottom_button.setChecked(True)
        else:
            self.item_edit_page.other_tags_bar.bottom_button.setChecked(False)

        if "shoe" in item.details:
            self.item_edit_page.other_tags_bar.shoe_button.setChecked(True)
        else:
            self.item_edit_page.other_tags_bar.shoe_button.setChecked(False)

        if "hanger" in item.details:
            self.item_edit_page.other_tags_bar.hanger_button.setChecked(True)
        else:
            self.item_edit_page.other_tags_bar.hanger_button.setChecked(False)

        for color in self.item_edit_page.color_tags_bar.color_buttons:
            color.setChecked(False)

        for tag in item.details:
            lc_tag = tag.lower()
            if lc_tag in color_list:
                for color in self.item_edit_page.color_tags_bar.color_buttons:
                    if lc_tag == color.tag:
                        color.setChecked(True)
            else:
                if not lc_tag in ["top", "bottom", "shoe", "hanger"]:
                    tag_input_text += f"{tag}\n"

        self.item_edit_page.tag_input.setPlainText(tag_input_text)

        self.go_item_edit_page()

    def edit_clothing(self):

        id = self.item_edit_page.id_input.text()
        name = self.item_edit_page.name_input.text()
        tags = self.item_edit_page.tag_input.toPlainText().split('\n') # this looks like "red\nshirt\n"
        tags = [tag.strip() for tag in tags if tag.strip()]

        for color in self.item_edit_page.color_tags_bar.color_buttons:
            if color.isChecked():
                tags.append(color.tag)

        if self.item_edit_page.other_tags_bar.top_button.isChecked():
            tags.append("top")
        if self.item_edit_page.other_tags_bar.bottom_button.isChecked():
            tags.append("bottom")
        if self.item_edit_page.other_tags_bar.shoe_button.isChecked():
            tags.append("shoe")
        if self.item_edit_page.other_tags_bar.hanger_button.isChecked():
            tags.append("hanger")

        image = f"image_{self.item_register_page.image_number}.png"

        closet_index = self.item_edit_page.closet_index
        update_clothes(closet, closet_index, id, name, image, tags)


        self.item_edit_page.confirm_button.setText("Confirm")

#        self.sort_closet(closet)
        self.reset_item_register_page()
        self.go_item_main_page()

    def delete_clothing(self):
        closet_index = self.item_edit_page.closet_index
        item = closet[closet_index]
        remove_clothes(closet, closet_index)

        if item.contains("top"):
            delete = "top"
        elif item.contains("bottom"):
            delete = "bottom"
        elif item.contains("shoe"):
            delete = "shoe"
        else:
            delete = "extra"

        for outfit in outfits:
            if delete == "top":
                if item == outfit.top:
                    outfit.top = None
            elif delete == "bottom":
                if item == outfit.bottom:
                    outfit.bottom = None
            elif delete == "shoe":
                if item == outfit.shoe:
                    outfit.shoe = None
            elif delete == "extra":
                if item == outfit.extra:
                    outfit.extra = None

        self.reset_item_register_page()
        self.go_item_main_page()
        #REI6 TODO

    def locate_item(self):

        clothing = closet[self.item_edit_page.closet_index]

        led_index = int(clothing.led_number)

        if clothing.led_on == True:
            self.pixels[led_index] = LED_Color.CLEAR
            clothing.led_on = False
        elif clothing.led_on == False:
            if clothing.contains("top"):
                self.pixels[led_index] = LED_Color.RED
                clothing.led_on = True
            elif clothing.contains("bottom"):
                self.pixels[led_index] = LED_Color.BLUE
            elif clothing.contains("shoe"):
                self.pixels[led_index] = LED_Color.GREEN
            else:
                self.pixels[led_index] = LED_Color.WHITE # 0xrrggbb
            clothing.led_on = True

        self.pixels.show()


    # CAMERA PAGE FUNCTIONS
    def take_photo(self):
#       qpicamera2.show()
        if(self.item_register_page.image_number == None):
            self.item_register_page.image_number = 0

        self.camera_page.camera_button.setEnabled(False)
        self.camera_page.cfg = self.camera_page.picam2.create_still_configuration()

        if(self.camera_page.new_image):
            self.camera_page.picam2.switch_mode_and_capture_file(self.camera_page.cfg, f"Item_Images/image_{self.item_register_page.image_number}.png", signal_function=self.camera_page.qpicamera2.signal_done)
        else:
            self.camera_page.picam2.switch_mode_and_capture_file(self.camera_page.cfg, f"{closet[self.item_edit_page.closet_index].image_name}", signal_function=self.camera_page.qpicamera2.signal_done)

    def capture_done(self,job):

        captured_image = Image.open(f"Item_Images/image_{self.item_register_page.image_number}.png")

        output_path = f"Item_Images/image_{self.item_register_page.image_number}.png"

        output_image = remove(captured_image)
        output_image.save(output_path)

        self.camera_page.result = self.camera_page.picam2.wait(job)
        self.camera_page.camera_button.setEnabled(True)

        if(self.camera_page.new_image):
            self.item_register_page.image_preview.setPixmap(QPixmap(f"Item_Images/image_{self.item_register_page.image_number}.png"))
            self.item_register_page.image_taken = True
            self.go_item_register_page()
        else:
            self.item_edit_page.image_preview.setPixmap(QPixmap(f"{closet[self.item_edit_page.closet_index].image_name}"))
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
        for i in reversed(range(self.outfit_main_page.main_scroll_layout.count())):
            self.outfit_main_page.main_scroll_layout.itemAt(i).widget().setParent(None)

        search_term = self.outfit_main_page.search_bar.text()

        for i in range(len(outfits)):
            if outfits[i].contains(search_term):
                newButton = self.outfit_button(i)

                if outfits[i].extra != None:
                    if outfits[i].extra.is_checked_in:
                         newButton.extra_image.setStyleSheet("")
                    else:
                        newButton.extra_image.setStyleSheet("border: 1px dashed black")

                if outfits[i].top != None:
                    if outfits[i].top.is_checked_in:
                         newButton.top_image.setStyleSheet("")
                    else:
                        newButton.top_image.setStyleSheet("border: 1px dashed black")

                if outfits[i].bottom != None:
                    if outfits[i].bottom.is_checked_in:
                         newButton.bottom_image.setStyleSheet("")
                    else:
                        newButton.bottom_image.setStyleSheet("border: 1px dashed black")

                if outfits[i].shoe != None:
                    if outfits[i].shoe.is_checked_in:
                         newButton.shoe_image.setStyleSheet("")
                    else:
                        newButton.shoe_image.setStyleSheet("border: 1px dashed black")

                newButton.clicked.connect(lambda state, item_index = i: self.setup_outfit_edit_page(item_index))
                self.outfit_main_page.main_scroll_layout.addWidget(newButton, value_count//3, value_count%3, alignment=Qt.AlignTop|Qt.AlignCenter)
                value_count += 1

        self.outfit_main_page.main_scroll.updateGeometry()

    # OUTFIT REGISTER PAGE FUNCTIONS
    def generate_outfit_selection_buttons(self):

        for i in reversed(range(self.outfit_register_page.extra_piece_bar.piece_scroll_layout.count())):
            self.outfit_register_page.extra_piece_bar.piece_scroll_layout.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.outfit_register_page.top_piece_bar.piece_scroll_layout.count())):
            self.outfit_register_page.top_piece_bar.piece_scroll_layout.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.outfit_register_page.bottom_piece_bar.piece_scroll_layout.count())):
            self.outfit_register_page.bottom_piece_bar.piece_scroll_layout.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.outfit_register_page.shoe_piece_bar.piece_scroll_layout.count())):
            self.outfit_register_page.shoe_piece_bar.piece_scroll_layout.itemAt(i).widget().setParent(None)

        blank_button = QPushButton("None")
        blank_button.setMinimumSize(170,190)
        blank_button.setMaximumSize(170,190)
        blank_button.clicked.connect(lambda state, item_index = None: self.set_as_extra(item_index))
        self.outfit_register_page.extra_piece_bar.piece_scroll_layout.addWidget(blank_button)

        blank_button = QPushButton("None")
        blank_button.setMinimumSize(170,190)
        blank_button.setMaximumSize(170,190)
        blank_button.clicked.connect(lambda state, item_index = None: self.set_as_top(item_index))
        self.outfit_register_page.top_piece_bar.piece_scroll_layout.addWidget(blank_button)

        blank_button = QPushButton("None")
        blank_button.setMinimumSize(170,190)
        blank_button.setMaximumSize(170,190)
        blank_button.clicked.connect(lambda state, item_index = None: self.set_as_bottom(item_index))
        self.outfit_register_page.bottom_piece_bar.piece_scroll_layout.addWidget(blank_button)

        blank_button = QPushButton("None")
        blank_button.setMinimumSize(170,190)
        blank_button.setMaximumSize(170,190)
        blank_button.clicked.connect(lambda state, item_index = None: self.set_as_shoe(item_index))
        self.outfit_register_page.shoe_piece_bar.piece_scroll_layout.addWidget(blank_button)

        # if clothing item has "top"
        for i, clothing in enumerate(closet):
            if clothing.contains("top"):
                newButton = self.clothing_button(i)
                newButton.clicked.connect(lambda state, item_index = i: self.set_as_top(item_index))
                self.outfit_register_page.top_piece_bar.piece_scroll_layout.addWidget(newButton)
        # else if clothing item has "bottom"
            elif clothing.contains("bottom"):
                newButton = self.clothing_button(i)
                newButton.clicked.connect(lambda state, item_index = i: self.set_as_bottom(item_index))
                self.outfit_register_page.bottom_piece_bar.piece_scroll_layout.addWidget(newButton)
            elif clothing.contains("shoe"):
        # else if clothing item has "shoe"
                newButton = self.clothing_button(i)
                newButton.clicked.connect(lambda state, item_index = i: self.set_as_shoe(item_index))
                self.outfit_register_page.shoe_piece_bar.piece_scroll_layout.addWidget(newButton)
            else:
                newButton = self.clothing_button(i)
                newButton.clicked.connect(lambda state, item_index = i: self.set_as_extra(item_index))
                self.outfit_register_page.extra_piece_bar.piece_scroll_layout.addWidget(newButton)

    def set_as_extra(self, item_index):
        if item_index == None:
            self.outfit_register_page.extra_piece_bar.piece_image.setText("No Extra               ")
        else:
            self.outfit_register_page.extra_piece_bar.piece_image.setPixmap(QPixmap(f"{closet[item_index].image_name}"))
        self.outfit_register_page.selected_extra = item_index

    def set_as_top(self, item_index):
        if item_index == None:
            self.outfit_register_page.top_piece_bar.piece_image.setText("No Top               ")
        else:
            self.outfit_register_page.top_piece_bar.piece_image.setPixmap(QPixmap(f"{closet[item_index].image_name}"))
        self.outfit_register_page.selected_top = item_index

    def set_as_bottom(self, item_index):
        if item_index == None:
            self.outfit_register_page.bottom_piece_bar.piece_image.setText("No Bottom               ")
        else:
            self.outfit_register_page.bottom_piece_bar.piece_image.setPixmap(QPixmap(f"{closet[item_index].image_name}"))
        self.outfit_register_page.selected_bottom = item_index

    def set_as_shoe(self, item_index):
        if item_index == None:
            self.outfit_register_page.shoe_piece_bar.piece_image.setText("No Shoe               ")
        else:
            self.outfit_register_page.shoe_piece_bar.piece_image.setPixmap(QPixmap(f"{closet[item_index].image_name}"))
        self.outfit_register_page.selected_shoe = item_index

    def register_outfit(self):

        name = self.outfit_register_page.name_input.text()
        if self.outfit_register_page.selected_extra == None:
            extra = None
        else:
            extra = closet[self.outfit_register_page.selected_extra]

        if self.outfit_register_page.selected_top == None:
            top = None
        else:
            top = closet[self.outfit_register_page.selected_top]

        if self.outfit_register_page.selected_bottom == None:
            bottom = None
        else:
            bottom = closet[self.outfit_register_page.selected_bottom]

        if self.outfit_register_page.selected_shoe == None:
            shoe = None
        else:
            shoe = closet[self.outfit_register_page.selected_shoe]

        tags = self.outfit_register_page.tag_input.toPlainText().split('\n') # this looks like "professional\ndark\n"
        tags = [tag.strip() for tag in tags if tag.strip()]

        input_outfit(outfits, name, extra, top, bottom, shoe, tags)
        # dont need to worry about any overlapping info, we will also not sort this in any way

        self.go_outfit_main_page()

    # OUTFIT EDIT PAGE FUNCTIONS
    def setup_outfit_edit_page(self, outfit_index):
        outfit = outfits[outfit_index]
        self.outfit_edit_page.outfit_index = outfit_index

        self.outfit_edit_page.name_input.setText(outfit.name)

        if outfits[outfit_index].extra == None:
            self.outfit_edit_page.extra_piece_bar.piece_image.setText("No Extra               ")
            self.outfit_edit_page.selected_extra = None
        else:
            self.outfit_edit_page.extra_piece_bar.piece_image.setPixmap(QPixmap(f"{outfits[outfit_index].extra.image_name}"))
            self.outfit_edit_page.selected_extra = closet.index(outfit.extra)

        if outfits[outfit_index].top == None:
            self.outfit_edit_page.top_piece_bar.piece_image.setText("No Top               ")
            self.outfit_edit_page.selected_top = None
        else:
            self.outfit_edit_page.top_piece_bar.piece_image.setPixmap(QPixmap(f"{outfits[outfit_index].top.image_name}"))
            self.outfit_edit_page.selected_top = closet.index(outfit.top)


        if outfits[outfit_index].bottom == None:
            self.outfit_edit_page.bottom_piece_bar.piece_image.setText("No Bottom               ")
            self.outfit_edit_page.selected_bottom = None
        else:
            self.outfit_edit_page.bottom_piece_bar.piece_image.setPixmap(QPixmap(f"{outfits[outfit_index].bottom.image_name}"))
            self.outfit_edit_page.selected_bottom = closet.index(outfit.bottom)

        if outfits[outfit_index].shoe == None:
            self.outfit_edit_page.shoe_piece_bar.piece_image.setText("No Shoes               ")
            self.outfit_edit_page.selected_shoe = None
        else:
            self.outfit_edit_page.shoe_piece_bar.piece_image.setPixmap(QPixmap(f"{outfits[outfit_index].shoe.image_name}"))
            self.outfit_edit_page.selected_shoe = closet.index(outfit.shoe)

        tag_input_text = ""
        for tag in outfit.tags:
            tag_input_text += f"{tag}\n"

        self.outfit_edit_page.tag_input.setPlainText(tag_input_text)

        self.go_outfit_edit_page()

    def generate_outfit_edit_selection_buttons(self):

        for i in reversed(range(self.outfit_edit_page.extra_piece_bar.piece_scroll_layout.count())):
            self.outfit_edit_page.extra_piece_bar.piece_scroll_layout.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.outfit_edit_page.top_piece_bar.piece_scroll_layout.count())):
            self.outfit_edit_page.top_piece_bar.piece_scroll_layout.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.outfit_edit_page.bottom_piece_bar.piece_scroll_layout.count())):
            self.outfit_edit_page.bottom_piece_bar.piece_scroll_layout.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.outfit_edit_page.shoe_piece_bar.piece_scroll_layout.count())):
            self.outfit_edit_page.shoe_piece_bar.piece_scroll_layout.itemAt(i).widget().setParent(None)

        blank_button = QPushButton("None")
        blank_button.setMinimumSize(170,190)
        blank_button.setMaximumSize(170,190)
        blank_button.clicked.connect(lambda state, item_index = None: self.edit_as_extra(item_index))
        self.outfit_edit_page.extra_piece_bar.piece_scroll_layout.addWidget(blank_button)

        blank_button = QPushButton("None")
        blank_button.setMinimumSize(170,190)
        blank_button.setMaximumSize(170,190)
        blank_button.clicked.connect(lambda state, item_index = None: self.edit_as_top(item_index))
        self.outfit_edit_page.top_piece_bar.piece_scroll_layout.addWidget(blank_button)

        blank_button = QPushButton("None")
        blank_button.setMinimumSize(170,190)
        blank_button.setMaximumSize(170,190)
        blank_button.clicked.connect(lambda state, item_index = None: self.edit_as_bottom(item_index))
        self.outfit_edit_page.bottom_piece_bar.piece_scroll_layout.addWidget(blank_button)

        blank_button = QPushButton("None")
        blank_button.setMinimumSize(170,190)
        blank_button.setMaximumSize(170,190)
        blank_button.clicked.connect(lambda state, item_index = None: self.edit_as_shoe(item_index))
        self.outfit_edit_page.shoe_piece_bar.piece_scroll_layout.addWidget(blank_button)



        # if clothing item has "top"
        for i, clothing in enumerate(closet):
            if clothing.contains("top"):
                newButton = self.clothing_button(i)
                newButton.clicked.connect(lambda state, item_index = i: self.edit_as_top(item_index))
                self.outfit_edit_page.top_piece_bar.piece_scroll_layout.addWidget(newButton)
        # else if clothing item has "bottom"
            elif clothing.contains("bottom"):
                newButton = self.clothing_button(i)
                newButton.clicked.connect(lambda state, item_index = i: self.edit_as_bottom(item_index))
                self.outfit_edit_page.bottom_piece_bar.piece_scroll_layout.addWidget(newButton)
            elif clothing.contains("shoe"):
        # else if clothing item has "shoe"
                newButton = self.clothing_button(i)
                newButton.clicked.connect(lambda state, item_index = i: self.edit_as_shoe(item_index))
                self.outfit_edit_page.shoe_piece_bar.piece_scroll_layout.addWidget(newButton)
            else:
                newButton = self.clothing_button(i)
                newButton.clicked.connect(lambda state, item_index = i: self.edit_as_extra(item_index))
                self.outfit_edit_page.extra_piece_bar.piece_scroll_layout.addWidget(newButton)

    def edit_as_extra(self, item_index):
        if item_index == None:
            self.outfit_edit_page.extra_piece_bar.piece_image.setText("No Extra               ")
        else:
            self.outfit_edit_page.extra_piece_bar.piece_image.setPixmap(QPixmap(f"{closet[item_index].image_name}"))
        self.outfit_edit_page.selected_extra = item_index

    def edit_as_top(self, item_index):
        if item_index == None:
            self.outfit_edit_page.top_piece_bar.piece_image.setText("No Top               ")
        else:
            self.outfit_edit_page.top_piece_bar.piece_image.setPixmap(QPixmap(f"{closet[item_index].image_name}"))
        self.outfit_edit_page.selected_top = item_index

    def edit_as_bottom(self, item_index):
        if item_index == None:
            self.outfit_edit_page.bottom_piece_bar.piece_image.setText("No Bottom               ")
        else:
            self.outfit_edit_page.bottom_piece_bar.piece_image.setPixmap(QPixmap(f"{closet[item_index].image_name}"))
        self.outfit_edit_page.selected_bottom = item_index

    def edit_as_shoe(self, item_index):
        if item_index == None:
            self.outfit_edit_page.shoe_piece_bar.piece_image.setText("No Shoe               ")
        else:
            self.outfit_edit_page.shoe_piece_bar.piece_image.setPixmap(QPixmap(f"{closet[item_index].image_name}"))
        self.outfit_edit_page.selected_shoe = item_index

    def edit_outfit(self):

        name = self.outfit_edit_page.name_input.text()
        if self.outfit_edit_page.selected_extra == None:
            extra = None
        else:
            extra = closet[self.outfit_edit_page.selected_extra]

        if self.outfit_edit_page.selected_top == None:
            top = None
        else:
            top = closet[self.outfit_edit_page.selected_top]

        if self.outfit_edit_page.selected_bottom == None:
            bottom = None
        else:
            bottom = closet[self.outfit_edit_page.selected_bottom]

        if self.outfit_edit_page.selected_shoe == None:
            shoe = None
        else:
            shoe = closet[self.outfit_edit_page.selected_shoe]

        tags = self.outfit_edit_page.tag_input.toPlainText().split('\n') # this looks like "professional\ndark\n"
        tags = [tag.strip() for tag in tags if tag.strip()]

        outfit_index = self.outfit_edit_page.outfit_index
        update_outfit(outfits, outfit_index, name, extra, top, bottom, shoe, tags)
        # dont need to worry about any overlapping info, we will also not sort this in any way

        self.go_outfit_main_page()

    def locate_outfit(self):
        outfit = outfits[self.outfit_edit_page.outfit_index]

        self.locate_outfit_item(outfit.extra)
        self.locate_outfit_item(outfit.top)
        self.locate_outfit_item(outfit.bottom)
        self.locate_outfit_item(outfit.shoe)

    def locate_outfit_item(self, item):

        clothing = item

        led_index = int(clothing.led_number)

        if clothing.led_on == True:
            self.pixels[led_index] = LED_Color.CLEAR
            clothing.led_on = False
        elif clothing.led_on == False:
            if clothing.contains("top"):
                self.pixels[led_index] = LED_Color.RED
                clothing.led_on = True
            elif clothing.contains("bottom"):
                self.pixels[led_index] = LED_Color.BLUE
            elif clothing.contains("shoe"):
                self.pixels[led_index] = LED_Color.GREEN
            else:
                self.pixels[led_index] = LED_Color.WHITE # 0xrrggbb
            clothing.led_on = True

        self.pixels.show()

    def delete_outfit(self):
        outfit_index = self.outfit_edit_page.outfit_index
        remove_outfit(outfits, outfit_index)

        self.go_outfit_main_page()

    # STACKED WIDGET TRAVERSAL FUNCTIONS
    def go_item_main_page(self):
        self.keyboard.KB_Off()
        self.generate_item_buttons()
        self.setCurrentIndex(Page.ITEM_MAIN)

    def go_item_register_page(self):
        self.keyboard.KB_Off()
        if(self.currentIndex() not in [Page.ITEM_REGISTER, Page.CAMERA]):
            self.reset_item_register_page()
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
        self.camera_page.new_image = False
        self.setCurrentIndex(Page.CAMERA)

    def go_outfit_main_page(self):
        self.keyboard.KB_Off()
        self.generate_outfit_buttons()
        self.setCurrentIndex(Page.OUTFIT_MAIN)

    def go_outfit_register_page(self):
        self.keyboard.KB_Off()
        self.generate_outfit_selection_buttons()
        self.setCurrentIndex(Page.OUTFIT_REGISTER)

    def go_outfit_edit_page(self):
        self.keyboard.KB_Off()
        self.generate_outfit_edit_selection_buttons()
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
        self.pixels.fill(LED_Color.CLEAR) # Turn off LEDs
        self.pixels.show()
        save_closet(closet, self.item_register_page.image_number, save_file)
        save_outfits(closet, outfits, save_file_2)

#ANDREW5 TODO debug button on outfit main if u need it
def debug_function():
    print_outfits(outfits)

if __name__ == "__main__":
    app = QApplication([])

    stacked_widget = Main_Stack()
    stacked_widget.item_register_page.image_number = load_closet(closet, save_file)
    load_outfits(closet, outfits, save_file_2)
    print_closet(closet)

    stacked_widget.go_item_main_page()

    stacked_widget.show()
    stacked_widget.showMaximized()


#    debug_button = QPushButton("DEBUG")
#    debug_button.clicked.connect(debug_function)
#    stacked_widget.outfit_main_page.layout.addWidget(debug_button)

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
