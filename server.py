import SocketServer
HOST, PORT = "localhost", 3000
DEBUG = True

class ServerHandler:
    """
    This class manages the client protocol and sends data back to the client.
    This includes creation and deletion of clients.
    """

    def __init__(self):
        self.usernames = {}
        self.clients = []

    def new_client(self,client):
        self.clients.append(client)
        self.usernames[str(client)] = "Guest"
        if DEBUG:
            print "User {} connected.".format(client)

    def remove_client(self,client):
        self.clients.remove(client)
        del self.usernames[str(client)]
        if DEBUG:
            print "User {} disconnected.".format(client)

    def message_all(self, socket, message, sent_from):
        for client in self.clients:
            socket.sendto(str(self.usernames[str(sent_from)]) + ": " + message[9:], client)

    def get_client_data(self,client,socket,data):

        # Handle unestablished clients
        if client not in self.clients and data != "::join":
            if DEBUG:
                print "Unestablished client '{}' tried to send data to server.".format(client)

        # Respond to message by sending message to all users
        elif data[:9] == "::message":
            self.message_all(socket, data, client)  
    
        # Respond to join request
        elif data == "::join":
            if client not in self.clients:
                self.new_client(client)

        # Repsond to leave request
        elif data == "::leave":
            if client in self.clients:
                self.remove_client(client)

        # Send ping back to client
        elif data == "::ping":
            socket.sendto("::ping", client)

        elif data[:10] == "::username":
            if len(data) > 10:
                if len(data[10:]) < 12:
                    self.usernames[str(client)] = data[10:]
            
        # Send number of users back to client
        elif data == "::users":
            number_of_users = str(len(self.clients)-1)
            if number_of_users == 1:
                socket.sendto("There is currently 1 other user online.", client)
            else:
                socket.sendto("There are currently " + number_of_users + " users online.", client)

        # Handle non-standard protocol
        else:
            if DEBUG:
                print "Client '{}' tried to send unknown data to server.".format(client)
            
        
class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    server_handler = ServerHandler()
    
    def handle(self):

        # Get information sent from the client
        data = self.request[0].strip()
        socket = self.request[1]
        client = self.client_address

        # Send the client data to the server handler 
        MyUDPHandler.server_handler.get_client_data(client,socket,data)
        
        # Log to server console the data recieved
        if data[:9] == "::message":
            if DEBUG:
                print "{}: {}".format(client,data[9:])
        else:
            if DEBUG:            
                print "{}: {}".format(client,data)
        

if __name__ == "__main__":
    print "Starting server on {}:{}...".format(HOST,PORT)
    print("Debug mode is set to " + str(DEBUG))
    connections = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    connections.serve_forever()
