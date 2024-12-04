from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *

from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2

from closet_inventory import *

closet = []

def debug_function():
    print_closet(closet)

def generate_item_buttons():
    for i in reversed(range(main_page.main_scroll_layout.count())):
        main_page.main_scroll_layout.itemAt(i).widget().setParent(None)

    for i in range(len(closet)):
        newButton = QPushButton()
        newButton.clicked.connect(lambda state, item = closet[i]: setup_edit_page(item))
        newButton.setStyleSheet("border-image : url({});".format(closet[i].image_name))
        newButton.setMinimumSize(100,100)
        newButton.setMaximumSize(100,100)
        main_page.main_scroll_layout.addWidget(newButton, i//3, i%3, alignment=Qt.AlignTop)

def setup_edit_page(item):
    print(item.ID)
    print(item.name)

def go_main_page():
    generate_item_buttons()
    stacked_widget.setCurrentIndex(0)

def go_register_page():
    stacked_widget.setCurrentIndex(1)

def go_camera_page():
    stacked_widget.setCurrentIndex(2)

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

        self.register_button = QPushButton("Register New Item")
        self.register_button.clicked.connect(go_register_page)

        # Initialize main page layout
        self.layout.addWidget(self.inventory_label, alignment = Qt.AlignTop|Qt.AlignCenter)
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.main_scroll)
        self.layout.addWidget(self.register_button)

        #DEBUG
        self.debug_button = QPushButton("DEBUG")
        self.debug_button.clicked.connect(debug_function)
        self.layout.addWidget(self.debug_button)




class register_page(QWidget):
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

        self.confirm_button = QPushButton("Confirm")
        self.exit_button = QPushButton("Exit")

        self.layout.addWidget(self.title, alignment = Qt.AlignTop|Qt.AlignCenter)
        self.layout.addWidget(self.id_input)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.image_preview, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.camera_button)
        self.layout.addWidget(self.tag_input)
        self.layout.addWidget(self.confirm_button)
        self.layout.addWidget(self.exit_button)

        self.camera_button.clicked.connect(go_camera_page)
        self.confirm_button.clicked.connect(self.register_clothing)
        self.exit_button.clicked.connect(go_main_page)

    def register_clothing(self):
        id = self.id_input.text()
        name = self.name_input.text()
        image = "test.jpg" #TODO, automatic image name scheme
        #tag = widget.ui.tagInput.plainText()

        closet.append(input_clothing(closet, id, name, image))

        #reset_register_page() #TODO
        go_main_page()


class camera_page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration())
        self.camera_button = QPushButton("Take Image")
        self.back_button = QPushButton("Go Back")
        self.back_button.clicked.connect(go_register_page)

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
        self.picam2.switch_mode_and_capture_file(self.cfg, "test.jpg", signal_function=self.qpicamera2.signal_done)

    def capture_done(self,job):
        self.result = self.picam2.wait(job)
        self.camera_button.setEnabled(True)
        register_page.image_preview.setPixmap(QPixmap('test.jpg'))
        go_register_page()

    def go_to_register_page(self):
        stacked_widget.setCurrentIndex(1)

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
    print("yo")




if __name__ == "__main__":
    app = QApplication([])

    # Initialize pages on stacked widget
    main_page = main_page()
    register_page = register_page()
    camera_page = camera_page()
    stacked_widget =  QStackedWidget()
    stacked_widget.addWidget(main_page)
    stacked_widget.addWidget(register_page)
    stacked_widget.addWidget(camera_page)

    ### RFID STUFF
    port = "/dev/ttyACM0"  # Hardcoded Arduino port
    rfid_reader = RFIDReader(port, 115200)
    rfid_reader.rfid_detected.connect(on_rfid_detected)
    rfid_reader.start()
    ### RFID STUFF

    stacked_widget.setGeometry(200, 0, 600, 500) #600, 1024)

    stacked_widget.setCurrentIndex(0)
    stacked_widget.setWindowTitle("Inside the Closet")
    stacked_widget.show()

    stacked_widget.showFullScreen()
    app.exec()
