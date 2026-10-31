import json
from pathlib import Path
from day_09_task1_baseline import BaseLineGenerator
class IntegrityDetector:

    def __init__(self, baseline_path="baseline.json"):
        base_file = Path(__file__).resolve().parent / baseline_path
        with open(base_file, "r") as r:
            self.base= json.load(r)
        self.hasher=BaseLineGenerator()

    def scan(self, target_dir: str) -> dict:
        current_file={}
        addes=[]
        modified=[]
        removed=[]
        for i in Path(target_dir).rglob("*"):
            if i.is_file():
                rel_path = str(i.relative_to(target_dir))
                if rel_path not in self.base:
                    addes.append(rel_path)

                else:
                    current_hash = self.hasher.calculate_hash(i)
                    old_hash = self.base[rel_path]["sha256"]
                    if current_hash != old_hash:
                        modified.append(rel_path)
        for file_lama in self.base:
            file_fisik = Path(target_dir) / file_lama
            if not file_fisik.exists():
                removed.append(file_lama)
        is_secure = (len(addes) == 0 and len(modified) == 0 and len(removed) == 0)
        return {
            "is_secure":is_secure,
            "added":addes,
            "modified":modified,
            "remove":removed,
        }
    def print_report(self, audit_result: dict):
        print("===============DETECTOR=================")
        if audit_result["is_secure"] == True:
            print("YOUR SYSTEM IS SAFE & CLEAN!")
        else:
            print("ALERT: SYSTEM IS COMPROMISED / NOT SAFE!")
        print("ini list hasil scannnya")
        for i in audit_result:
            print(f"{i}= {audit_result[i]}")

if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    test_dir = current_dir / "dummy_app"
    test_dir.mkdir(exist_ok=True)
    (test_dir / "backdoor.py").write_text("import os; os.system('whoami')")
    (test_dir / "config.ini").write_text("port=666; hacked=True")
    oi=IntegrityDetector()
   
    oi.print_report( oi.scan(test_dir))
