from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *

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
