from picamera2 import Picamera2
#from capture_and_process_image import capture_and_process_image
#from read_card_id import read_card_id
import os
from enum import IntEnum

# Define a class to hold the clothing details

image_name_list = []
class color_order(IntEnum):
    RED = 1
    ORANGE = 2
    YELLOW = 3
    GREEN = 4
    BLUE = 5
    PURPLE = 6
    BLACK = 7
    WHITE = 8
    GRAY = 9
    BROWN = 10

class clothing_type(IntEnum):
    TOP = 1
    BOTTOM = 2
    SHOE = 3
    OTHER = 4

class Clothing:
    def __init__(self):
        self.name = ""
        self.image_name = ""
        self.ID = ""
        self.details = []
        self.is_checked_in = True
        self.has_hanger = True
        self.led_number = ""
        self.led_on = False
	    
    # Function to print clothing details
    def print(self):
        print(f"Clothing ID: {self.ID}")
        print(f"Clothing Name: {self.name}")
        print(f"Image Name: {self.image_name}") #Will be deleted later, used as a placeholder for now
        print("Tags:")
        for detail in self.details:
            print(f"- {detail}")
        print(f"Status: {'checked in' if self.is_checked_in else 'checked out'}")
        print(f"It is {'on' if self.has_hanger else 'not on'} a hanger")
        print(f"It is assigned to LED #: {self.led_number if self.has_hanger else '0'}")
        print()

    # Function to check if any detail contains the search term
    def contains(self, term):
        if term in self.name:
            return True
        for detail in self.details:
            if term.lower() in detail.lower():
                return True
        return False
    def check_existing_id(closet, new_id):
        for clothing in closet:
            if clothing.ID == new_id:
                return True
        return False



def input_clothing(closet, manual_id = "", manual_name = "", manual_image = "", manual_detail = "", ser=None):
    clothing = Clothing() 
    clothing.ID = manual_id #input("Enter Clothing ID: ")
                
#        if Clothing.check_existing_id(closet, clothing.ID):
#            print("Tag is already registered. Use another tag. ")
#        else:
    closet.append(clothing)
    clothing.name = manual_name

    clothing.details = manual_detail
    for clothing in closet:
        if clothing.contains("hanger"):
            clothing.has_hanger = True
        else:
            clothing.has_hanger = False

    clothing.image_name = manual_image
    image_name_list.append(clothing.image_name)

    clothing.led_number = 0

    return clothing
    
def remove_clothes(closet, index):
    
    if 0 <= index < len(closet):
        del closet[index]
        print("Clothing removed successfully.")
    else:
        print(f"There is no clothing in index {index}.")
    
def print_closet(closet):
    print("Closet contents:")
    for i, clothing in enumerate(closet):
        print(f"Clothing {i + 1}:")
        clothing.print()
# Function to update clothing
def update_clothes(closet, index, id, name, image, tags):
    clothing = closet[index]
    clothing.ID = id
    clothing.name = name
    clothing.details = tags
    if clothing.contains("hanger"):
        clothing.has_hanger = True
    else:
        clothing.has_hanger = False


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
        print("The IDs have been swapped")
    else:
        print("One or both Clothing IDs are invalid.")
# Function to save the closet to a file
def save_closet(closet, number, filename):
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
                out_file.write(f"Assigned to LED #: {clothes.led_number if clothes.has_hanger else '0'}\n")
                out_file.write(f"Current image number: {number}")
                out_file.write("\n")

#            # Save outfits
#            out_file.write("OUTFITS:\n")
#            for outfit in outfits:
#                out_file.write(f"Outfit Name: {outfit.outfit_name}\n")
#                for clothing_type, clothing_item in outfit.clothing_items.items():
#                    out_file.write(f"Outfit Item Type: {clothing_type}\n")
#                    out_file.write(f"Clothing ID: {clothing_item.ID}\n")
#                    out_file.write(f"Clothing Name: {clothing_item.name}\n")
#                    for detail in clothing_item.details:
#                        out_file.write(f"- {detail}\n")
#                    out_file.write(f"Image Name: {clothes.image_name}\n")
#                    out_file.write(f"Checked in Status: {clothing_item.is_checked_in}\n")
#                    out_file.write(f"Clothing on Hanger: {clothes.has_hanger}\n")
#                    out_file.write("\n")
#                out_file.write("\n")
    print(f"Closet and outfits saved to {filename}")
# Function to load the closet from a file
def load_closet(closet, filename):
    if not os.path.isfile(filename):
        print("Error opening file for loading!")
        return

    closet.clear()
    clothes = Clothing()
    image_number = 0

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
            elif "Checked in Status:" in line:
                clothes.is_checked_in = (line.split(": ")[1].strip().lower() == 'true')
            elif "Image Name:" in line:
                clothes.image_name = line.split(": ")[1]
            elif "Clothing on Hanger:" in line:
                clothes.has_hanger = (line.split(": ")[1].strip().lower() == 'true')
            elif "Assigned to LED #:" in line:
                clothes.led_number = line.split(": ")[1]
            elif "Current image number:" in line:
                image_number = line.split(": ")[1]

    if clothes.name:
        closet.append(clothes)
    print(f"Closet loaded from {filename}")

    if(image_number == None):
        image_number = 0

    return int(image_number)

def sort_by_alphabet(closet):
    closet.sort(key=lambda clothing:clothing.name.lower())
    closet[:] = closet
def get_color_from_detail(details):
    for detail in details:
        for color in color_order:
            if color.name.lower() in detail.lower():
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
    colored_clothes.sort(key=lambda x: x[0].value)

    closet[:] = [clothing for _, clothing in colored_clothes] + uncolored_clothes

def get_clothing_type_from_detail(details):
    for detail in details:
        for type in clothing_type:
            if type.name.lower() in detail.lower():
                return type
    return None

def sort_by_type(closet):
    typed_clothes = []
    other_clothes = []

    for clothing in closet:
        type = get_clothing_type_from_detail(clothing.details)
        if type:
            typed_clothes.append((type, clothing))
        else:
            other_clothes.append(clothing)
    typed_clothes.sort(key=lambda x: x[0].value)

    closet[:] = [clothing for _, clothing in typed_clothes] + other_clothes



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


def hanger_system(closet, status):
    chosen_id = input(f"Enter the Clothing ID that you want to {'add to ' if status else 'take out from '} a hanger: ")

    for clothing in closet:
        if clothing.ID == chosen_id:
            clothing.has_hanger = status
            print(f"Clothing ID: {chosen_id} has been {'added' if status else 'taken out'}.")
            return
    print(f"Clothing with ID {chosen_id} not found.")

def map_closet_to_leds(closet, num_leds):
    hanger_count = 0
    hanger_position = 0
    for clothing in closet:
        if clothing.has_hanger == True:
            hanger_count += 1

    if (hanger_count <= 1):
        return

    for clothing in closet:
        if clothing.has_hanger == True:
            clothing.led_number = map_clothes_to_leds(hanger_position, hanger_count, num_leds)
            hanger_position += 1


def map_clothes_to_leds(hanger_position, num_hangers, num_leds):
    # Mapping from clothes to LEDs
    led_position = int(((hanger_position) * num_leds) / (num_hangers - 1))
    return led_position


def assign_led(closet):
    current_led_number = 0
    for clothing in closet:
        if clothing.has_hanger == True:
            current_led_number += 1
            clothing.led_number = current_led_number




