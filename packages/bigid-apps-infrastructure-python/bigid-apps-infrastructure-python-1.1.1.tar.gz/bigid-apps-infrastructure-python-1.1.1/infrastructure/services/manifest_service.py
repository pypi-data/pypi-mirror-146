import os


class ManifestService:
    def __init__(self, manifest_path: str):
        self.manifest_path = manifest_path

    def manifest(self):
        cwd = os.getcwd()
        return open(cwd + self.manifest_path, "rt").read()
