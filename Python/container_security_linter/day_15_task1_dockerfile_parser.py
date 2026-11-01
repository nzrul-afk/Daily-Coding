class DockerfileParser:
    def parse_content(self, content: str) -> list:
        parsed_instructions = []
        lines=content.splitlines()
        for index, line in enumerate(lines, start=1):
            line_str=line.strip()
            if line_str.startswith("#") or  not line_str:
                continue

            parts = line_str.split(None, 1)
            instruction = parts[0].upper()

            if len(parts) > 1:
                arguments = parts[1]
            else:
                arguments = ""
            parsed_instructions.append({
                "line_number": index,
                "instruction": instruction,
                "arguments": arguments,
                "raw": line_str
            })

        return parsed_instructions
    def parse_file(self, file_path: str) -> list:
        with open(file_path, "r", encoding="utf-8") as f:
            content=f.read()
            oi =self.parse_content(content)
            return oi

if __name__ == "__main__":
    dummy_dockerfile = """
    # Setup base image
    FROM python:latest
    
    WORKDIR /app
    COPY . /app
    
    # Install library
    RUN pip install -r requirements.txt
    ENV API_KEY="***"
    EXPOSE 8080
    
    CMD ["python", "app.py"]
    """

    print("=== TEST DOCKERFILE PARSER ===")
    parser = DockerfileParser()
    hasil = parser.parse_content(dummy_dockerfile)

    print(f"Total Instruksi Terdeteksi: {len(hasil)}\n")
    print(f"{'BARIS':<8} {'INSTRUKSI':<12} {'ARGUMEN'}")
    print("-" * 50)
    for item in hasil:
        print(f"Line {item['line_number']:<3} | {item['instruction']:<10} : {item['arguments']}")
