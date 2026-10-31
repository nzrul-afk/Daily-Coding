import json
from pathlib import Path
from day_16_task1_manifest_parser import K8sManifestParser
from day_16_task2_pss_rule_engine import PSSRuleEngine
class K8sComplianceGate:
    def __init__(self):
        self.parser = K8sManifestParser()
        self.engine = PSSRuleEngine()
    def audit_manifest(self, yaml_content_or_file: str, is_file: bool = False) -> dict:
        if is_file == True:
            docs =self.parser.parse_yaml_file(yaml_content_or_file)
        else:
            docs =self.parser.parse_yaml_str(yaml_content_or_file)
        findings = self.engine.audit_manifests(docs)

        crit_count = sum(1 for f in findings if f["severity"] == "CRITICAL")
        high_count = sum(1 for f in findings if f["severity"] == "HIGH")
        med_count = sum(1 for f in findings if f["severity"] == "MEDIUM")
        low_count = sum(1 for f in findings if f["severity"] == "LOW")
        if crit_count > 0 or high_count > 0:
            status = "BLOCKED"
            is_passed = False
        elif len(findings) == 0:
            status = "PASSED"
            is_passed = True
        else:
            status = "WARNING"
            is_passed = True

        return {
            "is_passed": is_passed,
            "gate_status": status,
            "total_documents": len(docs),
            "summary": {
                "total_findings": len(findings),
                "critical": crit_count,
                "high": high_count,
                "medium": med_count,
                "low": low_count
            },
            "findings": findings
        }
    def save_report(self, report: dict, output_file: str = "k8s_compliance_report.json"):
        with open (output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent= 2)
        print("\n" + "=" * 65)
        print("☸️  KUBERNETES MANIFEST COMPLIANCE GATE REPORT")
        print("=" * 65)

        if report["gate_status"] == "PASSED":
            badge = "✅ LOLOS (PASSED)"
        elif report["gate_status"] == "WARNING":
            badge = "⚠️  LOLOS BERSYARAT (WARNING)"
        else:
            badge = "🛑 DITOLAK (BLOCKED)"

        print(f"[+] Status Quality Gate : {badge}")
        print(f"[+] Dokumen K8s Diuji   : {report['total_documents']} Dokumen")
        
        s = report["summary"]
        print(f"[+] Ringkasan Temuan    : {s['total_findings']} Masalah (🚨 CRIT: {s['critical']} | 🔴 HIGH: {s['high']} | ⚠️ MED: {s['medium']} | ℹ️ LOW: {s['low']})")
        print("-" * 65)

        if report["findings"]:
            print("Daftar Pelanggaran Pod Security Standards (PSS):")
            for f in report["findings"]:
                print(f"  [!] [{f['severity']:<8}] {f['rule_id']} -> {f['target']}")
                print(f"      -> {f['message']}")
        else:
            print("🎉 Manifest bersih! Mematuhi seluruh standar keamanan Kubernetes!")

        print("-" * 65)
        if report["is_passed"]:
            print("[GATE PASS] Manifest diizinkan untuk di-apply ke Cluster K8s! ✅")
        else:
            print("[GATE BLOCKED] Pipeline CI/CD Dihentikan! Perbaiki temuan sebelum apply ke K8s! ❌")

        print("=" * 65)
        print(f"[INFO] Laporan audit resmi disimpan ke: {output_file}\n")

if __name__ == "__main__":
    k8s_manifest_cluster = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-gateway
  namespace: prod-finance
spec:
  template:
    spec:
      containers:
        - name: gateway-container
          image: payment-gateway:1.0.4
          securityContext:
            privileged: true
            runAsNonRoot: false
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
  namespace: prod-auth
spec:
  template:
    spec:
      containers:
        - name: auth-api
          image: auth:2.1.0
          securityContext:
            privileged: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
          resources:
            limits:
              cpu: "1"
              memory: "512Mi"
"""

    current_dir = Path(__file__).resolve().parent
    output_path = current_dir / "k8s_compliance_report.json"

    print("Menginisialisasi Kubernetes Compliance Quality Gate...")
    gate = K8sComplianceGate()

    print("Mengaudit manifest cluster Kubernetes...")
    report = gate.audit_manifest(k8s_manifest_cluster)

    gate.save_report(report, str(output_path))