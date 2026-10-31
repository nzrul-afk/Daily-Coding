
class AttackSurfaceProfile:
    def __init__(self):
        self.risk_rules = {
            3306: ("CRITICAL", "Database MySQL terbuka ke publik! Risiko kebocoran data."),
            5432: ("CRITICAL", "Database PostgreSQL terbuka ke publik! Risiko ransomware."),
            6379: ("CRITICAL", "Cache Redis terbuka tanpa autentikasi! Celah Remote Code Execution."),
            21:   ("HIGH",     "Protokol FTP tidak terenkripsi, kredensial rawan disadap."),
            23:   ("HIGH",     "Telnet mengirim password dalam teks polos! Wajib ganti ke SSH."),
            22:   ("MEDIUM",   "SSH terbuka ke publik. Sebaiknya batasi akses lewat VPN/Bastion."),
            80:   ("LOW",      "Web HTTP biasa. Disarankan redirect ke HTTPS (port 443)."),
            443:  ("LOW",      "Web HTTPS aman dengan enkripsi TLS.")
        }

    def evaluate_risk(self, host:str, scan_results: list[dict]) -> dict:
        hasil={
            "LOW": [],
            "MEDIUM": [],
            "HIGH": [],
            "CRITICAL": [],
        }
        rekomendasi=[]
        open_ports_count = 0

        for item in scan_results:
            if item["is_open"]:
                open_ports_count += 1
                port = item["port"]
                service = item["service"]
                severity, description = self.risk_rules.get(
                    port, 
                    ("LOW", f"Layanan {service} terbuka.")
                )


                hasil[severity].append({
                    "port": port,
                    "service": service,
                    "description": description
                })

                # 4. Jika port bahaya (CRITICAL atau HIGH), catat rekomendasi perbaikan!
                if severity in ["CRITICAL", "HIGH"]:
                    rekomendasi.append(
                        f"TUTUP SEGERA port {port} ({service}) menggunakan Firewall atau pindahkan ke private network!"
                    )
        is_compliant = (len(hasil["CRITICAL"]) == 0 and len(hasil["HIGH"]) == 0)

        return {
            "host": host,
            "total_open": open_ports_count,
            "is_compliant": is_compliant,
            "findings": hasil,
            "recommendations": rekomendasi
        }
    def enforce_security_gate(self, profile: dict) -> bool:
        print("\n" + "=" * 60)
        print("🛡️  HASIL AUDIT ATTACK SURFACE & SECURITY GATE")
        print("=" * 60)
        print(f"Target Host : {profile['host']}")
        print(f"Port Terbuka: {profile['total_open']}")

        if profile["is_compliant"]:
            print("\n[PASS] Security Gate LOLOS! ✅")
            print("Status: Attack surface aman, tidak ada port database/kritis yang terekspos.")
            return True
        else:
            print("\n[BLOCKED] Security Gate DITOLAK! ❌")
            print("PERINGATAN: Ditemukan port berbahaya yang terekspos ke internet publik!")
            print("\nRekomendasi Tindakan Cepat:")
            for rec in profile["recommendations"]:
                print(f"  [!] {rec}")
            return False
    def generate_report(self, profile: dict, output_file: str = "attack_surface_report.json"):
        import json
        with open(output_file, "w") as f:
            json.dump(profile, f, indent=2)
        print(f"\n[INFO] Laporan audit berhasil disimpan ke file: {output_file}")



if __name__ == "__main__":
    from pathlib import Path
    from day_11_task2_concurrent_engine import ConcurrentPortScanner
    current_folder= Path(__file__).resolve().parent
    target = "scanme.nmap.org"
    print("=" * 60)
    print(f"MEMULAI AUDIT ATTACK SURFACE PADA TARGET: {target}")
    print("=" * 60)

    ports_to_check = [21, 22, 23, 25, 80, 443, 3306, 5432, 6379, 8080]
    scanner = ConcurrentPortScanner(max_workers=20)
    scan_data = scanner.scan_ports(target, ports_to_check, timeout=1.0)

    profiler = AttackSurfaceProfile()
    hasil_profiling = profiler.evaluate_risk(target, scan_data)
    profiler.generate_report(hasil_profiling, current_folder/"attack_surface_report.json")
    profiler.enforce_security_gate(hasil_profiling)
