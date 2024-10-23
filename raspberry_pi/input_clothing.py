from clothing import Clothing
from picamera2 import Picamera2, Preview
from capture_and_process_image import capture_and_process_image
from read_card_id import read_card_id

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
        print("Skipping image capture.")
        
    else:

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