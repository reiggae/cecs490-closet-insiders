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
from outfits import create_outfit
from outfits import add_clothing_to_outfit
from outfits import print_outfits


def main():
    i = 1

    closet = []
    outfits = []
    
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
        print("12. Take a picture of a clothing")
        print("13. Add an outfit")
        print("14. Add clothing items to an outfit")
        print("15. Print all outfits")
        print("16. Exit")
        command = input("Select options from 1 to 16: ")
        
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
            print("Camera not available")
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
            chosen_id = input("Enter the Clothing ID that you want to add: ")
            clothing_type = input("Enter the type of clothing (Shirt, Pants, etc.): ")
            clothing_item = next((c for c in closet if c.ID == chosen_id), None)
            if clothing_item:
                add_clothing_to_outfit(outfits, outfit_name, clothing_type, clothing_item)
            else:
                print(f"No clothing item found with ID {chosen_id}")
        elif command == "15":
            print_outfits(outfits)
        elif command == "16":
            break
        else:
            print("Invalid command. Select a valid number.")
    print("\nExiting program.")

if __name__ == "__main__":
    main()