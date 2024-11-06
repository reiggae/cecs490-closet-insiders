# This Python file uses the following encoding: utf-8
import sys
import time
import board
import neopixel_spi as neopixel

from PySide6.QtWidgets import QApplication, QWidget, QPushButton

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

i = 0
col = [0x000000, 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFFFF, 0xFFFF00, 0xFF00FF, 0x00FFFF]

def LED_function():
    global i
    if i == 7:
        i = 0
    else:
        i += 1
    pixels[0] = col[i]
    pixels.show()
    print(i)


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        button = QPushButton("PB1", self)
        button.setGeometry(300,250,100,50)
        button.clicked.connect(LED_function)


if __name__ == "__main__":
    spi = board.SPI()
    pixels = neopixel.NeoPixel_SPI(spi, 60, pixel_order=neopixel.GRB, auto_write=False)
    pixels.fill(0x000000)
    pixels.show()
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
