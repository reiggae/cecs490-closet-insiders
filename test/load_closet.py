import os
from clothing import Clothing

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
                    closet.append(clothes)  # Save the previous clothing item before starting a new one
                clothes = Clothing()  # Reset the clothing object for the new item
                clothes.ID = line.split(": ")[1]
            elif "Clothing Name:" in line:
                clothes.name = line.split(": ")[1]
            elif line.startswith("- "):
                clothes.details.append(line[2:])  # Add the detail to the list

    if clothes.name:
        closet.append(clothes)  # Save the last clothing item

    print(f"Closet loaded from {filename}")