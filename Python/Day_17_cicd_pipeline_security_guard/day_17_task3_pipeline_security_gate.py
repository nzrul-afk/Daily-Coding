import json
from day_17_task1_workflow_parser import GithubWorkFlowParser
from day_17_task2_supply_chain_rules import SupplyChainRuleEngine
class PipelineSecurityGate:
    def __init__(self):
        self.parser = GithubWorkFlowParser()
        self.engine = SupplyChainRuleEngine()
    def audit_workflow(self, content_or_path: str, is_file: bool = False) -> dict:
        if is_file == True:
            manuk = self.parser.parse_workflow_file(content_or_path)
        else:
            manuk = self.parser.parse_workflow_str(content_or_path)

        findings = self.engine.audit_workflow(manuk)
        crit_count=0
        high_count=0
        med_count=0
        for f in findings:
            if f["severity"] == "CRITICAL":
                crit_count = crit_count + 1
            elif f["severity"] == "HIGH":
                high_count = high_count + 1
            else:
                med_count = med_count + 1
        score = max(0, 100 - (crit_count * 40) - (high_count * 20) - (med_count * 10))
        if score >= 90:
                Grade = "A"
                gate_status ="PASSED"
                is_passed = True
        elif score >= 70 and score < 90:
                Grade = "B"
                gate_status ="PASSED"
                is_passed = True
        elif score < 70 or crit_count > 0:
                Grade = "C"
                gate_status ="BLOCKED"
                is_passed = False
        return {
            "workflow_name": manuk.get("name", "unnamed-workflow"),
            "is_passed": is_passed,
            "gate_status": gate_status, 
            "security_grade": Grade,   
            "security_score": score,      
            "total_jobs": manuk.get("total_jobs", 0),
            "total_steps": manuk.get("total_steps", 0),
            "summary": {
                "total_findings": len(findings),
                "critical": crit_count,
                "high": high_count,
                "medium": med_count
            },
            "findings": findings
        }
    

    def save_report(self, report: dict, output_file: str = "pipeline_security_report.json"):
        with open(output_file, "w", encoding="utf-8") as output:
            json.dump(report, output, indent=2)
        print("\n" + "=" * 65)
        print("🛡️  GITHUB ACTIONS PIPELINE SECURITY SCORECARD REPORT")
        print("=" * 65)

        if report["gate_status"] == "PASSED":
            badge = "✅ LOLOS (PASSED)"
        elif report["gate_status"] == "WARNING":
            badge = "⚠️  LOLOS BERSYARAT (WARNING)"
        else:
            badge = "🛑 DITOLAK (BLOCKED)"

        print(f"[+] Workflow Name       : {report['workflow_name']}")
        print(f"[+] Security Grade      : Grade {report['security_grade']} (Score: {report['security_score']}/100)")
        print(f"[+] Quality Gate Status : {badge}")
        print(f"[+] Total Jobs / Steps  : {report['total_jobs']} Jobs | {report['total_steps']} Steps")
        
        s = report["summary"]
        print(f"[+] Ringkasan Temuan    : {s['total_findings']} Masalah (🚨 CRIT: {s['critical']} | 🔴 HIGH: {s['high']} | ⚠️ MED: {s['medium']})")
        print("-" * 65)

        if report["findings"]:
            print("Rincian Pelanggaran Keamanan Pipeline (OpenSSF / CIS Benchmark):")
            for f in report["findings"]:
                print(f"  [!] [{f['severity']:<8}] {f['rule_id']} -> {f['target']}")
                print(f"      -> {f['message']}")
        else:
            print("🎉 Workflow bersih! Mematuhi seluruh standar keamanan CI/CD!")

        print("-" * 65)
        if report["is_passed"]:
            print("🚀 [GATE PASS] Pipeline aman! Diizinkan untuk dieksekusi di GitHub Actions! ✅")
        else:
            print("🛑 [GATE BLOCKED] Pipeline Ditolak! Perbaiki celah keamanan sebelum merge PR! ❌")

        print("=" * 65)
        print(f"[INFO] Laporan audit resmi disimpan ke: {output_file}\n")
if __name__ == "__main__":
    from pathlib import Path

    sample_pipeline_yaml = """
name: Production-Release-Pipeline
on: [push]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code Tanpa Pinning
        uses: actions/checkout@v3

      - name: Eksekusi Input User Berbahaya
        run: |
          echo "Processing PR: ${{ github.event.pull_request.title }}"

      - name: Setup Node Unpinned
        uses: actions/setup-node@v2
"""

    current_dir = Path(__file__).resolve().parent
    output_path = current_dir / "pipeline_security_report.json"

    print("Menginisialisasi GitHub Actions Pipeline Security Gate...")
    gate = PipelineSecurityGate()

    print("Mengaudit workflow pipeline...")
    report = gate.audit_workflow(sample_pipeline_yaml)
    gate.save_report(report, str(output_path))


         

