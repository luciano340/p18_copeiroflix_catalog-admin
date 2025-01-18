from pathlib import Path
from src._shared.logger import get_logger
from src.core._shared.infrrastrructure.storage_service_interface import StorageServiceInterface


class LocalStorage(StorageServiceInterface):
    TMP_BUCKET="C:/Users/Luciano Romão/projetos/volumes"
    def __init__(self, bucket: str = TMP_BUCKET) -> None:
        self.bucket = Path(bucket)
        self.logger = get_logger(__name__)

        if not self.bucket.exists():
            self.bucket.mkdir(parents=True)

        self.logger.debug(f'instância iniciada com {self.bucket}')

    def store(self, path: str, content: bytes, type: str) -> None:
        full_path = Path(f"{self.bucket}/{path}")
        self.logger.info(f"Iniciando upload para {full_path}")
        if not full_path.parent.exists():
            self.logger.debug(f"criando diretório")
            full_path.parent.mkdir(parents=True)
        
        with open(full_path, "wb") as file:
            file.write(content)
        self.logger.info('Escrita finalizada')
        
        