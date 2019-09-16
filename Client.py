import socket as s
import select
import errno
import sys

HEADER_LENGTH = 10
IP = "127.0.0.1"  # Localhost
PORT = 1234

my_username = input("Username: ")  # Inputs the username
client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)  # This way, the receive function won't be blocking

username = my_username.encode('utf-8')  # Encodes the username so we can send it
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")

    if message:  # If there is a message, encode and send it
        message = message.encode('utf-8')
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        while True:
            # Receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()

            username_length = int(username_header.decode('utf-8'))
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8'))
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"{username} > {message}")

    except IOError as e:  # These are the errors that we might see when there are no more messages to be received
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            # EAGAIN means "there is no data available right now, try again later"
            # EWOULDBLOCK means "your thread would have to block in order to do that"

            print('Reading error', str(e))
            sys.exit()
        continue  # Otherwise, continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()
