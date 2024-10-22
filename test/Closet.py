from input_clothing import input_clothing
from remove_clothes import remove_clothes
from print_closet import print_closet
from update_clothes import update_clothes
from search_clothes import search_clothes
from switch_ids import switch_ids
from save_closet import save_closet
from load_closet import load_closet
from sort_by_color import sort_by_color
from checking_system import checking_system

def main():
    # Create a list to store the Clothings
    closet = []
    
    print("Welcome to the Closet Manager")

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

if __name__ == "__main__":
    main()
