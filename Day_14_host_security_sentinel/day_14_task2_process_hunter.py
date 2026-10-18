import psutil
class ProsessHunter:
    def __init__(self, suspicious_keywords: list = None):
        if suspicious_keywords is None:
            self.suspicious_keywords = ["miner", "xmrig", "mimikatz", "chisel", "netcat", "backdoor"]
        else:
            self.suspicious_keywords = suspicious_keywords

    def get_top_memory_processes(self, limit: int = 5) -> list:
        procs=[]
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'memory_info']):
            try:
                p_info = proc.info
                if p_info['memory_info'] is None:
                    continue
                mem_mb = round(p_info['memory_info'].rss / (1024**2), 2)
                mem_pct = round(p_info['memory_percent'] or 0.0, 2)

                procs.append({
                    "pid": p_info["pid"],
                    "name": p_info["name"] or "Unknown",
                    "memory_mb": mem_mb,
                    "memory_percent": mem_pct
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        procs.sort(key=lambda x: x["memory_mb"], reverse=True)

        return procs[:limit]

    def hunt_suspicious_processes(self) -> list:
        suspicious_found = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'status']):
            try:
                p_name = proc.info.get('name') or ""
                p_name_lower = p_name.lower()

                for kw in self.suspicious_keywords:
                    if kw in p_name_lower:
                        suspicious_found.append({
                            'pid': proc.info['pid'],
                            'name': p_name,
                            'username': proc.info.get("username", "Unknown"),
                            'status': proc.info.get("status", "running"),
                            'triggered_keyword': kw
                        })
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        return suspicious_found

    def audit_processes(self) -> dict:
        top_mem = self.get_top_memory_processes(limit=5)
        suspicious = self.hunt_suspicious_processes()
        is_clean = len(suspicious) == 0
        return {
            "is_clean": is_clean,
            "total_suspicious": len(suspicious),
            "suspicious_processes": suspicious,
            "top_memory_processes": top_mem
        }
if __name__ == "__main__":
    print("=== HOST PROCESS HUNTER & TELEMETRY AUDIT ===")
    hunter = ProsessHunter()

    print("Memindai proses aktif di sistem...")
    audit = hunter.audit_processes()

    print("\n" + "=" * 60)
    print("TOP 5 PROSES PALING RAKUS MEMORI (RAM)")
    print("=" * 60)
    print(f"{'PID':<8} {'NAMA PROSES':<25} {'RAM (MB)':<12} {'RAM (%)':<8}")
    print("-" * 60)
    for p in audit["top_memory_processes"]:
        print(f"{p['pid']:<8} {p['name']:<25} {p['memory_mb']:<12} {p['memory_percent']}%")

    print("\n" + "=" * 60)
    print("🛡️ STATUS PERBURUAN PROSES MENCURIGAKAN")
    print("=" * 60)
    if audit["is_clean"]:
        print("[CLEAN] Tidak ada proses mencurigakan/malware yang terdeteksi! ✅")
    else:
        print(f"🚨 [ALERT] DITEMUKAN {audit['total_suspicious']} PROSES MENCURIGAKAN:")
        for sp in audit["suspicious_processes"]:
            print(f"  [!] PID {sp['pid']} | {sp['name']} | User: {sp['username']} | Trigger: '{sp['triggered_keyword']}'")
    print("=" * 60)

