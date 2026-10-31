from pathlib import Path
import shutil
from day_09_task1_baseline import BaseLineGenerator
from day_09_task2_detector import IntegrityDetector
current_file=Path(__file__).resolve().parent
class InsidentResponder:
    def __init__(self, quarantine_dir="quarantine", vault_dir="backup_vault"):
        self.quarantine_dir = current_file / quarantine_dir
        self.vault_dir = current_file / vault_dir
        self.quarantine_dir.mkdir(exist_ok=True)
        self.vault_dir.mkdir(exist_ok=True)
    def create_backup(self, target_dir: str):
        for i in Path(target_dir).rglob("*"):
            if i.is_file():
                rel_path=str(i.relative_to(target_dir))
                dest_file=self.vault_dir/rel_path
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(i, dest_file)
                print(f"  + Cadangan tersimpan: {rel_path}")

        print("[BACKUP] Seluruh file bersih berhasil diamankan ke backup vault!\n")
    def remediate(self, audit_result: dict, target_dir: str):
        if audit_result["is_secure"] == True:
            print("[STATUS] Sistem aman, tidak perlu tindakan mitigasi.")
        else:
            print("[ALERT] Anomali terdeteksi! Memulai prosedur isolasi otomatis...")
            for i in audit_result["added"]:
                source_file = Path(target_dir) / i
                dest_file = self.quarantine_dir / i
                if source_file.exists():
                    shutil.move(source_file, dest_file)
                print(f"[ISOLATED] File liar '{i}' berhasil dipindahkan ke karantina! -> {dest_file}")

            for i in audit_result["modified"]:
                vault_file=self.vault_dir / i
                source_file= Path(target_dir) / i
                quarantine_file = self.quarantine_dir / i
                if source_file.exists():
                    shutil.move(source_file, quarantine_file)
                    shutil.copy2(vault_file, source_file)
                print(f"[RESTORED] File '{i}' berhasil dipulihkan dari backup vault!")
            for file_name in audit_result.get("remove", []):
                source_backup = self.vault_dir / file_name
                dest_target = Path(target_dir) / file_name
                if source_backup.exists():
                    dest_target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_backup, dest_target)
                    print(f"[RESTORED] File penting yang hilang '{file_name}' berhasil dipulihkan dari backup!")
                else:
                    print(f"[WARNING] File '{file_name}' tidak ditemukan di backup vault!")

if __name__ == "__main__":

    app_dir = current_file / "dummy_app"
    app_dir.mkdir(exist_ok=True)
    print("=" * 60)
    print("STEP 1: MENYIAPKAN APLIKASI BERSIH & BASELINE")
    print("=" * 60)
    (app_dir / "index.html").write_text("<h1>Website Bersih</h1>")
    (app_dir / "app.py").write_text("print('App OK')")
    (app_dir / "config.ini").write_text("port=8080\nenv=production")
    gen = BaseLineGenerator()
    gen.generate(app_dir, "baseline.json")
    responder = InsidentResponder()
    responder.create_backup(app_dir)
    print("=" * 60)
    print("STEP 2: SIMULASI SERANGAN SIBER (TAMPERING & SABOTASE)!")
    print("=" * 60)
    (app_dir / "backdoor.py").write_text("import os; os.system('whoami')")
    print("  [ATTACK] Hacker mengunggah 'backdoor.py'")
    (app_dir / "config.ini").write_text("port=666; hacked=True")
    print("  [ATTACK] Hacker mengubah 'config.ini'")
    if (app_dir / "index.html").exists():
        (app_dir / "index.html").unlink()
    print("  [ATTACK] Hacker menghapus 'index.html'")
    print("\n" + "=" * 60)
    print("STEP 3: DETEKTOR FIM MEMINDAI SISTEM")
    print("=" * 60)
    detector = IntegrityDetector(baseline_path="baseline.json")
    hasil_audit = detector.scan(app_dir)
    detector.print_report(hasil_audit)
    print("\n" + "=" * 60)
    print("STEP 4: AUTO-QUARANTINE & INCIDENT RESPONSE BERAKSI!")
    print("=" * 60)
    responder.remediate(hasil_audit, app_dir)
    print("\n" + "=" * 60)
    print("STEP 5: PEMINDAIAN ULANG PASCA-REMEDIASI (VERIFIKASI)")
    print("=" * 60)
    hasil_verifikasi = detector.scan(app_dir)
    detector.print_report(hasil_verifikasi)
    if hasil_verifikasi["is_secure"]:
        print("\nSISTEM BERHASIL MEMULIHKAN DIRI (SELF-HEALING) 100%!")
    else:
        print("\nMASIH ADA ANOMALI!")


        

