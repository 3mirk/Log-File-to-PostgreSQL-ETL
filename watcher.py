import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler

from .config import settings
from .db import insert_job_entry, load_processed_keys
from .parser import parse_file, should_process_file


def process_one_file(path: str | Path) -> None:
    data = parse_file(path)
    insert_job_entry(data)
    print(f"Processed: {data['file_name']} | {data['file_modified_at']}")


def process_existing_files(monitored_folder: str | Path) -> None:
    folder = Path(monitored_folder)
    processed = load_processed_keys()

    for path in folder.iterdir():
        if not should_process_file(path):
            continue

        data = parse_file(path)
        key = (data["file_name"], data["file_modified_at"])

        if key in processed:
            continue

        insert_job_entry(data)
        print(f"Backfilled: {data['file_name']} | {data['file_modified_at']}")


class LogFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not should_process_file(event.src_path):
            return

        time.sleep(settings.file_settle_seconds)

        try:
            process_one_file(event.src_path)
        except Exception as exc:
            print(f"Error processing {event.src_path}: {exc}")
