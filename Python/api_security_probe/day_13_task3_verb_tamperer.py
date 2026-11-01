import json
from day_13_task1_session_prober import APISessionProber

class VerbTamperer:
    def __init__(self, prober: APISessionProber):
        self.prober=prober
        self.test_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    def tamper_endpoint(self, endpoint:str) -> dict:
        results = []
        allowed_methods = []

        for method in self.test_methods:
            res = self.prober.send_request(method, endpoint)
            results.append({
                "method": method,
                "status_code": res["status_code"],
                "elapsed_ms": res.get("elapsed_ms")
            })
            if res["status_code"] in [200, 201]:
                allowed_methods.append(method)

        return {
            "endpoint": endpoint,
            "methods_tested": len(self.test_methods),
            "allowed_methods": allowed_methods,
            "details": results
        }
    def save_report(self, audit_data: dict, filename: str = "api_security_audit.json"):
        with open(filename, "w" ) as write:
            json.dump(audit_data, write, indent=2)
        print(f"HASIL AUDIT HTPP VERB TAMPERING: {audit_data['endpoint']}")
        print(f"Total Method Diuji   : {audit_data['methods_tested']}")
        print(f"Method Yang Diterima : {audit_data['allowed_methods']}")
        for item in audit_data["details"]:
            status = item["status_code"]
            method = item["method"]
            if status in [200, 201]:
                status_label = f"[{status} OK / DITERIMA] ⚠️"
            elif status == 405:
                status_label = f"[{status} Method Not Allowed] ✅ (Aman)"
            elif status == 404:
                status_label = f"[{status} Not Found]"
            else:
                status_label = f"[{status}]"

            print(f"  -> {method:<8} : {status_label}")

        print("=" * 60)
        print(f"[INFO] Bukti audit berhasil disimpan ke: {filename}\n")

if __name__ == "__main__":
    from pathlib import Path
    current_path=Path(__file__).resolve().parent
    prober=APISessionProber('https://httpbin.org', timeout=3.0)
    VerbTampering = VerbTamperer(prober=prober)
    oi=VerbTampering.tamper_endpoint("/post")
    VerbTampering.save_report(oi,  current_path/"api_security_audit.json")
    prober.close()

