import socket


def setup_server():
    """ Setups game's TCP server
    :return: The TCP server's socket to accept clients on
    """
    try:
        sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 4321)
        sock_fd.bind(server_address)
        sock_fd.listen(100)
    except socket.error as e:
        quit(e)
    return sock_fd