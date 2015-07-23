import SocketServer

USERS = []

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        if self.client_address not in USERS:
            USERS.append(self.client_address)
            print(USERS)
        print "{}: {}".format(self.client_address,data)
        for user in USERS:
            if data != "":
                socket.sendto("{}: {}".format(self.client_address[0],data), user)
            else:
                socket.sendto("", user)           

if __name__ == "__main__":
    HOST, PORT = "192.168.1.77", 3000
    print "Starting server on {}:{}...".format(HOST,PORT)
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()
