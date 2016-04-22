class Room:
    def __init__(self):
        self.characters = []
        self.items = []  # May hold duplicates!
        self.description = "An empty room."
        self.name = "Empty Room"
        self.directions = {}  # maps direction to room index, ex. "north" : 1

    def set_name(self, name):
        self.name = name

    def set_description(self, desc):
        self.description = desc

    # Will overwrite dir if it exists, and does not check roomNum is valid
    def add_direction(self, direction, roomNum):
        self.directions[direction] = roomNum
        assert direction in self.directions and self.directions[direction] == roomNum, \
            "ERROR: New direction failed to add!"

    # Adds item to the item list in the room, allows for duplicates
    def add_item(self, item):
        self.items.append(item)

    # Adds name of character to character list in the room
    def add_character(self, name):
        self.characters.append(name)
