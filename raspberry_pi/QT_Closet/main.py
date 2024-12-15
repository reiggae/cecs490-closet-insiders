# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *

from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2
from enum import IntEnum

from closet_inventory import *

class Page(IntEnum):
    MAIN = 0
    REGISTER = 1
    EDIT = 2
    CAMERA = 3
    OUTFIT_MAIN = 4
    OUTFIT_REGISTER = 5
    OUTFIT_EDIT = 6

closet = []

def debug_function():
    print_closet(closet)

def load_function():
    load_closet(closet, "MyCloset.txt")
    go_main_page()
    pass

def save_function():
    save_closet(closet, "MyCloset.txt")
    pass

def sort_closet(closet): #ANDREW2 TODO
    sort_by_color(closet)
    assign_led(closet)

class clothing_button(QPushButton):
    def __init__(self, closet_index, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())

        self.image = QLabel()
        self.image.setPixmap(QPixmap(f"{closet[closet_index].image_name}"))
        self.image.setScaledContents(True)
        self.image.setMaximumSize(150,150)

        self.label = QLabel(closet[closet_index].name)

        self.layout().addWidget(self.label,alignment=Qt.AlignTop|Qt.AlignCenter)
        self.layout().addWidget(self.image,alignment=Qt.AlignTop|Qt.AlignCenter)


        self.clicked.connect(lambda state, item_index = closet_index: setup_edit_page(item_index))
#        self.setStyleSheet("border-image : url({});".format(closet[closet_index].image_name))
        self.setMinimumSize(170,190)
        self.setMaximumSize(170,190)

def generate_item_buttons():
    value_count = 0
    # deletes existing item buttons
    for i in reversed(range(main_page.main_scroll_layout.count())):
        main_page.main_scroll_layout.itemAt(i).widget().setParent(None)

    search_term = main_page.search_bar.text()

    for i in range(len(closet)):
        if closet[i].contains(search_term):
            #ANDREW TODO does item match filter text? true:
            newButton = clothing_button(i)
            #ANDREW TODO replace "i" here with valid count or whatever
            main_page.main_scroll_layout.addWidget(newButton, value_count//3, value_count%3, alignment=Qt.AlignTop|Qt.AlignCenter)
            value_count += 1

    main_page.main_scroll.updateGeometry()


def generate_outfit_buttons():
    return
    # either top bottom shoe or something else
    item_type = "top"


    new_button = QPushButton("Hi")
    outfit_register_page.top_piece_bar.piece_scroll_layout.addWidget(new_button)

def setup_edit_page(item_index):
    item = closet[item_index]
    edit_page.closet_index = item_index

    edit_page.id_input.setText(item.ID)
    edit_page.name_input.setText(item.name)
    edit_page.image_preview.setPixmap(QPixmap(f"{item.image_name}"))
    edit_page.image_preview.setScaledContents(True)
    edit_page.image_preview.setMaximumSize(100,100)

    tag_input_text = ""
    for tag in item.details:
        tag_input_text += f"{tag}\n"

    edit_page.tag_input.setPlainText(tag_input_text)

    go_edit_page()

def go_main_page():
    generate_item_buttons()
    stacked_widget.setCurrentIndex(Page.MAIN)

def go_register_page():
    stacked_widget.setCurrentIndex(Page.REGISTER)

def go_edit_page():
    stacked_widget.setCurrentIndex(Page.EDIT)

def go_register_camera_page():
    camera_page.new_image = True
    stacked_widget.setCurrentIndex(Page.CAMERA)

def go_edit_camera_page():
    camera_page.new_image = False
    stacked_widget.setCurrentIndex(Page.CAMERA)

def go_outfit_main_page():
    stacked_widget.setCurrentIndex(Page.OUTFIT_MAIN)

def go_outfit_register_page():
    generate_outfit_buttons()
    stacked_widget.setCurrentIndex(Page.OUTFIT_REGISTER)

class main_page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Initialize main page widgets
        self.inventory_label = QLabel("INVENTORY")
        self.inventory_label.setFont(QFont("Sans Serif",32))

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Bar")

        self.search_button = QPushButton("Search")

        self.main_scroll = QScrollArea()
        self.scroll_area_contents = QWidget()
        self.main_scroll_layout = QGridLayout()
        self.main_scroll_layout.setSizeConstraint(QLayout.SetFixedSize)

        #TEMP
        row = 0
        col = 0
        for row in range(0,20):
            for col in range(0,3):
                object = QPushButton(str(row))
                object.setMinimumSize(170,170)
                object.setMaximumSize(170,170)
                self.main_scroll_layout.addWidget(object,row,col)

        self.scroll_area_contents.setLayout(self.main_scroll_layout)
        QScroller.grabGesture(self.main_scroll.viewport(), QScroller.LeftMouseButtonGesture)
        self.main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_scroll.setWidgetResizable(False)
        self.main_scroll.setWidget(self.scroll_area_contents)

        self.register_button = QPushButton("Register New Item")
        self.outfits_button = QPushButton("OUTFITS")

        # Initialize main page layout
        self.layout.addWidget(self.inventory_label, alignment = Qt.AlignTop|Qt.AlignCenter)
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.main_scroll)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.outfits_button)

        self.register_button.clicked.connect(go_register_page)
        self.search_button.clicked.connect(generate_item_buttons)
        self.outfits_button.clicked.connect(go_outfit_main_page)

        self.debug_button = QPushButton("DEBUG")
        self.debug_button.clicked.connect(debug_function)
        self.layout.addWidget(self.debug_button)

        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(load_function)
        self.layout.addWidget(self.load_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(save_function)
        self.layout.addWidget(self.save_button)

class register_page(QWidget):
    image_number = 0
    id_list = []
    def __init__(self, parent=None):
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
        self.image_preview.setPixmap(QPixmap('placeholder_shirt.png'))
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

        self.camera_button.clicked.connect(go_register_camera_page)
        self.confirm_button.clicked.connect(self.register_clothing)
        self.exit_button.clicked.connect(go_main_page)

    def register_clothing(self):
        id = self.id_input.text()
        name = self.name_input.text()
        tags = self.tag_input.toPlainText().split('\n') # this looks like "red\nshirt\n"
        tags = [tag.strip() for tag in tags if tag.strip()]

        # generate_image_name(), consider the count when loading??
        #ANDREW TODO if overlapping any
        if Clothing.check_existing_id(closet, id) == False:   # True flag is temp
            image = f"image_{register_page.image_number}.jpg" #ANDREW TODO, automatic image name scheme
            register_page.image_number += 1
            input_clothing(closet, id, name, image, tags) #ANDREW TODO input_clothing also takes tag string

            self.confirm_button.setText("Confirm")

            sort_closet(closet) #ANDREW2 TODO, sort by color and also assign led number
            reset_register_page()
            go_main_page()
        else:

            self.confirm_button.setText("Confirm (Error: ID already taken)")

def reset_register_page():
    register_page.id_input.setText("")
    register_page.name_input.setText("")
    register_page.image_preview.setPixmap(QPixmap('placeholder_shirt.png'))
    register_page.tag_input.setPlainText("")



class camera_page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.new_image = True

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration())
        self.camera_button = QPushButton("Take Image")
        self.back_button = QPushButton("Go Back")
        self.back_button.clicked.connect(self.go_previous_page)

        self.qpicamera2 = QGlPicamera2(self.picam2, keep_ar=False)
#        self.qpicamera2.setMaximumSize(500,500)

        self.layout.addWidget(self.qpicamera2)
        self.layout.addWidget(self.camera_button)
        self.layout.addWidget(self.back_button)

        self.picam2.start()

        self.camera_button.clicked.connect(self.take_photo)

        self.qpicamera2.done_signal.connect(self.capture_done)

    def take_photo(self):
#       qpicamera2.show()
        self.camera_button.setEnabled(False)
        self.cfg = self.picam2.create_still_configuration()

        if(self.new_image):
            self.picam2.switch_mode_and_capture_file(self.cfg, f"image_{register_page.image_number}.jpg", signal_function=self.qpicamera2.signal_done)
        else:
            self.picam2.switch_mode_and_capture_file(self.cfg, f"{closet[edit_page.closet_index].image_name}", signal_function=self.qpicamera2.signal_done)

    def capture_done(self,job):
        self.result = self.picam2.wait(job)
        self.camera_button.setEnabled(True)

        if(self.new_image):
            register_page.image_preview.setPixmap(QPixmap(f"image_{register_page.image_number}.jpg"))
            go_register_page()
        else:
            edit_page.image_preview.setPixmap(QPixmap(f"closet[edit_page.closet_index].image_name"))
            go_edit_page()

    def go_previous_page(self):
        if(self.new_image):
            go_register_page()
        else:
            go_edit_page()

class edit_page(QWidget):
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
        self.image_preview.setPixmap(QPixmap('placeholder_shirt.png'))
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


        self.camera_button.clicked.connect(go_edit_camera_page)
        self.confirm_button.clicked.connect(self.edit_clothing)
        self.exit_button.clicked.connect(go_main_page)

    def edit_clothing(self):
        id = self.id_input.text()
        name = self.name_input.text()
        tags = self.tag_input.toPlainText().split('\n') # this looks like "red\nshirt\n"
        tags = [tag.strip() for tag in tags if tag.strip()]
        # generate_image_name(), consider the count when loading??
        #ANDREW TODO if overlapping any
        image = f"image_{register_page.image_number}.jpg" #ANDREW TODO, automatic image name scheme

        update_clothes(closet, id, name, image, tags) #ANDREW TODO input_clothing also takes tag string

        self.confirm_button.setText("Confirm")

        sort_closet(closet) #ANDREW2 TODO, sort by color and also assign led number
        reset_register_page()
        go_main_page()

class outfit_main_page(QWidget):
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

        #TEMP
        row = 0
        col = 0
        for row in range(0,20):
            for col in range(0,3):
                object = QPushButton(str(row))
                object.setMinimumSize(100,100)
                object.setMaximumSize(100,100)
                self.main_scroll_layout.addWidget(object,row,col)

        self.scroll_area_contents.setLayout(self.main_scroll_layout)
        QScroller.grabGesture(self.main_scroll.viewport(), QScroller.LeftMouseButtonGesture)
        self.main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_scroll.setWidgetResizable(False)
        self.main_scroll.setWidget(self.scroll_area_contents)

        self.register_button = QPushButton("Register New Outfit")
        self.clothes_button = QPushButton("CLOTHES")

        # Initialize main page layout
        self.layout.addWidget(self.inventory_label, alignment = Qt.AlignTop|Qt.AlignCenter)
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.main_scroll)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.clothes_button)

        self.register_button.clicked.connect(go_outfit_register_page)
        self.search_button.clicked.connect(generate_outfit_buttons)
        self.clothes_button.clicked.connect(go_main_page)

class outfit_register_page(QWidget):
    class clothing_piece_bar(QWidget):
        def __init__(self, piece_name, parent=None):
            super().__init__(parent)

            self.piece_scroll = QScrollArea()
            self.piece_scroll_area_contents = QWidget()
            self.piece_scroll_layout = QHBoxLayout()

            #TEMP
#            for i in range(0,20):
#                object = QPushButton(str(i))
#                object.setMinimumSize(100,100)
#                object.setMaximumSize(100,100)
#                self.piece_scroll_layout.addWidget(object)

            self.piece_scroll_area_contents.setLayout(self.piece_scroll_layout)
            QScroller.grabGesture(self.piece_scroll.viewport(), QScroller.LeftMouseButtonGesture)
            self.piece_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.piece_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.piece_scroll.setWidgetResizable(False)
            self.piece_scroll.setWidget(self.piece_scroll_area_contents)
            self.piece_scroll.setMinimumHeight(140)

            self.piece_image = QPushButton(piece_name)
            self.setLayout(QHBoxLayout())
            self.layout().addWidget(self.piece_image)
            self.layout().addWidget(self.piece_scroll)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("NEW OUTFIT DETAILS")
        self.title.setFont(QFont("Sans Serif",32))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        self.top_piece_bar = self.clothing_piece_bar("top")
        new_button = QPushButton("Hi")
        self.top_piece_bar.piece_scroll_layout.addWidget(new_button)

#        new_button2 = QPushButton("Hi2")
#        self.top_piece_bar.piece_scroll.addWidget(new_button2)

        self.bottom_piece_bar = self.clothing_piece_bar("bottom")
        self.shoe_piece_bar = self.clothing_piece_bar("shoe")

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

        self.confirm_button.clicked.connect(self.register_clothing)
        self.exit_button.clicked.connect(go_main_page)

    def register_clothing(self):
        id = self.id_input.text()
        name = self.name_input.text()
        tags = self.tag_input.toPlainText().split('\n') # this looks like "red\nshirt\n"
        tags = [tag.strip() for tag in tags if tag.strip()]

        # generate_image_name(), consider the count when loading??
        #ANDREW TODO if overlapping any
        if id not in register_page.id_list:   # True flag is temp
            register_page.id_list.append(id)
            image = f"image_{register_page.image_number}.jpg" #ANDREW TODO, automatic image name scheme
            register_page.image_number += 1
            closet.append(input_clothing(closet, id, name, image, tags)) #ANDREW TODO input_clothing also takes tag string

            self.confirm_button.setText("Confirm")

            sort_closet(closet) #ANDREW2 TODO, sort by color and also assign led number
            reset_register_page()
            go_main_page()
        else:

            self.confirm_button.setText("Confirm (Error: ID already taken)")



class RFIDReader(QThread):
    rfid_detected = pyqtSignal(str)

    def __init__(self, port, baud_rate):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.serial_port = QSerialPort()
        self.running = False

    def run(self):
        self.serial_port.setPortName(self.port)
        self.serial_port.setBaudRate(self.baud_rate)
        if self.serial_port.open(QSerialPort.ReadOnly):
            self.serial_port.setDataTerminalReady(True)  # Set DTR
            print(f"Successfully opened port {self.port}")
            self.running = True
            while self.running:
                if self.serial_port.waitForReadyRead(100):
                    data = self.serial_port.readAll()
                    rfid_data = data.data().decode().strip()
                    print(f"Raw data received: {rfid_data}")
                    if rfid_data:
                        self.rfid_detected.emit(rfid_data)
        else:
            print(f"Failed to open port {self.port}. Error: {self.serial_port.error()}")

    def stop(self):
        self.running = False
        if self.serial_port.isOpen():
            self.serial_port.close()

def on_rfid_detected(rfid_data):
    print(rfid_data)

    curr_index = stacked_widget.currentIndex()
    if  curr_index == Page.MAIN or curr_index == Page.REGISTER:
        register_page.id_input.setText(rfid_data)
        go_register_page()


if __name__ == "__main__":
    app = QApplication([])

    # Initialize pages on stacked widget
    main_page = main_page()
    register_page = register_page()
    camera_page = camera_page()
    edit_page = edit_page()
    outfit_main_page = outfit_main_page()
    outfit_register_page = outfit_register_page()

    stacked_widget =  QStackedWidget()
    stacked_widget.addWidget(main_page)
    stacked_widget.addWidget(register_page)
    stacked_widget.addWidget(edit_page)
    stacked_widget.addWidget(camera_page)
    stacked_widget.addWidget(outfit_main_page)             #matches main_page
    stacked_widget.addWidget(outfit_register_page)
    #stacked_widget.addWidget(outfit_edit_page)

    ### RFID STUFF
    port = "/dev/ttyACM0"  # Hardcoded Arduino port
    rfid_reader = RFIDReader(port, 115200)
    rfid_reader.rfid_detected.connect(on_rfid_detected)
    rfid_reader.start()
    ### RFID STUFF

    stacked_widget.setGeometry(200, 0, 600, 500) #600, 1024)

    stacked_widget.setCurrentIndex(Page.MAIN) #TODO replace to go_main_page when done
    stacked_widget.setWindowTitle("Inside the Closet")
    stacked_widget.show()

    stacked_widget.showFullScreen()
    app.exec()
