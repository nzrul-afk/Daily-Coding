import re
from day_17_task1_workflow_parser import GithubWorkFlowParser

class SupplyChainRuleEngine:
    def __init__(self):
        self.dangerous_context_patterns = [
            "github.event.issue.title",
            "github.event.issue.body",
            "github.event.pull_request.title",
            "github.event.comment.body",
            "github.head_ref"
        ]
    def audit_workflow(self, workflow_data: dict) -> dict:
        findings=[]
        global_perm = workflow_data.get("global_permission")
        if global_perm is None or global_perm == "write-all":
            findings.append({
                "rule_id": "GHA-003",
                "severity" : "MEDIUM",
                "target" : "Workflow:Permissions",
                "message" : "Workflow tidak membatasi permissions global atau menggunakan write-all. Berisiko privilege escalation.",
            })
        for job in workflow_data.get("jobs", []):
            job_id = job.get("job_id")
            for step in job.get("steps", []):
                step_name = step.get("name", "unnamed-step")
                target_loc = f"{job_id}:{step_name}"
                if  "uses" in step:
                    action_ref = step["uses"]
                    if action_ref.startswith("./") or action_ref.startswith("docker://"):
                        pass
                    elif "@" in action_ref:
                        parts = action_ref.split("@")
                        version = parts[1]

                        if len(version) != 40:
                            findings.append({
                                "rule_id": "GHA-001",
                                "severity": "HIGH",
                                "target": target_loc,
                                "message": f"Action '{action_ref}' tidak menggunakan Full Commit SHA pinning. Rentan Supply Chain Attack."
                            })
                    else:
                        findings.append({
                            "rule_id": "GHA-001",
                            "severity": "HIGH",
                            "target": target_loc,
                            "message": f"Action '{action_ref}' tidak memiliki spesifikasi versi atau commit hash."
                        })
                if "run" in step:
                    run_script = step["run"]
                    for pattern in self.dangerous_context_patterns:
                        if pattern in run_script:
                            findings.append({
                                "rule_id": "GHA-002",
                                "severity": "CRITICAL",
                                "target": target_loc,
                                "message": f"Terdeteksi potensi Command Injection pada expression '{pattern}' di dalam perintah run shell.",
                            })
                            break
        return findings

if __name__ == "__main__":
    vulnerable_workflow = """
name: Insecure-Release-Pipeline
on: [push, pull_request]

jobs:
  build-and-notify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code Tanpa Pinning
        uses: actions/checkout@v3

      - name: Jalankan Skrip dengan Celah Command Injection
        run: |
          echo "Memproses Issue: ${{ github.event.issue.title }}"
          echo "Status: Running"

      - name: Setup Python Aman Pakai Full Commit SHA
        uses: actions/setup-python@65d7f2d534ac1bc67fcd62888c5f4f3d2cb2b236
"""

    print("=== TEST SUPPLY CHAIN SECURITY RULE ENGINE ===")
    parser = GithubWorkFlowParser()
    parsed_wf = parser.parse_workflow_str(vulnerable_workflow)

    engine = SupplyChainRuleEngine()
    audit_results = engine.audit_workflow(parsed_wf)

    print(f"Workflow yang Diuji : {parsed_wf['name']}")
    print(f"Total Pelanggaran   : {len(audit_results)}\n")
    print(f"{'SEVERITY':<10} {'RULE ID':<10} {'TARGET':<45} {'MESSAGE'}")
    print("-" * 105)

    for item in audit_results:
        print(f"[{item['severity']:<8}] {item['rule_id']:<10} {item['target']:<45} {item['message']}")


