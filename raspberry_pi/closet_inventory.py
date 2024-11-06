from picamera2 import Picamera2, Preview
from capture_and_process_image import capture_and_process_image
from read_card_id import read_card_id
import os

color_order = {"Red": 1, "Orange": 2, "Yellow": 3, "Green": 4, "Blue": 5, "Purple": 6, "Black": 7, "White": 8, "Gray": 9, "Brown": 10}
# Define a class to hold the clothing details
class Clothing:
    def __init__(self):
        self.name = ""
        self.ID = ""
        self.details = []
        self.is_checked_in = False
	    
    # Function to print clothing details
    def print(self):
        print(f"Position Number: {self.position_number}")
        print(f"Clothing ID: {self.ID}")
        print(f"Clothing Name: {self.name}")
        print("Tags:")
        for detail in self.details:
            print(f"- {detail}")
        print(f"Status: {'checked in' if self.is_checked_in else 'checked out'}")
        print()

    # Function to check if any detail contains the search term
    def contains(self, term):
        if term in self.name:
            return True
        for detail in self.details:
            if term in detail:
                return True
        return False
        
def input_clothing(closet, ser=None):
    clothing = Clothing()
    ID_array = [clothes.ID for clothes in closet]
    
    while True:
        if ser:
            print("Please scan the clothing tag or enter the ID manually:")
            card_id = read_card_id(ser)
            if card_id:
                clothing.ID = card_id
                print(f"Clothing ID scanned: {clothing.ID}")
            else:
                clothing.ID = input("Enter Clothing ID manually: ")
        else:
            clothing.ID = input("Enter Clothing ID: ")
                
        if clothing.ID in ID_array:
            print("Tag is already registered. Use another tag. ")
        else:
            ID_array.append(clothing.ID)
            break
    
        
    clothing.name = input("Enter Clothing Name(add .png if you want to take a picture: ")
    if not clothing.name.endswith(".png"):
        print("Skipping image capture.")
    else:
        picam2 = Picamera2()
        # Loop until the user is happy with the image
        while True:
            # Capture and process the image
            if capture_and_process_image(picam2, clothing.name):
                break  # Exit loop if the user is happy

        # Properly stop and release the camera at the end
        picam2.stop()
    
    while True:
        detail = input("Enter Detail (or type 'done' to finish): ")
        if detail == "done":
            break
        clothing.details.append(detail)

    return clothing
    
def remove_clothes(closet, ser=None):
    if ser:
        print("Please scan the clothing tag or enter the ID manually:")
        chosen_id = read_card_id(ser)
        if not chosen_id:
            chosen_id = input("Enter the Clothing ID that you want to remove: ")
    else:
        chosen_id = input("Enter the Clothing ID that you want to remove: ")
    
    for i, clothing in enumerate(closet):
        if clothing.ID == chosen_id:
            del closet[i]
            print("Clothing removed successfully.")
            return
    print(f"There are no Clothings with the ID of {chosen_id}")
    
def print_closet(closet):
    rack = []
    print("Closet contents:")
    for i, clothing in enumerate(closet):
        rack.append(i)
        print(f"Clothing {i + 1}:")
        clothing.print()
    print(f"Rack List: {rack}")
# Function to update clothing
def update_clothes(closet, ser=None):
    if ser:
        print("Please scan the clothing tag or enter the ID manually:")
        chosen_id = read_card_id(ser)
        if not chosen_id:
            chosen_id = input("Enter the clothing ID that you want to update: ")
    else:
        chosen_id = input("Enter the clothing ID that you want to update: ")

    for clothing in closet:
        if clothing.ID == chosen_id:
            print("Clothing ID found")
            while True:
                clothing.print()
                choice = input("Do you want to 'add' or 'remove' details (Type 'exit' to exit)? ")
                
                if choice == "add":
                    while True:
                        detail_add = input("Enter detail (or type 'done' to finish): ")
                        if detail_add == "done":
                            break
                        clothing.details.append(detail_add)
                
                elif choice == "remove":
                    while True:
                        detail_remove = input("Enter existing detail to remove (or type 'done' to finish): ")
                        if detail_remove == "done":
                            break
                        if detail_remove in clothing.details:
                            clothing.details.remove(detail_remove)
                            print("Detail removed successfully.")
                        else:
                            print("Detail not found.")
                
                elif choice == "exit":
                    break
                
                else:
                    print("Invalid choice. Please type 'add' or 'remove'.")
            return
    print("Clothing ID not found.")
# Search Function
def search_clothes(closet):
    search_term = input("Enter a detail to search for: ")
    print(f"Current Filters: {search_term}")
    
    found = False
    for clothing in closet:
        if clothing.contains(search_term):
            clothing.print()
            found = True

    if not found:
        print(f"No clothings found with the detail: {search_term}")

def switch_ids(closet, ser=None):
    if ser:
        print("Please scan the first clothing tag or enter the ID manually:")
        id1 = read_card_id(ser)
        if not id1:
            id1 = input("Enter the first Clothing ID: ")
        
        print("Please scan the second clothing tag or enter the ID manually:")
        id2 = read_card_id(ser)
        if not id2:
            id2 = input("Enter the second Clothing ID: ")
    else:
        id1 = input("Enter the first Clothing ID: ")
        id2 = input("Enter the second Clothing ID: ")

    clothes1 = None
    clothes2 = None

    for clothing in closet:
        if clothing.ID == id1:
            clothes1 = clothing
        elif clothing.ID == id2:
            clothes2 = clothing

        if clothes1 and clothes2:
            break
    
    if clothes1 and clothes2:
        clothes1.ID, clothes2.ID = clothes2.ID, clothes1.ID
        clothes1.name, clothes2.name = clothes2.name, clothes1.name
        clothes1.details, clothes2.details = clothes2.details, clothes1.details
        print("The IDs have been swapped")
    else:
        print("One or both Clothing IDs are invalid.")
# Function to save the closet to a file
def save_closet(closet, filename):
    with open(filename, 'w') as out_file:
        for clothes in closet:
            out_file.write(f"Clothing ID: {clothes.ID}\n")
            out_file.write(f"Clothing Name: {clothes.name}\n")
            for detail in clothes.details:
                out_file.write(f"- {detail}\n")
    print(f"Closet saved to {filename}")
# Function to load the closet from a file
def load_closet(closet, filename):
    if not os.path.isfile(filename):
        print("Error opening file for loading!")
        return

    closet.clear()
    clothes = Clothing()

    with open(filename, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if "Clothing ID:" in line:
                if clothes.name:
                    closet.append(clothes)
                clothes = Clothing()
                clothes.ID = line.split(": ")[1]
            elif "Clothing Name:" in line:
                clothes.name = line.split(": ")[1]
            elif line.startswith("- "):
                clothes.details.append(line[2:])

    if clothes.name:
        closet.append(clothes)

    print(f"Closet loaded from {filename}")

def get_color_from_detail(details):
    for detail in details:
        for color in color_order:
            if color.lower() in detail.lower():
                return color
    return None

def sort_by_color(closet):
    colored_clothes = []
    uncolored_clothes = []

    for clothing in closet:
        color = get_color_from_detail(clothing.details)
        if color:
            colored_clothes.append((color, clothing))
        else:
            uncolored_clothes.append(clothing)
    colored_clothes.sort(key=lambda x: color_order[x[0]])
    
    closet[:] = [clothing for _, clothing in colored_clothes] + uncolored_clothes

def checking_system(closet, status, ser = None):
    if ser:
        print(f"Enter the Clothing ID that you want to {'check in' if status else 'check out'}: ")
        chosen_id = read_card_id(ser)
        if not chosen_id:
            chosen_id = input(f"Enter the Clothing ID that you want to {'check in' if status else 'check out'}: ")
    else:
        chosen_id = input(f"Enter the Clothing ID that you want to {'check in' if status else 'check out'}: ")

    for clothing in closet:
        if clothing.ID == chosen_id:
            clothing.is_checked_in = status
            print(f"Clothing ID: {chosen_id} has been {'checked in' if status else 'checked out'}.")
            return
    print(f"Clothing with ID {chosen_id} not found.")
    
def check_items(closet, status):
	for clothing in closet:
		if clothing.is_checked_in == status:
			clothing.print()
