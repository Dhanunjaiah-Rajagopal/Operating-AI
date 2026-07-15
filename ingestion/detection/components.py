from datetime import datetime, timezone
import hashlib
import logging
from pathlib import Path

import magic
import yaml
from ingestion.detection.models import ApplicationConfig, FileHash, Metadata, MimeType, ValidationStatus


class MetadataExtractor:
    def extract(self, file_path: Path) -> Metadata:
        stats = file_path.stat()
        return Metadata(
            name=file_path.name,
            extension=file_path.suffix,
            size=stats.st_size,
            created_time=datetime.fromtimestamp(stats.st_ctime, tz=timezone.utc),
            modified_time=datetime.fromtimestamp(stats.st_mtime, tz=timezone.utc)
        )

class MimeDetector:
    def detect(self, file_path: Path) -> MimeType:
        mime_type = magic.from_file(str(file_path), mime=True)
        return MimeType(value=mime_type)
    
class HashGenerator:
    def __init__(self, algorithm: str):
        self.algorithm = algorithm
        
        if not hasattr(hashlib, self.algorithm):
            raise ValueError(
                f"Unsupported hash algorithm: {self.algorithm}"
            )

    def generate(self, file_path: Path) -> FileHash:
        hasher = getattr(hashlib, self.algorithm)()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return FileHash(algorithm=self.algorithm, value=hasher.hexdigest())

class ExtensionValidator:
    def __init__(self, extension_mime_mapping: dict[str, str]):
        self.extension_mime_mapping = extension_mime_mapping

    def validate(self, metadata: Metadata, mime_type: MimeType) -> ValidationStatus:
        expected_mime = self.extension_mime_mapping.get(metadata.extension.lower())
        if expected_mime is None:
            return ValidationStatus.UNKNOWN
        if expected_mime == mime_type.value:
            return ValidationStatus.VALID
        
        return ValidationStatus.SUSPICIOUS

class ConfigurationLoader:
    def __init__(self, config_path: Path):
        self.config_path = config_path

    def load(self) -> ApplicationConfig:
        with open(self.config_path, "r") as file:
            data = yaml.safe_load(file)

        return ApplicationConfig(
            extension_mime_mapping=data["extension_mime_mapping"],
            hash_algorithm=data["hash_algorithm"],
        )

class ConfigurationProvider:
    def __init__(self, loader: ConfigurationLoader):
        self.loader = loader
        self.logger = logging.getLogger(__name__)

        self.config = loader.load()
        self.last_modified = loader.config_path.stat().st_mtime

    def get_config(self) -> ApplicationConfig:
        return self.config

    def reload_if_changed(self):
        current_modified = self.loader.config_path.stat().st_mtime

        if current_modified != self.last_modified:
            self.logger.info("Configuration change detected. Reloading configuration.")

            try:
                new_config = self.loader.load()

            except Exception:
                self.logger.exception(
                    "Failed to reload configuration. Keeping existing configuration."
                )

            else:
                self.config = new_config
                self.last_modified = current_modified

                self.logger.info(
                    "Configuration reloaded successfully."
                )