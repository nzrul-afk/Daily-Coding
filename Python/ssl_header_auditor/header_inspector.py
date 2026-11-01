import http.client
class HeaderInspector:
    def __init__(self):
        self.required_headers = {
        "Strict-Transport-Security": "Mencegah downgrade serangan SSL Stripping.",
        "Content-Security-Policy": "Mencegah injeksi script berbahaya (XSS).",
        "X-Frame-Options": "Mencegah pembajakan klik (Clickjacking).",
        "X-Content-Type-Options": "Mencegah MIME-sniffing celah file palsu."
        }
    def inspect_headers(self, hostname: str, timeout: float = 3.0) -> dict:
        conn = http.client.HTTPSConnection(hostname, timeout=timeout)
        conn.request("HEAD", "/")
        response = conn.getresponse()
        raw_headers = response.getheaders()
        conn.close()
        headers_lower = {k.lower(): v for k, v in response.getheaders()}
        present_headers = []
        missing_headers = []

        for header_name, desc in self.required_headers.items():

            if header_name.lower() in headers_lower:
                present_headers.append({
                    "header": header_name,
                    "value": headers_lower[header_name.lower()],
                    "description": desc
                })
            else:
                missing_headers.append({
                    "header": header_name,
                    "description": desc
                })
        server_info = headers_lower.get("server", "Hidden / Not Disclosed")
        powered_by = headers_lower.get("x-powered-by", None)
        total_required = len(self.required_headers)
        score_percent = round((len(present_headers) / total_required) * 100, 1)

        return {
            "valid": True,
            "hostname": hostname,
            "status_code": response.status,
            "score_percent": score_percent,
            "score_summary": f"{len(present_headers)}/{total_required} Terpasang",
            "present_headers": present_headers,
            "missing_headers": missing_headers,
            "server_banner": server_info,
            "powered_by": powered_by
        }

if __name__ == "__main__":
    inspector = HeaderInspector()
    print("=== UJI OWASP SECURITY HEADERS INSPECTOR ===")
    
    for domain in ["github.com", "google.com"]:
        res = inspector.inspect_headers(domain)
        print(f"\nTarget: {res['hostname']}")
        if res["valid"]:
            print(f"[+] HTTP Status     : {res['status_code']}")
            print(f"[+] Skor Keamanan   : {res['score_percent']}% ({res['score_summary']})")
            print(f"[+] Server Banner   : {res['server_banner']}")
            
            print(f"[-] Header Terpasang ({len(res['present_headers'])}):")
            for h in res["present_headers"]:
                print(f"    ✓ {h['header']}")

            print(f"[-] Header Hilang ({len(res['missing_headers'])}):")
            for h in res["missing_headers"]:
                print(f"    ✗ {h['header']} -> {h['description']}")
        else:
            print(f"[-] Gagal Mengaudit : {res['error']}")




