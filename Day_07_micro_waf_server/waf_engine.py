import re
class WAFengine:
    def __init__(self, score_threshold=5):
        self.score_threshold=score_threshold
        
        self.rules = [
            (r'(\.\./|\.\.\\)', "Path Traversal", 5),
            (r"(\b(UNION|SELECT|INSERT|DELETE|DROP)\b|--|['\"]\s*OR\b|\bOR\b\s+[\w\d]+\s*=\s*[\w\d]+)", "SQL Injection", 5),
            (r'([;&|`]\s*(cat|ls|whoami|sh|bash|curl|wget))', "Command Injection", 5),
            (r'(<script.*?>|javascript:|onload=|onerror=)', "Cross-Site Scripting (XSS)", 5)
        ]
    def inspect(self, method, path, headers, body) -> dict:
        gabungan = f"{path} {body}"
        score = 0
        triggers = []
        for pattern, rule_name, rule_score in self.rules:
            if re.search(pattern, gabungan, re.I):
                score += rule_score
                triggers.append(rule_name)
        is_blocked = score >= self.score_threshold
        return {
            "is_blocked": is_blocked,
            "score": score,
            "triggers": triggers
        }
