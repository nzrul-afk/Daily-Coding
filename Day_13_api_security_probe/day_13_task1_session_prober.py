import requests
from urllib.parse import urljoin
class APISessionProber:
    def __init__(self, base_url: str, timeout: float = 5.0, user_agent: str = "DevSecOps-Prober/1.0"):
        self.base_url= base_url
        self.timeout = timeout
        self.session= requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent,
            'Accept': "application/json, text/plain, */*"
        })
    def send_request(self, method: str, endpoint: str, **kwargs) -> dict:
        full_url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.request(
            method=method.upper(),
            url=full_url,    
            timeout=self.timeout,
            **kwargs,
            )
            elapsed_ms = round(response.elapsed.total_seconds() * 1000, 2)
            return {
                "success": True,
                "method": method.upper(),
                "url": full_url,
                "status_code": response.status_code,
                "elapsed_ms": elapsed_ms,
                "content_type": response.headers.get("Content-Type", ""),
                "server": response.headers.get("Server", "Hidden"),
                "error": None

            }
        except requests.exceptions.Timeout as e:
            return {
                "success": False,
                "method": method.upper(),
                "url": full_url,
                "status_code": None,
                "elapsed_ms": 0.0,
                "content_type": None,
                "server": None,
                "error": f"Timeout exceeded ({self.timeout}s): {str(e)}"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "method": method.upper(),
                "url": full_url,
                "status_code": None,
                "elapsed_ms": 0.0,
                "content_type": None,
                "server": None,
                "error": f"Request failed: {str(e)}"
            }
    def close(self):
        self.session.close()

if __name__ == "__main__":
    prober= APISessionProber("https://httpbin.org", timeout=3.0)
    res_get=prober.send_request("GET", "/get")
    print(f"[+] GET /get        : Status {res_get['status_code']} ({res_get['elapsed_ms']} ms) - Sukses: {res_get['success']}")
    res_404 = prober.send_request("GET", "/status/404")
    print(f"[+] GET /status/404 : Status {res_404['status_code']} - Sukses: {res_404['success']}")
    res_delay = prober.send_request("GET", "/delay/5")
    print(f"[-] GET /delay/5    : Sukses: {res_delay['success']} - Error: {res_delay['error']}")
    prober.close()
