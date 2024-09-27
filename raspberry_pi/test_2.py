#This is just to have the raspberry pi recieve the Tag IDs.
import serial

# Adjust the port and baud rate as necessary
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

print("Waiting for Tag IDs...")

while True:  # Infinite loop to continuously check for incoming data
    if ser.in_waiting > 0:  # Check if there's any data 
        # Read a line from the serial port, decode it from bytes to ASCII string,
        # and remove any leading/trailing whitespace but if you want the whitespaces remove ".strip()
        card_id = ser.readline().decode('ascii').strip()
        
        if card_id:  # Check if card_id is not empty
            # If a non-empty card ID was received, print it
            print(f"Card ID received: {card_id}")
