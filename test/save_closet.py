# Function to save the closet to a file
def save_closet(closet, filename):
    with open(filename, 'w') as out_file:
        for clothes in closet:
            out_file.write(f"Clothing ID: {clothes.ID}\n")
            out_file.write(f"Clothing Name: {clothes.name}\n")
            for detail in clothes.details:
                out_file.write(f"- {detail}\n")
    print(f"Closet saved to {filename}")
