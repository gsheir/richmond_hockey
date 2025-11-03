from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

from settings import (
    BOX_DIMENSIONS,
    COLOURS,
    FIG_SIZE,
    FONT_SIZES,
    LINE_WIDTHS,
)


def create_dashboard(match, team_name="Richmond M1", opponent_name="Opponent"):
    """Create a complete match dashboard"""
    # Create figure with dark red background
    fig = plt.figure(figsize=FIG_SIZE)
    fig.patch.set_facecolor(COLOURS["Richmond red"])

    # Add black title bar at the top
    title_ax = fig.add_axes([0, 0.90, 1, 0.10])
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
        logo_ax = fig.add_axes([0.01, 0.935, 0.08, 0.055])
        logo_ax.imshow(logo_img)
        logo_ax.axis("off")

    # Add title text
    title_text = f"{team_name} vs {opponent_name}"
    fig.text(
        0.5,
        0.965,
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
    _add_quarter_stats_tables(fig, match)
    _add_overall_stats(fig, match)
    _add_pca_pcd(fig, match.stats)
    _add_circle_entries(fig, match.stats)

    return fig


def _add_result_box(fig, for_score, against_score):
    """Add result box in top left"""
    ax = fig.add_axes([0.025, 0.815, 0.075, 0.09])
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
        fontsize=FONT_SIZES["medium_small"],
        color=COLOURS["White"],
        ha="center",
        va="center",
        fontweight="bold",
    )
    ax.text(
        0.5,
        0.3,
        f"{for_score} - {against_score}",
        fontsize=FONT_SIZES["extra_large"],
        fontweight="bold",
        color=COLOURS["White"],
        ha="center",
        va="center",
    )


def _add_period_scores(fig, goals_by_quarter):
    """Add within period scoring table"""
    ax = fig.add_axes([0.115, 0.815, 0.23, 0.09])
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 3.5)
    ax.axis("off")

    # Black background for title
    title_rect = Rectangle(
        (0, 2.6), 5, 0.8, facecolor=COLOURS["Black"], edgecolor="none"
    )
    ax.add_patch(title_rect)

    # Title
    ax.text(
        2.5,
        3.0,
        "WITHIN PERIOD",
        fontsize=FONT_SIZES["medium"],
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
            2.1,
            q,
            fontsize=FONT_SIZES["small_text"],
            color=COLOURS["Black"],
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
            (i, 0.5),
            1,
            1.3,
            facecolor=bgcolor,
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect)

        ax.text(
            i + 0.5,
            1.15,
            score_text,
            fontsize=FONT_SIZES["large"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )


def _add_quarter_stats_tables(fig, match):
    """Add quarter-by-quarter stats tables on left and right sides"""
    # FOR table (left side)
    ax_for = fig.add_axes([0.025, 0.42, 0.12, 0.35])
    ax_for.set_xlim(0, 5)
    ax_for.set_ylim(0, 6)
    ax_for.axis("off")

    # Black background for FOR title
    title_rect = Rectangle(
        (0, 5.2), 5, 0.7, facecolor=COLOURS["Black"], edgecolor="none"
    )
    ax_for.add_patch(title_rect)
    ax_for.text(
        2.5,
        5.55,
        "FOR",
        fontsize=FONT_SIZES["medium_large"],
        color=COLOURS["White"],
        ha="center",
        va="center",
        fontweight="bold",
    )

    # Quarter headers
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    for i, q in enumerate(quarters):
        ax_for.text(
            i + 0.5,
            4.8,
            q,
            fontsize=FONT_SIZES["medium_small"],
            color=COLOURS["Black"],
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
    y_positions = [4.0, 3.0, 2.0, 1.0]

    for row_idx, (label, y_pos) in enumerate(zip(event_labels, y_positions)):
        for col_idx, q in enumerate(quarters):
            if q in match.stats["quarters"] and not match.stats["quarters"][q].empty:
                q_events = match.stats["quarters"][q]
                q_for = q_events[
                    q_events["EventType"].str.contains("ATT", case=False, na=False)
                ]

                # Count relevant events
                if "restart" in label.lower():
                    count = len(
                        q_for[
                            q_for["EventType"].str.contains(
                                "Own Half Restart", case=False, na=False
                            )
                        ]
                    )
                elif "23 entries" in label.lower():
                    count = len(
                        q_for[
                            q_for["EventType"].str.contains(
                                "23 Entry", case=False, na=False
                            )
                        ]
                    )
                elif "Circle" in label:
                    count = len(
                        q_for[
                            q_for["EventType"].str.contains(
                                "Circle Entry", case=False, na=False
                            )
                        ]
                    )
                elif "Penalty" in label:
                    count = len(
                        q_for[
                            q_for["EventType"].str.contains("PCA", case=False, na=False)
                        ]
                    )
                else:
                    count = 0
            else:
                count = 0

            rect = Rectangle(
                (col_idx, y_pos - 0.4),
                1,
                0.8,
                facecolor=COLOURS["Beige"],
                edgecolor=COLOURS["Black"],
                linewidth=LINE_WIDTHS["thin"],
            )
            ax_for.add_patch(rect)
            ax_for.text(
                col_idx + 0.5,
                y_pos,
                str(count),
                fontsize=FONT_SIZES["medium"],
                fontweight="bold",
                color=COLOURS["Black"],
                ha="center",
                va="center",
            )

    # AGAINST table (right side)
    ax_against = fig.add_axes([0.855, 0.42, 0.12, 0.35])
    ax_against.set_xlim(0, 5)
    ax_against.set_ylim(0, 6)
    ax_against.axis("off")

    # Black background for AGAINST title
    title_rect = Rectangle(
        (0, 5.2), 5, 0.7, facecolor=COLOURS["Black"], edgecolor="none"
    )
    ax_against.add_patch(title_rect)
    ax_against.text(
        2.5,
        5.55,
        "AGAINST",
        fontsize=FONT_SIZES["medium_large"],
        color=COLOURS["White"],
        ha="center",
        va="center",
        fontweight="bold",
    )

    # Quarter headers
    for i, q in enumerate(quarters):
        ax_against.text(
            i + 0.5,
            4.8,
            q,
            fontsize=FONT_SIZES["medium_small"],
            color=COLOURS["Black"],
            ha="center",
            va="center",
            fontweight="bold",
        )

    # Event counts by quarter
    for row_idx, (label, y_pos) in enumerate(zip(event_labels, y_positions)):
        for col_idx, q in enumerate(quarters):
            if q in match.stats["quarters"] and not match.stats["quarters"][q].empty:
                q_events = match.stats["quarters"][q]
                q_against = q_events[
                    q_events["EventType"].str.contains("DEF", case=False, na=False)
                ]

                # Count relevant events
                if "restart" in label.lower():
                    count = len(
                        q_against[
                            q_against["EventType"].str.contains(
                                "Own Half Restart", case=False, na=False
                            )
                        ]
                    )
                elif "23 entries" in label.lower():
                    count = len(
                        q_against[
                            q_against["EventType"].str.contains(
                                "23 Entry", case=False, na=False
                            )
                        ]
                    )
                elif "Circle" in label:
                    count = len(
                        q_against[
                            q_against["EventType"].str.contains(
                                "Circle Entry", case=False, na=False
                            )
                        ]
                    )
                elif "Penalty" in label:
                    count = len(
                        q_against[
                            q_against["EventType"].str.contains(
                                "PCD", case=False, na=False
                            )
                        ]
                    )
                else:
                    count = 0
            else:
                count = 0

            rect = Rectangle(
                (col_idx, y_pos - 0.4),
                1,
                0.8,
                facecolor=COLOURS["Light pink"],
                edgecolor=COLOURS["Black"],
                linewidth=LINE_WIDTHS["thin"],
            )
            ax_against.add_patch(rect)
            ax_against.text(
                col_idx + 0.5,
                y_pos,
                str(count),
                fontsize=FONT_SIZES["medium"],
                fontweight="bold",
                color=COLOURS["Black"],
                ha="center",
                va="center",
            )


def _add_overall_stats(fig, match):
    """Add overall stats table in center"""
    ax = fig.add_axes([0.17, 0.42, 0.18, 0.41])
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # Black background for title
    title_rect = Rectangle(
        (0, 9.3), 3, 0.7, facecolor=COLOURS["Black"], edgecolor="none"
    )
    ax.add_patch(title_rect)

    ax.text(
        1.5,
        9.65,
        "OVERALL STATS",
        fontsize=FONT_SIZES["medium_large"],
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

    y_start = 8.5
    y_step = 1.3

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
            (0, y_pos - 0.4),
            0.8,
            0.8,
            facecolor=COLOURS["Beige"],
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect_for)
        ax.text(
            0.4,
            y_pos,
            str(for_count),
            fontsize=FONT_SIZES["text"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )

        # Label
        ax.text(
            1.5,
            y_pos,
            label,
            fontsize=FONT_SIZES["small_text"],
            color=COLOURS["White"],
            ha="center",
            va="center",
        )

        # AGAINST box
        rect_against = Rectangle(
            (2.2, y_pos - 0.4),
            0.8,
            0.8,
            facecolor=COLOURS["Light pink"],
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect_against)
        ax.text(
            2.6,
            y_pos,
            str(against_count),
            fontsize=FONT_SIZES["text"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )


def _add_pca_pcd(fig, stats):
    """Add penalty corner attack and defense sections"""
    # PCA
    _add_pc_section(fig, stats["pca"], 0.38, 0.815, "PCA")
    # PCD
    _add_pc_section(fig, stats["pcd"], 0.61, 0.815, "PCD")


def _add_pc_section(fig, pc_stats, x_pos, y_pos, title):
    """Add a penalty corner section (PCA or PCD)"""
    ax = fig.add_axes([x_pos, y_pos, 0.21, 0.10])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # Add pitch image as background
    pitch_path = Path("images/black_tquarter.jpg")
    if pitch_path.exists():
        pitch_img = mpimg.imread(pitch_path)
        ax.imshow(pitch_img, extent=[0, 10, 0, 10], aspect="auto", alpha=0.3)

    # Border
    rect = Rectangle(
        (0, 0),
        10,
        10,
        facecolor="none",
        edgecolor=COLOURS["White"],
        linewidth=LINE_WIDTHS["thick"],
    )
    ax.add_patch(rect)

    # Black background for title
    title_rect = Rectangle(
        (0, 8.5), 10, 1.5, facecolor=COLOURS["Black"], edgecolor="none"
    )
    ax.add_patch(title_rect)

    # Title
    ax.text(
        5,
        9.25,
        title,
        fontsize=FONT_SIZES["text"],
        color=COLOURS["White"],
        ha="center",
        va="center",
        fontweight="bold",
    )
    ax.text(
        5,
        9.5,
        title,
        fontsize=FONT_SIZES["text"],
        color=COLOURS["White"],
        ha="center",
        va="top",
        fontweight="bold",
    )

    # Top row: Goal, Ph2 Goal, Reawarded
    goal = pc_stats["goal"]
    ph2_goal = pc_stats["ph2_goal"]
    reawarded = pc_stats["reawarded"]

    # Goal box (green if > 0)
    goal_color = COLOURS["Light green"] if goal > 0 else COLOURS["Beige"]
    rect = Rectangle(
        (1, 7.5),
        2,
        1.2,
        facecolor=goal_color,
        edgecolor=COLOURS["Black"],
        linewidth=LINE_WIDTHS["thin"],
    )
    ax.add_patch(rect)
    ax.text(
        2,
        8.7,
        "GOAL",
        fontsize=FONT_SIZES["small"],
        color=COLOURS["Black"],
        ha="center",
        va="center",
    )
    ax.text(
        2,
        7.9,
        str(goal),
        fontsize=FONT_SIZES["text"],
        fontweight="bold",
        color=COLOURS["Black"],
        ha="center",
        va="center",
    )

    # Ph2 Goal box
    ph2_color = COLOURS["Light green"] if ph2_goal > 0 else COLOURS["Beige"]
    rect = Rectangle(
        (4, 7.5),
        2,
        1.2,
        facecolor=ph2_color,
        edgecolor=COLOURS["Black"],
        linewidth=LINE_WIDTHS["thin"],
    )
    ax.add_patch(rect)
    ax.text(
        5,
        8.7,
        "PH2 GOAL",
        fontsize=FONT_SIZES["extra_small"],
        color=COLOURS["Black"],
        ha="center",
        va="center",
    )
    ax.text(
        5,
        7.9,
        str(ph2_goal),
        fontsize=FONT_SIZES["text"],
        fontweight="bold",
        color=COLOURS["Black"],
        ha="center",
        va="center",
    )

    # Reawarded box
    rect = Rectangle(
        (7, 7.5),
        2,
        1.2,
        facecolor=COLOURS["Beige"],
        edgecolor=COLOURS["Black"],
        linewidth=LINE_WIDTHS["thin"],
    )
    ax.add_patch(rect)
    ax.text(
        8,
        8.7,
        "REAWARDED",
        fontsize=FONT_SIZES["extra_small"],
        color=COLOURS["Black"],
        ha="center",
        va="center",
    )
    ax.text(
        8,
        7.9,
        str(reawarded),
        fontsize=FONT_SIZES["text"],
        fontweight="bold",
        color=COLOURS["Black"],
        ha="center",
        va="center",
    )

    # Second row: Saved, Recycled, Miss, Turnover
    saved = pc_stats["saved"]
    recycled = pc_stats["recycled"]
    miss = pc_stats["miss"]
    turnover = pc_stats["turnover"]

    y2 = 6.0
    labels = ["SAVED", "RECYCLED", "MISS", "TURNOVER"]
    values = [saved, recycled, miss, turnover]
    x_positions = [0.5, 3, 5.5, 8]

    for label, value, x in zip(labels, values, x_positions):
        rect = Rectangle(
            (x, y2),
            1.8,
            1.2,
            facecolor=COLOURS["Beige"],
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect)
        ax.text(
            x + 0.9,
            y2 + 1.0,
            label,
            fontsize=FONT_SIZES["extra_small"],
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )
        ax.text(
            x + 0.9,
            y2 + 0.3,
            str(value),
            fontsize=FONT_SIZES["medium_large"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )

    # Third row: Left, Right, Straight, Variation (Castle vs Routine)
    left = pc_stats["left"]
    right = pc_stats["right"]
    straight = pc_stats["straight"]
    variation = pc_stats["variation"]

    y3 = 4.3
    ax.text(
        2.5,
        y3 + 0.5,
        "CASTLE",
        fontsize=FONT_SIZES["medium_small"],
        color=COLOURS["White"],
        ha="center",
        va="center",
    )
    ax.text(
        7.5,
        y3 + 0.5,
        "ROUTINE",
        fontsize=FONT_SIZES["medium_small"],
        color=COLOURS["White"],
        ha="center",
        va="center",
    )

    # Castle: Left, Right, Straight
    castle_labels = ["LEFT", "RIGHT", "STRAIGHT"]
    castle_values = [left, right, straight]
    castle_x = [0.5, 1.8, 3.1]

    for label, value, x in zip(castle_labels, castle_values, castle_x):
        rect = Rectangle(
            (x, y3 - 0.8),
            1.0,
            1.0,
            facecolor=COLOURS["Beige"],
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect)
        ax.text(
            x + 0.5,
            y3 - 0.5,
            label,
            fontsize=FONT_SIZES["tiny"],
            color=COLOURS["Black"],
            ha="center",
            va="top",
        )
        ax.text(
            x + 0.5,
            y3 - 0.15,
            str(value),
            fontsize=FONT_SIZES["medium"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )

    # Routine: Straight, Variation
    routine_labels = ["STRAIGHT", "VARIATION"]
    routine_values = [straight, variation]
    routine_x = [6, 7.8]

    for label, value, x in zip(routine_labels, routine_values, routine_x):
        rect = Rectangle(
            (x, y3 - 0.8),
            1.5,
            1.0,
            facecolor=COLOURS["Beige"],
            edgecolor=COLOURS["Black"],
            linewidth=LINE_WIDTHS["thin"],
        )
        ax.add_patch(rect)
        ax.text(
            x + 0.75,
            y3 - 0.5,
            label,
            fontsize=FONT_SIZES["tiny"],
            color=COLOURS["Black"],
            ha="center",
            va="top",
        )
        ax.text(
            x + 0.75,
            y3 - 0.15,
            str(value),
            fontsize=FONT_SIZES["medium"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
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
        fontsize=FONT_SIZES["text"],
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
            fontsize=FONT_SIZES["medium_large"],
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
            fontsize=FONT_SIZES["medium_large"],
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
            fontsize=FONT_SIZES["extra_small"],
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )
        ax.text(
            x + 0.9,
            y_bottom + 0.25,
            str(value),
            fontsize=FONT_SIZES["medium_large"],
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
            fontsize=FONT_SIZES["extra_small"],
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )
        ax.text(
            x + 0.9,
            y_bottom2 + 0.25,
            str(value),
            fontsize=FONT_SIZES["medium_large"],
            fontweight="bold",
            color=COLOURS["Black"],
            ha="center",
            va="center",
        )
