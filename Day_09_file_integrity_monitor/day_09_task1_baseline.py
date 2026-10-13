import hashlib
import json
from pathlib import Path
current_dir = Path(__file__).resolve().parent

class BaseLineGenerator:
    
    def calculate_hash(self, file_path) -> str:
        self.file_path = file_path
        hasher = hashlib.sha256()
        with open(self.file_path, "rb") as f:
            while chunk := f.read(4096):
                hasher.update(chunk)

        return hasher.hexdigest()
    
    def generate(self, target_dir: str, output_json: str = "baseline.json") -> dict:
        
        base_path = Path(target_dir)
        baseline = {}
        for i in base_path.rglob("*"):
            if i.is_file():
                rel_path = str(i.relative_to(base_path))
                file_hash=self.calculate_hash(i)
                file_size = i.stat().st_size
                baseline[rel_path] ={
                    "sha256": file_hash,
                    "size_bytes": file_size
                }
        with open(current_dir/output_json, "w") as wr:
            json.dump(baseline, wr, indent=2)
        return baseline

if __name__ == "__main__":
    namafile="dummy_app"
    test_dir = Path(current_dir/namafile)
    test_dir.mkdir(exist_ok=True)
    (test_dir / "index.html").write_text("<h1>Website Aman</h1>")
    (test_dir / "app.py").write_text("print('Aplikasi berjalan')")
    (test_dir / "config.ini").write_text("port=8080\nenv=production")
    
    generator = BaseLineGenerator()
    hasil = generator.generate(current_dir/namafile, current_dir/"baseline.json")
    print("\n--- HASIL BASELINE DARI FOLDER dummy_app ---")
    print(json.dumps(hasil, indent=2))
    

