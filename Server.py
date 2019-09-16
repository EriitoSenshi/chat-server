import socket as s
import select

# Sockets are endpoints that receive data, they sit at an IP and a PORT
IP = "127.0.0.1"  # localhost
PORT = 1234  # Port to listen on
HEADER_LENGTH = 10

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)  # Creating the socket object, AF_NET is IPV4, SOCK_STREAM is TCP
server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)  # This will allow reconnection

server_socket.bind((IP, PORT))  # Binds the server with an IP and a Port
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

        message_length = int(message_header.decode("utf-8"))  # utf-8 is an encoding represented with bytes
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:  # In case the script is broken by the client
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    # The 3 parameters are, in order, the sockets that we want to read, the sockets that we want to write,
    # and the sockets that we might air on

    for notified_socket in read_sockets:
        if notified_socket == server_socket:  # This accepts the connection from a client and handles it
            client_connection, client_address = server_socket.accept()

            user = receive_message(client_connection)
            if user is False:  # If client disconnected
                continue

            sockets_list.append(client_connection)

            clients[client_connection] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} "
                  f"username:{user['data'].decode('utf-8')}")

        else:  # This handles sent messages
            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')}")

            for client in clients:  # Shares the message to everyone
                if client != notified_socket:
                    client.send(user['header'] + user['data'] + message['header'] + message['data'])
                    # Sends username data and the message itself

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
