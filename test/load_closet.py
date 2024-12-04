import os
from clothing import Clothing
from outfits import Outfit

# Function to load the closet from a file
def load_closet(closet, outfits, filename):
    if not os.path.isfile(filename):
        print("Error opening file for loading!")
        return 0

    closet.clear()
    outfits.clear()
    current_section = None
    current_outfit = None
    current_clothing = None
    current_image_number = 0

    with open(filename, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if line == "CLOTHING ITEMS:":
                current_section = "clothing"
            elif line == "OUTFITS:":
                current_section = "outfits"
            elif line.startswith("Clothing ID:"):
                if current_clothing:
                    if current_section == "clothing":
                        closet.append(current_clothing)
                    elif current_section == "outfits" and current_outfit and 'current_clothing_type' in locals():
                        current_outfit.add_clothing_item(current_clothing_type, current_clothing)
                current_clothing = Clothing()
                current_clothing.ID = line.split(": ")[1]
            elif line.startswith("Clothing Name:"):
                current_clothing.name = line.split(": ")[1]
            elif line.startswith("Image Name:"):
                current_clothing.image_name = line.split(": ")[1]
            elif line.startswith("Checked in Status:"):
                current_clothing.is_checked_in = line.split(": ")[1].lower() == "true"
            elif line.startswith("Clothing on Hanger:"):
                current_clothing.has_hanger = line.split(": ")[1].lower() == "true"
            elif line.startswith("Outfit Name:"):
                if current_outfit:
                    outfits.append(current_outfit)
                current_outfit = Outfit(line.split(": ")[1])
            elif line.startswith("Outfit Item Type:"):
                current_clothing_type = line.split(": ")[1]
            elif line.startswith("Current image count:"):
                current_image_number = int(line.split(": ")[1])

    # Add the last clothing item or outfit
    if current_clothing:
        if current_section == "clothing":
            closet.append(current_clothing)
        elif current_section == "outfits" and current_outfit and 'current_clothing_type' in locals():
            current_outfit.add_clothing_item(current_clothing_type, current_clothing)
    if current_outfit:
        outfits.append(current_outfit)

    print(f"Closet and outfits loaded from {filename}")
    return current_image_number