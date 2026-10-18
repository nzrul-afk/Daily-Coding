import json
import psutil
from day_14_task1_resource_sentinel import ResourceSentinel
from day_14_task2_process_hunter import ProsessHunter

class HostSecurityAuditor:
    def __init__(self):
        self.sentinel = ResourceSentinel()
        self.hunter = ProsessHunter()
        self.high_risk_ports = [21, 23, 445, 3389]
    def audit_listening_ports(self) -> dict:
        open_ports =[]
        try:
            connections = psutil.net_connections(kind='inet')
            for conn in connections:
                if conn.status == psutil.CONN_LISTEN or conn.status == "LISTEN":
                    if conn.laddr:
                        ip = conn.laddr.ip
                        port = conn.laddr.port
                        is_risky = port in self.high_risk_ports

                        open_ports.append({
                            "ip": ip,
                            "port": port,
                            "pid": conn.pid,
                            "is_risky": is_risky
                        })

        except (psutil.AccessDenied, PermissionError):
            pass
        has_risky = any(p["is_risky"] for p in open_ports)
        return {
            "total_listening": len(open_ports),
            "has_risky_ports": has_risky,
            "listening_ports": open_ports
        }
    def generate_host_report(self) -> dict:
        hardware = self.sentinel.collect_telemetry()
        processes = self.hunter.audit_processes()
        network = self.audit_listening_ports()
        is_secure = hardware["is_healthy"] and processes["is_clean"] and not network["has_risky_ports"]
        return {
        "is_secure": is_secure,
        "hardware": hardware,
        "processes": processes,
        "network": network
        }

    def save_and_display(self, report: dict, output_file: str = "host_security_report.json"):
        with open(output_file, "w") as oi :
            json.dump(report, oi, indent=2)

        print("\n" + "=" * 65)
        print("🛡️  KARTU RAPOR KEAMANAN & TELEMETRI HOST (OS AUDIT)")
        print("=" * 65)
        
        hw = report["hardware"]
        hw_icon = "✅" if hw["is_healthy"] else "⚠️"
        print(f"[+] Status Hardware  : {hw['status']} {hw_icon}")
        print(f"    - CPU : {hw['metrics']['cpu']['usage_percent']}% | RAM : {hw['metrics']['ram']['percent']}% | Disk : {hw['metrics']['disk']['percent']}%")
        if hw["alerts"]:
            for alert in hw["alerts"]:
                print(f"    [!] Alert: {alert}")

        proc = report["processes"]
        proc_icon = "✅" if proc["is_clean"] else "🚨"
        print(f"\n[+] Status Proses    : {'CLEAN (Aman)' if proc['is_clean'] else 'ALERT (Ada Ancaman)'} {proc_icon}")
        print(f"    - Ditemukan {proc['total_suspicious']} proses mencurigakan")
        print(f"    - Top 1 RAM Eater : {proc['top_memory_processes'][0]['name']} ({proc['top_memory_processes'][0]['memory_mb']} MB)")
        net = report["network"]
        net_icon = "🚨" if net["has_risky_ports"] else "✅"
        print(f"\n[+] Status Jaringan  : {net['total_listening']} Port Terbuka (LISTEN) {net_icon}")
        if net["has_risky_ports"]:
            risky_list = [p['port'] for p in net['listening_ports'] if p['is_risky']]
            print(f"    [!] PERINGATAN: Terdeteksi port berisiko tinggi terbuka: {risky_list}")
        else:
            print("    - Semua port terbuka dalam kategori aman")

        print("-" * 65)
        if report["is_secure"]:
            print("🚀 [PASS] HOST SECURITY GATE LOLOS! Sistem aman dan layak produksi. ✅")
        else:
            print("🛑 [BLOCKED] HOST SECURITY GATE GAGAL! Terdeteksi anomali/beban kritis. ❌")

        print("=" * 65)
        print(f"[INFO] Laporan audit resmi berhasil disimpan ke: {output_file}\n")

if __name__ == "__main__":
    from pathlib import Path
    current_dir = Path(__file__).resolve().parent
    output_json = current_dir / "host_security_report.json"

    print("Menginisialisasi Host Security Auditor...")
    auditor = HostSecurityAuditor()

    print("Sedang mengaudit kesehatan sistem, proses, dan soket jaringan...")
    laporan = auditor.generate_host_report()
    auditor.save_and_display(laporan, output_json)



