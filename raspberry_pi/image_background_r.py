from picamera2 import Picamera2, Preview
import cv2
import numpy as np
from rembg import remove
from PIL import Image
import time
import os

# Function to capture and process the image
def capture_process_image(file_name):
    # Define the path where the image will be saved
    save_path = f"/home/andrewsCloset/Inventory System/Clothes/{file_name}"

    # Start the camera
    picam2 = Picamera2()

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

    # Stop camera preview
    picam2.stop_preview()
    picam2.stop()

    # Remove the background using rembg (NumPy array)
    output_image_np = remove(captured_image)

    # Save the image using the user-defined file name
    output_image = Image.fromarray(output_image_np)
    output_image.save(save_path)

    # Let the user know that the process is done
    print(f"Background was removed and the image was saved as '{file_name}'.")


def main():
	while True:
		new_image_name = input("Enter the new file name (with .png): ")
		
		if not new_image_name.endswith(".png"):
			print("Missing '.png' at the end.")
			continue
		else:
			capture_process_image(new_image_name)
			break

if __name__ == "__main__":
	main()
