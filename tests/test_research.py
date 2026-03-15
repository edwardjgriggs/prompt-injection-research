"""Research module tests — contract for all six research data modules."""
import pytest


# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------

class TestSources:
    def test_sources_importable(self):
        from src.research.sources import SOURCES
        assert isinstance(SOURCES, list)

    def test_sources_count(self):
        from src.research.sources import SOURCES
        assert len(SOURCES) >= 18, f"Expected 18+ sources, got {len(SOURCES)}"

    def test_sources_required_fields(self):
        from src.research.sources import SOURCES
        required = {"author", "year", "title", "source_type", "credibility", "url"}
        for i, src in enumerate(SOURCES):
            missing = required - set(src.keys())
            assert not missing, f"Source {i} ({src.get('title','?')}) missing fields: {missing}"

    def test_sources_field_values(self):
        from src.research.sources import SOURCES
        valid_types = {"academic", "industry", "government", "tool"}
        valid_cred = {"high", "medium"}
        for i, src in enumerate(SOURCES):
            assert src["source_type"] in valid_types, (
                f"Source {i} has invalid source_type: {src['source_type']}"
            )
            assert src["credibility"] in valid_cred, (
                f"Source {i} has invalid credibility: {src['credibility']}"
            )
            assert isinstance(src["year"], int), f"Source {i} year must be int"
            assert src["url"].startswith("http"), f"Source {i} URL invalid: {src['url']}"

    def test_sources_have_pillar_tags(self):
        from src.research.sources import SOURCES
        valid_pillars = {"taxonomy", "risks", "detection", "prevention"}
        for i, src in enumerate(SOURCES):
            tags = src.get("pillar_tags", [])
            assert isinstance(tags, list) and len(tags) > 0, (
                f"Source {i} ({src.get('title','?')}) must have at least one pillar_tag"
            )
            invalid = set(tags) - valid_pillars
            assert not invalid, f"Source {i} has invalid pillar_tags: {invalid}"


# ---------------------------------------------------------------------------
# References
# ---------------------------------------------------------------------------

class TestReferences:
    def test_references_importable(self):
        from src.research.references import REFERENCES
        assert isinstance(REFERENCES, list)

    def test_references_count_matches_sources(self):
        from src.research.sources import SOURCES
        from src.research.references import REFERENCES
        assert len(REFERENCES) == len(SOURCES), (
            f"REFERENCES ({len(REFERENCES)}) must match SOURCES ({len(SOURCES)})"
        )

    def test_references_are_strings(self):
        from src.research.references import REFERENCES
        for i, ref in enumerate(REFERENCES):
            assert isinstance(ref, str) and len(ref) > 20, (
                f"Reference {i} is not a valid citation string"
            )

    def test_references_apa_format(self):
        """Each reference should contain author, year in parens, and a period."""
        from src.research.references import REFERENCES
        for i, ref in enumerate(REFERENCES):
            assert "(" in ref and ")" in ref, (
                f"Reference {i} missing year in parentheses: {ref[:60]}"
            )
            stripped = ref.rstrip()
            ends_ok = (
                stripped.endswith(".")
                or stripped.endswith("/")
                or "http" in stripped.split()[-1]  # ends with a URL
            )
            assert ends_ok, (
                f"Reference {i} should end with period or URL: {ref[:60]}"
            )

    def test_references_alphabetical(self):
        from src.research.references import REFERENCES
        lowered = [r.lower() for r in REFERENCES]
        assert lowered == sorted(lowered), "REFERENCES must be in alphabetical order"


# ---------------------------------------------------------------------------
# Attack Taxonomy (T02)
# ---------------------------------------------------------------------------

class TestAttackTaxonomy:
    def test_taxonomy_importable(self):
        from src.research.taxonomy import ATTACK_TAXONOMY
        assert isinstance(ATTACK_TAXONOMY, list)

    def test_taxonomy_category_count(self):
        from src.research.taxonomy import ATTACK_TAXONOMY
        assert len(ATTACK_TAXONOMY) >= 6, (
            f"Expected 6+ taxonomy categories, got {len(ATTACK_TAXONOMY)}"
        )

    def test_taxonomy_has_subcategories(self):
        from src.research.taxonomy import ATTACK_TAXONOMY
        for cat in ATTACK_TAXONOMY:
            assert "category" in cat, f"Taxonomy entry missing 'category': {cat}"
            assert "description" in cat, f"Category {cat['category']} missing 'description'"
            subs = cat.get("subcategories", [])
            assert len(subs) >= 1, (
                f"Category {cat['category']} must have at least 1 subcategory"
            )


# ---------------------------------------------------------------------------
# Risk Categories (T02)
# ---------------------------------------------------------------------------

class TestRiskCategories:
    def test_risks_importable(self):
        from src.research.risks import RISK_CATEGORIES
        assert isinstance(RISK_CATEGORIES, list)

    def test_risks_count(self):
        from src.research.risks import RISK_CATEGORIES
        assert len(RISK_CATEGORIES) >= 4, (
            f"Expected 4+ risk categories, got {len(RISK_CATEGORIES)}"
        )

    def test_risks_have_examples(self):
        from src.research.risks import RISK_CATEGORIES
        for risk in RISK_CATEGORIES:
            assert "category" in risk, f"Risk entry missing 'category'"
            assert "description" in risk, f"Risk {risk.get('category')} missing 'description'"
            examples = risk.get("examples", [])
            assert len(examples) >= 1, (
                f"Risk {risk['category']} must have at least 1 example"
            )


# ---------------------------------------------------------------------------
# Detection Techniques (T02/T03)
# ---------------------------------------------------------------------------

class TestDetectionTechniques:
    def test_detection_importable(self):
        from src.research.detection import DETECTION_TECHNIQUES
        assert isinstance(DETECTION_TECHNIQUES, list)

    def test_detection_count(self):
        from src.research.detection import DETECTION_TECHNIQUES
        assert len(DETECTION_TECHNIQUES) >= 4, (
            f"Expected 4+ detection techniques, got {len(DETECTION_TECHNIQUES)}"
        )

    def test_detection_have_descriptions(self):
        from src.research.detection import DETECTION_TECHNIQUES
        for tech in DETECTION_TECHNIQUES:
            assert "technique" in tech, f"Detection entry missing 'technique'"
            assert "description" in tech and len(tech["description"]) > 20, (
                f"Detection {tech.get('technique')} needs a substantive description"
            )


# ---------------------------------------------------------------------------
# Prevention Strategies (T02/T03)
# ---------------------------------------------------------------------------

class TestPreventionStrategies:
    def test_prevention_importable(self):
        from src.research.prevention import PREVENTION_STRATEGIES
        assert isinstance(PREVENTION_STRATEGIES, list)

    def test_prevention_count(self):
        from src.research.prevention import PREVENTION_STRATEGIES
        assert len(PREVENTION_STRATEGIES) >= 4, (
            f"Expected 4+ prevention strategies, got {len(PREVENTION_STRATEGIES)}"
        )

    def test_prevention_have_descriptions(self):
        from src.research.prevention import PREVENTION_STRATEGIES
        for strat in PREVENTION_STRATEGIES:
            assert "strategy" in strat, f"Prevention entry missing 'strategy'"
            assert "description" in strat and len(strat["description"]) > 20, (
                f"Prevention {strat.get('strategy')} needs a substantive description"
            )


# ---------------------------------------------------------------------------
# Cross-module: Pillar Balance
# ---------------------------------------------------------------------------

class TestPillarBalance:
    def test_no_pillar_underrepresented(self):
        from src.research.sources import SOURCES
        pillar_counts = {"taxonomy": 0, "risks": 0, "detection": 0, "prevention": 0}
        for src in SOURCES:
            for tag in src.get("pillar_tags", []):
                if tag in pillar_counts:
                    pillar_counts[tag] += 1
        for pillar, count in pillar_counts.items():
            assert count >= 3, (
                f"Pillar '{pillar}' has only {count} sources (need 3+)"
            )
