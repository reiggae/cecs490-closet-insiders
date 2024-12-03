def hanger_system(closet, status):
    chosen_id = input(f"Enter the Clothing ID that you want to {'add to' if status else 'take out from'} a hanger: ")

    for clothing in closet:
        if clothing.ID == chosen_id:
            clothing.has_hanger = status
            print(f"Clothing ID: {chosen_id} has been {'added' if status else 'taken out'}.")
            return
    print(f"Clothing with ID {chosen_id} not found.")