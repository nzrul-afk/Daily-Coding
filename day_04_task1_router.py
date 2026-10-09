class Interface:
    def __init__ (self,name, ip_address):
        self.name = name
        self.ip_address = ip_address
        self.is_up= False
    def is_on(self):
        self.is_up= True
    def is_off(self):
        self.is_up=False

class Router:
    def __init__(self, hostname):
        self.hostname = hostname
        self.interface = {}
    def add_interface(self, obj):
        self.interface[obj.name] = obj
    def ping(self, ifacename, target_ip):
        objek_iface = self.interface[ifacename]
        if ifacename in self.interface:
            if objek_iface.is_up == True:
                print(f"Ping ke {target_ip} melalui {objek_iface.name} ({objek_iface.ip_address})... Reply dari {target_ip}!")
            if objek_iface.is_up == False:
                print(f"Error: Interface {ifacename} sedang DOWN!")

        else:
            print(f"Error: Interface {ifacename} tidak ditemukan!")

interface1= Interface("Wth0", "192.168.1.1")
interface2= Interface("coli", "192.168.1.2")
interface1.is_on()
interface2.is_on()

Router1=Router("cisco")
Router2=Router("ocsic")
Router1.add_interface(interface1)
Router2.add_interface(interface2)
Router1.ping("Wth0", "8.8.8.8" )
Router2.ping("coli", "8.8.8.8")