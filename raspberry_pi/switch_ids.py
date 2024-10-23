from read_card_id import read_card_id

def switch_ids(closet, ser=None):
    if ser:
        print("Please scan the first clothing tag or enter the ID manually:")
        id1 = read_card_id(ser)
        if not id1:
            id1 = input("Enter the first Clothing ID: ")
        
        print("Please scan the second clothing tag or enter the ID manually:")
        id2 = read_card_id(ser)
        if not id2:
            id2 = input("Enter the second Clothing ID: ")
    else:
        id1 = input("Enter the first Clothing ID: ")
        id2 = input("Enter the second Clothing ID: ")

    clothes1 = None
    clothes2 = None

    for clothing in closet:
        if clothing.ID == id1:
            clothes1 = clothing
        elif clothing.ID == id2:
            clothes2 = clothing

        if clothes1 and clothes2:
            break
    
    if clothes1 and clothes2:
        clothes1.ID, clothes2.ID = clothes2.ID, clothes1.ID
        clothes1.name, clothes2.name = clothes2.name, clothes1.name
        clothes1.details, clothes2.details = clothes2.details, clothes1.details
        print("The IDs have been swapped")
    else:
        print("One or both Clothing IDs are invalid.")