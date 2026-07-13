from pprint import pprint

from ingestion.detection.components import ExtensionValidator, HashGenerator, MetadataExtractor, MimeDetector
from ingestion.detection.pipeline import FilePipeline

from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

pipeline = FilePipeline(
    metadata_extractor=MetadataExtractor(),
    mime_detector=MimeDetector(),
    hash_generator=HashGenerator(),
    extension_validator=ExtensionValidator(),
)



def main():
    file_path = Path(r"C:\Users\ADMIN\OneDrive\Documents\chatgpt.txt")
    file_profile = pipeline.process(file_path)
    pprint(file_profile)

if __name__ == "__main__":
    main()
    