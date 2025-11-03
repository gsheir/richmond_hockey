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


def generate_dashboard(match_name="Old Loughts (A)"):
    """Generate dashboard for a specific match"""
    matches = load_data()

    if match_name not in matches:
        print(f"Match '{match_name}' not found. Available matches:")
        for name in matches.keys():
            print(f"  - {name}")
        return

    match = matches[match_name]
    print(f"\nGenerating dashboard for: {match_name}")

    # Create dashboard
    fig = create_dashboard(
        match, team_name="Richmond M1", opponent_name="Old Loughtonians M1"
    )

    # Save to output
    output_path = Path(OUTPUT_DIR) / f"{match_name.replace(' ', '_')}_dashboard.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, facecolor=fig.get_facecolor())
    print(f"Dashboard saved to: {output_path}")

    return fig


if __name__ == "__main__":
    generate_dashboard()
