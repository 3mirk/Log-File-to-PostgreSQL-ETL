import os
from datetime import datetime
from pathlib import Path
from typing import Any


def parse_scan(scan_value: str) -> datetime | None:
    scan_value = scan_value.strip()
    if not scan_value:
        return None
    return datetime.strptime(scan_value, "%Y%m%d%H%M%S")


def parse_file(filepath: str | Path) -> dict[str, Any]:
    path = Path(filepath)
    file_modified_at = datetime.fromtimestamp(os.path.getmtime(path))

    data: dict[str, Any] = {
        "file_name": path.name,
        "file_modified_at": file_modified_at,
        "job": "",
        "do_val": "",
        "blk": "",
        "blk_scan": None,
        "blk_do": "",
        "gen": "",
        "gen_scan": None,
        "gen_do": "",
        "pol": "",
        "pol_scan": None,
        "pol_do": "",
        "eng": "",
        "eng_scan": None,
        "eng_do": "",
        "dba": "",
        "dba_scan": None,
        "dba_do": "",
    }

    with path.open("r", encoding="utf-8", errors="replace") as file:
        for raw_line in file:
            line = raw_line.strip()

            if line.startswith("JOB="):
                data["job"] = line.split("=", 1)[1]
                continue

            if line.startswith("DO="):
                data["do_val"] = line.split("=", 1)[1]
                continue

            if not line.startswith("JOBRTE="):
                continue

            parts = line[len("JOBRTE=") :].split(";")
            if len(parts) < 7:
                continue

            route_do = parts[0].strip()
            tag = parts[1].strip()
            station = parts[5].strip()
            scan_dt = parse_scan(parts[6])

            if tag == "SBLK":
                data.update({"blk_do": route_do, "blk": station, "blk_scan": scan_dt})
            elif tag == "GEN":
                data.update({"gen_do": route_do, "gen": station, "gen_scan": scan_dt})
            elif tag == "POL":
                data.update({"pol_do": route_do, "pol": station, "pol_scan": scan_dt})
            elif tag == "ENG":
                data.update({"eng_do": route_do, "eng": station, "eng_scan": scan_dt})
            elif tag == "" and "DEBLOCKER" in station.upper():
                data.update({"dba_do": route_do, "dba": station, "dba_scan": scan_dt})

    return data


def should_process_file(path: str | Path) -> bool:
    path = Path(path)
    return path.is_file() and (path.suffix.lower() == ".txt" or path.suffix == "")
