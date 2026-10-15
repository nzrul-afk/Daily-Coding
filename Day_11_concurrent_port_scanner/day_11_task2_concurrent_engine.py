import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from day_11_task1_socket_probe import SocketProbe

class ConcurrentPortScanner:
    def __init__(self, max_workers: int = 50):
        self.max_workers = max_workers
        self.prober = SocketProbe()
    def scan_ports(self, host: str, ports: list[int], timeout:float=1.0) ->list[dict]:
        start_time=time.time()
        results=[]
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_port = {
                executor.submit(self.prober.probe_port, host, port, timeout): port
                for port in ports
            }

        for future in as_completed(future_to_port):
            try:
                data= future.result()
                results.append(data)
            except Exception:
                pass
        results.sort(key=lambda x: x["port"])
        elapsed = round(time.time() - start_time, 2)
        print(f"[INFO] Selesai memindai {len(ports)} port dalam {elapsed} detik!")
        return results


if __name__ == "__main__":
    target = "scanme.nmap.org"

    ports_to_scan = list(range(1, 101)) + [3306, 5432, 6379, 8080]

    print(f"=== MEMULAI CONCURRENT SCAN KE {target} ({len(ports_to_scan)} PORT) ===")
    scanner = ConcurrentPortScanner(max_workers=50)
    
    hasil_scan = scanner.scan_ports(target, ports_to_scan, timeout=1.0)

    print("\n--- DAFTAR PORT YANG TERBUKA ---")
    open_ports = [p for p in hasil_scan if p["is_open"]]
    for p in open_ports:
        banner_info = f" | Banner: {p['banner'].splitlines()[0]}" if p["banner"] else ""
        print(f"[+] Port {p['port']:<5} ({p['service']:<10}) : OPEN{banner_info}")

    print(f"\nTotal port terbuka: {len(open_ports)} dari {len(ports_to_scan)} port yang diperiksa.")
        

