# Function to print all clothings in the closet
def print_closet(closet):
    print("Closet contents:")
    for i, clothing in enumerate(closet):
        print(f"Clothing {i + 1}:")
        clothing.print()