import re
class CTFParser:
    def cariflag(self,nama_file):
        with open(nama_file, "r")as baca:
            for line in baca:
                try:
                    dapet= re.search(r'FLAG\{.*?\}', line)
                    if dapet:
                        return dapet.group()
                except:
                    if "[CORRUPT]" in line:
                        raise ValueError("baris error")
                        continue


file =CTFParser()
print(file.cariflag("corrupted_log.txt"))
                     