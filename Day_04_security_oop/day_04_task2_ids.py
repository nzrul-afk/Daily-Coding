class Packet:
    def __init__ (self, src_ip, payload):
        self.src_ip = src_ip
        self.payload = payload

class IDS:
    def __init__(self):
        self.blocked_ip=[]
        self.blocked_count=0
    def analyze(self,packet_obj):

        bad_words = ["DROP TABLE", "union select", "<script>"]
        for payloadnya in bad_words:
            if payloadnya in packet_obj.payload:
                self.blocked_ip.append(packet_obj.src_ip)
                if packet_obj.src_ip in self.blocked_ip:
                    self.blocked_count += 1
                    print(f"[ALERT] Malicious packet dari {packet_obj.src_ip} diblokir! Payload: {packet_obj.payload}")
                    break
                else:
                    self.blocked_ip.append(packet_obj.src_ip)
                    self.blocked_count += 1
                    print(f"[ALERT] Malicious packet dari {packet_obj.src_ip} diblokir! Payload: {packet_obj.payload}")
                    break

        else:
            print(f"[PASS] Packet dari {packet_obj.src_ip} aman.")
    def show(self):
        print("ip yang di blokir")
        for i in self.blocked_ip:
            print(i)
        print(self.blocked_count)
packet2=Packet("192.168.1.1", "union selet makrufsjfshfiwehofihwiehfihewipfhpewhfip")
packet1=Packet("192.168.1.1", "union select makrufsjfshfiwehofihwiehfihewipfhpewhfip")
Ids=IDS()

Ids.analyze(packet2)
Ids.analyze(packet1)
Ids.show()


