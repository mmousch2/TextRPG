from characters import npc


# commands: a dict mapping command to possible options, like "go" : "[east/west/north/south]")
# rooms: a dict mapping indices to Rooms, like integer : Room
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
    npcs = dict()

    npcs["Bartender"] = npc.NPC("Bartender", player_conversations)
    npcs["Vivi"] = npc.NPC("Vivi", player_conversations)

    return npcs

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