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