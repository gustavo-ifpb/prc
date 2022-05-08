import socket

HOST = '127.0.0.1'
PORT = 5004

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind( (HOST, PORT) )
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f'{addr}')
        while True:
            data = conn.recv(1024)
            print(data)
            if not data:
                break
            data_str = str(data, 'utf-8')
            conn.sendall(bytearray(data_str[::-1], 'utf-8'))

    s.close()