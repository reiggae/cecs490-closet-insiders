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