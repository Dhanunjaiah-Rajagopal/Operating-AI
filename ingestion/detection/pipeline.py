import logging
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
        self.logger = logging.getLogger(__name__)
        self.metadata_extractor = metadata_extractor
        self.mime_detector = mime_detector
        self.hash_generator = hash_generator
        self.extension_validator = extension_validator

    def process(self, file_path: Path) -> ProcessingResult:
        self.logger.info("Processing started: %s", file_path.name)

        try:
            metadata = self.metadata_extractor.extract(file_path)
            self.logger.info("Metadata extracted for '%s'", file_path.name)

            mime_type = self.mime_detector.detect(file_path)
            self.logger.info("MIME detected: %s", mime_type.value)

            file_hash = self.hash_generator.generate(file_path)
            self.logger.info("Hash generated for '%s': %s", file_path.name, file_hash.algorithm)

            validation_status = self.extension_validator.validate(metadata, mime_type)
            self.logger.info(
                "Validation completed for '%s': %s",
                file_path.name,
                validation_status.value,
            )

            self.logger.info("Processing completed for '%s'", file_path.name)

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
            self.logger.exception(
                "Processing failed for '%s'",
                file_path.name,
            )
            return ProcessingResult(
                file_profile=None,
                error=FileProcessingError(
                    f"Failed to process '{file_path.name}'", original_error=e
                )
            )
