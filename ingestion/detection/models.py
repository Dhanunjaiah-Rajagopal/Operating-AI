from dataclasses import dataclass
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class Metadata:
    name : str
    extension : str
    size : int
    created_time : datetime
    modified_time : datetime

@dataclass(frozen=True)
class MimeType:
    value: str

@dataclass(frozen=True)
class FileHash:
    algorithm: str
    value: str

class ValidationStatus(Enum):
    VALID = "valid"
    SUSPICIOUS = "suspicious"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class FileProfile:
    metadata: Metadata
    mime_type: MimeType
    file_hash: FileHash
    validation_status: ValidationStatus

class FileProcessingError(Exception):
    def __init__(self, message: str, original_error: BaseException):
        super().__init__(message)
        self.original_error = original_error

@dataclass(frozen=True)
class ProcessingResult:
    file_profile: FileProfile | None
    error: FileProcessingError | None