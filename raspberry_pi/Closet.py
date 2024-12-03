import serial
from closet_inventory import input_clothing
from closet_inventory import remove_clothes
from closet_inventory import print_closet
from closet_inventory import update_clothes
from closet_inventory import search_clothes
from closet_inventory import switch_ids
from closet_inventory import save_closet
from closet_inventory import load_closet
from closet_inventory import sort_by_color
from closet_inventory import checking_system
from closet_inventory import take_a_picture
from closet_inventory import create_outfit
from closet_inventory import add_clothing_to_outfit
from closet_inventory import print_outfits
from closet_inventory import hanger_system
from closet_inventory import map_clothes_to_leds
from read_card_id import read_card_id


def main():
    SERIAL_PORT = '/dev/ttyACM0'
    BAUD_RATE = 115200
    ser = None
    i = 1

    closet = []
    outfits = []
    clothing_types = ["Top", "Middle", "Bottom"]
    
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
        print("12. Take a picture of a clothing")
        print("13. Add an outfit")
        print("14. Add clothing items to an outfit")
        print("15. Print all outfits")
        print("16. Add clothing to a hanger")
        print("17. Take out clothing from a hanger")
        print("18. Assign hangers to LEDs")
        print("19. Exit")
        command = input("Select options from 1 to 19: ")
        
        if command == "done":
            break
        elif command == "1":
            closet.append(input_clothing(closet, i))
            i += 1
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
            save_closet(closet, outfits, filename)
        elif command == "8":
            filename = input("Enter file name to load from: ")
            load_closet(closet, outfits, filename)
        elif command == "9":
            sort_by_color(closet)
        elif command == "10":
            checking_system(closet, True)
        elif command == "11":
            checking_system(closet, False)
        elif command == "12":
            take_a_picture(closet)
        elif command == "13":
            outfit_name = input("Enter the name of the new outfit: ")
            create_outfit(outfits, outfit_name)
        elif command == "14":
            if not outfits:
                print("No outfits registered yet. Please create an outfit first.")
            else:
                print("Registered outfits: ")
                for index, outfit in enumerate(outfits, 1):
                    print(f"{index}. {outfit.outfit_name}")
            outfit_name = input("Choose which outfit to add clothes too: ")
            if ser:
                print("Please scan the clothing tag or enter the ID manually:")
                chosen_id = read_card_id(ser)
                if not chosen_id:
                    chosen_id = input("Enter the Clothing ID that you want to add: ")
            else:
                chosen_id = input("Enter the Clothing ID that you want to add: ")
            clothing_type = input("Enter the type of clothing (Top, Middle, Bottom): ")
            clothing_item = next((c for c in closet if c.ID == chosen_id), None)
            if clothing_item:
                if any(x in clothing_type for x in clothing_types):
                    add_clothing_to_outfit(outfits, outfit_name, clothing_type, clothing_item)
                else:
                    print("Invalid clothing type")
            else:
                print(f"No clothing item found with ID {chosen_id}")
        elif command == "15":
            print_outfits(outfits)
        elif command == "16":
            hanger_system(closet, True)
        elif command == "17":
            hanger_system(closet, False)
        elif command == "18":
            hanger_count = 0
            for clothing in closet:
                if clothing.has_hanger == True:
                    hanger_count += 1
            led_count = int(input("How many LEDs are available? "))
            map_clothes_to_leds(hanger_count, led_count)        
        elif command == "19":
            break
        else:
            print("Invalid command. Select a valid number.")

    if ser:
        ser.close()
    print("\nExiting program.")

if __name__ == "__main__":
    main()