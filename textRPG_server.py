# Main file for text RPG game
# Note: I'm using 25 ='s or -'s, = for "system" stuff, - for in-game stuff
# Note: > will precede the input line so the user knows they can type.


import sys
import signal
from threading import Thread, Lock

from setup import gameSetup
from setup import data
from Tests import debug
from characters import player
from network import server

global damagePoints             # Amount (int) to damage a player when attacked
damagePoints = 25
global commands                 # dict mapping command to possible options, like "go" : "[east/west/north/south]")
global rooms                    # dict of Rooms, {integer (index) : Room}
global npcs                     # {"name" : NPC}
global player_conversations     #
global players                  # List of players in the game (not all might be connected)
global saved_players            # Dictionary of player saves
global lock                     # Global lock to limit only one player's action to change the game state at a time
global end_server               # Flags whether or not the server should end
__LINE__ = debug.__LINE__()     # Line number at which __LINE__ is used
DEBUG = False                   # Enable/Disable debug information


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

    # Check if player is dead - if so, end the game
    if this_player.get_health() == 0:
        # Lose all your items
        if this_player.currentRoom.id != "63" and this_player.currentRoom.id != "440":
            for item in this_player.inventory:
                this_player.drop_item(["drop", item])
        # Special cases (hard-to-get-to rooms)
        else:
            # If player is in the room with the Grue, drop in the room to the north instead
            if this_player.currentRoom.id == "63":
                for item in this_player.inventory:
                    this_player.inventory.remove(item)
                    rooms["53"].add_item(item)
            # If player is in the basement, drop in the room above instead
            if this_player.currentRoom.id == "440":
                for item in this_player.inventory:
                    this_player.inventory.remove(item)
                    rooms["44"].add_item(item)
        return "YOU ARE DEAD!  Dumping your items now!\nEnding game!\n"

    assert (currentRoom.name is not None), "ERROR: Current room is None!"

    msg += "-------------------------\n"
    msg += "Player Name: " + this_player.name + '\n'
    msg += "You are in the " + currentRoom.name + '\n'
    show_items = show("items", this_player)
    if show_items != "":
        msg += show_items + '\n'
    show_people = show("people", this_player)
    if show_people != "":
        msg += show_people + '\n'
    msg += "Inventory: " + str(inventory) + '\n'
    msg += "Active Inventory: " + str(this_player.activeInventory) + '\n'
    msg += "Health: " + str(this_player.get_health()) + '\n'
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
        roomStuff = []
        for person in currentRoom.characters:
            if person != this_player.name:
                roomStuff.append(person)

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


def run_action(action, this_player):
    global rooms
    global npcs
    global players
    global damagePoints
    currentRoom = this_player.currentRoom
    inventory = this_player.inventory
    msg = ""

    if len(action) == 2 and commands.get(action[0]) is not None:

        # Decide what to do based on action[0]
        if action[0] in ["go", "move", "walk", "head"]:
            return this_player.move(action)

        elif action[0] in ["get", "grab", "take"]:
            return this_player.get_item(action)

        elif action[0] in ["talk", "speak", "greet"] and action[1] in currentRoom.characters and action[1] in npcs:
            # Launch conversation tree!
            # Note: Cannot talk to other non-NPCs!
            assert action[1] in npcs, "ERROR: NPC in room but not in global dict!"
            # npcs[action[1]].talk()
            return "talk " + action[1] + ' '

        elif action[0] in ["drop"]:
            return this_player.drop_item(action)

        elif action[0] == "show" and action[1] == "help":
            return show_help()

        elif action[0] == "look" and action[1] == "around":
            ret_str = "-------------------------\n"
            ret_str += "\nRoom Description:\n"
            ret_str += currentRoom.description + "\n"
            ret_str += "\n"
            return ret_str

        elif action[0] == "fight" and action[1] in currentRoom.characters:
            # Check opponent is in players
            for p in players:
                if p.name == action[1]:
                    p.damage(damagePoints)
                    return "-------------------------\n\nDealt " + str(damagePoints) + \
                           " damage to " + action[1] + "!\n\n"
            return "-------------------------\n\nCould not fight " + action[1] + "!\n\n"

        elif action[0] in ["use", "equip", "activate"]:
            return this_player.activate_item(action)

        elif action[0] in ["unuse", "unequip", "deactivate"]:
            return this_player.deactivate_item(action)

        elif ((action[0] == "quit" or action[0] == "end") and action[1] == "game") or \
                (action[0] == "game" and action[1] == "over"):
            return "Ending game!\n"

    else:
        return "-------------------------\n\nCannot perform that action!\n\n"

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
    global saved_players
    rooms, saved_players = data.load_saved_data()
    global commands
    commands = gameSetup.set_commands()
    global players
    players = []


def make_move(fd, this_player):
    """
    Called per client thread to handle client requests asynchronously.
    Each client will make an action, the server will process it and then
    send to the client the current status of the client's player
    :param fd:          The socket file descriptor of this player
    :param this_player: The player information for this connected client
    :return: A message for the game loop to know when to end (if the message contains "Ending game!")
    """

    global lock

    # Try getting the player's action
    try:
        response = fd.recv(100).decode('utf-8')
    except:
        if DEBUG:
            e = sys.exc_info()[0]
            print("Error: {}\nOn: {}\nLine: {}".format(e, this_player.name, __LINE__))
        return "Ending game!\n"

    # Run the player's action while locking the shared data
    with lock:
        msg = run_action(response.split(), this_player)

    # Try sending information to the player
    try:
        if "Ending game!" not in msg:
            msg += show_status(this_player)
        fd.sendall(msg.encode('utf-8'))
    except:
        if DEBUG:
            e = sys.exc_info()[0]
            print("Error: {}\nOn: {}\nLine: {}".format(e, this_player.name, __LINE__))
        return "Ending game!\n"

    return msg


def add_player(sock_fd):
    """
    Given a socket, requests player name from client
    Sets up the player or loads player if already exists
    Unique player names only
    :param sock_fd: socket of connected client
    :return:    Tuple containing the player object and a bool for if
                player creation succeeded or not
    """
    global players
    msg =   "=========================\n" + \
            "TEXT RPG\n" + \
            "=========================\n" + \
            "Do not put any spaces in your player name or in any items.\n" + \
            "Type 'show help' (w/o quotes) to see the list of possible commands.\n" + \
            "Type 'look around' (w/o quotes) to see a description of the area you are in.\n" + \
            "Commands are all in the format [verb] [noun].\n" + \
            "Type 'quit game' at any time to exit the game.\n" + \
            "=========================\n\n" + \
            "What do you want to be called?\n"

    # Get the player's name
    try:
        sock_fd.sendall(msg.encode('utf-8'))
        response = sock_fd.recv(20).decode('utf-8')  # You get 20 characters for your name :P
    except:
        if DEBUG:
            e = sys.exc_info()[0]
            print("Error: {}\nLine: {}".format(e, __LINE__))
        return "", False

    # Set up this player's character info
    if response in saved_players:
        if saved_players[response] in players:
            try:
                sock_fd.sendall("Name already in use!\nEnding Game!".encode('utf-8'))
            except:
                pass  # Ignore failed case
            sock_fd.close()
            return "", False
        this_player = saved_players[response]
    else:
        this_player = player.Player()
        this_player.set_name(response)
        this_player.currentRoom = rooms['22']

    if this_player.get_health() == 0:
        this_player.health = 25

    if this_player.currentRoom.id == "63":
        this_player.currentRoom = rooms["22"]

    this_player.currentRoom.add_character(this_player.name)

    players.append(this_player)
    return this_player, True


def process_client(fd, addr):
    """
    This function is called per client
    Each client is handled by a thread which uses this function to
    monitor the player's status and start taking their actions
    :param fd:   socket file descriptor of player
    :param addr: address information of player
    :return: Nothing (Though in the workplace this should return exit statuses of threads)
    """

    msg = ""
    global players
    this_player, success = add_player(fd)
    if not success:
        return

    # Starting statue information for player
    try:
        fd.sendall(show_status(this_player).encode('utf-8'))
    except:
        if DEBUG:
            e = sys.exc_info()[0]
            print("Error: {}\nLine: {}".format(e, __LINE__))
        msg = "Ending game!"

    # Continue until the game has ended for this player
    while "Ending game!" not in msg:
        msg = make_move(fd, this_player)

    print("Client Leaving: {}".format(addr))
    players.remove(this_player)
    name = this_player.name
    this_player.currentRoom.remove_character(name)
    saved_players[name] = this_player
    fd.close()


def start():
    """
    Starts the game
    Clients will be accepted one at a time as they connect to the server
    A thread is spawned per client to handle the client's actions
    Server will end upon a SIGINT
    """
    global end_server
    server_socket = server.setup_server()
    server_socket.settimeout(1)

    while True:
        try:
            client = sock_fd, addr = server_socket.accept()
        except:
            if DEBUG:
                e = sys.exc_info()[0]
                print("Error: {}\nLine: {}".format(e, __LINE__))
            if end_server:
                break
            continue
        print("client Joined: {}".format(addr))
        thread = Thread(target=process_client, args=client, daemon=True)
        thread.start()

    print("Ending Server!")
    server_socket.close()
    data.save_data(rooms, saved_players)


def shutdown_server(signum, frame):
    """Signal handler for closing the server on SIGINT
    :param signum:  signal number caught (doesn't matter for python...)
    :param frame:   stack from during this interrupt
    """
    global end_server
    end_server = True

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        quit("Usage: python textRPG_server.py <port>")
    signal.signal(signal.SIGINT, shutdown_server)
    global end_server
    end_server = False
    setup()
    start()

    exit(0)
