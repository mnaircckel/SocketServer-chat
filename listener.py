import socket
import sys

HOST, PORT = "192.168.1.77", 3000
data = ""

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(data + "\n", (HOST, PORT))

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
print("--- Chatroom Client ---")
while True:
    try:
        received = sock.recv(1024)
    except:
        print("Server is unresponsive, closing connection...")
        print("Press any key to continue.")
        raw_input()
        break
    else:
        if received != "":
            print(received)

