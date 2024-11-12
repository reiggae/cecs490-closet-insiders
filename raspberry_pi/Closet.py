import os
import serial
from raspberry_pi.closet_inventory import Clothing
from raspberry_pi.closet_inventory import input_clothing
from raspberry_pi.closet_inventory import remove_clothes
from raspberry_pi.closet_inventory import print_closet
from raspberry_pi.closet_inventory import update_clothes
from raspberry_pi.closet_inventory import search_clothes
from raspberry_pi.closet_inventory import switch_ids
from raspberry_pi.closet_inventory import save_closet
from raspberry_pi.closet_inventory import load_closet
from raspberry_pi.closet_inventory import sort_by_color
from raspberry_pi.closet_inventory import checking_system


def main():
    SERIAL_PORT = '/dev/ttyACM0'
    BAUD_RATE = 115200
    ser = None

    closet = []
    
    print("Welcome to the Closet Manager")

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to card reader on {SERIAL_PORT} at {BAUD_RATE} baud")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        print("Continuing without card reader...")

    while True:
        print("Please choose an option")
        print("1. Add clothing")
        print("2. Remove clothing")
        print("3. View current closet")
        print("4. Update current clothing")
        print("5. Search for specific clothing")
        print("6. Swap clothing")
        print("7. Save closet information to a text file")
        print("8. Load closet information from a text file")
        print("9. Sort closet by color")
        print("10. Check in clothing")
        print("11. Check out clothing")
        print("12. Exit")
        command = input("Select options from 1 to 12: ")
        
        if command == "done":
            break
        elif command == "1":
            closet.append(input_clothing(closet))
        elif command == "2":
            remove_clothes(closet)    
        elif command == "3":
            print_closet(closet)
        elif command == "4":
            update_clothes(closet)    
        elif command == "5":
            search_clothes(closet)
        elif command == "6":
            switch_ids(closet)
        elif command == "7":
            filename = input("Enter file name to save to: ")
            save_closet(closet, filename)
        elif command == "8":
            filename = input("Enter file name to load from: ")
            load_closet(closet, filename)
        elif command == "9":
            sort_by_color(closet)
        elif command == "10":
            checking_system(closet, True)
        elif command == "11":
            checking_system(closet, False)
        elif command == "12":
            break
        else:
            print("Invalid command. Select a valid number.")

    if ser:
        ser.close()
    print("\nExiting program.")

if __name__ == "__main__":
    main()