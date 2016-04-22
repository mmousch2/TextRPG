from objects import room
from characters import npc

# commands: a dict mapping command to possible options, like "go" : "[east/west/north/south]")
# rooms: a dict mapping indices to Rooms, like integer : Room

global npcs


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

    # Quit
    commands["quit"] = commands["end"] = "game"
    commands["game"] = "over"

    return commands


def set_npcs(player_conversations):
    global npcs

    npcs = dict()

    npcs["Bartender"] = npc.NPC("Bartender", player_conversations)
    npcs["Vivi"] = npc.NPC("Vivi", player_conversations)

    return npcs


def set_rooms(npcs):
    # Hard-coded, unfortunately
    rooms = dict()

    # Create the Room objects here:
    # Bathroom
    rooms[12] = room.Room()
    rooms[12].set_name("Bathroom")
    rooms[12].set_description("")
    rooms[12].add_direction("south", 22)

    # Woods
    rooms[13] = room.Room()
    rooms[13].set_name("Woods")
    rooms[13].set_description("")
    rooms[13].add_direction("north", 13)  # Loop north
    rooms[13].add_direction("east", 14)

    # Woods
    rooms[14] = room.Room()
    rooms[14].set_name("Woods")
    rooms[14].set_description("")
    rooms[14].add_direction("north", 14)  # Loop north
    rooms[14].add_direction("west", 13)
    rooms[14].add_direction("east", 15)
    rooms[14].add_direction("south", 24)

    # Woods
    rooms[15] = room.Room()
    rooms[15].set_name("Woods")
    rooms[15].set_description("")
    rooms[15].add_direction("north", 15)  # Loop north
    rooms[15].add_direction("west", 14)
    rooms[15].add_direction("east", 15)  # Loop east
    rooms[15].add_direction("south", 25)

    # Bedroom
    rooms[21] = room.Room()
    rooms[21].set_name("Bedroom")
    rooms[21].set_description("")
    rooms[21].add_direction("east", 22)

    # Living Room
    rooms[22] = room.Room()
    rooms[22].set_name("Living Room")
    rooms[22].set_description("")
    rooms[22].add_direction("north", 12)
    rooms[22].add_direction("west", 21)
    rooms[22].add_direction("east", 23)
    rooms[22].add_direction("south", 32)
    rooms[22].add_item("book")

    # Kitchen
    rooms[23] = room.Room()
    rooms[23].set_name("Kitchen")
    rooms[23].set_description("")
    rooms[23].add_direction("west", 22)
    rooms[23].add_item("knife")
    rooms[23].add_item("pan")

    # Woods
    rooms[24] = room.Room()
    rooms[24].set_name("Woods")
    rooms[24].set_description("The woods are not too thick here.  There is a wall to the west.")
    rooms[24].add_direction("north", 14)
    rooms[24].add_direction("east", 25)
    rooms[24].add_direction("south", 34)

    # Woods
    rooms[25] = room.Room()
    rooms[25].set_name("Woods")
    rooms[25].set_description("The woods are not too thick here.")
    rooms[25].add_direction("north", 15)
    rooms[25].add_direction("east", 25)  # Loop east
    rooms[25].add_direction("west", 24)
    rooms[25].add_direction("south", 35)

    # Lawn
    rooms[31] = room.Room()
    rooms[31].set_name("Lawn")
    rooms[31].set_description("It's just grass...I don't know what you want from me, here.  " +
                              "There is a wall to the north and the south.")
    rooms[31].add_direction("east", 32)
    rooms[31].add_direction("west", 31)  # Loop west

    # Street
    rooms[32] = room.Room()
    rooms[32].set_name("Street")
    rooms[32].set_description("It's a street.")
    rooms[32].add_direction("north", 22)
    rooms[32].add_direction("east", 33)
    rooms[32].add_direction("west", 31)
    rooms[32].add_direction("south", 42)

    # Garden
    rooms[33] = room.Room()
    rooms[33].set_name("Garden")
    rooms[33].set_description("It's a very nice garden.  You should feel bad for stepping on the flowers.")
    rooms[33].add_direction("east", 34)
    rooms[33].add_direction("west", 32)
    rooms[33].add_direction("south", 43)

    # Woods
    rooms[34] = room.Room()
    rooms[34].set_name("Woods")
    rooms[34].set_description("The woods are thin here.  There is a wall to the south.")
    rooms[34].add_direction("north", 24)
    rooms[34].add_direction("west", 33)
    rooms[34].add_direction("east", 35)

    # Woods
    rooms[35] = room.Room()
    rooms[35].set_name("Woods")
    rooms[35].set_description("The woods are not too thick here.  There is a wall to the south.")
    rooms[35].add_direction("north", 25)
    rooms[35].add_direction("east", 35)  # Loop east
    rooms[35].add_direction("west", 34)

    # Tavern
    rooms[41] = room.Room()
    rooms[41].set_name("Tavern")
    rooms[41].set_description("It's a dimly-lit but clean tavern.")
    rooms[41].add_direction("east", 42)
    rooms[41].add_item("key")
    rooms[41].add_character("Bartender")
    rooms[41].add_character("Vivi")
    assert "Bartender" in npcs, "ERROR: Bartender not in npcs!"
    assert "Vivi" in npcs, "ERROR: Vivi not in npcs!"

    # Street
    rooms[42] = room.Room()
    rooms[42].set_name("Street")
    rooms[42].set_description("It's a street.")
    rooms[42].add_direction("north", 32)
    rooms[42].add_direction("east", 43)
    rooms[42].add_direction("west", 41)
    rooms[42].add_direction("south", 52)

    # Street
    rooms[43] = room.Room()
    rooms[43].set_name("Street")
    rooms[43].set_description("It's a street.")
    rooms[43].add_direction("north", 33)
    rooms[43].add_direction("east", 44)
    rooms[43].add_direction("west", 42)
    rooms[43].add_direction("south", 53)

    # Living Room
    rooms[44] = room.Room()
    rooms[44].set_name("Living Room")
    rooms[44].set_description("It's a nice living room, with a fireplace against one wall and a rug on the floor.  " +
                              "It looks like someone tripped over it.")
    rooms[44].add_direction("east", 45)
    rooms[44].add_direction("west", 43)
    rooms[44].add_direction("south", 54)
    rooms[44].add_item("flashlight")

    # Bedroom
    rooms[45] = room.Room()
    rooms[45].set_name("Bedroom")
    rooms[45].set_description("")
    rooms[45].add_direction("west", 44)

    # Light Woods
    rooms[51] = room.Room()
    rooms[51].set_name("Light Woods")
    rooms[51].set_description("The woods are light here.  There is a wall to the north.")
    rooms[51].add_direction("east", 52)
    rooms[51].add_direction("west", 51)  # Loop west
    rooms[51].add_direction("south", 61)

    # Creepy Woods
    rooms[52] = room.Room()
    rooms[52].set_name("Woods")
    rooms[52].set_description("There is something creepy about the woods here.")
    rooms[52].add_direction("north", 42)
    rooms[52].add_direction("east", 53)
    rooms[52].add_direction("west", 51)
    rooms[52].add_direction("south", 62)

    # Creepy Woods
    rooms[53] = room.Room()
    rooms[53].set_name("Woods")
    rooms[53].set_description("There is something creepy about the woods here.  There is a wall to the east.")
    rooms[53].add_direction("north", 43)
    rooms[53].add_direction("west", 52)
    rooms[53].add_direction("south", 63)

    # Hall
    rooms[54] = room.Room()
    rooms[54].set_name("Hall")
    rooms[54].set_description("It's a hallway.")
    rooms[54].add_direction("north", 44)
    rooms[54].add_direction("east", 55)

    # Dining Room
    rooms[55] = room.Room()
    rooms[55].set_name("Dining Room")
    rooms[55].set_description("It's a normal-looking dining room.  The scent of food is coming from somewhere.")
    rooms[55].add_direction("west", 54)
    rooms[55].add_direction("south", 65)
    rooms[55].add_item("bowl")

    # Woods
    rooms[61] = room.Room()
    rooms[61].set_name("Woods")
    rooms[61].set_description("The woods are thick here.")
    rooms[61].add_direction("north", 51)
    rooms[61].add_direction("east", 62)
    rooms[61].add_direction("west", 61)  # Loop west
    rooms[61].add_direction("south", 61)  # Loop south

    # The Pit (stuck forever)
    rooms[62] = room.Room()
    rooms[62].set_name("The Pit")
    rooms[62].set_description("Eternal darkness, forever.  There is no way out.")

    # Pitch Black Woods (eaten by a Grue)
    rooms[63] = room.Room()
    rooms[63].set_name("Pitch Black")
    rooms[63].set_description("THERE IS SOMETHING IN THE DARK.")
    rooms[63].add_direction("north", 53)
    rooms[63].add_direction("east", 63)  # Loop east
    rooms[63].add_direction("west", 62)
    rooms[63].add_direction("south", 63)  # Loop south

    # Kitchen
    rooms[65] = room.Room()
    rooms[65].set_name("Kitchen")
    rooms[65].set_description("It's a normal-looking kitchen.  The whole room smells like cheap ramen.")
    rooms[65].add_direction("north", 55)
    rooms[65].add_item("ramen")

    # Basement (adding 0 after number for ground floor instead of before)
    rooms[440] = room.Room()
    rooms[440].set_name("Basement")
    rooms[440].set_description("It's an unfinished basement with a TV, a couch, and some bookshelves.")
    rooms[440].add_direction("north", 44)
    rooms[440].add_direction("east", 55)
    rooms[440].add_item("candy")
    rooms[440].add_item("manga")
    rooms[440].add_item("bones")

    # verify that any characters added are in npcs

    return rooms


# Note: All player conversations must have at least two keys, "Hello." and "Goodbye."
# "Hello." maps to ("[NPC greeting]", ...), and "Goodbye." maps to ("Goodbye.").
# "<Stop Talking>" must NOT be in the tree.
def make_conv_trees():
    player_conversations = dict()  # {"NPC name" : {"What player says" : ("What NPC says", ..., "Possible replies")}}

    # Vivi
    vivi_dict = dict()
    vivi_dict["Hello."] = ("...","How are you?","What's your name?")
    vivi_dict["How are you?"] = ("...", "...", "Goodbye.")
    vivi_dict["What's your name?"] = ("...", "...", "Goodbye.")
    vivi_dict["..."] = ("...", "Goodbye.")
    vivi_dict["Goodbye."] = ("...")
    player_conversations["Vivi"] = vivi_dict

    # Bartender
    bar_dict = dict()
    bar_dict["Hello."] = ("What can I do for you?", "Can I have a drink?",
                          "Can you tell me about that abandoned house?")
    bar_dict["Can I have a drink?"] = ("Sure, what kind?", "Whatever you've got is fine.", "Water.")
    bar_dict["Whatever you've got is fine."] = ("Here's some water.", "This is not what I asked for...", "...Thanks.")
    bar_dict["This is not what I asked for..."] =  ("Well, it's what I got for you.",
                                                    "Give me what I asked for, or else.", "...Thanks.")
    bar_dict["Give me what I asked for, or else."] = ("...", "...")
    bar_dict["..."] = ("...", "...")
    bar_dict["...Thanks."] = ("Not a problem.", "Can you tell me about that abandoned house?")
    bar_dict["Water."] = ("Here you go.", "Can you tell me about that abandoned house?")
    bar_dict["Can you tell me about that abandoned house?"] = ("Some strange fellow lived there.  Now they don't.",
                                                               "Where did they go?", "Goodbye.")
    long_str = "Ha!  Hell if I know.  One day they came in here, shoutin' about how they have prepared their whole " + \
               "life for this moment, and now it was time to show the world what an otaku could do.  Whatever the " + \
               "hell an otaku is..."
    bar_dict["Where did they go?"] = (long_str, "What...?", "Who owns the house now?")
    bar_dict["What...?"] = ("None of my business, though.", "I'm going to check out the house.  Thanks for everything.")
    bar_dict["Who owns the house now?"] = ("No one.  They left a key behind in here, though.", "Uh...Thanks.",
                                           "I don't want it.")
    bar_dict["Uh...Thanks."] = ("Eh, it was just taking up space.")
    bar_dict["I don't want it."] = ("Fine by me.")
    bar_dict["I'm going to check out the house.  Thanks for everything."] = ("...Take care.")
    bar_dict["Goodbye."] = ("Goodbye.")
    player_conversations["Bartender"] = bar_dict

    return player_conversations


def get_conv_tree(npc_name, player_conversations):
    assert npc_name in player_conversations, "ERROR: That character has no conversation tree!"

    return player_conversations[npc_name]
