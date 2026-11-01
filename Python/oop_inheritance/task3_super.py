class Server:
    def __init__(self, name):
        self.name=name
        

class WebServer(Server):
    def __init__(self, name, port):
        super().__init__(name)
        self.port=port
    def start(self):
        print(f"{self.name} is starting in {self.port} port")

namaserver= Server("nginx")
WebServernya=WebServer("ngentod", 2220)
WebServernya.start()