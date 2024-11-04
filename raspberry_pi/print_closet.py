# Function to print all clothings in the closet
def print_closet(closet):
    rack = []
    print("Closet contents:")
    for i, clothing in enumerate(closet):
        rack.append(i)
        print(f"Clothing {i + 1}:")
        clothing.print()
    print(f"Rack List: {rack}")
