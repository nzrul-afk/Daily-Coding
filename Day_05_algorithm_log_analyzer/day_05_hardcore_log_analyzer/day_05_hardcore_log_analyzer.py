class ConfigManager:
    def __init__(self, config_file):
        self.rules = {}
        with open(config_file, "r") as baca:
            for baris in baca:
                baris_bersih = baris.strip()
                pecah = baris_bersih.split("=")
                if pecah[0] == "MAX_FAILED_LOGIN":
                    self.rules[pecah[0]]=int(pecah[1])
                if pecah[0] == "BLOCKED_USER_AGENT":
                    self.rules[pecah[0]]=(pecah[1]).split(",")

class LogEntry:
    
    def __init__(self, raw_log_line):
        bersih = raw_log_line.split(" ")
        self.ip = bersih[1].replace("IP:", "")
        self.method= bersih[2].replace("METHOD:", "")
        self.path= bersih[3].replace("PATH:", "")
        self.status= bersih[4].replace("STATUS:", "")
        self.agent = bersih[5].replace("AGENT:", "")

class SecurityAnalyzer:

    def __init__(self, obj):
        self.obj = obj
        self.failed_logins = {}
        self.quarantine_ips = []
    def analyze_log(self, log_file):
        with open(log_file, "r") as log:
            for i in log:
                oi = LogEntry(i)
                for j in self.obj.rules["BLOCKED_USER_AGENT"]:
                    if j in oi.agent:
                        self.quarantine_ips.append(f"IP:{oi.ip} REASON:{oi.agent}")
                        break
                if oi.status == "401":
                    if oi.ip not in self.failed_logins:
                        self.failed_logins[oi.ip] = 0
                    else:
                        self.failed_logins[oi.ip] = self.failed_logins[oi.ip] + 1
                    if self.failed_logins[oi.ip] >= self.obj.rules["MAX_FAILED_LOGIN"]:
                        self.quarantine_ips.append(f"IP:{oi.ip} REASON:BRUCE_FORCE")

    def export_report(self, output_file):
        with open(output_file, "w") as nulis:
            nulis.write("IP_ADDRESS,REASON\n")
            for i in self.quarantine_ips:
                i = i.replace(" " , ",")
                nulis.write(f"{i}\n")

obj = ConfigManager("defense_config.ini")
print(obj.rules)
analyze = SecurityAnalyzer(obj)
analyze.analyze_log("server.log")
analyze.export_report("manuk.csv")
print("Proses selesai. Silakan cek quarantine.csv!")



