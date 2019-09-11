import socket

HOST = ''
PORT = 0
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(HOST, PORT)
    s.listen()
    connection, address = s.accept()
    with connection:
        print('Connected by', address)
        while True:
            data = connection.recv(buffer_size)
            if not data:
                break
            connection.sendall(data)
