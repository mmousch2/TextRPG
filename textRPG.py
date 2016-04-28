import sys

from setup import gameSetup
from network import client

global player_conversations
global npcs
DEBUG = False


def perror_close(fd):
    fd.close()
    if DEBUG:
        e = sys.exc_info()[0]
        print("Error: {}".format(e))
    quit("Game Ended")


def game_loop(sock_fd):
    """
    Continues sending actions to the server and reading
    from the server until the game ends or an error occurs
    :param sock_fd: the server socket to read from and write to
    """
    global npcs
    msg = ""
    while "Ending game!" not in msg:

        # Get a new command from the player
        # ex. "go east" is stored as ["go", "east"]
        try:
            msg = sock_fd.recv(512).decode('utf-8')
        except:
            perror_close(sock_fd)

        if "talk" == msg.split()[0]:
            npc = msg.split()[1]
            npcs[npc].talk()
        else:
            print(msg)
            if "Ending game!" in msg:
                break
        action = input("> ")

        try:
            sock_fd.sendall(action.encode('utf-8'))
        except:
            perror_close(sock_fd)
    sock_fd.close()
    print(msg)


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 3:
        quit("Usage: python textRPG.py <host> <port>")
    sock_fd = client.start_client()
    global player_conversations
    player_conversations = gameSetup.make_conv_trees()
    global npcs
    npcs = gameSetup.set_npcs(player_conversations)
    game_loop(sock_fd)