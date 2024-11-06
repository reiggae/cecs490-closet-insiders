# This Python file uses the following encoding: utf-8
import sys
import time
import board
import neopixel_spi as neopixel

from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtGui import QPalette, QColor

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

i = 0
col = [0x000000, 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFFFF, 0xFFFF00, 0xFF00FF, 0x00FFFF]

def RedFun():
    pixels[0] = 0xFF0000
    pixels.show()
    print("Red")

def GreenFun():
    pixels[0] = 0x00FF00
    pixels.show()
    print("Green")

def BlueFun():
    pixels[0] = 0x0000FF
    pixels.show()
    print("Blue")

def WhiteFun():
    pixels[0] = 0xFFFFFF
    pixels.show()
    print("White")

def YellowFun():
    pixels[0] = 0xFFFF00
    pixels.show()
    print("Yellow")

def MagentaFun():
    pixels[0] = 0xFF00FF
    pixels.show()
    print("Magenta")

def CyanFun():
    pixels[0] = 0x00FFFF
    pixels.show()
    print("Cyan")

def ClearFun():
    pixels[0] = 0x000000
    pixels.show()
    print("Clear")


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        Redbutton = QPushButton("Red", self)
        Redbutton.setGeometry(50,50,100,50)
        palette = Redbutton.palette()
        palette.setColor(QPalette.Button, QColor(255,0,0))
        Redbutton.setPalette(palette)
        Redbutton.clicked.connect(RedFun)

        Greenbutton = QPushButton("Green", self)
        Greenbutton.setGeometry(200,50,100,50)
        palette = Greenbutton.palette()
        palette.setColor(QPalette.Button, QColor(0,255,0))
        Greenbutton.setPalette(palette)
        Greenbutton.clicked.connect(GreenFun)

        Bluebutton = QPushButton("Blue", self)
        Bluebutton.setGeometry(350,50,100,50)
        palette = Bluebutton.palette()
        palette.setColor(QPalette.Button, QColor(0,0,255))
        Bluebutton.setPalette(palette)
        Bluebutton.clicked.connect(BlueFun)

        Whitebutton = QPushButton("White", self)
        Whitebutton.setGeometry(500,50,100,50)
        palette = Whitebutton.palette()
        palette.setColor(QPalette.Button, QColor(255,255,255))
        Whitebutton.setPalette(palette)
        Whitebutton.clicked.connect(WhiteFun)

        Yellowbutton = QPushButton("Yellow", self)
        Yellowbutton.setGeometry(50,150,100,50)
        palette = Yellowbutton.palette()
        palette.setColor(QPalette.Button, QColor(255,255,0))
        Yellowbutton.setPalette(palette)
        Yellowbutton.clicked.connect(YellowFun)

        Magentabutton = QPushButton("Magenta", self)
        Magentabutton.setGeometry(200,150,100,50)
        palette = Magentabutton.palette()
        palette.setColor(QPalette.Button, QColor(255,0,255))
        Magentabutton.setPalette(palette)
        Magentabutton.clicked.connect(MagentaFun)

        Cyanbutton = QPushButton("Cyan", self)
        Cyanbutton.setGeometry(350,150,100,50)
        palette = Cyanbutton.palette()
        palette.setColor(QPalette.Button, QColor(0,255,255))
        Cyanbutton.setPalette(palette)
        Cyanbutton.clicked.connect(CyanFun)

        Clearbutton = QPushButton("Clear", self)
        Clearbutton.setGeometry(500,150,100,50)
        Clearbutton.clicked.connect(ClearFun)


if __name__ == "__main__":
    spi = board.SPI()
    pixels = neopixel.NeoPixel_SPI(spi, 60, pixel_order=neopixel.GRB, auto_write=False)
    pixels.fill(0x000000)
    pixels.show()
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
