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
        
        # Add user to chat room
        if self.client_address not in USERS and data[:2] == "!n":
            USERS.append(self.client_address)
            print "Current users: {}".format(USERS)
            
        # Remove user from chat room
        if self.client_address in USERS and data[:2] == "!q":
            USERS.remove(self.client_address)
            print "Current users: {}".format(USERS)
        
        # Respond to client ping
        if data[:2] == "?p":
            socket.sendto("?p",self.client_address)
                
        # Request number of users in chat room
        if data[:2] == "?u":
            if (len(USERS)-1) == 1:
                socket.sendto("There is currently 1 other user in this chatroom.",self.client_address)
            else:
                socket.sendto("There are currently " + str(len(USERS)-1) + " other users in this chatroom.",self.client_address)
        
        # Log to server console the message recieved
        print "{}: {}".format(self.client_address,data)
        
        # Send back to connected clients the message that was recieved
        for user in USERS:
            
            # Ignore blank data
            if data != "":
                # Message sent
                if data[:2] == "!m":
                    socket.sendto("{}: {}".format(self.client_address[0],data[3:]), user)
                # User joined chat
                elif data[:2] == "!n":
                    socket.sendto("User {} has joined.".format(self.client_address[0]), user)
                # User left chat
                elif data[:2] == "!q":
                    socket.sendto("User {} has left.".format(self.client_address[0]), user)
            else:
                socket.sendto("", user)           

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 3000
    print "Starting server on {}:{}...".format(HOST,PORT)
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()
