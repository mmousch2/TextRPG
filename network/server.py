import socket


def setup_server(num_clients):
    """ Setups game's TCP server and begins accepting clients
    Game will not start until all starting clients have joined
    :param num_clients: Number of clients to connect to the server
    :return: A list of client information [(Socket file descriptor, address), ...]
    """
    try:
        sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 4321)
        sock_fd.bind(server_address)
        sock_fd.listen(num_clients)
        clients = []
        for i in range(num_clients):
            clients.append(sock_fd.accept())
    except socket.error as e:
        quit(e)
    return clients