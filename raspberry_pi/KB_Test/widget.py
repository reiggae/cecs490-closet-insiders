# This Python file uses the following encoding: utf-8
import sys
import subprocess

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QEvent, Qt

# Import the generated UI file
from ui_form import Ui_Widget

KB_Active = False

def KB_On():
    global KB_Active
    KB_Active = True
    subprocess.Popen(["bash", "KB_Start.sh"])

def KB_Off():
    global KB_Active
    KB_Active = False
    subprocess.Popen(["bash", "KB_Off.sh"])

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # Install event filter on lineEdit
        self.ui.lineEdit.installEventFilter(self)

    def eventFilter(self, obj, event):
        global KB_Active
        #Check for events on lineEdit
        if obj == self.ui.lineEdit:
            #Turns on KB
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton and KB_Active == False:
                KB_On()
                return True
            #Turns off KB
            elif event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton and KB_Active == True:
                KB_Off()
                return True

        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.ui.kill.clicked.connect(KB_Off)
    widget.show()
    sys.exit(app.exec())
