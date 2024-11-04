# Define a class to hold the clothing details
class Clothing:
    position_spots = set()
    available_position = 1
    def __init__(self):
        self.name = ""
        self.ID = ""
        self.details = []
        self.is_checked_in = False
        position_number = None

        if position_number is None:
            while Clothing.available_position in Clothing.position_spots:
                Clothing.available_position += 1
            position_number = Clothing.available_position
            Clothing.available_position += 1


    # Function to print clothing details
    def print(self):
        print(f"Position Number: {self.position_number}")
        print(f"Clothing ID: {self.ID}")
        print(f"Clothing Name: {self.name}")
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
