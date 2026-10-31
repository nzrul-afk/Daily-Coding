from day_13_task1_session_prober import APISessionProber
class ExposureScanner:
    def __init__(self, prober: APISessionProber):
        self.prober = prober
        self.sensitive_targets = [
            {"path": "/.env", "risk": "HIGH", "desc": "File kredensial & environment aplikasi"},
            {"path": "/.git/HEAD", "risk": "HIGH", "desc": "Repositori source code internal"},
            {"path": "/actuator/health", "risk": "MEDIUM", "desc": "Spring Boot actuator info"},
            {"path": "/api/docs", "risk": "LOW", "desc": "Dokumentasi API Swagger / OpenAPI"},
            {"path": "/server-status", "risk": "MEDIUM", "desc": "Apache server runtime status"},
            {"path": "/config.json", "risk": "HIGH", "desc": "Konfigurasi frontend/backend"}
        ]

    def scan_endpoints(self) -> dict:
        findings= []
        all_results=[]
        for target in self.sensitive_targets:
            res = self.prober.send_request("GET", target["path"])
            if res['status_code'] == 200:
                findings.append({
                    "path": target["path"],
                    "url": res["url"],
                    "risk": target["risk"],
                    "desc": target["desc"],
                    "status_code": res["status_code"]
                })
            all_results.append({
                "path": target["path"],
                "status_code": res["status_code"],
                "elapsed_ms": res.get("elapsed_ms")
            })

        return {
        "total_scanned": len(self.sensitive_targets),
        "total_exposed": len(findings),
        "is_vulnerable": len(findings) > 0,
        "findings": findings,
        "scan_details": all_results
        }

    def print_report(self, scan_result: dict):
        print ("=== HASIL AUDIT SENSITIVE ENDPOINT EXPOSURE ===")
        print("Total Scanned: ", scan_result["total_scanned"])
        print("Total Yang Bocor: ", scan_result["total_exposed"])
        if scan_result["is_vulnerable"]:
            for f in scan_result['findings']:
                print(f"  [!] [{f['risk']}] {f['path']} -> {f['desc']}")
        else:
            print("AMAN CUYY NO BOCOR BOCOR")

if __name__ == "__main__":
    prober= APISessionProber("https://httpbin.org", timeout=3.0)
    scanner= ExposureScanner(prober=prober)
    print("Sedang memindai target...")
    laporan = scanner.scan_endpoints()
    scanner.print_report(laporan)
    prober.close()



