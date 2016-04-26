from setup import gameSetup
from network import client

global player_conversations
global npcs

def game_loop(sock_fd):
    global npcs
    msg = ""
    while "Ending game!" not in msg:

        # Get a new command from the player
        # ex. "go east" is stored as ["go", "east"]
        msg = sock_fd.recv(512).decode('utf-8')
        if "talk" == msg.split()[0]:
            npc = msg.split()[1]
            npcs[npc].talk()
        else:
            print(msg)
        action = input("> ")
        sock_fd.sendall(action.encode('utf-8'))
    sock_fd.close()
    print(msg)


if __name__ == '__main__':
    sock_fd = client.start_client()
    global player_conversations
    player_conversations = gameSetup.make_conv_trees()
    global npcs
    npcs = gameSetup.set_npcs(player_conversations)
    game_loop(sock_fd)