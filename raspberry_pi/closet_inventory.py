from picamera2 import Picamera2
from capture_and_process_image import capture_and_process_image
from read_card_id import read_card_id
import os

color_order = {"Red": 1, "Orange": 2, "Yellow": 3, "Green": 4, "Blue": 5, "Purple": 6, "Black": 7, "White": 8, "Gray": 9, "Brown": 10}
# Define a class to hold the clothing details
image_name_list = []
class Clothing:
    def __init__(self):
        self.name = ""
        self.image_name = ""
        self.ID = ""
        self.details = []
        self.is_checked_in = False
        self.has_hanger = False
	    
    # Function to print clothing details
    def print(self):
        print(f"Clothing ID: {self.ID}")
        print(f"Clothing Name: {self.name}")
        print(f"Image Name: {self.image_name}") #Will be deleted later, used as a placeholder for now
        print("Tags:")
        for detail in self.details:
            print(f"- {detail}")
        print(f"Status: {'checked in' if self.is_checked_in else 'checked out'}")
        print(f"It is {'' if self.has_hanger else 'not'} on a hanger")
        print()

    # Function to check if any detail contains the search term
    def contains(self, term):
        if term in self.name:
            return True
        for detail in self.details:
            if term in detail:
                return True
        return False
class Outfit:
    def __init__(self):
        self.outfit_name = ""
        self.clothing_items = {}

    def add_clothing_item(self, clothing_type, clothing_item):
        self.clothing_items[clothing_type] = clothing_item
    
    def remove_clothing_item(self, clothing_type):
        if clothing_type in self.clothing_items:
            del self.clothing_items[clothing_type]
    
    def edit_clothing_item(self, clothing_type, new_clothing_item):
        if clothing_type in self.clothing_items:
            self.clothing_items[clothing_type] = new_clothing_item
    
    def print_outfit(self):
        print(f"Outfit Name: {self.outfit_name}")
        for clothing_type, clothing_item in self.clothing_items.items():
            print(f"{clothing_type}:")
            clothing_item.print()


def input_clothing(closet, number, ser=None):
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
    clothing.name = input("Enter Clothing Name: ")

    while True:
        detail = input("Enter Detail (or type 'done' to finish): ")
        if detail == "done":
            break
        clothing.details.append(detail)
    
    clothing.image_name = f"image_{number}.png"
    image_name_list.append(clothing.image_name)

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
    print("Closet contents:")
    for i, clothing in enumerate(closet):
        print(f"Clothing {i + 1}:")
        clothing.print()
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
        clothes1.is_checked_in, clothes2.is_checked_in = clothes2.is_checked_in, clothes1.is_checked_in
        clothes1.image_name, clothes2.image_name = clothes2.image_name, clothes1.image_name
        clothes1.has_hanger, clothes2.has_hanger = clothes2.has_hanger, clothes1.has_hanger
        print("The IDs have been swapped")
    else:
        print("One or both Clothing IDs are invalid.")
# Function to save the closet and outfits to a file
def save_closet(closet, outfits, number, filename):
    with open(filename, 'w') as out_file:
        # Save clothing items
        out_file.write("CLOTHING ITEMS:\n")
        for clothes in closet:
            out_file.write(f"Clothing ID: {clothes.ID}\n")
            out_file.write(f"Clothing Name: {clothes.name}\n")
            for detail in clothes.details:
                out_file.write(f"- {detail}\n")
            out_file.write(f"Image Name: {clothes.image_name}\n")
            out_file.write(f"Checked in Status: {clothes.is_checked_in}\n")
            out_file.write(f"Clothing on Hanger: {clothes.has_hanger}\n")
            out_file.write("\n")
        
        # Save outfits
        out_file.write("OUTFITS:\n")
        for outfit in outfits:
            out_file.write(f"Outfit Name: {outfit.outfit_name}\n")
            for clothing_type, clothing_item in outfit.clothing_items.items():
                out_file.write(f"Outfit Item Type: {clothing_type}\n")
                out_file.write(f"Clothing ID: {clothing_item.ID}\n")
                out_file.write(f"Clothing Name: {clothing_item.name}\n")
                for detail in clothing_item.details:
                    out_file.write(f"- {detail}\n")
                out_file.write(f"Image Name: {clothes.image_name}\n")
                out_file.write(f"Checked in Status: {clothing_item.is_checked_in}\n")
                out_file.write(f"Clothing on Hanger: {clothes.has_hanger}\n")
                out_file.write("\n")  
            out_file.write("\n")  
        out_file.write(f"Current image count: {number}")
    print(f"Closet and outfits saved to {filename}")
# Function to load the closet from a file
def load_closet(closet, outfits, filename):
    if not os.path.isfile(filename):
        print("Error opening file for loading!")
        return

    closet.clear()
    outfits.clear()
    current_section = None
    current_outfit = None
    current_clothing = None
    current_clothing_type = None
    current_image_count = 0

    with open(filename, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if line == "CLOTHING ITEMS:":
                current_section = "clothing"
            elif line == "OUTFITS:":
                current_section = "outfits"
            elif line.startswith("Clothing ID:"):
                if current_clothing and current_section == "clothing":
                    closet.append(current_clothing)
                current_clothing = Clothing()
                current_clothing.ID = line.split(": ")[1]
            elif line.startswith("Clothing Name:"):
                current_clothing.name = line.split(": ")[1]
            elif line.startswith("- "):
                if current_clothing:
                    current_clothing.details.append(line[2:])
            elif line.startswith("Image Name:"):
                current_clothing.image_name = line.split(": ")[1]
            elif line.startswith("Checked in Status:"):
                if current_clothing:
                    current_clothing.is_checked_in = line.split(": ")[1].lower() == "true"
            elif line.startswith("Clothing on Hanger:"):
                if current_clothing:
                    current_clothing.has_hanger = line.split(": ")[1].lower() == "true"
            elif line.startswith("Outfit Name:"):
                if current_outfit:
                    outfits.append(current_outfit)
                current_outfit = Outfit(line.split(": ")[1])
            elif line.startswith("Outfit Item Type:"):
                current_clothing_type = line.split(": ")[1]
            elif line.startswith("Current image count:"):
                current_image_count = int(line.split(": ")[1])

            if current_section == "outfits" and current_clothing and current_outfit and current_clothing_type:
                current_outfit.add_clothing_item(current_clothing_type, current_clothing)
                current_clothing = None
                current_clothing_type = None

    # Add the last clothing item if in clothing section
    if current_section == "clothing" and current_clothing:
        closet.append(current_clothing)
    # Add the last outfit
    if current_outfit:
        outfits.append(current_outfit)

    print(f"Closet and outfits loaded from {filename}")
    return current_image_count

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

def take_a_picture(closet):
    image_name_list = [i.image_name for i in closet]
    while True:
        print("These are all of the image names that are registered so far: ", image_name_list)
        choice = input("Choose which one to take a picture of: ")
        if choice in image_name_list:
            picam2 = Picamera2()
            #Loop until the user is happy with the image
            while True:
                #Capture and process the image
                if capture_and_process_image(picam2, choice):
                    break  # Exit loop if the user is happy

            #Properly stop and release the camera at the end
            picam2.stop()
            break
        else:
            print("Image name not found in list. Please try again.")

def create_outfit(outfits, outfit_name):
    outfit = Outfit(outfit_name)
    outfits.append(outfit)
    return outfit

def add_clothing_to_outfit(outfits, outfit_name, clothing_type, clothing_item):
    for outfit in outfits:
        if outfit.outfit_name == outfit_name:
            outfit.add_clothing_item(clothing_type, clothing_item)
            return
        print(f"Outfit named {outfit_name} not found.")

def print_outfits(outfits):
    for outfit in outfits:
        outfit.print_outfit()
        
def hanger_system(closet, status):
    chosen_id = input(f"Enter the Clothing ID that you want to {'add to ' if status else 'take out from '} a hanger: ")

    for clothing in closet:
        if clothing.ID == chosen_id:
            clothing.has_hanger = status
            print(f"Clothing ID: {chosen_id} has been {'added' if status else 'taken out'}.")
            return
    print(f"Clothing with ID {chosen_id} not found.")

def map_clothes_to_leds(num_clothes, num_leds):
    # Mapping from clothes to LEDs
    constant = num_clothes / num_leds
    clothes_to_leds = {}
    leds_to_clothes = {i: [] for i in range(1, num_leds + 1)}

    for i in range(num_clothes):
        # Assigning each cloth to an LED
        led_index = (i // constant) % num_leds + 1  # First two clothes share LED 1, next two LED 2, etc.
        clothes_to_leds[i + 1] = led_index
        leds_to_clothes[led_index].append(i + 1)
    
    return clothes_to_leds


