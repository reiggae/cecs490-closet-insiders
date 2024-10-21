import os
import serial
import time
from picamera2 import Picamera2, Preview
import cv2
import numpy as np
from rembg import remove
from PIL import Image
import time
import os
import matplotlib.pyplot as plt

# Function to capture and process the image
def capture_and_process_image(picam2, file_name):
    # Define the path where the image will be saved
    save_path = f"/home/andrewsCloset/Desktop/Serial_Communication/Closet_Image/{file_name}"

    # Configure the camera for preview
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)

    # Start camera preview
    picam2.start_preview(Preview.QTGL)
    picam2.start()

    # Wait for 5 seconds
    print("Capturing image in 5 seconds...")
    time.sleep(5)
    print("Gotcha!")

    # Capture the image (BGR format from OpenCV)
    captured_image = picam2.capture_array()

    # Stop the camera preview
    picam2.stop()
    picam2.stop_preview()

    # Remove the background using rembg (NumPy array)
    output_image_np = remove(captured_image)

    # Display the processed image using matplotlib
    plt.ion()
    plt.clf()
    plt.imshow(output_image_np)
    plt.title("Processed Image - Background Removed")
    plt.axis('off')  # Hide axis
    plt.draw()
    plt.pause(0.001)

    # Ask user if they are happy with the image
    while True:
        user_input = input("Are you happy with the image? (y/n): ").strip().lower()

        if user_input == 'y':
            # Save the output image if the user is happy
            output_image = Image.fromarray(output_image_np)
            output_image.save(save_path)
            print(f"Image saved as '{file_name}'.")
            return True
        elif user_input == 'n':
            print("Let's capture the image again.")
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")
            
class Clothing:
    def __init__(self):
        self.name = ""
        self.ID = ""
        self.details = []

    def print(self):
        print(f"Clothing ID: {self.ID}")
        print(f"Clothing Name: {self.name}")
        print("Tags:")
        for detail in self.details:
            print(f"- {detail}")
        print()

    def contains(self, term):
        if term.lower() in self.name.lower() or term.lower() in self.ID.lower():
            return True
        for detail in self.details:
            if term.lower() in detail.lower():
                return True
        return False

def read_card_id(ser):
    start_time = time.time()
    while time.time() - start_time < 10:
        if ser.in_waiting > 0:
            card_id = ser.readline().decode('ascii').strip()
            if card_id:
                return card_id
        time.sleep(0.1)
    return None

def input_clothing(ser=None):
    clothing = Clothing()
    picam2 = Picamera2()
    
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
    
    clothing.name = input("Enter Clothing Name: ")
    if not clothing.name.endswith(".png"):
        print("Please make sure the file name ends with '.png'")
        return  # Exit if the filename isn't valid

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
    print("Closet contents:")
    for i, clothing in enumerate(closet):
        print(f"Clothing {i + 1}:")
        clothing.print()

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

def save_closet(closet, filename):
    with open(filename, 'w') as out_file:
        for clothes in closet:
            out_file.write(f"Clothing ID: {clothes.ID}\n")
            out_file.write(f"Clothing Name: {clothes.name}\n")
            for detail in clothes.details:
                out_file.write(f"- {detail}\n")
    print(f"Closet saved to {filename}")

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
        print("\nPlease choose an option")
        print("1. Add clothing")
        print("2. Remove clothing")
        print("3. View current closet")
        print("4. Update current clothing")
        print("5. Search for specific clothing")
        print("6. Swap clothing")
        print("7. Save closet information to a text file")
        print("8. Load closet information from a text file")
        print("9. Exit")
        command = input("Select options from 1 to 9: ")
        
        if command == "1":
            closet.append(input_clothing(ser))
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
            break
        else:
            print("Invalid command. Select a valid number.")

    if ser:
        ser.close()
    print("\nExiting program.")

if __name__ == "__main__":
    main()
