import socket as s
import select

# Sockets are endpoints that receive data, they sit at an IP and a PORT
HEADER_LENGTH = 10
IP = "127.0.0.1"  # localhost
PORT = 1234  # port to listen on

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)  # Creating the socket object, AF_NET is IPV4, SOCK_STREAM is TCP
server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)  # This will allow reconnection

server_socket.bind((IP, PORT))  # Binds the server with an IP and a Port, the IP is localhost
server_socket.listen()  # This makes the server prepare itself to accept connections

sockets_list = [server_socket]  # List of client sockets

clients = {}


def receive_message(client_socket):
    """Function used to receive messages

    """
    try:
        message_header = client_socket.recv(HEADER_LENGTH)  # Receive message header

        if not len(message_header):  # If no data is received, the connection for the client is closed
            return False

        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
