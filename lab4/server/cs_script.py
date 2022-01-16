import socket

s = socket.socket()
host = 'localhost'

port = 12345
s = socket.socket()
s.bind((host, port))

s.listen(5)

conn, addr = s.accept()
print('Got connection from ', addr[0], '(', addr[1], ')')

while True:
    intosend = input("message to send:")
    conn.sendall(intosend.encode('utf-8'))
    data = conn.recv(1024)
    print(data.decode("utf-8"))
    if not data:
        break

conn.close()

print('Thank you for connecting')