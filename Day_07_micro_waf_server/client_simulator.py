import time
from rate_limiter import Rate_Limiter
from waf_engine import WAFengine
from micro_server import MicroServer

def run_simulation():
    print("=" * 60)
    print("🚀 MEMULAI SIMULASI KEAMANAN WAF & MICRO SERVER (DAY 07)")
    print("=" * 60)

    limiter = Rate_Limiter(maxRequest=3, window_seconds=2)
    waf = WAFengine(score_threshold=5)
    server = MicroServer(limiter, waf)


    print("\n[TEST 1] Mengirim Request Normal (User Biasa)...")
    req_normal = (
        "GET / HTTP/1.1\r\n"
        "Host: localhost:8080\r\n"
        "User-Agent: Mozilla/5.0 (Windows NT 10.0)\r\n"
        "\r\n"
    )
    status, response = server.handle_request("192.168.1.10", req_normal)
    print(f"Hasil -> HTTP {status} | Pesan: {response.strip()}")

    print("\n[TEST 2] Mengirim Serangan SQL Injection di URL...")
    req_sqli = (
        "GET /products?id=1' OR 1=1 -- HTTP/1.1\r\n"
        "Host: localhost:8080\r\n"
        "User-Agent: sqlmap/1.5\r\n"
        "\r\n"
    )
    status, response = server.handle_request("10.0.0.5", req_sqli)
    print(f"Hasil -> HTTP {status} | Pesan: {response.strip()}")

    print("\n[TEST 3] Mengirim Serangan Path Traversal...")
    req_traversal = (
        "GET /images/../../etc/passwd HTTP/1.1\r\n"
        "Host: localhost:8080\r\n"
        "User-Agent: curl/7.68.0\r\n"
        "\r\n"
    )
    status, response = server.handle_request("10.0.0.6", req_traversal)
    print(f"Hasil -> HTTP {status} | Pesan: {response.strip()}")

    print("\n[TEST 4] Mengirim Serangan XSS di Payload Body...")
    req_xss = (
        "POST /comment HTTP/1.1\r\n"
        "Host: localhost:8080\r\n"
        "Content-Type: application/json\r\n"
        "\r\n"
        "<script>alert('HACKED')</script>"
    )
    status, response = server.handle_request("10.0.0.7", req_xss)
    print(f"Hasil -> HTTP {status} | Pesan: {response.strip()}")

    print("\n[TEST 5] Menguji Serangan Spam / Brute Force (5 Request Cepat)...")
    ip_spammer = "172.16.0.99"
    req_spam = (
        "GET /health HTTP/1.1\r\n"
        "Host: localhost:8080\r\n"
        "\r\n"
    )

    for i in range(1, 6):
        status, response = server.handle_request(ip_spammer, req_spam)
        print(f"  Request #{i} -> HTTP {status} | {response.strip()}")
        time.sleep(0.05)

    print("\n" + "=" * 60)
    print("✅ SIMULASI SELESAI! Silakan periksa file Day_07/audit_log.json")
    print("=" * 60)

if __name__ == "__main__":
    run_simulation()
