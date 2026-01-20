import os

from dotenv import load_dotenv

load_dotenv()

MATCH_DATA_DIR = os.environ.get("MATCH_DATA_DIR", "/default/path/to/match_data")

MATCH_INDEX = "matches.csv"

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/default/path/to/output")


TAG_NAMES = {
    # Outcomes
    "goal": ["Goal"],
    "ph2_goal": ["Ph2 Goal", "Phase 2 Goal"],
    "reawarded": ["Reaward"],
    "saved": ["Saved"],
    "recycled": ["Recycled"],
    "miss": ["Miss"],
    "turnover": ["Turnover"],
    "upgrade": ["Upgrade"],
    # Penalty corners
    "left": ["Left Castle"],
    "right": ["Right Castle"],
    "straight": ["Straight", "Straight Flick", "Straight Strike"],
    "variation": ["Variation"],
    # Circle entry positions
    "left_baseline": ["Left Baseline"],
    "l45": ["L45", "Left"],
    "centre": ["Centre", "Central"],
    "r45": ["R45", "Right"],
    "right_baseline": ["Right Baseline"],
}

EVENT_NAMES = {
    "Own Half Restarts": {
        "att": "Own Half Restart ATT",
        "def": "Own Half Restart DEF",
    },
    "23 Entries": {
        "att": "23 Entry ATT",
        "def": "23 Entry DEF",
    },
    "Circle Entries": {
        "att": "Circle Entry ATT",
        "def": "Circle Entry DEF",
    },
    "Penalty Corners": {
        "att": "PCA",
        "def": "PCD",
    },
    "Penalty Strokes": {
        "att": "Stroke ATT",
        "def": "Stroke DEF",
    },
    "Goals": {
        "att": "Goal FOR",
        "def": "Goal AGAINST",
    },
    "Green Cards": {
        "att": "GC Man Down",
        "def": "GC Man Up",
    },
    "Yellow Cards": {
        "att": "YC Man Down",
        "def": "YC Man Up",
    },
    "Red Cards": {
        "att": "RC Man Down",
        "def": "RC Man Up",
    },
}
