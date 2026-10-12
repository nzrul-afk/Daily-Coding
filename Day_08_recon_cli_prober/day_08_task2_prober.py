import platform
import subprocess
os_name= platform.system()
class SystemProber:
    def ping(self, target: str, count: int = 2, timeout: int = 5) -> dict:
        if os_name == "Windows":
            perintah = ["ping", "-n", str(count), target]
        if os_name == "Linux":
            perintah = ["ping", "-c", str(count), target]
        hasil = subprocess.run(
            perintah,
            capture_output=True,
            text=True,
            timeout=5
            )
        return {
                "target": target,
                "alive": True if hasil.returncode == 0 else False,
                "exit_code": hasil.returncode,
                "output": hasil.stdout,
                "summary": "Host UP / Responsive" if hasil.returncode == 0 else "Host DOWN / Timeout"
        }
    def check_dns(self, domain: str, timeoutnya: int = 5) -> dict:
        perintah = ["nslookup", domain]
        hasil = subprocess.run (
            perintah,
            capture_output=True,
            text=True,
            timeout=timeoutnya
        )
        return {
            "domain" : domain,
            "resolved" : True if hasil.returncode == 0 else False,
            "output": hasil.stdout,
            "summary": "DNS Resolved successfully" if hasil.returncode == 0 else "DNS Resolution Failed"
        }
if __name__ == "__main__":
    prober = SystemProber()

    print("--- 1. TES PING HOST HIDUP (127.0.0.1) ---")
    res1 = prober.ping("127.0.0.1", count=2)
    print(f"Target : {res1['target']}")
    print(f"Alive  : {res1['alive']}")
    print(f"Code   : {res1['exit_code']}")
    print(f"Summary: {res1['summary']}\n")

    print("--- 2. TES PING HOST MATI (192.0.2.1) ---")
    res2 = prober.ping("192.0.2.1", count=1, timeout=3)
    print(f"Target : {res2['target']}")
    print(f"Alive  : {res2['alive']}")
    print(f"Code   : {res2['exit_code']}")
    print(f"Summary: {res2['summary']}\n")

    print("--- 3. TES DNS RESOLVE (google.com) ---")
    res3 = prober.check_dns("google.com")
    print(f"Domain : {res3['domain']}")
    print(f"Resolved: {res3['resolved']}")
    print(f"Summary: {res3['summary']}")

