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