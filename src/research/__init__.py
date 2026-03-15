"""Research data modules for prompt injection paper.

Provides curated sources, APA references, and (when available)
pillar data: taxonomy, risks, detection, prevention.
"""

from src.research.sources import SOURCES
from src.research.references import REFERENCES

# Pillar modules — imported when available (T02/T03 create these)
try:
    from src.research.taxonomy import ATTACK_TAXONOMY
except ImportError:
    ATTACK_TAXONOMY = None

try:
    from src.research.risks import RISK_CATEGORIES
except ImportError:
    RISK_CATEGORIES = None

try:
    from src.research.detection import DETECTION_TECHNIQUES
except ImportError:
    DETECTION_TECHNIQUES = None

try:
    from src.research.prevention import PREVENTION_STRATEGIES
except ImportError:
    PREVENTION_STRATEGIES = None

__all__ = [
    "SOURCES",
    "REFERENCES",
    "ATTACK_TAXONOMY",
    "RISK_CATEGORIES",
    "DETECTION_TECHNIQUES",
    "PREVENTION_STRATEGIES",
]
