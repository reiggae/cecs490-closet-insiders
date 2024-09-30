import os

# Define a class to hold the clothing details
class Clothing:
    def __init__(self):
        self.name = ""
        self.ID = ""
        self.details = []

    # Function to print clothing details
    def print(self):
        print(f"Clothing ID: {self.ID}")
        print(f"Clothing Name: {self.name}")
        print("Tags:")
        for detail in self.details:
            print(f"- {detail}")
        print()

    # Function to check if any detail contains the search term
    def contains(self, term):
        if term in self.name:
            return True
        for detail in self.details:
            if term in detail:
                return True
        return False

# Structure to input clothing details from the user
def input_clothing():
    clothing = Clothing()
    
    clothing.ID = input("Enter Clothing ID: ")
    clothing.name = input("Enter Clothing Name: ")
    
    while True:
        detail = input("Enter Detail (or type 'done' to finish): ")
        if detail == "done":
            break
        clothing.details.append(detail)

    return clothing

# Remove clothing from closet
def remove_clothes(closet):
    chosen_id = input("Enter the Clothing ID that you want to remove: ")
    
    for i, clothing in enumerate(closet):
        if clothing.ID == chosen_id:
            del closet[i]
            print("Clothing removed successfully.")
            return
    print(f"There are no Clothings with the ID of {chosen_id}")

# Function to print all clothings in the closet
def print_closet(closet):
    print("Closet contents:")
    for i, clothing in enumerate(closet):
        print(f"Clothing {i + 1}:")
        clothing.print()

# Function to update clothing
def update_clothes(closet):
    chosen_id = input("Enter the clothing ID that you want to update: ")

    for clothing in closet:
        if clothing.ID == chosen_id:
            print("Clothing ID found")
            while True:
                clothing.print()
                choice = input("Do you want to 'add' or 'remove' details (Type 'exit' to exit)? ")
                
                if choice == "add":
                    while True:
                        detail_add = input("Enter detail (or type 'done' to finish): ")
                        if detail_add == "done":
                            break
                        clothing.details.append(detail_add)
                
                elif choice == "remove":
                    while True:
                        detail_remove = input("Enter existing detail to remove (or type 'done' to finish): ")
                        if detail_remove == "done":
                            break
                        if detail_remove in clothing.details:
                            clothing.details.remove(detail_remove)
                            print("Detail removed successfully.")
                        else:
                            print("Detail not found.")
                
                elif choice == "exit":
                    break
                
                else:
                    print("Invalid choice. Please type 'add' or 'remove'.")
            return
    print("Clothing ID not found.")

# Search Function
def search_clothes(closet):
    search_term = input("Enter a detail to search for: ")
    print(f"Current Filters: {search_term}")
    
    found = False
    for clothing in closet:
        if clothing.contains(search_term):
            clothing.print()
            found = True

    if not found:
        print(f"No clothings found with the detail: {search_term}")

# Function to save the closet to a file
def save_closet(closet, filename):
    with open(filename, 'w') as out_file:
        for clothes in closet:
            out_file.write(f"Clothing ID: {clothes.ID}\n")
            out_file.write(f"Clothing Name: {clothes.name}\n")
            for detail in clothes.details:
                out_file.write(f"- {detail}\n")
    print(f"Closet saved to {filename}")

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

def switch_ids(closet):
    id1 = input("Enter the first Clothing ID: ")
    id2 = input("Enter the second Clothing ID: ")

    clothes1 = None
    clothes2 = None

    #Find both clothing IDs
    for clothing in closet:
        if clothing.ID == id1:
            clothes1 = clothing
        elif clothing.ID == id2:
            clothes2 = clothing

        if clothes1 and clothes2:
            break
    
    #If both are found, swap IDs
    if clothes1 and clothes2:
        clothes1.ID, clothes2.ID = clothes2.ID, clothes1.ID
        clothes1.name, clothes2.name = clothes2.name, clothes1.name
        clothes1.details, clothes2.details = clothes2.details, clothes1.details
        print("The IDs have been swapped")
    else:
        print("One or both Clothing IDs are invalid.")

def main():
    # Create a list to store the Clothings
    closet = []
    
    print("Welcome to the Closet Manager")

    while True:
        print("Please choose an option")
        print("1. Add clothing")
        print("2. Remove clothing")
        print("3. View current closet")
        print("4. Update current clothing")
        print("5. Search for specific clothing")
        print("6. Swap clothing")
        print("7. Save closet information to a text file")
        print("8. Load closet information from a text file")
        print("9. Exit")
        command = input("Select options from 1 to 9: ")
        
        if command == "done":
            break
        elif command == "1":
            closet.append(input_clothing())
        elif command == "2":
            remove_clothes(closet)    
        elif command == "3":
            print_closet(closet)
        elif command == "4":
            update_clothes(closet)    
        elif command == "5":
            search_clothes(closet)
        elif command == "6":
            switch_ids(closet)
        elif command == "7":
            filename = input("Enter file name to save to: ")
            save_closet(closet, filename)
        elif command == "8":
            filename = input("Enter file name to load from: ")
            load_closet(closet, filename)
        elif command == "9":
            break
        else:
            print("Invalid command. Select a valid number.")

if __name__ == "__main__":
    main()
