import yaml
from pathlib import Path

class GithubWorkFlowParser:

    def _extract_jobs(self, raw_jobs: dict) -> list:
        job_list=[]
        if isinstance(raw_jobs, dict) == False:
            return []
        for job_id, job_data in raw_jobs.items():
            runs_on=job_data.get("runs-on", "unkown")
            permissions=job_data.get("permissions")
            steps=job_data.get("steps", None) or []

            job_list.append({
                "job_id" : job_id,
                "runs_on" : runs_on,
                "permissions" : permissions,
                "steps" : steps,
            })
        return job_list
    def parse_workflow_str(self, yaml_content: str) -> dict:
        data = yaml.safe_load(yaml_content)
        if isinstance(data, dict) == False:
            return {}
        name = data.get("name", "unkown")
        triggers = data.get("on", None) or []
        global_permission= data.get("permissions")
        raw_jobs=data.get("jobs", None) or {}

        jobs= self._extract_jobs(raw_jobs)

        total_jobs = len(jobs)
        total_steps = sum(len(j["steps"]) for j in jobs)

        return {
            "name" : name,
            "triggers" : triggers,
            "global_permission" : global_permission,
            "jobs" : jobs,
            "total_jobs" : total_jobs,
            "total_steps": total_steps,
        }
    def parse_workflow_file(self, file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return self.parse_workflow_str(content)

if __name__ == "__main__":
    sample_workflow = """
name: CI-Build-Deploy
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - name: Run Test Suite
        run: pytest --cov=src
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Run Security Linter
        run: flake8 .
"""
    print("=== TEST GITHUB ACTIONS WORKFLOW PARSER ===")
    parser = GithubWorkFlowParser()
    result = parser.parse_workflow_str(sample_workflow)
    print(f"Workflow Name       : {result['name']}")
    print(f"Triggers            : {result['triggers']}")
    print(f"Global Permissions  : {result['global_permission']}")
    print(f"Total Jobs          : {result['total_jobs']}")
    print(f"Total Steps         : {result['total_steps']}")
    print("-" * 55)
    for job in result["jobs"]:
        print(f"Job: [{job['job_id']}] (runs-on: {job['runs_on']})")
        print(f"  Jumlah Steps: {len(job['steps'])}")
        for idx, step in enumerate(job["steps"], start=1):
            s_name = step.get("name", "unnamed step")
            if "uses" in step:
                print(f"    {idx}. Action : {step['uses']} ({s_name})")
            elif "run" in step:
                print(f"    {idx}. Shell  : {step['run'].strip()} ({s_name})")
        print("-" * 55)


        