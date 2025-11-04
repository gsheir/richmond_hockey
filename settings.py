import os

from dotenv import load_dotenv

load_dotenv()

MATCH_DATA_DIR = os.environ.get("MATCH_DATA_DIR", "/default/path/to/match_data")

MATCH_INDEX = "matches.csv"

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/default/path/to/output")

COLOURS = {
    "Richmond red": "#660000",
    "White": "#FFFFFF",
    "Black": "#000000",
    "Light green": "#63EF63",
    "Light pink": "#FF8799",
    "Grey": "#7B7B7B",
    "Light yellow": "#FFFACD",
}
FONT_SIZES = {
    "title": 24,
    "large": 16,
    "medium": 12,
    "small": 10,
}

FIG_SIZE = (16, 9)

CANVAS_TOP = 1.0
CANVAS_BOTTOM = 0.0
CANVAS_LEFT = 0.0
CANVAS_RIGHT = 1.0

TITLE_HEIGHT = 0.1

CONTENT_TOP = 1 - TITLE_HEIGHT
CONTENT_BOTTOM = 0.05
CONTENT_LEFT = 0.05
CONTENT_RIGHT = 0.95

LOGO_SIZE = 0.14  # Proportion of figure height

STD_GAP = 0.02
STD_HEIGHT = 0.04
STD_WIDTH = 0.04

V_ANCHOR_0 = CONTENT_LEFT + 0.08
V_ANCHOR_1 = CONTENT_LEFT + 0.42

PC_WIDTH = 6
PC_HEIGHT = 7

CIRCLE_WIDTH = 6
CIRCLE_HEIGHT = 10

OVERALL_HEIGHT = 10
OVERALL_WIDTH = 5

# Coordinates defined as (left, bottom, width, height)
ELEMENT_COORDINATES = {
    "logo_position": (
        CANVAS_LEFT,
        CONTENT_TOP - 0.5 * LOGO_SIZE,
        LOGO_SIZE,
        LOGO_SIZE,
    ),
    "result_position": (
        V_ANCHOR_0 - 2 * STD_WIDTH - STD_GAP,
        0.7,
        2 * STD_WIDTH,
        2 * STD_HEIGHT,
    ),
    "period_scores_position": (
        V_ANCHOR_0 + 0.5 * STD_WIDTH,
        0.7 - STD_HEIGHT,
        4 * STD_WIDTH,
        3 * STD_HEIGHT,
    ),
    "overall_stats_position": (
        V_ANCHOR_0,
        0.18,
        OVERALL_WIDTH * STD_WIDTH,
        OVERALL_HEIGHT * STD_HEIGHT,
    ),
    "quarter_stats_for_position": (
        V_ANCHOR_0 - 2 * STD_WIDTH - STD_GAP,
        0.3 + 2 * STD_HEIGHT,
        4 / 2 * STD_WIDTH,
        5 * STD_HEIGHT,
    ),
    "quarter_stats_against_position": (
        V_ANCHOR_0 + 5 * STD_WIDTH + STD_GAP,
        0.3 + 2 * STD_HEIGHT,
        4 / 2 * STD_WIDTH,
        5 * STD_HEIGHT,
    ),
    "pca_position": (
        V_ANCHOR_1,
        0.6,
        PC_WIDTH * STD_WIDTH,
        PC_HEIGHT * STD_HEIGHT,
    ),
    "pcd_position": (
        V_ANCHOR_1 + PC_WIDTH * STD_WIDTH + STD_GAP,
        0.6,
        PC_WIDTH * STD_WIDTH,
        PC_HEIGHT * STD_HEIGHT,
    ),
    "circle_att_position": (
        V_ANCHOR_1,
        0.1,
        CIRCLE_WIDTH * STD_WIDTH,
        CIRCLE_HEIGHT * STD_HEIGHT,
    ),
    "circle_def_position": (
        V_ANCHOR_1 + PC_WIDTH * STD_WIDTH + STD_GAP,
        0.1,
        CIRCLE_WIDTH * STD_WIDTH,
        CIRCLE_HEIGHT * STD_HEIGHT,
    ),
}

# Line widths
LINE_WIDTHS = {
    "thin": 1,
    "thick": 2,
}

# Box dimensions and padding
BOX_DIMENSIONS = {
    "padding": 0.02,
    "border_radius": "round,pad=0.02",
}

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
