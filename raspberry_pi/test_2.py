import serial
import time

SERIAL_PORT = '/dev/ttyACM0'  # Port Number for the Card Reader
BAUD_RATE = 115200

def main():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud")
            print("Waiting for Tag IDs... (Press Ctrl+C to exit)")

            while True:
                if ser.in_waiting > 0:
                    card_id = ser.readline().decode('ascii').strip()
                    if card_id:
                        print(f"Card ID received: {card_id}")
                time.sleep(0.1)  # Short delay to reduce CPU usage

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    except KeyboardInterrupt:
        print("\nExiting program.")

if __name__ == "__main__":
    main()
