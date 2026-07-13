from datetime import datetime, timezone
import hashlib
from pathlib import Path

import magic

from ingestion.detection.models import FileHash, Metadata, MimeType, ValidationStatus


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
    def generate(self, file_path: Path, algorithm: str = 'sha256') -> FileHash:
        hasher = getattr(hashlib, algorithm)()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return FileHash(algorithm=algorithm, value=hasher.hexdigest())

EXTENSION_MIME_MAPPING = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".pdf": "application/pdf",
    ".txt": "text/plain"
}

class ExtensionValidator:
    def validate(self, metadata: Metadata, mime_type: MimeType) -> ValidationStatus:
        expected_mime = EXTENSION_MIME_MAPPING.get(metadata.extension.lower())
        if expected_mime is None:
            return ValidationStatus.UNKNOWN
        if expected_mime == mime_type.value:
            return ValidationStatus.VALID
        
        return ValidationStatus.SUSPICIOUS

