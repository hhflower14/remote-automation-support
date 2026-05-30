#!/usr/bin/env python3
"""
Small CSV cleanup utility for client demos.

Usage:
  python3 csv_cleanup.py input.csv output.csv

What it does:
  - trims whitespace in all cells
  - normalizes column names
  - removes fully empty rows
  - removes duplicate rows
  - lowercases email-like columns
"""

import csv
import re
import sys
from pathlib import Path


def normalize_header(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "column"


def clean_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def clean_csv(input_path: Path, output_path: Path) -> tuple[int, int]:
    with input_path.open("r", newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")

        headers = [normalize_header(name) for name in reader.fieldnames]
        rows = []
        seen = set()

        for raw_row in reader:
            cleaned = {}
            for original, header in zip(reader.fieldnames, headers):
                value = clean_cell(raw_row.get(original, ""))
                if "email" in header:
                    value = value.lower()
                cleaned[header] = value

            if not any(cleaned.values()):
                continue

            key = tuple(cleaned[h] for h in headers)
            if key in seen:
                continue
            seen.add(key)
            rows.append(cleaned)

    with output_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    return len(seen), len(rows)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python3 csv_cleanup.py input.csv output.csv", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    _, row_count = clean_csv(input_path, output_path)
    print(f"Cleaned {row_count} rows -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
