from clothing import Clothing

# Structure to input clothing details from the user
def input_clothing(closet):
    clothing = Clothing()
    ID_array = [clothes.ID for clothes in closet]
    
    while True:
        clothing.ID = input("Enter Clothing ID: ")
        if clothing.ID in ID_array:
            print("Tag is already registered, use another tag.")
        else:
            ID_array.append(clothing.ID)
            break
    clothing.name = input("Enter Clothing Name: ")
        
    while True:
        detail = input("Enter Detail (or type 'done' to finish): ")
        if detail == "done":
            break
        clothing.details.append(detail)

    return clothing