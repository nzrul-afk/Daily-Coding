from day_10_task1_matcher import SecretMatcher
from day_10_task2_entropy import EntropyScanner
class SecretSanitizer:
    def mask_secret(self, secret: str) -> str:
        if len(secret) <= 8:
            masked = "*" * len(secret)
        else:
            masked = f"{secret[:4]}{'*' * (len(secret) - 8)}{secret[-4:]}"

        return masked
    def audit_code(self, content: str) -> dict:
        findings =SecretMatcher().scan_text(content)
        hasilentropy =EntropyScanner().scan_high_entropy_words(content)

        masked_sig=[]
        for f in findings:
            masked_sig.append({
                "rule": f["rule"],
                "line": f["line"],
                "matched": self.mask_secret(f["matched"])
            })

        masked_en=[]
        for e in hasilentropy:
            masked_en.append({
                "line": e["line"],
                "word": self.mask_secret(e["word"]),
                "entropy": e["entropy"],
            })

        total_leaks = len(masked_sig) + len(masked_en)
        is_safe = (total_leaks == 0)
        return {
            "is_safe": is_safe,
            "total_leaks": total_leaks,
            "signature_leaks": masked_sig,
            "entropy_leaks": masked_en
        }
    def enforce_security_gate(self, audit_result: dict) -> bool:
        if audit_result["is_safe"]:
            print("[PASS] Security Gate Lolos! Kode aman untuk di-push ke GitHub.")
            return True
        else:
            print("[BLOCKED] Security Gate Menggagalkan Push! Kredensial rahasia terdeteksi!")
            print(f"Total kebocoran ditemukan: {audit_result['total_leaks']}")
            
            for item in audit_result["signature_leaks"]:
                print(f"  [!] Baris {item['line']} | {item['rule']} | Nilai: {item['matched']}")
                
            for item in audit_result["entropy_leaks"]:
                print(f"  [!] Baris {item['line']} | High Entropy Token | Nilai: {item['word']} (Skor: {item['entropy']})")
            return  False

if __name__ == "__main__":
    sanitizer = SecretSanitizer()

    print("=" * 60)
    print("TEST 1: MEMINDAI KODE YANG MENGANDUNG KUNCI RAHASIA (DIRUSAK)")
    print("=" * 60)
    dirty_code = '''
import os
# Kunci AWS produksi tidak sengaja tertulis di kode
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
DATABASE_URL = "postgres://root:SuperSecretP@ssw0rd!@10.0.0.1:5432/prod"
# Token rahasia dengan entropi tinggi
internal_token = "z8K!m9#vL2$pQ0@wX5"
print("Menghubungkan ke server...")
'''
    audit_dirty = sanitizer.audit_code(dirty_code)
    sanitizer.enforce_security_gate(audit_dirty)

    print("\n" + "=" * 60)
    print("TEST 2: MEMINDAI KODE YANG SUDAH BERSIH (AMBIL DARI ENV VAR)")
    print("=" * 60)
    clean_code = '''
import os
# Kode bersih menggunakan environment variable sesuai best practice DevSecOps!
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
DATABASE_URL = os.getenv("DATABASE_URL")
internal_token = os.getenv("APP_TOKEN")
print("Menghubungkan ke server dengan aman...")
'''
    audit_clean = sanitizer.audit_code(clean_code)
    sanitizer.enforce_security_gate(audit_clean)
