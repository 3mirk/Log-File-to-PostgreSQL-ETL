import time

from watchdog.observers import Observer

from .config import settings
from .watcher import LogFileHandler, process_existing_files


def main() -> None:
    print(f"Starting LDS Log ETL watcher...")
    print(f"Monitoring folder: {settings.monitored_folder}")

    process_existing_files(settings.monitored_folder)

    observer = Observer()
    observer.schedule(LogFileHandler(), path=settings.monitored_folder, recursive=False)
    observer.start()

    print("Watcher is running. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
