from day_16_task1_manifest_parser   import K8sManifestParser
class PSSRuleEngine:
    def audit_manifests(self, parsed_docs: list) -> list:
        findings = []
        for doc in parsed_docs:
            doc_kind = doc["kind"]
            doc_name = doc["name"]
            doc_ns = doc["namespace"]
            for c in doc["containers"]:
                c_name = c.get("name", "unnamed")
                sec_ctx = c.get("securityContext", {}) or {}
                res = c.get("resources", {}) or {}
                limits = res.get("limits", {}) or {}
                if sec_ctx.get("privileged") is True:
                    findings.append({
                        "rule_id": "PSS-001",
                        "severity": "CRITICAL",
                        "target": f"{doc_kind}/{doc_name}:{c_name}",
                        "message": "Container berjalan dalam mode PRIVILEGED! Ini memberikan akses penuh ke kernel host."
                    })
                if sec_ctx.get("readOnlyRootFilesystem") is not True:
                    findings.append({
                        "rule_id": "PSS-002",
                        "severity": "HIGH",
                        "target": f"{doc_kind}/{doc_name}:{c_name}",
                        "message": "readOnlyRootFilesystem tidak diaktifkan. Filesystem container dapat dimodifikasi oleh penyerang."
                    })
                if sec_ctx.get("runAsNonRoot") is not True:
                    findings.append({
                        "rule_id": "PSS-003",
                        "severity": "HIGH",
                        "target": f"{doc_kind}/{doc_name}:{c_name}",
                        "message": "runAsNonRoot tidak diset True. Container berpotensi berjalan sebagai root user (UID 0)."
                    })
                has_cpu_limit = "cpu" in limits
                has_mem_limit = "memory" in limits
                if not (has_cpu_limit and has_mem_limit):
                    findings.append({
                        "rule_id": "PSS-004",
                        "severity": "MEDIUM",
                        "target": f"{doc_kind}/{doc_name}:{c_name}",
                        "message": "Resource limits (cpu/memory) tidak lengkap. Berisiko menyebabkan resource starvation (OOMKilled)."
                    })
        return findings
if __name__ == "__main__":
    vulnerable_manifest = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: insecure-worker
  namespace: backend
spec:
  template:
    spec:
      containers:
        - name: raw-worker
          image: worker:v1
          securityContext:
            privileged: true
            runAsNonRoot: false
---
apiVersion: v1
kind: Pod
metadata:
  name: secure-web
  namespace: frontend
spec:
  containers:
    - name: web-app
      image: nginx:1.25-alpine
      securityContext:
        privileged: false
        readOnlyRootFilesystem: true
        runAsNonRoot: true
      resources:
        limits:
          cpu: "500m"
          memory: "256Mi"
"""

    print("=== TEST PSS RULE ENGINE ===")
    parser = K8sManifestParser()
    parsed = parser.parse_yaml_str(vulnerable_manifest)

    engine = PSSRuleEngine()
    results = engine.audit_manifests(parsed)

    print(f"Total Temuan Pelanggaran: {len(results)}\n")
    for r in results:
        print(f"[{r['severity']:<8}] {r['rule_id']} -> {r['target']}")
        print(f"         {r['message']}")

