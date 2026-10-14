import collections
import math
class EntropyScanner:
    def calculate_entropy(self, text:str) -> float:
        if len(text) == 0:
            return 0
        count=collections.Counter(text)
        entropy = 0.0
        for c in count.values():
            p = c / len(text)
            entropy -= p * math.log2(p)
        return round(entropy, 3)
    def scan_high_entropy_words(self, content: str, threshold: float = 3.5, min_length: int = 12) -> list[dict]:
        found=[]
        import re
        for index, line in enumerate(content.splitlines(), start=1):
            # Abaikan baris komentar atau baris import
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("import ") or stripped.startswith("from "):
                continue

            # Cari teks yang ada di dalam tanda petik (string literal)
            string_literals = re.findall(r'["\']([^"\']+)["\']', line)

            for clean_word in string_literals:
                # Abaikan kalimat biasa yang mengandung spasi
                if " " in clean_word:
                    continue

                # Abaikan path import biasa atau variabel env
                if clean_word.isupper() and "_" in clean_word:
                    continue

                if len(clean_word) >= min_length:
                    skor = self.calculate_entropy(clean_word)
                    if skor >= threshold:
                        found.append({
                            "line": index,
                            "word": clean_word,
                            "entropy": skor
                        })
        return found
