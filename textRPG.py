# Main file for text RPG game
# Note: I'm using 25 ='s or -'s, = for "system" stuff, - for in-game stuff
# Note: > will precede the input line so the user knows they can type.


import gameSetup

global commands  # dict mapping command to possible options, like "go" : "[east/west/north/south]")
global rooms  # dict of Rooms, {integer (index) : Room}
global currentRoom  # integer index
global inventory  # list (maybe limit the size later?)
global game_over
global npcs  # {"name" : NPC}


def show_help():
    global commands

    print("=========================")
    print("Help Menu")
    print("=========================")
    print("Possible commands:")

    for cmd in commands.keys():
        print(cmd + " " + commands[cmd])


def show_status():
    global rooms
    global currentRoom
    global inventory

    print("-------------------------")
    assert (rooms[currentRoom].name is not None), "ERROR: Current room is None!"
    print("You are in the " + rooms[currentRoom].name)
    show_items()
    print("Inventory: " + str(inventory))
    print("-------------------------")


def show_items():
    global rooms
    global currentRoom

    roomItems = rooms[currentRoom].items
    if len(roomItems) > 0:
        if len(roomItems) == 1:
            print("You can see a " + roomItems[0])
        else:
            seeItems = "You can see "
            for i in range(0, len(roomItems) - 1, 1):
                seeItems += "a " + roomItems[i] + ", "
            seeItems += "and a " + roomItems[len(roomItems) - 1]
            print(seeItems)
    return


# Returns True if game is over
def run_action(action, player):
    global rooms
    global currentRoom
    global inventory
    global npcs

    if len(action) != 2 and commands.get(action[0]) is not None:
        # Decide what to do based on action[0]
        if action[0] in ["go", "move", "walk", "head"]:
            currentRoom = player.move(action, rooms[currentRoom], currentRoom)

        elif action[0] in ["get", "grab", "take"]:
            player.get_item(action, rooms[currentRoom], inventory)

        elif action[0] in ["talk", "speak", "greet"] and action[1] in rooms[currentRoom].characters:
            # Launch conversation tree!
            print("Have not implemented conversation tree yet!")
            #assert action[1] in npcs, "ERROR: NPC in room but not in global dict!"
            #npcs[action[1]].talk()

        elif action[0] in ["drop"]:
            player.drop_item(action, inventory)

        elif action[0] == "show" and action[1] == "help":
            show_help()

        elif ((action[0] == "quit" or action[0] == "end") and action[1] == "game") or \
                (action[0] == "game" and action[1] == "over"):
            print("Ending game!")
            return True  # The game is over!

    else:
        print("Cannot perform that action!")

    return False


def game_loop():
    # Set defaults
    global game_over
    game_over = False
    global npcs
    npcs = gameSetup.set_npcs()
    global currentRoom
    currentRoom = 0
    global rooms
    rooms = gameSetup.set_rooms(npcs)
    global commands
    commands = gameSetup.set_commands()
    global inventory
    inventory = []

    print("=========================")
    print("TEXT RPG")
    print("=========================")
    print("Type 'show help' (w/o quotes) to see the list of possible commands.")
    print("Type 'look around' (w/o quotes) to see a description of the area you are in.")
    print("Commands are all in the format [verb] [noun].")
    print("=========================")

    while not game_over:
        assert (currentRoom in rooms.keys()), "The current room index is not a room!"

        # Show current location
        show_status()

        # Get a new command from the player
        # ex. "go east" is stored as ["go", "east"]
        action = input("> ").lower().split()

        # Checks for invalid actions and performs it if possible
        game_over = run_action(action)
        print("-------------------------")


if __name__ == '__main__':
    game_loop()
