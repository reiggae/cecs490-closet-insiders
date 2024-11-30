# Define a class to hold the clothing details
class Clothing:
    def __init__(self):
        self.name = ""
        self.image_name = ""
        self.ID = ""
        self.details = []
        self.is_checked_in = False
	    
    # Function to print clothing details
    def print(self):
        print(f"Clothing ID: {self.ID}")
        print(f"Clothing Name: {self.name}")
        print(f"Image Name: {self.image_name}") #Will be deleted later, used as a placeholder for now
        print("Tags:")
        for detail in self.details:
            print(f"- {detail}")
        print(f"Status: {'checked in' if self.is_checked_in else 'checked out'}")
        print()

    # Function to check if any detail contains the search term
    def contains(self, term):
        if term in self.name:
            return True
        for detail in self.details:
            if term in detail:
                return True
        return False