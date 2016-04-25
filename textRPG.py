# Main file for text RPG game
# Note: I'm using 25 ='s or -'s, = for "system" stuff, - for in-game stuff
# Note: > will precede the input line so the user knows they can type.


import sys
from threading import Thread, Lock

import gameSetup
from Tests import debug
from characters import player
from network import server

global commands                 # dict mapping command to possible options, like "go" : "[east/west/north/south]")
global rooms                    # dict of Rooms, {integer (index) : Room}
global npcs                     # {"name" : NPC}
global player_conversations     #
global players                  # List of players in the game (not all might be connected)
global number_players           # The number of required players to star the game
global lock                     # Global lock to limit only one player's action to change the game state at a time
__LINE__ = debug.__LINE__()


def show_help():
    global commands
    msg = ""
    msg += "=========================\n"
    msg += "Help Menu\n"
    msg += "=========================\n"
    msg += "Possible commands:\n"

    for cmd in commands.keys():
        msg += cmd + " " + commands[cmd] + '\n'

    return msg


def show_status(this_player):
    global rooms
    currentRoom = this_player.currentRoom
    inventory = this_player.inventory
    msg = ""

    msg += " -------------------------\n"
    assert (currentRoom.name is not None), "ERROR: Current room is None!"
    msg += "You are in the " + currentRoom.name + '\n'
    msg += show("items", this_player) + '\n'
    msg += show("people", this_player) + '\n'
    msg += "Inventory: " + str(inventory) + '\n'
    msg += "-------------------------\n"
    return msg


def show(items, this_player):
    global rooms
    currentRoom = this_player.currentRoom
    msg = ""

    if items == "items":
        roomStuff = currentRoom.items
    else:
        assert items == "people", "ERROR: Invalid option given to show(items)!"
        roomStuff = currentRoom.characters[:-1]

    if len(roomStuff) > 0:
        if len(roomStuff) == 1:
            msg += "You can see " + roomStuff[0]
        else:
            seeItems = "You can see "
            for i in range(0, len(roomStuff) - 1, 1):
                seeItems += roomStuff[i] + ", "
            seeItems += "and " + roomStuff[len(roomStuff) - 1]
            msg += seeItems
    return msg


# Returns True if game is over
def run_action(action, this_player):
    global rooms
    global npcs
    currentRoom = this_player.currentRoom
    inventory = this_player.inventory
    msg = ""

    if len(action) == 2 and commands.get(action[0]) is not None:

        # Decide what to do based on action[0]
        if action[0] in ["go", "move", "walk", "head"]:
            return this_player.move(action)

        elif action[0] in ["get", "grab", "take"]:
            #player.get_item(action, currentRoom, inventory)
            if action[1] in currentRoom.items:
                inventory.append(action[1])
                assert action[1] in inventory, "ERROR: Failed to pick up item in room!"
                currentRoom.items.remove(action[1])
                assert action[1] not in currentRoom.items, "ERROR: Failed to remove picked up item from room!"
                return "Picked up a " + action[1] + "!\n"
            else:
                return "Cannot pick up that item!\n"

        elif action[0] in ["talk", "speak", "greet"] and action[1] in currentRoom.characters:
            # Launch conversation tree!
            # print("Have not implemented conversation tree yet!")
            assert action[1] in npcs, "ERROR: NPC in room but not in global dict!"
            # npcs[action[1]].talk()
            return "talk " + action[1]

        elif action[0] in ["drop"]:
            return this_player.drop_item(action)

        elif action[0] == "show" and action[1] == "help":
            return show_help()

        elif action[0] == "look" and action[1] == "around":
            return currentRoom.description + '\n'

        elif ((action[0] == "quit" or action[0] == "end") and action[1] == "game") or \
                (action[0] == "game" and action[1] == "over"):
            return "Ending game!\n"

    else:
        return "Cannot perform that action!\n"

    return ""


def setup():
    """Sets up the game by initializing objects and players"""
    global lock
    lock = Lock()
    global player_conversations
    player_conversations = gameSetup.make_conv_trees()
    global npcs
    npcs = gameSetup.set_npcs(player_conversations)
    global rooms
    rooms = gameSetup.set_rooms(npcs)
    global commands
    commands = gameSetup.set_commands()

    # Set up the players for the game
    # Right now each player starts in the same room (Living Room - 22)
    global players
    global number_players
    players = []
    for i in range(number_players):
        p = player.Player()
        p.currentRoom = rooms[22]
        players.append(p)


def make_move(fd, this_player):
    """
    Called per client thread to handle client requests asynchronously.
    Each client will make an action, the server will process it and then
    send to the client the current status of the client's player
    :param fd: The socket file descriptor of this player
    :param this_player: The player information for this connected client
    :return: A message for the game loop to know when to end (if the message is "Ending game!\n")
    """

    global lock

    # Try getting the player's action
    try:
        response = fd.recv(100).decode('utf-8')
    except:
        e = sys.exc_info()[0]
        print("Error: {}\nOn: {}\nLine: {}".format(e, this_player.name, __LINE__))
        return "Ending game!\n"

    # Run the player's action while locking the shared data
    with lock:
        msg = run_action(response.split(), this_player)

    # Try sending information to the player
    try:
        msg += show_status(this_player)
        fd.sendall(msg.encode('utf-8'))
    except:
        e = sys.exc_info()[0]
        print("Error: {}\nOn: {}\nLine: {}".format(e, this_player.name, __LINE__))
        return "Ending game!\n"

    return msg


def process_client(client, player_id):
    """
    This function is called per client
    Each client is handled by a thread which uses this function to
    monitor the player's status and start taking their actions
    :param client: Tuple containing (socket file descriptor, address)
    :param player_id: Index of player in the global players list
    :return: Nothing (Though in the workplace this should return exit statuses of threads)
    """

    fd, addr = client
    msg =   "=========================\n" + \
            "TEXT RPG\n" + \
            "=========================\n" + \
            "Type 'show help' (w/o quotes) to see the list of possible commands.\n" + \
            "Type 'look around' (w/o quotes) to see a description of the area you are in.\n" + \
            "Commands are all in the format [verb] [noun].\n" + \
            "=========================\n\n" + \
            "What do you want to be called?\n"

    try:
        fd.sendall(msg.encode('utf-8'))
        response = fd.recv(20).decode('utf-8')  # You get 20 characters for your name :P
    except:
        e = sys.exc_info()[0]
        print("Error: {}\nLine: {}".format(e, __LINE__))
        return
    # Set up this player's character info
    this_player = players[player_id]
    this_player.set_name(response)
    this_player.currentRoom.add_character(this_player.name)

    # Starting statue information for player
    fd.sendall(show_status(this_player).encode('utf-8'))

    # Continue until the game has ended for this player
    while msg != "Ending game!\n":
            msg = make_move(fd, this_player)

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        quit("Usage: python textRPG.py <number of players>")
    global number_players
    number_players = int(args[1])
    setup()
    threads = []

    # A list of clients connected to the sever [(file descriptor, address), ...]
    info = server.setup_server(number_players)
    for i in range(number_players):
        thread = Thread(target=process_client, args=(info[i], i))
        thread.start()
        threads.append(thread)

    # Joins with each thread
    # This prevents players from dropping in and out
    # For future, could use condition variables and detached states
    for i in range(number_players):
        threads[i].join()
    exit(0)
