from characters import character


class Player(character.Character):
    def __init__(self):
        character.Character.__init__(self)
        self.inventory = []
        self.currentRoom = -1
        self.name = ""
        self.online = False

    def set_name(self, name):
        self.name = name

    # Returns the new currentRoom index if the move is successful, or the old one otherwise
    def move(self, action):
        if action[1] in self.currentRoom.directions:
            self.currentRoom.remove_character(self.name)
            self.currentRoom = self.currentRoom.directions[action[1]]
            self.currentRoom.add_character(self.name)
        else:
            return "Can't move in that direction!\n"

        return ""

    def get_item(self, action):
        if action[1] in self.currentRoom.items:
            self.inventory.append(action[1])
            assert action[1] in self.inventory, "ERROR: Failed to pick up item in room!"
            self.currentRoom.items.remove(action[1])
            assert action[1] not in self.currentRoom.items, "ERROR: Failed to remove picked up item from room!"
            print("Picked up a " + action[1] + "!")
        else:
            print("Cannot pick up that item!")

    def drop_item(self, action):
        if action[1] in self.inventory:
            self.inventory.remove(action[1])
            self.currentRoom.add_item(action[1])
            assert action[1] not in self.inventory, "ERROR: Failed to drop item in inventory!"
            return "You dropped a " + action[1] + '\n'
        else:
            return "That item is not in your inventory!\n"
