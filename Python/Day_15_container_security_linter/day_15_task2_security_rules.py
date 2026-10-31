from day_15_task1_dockerfile_parser import DockerfileParser
class SecurityRulesEngine:
    def __init__(self):
        self.secret_keywords = ["KEY", "SECRET", "PASSWORD", "TOKEN", "PASSWD"]
    def lint(self, instructions: list) -> list:
        findings = []
        has_user = False
        has_healthcheck = False
        for inst in instructions:
            name = inst["instruction"]
            args = inst["arguments"]
            line = inst["line_number"]
            if name == 'FROM':
                image_name = args.split()[0].lower() if args else ""
                if ":latest" in image_name or (":" not in image_name and image_name != "scratch"):
                    findings.append({
                        "rule_id": "CIS-DI-001",
                        "severity": "MEDIUM",
                        "line_number": line,
                        "instruction": name,
                        "message": f"Hindari tag :latest atau image tanpa versi ('{args}'). Gunakan versi spesifik."
                    })
            elif name in ["ENV", "ARG"]:
                for kw in self.secret_keywords:
                    if kw in args.upper():
                        findings.append({
                            "rule_id": "CIS-DI-002",
                            "severity": "HIGH",
                            "line_number": line,
                            "instruction": name,
                            "message": f"Ditemukan potensi secret/kredensial ('{kw}') di dalam {name}. Gunakan Secret Management!"
                        })
                        break
            if name == "USER":
                if args.strip() not in ["root", "0"]:
                    has_user = True
            elif name == "HEALTHCHECK":
                has_healthcheck = True

        if not has_user:
            findings.append({
                "rule_id": "CIS-DI-003",
                "severity": "HIGH",
                "line_number": None,
                "instruction": "USER",
                "message": "Instruksi 'USER' non-root tidak ditemukan! Container berjalan sebagai root (berbahaya)."
            })

        if not has_healthcheck:
            findings.append({
                "rule_id": "CIS-DI-004",
                "severity": "LOW",
                "line_number": None,
                "instruction": "HEALTHCHECK",
                "message": "Instruksi 'HEALTHCHECK' tidak ditemukan. Tambahkan agar status container dapat dipantau."
            })

        return findings

if __name__ == "__main__":
    dummy_dockerfile = """
    # Dockerfile Rentan Keamanan
    FROM python:latest
    WORKDIR /app
    COPY . /app
    RUN pip install -r requirements.txt
    ENV API_KEY="***"
    EXPOSE 8080
    CMD ["python", "app.py"]
    """

    print("=== TEST SECURITY RULES ENGINE ===")
    parser = DockerfileParser()
    parsed_data = parser.parse_content(dummy_dockerfile)

    engine = SecurityRulesEngine()
    hasil_audit = engine.lint(parsed_data)

    print(f"Total Temuan Pelanggaran: {len(hasil_audit)}\n")
    for item in hasil_audit:
        baris_str = f"Line {item['line_number']}" if item['line_number'] else "Global"
        print(f"[{item['severity']:<6}] {item['rule_id']} ({baris_str}) : {item['message']}")


                                        
