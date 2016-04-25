import socket


def start_client():
    """
    Sets up a TCP client and connect
    to the server at the given address

    :return: Socket file descriptor for the server
    """
    try:
        sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 4321)
        sock_fd.connect(server_address)
    except socket.error as e:
        quit(e)

    return sock_fd