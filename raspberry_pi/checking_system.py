def checking_system(closet, status):
    chosen_id = input(f"Enter the Clothing ID that you want to {'check in' if status else 'check out'}: ")

    for clothing in closet:
        if clothing.ID == chosen_id:
            clothing.is_checked_in = status
            print(f"Clothing ID: {chosen_id} has been {'checked in' if status else 'checked out'}.")
            return
    print(f"Clothing with ID {chosen_id} not found.")