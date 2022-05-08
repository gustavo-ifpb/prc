import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5004

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect( (SERVER_HOST, SERVER_PORT) )
    s.sendall(b'ola')
    data = s.recv(1024)
    print(f"{str(data, 'utf-8')}")