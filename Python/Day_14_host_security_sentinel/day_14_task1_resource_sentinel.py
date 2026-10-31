import psutil
class ResourceSentinel:

    def __init__(self, cpu_threshold: float = 85.0, ram_threshold: float = 85.0, disk_threshold: float = 90.0):
        self.cpu_threshold = cpu_threshold
        self.ram_threshold=ram_threshold
        self.disk_threshold=disk_threshold

    def get_cpu_metrics(self) -> dict:
        persentase=psutil.cpu_percent(interval=1.0)
        core=psutil.cpu_count(logical=True)
        return{
        "usage_percent": persentase,
        "core_count": core,
        "is_alert": persentase >= self.cpu_threshold
        }

    def get_memory_metrics(self) -> dict:
        mem = psutil.virtual_memory()
        total=round(mem.total / (1024**3), 2)
        used=round(mem.used / (1024**3), 2)
        return {
            "total_gb" : total,
            "used_gb" : used,
            "percent": mem.percent, 
            "is_alert": mem.percent >= self.ram_threshold
            }
    def get_disk_metrics(self, path: str = "C:\\") -> dict:
        disk = psutil.disk_usage(path)
        total_gb = round(disk.total / (1024**3), 2)
        used_gb = round(disk.used / (1024**3), 2)
        return {
            "total_gb" : total_gb,
            "used_gb" : used_gb,
            "percent": disk.percent,
            "is_alert" : disk.percent >= self.disk_threshold
        }

    def collect_telemetry(self) -> dict:
        get_cpu = self.get_cpu_metrics()
        get_memory= self.get_memory_metrics()
        get_disk= self.get_disk_metrics()
        alert=[]
        if get_cpu["is_alert"]:
            alert.append(f"CPU Overload: {get_cpu['usage_percent']}%")
        if get_memory["is_alert"]:
            alert.append(f"RAM High: {get_memory['percent']}%")
        if get_disk["is_alert"]:
            alert.append(f"Disk High: {get_disk['percent']}%")

        is_healthy = len(alert) == 0
        return {
            "is_healthy": is_healthy,
            "status": "HEALTHY" if is_healthy else "WARNING",
            "alerts": alert,
            "metrics": {
                "cpu": get_cpu,
                "ram": get_memory,
                "disk": get_disk
            }
        }
    

if __name__ == "__main__":
    print("=== MONITORING HARDWARE TELEMETRY SENTINEL ===")
    sentinel = ResourceSentinel()

    print("Mengambil telemetri sistem (mohon tunggu 1 detik)...")
    telemetry = sentinel.collect_telemetry()
    m = telemetry["metrics"]

    print("\n" + "=" * 55)
    print("🖥️  STATUS KESEHATAN SISTEM OPERASI (HOST)")
    print("=" * 55)
    print(f"[+] CPU Usage  : {m['cpu']['usage_percent']}% ({m['cpu']['core_count']} Cores)")

    print(f"[+] RAM Usage  : {m['ram']['used_gb']} GB / {m['ram']['total_gb']} GB ({m['ram']['percent']}%)")
    
    print(f"[+] Disk Usage : {m['disk']['used_gb']} GB / {m['disk']['total_gb']} GB ({m['disk']['percent']}%)")
    
    print("-" * 55)
    if telemetry["is_healthy"]:
        print("[HEALTHY] Sistem berjalan normal dan aman!")
    else:
        print("🚨 [WARNING] TERDETEKSI BEBAN ABNORMAL PADA SISTEM:")
        for alert in telemetry["alerts"]:
            print(f"  [!] {alert}")
    print("=" * 55)
