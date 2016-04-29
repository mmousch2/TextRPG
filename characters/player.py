from characters import character

global maxActiveItems
maxActiveItems = 2

class Player(character.Character):
    def __init__(self):
        character.Character.__init__(self)
        self.inventory = []
        self.currentRoom = None
        self.name = ""
        self.online = False
        self.health = 100
        self.activeInventory = []

    def set_name(self, name):
        self.name = name

    # Returns the new currentRoom index if the move is successful, or the old one otherwise
    def move(self, action):
        if action[1] in self.currentRoom.directions:
            # Special case about the locked basement (44 -> 440)
            if action[1] == "down" and self.currentRoom.id == "44":
                if "key" not in self.activeInventory:
                    return "-------------------------\n\nThe trap door is locked!\n\n"

            # Special case about the Pit (62)
            if action[1] in self.currentRoom.directions and self.currentRoom.id == "62":
                if "rope" not in self.activeInventory:
                    return "-------------------------\n\nThe pit is too deep to climb out of!\n\n"

            # Normal cases
            self.currentRoom.remove_character(self.name)
            self.currentRoom = self.currentRoom.directions[action[1]]
            self.currentRoom.add_character(self.name)

            # Special case about any room with the grue in it (-> instant death)
            if "Grue" in self.currentRoom.characters and "flashlight" not in self.activeInventory \
                    and "torch" not in self.activeInventory:
                self.health = 0
                return "-------------------------\n\nYOU HAVE BEEN EATEN BY A GRUE!\n"
        else:
            return "-------------------------\n\nCan't move in that direction!\n\n"

        return ""

    def get_item(self, action):
        if action[1] in self.currentRoom.items:
            self.inventory.append(action[1])
            assert action[1] in self.inventory, "ERROR: Failed to pick up item in room!"
            self.currentRoom.items.remove(action[1])
            return "-------------------------\n\nPicked up a " + action[1] + "!\n\n"
        else:
            return "-------------------------\n\nCannot pick up that item!\n\n"

    def drop_item(self, action):
        if action[1] in self.activeInventory:
            self.activeInventory.remove(action[1])

        if action[1] in self.inventory:
            self.inventory.remove(action[1])
            self.currentRoom.add_item(action[1])
            return "-------------------------\n\nYou dropped a " + action[1] + "\n\n"
        else:
            return "-------------------------\n\nThat item is not in your inventory!\n\n"

    def get_health(self):
        return self.health

    def damage(self, amount):
        self.health = max(0, self.health - amount)

    def activate_item(self, action):
        global maxActiveItems

        if action[1] in self.inventory:
            if len(self.activeInventory) < maxActiveItems:
                self.activeInventory.append(action[1])
                assert action[1] in self.activeInventory, "ERROR: Failed to add item to active inventory!"
            else:
                assert len(self.activeInventory) == maxActiveItems, "ERROR: Active inventory > maxActiveItems!"
                ret_str = "-------------------------\n\nCannot use more than two items at once!\n"
                ret_str += "'Unuse' an item before you try to use another one!\n\n"
                return ret_str

            assert action[1] in self.inventory, "ERROR: Item disappeared from inventory when activating!"
            return "-------------------------\n\nItem: " + action[1] + " now in use!\n\n"
        else:
            return "-------------------------\n\nCannot use item not in inventory!\n\n"

    def deactivate_item(self, action):
        global maxActiveItems

        if action[1] in self.activeInventory:
            self.activeInventory.remove(action[1])
            assert action[1] not in self.activeInventory, "ERROR: Failed to remove item from active inventory!"
            assert action[1] in self.inventory, "ERROR: Item disappeared from inventory when deactivating!"
            return "-------------------------\n\nItem: " + action[1] + " is no longer in use!\n\n"
        else:
            return "-------------------------\n\nItem: " + action[1] + " was not in use!\n\n"
