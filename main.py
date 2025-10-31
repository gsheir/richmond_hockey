import json
from pathlib import Path

import polars as pl

from settings import MATCH_DATA_DIR, MATCH_INDEX


def main():
    print(f"Reading match data from: {MATCH_DATA_DIR}")

    index_path = Path(MATCH_DATA_DIR) / MATCH_INDEX
    matches = pl.read_csv(index_path, try_parse_dates=True)

    for json_file in matches["JSON file name"]:
        if not isinstance(json_file, str):
            continue
        match_path = Path(MATCH_DATA_DIR) / json_file
        with open(match_path, "r") as f:
            match_data = json.load(f)

            # Placeholder
            num_events = len(match_data.get("Events", []))
            print(f"Match: {json_file}, Number of events: {num_events}")

    print(matches)


if __name__ == "__main__":
    main()
