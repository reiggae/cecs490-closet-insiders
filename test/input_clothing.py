from clothing import Clothing
image_name_list = []

def input_clothing(closet, number):
    clothing = Clothing()
    ID_array = [clothes.ID for clothes in closet]

    while True:
        clothing.ID = input("Enter Clothing ID: ")
                
        if clothing.ID in ID_array:
            print("Tag is already registered. Use another tag. ")
        else:
            ID_array.append(clothing.ID)
            break
    clothing.name = input("Enter Clothing Name: ")

    while True:
        detail = input("Enter Detail (or type 'done' to finish): ")
        if detail == "done":
            break
        clothing.details.append(detail)
    
    clothing.image_name = f"image_{number}.png"
    image_name_list.append(clothing.image_name)

    return clothing