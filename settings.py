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
    "large": 20,
    "medium": 11,
    "small": 8,
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

STD_MARGIN = 0.02
# Coordinates defined as (left, bottom, width, height)
ELEMENT_COORDINATES = {
    "logo_position": (
        CANVAS_LEFT,
        CONTENT_TOP - 0.5 * LOGO_SIZE,
        LOGO_SIZE,
        LOGO_SIZE,
    ),
    "result_position": (CONTENT_LEFT, 0.7, 0.075, 0.09),
    "period_scores_position": (CONTENT_LEFT + 0.1, 0.7, 0.16, 0.12),
    "quarter_stats_for_position": (CONTENT_LEFT, 0.42, 0.12, 0.35),
    "quarter_stats_against_position": (CONTENT_LEFT + 0.13, 0.42, 0.12, 0.35),
    "overall_stats_position": (CONTENT_LEFT + 0.26, 0.42, 0.18, 0.35),
    "pc_position": (CONTENT_LEFT + 0.45, 0.42, 0.18, 0.35),
    "circle_position": (0.65, 0.05, 0.3, 0.3),
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
