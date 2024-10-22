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
    save_path = f"/home/andrewsCloset/Inventory System/Clothes/{file_name}"

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
	    
def main():
    # Initialize the camera once
    picam2 = Picamera2()

    new_image_name = input("Enter the new file name (with .png extension): ")
    
    if not new_image_name.endswith(".png"):
        print("Please make sure the file name ends with '.png'")
        return  # Exit if the filename isn't valid

    # Loop until the user is happy with the image
    while True:
        # Capture and process the image
        if capture_and_process_image(picam2, new_image_name):
            break  # Exit loop if the user is happy

    # Properly stop and release the camera at the end
    picam2.stop()


if __name__ == "__main__":
	main()
