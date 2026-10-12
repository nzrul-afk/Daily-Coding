class Server:
    total_server= 0
    def __init__(self, name):
        Server.total_server += 1

server1 = Server("megawati")
server2 = Server("jokowi")
server3 = Server("prabowo")
print(Server.total_server)
