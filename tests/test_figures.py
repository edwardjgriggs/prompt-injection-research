"""Tests for publication-quality figure generation.

Covers all three figures from S03: attack taxonomy, defense flow, and
architecture diagram. Tests for flow and defense will fail until T02
implements them — that's expected.
"""
import os
from pathlib import Path
from PIL import Image
import pytest

ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = ROOT / "results" / "figures"


def _check_figure(name: str):
    """Common assertions for any generated figure."""
    path = FIGURES_DIR / name
    assert path.exists(), f"Missing figure: {path}"
    assert path.stat().st_size > 10_000, f"Figure too small (<10KB): {path}"
    img = Image.open(path)
    dpi = img.info.get("dpi", (72, 72))
    assert dpi[0] >= 299.99, f"DPI too low: {dpi[0]} (need ≥300)"


# --- Attack Taxonomy ---

def test_attack_taxonomy_exists():
    from src.visualization.figures import generate_attack_taxonomy
    generate_attack_taxonomy()
    _check_figure("attack_taxonomy.png")


def test_attack_taxonomy_importable():
    from src.visualization.figures import generate_attack_taxonomy
    assert callable(generate_attack_taxonomy)


# --- Defense Flow ---

def test_defense_flow_exists():
    from src.visualization.figures import generate_defense_flow
    generate_defense_flow()
    _check_figure("defense_flow.png")


def test_defense_flow_importable():
    from src.visualization.figures import generate_defense_flow
    assert callable(generate_defense_flow)


# --- Architecture Diagram ---

def test_architecture_diagram_exists():
    from src.visualization.figures import generate_architecture_diagram
    generate_architecture_diagram()
    _check_figure("architecture_diagram.png")


def test_architecture_diagram_importable():
    from src.visualization.figures import generate_architecture_diagram
    assert callable(generate_architecture_diagram)
