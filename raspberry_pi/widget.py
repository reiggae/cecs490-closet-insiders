import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLineEdit
from PySide6.QtCore import QThread, Signal
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

class RFIDReader(QThread):
    rfid_detected = Signal(str)

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RFID Reader")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.input_line = QLineEdit()
        layout.addWidget(self.input_line)

        self.button = QPushButton("Send")
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        port = "/dev/ttyACM0"  # Hardcoded Arduino port
        self.rfid_reader = RFIDReader(port, 115200)
        self.rfid_reader.rfid_detected.connect(self.on_rfid_detected)
        self.rfid_reader.start()

    def on_rfid_detected(self, rfid_data):
        self.text_edit.append(f"RFID Detected: {rfid_data}")

    def on_button_click(self):
        text = self.input_line.text()
        self.text_edit.append(f"Button clicked: {text}")
        self.input_line.clear()

    def closeEvent(self, event):
        if hasattr(self, 'rfid_reader'):
            self.rfid_reader.stop()
            self.rfid_reader.wait()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
