import json
from day_12_task1_ssl_watchdog import SLLWatchDog
from day_12_task2_header_inspector import HeaderInspector
from pathlib import Path

class DomainSecuritygate:
    def __init__(self):
        self.ssl_watchdog = SLLWatchDog()
        self.header_inspector = HeaderInspector()
    def audit_domain(self, hostname: str) -> dict:
        ssl_res = self.ssl_watchdog.get_certificate_info(hostname)
        header_res = self.header_inspector.inspect_headers(hostname)

        if not ssl_res.get("valid") or ssl_res.get("is_expired"):
            grade = "F"

        elif ssl_res["days_remaining"] > 30 and header_res["score_percent"] == 100:
            grade = "A"
        elif ssl_res["days_remaining"] > 14 and header_res["score_percent"] >= 75:
            grade = "B"
        elif ssl_res["days_remaining"] > 7 and header_res["score_percent"] >= 50:
            grade = "C"
        else:
            grade = "D"

        is_compliant = grade in ["A", "B"]
        recommendations = []
        if ssl_res.get("days_remaining", 0) <= 30:
            recommendations.append(f"Perbarui sertifikat SSL! Sisa masa aktif tinggal {ssl_res.get('days_remaining')} hari.")

        for mh in header_res.get("missing_headers", []):
            recommendations.append(f"Pasang header '{mh['header']}' di konfigurasi web server.")

        return {
            "hostname": hostname,
            "security_grade": grade,
            "is_compliant": is_compliant,
            "ssl_audit": ssl_res,
            "header_audit": header_res,
            "recommendations": recommendations
        }
    def generate_report(self, report: dict, output_file: str = "domain_security_report.json"):
  
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        print("\n" + "=" * 60)
        print(f"📊 KARTU RAPOR KEAMANAN DOMAIN: {report['hostname']}")
        print("=" * 60)
        print(f"Nilai Akhir (Security Grade) : [ {report['security_grade']} ]")
        print(f"Status Kepatuhan Gate       : {'LOLOS (PASS) ✅' if report['is_compliant'] else 'DITOLAK (FAIL) ❌'}")
        
        ssl_data = report["ssl_audit"]
        if ssl_data.get("valid"):
            print(f"Sisa Hari Aktif SSL       : {ssl_data['days_remaining']} hari (Issuer: {ssl_data['issuer']})")
        else:
            print(f"Status SSL                 : GAGAL / ERROR ({ssl_data.get('error')})")

        hdr_data = report["header_audit"]
        print(f"Kelengkapan Security Headers : {hdr_data['score_percent']}% ({hdr_data['score_summary']})")

        if report["recommendations"]:
            print("\nRekomendasi Perbaikan:")
            for rec in report["recommendations"]:
                print(f"  [!] {rec}")

        print(f"\n[INFO] Laporan audit berhasil disimpan ke: {output_file}")

    def enforce_gate(self, report: dict) -> bool:
        if report["is_compliant"]:
            print(f"\n[PASS] Security Gate Lolos untuk '{report['hostname']}'! Siap")
            return True
        else:
            print(f"\n[BLOCKED] Security Gate Menggagalkan Deployment untuk '{report['hostname']}'! Belum siap")
            return False

if __name__ == "__main__":
    current= Path(__file__).resolve().parent
    gate = DomainSecuritygate()
    hasil = gate.audit_domain("google.com")
    gate.generate_report(hasil,current/"google_security_report.json")
    gate.enforce_gate(hasil)


