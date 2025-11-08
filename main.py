import argparse
from pathlib import Path

import pandas as pd

from match import Match
from plotting_tools import create_dashboard
from settings import MATCH_DATA_DIR, MATCH_INDEX, OUTPUT_DIR


def load_data(match_data_dir=None, match_index=None):
    # Use provided directories or fall back to settings
    data_dir = match_data_dir or MATCH_DATA_DIR
    index_file = match_index or MATCH_INDEX

    print(f"Reading match data from: {data_dir}")

    index_path = Path(data_dir) / index_file
    matches_info = pd.read_csv(index_path)
    matches = {}

    for _, row in matches_info.iterrows():
        if row["Coded?"] != "Yes":
            continue

        match = Match(row["JSON file name"], match_data_dir=data_dir)
        match.load_data()
        match.extract_events()
        match.count_stats()
        matches[row["Name"]] = match

    return matches


def generate_all_dashboards(match_data_dir=None, match_index=None, output_dir=None):
    """Generate dashboards for all matches"""
    # Use provided directories or fall back to settings
    out_dir = output_dir or OUTPUT_DIR

    matches = load_data(match_data_dir, match_index)

    for match_name, match in matches.items():
        print(f"\nGenerating dashboard for: {match_name}")

        # Create dashboard
        fig = create_dashboard(match, team_name="Richmond M1", opponent_name=match_name)

        # Save to output
        output_path = Path(out_dir) / f"{match_name.replace(' ', '_')}_dashboard.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, facecolor=fig.get_facecolor())
        print(f"Dashboard saved to: {output_path}")

        fig.clf()  # Clear figure to free memory

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate hockey match dashboards")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run in demo mode using demo/data and saving to demo/output",
    )

    args = parser.parse_args()

    if args.demo:
        # Get the script's directory and construct demo paths
        script_dir = Path(__file__).parent
        demo_data_dir = script_dir / "demo" / "data"
        demo_output_dir = script_dir / "demo" / "output"

        print("Running in DEMO mode")
        print(f"Demo data directory: {demo_data_dir}")
        print(f"Demo output directory: {demo_output_dir}")

        generate_all_dashboards(
            match_data_dir=str(demo_data_dir),
            match_index="matches.csv",
            output_dir=str(demo_output_dir),
        )
    else:
        generate_all_dashboards()
