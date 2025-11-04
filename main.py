from pathlib import Path

import pandas as pd

from match import Match
from plotting_tools import create_dashboard
from settings import MATCH_DATA_DIR, MATCH_INDEX, OUTPUT_DIR


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

    return matches


def generate_all_dashboards():
    """Generate dashboards for all matches"""
    matches = load_data()

    for match_name, match in matches.items():
        print(f"\nGenerating dashboard for: {match_name}")

        # Create dashboard
        fig = create_dashboard(match, team_name="Richmond M1", opponent_name=match_name)

        # Save to output
        output_path = Path(OUTPUT_DIR) / f"{match_name.replace(' ', '_')}_dashboard.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, facecolor=fig.get_facecolor())
        print(f"Dashboard saved to: {output_path}")

        fig.clf()  # Clear figure to free memory

    return


if __name__ == "__main__":
    generate_all_dashboards()
