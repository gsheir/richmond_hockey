from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

from settings import (
    BOX_DIMENSIONS,
    CANVAS_LEFT,
    CANVAS_RIGHT,
    COLOURS,
    ELEMENT_COORDINATES,
    FIG_SIZE,
    FONT_SIZES,
    LINE_WIDTHS,
    PC_HEIGHT,
    PC_WIDTH,
    TITLE_HEIGHT,
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
    # _add_circle_entries(fig, match.stats)

    return fig


def _add_result_box(fig, for_score, against_score):
    """Add result box in top left"""
    ax = fig.add_axes(ELEMENT_COORDINATES["result_position"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    # ax.axis("off")

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
    # ax.axis("off")

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
            bgcolor = COLOURS["Beige"]
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
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 7)
    # ax.axis("off")

    # Black background
    title_rect = Rectangle((0, 0), 5, 7, facecolor=COLOURS["Black"], edgecolor="none")
    ax.add_patch(title_rect)

    ax.text(
        2.5,
        6.5,
        "OVERALL STATS",
        fontsize=FONT_SIZES["large"],
        color=COLOURS["White"],
        ha="center",
        va="center",
        fontweight="bold",
    )

    # Stats labels
    stats_labels = [
        "Own half restarts",
        "23 entries",
        "Circle entries",
        "Penalty corners",
        "Penalty strokes",
        "Goals",
    ]

    y_start = 5.5
    y_step = 1

    for i, label in enumerate(stats_labels):
        y_pos = y_start - i * y_step

        # Count FOR events
        for_count = 0
        against_count = 0

        if "restart" in label.lower():
            for_count = len(
                match.stats["for_events"][
                    match.stats["for_events"]["EventType"].str.contains(
                        "Own Half Restart", case=False, na=False
                    )
                ]
            )
            against_count = len(
                match.stats["against_events"][
                    match.stats["against_events"]["EventType"].str.contains(
                        "Own Half Restart", case=False, na=False
                    )
                ]
            )
        elif "23 entries" in label.lower():
            for_count = len(
                match.stats["for_events"][
                    match.stats["for_events"]["EventType"].str.contains(
                        "23 Entry", case=False, na=False
                    )
                ]
            )
            against_count = len(
                match.stats["against_events"][
                    match.stats["against_events"]["EventType"].str.contains(
                        "23 Entry", case=False, na=False
                    )
                ]
            )
        elif "Circle" in label:
            for_count = match.stats["circle_att"]["total"]
            against_count = match.stats["circle_def"]["total"]
        elif "Penalty corners" in label:
            for_count = match.stats["pca"]["total"]
            against_count = match.stats["pcd"]["total"]
        elif "Penalty strokes" in label:
            for_count = len(
                match.stats["for_events"][
                    match.stats["for_events"]["EventType"].str.contains(
                        "Penalty Stroke", case=False, na=False
                    )
                ]
            )
            against_count = len(
                match.stats["against_events"][
                    match.stats["against_events"]["EventType"].str.contains(
                        "Penalty Stroke", case=False, na=False
                    )
                ]
            )
        elif "Goals" in label:
            for_count = sum(match.stats["goals_by_quarter"]["for"].values())
            against_count = sum(match.stats["goals_by_quarter"]["against"].values())

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
            (4, y_pos - 0.5),
            1,
            1,
            facecolor=COLOURS["White"],
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect_against)
        ax.text(
            4.5,
            y_pos,
            str(against_count),
            fontsize=FONT_SIZES["medium"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )


def _add_single_quarter_stats_table(fig, match, is_for=True):
    """Add quarter-by-quarter stats tables on left and right sides"""

    if is_for:
        ax = fig.add_axes(ELEMENT_COORDINATES["quarter_stats_for_position"])
    else:
        ax = fig.add_axes(ELEMENT_COORDINATES["quarter_stats_against_position"])

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 5)
    # ax_for.axis("off")

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
    event_labels = [
        "Own half restarts",
        "23 entries",
        "Circle entries",
        "Penalty corners",
    ]
    y_positions = [3.5, 2.5, 1.5, 0.5]

    if is_for:
        col_str = "ATT"
        pc_str = "PCA"
    else:
        col_str = "DEF"
        pc_str = "PCD"

    for row_idx, (label, y_pos) in enumerate(zip(event_labels, y_positions)):
        for col_idx, q in enumerate(quarters):
            if q in match.stats["quarters"] and not match.stats["quarters"][q].empty:
                q_events = match.stats["quarters"][q]
                q_events = q_events[
                    q_events["EventType"].str.contains(col_str, case=False, na=False)
                ]

                # Count relevant events
                if "restart" in label.lower():
                    count = len(
                        q_events[
                            q_events["EventType"].str.contains(
                                "Own Half Restart", case=False, na=False
                            )
                        ]
                    )
                elif "23 entries" in label.lower():
                    count = len(
                        q_events[
                            q_events["EventType"].str.contains(
                                "23 Entry", case=False, na=False
                            )
                        ]
                    )
                elif "Circle" in label:
                    count = len(
                        q_events[
                            q_events["EventType"].str.contains(
                                "Circle Entry", case=False, na=False
                            )
                        ]
                    )
                elif "Penalty" in label:
                    count = len(
                        q_events[
                            q_events["EventType"].str.contains(
                                pc_str, case=False, na=False
                            )
                        ]
                    )
                else:
                    count = 0
            else:
                count = 0

            rect = Rectangle(
                (col_idx, y_pos - 0.5),
                1,
                1,
                facecolor=COLOURS["White"],
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
    _add_single_quarter_stats_table(fig, match, is_for=True)
    _add_single_quarter_stats_table(fig, match, is_for=False)


def _add_pca_pcd(fig, stats):
    """Add penalty corner attack and defense sections"""
    # PCA
    _add_pc_section(
        fig,
        stats["pca"],
        ELEMENT_COORDINATES["pca_position"],
        "PCA",
    )
    # PCD
    _add_pc_section(
        fig,
        stats["pcd"],
        ELEMENT_COORDINATES["pcd_position"],
        "PCD",
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


def _add_pc_section(fig, pc_stats, position, title):
    """Add a penalty corner section (PCA or PCD)"""
    ax = fig.add_axes(position)
    ax.set_xlim(0, PC_WIDTH)
    ax.set_ylim(0, PC_HEIGHT)
    # ax.axis("off")

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
        edgecolor=COLOURS["White"],
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

    for label, value, x in zip(labels, values, col_3_x):
        add_box(
            x,
            row_3_y[0],
            label,
            value,
            ax,
        )

    # Second row: Saved, Recycled, Miss, Turnover
    saved = pc_stats["saved"]
    recycled = pc_stats["recycled"]
    miss = pc_stats["miss"]
    turnover = pc_stats["turnover"]

    labels = ["SAVED", "RECYCLED", "MISS", "TURNOVER"]
    values = [saved, recycled, miss, turnover]

    for label, value, x in zip(labels, values, col_4_x):
        add_box(
            x,
            row_3_y[1],
            label,
            value,
            ax,
        )

    # Third row: Left, Right, Straight, Variation (Castle vs Routine)
    left = pc_stats["left"]
    right = pc_stats["right"]
    straight = pc_stats["straight"]
    variation = pc_stats["variation"]

    labels = ["LEFT", "RIGHT", "STRAIGHT", "VARIATION"]
    values = [left, right, straight, variation]

    for label, value, x in zip(labels, values, col_4_x):
        add_box(
            x,
            row_3_y[2],
            label,
            value,
            ax,
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
    _add_circle_section(fig, stats["circle_att"], 0.38, 0.08, "CIRCLE ATT")
    # Circle DEF
    _add_circle_section(fig, stats["circle_def"], 0.61, 0.08, "CIRCLE DEF")


def _add_circle_section(fig, circle_stats, x_pos, y_pos, title):
    """Add a circle entry section (ATT or DEF)"""
    ax = fig.add_axes([x_pos, y_pos, 0.21, 0.35])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis("off")

    # Add pitch image as background
    pitch_path = Path("images/black_thalf.jpg")
    if pitch_path.exists():
        pitch_img = mpimg.imread(pitch_path)
        ax.imshow(pitch_img, extent=[0, 10, 0, 14], aspect="auto", alpha=0.3)

    # Border
    rect = Rectangle(
        (0, 0),
        10,
        14,
        facecolor="none",
        edgecolor=COLOURS["White"],
        linewidth=LINE_WIDTHS["thick"],
    )
    ax.add_patch(rect)

    # Black background for title
    title_rect = Rectangle(
        (0, 12.7), 10, 1.3, facecolor=COLOURS["Black"], edgecolor="none"
    )
    ax.add_patch(title_rect)

    # Title
    ax.text(
        5,
        13.35,
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

    # Draw simplified circle representation
    y_circle = 9

    # Top arc positions
    top_positions = [left_baseline, l45, centre, r45, right_baseline]
    top_x = [1.5, 3, 5, 7, 8.5]

    # Top boxes
    for value, x in zip([left_baseline, right_baseline], [1.5, 8.5]):
        rect = Rectangle(
            (x - 0.6, y_circle + 1.5),
            1.2,
            0.8,
            facecolor=COLOURS["Beige"],
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect)
        ax.text(
            x,
            y_circle + 1.9,
            str(value),
            fontsize=FONT_SIZES["medium"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )

    # Middle arc positions (l45, centre, r45)
    for value, x in zip([l45, centre, r45], [3, 5, 7]):
        rect = Rectangle(
            (x - 0.6, y_circle + 0.3),
            1.2,
            0.8,
            facecolor=COLOURS["Beige"],
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect)
        ax.text(
            x,
            y_circle + 0.7,
            str(value),
            fontsize=FONT_SIZES["medium"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )

    # Center position (additional centre display in middle)
    rect = Rectangle(
        (4.3, y_circle - 1.2),
        1.4,
        0.8,
        facecolor=COLOURS["Beige"],
        edgecolor=COLOURS["Black"],
        linewidth=LINE_WIDTHS["thin"],
        linestyle="--",
    )
    ax.add_patch(rect)
    ax.text(
        5,
        y_circle - 0.8,
        str(centre),
        fontsize=FONT_SIZES["medium"],
        fontweight="bold",
        color=COLOURS["Black"],
        ha="center",
        va="center",
    )

    # Bottom row: Goal, Upgrade, Saved, Recycled
    goal = circle_stats["goal"]
    upgrade = circle_stats["upgrade"]
    saved = circle_stats["saved"]
    recycled = circle_stats["recycled"]

    y_bottom = 5.5
    labels = ["GOAL", "UPGRADE", "SAVED", "RECYCLED"]
    values = [goal, upgrade, saved, recycled]

    for i, (label, value) in enumerate(zip(labels, values)):
        x = 0.8 + i * 2.3
        # Color coding
        if label == "GOAL":
            bgcolor = COLOURS["Light green"] if value > 0 else COLOURS["Beige"]
        elif label == "UPGRADE":
            bgcolor = COLOURS["Light pink"]
        elif label == "SAVED":
            bgcolor = COLOURS["Light yellow"]
        else:
            bgcolor = COLOURS["Beige"]

        rect = Rectangle(
            (x, y_bottom),
            1.8,
            1.0,
            facecolor=bgcolor,
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect)
        ax.text(
            x + 0.9,
            y_bottom + 0.75,
            label,
            fontsize=FONT_SIZES["small"],
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )
        ax.text(
            x + 0.9,
            y_bottom + 0.25,
            str(value),
            fontsize=FONT_SIZES["medium"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )

    # Bottom row: Miss, Turnover
    miss = circle_stats["miss"]
    turnover = circle_stats["turnover"]

    y_bottom2 = 4.0
    labels2 = ["MISS", "TURNOVER"]
    values2 = [miss, turnover]

    for i, (label, value) in enumerate(zip(labels2, values2)):
        x = 3 + i * 2.5
        bgcolor = COLOURS["Light pink"] if label == "MISS" else COLOURS["Beige"]

        rect = Rectangle(
            (x, y_bottom2),
            1.8,
            1.0,
            facecolor=bgcolor,
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect)
        ax.text(
            x + 0.9,
            y_bottom2 + 0.75,
            label,
            fontsize=FONT_SIZES["small"],
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )
        ax.text(
            x + 0.9,
            y_bottom2 + 0.25,
            str(value),
            fontsize=FONT_SIZES["medium"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )
