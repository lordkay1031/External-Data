"""Convert a JSON file to a CSV file based on column names."""

import argparse
import csv
import json
import sys


def json_to_csv(input_path: str, output_path: str, columns: list[str] | None = None) -> None:
    """Read a JSON file and write its contents to a CSV file.

    Args:
        input_path: Path to the input JSON file. The file must contain a list of objects.
        output_path: Path to the output CSV file to create.
        columns: Optional list of column names to include (in order). If not provided,
                 all keys from the first record are used.

    Raises:
        ValueError: If the JSON file does not contain a list of objects.
    """
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON file must contain a list of objects.")

    fieldnames = columns if columns else (list(data[0].keys()) if data else [])

    if not data:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if fieldnames:
                writer.writeheader()
        return

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a JSON file to a CSV file.")
    parser.add_argument("input", help="Path to the input JSON file.")
    parser.add_argument("output", help="Path to the output CSV file.")
    parser.add_argument(
        "--columns",
        nargs="+",
        metavar="COLUMN",
        help="Column names to include in the CSV (in order). "
             "Defaults to all keys in the first JSON record.",
    )
    args = parser.parse_args()

    try:
        json_to_csv(args.input, args.output, args.columns)
        print(f"Converted '{args.input}' -> '{args.output}'")
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
