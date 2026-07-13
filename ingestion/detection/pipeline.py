from pathlib import Path

from ingestion.detection.components import (
    ExtensionValidator,
    HashGenerator,
    MetadataExtractor,
    MimeDetector,
)
from ingestion.detection.models import (
    FileProcessingError,
    FileProfile,
    ProcessingResult,
)


class FilePipeline:
    def __init__(
        self,
        metadata_extractor: MetadataExtractor,
        mime_detector: MimeDetector,
        hash_generator: HashGenerator,
        extension_validator: ExtensionValidator,
    ):
        self.metadata_extractor = metadata_extractor
        self.mime_detector = mime_detector
        self.hash_generator = hash_generator
        self.extension_validator = extension_validator

    def process(self, file_path: Path) -> ProcessingResult:
        try:
            metadata = self.metadata_extractor.extract(file_path)
            mime_type = self.mime_detector.detect(file_path)
            file_hash = self.hash_generator.generate(file_path)
            validation_status = self.extension_validator.validate(metadata, mime_type)

            return ProcessingResult(
                file_profile=FileProfile(
                    metadata=metadata,
                    mime_type=mime_type,
                    file_hash=file_hash,
                    validation_status=validation_status,
                ),
                error=None,
            )
        except (FileNotFoundError, PermissionError, OSError) as e:
            return ProcessingResult(
                file_profile=None,
                error=FileProcessingError(
                    f"Failed to process '{file_path.name}'", original_error=e
                )
            )
