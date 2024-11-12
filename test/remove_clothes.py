from read_card_id import read_card_id

def remove_clothes(closet, ser=None):
    if ser:
        print("Please scan the clothing tag or enter the ID manually:")
        chosen_id = read_card_id(ser)
        if not chosen_id:
            chosen_id = input("Enter the Clothing ID that you want to remove: ")
    else:
        chosen_id = input("Enter the Clothing ID that you want to remove: ")
    
    for i, clothing in enumerate(closet):
        if clothing.ID == chosen_id:
            del closet[i]
            print("Clothing removed successfully.")
            return
    print(f"There are no Clothings with the ID of {chosen_id}")