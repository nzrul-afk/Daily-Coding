import yaml
from pathlib    import Path
class K8sManifestParser:
    def _extract_containers(self, kind: str, spec: dict) -> list:
        if kind == "Pod":
            return spec.get("containers", [])
        elif kind in ["Deployment", "StatefulSet", "DaemonSet", "Job"]:
            return spec.get("template", {}).get("spec", {}).get("containers", [])
        else:
            return []
    def parse_yaml_str(self, yaml_content: str) -> list:
        extracted=[]
        doc = yaml.safe_load_all(yaml_content)
        for i in doc:
            if i is None or not isinstance(i, dict):
                continue
            kind = i.get("kind",    "Unkown")
            metadata = i.get("metadata", {})
            name = metadata.get("name", "unnamed")
            namespace = metadata.get("namespace", "default")
            spec= i.get("spec", {})
            containers = self._extract_containers(kind, spec)

            extracted.append({
                "kind": kind,
                "name": name,
                "namespace": namespace,
                "containers": containers,
                "raw_doc": i
            })
        return extracted
    def parse_yaml_file(self, file_path: str) -> list:
        with open(file_path, "r", encoding="utf-8") as read:
            read = read.read()
            return self.parse_yaml_str(read)


if __name__ == "__main__":
    sample_k8s_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  namespace: fin-core
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: payment-api
          image: payment-api:v1.2
        - name: log-collector
          image: fluentbit:latest
---
apiVersion: v1
kind: Pod
metadata:
  name: debug-tool
  namespace: default
spec:
  containers:
    - name: net-debugger
      image: alpine:3.18
"""

    print("=== TEST KUBERNETES MANIFEST PARSER ===")
    parser = K8sManifestParser()
    manifests = parser.parse_yaml_str(sample_k8s_yaml)

    print(f"Total Dokumen K8s Terbaca: {len(manifests)}\n")
    for doc in manifests:
        print(f"[{doc['kind']}] {doc['namespace']}/{doc['name']}")
        print(f"  Jumlah Container: {len(doc['containers'])}")
        for c in doc["containers"]:
            print(f"    - Container: {c.get('name')} | Image: {c.get('image')}")
        print("-" * 50)



