from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyBboxPatch, Rectangle

from settings import (
    BOX_DIMENSIONS,
    CANVAS_LEFT,
    CANVAS_RIGHT,
    CIRCLE_HEIGHT,
    CIRCLE_WIDTH,
    COLOURS,
    ELEMENT_COORDINATES,
    EVENT_NAMES,
    FIG_SIZE,
    FONT_SIZES,
    LINE_WIDTHS,
    OVERALL_HEIGHT,
    OVERALL_WIDTH,
    PC_HEIGHT,
    PC_WIDTH,
    TITLE_HEIGHT,
)


def interpolate_color(value, min_val, max_val, min_color, max_color):
    """Interpolate between two colors based on value between min and max"""
    if max_val == min_val:
        return min_color

    # Convert hex colors to RGB
    min_rgb = np.array(to_rgb(min_color))
    max_rgb = np.array(to_rgb(max_color))

    # Calculate the interpolation factor (0 to 1)
    factor = (value - min_val) / (max_val - min_val)
    factor = np.clip(factor, 0, 1)

    # Interpolate
    interp_rgb = min_rgb + factor * (max_rgb - min_rgb)

    # Convert back to hex
    return "#{:02x}{:02x}{:02x}".format(
        int(interp_rgb[0] * 255), int(interp_rgb[1] * 255), int(interp_rgb[2] * 255)
    )


def create_dashboard(match, team_name="Richmond M1", opponent_name="Opponent"):
    """Create a complete match dashboard"""
    # Create figure with dark red background
    fig = plt.figure(figsize=FIG_SIZE)
    fig.patch.set_facecolor(COLOURS["Richmond red"])

    # Add black title bar at the top
    title_ax = fig.add_axes([CANVAS_LEFT, 1 - TITLE_HEIGHT, CANVAS_RIGHT, TITLE_HEIGHT])
    title_ax.set_xlim(0, 1)
    title_ax.set_ylim(0, 1)
    title_ax.axis("off")
    title_ax.add_patch(
        Rectangle((0, 0), 1, 1, facecolor=COLOURS["Black"], edgecolor="none")
    )

    # Add logo
    logo_path = Path("images/richmond_logo.png")
    if logo_path.exists():
        logo_img = mpimg.imread(logo_path)
        logo_ax = fig.add_axes(ELEMENT_COORDINATES["logo_position"])
        logo_ax.imshow(logo_img)
        logo_ax.axis("off")

    # Add title text
    title_text = f"{team_name} vs {opponent_name}"
    fig.text(
        0.5,
        1 - 0.5 * TITLE_HEIGHT,
        title_text,
        fontsize=FONT_SIZES["title"],
        fontweight="bold",
        color=COLOURS["White"],
        ha="center",
        va="center",
    )

    # Calculate overall score
    total_for = sum(match.stats["goals_by_quarter"]["for"].values())
    total_against = sum(match.stats["goals_by_quarter"]["against"].values())

    # Create sections with new layout
    _add_result_box(fig, total_for, total_against)
    _add_period_scores(fig, match.stats["goals_by_quarter"])
    _add_overall_stats(fig, match)
    _add_quarter_stats_tables(fig, match)
    _add_pca_pcd(fig, match.stats)
    _add_circle_entries(fig, match.stats)

    return fig


def _add_result_box(fig, for_score, against_score):
    """Add result box in top left"""
    ax = fig.add_axes(ELEMENT_COORDINATES["result_position"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Result box with border
    rect = FancyBboxPatch(
        (0.05, 0.1),
        0.9,
        0.8,
        boxstyle=BOX_DIMENSIONS["border_radius"],
        edgecolor=COLOURS["White"],
        facecolor=COLOURS["Black"],
        linewidth=LINE_WIDTHS["thick"],
    )
    ax.add_patch(rect)

    ax.text(
        0.5,
        0.7,
        "RESULT",
        fontsize=FONT_SIZES["large"],
        color=COLOURS["White"],
        ha="center",
        va="center",
        fontweight="bold",
    )
    ax.text(
        0.5,
        0.3,
        f"{for_score} - {against_score}",
        fontsize=FONT_SIZES["large"],
        fontweight="bold",
        color=COLOURS["White"],
        ha="center",
        va="center",
    )


def _add_period_scores(fig, goals_by_quarter):
    """Add within period scoring table"""
    ax = fig.add_axes(ELEMENT_COORDINATES["period_scores_position"])
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 3)
    ax.axis("off")

    # Black background for title
    title_rect = Rectangle((0, 1), 4, 2, facecolor=COLOURS["Black"], edgecolor="none")
    ax.add_patch(title_rect)

    # Title
    ax.text(
        2,
        2.5,
        "WITHIN PERIOD",
        fontsize=FONT_SIZES["large"],
        color=COLOURS["White"],
        ha="center",
        va="center",
        fontweight="bold",
    )

    # Headers
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    for i, q in enumerate(quarters):
        ax.text(
            i + 0.5,
            1.5,
            q,
            fontsize=FONT_SIZES["medium"],
            color=COLOURS["White"],
            ha="center",
            va="center",
            fontweight="bold",
        )

    # Scores
    for i, q in enumerate(quarters):
        for_goals = goals_by_quarter["for"].get(q, 0)
        against_goals = goals_by_quarter["against"].get(q, 0)
        score_text = f"{for_goals} - {against_goals}"

        # Background color - green if winning, white if drawing, red if losing
        if for_goals > against_goals:
            bgcolor = COLOURS["Light green"]
        elif for_goals == against_goals:
            bgcolor = COLOURS["White"]
        else:
            bgcolor = COLOURS["Light pink"]

        rect = Rectangle(
            (i, 0),
            1,
            1,
            facecolor=bgcolor,
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect)

        ax.text(
            i + 0.5,
            0.5,
            score_text,
            fontsize=FONT_SIZES["medium"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )


def _add_overall_stats(fig, match):
    """Add overall stats table in center"""
    ax = fig.add_axes(ELEMENT_COORDINATES["overall_stats_position"])
    ax.set_xlim(0, OVERALL_WIDTH)
    ax.set_ylim(0, OVERALL_HEIGHT)
    ax.axis("off")

    # Black background
    title_rect = Rectangle(
        (0, 0),
        OVERALL_WIDTH,
        OVERALL_HEIGHT,
        facecolor=COLOURS["Black"],
        edgecolor="none",
    )
    ax.add_patch(title_rect)

    ax.text(
        OVERALL_WIDTH / 2,
        OVERALL_HEIGHT - 0.5,
        "OVERALL STATS",
        fontsize=FONT_SIZES["large"],
        color=COLOURS["White"],
        ha="center",
        va="center",
        fontweight="bold",
    )

    # Stats labels
    y_start = OVERALL_HEIGHT - 1.5
    y_step = 1

    for i, label in enumerate(EVENT_NAMES.keys()):
        y_pos = y_start - i * y_step

        # Count FOR events
        for_count = len(
            match.stats["for_events"][
                match.stats["for_events"]["EventType"].str.contains(
                    EVENT_NAMES[label]["att"], case=False, na=False
                )
            ]
        )
        # Count AGAINST events
        against_count = len(
            match.stats["against_events"][
                match.stats["against_events"]["EventType"].str.contains(
                    EVENT_NAMES[label]["def"], case=False, na=False
                )
            ]
        )

        # FOR box
        rect_for = Rectangle(
            (0, y_pos - 0.5),
            1,
            1,
            facecolor=COLOURS["White"],
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect_for)
        ax.text(
            0.5,
            y_pos,
            str(for_count),
            fontsize=FONT_SIZES["medium"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )

        # Label
        ax.text(
            2.5,
            y_pos,
            label,
            fontsize=FONT_SIZES["medium"],
            fontweight="bold",
            color=COLOURS["White"],
            ha="center",
            va="center",
        )

        # AGAINST box
        rect_against = Rectangle(
            (OVERALL_WIDTH - 1, y_pos - 0.5),
            1,
            1,
            facecolor=COLOURS["White"],
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect_against)
        ax.text(
            OVERALL_WIDTH - 0.5,
            y_pos,
            str(against_count),
            fontsize=FONT_SIZES["medium"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )


def _add_single_quarter_stats_table(fig, match, side="att"):
    """Add quarter-by-quarter stats tables on left and right sides"""

    if side == "att":
        ax = fig.add_axes(ELEMENT_COORDINATES["quarter_stats_for_position"])
    elif side == "def":
        ax = fig.add_axes(ELEMENT_COORDINATES["quarter_stats_against_position"])

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 5)
    ax.axis("off")

    # Black background for FOR title
    title_rect = Rectangle((0, 4), 5, 1, facecolor=COLOURS["Black"], edgecolor="none")
    ax.add_patch(title_rect)

    # Quarter headers
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    for i, q in enumerate(quarters):
        ax.text(
            i + 0.5,
            4.5,
            q,
            fontsize=FONT_SIZES["small"],
            color=COLOURS["White"],
            ha="center",
            va="center",
            fontweight="bold",
        )

    # Event counts by quarter
    events_to_count = [
        "Own Half Restarts",
        "23 Entries",
        "Circle Entries",
        "Penalty Corners",
    ]
    y_positions = [3.5, 2.5, 1.5, 0.5]

    # First pass: collect all counts
    counts_by_row = []
    for row_idx, (label, y_pos) in enumerate(zip(events_to_count, y_positions)):
        row_counts = []
        for col_idx, q in enumerate(quarters):
            if q in match.stats["quarters"] and not match.stats["quarters"][q].empty:
                quarter_events = match.stats["quarters"][q]

                # Count relevant events
                count = len(
                    quarter_events[
                        quarter_events["EventType"].str.contains(
                            EVENT_NAMES[label][side], case=False, na=False
                        )
                    ]
                )

            else:
                count = 0
            row_counts.append(count)
        counts_by_row.append(row_counts)

    # Second pass: draw with conditional formatting
    for row_idx, (label, y_pos) in enumerate(zip(events_to_count, y_positions)):
        row_counts = counts_by_row[row_idx]

        # Apply conditional formatting to all rows
        if len(row_counts) > 0:
            min_count = 0
            max_count = max(row_counts)
        else:
            min_count = max_count = None

        for col_idx, count in enumerate(row_counts):
            # Determine background color
            if min_count is not None and max_count is not None:
                bgcolor = interpolate_color(
                    count,
                    min_count,
                    max_count,
                    COLOURS["Grey"],
                    COLOURS["Light green"] if side == "att" else COLOURS["Light pink"],
                )
            else:
                bgcolor = COLOURS["Grey"]

            rect = Rectangle(
                (col_idx, y_pos - 0.5),
                1,
                1,
                facecolor=bgcolor,
                edgecolor=COLOURS["Black"],
                linewidth=LINE_WIDTHS["thin"],
            )
            ax.add_patch(rect)
            ax.text(
                col_idx + 0.5,
                y_pos,
                str(count),
                fontsize=FONT_SIZES["medium"],
                fontweight="bold",
                color=COLOURS["Black"],
                ha="center",
                va="center",
            )


def _add_quarter_stats_tables(fig, match):
    """Add quarter stats tables for both FOR and AGAINST"""
    _add_single_quarter_stats_table(fig, match, side="att")
    _add_single_quarter_stats_table(fig, match, side="def")


def _add_pca_pcd(fig, stats):
    """Add penalty corner attack and defense sections"""
    # PCA
    _add_pc_section(
        fig,
        stats["pca"],
        ELEMENT_COORDINATES["pca_position"],
        "PCA",
        side="att",
    )
    # PCD
    _add_pc_section(
        fig,
        stats["pcd"],
        ELEMENT_COORDINATES["pcd_position"],
        "PCD",
        side="def",
    )


def add_box(
    x,
    y,
    label,
    value,
    ax,
    width=1,
    height=1,
    bgcolor=COLOURS["White"],
):
    """Helper function to add a labeled box with value"""
    rect = Rectangle(
        (x, y),
        width,
        height,
        facecolor=bgcolor,
        edgecolor=COLOURS["Black"],
        linewidth=LINE_WIDTHS["thin"],
    )
    ax.add_patch(rect)
    ax.text(
        x + 0.5 * width,
        y + height,
        label,
        fontsize=FONT_SIZES["small"],
        fontweight="bold",
        color=COLOURS["White"],
        ha="center",
        va="bottom",
    )
    ax.text(
        x + 0.5 * width,
        y + 0.5 * height,
        str(value),
        fontsize=FONT_SIZES["medium"],
        fontweight="bold",
        color=COLOURS["Black"],
        ha="center",
        va="center",
    )


def _add_pc_section(fig, pc_stats, position, title, side="att"):
    """Add a penalty corner section (PCA or PCD)"""
    ax = fig.add_axes(position)
    ax.set_xlim(0, PC_WIDTH)
    ax.set_ylim(0, PC_HEIGHT)
    ax.axis("off")

    # Add pitch image as background
    pitch_path = Path("images/black_tquarter.jpg")
    if pitch_path.exists():
        pitch_img = mpimg.imread(pitch_path)
        ax.imshow(pitch_img, extent=[0, PC_WIDTH, 0, PC_HEIGHT - 1], aspect="auto")

    # Border
    rect = Rectangle(
        (0, 0),
        PC_WIDTH,
        PC_HEIGHT,
        facecolor="none",
        edgecolor=COLOURS["Black"],
        linewidth=LINE_WIDTHS["thick"],
    )
    ax.add_patch(rect)

    # Black background for title
    title_rect = Rectangle(
        (0, PC_HEIGHT - 1), PC_WIDTH, 1, facecolor=COLOURS["Black"], edgecolor="none"
    )
    ax.add_patch(title_rect)

    # Title
    ax.text(
        PC_WIDTH / 2,
        PC_HEIGHT - 0.5,
        title,
        fontsize=FONT_SIZES["medium"],
        color=COLOURS["White"],
        ha="center",
        va="center",
        fontweight="bold",
    )

    # Preset 3 and 4 column x positions
    col_4_x = np.linspace(0.2, PC_WIDTH - 1.2, 4)
    col_3_x = np.linspace(0.5, PC_WIDTH - 1.2, 3)

    # Preset 3 row y positions
    row_3_y = np.linspace(PC_HEIGHT - 2.5, 1, 3)

    # Top row: Goal, Ph2 Goal, Reawarded
    goal = pc_stats["goal"]
    ph2_goal = pc_stats["ph2_goal"]
    reawarded = pc_stats["reawarded"]

    labels = ["GOAL", "PH2 GOAL", "REAWARD"]
    values = [goal, ph2_goal, reawarded]

    # Second row: Saved, Recycled, Miss, Turnover
    saved = pc_stats["saved"]
    recycled = pc_stats["recycled"]
    miss = pc_stats["miss"]
    turnover = pc_stats["turnover"]

    # Group 1: Goal, PH2 goal, Reawarded, Saved, Recycled (good outcomes)
    group1_values = [goal, ph2_goal, reawarded, saved, recycled]
    min_group1 = 0
    max_group1 = max(group1_values)

    # Group 2: Miss, Turnover (bad outcomes)
    group2_values = [miss, turnover]
    min_group2 = 0
    max_group2 = max(group2_values)

    # Re-draw top row with conditional formatting
    for label, value, x in zip(labels, values, col_3_x):
        bgcolor = interpolate_color(
            value,
            min_group1,
            max_group1,
            COLOURS["Grey"],
            COLOURS["Light green"] if side == "att" else COLOURS["Light pink"],
        )
        add_box(
            x,
            row_3_y[0],
            label,
            value,
            ax,
            bgcolor=bgcolor,
        )

    labels = ["SAVED", "RECYCLED", "MISS", "TURNOVER"]
    values = [saved, recycled, miss, turnover]

    for i, (label, value, x) in enumerate(zip(labels, values, col_4_x)):
        # First two are group 1, last two are group 2
        if i < 2:
            bgcolor = interpolate_color(
                value,
                min_group1,
                max_group1,
                COLOURS["Grey"],
                COLOURS["Light green"] if side == "att" else COLOURS["Light pink"],
            )
        else:
            bgcolor = interpolate_color(
                value,
                min_group2,
                max_group2,
                COLOURS["Grey"],
                COLOURS["Light pink"] if side == "att" else COLOURS["Light green"],
            )

        add_box(
            x,
            row_3_y[1],
            label,
            value,
            ax,
            bgcolor=bgcolor,
        )

    # Third row: Left, Right, Straight, Variation (Castle vs Routine)
    left = pc_stats["left"]
    right = pc_stats["right"]
    straight = pc_stats["straight"]
    variation = pc_stats["variation"]

    # Group 3: All direction values
    group3_values = [left, right, straight, variation]
    min_group3 = 0
    max_group3 = max(group3_values)

    labels = ["LEFT", "RIGHT", "STRAIGHT", "VARIATION"]
    values = [left, right, straight, variation]

    for label, value, x in zip(labels, values, col_4_x):
        bgcolor = interpolate_color(
            value,
            min_group3,
            max_group3,
            COLOURS["Grey"],
            COLOURS["Light green"] if side == "att" else COLOURS["Light pink"],
        )
        add_box(
            x,
            row_3_y[2],
            label,
            value,
            ax,
            bgcolor=bgcolor,
        )

    ax.text(
        np.mean(col_4_x[:2]) + 0.5,
        0.2,
        "CASTLE",
        fontsize=FONT_SIZES["small"],
        fontweight="bold",
        color=COLOURS["White"],
        ha="center",
        va="bottom",
    )

    ax.text(
        np.mean(col_4_x[2:]) + 0.5,
        0.2,
        "ROUTINE",
        fontsize=FONT_SIZES["small"],
        fontweight="bold",
        color=COLOURS["White"],
        ha="center",
        va="bottom",
    )


def _add_circle_entries(fig, stats):
    """Add circle entry attack and defense sections"""
    # Circle ATT
    _add_circle_section(
        fig,
        stats["circle_att"],
        ELEMENT_COORDINATES["circle_att_position"],
        "CIRCLE ATT",
        side="att",
    )
    # Circle DEF
    _add_circle_section(
        fig,
        stats["circle_def"],
        ELEMENT_COORDINATES["circle_def_position"],
        "CIRCLE DEF",
        side="def",
    )


def _add_circle_section(fig, circle_stats, position, title, side="att"):
    """Add a circle entry section (ATT or DEF)"""
    ax = fig.add_axes(position)
    ax.set_xlim(0, CIRCLE_WIDTH)
    ax.set_ylim(0, CIRCLE_HEIGHT)
    ax.axis("off")

    # Add pitch image as background
    pitch_path = Path("images/black_thalf.jpg")
    if pitch_path.exists():
        pitch_img = mpimg.imread(pitch_path)
        ax.imshow(
            pitch_img,
            extent=[0, CIRCLE_WIDTH, 0, CIRCLE_HEIGHT - 1],
            aspect="auto",
        )

    # Border
    rect = Rectangle(
        (0, 0),
        CIRCLE_WIDTH,
        CIRCLE_HEIGHT,
        facecolor="none",
        edgecolor=COLOURS["Black"],
        linewidth=LINE_WIDTHS["thick"],
    )
    ax.add_patch(rect)

    # Black background for title
    title_rect = Rectangle(
        (0, CIRCLE_HEIGHT - 1),
        CIRCLE_WIDTH,
        1,
        facecolor=COLOURS["Black"],
        edgecolor="none",
    )
    ax.add_patch(title_rect)

    # Title
    ax.text(
        CIRCLE_WIDTH / 2,
        CIRCLE_HEIGHT - 0.5,
        title,
        fontsize=FONT_SIZES["medium"],
        color=COLOURS["White"],
        ha="center",
        va="center",
        fontweight="bold",
    )

    # Circle diagram with position counts
    # Top positions (left baseline, l45, centre, r45, right baseline)
    left_baseline = circle_stats["left_baseline"]
    l45 = circle_stats["l45"]
    centre = circle_stats["centre"]
    r45 = circle_stats["r45"]
    right_baseline = circle_stats["right_baseline"]

    # Calculate min/max for conditional formatting
    position_values = [left_baseline, l45, centre, r45, right_baseline]
    min_position = 0
    max_position = max(position_values)

    # Draw simplified circle representation
    y_circle = CIRCLE_HEIGHT - 3

    # Arc positions
    arc_x = [1, 1.4, CIRCLE_WIDTH / 2 - 0.5, CIRCLE_WIDTH - 2.4, CIRCLE_WIDTH - 2]
    arc_y = [y_circle, y_circle - 1.2, y_circle - 1.5, y_circle - 1.2, y_circle]

    # Top boxes with conditional formatting
    for value, x, y in zip(
        [left_baseline, right_baseline], [arc_x[0], arc_x[-1]], [arc_y[0], arc_y[-1]]
    ):
        bgcolor = interpolate_color(
            value,
            min_position,
            max_position,
            COLOURS["Grey"],
            COLOURS["Light green"] if side == "att" else COLOURS["Light pink"],
        )
        add_box(
            x,
            y,
            "",
            value,
            ax,
            bgcolor=bgcolor,
        )

    # Middle arc positions (l45, r45) with conditional formatting
    for value, x, y in zip([l45, r45], [arc_x[1], arc_x[3]], [arc_y[1], arc_y[3]]):
        bgcolor = interpolate_color(
            value,
            min_position,
            max_position,
            COLOURS["Grey"],
            COLOURS["Light green"] if side == "att" else COLOURS["Light pink"],
        )
        add_box(
            x,
            y,
            "",
            value,
            ax,
            bgcolor=bgcolor,
        )

    # Center position with conditional formatting
    bgcolor = interpolate_color(
        centre,
        min_position,
        max_position,
        COLOURS["Grey"],
        COLOURS["Light green"] if side == "att" else COLOURS["Light pink"],
    )
    add_box(
        arc_x[2],
        arc_y[2],
        "",
        centre,
        ax,
        bgcolor=bgcolor,
    )

    # Bottom stats boxes
    row_y = np.linspace(3, 1, 2)
    row_x = np.linspace(0.5, CIRCLE_WIDTH - 1.5, 4)

    # 1st row: Goal, Upgrade, Saved, Recycled
    goal = circle_stats["goal"]
    upgrade = circle_stats["upgrade"]
    saved = circle_stats["saved"]
    recycled = circle_stats["recycled"]

    labels = ["GOAL", "UPGRADE", "SAVED", "RECYCLED"]
    values = [goal, upgrade, saved, recycled]

    # Calculate min/max for first row
    min_val_row1 = 0
    max_val_row1 = max(values)

    for label, value, x in zip(labels, values, row_x):
        # Conditional formatting
        bgcolor = interpolate_color(
            value,
            min_val_row1,
            max_val_row1,
            COLOURS["Grey"],
            COLOURS["Light green"] if side == "att" else COLOURS["Light pink"],
        )

        add_box(
            x,
            row_y[0],
            label,
            value,
            ax,
            bgcolor=bgcolor,
        )

    # Bottom row: Miss, Turnover
    miss = circle_stats["miss"]
    turnover = circle_stats["turnover"]

    labels2 = ["MISS", "TURNOVER"]
    values2 = [miss, turnover]

    # Calculate min/max for second row
    min_val_row2 = 0
    max_val_row2 = max(values2)

    for label, value, x in zip(
        labels2, values2, [CIRCLE_WIDTH / 2 - 1.5, CIRCLE_WIDTH / 2 + 0.5]
    ):
        # Conditional formatting
        bgcolor = interpolate_color(
            value,
            min_val_row2,
            max_val_row2,
            COLOURS["Grey"],
            COLOURS["Light pink"] if side == "att" else COLOURS["Light green"],
        )

        add_box(
            x,
            row_y[1],
            label,
            value,
            ax,
            bgcolor=bgcolor,
        )
