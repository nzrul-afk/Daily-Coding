import socket
import ssl
import datetime
class SLLWatchDog:
    def get_certificate_info(self, hostname: str, port: int = 443, timeout: float= 3.0 ) -> dict:
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=timeout) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    exp_date= datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=datetime.timezone.utc)
                    now = datetime.datetime.now(datetime.timezone.utc)
                    days_remaining = (exp_date - now).days
                    is_expired = days_remaining <= 0
                    issuer_name= cert['issuer'][1][0][1]
                    subject=cert['subject'][0][0][1]
                    san_list=cert.get('subjectAltName', [])
            return {
                "valid": True,
                "hostname": hostname,
                "days_remaining": days_remaining,
                "is_expired": is_expired,
                "expires_on": str(exp_date),
                "issuer": issuer_name,
                "san_count": len(san_list)
            }
        except ssl.SSLError as e:
            return {
                "valid": False,
                "hostname": hostname,
                "error": f"SSL/TLS Error: {e.reason if hasattr(e, 'reason') else e}",
                "days_remaining": 0,
                "is_expired": True
            }
        except (socket.timeout, TimeoutError):

            return {
                "valid": False,
                "hostname": hostname,
                "error": f"Connection Timeout ({timeout} detik)",
                "days_remaining": None,
                "is_expired": None
            }
        except Exception as e:

            return {
                "valid": False,
                "hostname": hostname,
                "error": f"Connection Error: {e}",
                "days_remaining": None,
                "is_expired": None
            }
