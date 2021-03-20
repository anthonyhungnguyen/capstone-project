# import socket
# import time
# import pickle


# HEADERSIZE = 10

# HOST = '192.168.1.6'  # Standard loopback interface address (localhost)
# PORT = 4499        # Port to listen on (non-privileged ports are > 1023)

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(5)

# while True:
#     # now our endpoint knows about the OTHER endpoint.
#     clientsocket, address = s.accept()
#     print(f"Connection from {address} has been established.")

#     d = {1: "hi", 2: "there"}
#     msg = pickle.dumps(d)
#     msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
#     print(msg)
#     clientsocket.send(msg)


#!/usr/bin/env python3

# import socket

# HOST = '192.168.1.6'  # Standard loopback interface address (localhost)
# PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)

#!/usr/bin/env python3

import socket

HOST = '192.168.1.6'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
