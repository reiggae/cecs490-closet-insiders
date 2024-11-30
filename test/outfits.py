class Outfit:
    def __init__(self, outfit_name):
        self.outfit_name = outfit_name
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
        print()