from pprint import pprint

from pathlib import Path
import logging

from ingestion.detection.pipeline import create_detection_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def main():
    batch_processor = create_detection_pipeline()
    folder_path = Path(r"C:\Users\ADMIN\OneDrive\Desktop\D\Blogs")

    file_paths = [
        file_path for file_path in folder_path.rglob("*") if file_path.is_file()
    ]

    batch_result = batch_processor.process(file_paths)

    pprint(batch_result)

    print("----------------------")
    print("Total files:", batch_result.total_files)
    print("Success:", batch_result.success_count)
    print("Failed:", batch_result.failure_count)


if __name__ == "__main__":
    main()
