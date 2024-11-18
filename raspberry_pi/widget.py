# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QPushButton
import os
import serial

import capture_and_process_image
import closet_inventory
import read_card_id
#import Rescale

from picamera2 import Picamera2, Preview

from ui_form import Ui_Widget

closet = []

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

def go_main_page():
    # TODO: better way of assigning buttons
    for i in range(len(closet)):
        temp = widget.ui.scrollAreaWidgetContents.findChild(QPushButton, "pushButton_{}".format(i+1))
        temp.setText(closet[0].name)
        temp.clicked.connect(go_edit_page) # TODO: find way to differentiate when 2 buttons

    widget.ui.stackedWidget.setCurrentIndex(0)

def go_register_page():
    widget.ui.stackedWidget.setCurrentIndex(1)

def go_edit_page():
    widget.ui.stackedWidget.setCurrentIndex(2)

def reset_register_page():
    widget.ui.idInput.setText("bleh")
    widget.ui.nameInput.setText("bleh")
    widget.ui.imageInput.setText("bleh")
    #widget.ui.tagInput.setText("bleh")

def confirm_register():
    # TODO: multiprocessing can read RFID and replace ID input automatically
    # read all inputs
    id = widget.ui.idInput.text()
    name = widget.ui.nameInput.text()
    image = widget.ui.imageInput.text()
    #tag = widget.ui.tagInput.plainText()

    # TODO: run input_clothing function
    closet.append(input_clothing(closet, id, name))
    # ANDREWTODO: add image name to input_clothing
    # TODO: automatically assign position to item, returning to main page generates proper image in location

    # reset page after returning to main page
    reset_register_page()
    go_main_page()

def button_search_function():
    text_input = widget.ui.textBox.text()
    print(text_input)
    widget.ui.pushButton_1.setStyleSheet("border-image : url({});".format(text_input))

def debug_function():
    print_closet(closet)

def debug_image():
#    picam2 = Picamera2()
#    while True:
#        if capture_and_process_image(picam2, "image_1"):
#            break
#    picam2.stop()
    pass




# TODO: figure out how to add infinito clothing buttons with their own function... or index parameter might be easier
# can prob use universal function and look at ID to recognize, but need to first correlate buttons to clothes

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()

    widget.ui.newItemButton.clicked.connect(go_register_page)
    widget.ui.goBackButton.clicked.connect(go_main_page)
    widget.ui.confirmRegisterButton.clicked.connect(confirm_register)
    widget.ui.debugPrintButton.clicked.connect(debug_function)
    widget.ui.debugImageButton.clicked.connect(debug_image)



    go_main_page()
    widget.show()


    # press add clothes
    # set flag for "adding clothes"
    # wait for rfid (button 2) or manual id input (button 3)
    # buttons do nothing if "adding clothes" is not true
    # if true run some other function and flag? dont forget reset flag
    # user does textbox inputs
    #


    sys.exit(app.exec())
