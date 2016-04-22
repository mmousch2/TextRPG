from characters import character


class Player(character.Character):
    def __init__(self):
        character.Character.__init__(self)

    def set_name(self, name):
        self.name = name

    # Returns the new currentRoom index if the move is successful, or the old one otherwise
    def move(self, action, room, currentRoom):
        if action[1] in room.directions:
            currentRoom = room.directions[action[1]]
        else:
            print("Can't move in that direction!")

        return currentRoom

    def get_item(self, action, room, inventory):
        if action[1] in room.items:
            inventory.append(action[1])
            assert action[1] in inventory, "ERROR: Failed to pick up item in room!"
            room.items.remove(action[1])
            assert action[1] not in room.items, "ERROR: Failed to remove picked up item from room!"
            print("Picked up a " + action[1] + "!")
        else:
            print("Cannot pick up that item!")

    def drop_item(self, action, inventory, room):
        if action[1] in inventory:
            inventory.remove(action[1])
            room.add_item(action[1])
            assert action[1] not in inventory, "ERROR: Failed to drop item in inventory!"
            print("You dropped a " + action[1])
        else:
            print("That item is not in your inventory!")
