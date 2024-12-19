from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *

from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2

class Camera_Page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.new_image = True

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration())
        self.camera_button = QPushButton("Take Image")
        self.back_button = QPushButton("Go Back")


        self.qpicamera2 = QGlPicamera2(self.picam2, keep_ar=False)
#        self.qpicamera2.setMaximumSize(500,500)

        self.layout.addWidget(self.qpicamera2)
        self.layout.addWidget(self.camera_button)
        self.layout.addWidget(self.back_button)

        self.picam2.start()

#        self.camera_button.clicked.connect(self.take_photo)
#        self.back_button.clicked.connect(self.go_previous_page)
#        self.qpicamera2.done_signal.connect(self.capture_done)


