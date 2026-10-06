class NetworkDevice:
    def __init__(self, ipAddress):
        self.ipAddress=[ipAddress]
    def ping(self):
        for i in self.ipAddress:
            print(f"Pinging to {i} Sukses!")
    def add(self, addipAddress):
        self.ipAddress.append(addipAddress)
        print("ip Address sudah masuk")

class Router(NetworkDevice):
    pass
ippertama=NetworkDevice("192.168.1.1")
ippertama.add("192.168.1.2")
print(ippertama.ping())
ipkedua=NetworkDevice("192.168.2.1")
print()
router1=Router("192.168.192")
print(router1.ping())