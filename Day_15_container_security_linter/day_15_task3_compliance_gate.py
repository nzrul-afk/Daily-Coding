import json
from pathlib import Path
from day_15_task1_dockerfile_parser import DockerfileParser
from day_15_task2_security_rules import SecurityRulesEngine
class ContainerComplianceGate:
    def __init__(self):
        self.parser = DockerfileParser()
        self.engine = SecurityRulesEngine()

    def audit_dockerfile(self, content_or_path: str, is_file: bool = False) -> dict:
        if is_file == True:
            instructions=self.parser.parse_file(content_or_path)
        else :
            instructions=self.parser.parse_content(content_or_path)

        findings = self.engine.lint(instructions)
        high_count = sum(1 for f in findings if f["severity"] == "HIGH")
        medium_count = sum(1 for f in findings if f["severity"] == "MEDIUM")
        low_count = sum(1 for f in findings if f["severity"] == "LOW")
        if high_count > 0:
            status ="BLOCKED"
            is_passed = False
        elif len(findings) == 0:
            status= "PASSED"
            is_passed = True
        else:
            status ="WARNING"
            is_passed = True                
        return {
            "is_passed": is_passed,              
            "gate_status": status,          
            "total_instructions": len(instructions),
            "summary": {
                "total_findings": len(findings),
                "high": high_count,
                "medium": medium_count,
                "low": low_count
            },
            "findings": findings
        }
    def save_report(self, report: dict, output_file: str = "container_compliance_report.json"):
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)


        print("\n" + "=" * 65)
        print("🛡️  KARTU RAPOR KEAMANAN CONTAINER (DOCKERFILE COMPLIANCE GATE)")
        print("=" * 65)
        if report["gate_status"] == "PASSED":
            gate_badge = "✅ LOLOS (PASSED)"
        elif report["gate_status"] == "WARNING":
            gate_badge = "⚠️  LOLOS BERSYARAT (WARNING)"
        else:
            gate_badge = "🛑 DITOLAK (BLOCKED)"

        print(f"[+] Status Quality Gate : {gate_badge}")
        print(f"[+] Total Instruksi     : {report['total_instructions']}")
        
        s = report["summary"]
        print(f"[+] Ringkasan Temuan    : {s['total_findings']} Masalah (🚨 HIGH: {s['high']} | ⚠️ MEDIUM: {s['medium']} | ℹ️ LOW: {s['low']})")
        print("-" * 65)
        if report["findings"]:
            print("Daftar Pelanggaran Aturan CIS Docker Benchmark:")
            for f in report["findings"]:
                line_str = f"Baris {f['line_number']}" if f['line_number'] else "Global"
                print(f"  [!] [{f['severity']:<6}] {f['rule_id']} ({line_str})")
                print(f"      -> {f['message']}")
        else:
            print("🎉 Selamat! Dockerfile bersih dan mematuhi seluruh standar keamanan!")

        print("-" * 65)
        if report["is_passed"]:
            print("🚀 [GATE PASS] Dockerfile diizinkan lanjut ke tahap Build & Deployment! ✅")
        else:
            print("🛑 [GATE BLOCKED] Pipeline CI/CD Dihentikan! Perbaiki temuan HIGH sebelum rilis! ❌")

        print("=" * 65)
        print(f"[INFO] Bukti audit resmi berhasil disimpan ke: {output_file}\n")
if __name__ == "__main__":
    vulnerable_dockerfile = """
    # Dockerfile Tidak Aman
    FROM python:latest
    WORKDIR /app
    COPY . /app
    RUN pip install -r requirements.txt
    ENV DB_PASSWORD="***"
    EXPOSE 8080
    CMD ["python", "app.py"]
    """

    current_dir = Path(__file__).resolve().parent
    output_path = current_dir / "container_compliance_report.json"

    print("Menginisialisasi Container Compliance Quality Gate...")
    gate = ContainerComplianceGate()

    print("Mengaudit blueprint container...")
    hasil_laporan = gate.audit_dockerfile(vulnerable_dockerfile)

    # Simpan dan tampilkan hasilnya
    gate.save_report(hasil_laporan, str(output_path))
