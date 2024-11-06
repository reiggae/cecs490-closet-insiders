from closet_inventory import Clothing
import serial

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
        print("10. Check in/out clothing")
        print("11. Check to see which clothes are checked in/out")
        print("12. Exit")
        command = input("Select options from 1 to 12: ")
        
        if command == "done":
            break
        elif command == "1":
            closet.append(input_clothing(closet,ser))
        elif command == "2":
            remove_clothes(closet, ser)    
        elif command == "3":
            print_closet(closet)
        elif command == "4":
            update_clothes(closet, ser)    
        elif command == "5":
            search_clothes(closet)
        elif command == "6":
            switch_ids(closet, ser)
        elif command == "7":
            filename = input("Enter file name to save to: ")
            save_closet(closet, filename)
        elif command == "8":
            filename = input("Enter file name to load from: ")
            load_closet(closet, filename)
        elif command == "9":
            sort_by_color(closet)
            print_closet(closet)
            print("Closet sorted by color.")
        elif command == "10":
            while True:
                choice = input("Do you want to check 'in' or 'out'? ")
                if choice == "in":
                    checking_system(closet, True, ser)
                    break
                elif choice == "out":
                    checking_system(closet, False, ser)
                    break
                else:
                    print("Invalid selection. Please try again.")
        elif command == "11":
            while True:
                choice = input("Do you want to see checked 'in' or 'out' items? ")
                if choice == "in":
                    check_items(closet, True)
                    break
                elif choice == "out":
                    check_items(closet, False)
                    break
                else:
                    print("Invalid selection. Please try again.") 
        elif command == "12":
            break
        else:
            print("Invalid command. Select a valid number.")

    if ser:
        ser.close()
    print("\nExiting program.")

if __name__ == "__main__":
    main()
