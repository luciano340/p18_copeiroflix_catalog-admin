from pathlib import Path
from src.core._shared.infra.storage.storage_service_interface import StorageServiceInterface


class LocalStorage(StorageServiceInterface):
    TMP_BUCKET="C:/Users/Luciano Romão/projetos/volumes"
    def __init__(self, bucket: str = TMP_BUCKET) -> None:
        self.bucket = Path(bucket)

        if not self.bucket.exists():
            self.bucket.mkdir(parents=True)

    def store(self, path: str, content: bytes, type: str) -> None:
        full_path = Path(f"{self.bucket}/{path}")
        if not full_path.parent.exists():
            full_path.parent.mkdir(parents=True)
        
        with open(full_path, "wb") as file:
            file.write(content)
        