import re
import json
import time
class HTTPRequest:
    def __init__(self, raw_data_string):
        self.method = ""
        self.path = ""
        self.headers = {}
        self.body = ""
        
         
        if "\r\n\r\n" in raw_data_string:
            header_part, body_part = raw_data_string.split("\r\n\r\n", 1)
        elif "\n\n" in raw_data_string:
            header_part, body_part = raw_data_string.split("\n\n", 1)
        else:
            header_part = raw_data_string
            body_part = ""
            
        self.body = body_part.strip()
        
         
        lines = header_part.strip().splitlines()
        if not lines:
            return
            
         
        first_line = lines[0].strip()
        first_space = first_line.find(" ")
        last_space = first_line.rfind(" ")
        if first_space != -1 and last_space != -1 and first_space != last_space:
            self.method = first_line[:first_space]
            self.path = first_line[first_space+1:last_space]
        elif first_space != -1:
            self.method = first_line[:first_space]
            self.path = first_line[first_space+1:]
            
         
        for line in lines[1:]:
            if ": " in line:
                key, val = line.split(": ", 1)
                self.headers[key] = val
 
 
 
import os

class MicroServer:
    def __init__(self, rate_limiter, waf_engine, audit_log_file=None):
        self.rate_limiter = rate_limiter
        self.waf_engine = waf_engine
        if audit_log_file is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.audit_log_file = os.path.join(base_dir, "audit_log.json")
        else:
            self.audit_log_file = audit_log_file
    def handle_request(self, client_ip, raw_http_data) -> tuple[int, str]:
         
        req = HTTPRequest(raw_http_data)
        
         
        if not self.rate_limiter.is_allowed(client_ip):
            self._log_audit(client_ip, req, 429, 0, ["Rate Limit Exceeded"])
            return 429, "429 Too Many Requests (Rate limit exceeded)\n"
            
         
        waf_result = self.waf_engine.inspect(req.method, req.path, req.headers, req.body)
        if waf_result["is_blocked"]:
            self._log_audit(client_ip, req, 403, waf_result["score"], waf_result["triggers"])
            return 403, f"403 Forbidden: Blocked by WAF! Triggers: {waf_result['triggers']}\n"
            
         
        if req.path == "/":
            status = 200
            response = "200 OK: Welcome to Secure API!\n"
        elif req.path == "/health":
            status = 200
            response = "200 OK: System Healthy\n"
        else:
            status = 404
            response = "404 Not Found\n"
            
         
        self._log_audit(client_ip, req, status, waf_result["score"], waf_result["triggers"])
        return status, response
    def _log_audit(self, client_ip, req, status_code, waf_score, triggers):
        """Mencatat setiap transaksi ke file audit_log.json (Append Mode)"""
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "client_ip": client_ip,
            "method": req.method,
            "path": req.path,
            "status_code": status_code,
            "waf_score": waf_score,
            "triggers": triggers
        }
        
         
        try:
            with open(self.audit_log_file, "r") as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
            
        logs.append(log_entry)
        
        with open(self.audit_log_file, "w") as f:
            json.dump(logs, f, indent=2)
