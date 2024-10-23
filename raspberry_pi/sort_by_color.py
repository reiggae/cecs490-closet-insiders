color_order = {"Red": 1, "Orange": 2, "Yellow": 3, "Green": 4, "Blue": 5, "Purple": 6, "Black": 7, "White": 8, "Gray": 9, "Brown": 10}

def get_color_from_detail(details):
    for detail in details:
        for color in color_order:
            if color.lower() in detail.lower():
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
    colored_clothes.sort(key=lambda x: color_order[x[0]])
    
    closet[:] = [clothing for _, clothing in colored_clothes] + uncolored_clothes

    print("Closet sorted by color.")