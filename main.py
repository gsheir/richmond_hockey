from pathlib import Path

import pandas as pd

from match import Match
from settings import MATCH_DATA_DIR, MATCH_INDEX


def load_data():
    print(f"Reading match data from: {MATCH_DATA_DIR}")

    index_path = Path(MATCH_DATA_DIR) / MATCH_INDEX
    matches_info = pd.read_csv(index_path)
    matches = {}

    for _, row in matches_info.iterrows():
        if row["Coded?"] != "Yes":
            continue

        match = Match(row["JSON file name"])
        match.load_data()
        match.extract_events()
        match.count_stats()
        matches[row["Name"]] = match


if __name__ == "__main__":
    load_data()
