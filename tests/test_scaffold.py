"""Scaffold verification tests — confirm project structure is correct."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_source_packages_exist():
    packages = ["src", "src/research", "src/visualization", "src/paper", "src/presentation"]
    for pkg in packages:
        init = ROOT / pkg / "__init__.py"
        assert init.exists(), f"Missing {init}"


def test_source_packages_importable():
    import src
    import src.research
    import src.visualization
    import src.paper
    import src.presentation


def test_tests_package_exists():
    assert (ROOT / "tests" / "__init__.py").exists()


def test_output_directories_exist():
    assert (ROOT / "results" / "figures" / ".gitkeep").exists()
    assert (ROOT / "output" / ".gitkeep").exists()


def test_config_files_exist():
    assert (ROOT / "requirements.txt").exists()
    assert (ROOT / "pytest.ini").exists()


def test_requirements_content():
    reqs = (ROOT / "requirements.txt").read_text()
    for dep in ["python-docx", "python-pptx", "matplotlib", "pytest"]:
        assert dep in reqs, f"Missing {dep} in requirements.txt"
