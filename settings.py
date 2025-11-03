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
    "Light green": "#90EE90",
    "Light pink": "#FFB6C1",
    "Beige": "#F5F5DC",
    "Light yellow": "#FFFACD",
}

FONT_SIZES = {
    "title": 24,
    "subtitle": 18,
    "text": 14,
    "small_text": 10,
    "tiny": 6,
    "extra_small": 7,
    "small": 8,
    "medium_small": 9,
    "medium": 11,
    "medium_large": 12,
    "large": 13,
    "extra_large": 20,
}

FIG_SIZE = (16, 9)

# Coordinates defined with 0,0 at top-left and 1,1 at bottom-right
ELEMENT_COORDINATES = {
    "title_height": 0.1,
    "result_position": (0.12, 0.05),
    "logo_position": (0.01, 0.935, 0.08, 0.055),
    "period_scores_position": (0.115, 0.815, 0.23, 0.09),
    "quarter_stats_position": (0.025, 0.42, 0.12, 0.35),
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
