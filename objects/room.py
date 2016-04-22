class Room:
    def __init__(self):
        self.characters = []
        self.items = [] # May hold duplicates!
        self.description = "An empty room."
        self.name = "Empty Room"
        self.directions = {}  # maps direction to room index, ex. "north" : 1

    # Will overwrite dir if it exists, and does not check roomNum is valid
    def add_direction(self, dir, roomNum):
        self.directions[dir] = roomNum
        assert dir in self.directions and self.directions[dir] == roomNum, "ERROR: New direction failed to add!"

    # Will not overwrite dir if it exists, and does check if roomNum is valid
    # Returns True if worked, False otherwise.
    def add_direction_safe(self, dir, roomNum, rooms):
        if dir not in self.directions and roomNum in rooms:
            self.directions[dir] = roomNum
            return True
        else:
            return False

    # Adds item to the item list in the room, allows for duplicates
    def add_item(self, item):
        self.items.append(item)
