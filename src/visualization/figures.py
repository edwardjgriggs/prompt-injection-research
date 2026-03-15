"""Publication-quality figure generation for prompt injection research paper.

All figures use a shared academic style: muted blues/grays, sans-serif fonts,
300 DPI output. Agg backend is set before any pyplot import to ensure
headless rendering.

Figures:
  - attack_taxonomy.png — hierarchical tree of 6 attack categories
  - defense_flow.png — layered defense strategy flow (T02)
  - architecture_diagram.png — system architecture overview (T02)
"""
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402
from pathlib import Path  # noqa: E402

from src.research.taxonomy import ATTACK_TAXONOMY  # noqa: E402

# ---------------------------------------------------------------------------
# Shared Style Configuration
# ---------------------------------------------------------------------------

# Muted academic palette — blues, grays, warm accents
COLORS = {
    "root": "#2C3E50",        # dark slate
    "category": "#2980B9",    # strong blue
    "subcategory": "#5DADE2", # light blue
    "cat_text": "#FFFFFF",
    "sub_text": "#1A252F",
    "root_text": "#FFFFFF",
    "edge": "#7F8C8D",        # gray
    "bg": "#FAFBFC",          # near-white
    "accent1": "#E67E22",     # warm orange (unused now, available for T02)
    "accent2": "#27AE60",     # green (unused now, available for T02)
    "accent3": "#8E44AD",     # purple (unused now, available for T02)
}

FONT = {
    "family": "sans-serif",
    "title": 11,
    "category": 8.5,
    "subcategory": 7,
    "root": 12,
}

OUTPUT_DIR_DEFAULT = Path(__file__).resolve().parent.parent.parent / "results" / "figures"


def _ensure_dir(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


# ---------------------------------------------------------------------------
# Attack Taxonomy — Horizontal Tree Chart
# ---------------------------------------------------------------------------

def generate_attack_taxonomy(output_dir: str | Path | None = None) -> Path:
    """Render the attack taxonomy as a horizontal tree chart.

    Root node on the left, 6 category nodes in the middle column,
    subcategory leaves on the right. Saved at 300 DPI.
    """
    out = _ensure_dir(Path(output_dir) if output_dir else OUTPUT_DIR_DEFAULT)
    categories = ATTACK_TAXONOMY

    # Layout constants
    n_cats = len(categories)
    # Count total subcategories for vertical spacing
    total_subs = sum(len(c["subcategories"]) for c in categories)

    fig_height = max(8, total_subs * 0.55 + 1)
    fig_width = 14
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, fig_height)
    ax.axis("off")

    # Column x-positions
    x_root = 0.5
    x_cat = 3.5
    x_sub = 7.5

    # Root node
    root_y = fig_height / 2
    _draw_box(ax, x_root, root_y, "Prompt Injection\nAttack Taxonomy",
              width=2.2, height=1.0,
              fc=COLORS["root"], tc=COLORS["root_text"],
              fontsize=FONT["root"], bold=True)

    # Distribute categories evenly
    cat_spacing = (fig_height - 1) / max(n_cats - 1, 1)
    cat_y_start = 0.5

    sub_idx = 0  # running index for vertical placement of subcategories
    for i, cat in enumerate(categories):
        cat_y = cat_y_start + i * cat_spacing
        # Shorten category label
        label = cat["category"]

        _draw_box(ax, x_cat, cat_y, label,
                  width=2.4, height=0.7,
                  fc=COLORS["category"], tc=COLORS["cat_text"],
                  fontsize=FONT["category"], bold=True)

        # Edge: root → category
        _draw_edge(ax, x_root + 1.1, root_y, x_cat - 1.2, cat_y)

        # Subcategories
        n_subs = len(cat["subcategories"])
        if n_subs == 1:
            sub_positions = [cat_y]
        else:
            spread = min(cat_spacing * 0.8, n_subs * 0.5)
            sub_positions = [
                cat_y - spread / 2 + j * spread / max(n_subs - 1, 1)
                for j in range(n_subs)
            ]

        for j, sub in enumerate(cat["subcategories"]):
            sy = sub_positions[j]
            _draw_box(ax, x_sub, sy, sub["name"],
                      width=2.2, height=0.45,
                      fc=COLORS["subcategory"], tc=COLORS["sub_text"],
                      fontsize=FONT["subcategory"], bold=False)
            _draw_edge(ax, x_cat + 1.2, cat_y, x_sub - 1.1, sy)

    # Title
    ax.text(fig_width / 2 / fig_width * 10.5, fig_height - 0.15,
            "Prompt Injection Attack Taxonomy",
            ha="center", va="top",
            fontsize=FONT["title"] + 2, fontweight="bold",
            fontfamily=FONT["family"], color=COLORS["root"])

    filepath = out / "attack_taxonomy.png"
    fig.savefig(filepath, dpi=300, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    w, h = fig.get_size_inches()
    print(f"Saved {filepath.name} ({w:.1f}×{h:.1f} in, 300 DPI)")
    plt.close(fig)
    return filepath


def _draw_box(ax, x, y, text, *, width, height, fc, tc, fontsize, bold):
    """Draw a rounded rectangle with centered text."""
    box = mpatches.FancyBboxPatch(
        (x - width / 2, y - height / 2), width, height,
        boxstyle="round,pad=0.12",
        facecolor=fc, edgecolor="#BDC3C7", linewidth=0.8,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center",
            fontsize=fontsize, fontfamily=FONT["family"],
            fontweight="bold" if bold else "normal",
            color=tc, zorder=3)


def _draw_edge(ax, x1, y1, x2, y2):
    """Draw a curved connector between two nodes."""
    mid_x = (x1 + x2) / 2
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="->,head_width=0.15,head_length=0.1",
            connectionstyle=f"arc3,rad=0.0",
            color=COLORS["edge"],
            linewidth=0.8,
        ),
    )


# ---------------------------------------------------------------------------
# Defense Flow (T02 placeholder)
# ---------------------------------------------------------------------------

def generate_defense_flow(output_dir: str | Path | None = None) -> Path:
    """Render the injection attack flow as a left-to-right pathway.

    Attacker → Input Channel (direct/indirect) → LLM Processing → Impact
    (data exfiltration, unauthorized actions, content manipulation,
    system compromise, supply chain propagation).
    """
    out = _ensure_dir(Path(output_dir) if output_dir else OUTPUT_DIR_DEFAULT)

    # Flow stages — defined inline since this is visual-specific
    stages = [
        {"label": "Attacker", "color": COLORS["accent1"]},
        {"label": "Input Channel", "color": COLORS["category"],
         "sub": ["Direct Injection\n(user prompt)", "Indirect Injection\n(external data)"]},
        {"label": "LLM\nProcessing", "color": COLORS["root"]},
        {"label": "Impact", "color": COLORS["accent3"],
         "sub": ["Data\nExfiltration", "Unauthorized\nActions",
                 "Content\nManipulation", "System\nCompromise",
                 "Supply Chain\nPropagation"]},
    ]

    fig_width, fig_height = 16, 7
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])
    ax.set_xlim(-0.5, 15.5)
    ax.set_ylim(-0.5, 6.5)
    ax.axis("off")

    # X positions for 4 main stages
    x_positions = [1.5, 5.0, 9.0, 13.0]
    main_y = 3.25

    for i, (stage, x) in enumerate(zip(stages, x_positions)):
        subs = stage.get("sub")
        if subs:
            # Draw sub-nodes vertically, with a group label above
            n = len(subs)
            spread = min(4.5, n * 1.0)
            y_start = main_y + spread / 2
            sub_ys = [y_start - j * spread / max(n - 1, 1) for j in range(n)] if n > 1 else [main_y]

            # Group label
            label_y = max(sub_ys) + 0.9
            ax.text(x, label_y, stage["label"],
                    ha="center", va="bottom",
                    fontsize=FONT["title"], fontweight="bold",
                    fontfamily=FONT["family"], color=stage["color"])

            for sy in sub_ys:
                _draw_box(ax, x, sy, subs[sub_ys.index(sy)],
                          width=2.2, height=0.65,
                          fc=stage["color"], tc="#FFFFFF",
                          fontsize=FONT["subcategory"], bold=False)

            # Arrows from previous stage to each sub
            if i > 0:
                prev_x = x_positions[i - 1]
                prev_stage = stages[i - 1]
                prev_subs = prev_stage.get("sub")
                if prev_subs:
                    n_prev = len(prev_subs)
                    prev_spread = min(4.5, n_prev * 1.0)
                    prev_y_start = main_y + prev_spread / 2
                    prev_sub_ys = [prev_y_start - j * prev_spread / max(n_prev - 1, 1) for j in range(n_prev)] if n_prev > 1 else [main_y]
                    for psy in prev_sub_ys:
                        for sy in sub_ys:
                            _draw_edge(ax, prev_x + 1.1, psy, x - 1.1, sy)
                else:
                    for sy in sub_ys:
                        _draw_edge(ax, prev_x + 1.1, main_y, x - 1.1, sy)

            # Arrows from each sub to next stage
            if i < len(stages) - 1:
                next_x = x_positions[i + 1]
                next_stage = stages[i + 1]
                next_subs = next_stage.get("sub")
                if not next_subs:
                    for sy in sub_ys:
                        _draw_edge(ax, x + 1.1, sy, next_x - 1.1, main_y)
        else:
            # Single main node
            _draw_box(ax, x, main_y, stage["label"],
                      width=2.2, height=1.0,
                      fc=stage["color"], tc="#FFFFFF",
                      fontsize=FONT["root"], bold=True)

            # Arrow to next
            if i < len(stages) - 1:
                next_x = x_positions[i + 1]
                next_stage = stages[i + 1]
                next_subs = next_stage.get("sub")
                if next_subs:
                    pass  # handled by next stage's incoming arrows
                else:
                    _draw_edge(ax, x + 1.1, main_y, next_x - 1.1, main_y)

    # Title
    ax.text(8.0, 6.2, "Prompt Injection Attack Flow",
            ha="center", va="top",
            fontsize=FONT["title"] + 2, fontweight="bold",
            fontfamily=FONT["family"], color=COLORS["root"])

    filepath = out / "defense_flow.png"
    fig.savefig(filepath, dpi=300, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    w, h = fig.get_size_inches()
    print(f"Saved {filepath.name} ({w:.1f}×{h:.1f} in, 300 DPI)")
    plt.close(fig)
    return filepath


# ---------------------------------------------------------------------------
# Defense Architecture — Three-Tier Diagram
# ---------------------------------------------------------------------------

def generate_architecture_diagram(output_dir: str | Path | None = None) -> Path:
    """Render the defense architecture as three horizontal tiers.

    Groups PREVENTION_STRATEGIES by implementation_level (model,
    application, system) and renders strategy boxes in each tier.
    """
    from src.research.prevention import PREVENTION_STRATEGIES

    out = _ensure_dir(Path(output_dir) if output_dir else OUTPUT_DIR_DEFAULT)

    # Group strategies by level
    tiers = {"model": [], "application": [], "system": []}
    for s in PREVENTION_STRATEGIES:
        level = s["implementation_level"]
        tiers.setdefault(level, []).append(s["strategy"])

    tier_order = ["system", "application", "model"]
    tier_colors = {
        "system": COLORS["accent3"],      # purple
        "application": COLORS["category"],  # blue
        "model": COLORS["accent2"],         # green
    }
    tier_labels = {
        "system": "System Level",
        "application": "Application Level",
        "model": "Model Level",
    }

    fig_width, fig_height = 14, 9
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # Draw tiers as horizontal bands
    tier_height = 2.2
    tier_gap = 0.3
    start_y = 0.8

    for i, level in enumerate(tier_order):
        y = start_y + i * (tier_height + tier_gap)
        strategies = tiers[level]
        color = tier_colors[level]

        # Tier background
        tier_bg = mpatches.FancyBboxPatch(
            (0.5, y), 13, tier_height,
            boxstyle="round,pad=0.15",
            facecolor=color, edgecolor=color,
            alpha=0.12, linewidth=1.5,
        )
        ax.add_patch(tier_bg)

        # Tier border
        tier_border = mpatches.FancyBboxPatch(
            (0.5, y), 13, tier_height,
            boxstyle="round,pad=0.15",
            facecolor="none", edgecolor=color,
            linewidth=1.5,
        )
        ax.add_patch(tier_border)

        # Tier label on the left
        ax.text(1.2, y + tier_height / 2, tier_labels[level],
                ha="left", va="center", rotation=90,
                fontsize=FONT["category"] + 1, fontweight="bold",
                fontfamily=FONT["family"], color=color)

        # Strategy boxes inside tier
        n = len(strategies)
        box_width = 3.2
        total_width = n * box_width + (n - 1) * 0.4
        x_start = 2.5 + (10.5 - total_width) / 2

        for j, strat in enumerate(strategies):
            bx = x_start + j * (box_width + 0.4)
            by = y + (tier_height - 1.2) / 2
            _draw_box(ax, bx + box_width / 2, by + 0.6, strat,
                      width=box_width, height=1.1,
                      fc=color, tc="#FFFFFF",
                      fontsize=FONT["category"], bold=True)

    # Title
    top_y = start_y + 3 * (tier_height + tier_gap) + 0.1
    ax.text(7.0, top_y, "Defense Architecture — Three-Tier Model",
            ha="center", va="bottom",
            fontsize=FONT["title"] + 2, fontweight="bold",
            fontfamily=FONT["family"], color=COLORS["root"])

    filepath = out / "architecture_diagram.png"
    fig.savefig(filepath, dpi=300, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    w, h = fig.get_size_inches()
    print(f"Saved {filepath.name} ({w:.1f}×{h:.1f} in, 300 DPI)")
    plt.close(fig)
    return filepath


# ---------------------------------------------------------------------------
# Convenience: generate all figures
# ---------------------------------------------------------------------------

def generate_all(output_dir: str | Path | None = None) -> list[Path]:
    """Generate all figures. Returns list of output paths."""
    results = []
    results.append(generate_attack_taxonomy(output_dir))
    results.append(generate_defense_flow(output_dir))
    results.append(generate_architecture_diagram(output_dir))
    return results
