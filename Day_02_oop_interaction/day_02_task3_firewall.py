class Firewall:
    def __init__(self):
        self.__blocked_ips=[]

    def add(self, ip_adress):
        if "192.168." in str(ip_adress):
            self.__blocked_ips.append(ip_adress)
            return f"ip {ip_adress} berhasil diblokir"
        else:
            return f"ip {ip_adress} tidak valid"

Fw=Firewall()
print(Fw.add("192.168.1.1"))
print(Fw.add("192.132.1.1"))
        