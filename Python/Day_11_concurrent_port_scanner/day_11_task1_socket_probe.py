import socket
class SocketProbe:
    def __init__(self):
        self.common_ports ={
            21 : "FTP",
            80 : "HTTP",
            22 : "SSH",
            443 : "HTTPS",
            3306 : "MySQL",
            5432 : "PostgreSQL",
            6379 : "Redis",
            8080 : "HTTP-Proxy" 
        }
    def probe_port(self, host: str, port: int, timeout: float = 1.0) -> dict:
        sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result_code= sock.connect_ex((host, port))
        Banner=None
        service_name = self.common_ports.get(port, "Unknown")
        if result_code  == 0:
            is_open = True
            try:
                sock.settimeout(0.5)
                if port in [80, 8080]:
                    sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                raw_banner = sock.recv(1024)
                Banner = raw_banner.decode("utf-8", errors="ignore").strip()
            except Exception:
                Banner = None
        else:
            is_open = False
        sock.close()
        return {
            "port": port,
            "is_open": is_open,
            "service": service_name,
            "banner" : Banner,
        }
if __name__ == "__main__":
    prober = SocketProbe()
    target = "scanme.nmap.org"
    print(f"=== UJI PROBE KE {target} ===")

    for test_port in [22, 80, 443, 3306]:
        hasil = prober.probe_port(target, test_port)
        status = "OPEN" if hasil["is_open"] else "CLOSED"
        print(f"Port {hasil['port']:<5} ({hasil['service']:<6}) : {status}")
        if hasil["banner"]:
            print(f"  -> Banner: {hasil['banner'].splitlines()[0]}")
