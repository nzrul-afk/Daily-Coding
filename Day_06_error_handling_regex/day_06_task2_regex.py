import re
class DataExtractor:
    def extract_ip(self, text):
        hasil = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text)
        if hasil:
            return hasil.group()
        else:
            return "IP tidak ditemukan"

    def extract_email(self, text):
        hasil = re.search(r'[a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-zA-Z]+', text)
        if hasil:
            return hasil.group()
        else:
            return "email tidak ditemukan"

extractor = DataExtractor()
print(extractor.extract_ip("Telah terjadi serangan dari IP 192.168.10.25 pada malam hari."))
print(extractor.extract_email("Hubungi admin di admin_server123@gmail.com segera!"))


  