import re
class SecretMatcher:
    def __init__(self):
        self.rules=[
            (
            "AWS Access Key",
            r'\b(AKIA[0-9A-Z]{16})\b'
            ),
            (
                "SSH Private Key",
                r'-----BEGIN (?:RSA|OPENSSH|DSA|EC)? ?PRIVATE KEY-----'
            ),
            (
                "Generic API / Secret Token",
                r'(?i)\b(api[_-]?key|secret[_-]?key|access[_-]?token|password)\s*=\s*[\'"][^\'"]{8,}[\'"]'
            ),
            (
                "Database Connection String",
                r'\b(?:postgres|mysql|mongodb):\/\/[a-zA-Z0-9_]+:[^@\s]+@[a-zA-Z0-9_.-]+(?::\d+)?\/[a-zA-Z0-9_.-]+'
            )
        ]
    def scan_text(self, content:str) ->list[dict]:
        findings=[]

        for index,baris in enumerate(content.splitlines(), start=1):
            for rule,pattern in self.rules:
                match=re.search(pattern, baris)
                if match:
                    findings.append({
                        "rule": rule,
                        "line": index,
                        "matched": match.group(0)
                        })
        return findings
    def scan_file(self, file_path:str) -> list[dict]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content =f.read()
            oi =self.scan_text(content)
        return oi

if __name__ == "__main__":
    from pathlib import Path
    filenya= Path(__file__).resolve().parent
    matcher = SecretMatcher()
    print(matcher.scan_file(filenya/"iya.py"))
        