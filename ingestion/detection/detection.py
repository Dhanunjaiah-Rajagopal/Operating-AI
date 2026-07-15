from pprint import pprint

from ingestion.detection.components import ConfigurationLoader, ConfigurationProvider, ExtensionValidator, HashGenerator, MetadataExtractor, MimeDetector
from ingestion.detection.pipeline import BatchProcessor, FilePipeline

from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

config = ConfigurationProvider(ConfigurationLoader(Path("ingestion\\detection\\config.yaml"))).get_config()

pipeline = FilePipeline(
    metadata_extractor=MetadataExtractor(),
    mime_detector=MimeDetector(),
    hash_generator=HashGenerator(algorithm=config.hash_algorithm),
    extension_validator=ExtensionValidator(extension_mime_mapping=config.extension_mime_mapping),
)

batch_processor = BatchProcessor(
    pipeline=pipeline
)

def main():
    folder_path = Path(r"C:\Users\ADMIN\OneDrive\Desktop\D\Blogs")

    file_paths = [
        file_path
        for file_path in folder_path.rglob("*")
        if file_path.is_file()
    ]

    batch_result = batch_processor.process(file_paths)

    pprint(batch_result)

    print("----------------------")
    print("Total files:", batch_result.total_files)
    print("Success:", batch_result.success_count)
    print("Failed:", batch_result.failure_count)

if __name__ == "__main__":
    main()
    