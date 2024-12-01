def save_closet(closet, outfits, filename):
    with open(filename, 'w') as out_file:
        # Save clothing items
        out_file.write("CLOTHING ITEMS:\n")
        for clothes in closet:
            out_file.write(f"Clothing ID: {clothes.ID}\n")
            out_file.write(f"Clothing Name: {clothes.name}\n")
            for detail in clothes.details:
                out_file.write(f"- {detail}\n")
            out_file.write(f"Checked in Status: {clothes.is_checked_in}\n")
            out_file.write("\n")  # Add a blank line between clothing items
        
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
                out_file.write(f"Checked in Status: {clothing_item.is_checked_in}\n")
                out_file.write("\n")  
            out_file.write("\n")  

    print(f"Closet and outfits saved to {filename}")
