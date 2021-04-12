# import socket
# import pickle

# HEADERSIZE = 10

# HOST = '192.168.1.6'  # Standard loopback interface address (localhost)
# PORT = 4499        # Port to listen on (non-privileged ports are > 1023)

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))

# while True:
#     full_msg = b''
#     new_msg = True
#     while True:
#         msg = s.recv(16)
#         if new_msg:
#             print("new msg len:", msg[:HEADERSIZE])
#             msglen = int(msg[:HEADERSIZE])
#             new_msg = False

#         print(f"full message length: {msglen}")

#         full_msg += msg

#         print(len(full_msg))

#         if len(full_msg)-HEADERSIZE == msglen:
#             print("full msg recvd")
#             print(full_msg[HEADERSIZE:])
#             print(pickle.loads(full_msg[HEADERSIZE:]))
#             new_msg = True
#             full_msg = b""


import socket
#!/usr/bin/env python3


HOST = '172.16.0.105'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))

#!/usr/bin/env python3

# import socket

# HOST = '172.16.0.105'  # The server's hostname or IP address
# PORT = 65432        # The port used by the server

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     while True:
#         data = s.recv(1024)
#         if data:
#             print('Received', repr(data))
