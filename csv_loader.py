"""Reading CSV files into flight records and error messages."""
import csv
import os

from validator import validate_row, to_record

def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    """Process the CSV files in the order given.

    Return (records, errors):
      records - valid flight records, in input order
      errors  - one message per invalid row, in input order, formatted as
                "<file name>:<line number>: <ERROR_CODE> | <free text>"
                (base file name only, no timestamp or level, no newline)

    Also performs the DUPLICATE_FLIGHT check across all the files.
    Does not write any files and does not log anything itself.
    """
    records = []
    errors = []
    seen = set()
    for path in paths:
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                stripped = line.strip()
                if lineno == 1 or not stripped or stripped.startswith("#"):
                    continue
                fields = next(csv.reader([line]))
                code = validate_row(fields, airports)
                if code is not None:
                    errors.append(f"{name}:{lineno}: {code} | {stripped}")
                    continue
                record = to_record(fields)
                key = (record["flight_id"], record["departure_datetime"])
                if key in seen:
                    errors.append(f"{name}:{lineno}: DUPLICATE_FLIGHT | {stripped}")
                    continue
                seen.add(key)
                records.append(record)
    return records, errors
    
