import gameSetup
from characters import character


# from textRPG import make_move


class NPC(character.Character):
    def __init__(self, name, player_conversations):
        character.Character.__init__(self)
        self.name = name
        self.convTree = gameSetup.get_conv_tree(self.name, player_conversations)
        self.convIndex = "Hello."  # Required first thing said by player!

    # Once the player says "Goodbye.", how to set it back to "Hello."?
    def talk(self):
        while(True):
            assert self.convIndex in self.convTree, "ERROR: convIndex not in convTree!"
            conv_node = self.convTree[self.convIndex]  # ("NPC says", ..., "Player can say")

            # Print the NPC's reply
            print(self.name + ": " + conv_node[0])

            # Print possible player responses:
            if len(conv_node) > 1:
                print("-------------------------")
                print("Type the number corresponding to your reply:")
                index = 1
                while index < len(conv_node):
                    print(str(index) + ". " + conv_node[index])
                    index += 1
                print(str(index) + ". " + "<Stop Talking>")
                assert index == len(conv_node), "ERROR: index is not len(conv_node)"

                replyNum = int(input("Say > "))
                print("-------------------------")

                # Don't update convIndex if stop conversation in the middle
                if replyNum == len(conv_node):  # "<Stop Talking>"
                    break

                if conv_node[replyNum] == "Goodbye.":  # If player says "Goodbye."
                    self.convIndex = "Hello."  # Reset the conversation
                    break

                # Invalid reply
                if replyNum < 1 or replyNum > len(conv_node)-1:  # not in conv_node[1:]
                    print("That response is not valid.")
                    continue

                # Valid reply
                else:
                    if conv_node[replyNum] == "Goodbye.":  # If player says "Goodbye."
                        self.convIndex = "Hello."  # Reset the conversation
                        break
                    else:
                        self.convIndex = conv_node[replyNum]
                        continue

            # Nothing left to say
            else:
                self.convIndex = "Hello."  # Restart the conversation
                break

        # End the conversation
        if self.name != "Vivi":
            print(self.name + ": Goodbye.")
        else:
            print(self.name + ": ...bye...")
