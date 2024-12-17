# This Python file uses the following encoding: utf-8

import os

class Outfit:
    def __init__(self):
        self.name = ""
        self.top = None
        self.bottom = None
        self.shoe = None
        self.tags = []

    def print(self):
        print(f"Outfit Name: {self.name}")
        print(f"Top Name: {self.top.name}")
        print(f"Bottom Name: {self.bottom.name}")
        print(f"Shoe Name:  {self.shoe.name}")
        print("Tags:")
        for tag in self.tags:
            print(f"- {tag}")
        print()
    # Function to check if any detail contains the search term
    def contains(self, term):
        if term in self.name:
            return True
        for tag in self.tags:
            if term.lower() in tag.lower():
                return True
        return False



def input_outfit(outfits,name, top, bottom, shoe, tags):
    outfit = Outfit()
    outfit.name = name
    outfit.top = top
    outfit.bottom = bottom
    outfit.shoe = shoe
    outfit.tags = tags
    outfits.append(outfit)
    return outfit

def print_outfits(outfits):
    print("Outfit contents:")
    for i, outfit in enumerate(outfits):
        print(f"Outfit {i + 1}:")
        outfit.print()

def update_outfit(outfits, outfit_index, name, top, bottom, shoe, tags):
    outfit = outfits[outfit_index]

    outfit.name = name
    outfit.top = top
    outfit.bottom = bottom
    outfit.shoe = shoe
    outfit.tags = tags

def save_outfits(closet, outfits, filename): # print(closet.index(outfit.top))
    with open(filename, 'w') as out_file:
            # Save clothing items
            out_file.write("OUTFITS:\n")
            for outfit in outfits:
                out_file.write(f"Outfit Name: {outfit.name}\n")
                top_index = closet.index(outfit.top)
                out_file.write(f"Top: {top_index}\n")
                bottom_index = closet.index(outfit.bottom)
                out_file.write(f"Bottom: {bottom_index}\n")
                shoe_index = closet.index(outfit.shoe)
                out_file.write(f"Shoe: {shoe_index}\n")
                for tag in outfit.tags:
                    out_file.write(f"- {tag}\n")

def load_outfits(closet, outfits, filename):
    if not os.path.isfile(filename):
        print("Error opening file for loading!")
        return

    outfits.clear()
    outfit = Outfit()
    image_number = 0

    with open(filename, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if "Outfit Name:" in line:
                if outfit.name:
                    outfits.append(outfit)
                outfit = Outfit()
                outfit.name = line.split(": ")[1]
            elif line.startswith("- "):
                outfit.tags.append(line[2:])
            elif "Top:" in line:
                top_index = line.split(": ")[1]
                outfit.top = closet[int(top_index)]
            elif "Bottom:" in line:
                bottom_index = line.split(": ")[1]
                outfit.bottom = closet[int(bottom_index)]
            elif "Shoe:" in line:
                shoe_index = line.split(": ")[1]
                outfit.shoe = closet[int(shoe_index)]

    if outfit.name:
        outfits.append(outfit)
    print(f"Outfits loaded from {filename}")

def remove_outfit(outfit, index):

    if 0 <= index < len(outfit):
        del outfit[index]
        print("Outfit removed successfully.")
    else:
        print(f"There is no outfit in index {index}.")
