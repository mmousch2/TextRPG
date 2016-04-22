# commands: a dict mapping command to possible options, like "go" : "[east/west/north/south]")
# rooms: a dict mapping indices to Rooms, like integer : Room

global npcs
global player_conversations


def set_commands():
    # Hard-coded, unfortunately
    commands = dict()

    # Movements
    commands["go"] = commands["move"] = commands["walk"] = commands["head"] = "[north/east/south/west]"

    # Pick up
    commands["get"] = commands["grab"] = commands["take"] = "[item]"

    # Characters
    commands["talk"] = commands["speak"] = commands["greet"] = "[name]"

    # Drop
    commands["drop"] = "[item]"

    # Help
    commands["show"] = "help"

    # Map
    commands["look"] = "around"

    return commands


def set_rooms(npcs):
    # Hard-coded, unfortunately
    rooms = dict()

    # Create the Room objects here:
    # rooms[0] = Room
    # verify that any characters added are in npcs

    return rooms


def set_npcs():
    global npcs

    npcs = []

    return npcs


# Note: All player conversations must have at least two keys, "Hello." and "Goodbye."
# "Hello." maps to ("[NPC greeting]", ...), and "Goodbye." maps to ("Goodbye.").
# "<Stop Talking>" must NOT be in the tree.
def make_conv_trees():
    global player_conversations

    player_conversations = dict()  # {"NPC name" : {"What player says" : ("What NPC says", ..., "Possible replies")}}

    # Map character names (NPCs only!) to their trees

    return player_conversations


def get_conv_tree(npc_name):
    global player_conversations

    assert npc_name in player_conversations, "ERROR: That character has no conversation tree!"

    return player_conversations[npc_name]
