"""Generate APA 7th edition research paper on prompt injection.

Composes structured research data from src.research modules into a
formatted .docx file with embedded figures and proper references.

Usage:
    python -m src.paper.generate
"""

import os
from pathlib import Path
from datetime import date

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_ORIENT

from src.research.taxonomy import ATTACK_TAXONOMY
from src.research.risks import RISK_CATEGORIES
from src.research.detection import DETECTION_TECHNIQUES
from src.research.prevention import PREVENTION_STRATEGIES
from src.research.references import REFERENCES

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
FIGURES_DIR = PROJECT_ROOT / "results" / "figures"

FIGURE_FILES = [
    ("attack_taxonomy.png", "Figure 1. Hierarchical taxonomy of prompt injection attack vectors."),
    ("defense_flow.png", "Figure 2. Detection and defense pipeline for prompt injection mitigation."),
    ("architecture_diagram.png", "Figure 3. System architecture for layered prompt injection defense."),
]

PAPER_TITLE = (
    "Prompt Injection Attacks in Large Language Models: "
    "A Survey of Attack Taxonomies, Risks, Detection, and Prevention"
)
AUTHOR = "Edward Research Group"
INSTITUTION = "Cybersecurity Research Division"


def _set_apa_defaults(doc: Document):
    """Configure document-wide APA 7th formatting."""
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Times New Roman"
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)

    pf = style.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    pf.space_after = Pt(0)
    pf.space_before = Pt(0)

    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Configure heading styles
    for level, size in [(1, 14), (2, 13), (3, 12)]:
        style_name = f"Heading {level}"
        if style_name in doc.styles:
            hs = doc.styles[style_name]
            hs.font.name = "Times New Roman"
            hs.font.size = Pt(size)
            hs.font.bold = True
            hs.font.color.rgb = RGBColor(0, 0, 0)
            hs.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
            hs.paragraph_format.space_before = Pt(12)
            hs.paragraph_format.space_after = Pt(6)
            if level == 1:
                hs.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER


def _add_title_page(doc: Document):
    """Add APA 7th title page."""
    # Blank lines to push title to upper-third
    for _ in range(6):
        doc.add_paragraph("")

    title_para = doc.add_paragraph()
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title_para.add_run(PAPER_TITLE)
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = "Times New Roman"

    doc.add_paragraph("")

    author_para = doc.add_paragraph()
    author_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = author_para.add_run(AUTHOR)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)

    inst_para = doc.add_paragraph()
    inst_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = inst_para.add_run(INSTITUTION)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)

    date_para = doc.add_paragraph()
    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = date_para.add_run(date.today().strftime("%B %d, %Y"))
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)

    doc.add_page_break()


def _add_body_paragraph(doc: Document, text: str):
    """Add a double-spaced body paragraph with first-line indent."""
    para = doc.add_paragraph(text)
    para.paragraph_format.first_line_indent = Inches(0.5)
    return para


def _add_abstract(doc: Document):
    """Add the Abstract section."""
    print("Writing section: Abstract...")
    doc.add_heading("Abstract", level=1)

    abstract_text = (
        "This survey examines the rapidly evolving landscape of prompt injection attacks "
        "targeting large language models (LLMs) and LLM-integrated applications. As LLMs "
        "become deeply embedded in enterprise workflows, agentic systems, and consumer "
        "applications, prompt injection has emerged as a fundamental security vulnerability "
        "that threatens the integrity, confidentiality, and reliability of AI-powered systems. "
        "This paper presents a comprehensive taxonomy of prompt injection attack vectors — "
        "spanning direct injection, indirect injection, multimodal attacks, tool and agent-based "
        "exploitation, hybrid chained techniques, and autonomous propagating threats. The survey "
        "analyzes the risk landscape across five impact categories: data exfiltration, unauthorized "
        "actions, content manipulation, system compromise, and supply chain propagation. Detection "
        "approaches are evaluated including heuristic methods, machine learning classification, "
        "perplexity analysis, canary tokens, and LLM-as-judge architectures. Prevention strategies "
        "are assessed across model-level, application-level, and system-level defenses, including "
        "instruction hierarchy, input sanitization, guardrail frameworks, sandboxing, and "
        "architectural patterns. The paper synthesizes findings from 18 primary sources published "
        "between 2023 and 2025, revealing that prompt injection remains a largely unsolved problem "
        "due to the fundamental inability of current LLM architectures to reliably distinguish "
        "between instructions and data. The survey concludes with recommendations for defense-in-depth "
        "strategies and identifies critical gaps requiring further research."
    )
    para = doc.add_paragraph(abstract_text)
    para.paragraph_format.first_line_indent = Inches(0)

    # Keywords
    kw_para = doc.add_paragraph()
    kw_para.paragraph_format.first_line_indent = Inches(0.5)
    run = kw_para.add_run("Keywords: ")
    run.italic = True
    kw_para.add_run(
        "prompt injection, large language models, adversarial attacks, "
        "AI security, jailbreaking, indirect injection, LLM safety"
    )

    doc.add_page_break()


def _add_introduction(doc: Document):
    """Add the Introduction section."""
    print("Writing section: Introduction...")
    doc.add_heading("Introduction", level=1)

    paras = [
        (
            "Large language models have transformed the landscape of artificial intelligence, "
            "enabling applications ranging from conversational assistants and code generation to "
            "autonomous agents capable of executing multi-step tasks with real-world consequences. "
            "As these models become integrated into critical infrastructure — enterprise workflows, "
            "financial systems, healthcare applications, and government services — the security "
            "implications of their deployment have become a pressing concern for the cybersecurity "
            "community."
        ),
        (
            "Prompt injection, first identified as a distinct vulnerability class in 2022, exploits "
            "a fundamental architectural limitation of current LLMs: the inability to reliably "
            "distinguish between trusted instructions and untrusted data within the same input "
            "stream. Unlike traditional software vulnerabilities that exploit implementation flaws, "
            "prompt injection attacks target the core operational mechanism of language models — "
            "their tendency to follow any instruction-like content in their context window, "
            "regardless of its source or intent."
        ),
        (
            "The OWASP Foundation recognized prompt injection as the number one vulnerability in "
            "their 2025 Top 10 for Large Language Model Applications, reflecting the severity and "
            "prevalence of this threat. The National Institute of Standards and Technology (NIST) "
            "included prompt injection in their 2025 taxonomy of adversarial machine learning "
            "attacks, further validating its significance within the broader cybersecurity landscape. "
            "The attack surface has expanded dramatically with the proliferation of agentic AI "
            "systems that combine language models with tool-use capabilities, where a successful "
            "prompt injection can cascade from text manipulation to unauthorized code execution, "
            "data exfiltration, and system compromise."
        ),
        (
            "This survey provides a structured examination of prompt injection across four pillars: "
            "attack taxonomy, risk analysis, detection techniques, and prevention strategies. By "
            "synthesizing findings from 18 primary sources spanning academic research, industry "
            "reports, and government standards published between 2023 and 2025, this paper aims "
            "to provide researchers and practitioners with a comprehensive understanding of the "
            "current threat landscape and the state of defensive capabilities."
        ),
    ]
    for text in paras:
        _add_body_paragraph(doc, text)


def _add_literature_review(doc: Document):
    """Add the Literature Review with four subsections and embedded figures."""
    print("Writing section: Literature Review...")
    doc.add_heading("Literature Review", level=1)

    _add_body_paragraph(doc, (
        "The following literature review is organized around four pillars that structure "
        "the current understanding of prompt injection: attack taxonomy and classification, "
        "risk analysis and impact assessment, detection techniques, and prevention strategies. "
        "Each subsection synthesizes findings from multiple sources to present a balanced "
        "view of the current state of knowledge."
    ))

    # --- Taxonomy subsection ---
    _add_taxonomy_subsection(doc)

    # --- Risks subsection ---
    _add_risks_subsection(doc)

    # --- Detection subsection ---
    _add_detection_subsection(doc)

    # --- Prevention subsection ---
    _add_prevention_subsection(doc)


def _add_taxonomy_subsection(doc: Document):
    """Attack Taxonomy and Classification subsection."""
    print("  Writing subsection: Attack Taxonomy...")
    doc.add_heading("Attack Taxonomy and Classification", level=2)

    _add_body_paragraph(doc, (
        "The classification of prompt injection attacks has evolved rapidly as new attack "
        "vectors emerge alongside advances in LLM capabilities. This survey adopts a six-category "
        "hierarchical taxonomy synthesized from multiple authoritative sources, including the "
        "comprehensive review by Abdallah et al. (2025), the hybrid threat framework by Ahmed "
        "et al. (2025), and the foundational work of Greshake et al. (2023) on indirect injection."
    ))

    for category in ATTACK_TAXONOMY:
        doc.add_heading(category["category"], level=3)
        _add_body_paragraph(doc, category["description"])

        # Add subcategories as prose
        for sub in category["subcategories"]:
            _add_body_paragraph(doc, (
                f"{sub['name']}. {sub['description']} "
                f"Documented examples include {sub['examples'][0].lower()} "
                f"and {sub['examples'][1].lower()}."
            ))

    # Embed Figure 1 after taxonomy
    _embed_figure(doc, 0)

    _add_body_paragraph(doc, (
        "Figure 1 illustrates the hierarchical relationships among these attack categories, "
        "showing how the taxonomy progresses from well-understood direct injection techniques "
        "to emerging autonomous and propagating threats. The increasing complexity of attack "
        "vectors reflects the expanding capabilities of LLM-integrated systems and the growing "
        "sophistication of adversarial techniques."
    ))


def _add_risks_subsection(doc: Document):
    """Risk Analysis subsection."""
    print("  Writing subsection: Risk Analysis...")
    doc.add_heading("Risk Analysis and Impact Assessment", level=2)

    _add_body_paragraph(doc, (
        "The impact of prompt injection extends far beyond the manipulation of model outputs. "
        "As LLMs are integrated with tools, APIs, and autonomous decision-making capabilities, "
        "successful injection attacks can cause real-world harm across multiple dimensions. "
        "This section examines five risk categories identified through analysis of documented "
        "incidents, vulnerability disclosures, and security research."
    ))

    for risk in RISK_CATEGORIES:
        doc.add_heading(risk["category"], level=3)
        _add_body_paragraph(doc, risk["description"])
        _add_body_paragraph(doc, (
            f"This risk category has been assessed as {risk['severity']} severity, "
            f"affecting systems including {', '.join(risk['affected_systems'][:2])}. "
            f"Documented examples include {risk['examples'][0].lower()}."
        ))


def _add_detection_subsection(doc: Document):
    """Detection Techniques subsection."""
    print("  Writing subsection: Detection Techniques...")
    doc.add_heading("Detection Techniques", level=2)

    _add_body_paragraph(doc, (
        "Detecting prompt injection attacks remains a significant challenge due to the "
        "fundamental difficulty of distinguishing adversarial instructions from legitimate "
        "user input in natural language. Current detection approaches span a spectrum from "
        "simple pattern matching to sophisticated model-based evaluation, each with distinct "
        "tradeoffs between accuracy, latency, and robustness."
    ))

    for technique in DETECTION_TECHNIQUES:
        doc.add_heading(technique["technique"], level=3)
        _add_body_paragraph(doc, technique["description"])
        _add_body_paragraph(doc, (
            f"This {technique['approach_type']} approach is exemplified by tools such as "
            f"{technique['tools_examples'][0]}. However, {technique['limitations']}"
        ))

    # Embed Figure 2 after detection
    _embed_figure(doc, 1)

    _add_body_paragraph(doc, (
        "Figure 2 illustrates the detection and defense pipeline, showing how multiple "
        "detection layers can be composed in sequence to improve overall detection rates. "
        "The multi-layered approach reflects the defense-in-depth principle: no single "
        "detection method provides sufficient coverage, but their combination significantly "
        "reduces the probability of a successful attack evading all layers."
    ))


def _add_prevention_subsection(doc: Document):
    """Prevention Strategies subsection."""
    print("  Writing subsection: Prevention Strategies...")
    doc.add_heading("Prevention Strategies", level=2)

    _add_body_paragraph(doc, (
        "Prevention strategies for prompt injection operate at three levels: model-level "
        "defenses that modify how the LLM processes instructions, application-level controls "
        "that filter inputs and outputs, and system-level architectural patterns that limit "
        "the blast radius of successful attacks. This section evaluates six major prevention "
        "approaches and their practical tradeoffs."
    ))

    for strategy in PREVENTION_STRATEGIES:
        doc.add_heading(strategy["strategy"], level=3)
        _add_body_paragraph(doc, strategy["description"])
        _add_body_paragraph(doc, (
            f"Operating at the {strategy['implementation_level']} level, this strategy is "
            f"implemented through approaches such as {strategy['tools_examples'][0]}. "
            f"{strategy['effectiveness']}"
        ))

    # Embed Figure 3 after prevention
    _embed_figure(doc, 2)

    _add_body_paragraph(doc, (
        "Figure 3 presents the system architecture for a layered prompt injection defense, "
        "illustrating how model-level, application-level, and system-level controls integrate "
        "to form a comprehensive defense posture. The architecture emphasizes that effective "
        "defense requires coordination across all three levels, as no single layer provides "
        "complete protection against the full spectrum of attack vectors."
    ))


def _embed_figure(doc: Document, index: int):
    """Embed a figure with caption at the current position."""
    filename, caption_text = FIGURE_FILES[index]
    figure_path = FIGURES_DIR / filename

    if not figure_path.exists():
        raise FileNotFoundError(
            f"Figure not found: {figure_path}. "
            f"Ensure results/figures/{filename} exists before generating the paper."
        )

    # Add the image centered
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    run.add_picture(str(figure_path), width=Inches(5.5))

    # Caption paragraph
    caption_para = doc.add_paragraph()
    caption_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption_para.paragraph_format.space_after = Pt(12)
    run = caption_para.add_run(caption_text)
    run.italic = True
    run.font.size = Pt(10)
    run.font.name = "Times New Roman"


def _add_methodology(doc: Document):
    """Add the Methodology section."""
    print("Writing section: Methodology...")
    doc.add_heading("Methodology", level=1)

    paras = [
        (
            "This research employs a structured literature survey methodology to examine "
            "the current state of prompt injection attacks and defenses. The survey follows "
            "a systematic approach to source selection, categorization, and synthesis designed "
            "to provide comprehensive coverage while maintaining analytical rigor."
        ),
        (
            "Source selection targeted four categories of publications: peer-reviewed academic "
            "papers from arXiv and journals, industry reports from major cybersecurity firms "
            "and AI companies, government standards and frameworks, and documentation from "
            "open-source security tools. A total of 18 primary sources published between 2023 "
            "and 2025 were selected based on relevance, credibility, and recency. Academic "
            "sources were prioritized for theoretical foundations and empirical findings, while "
            "industry and government sources provided practical context and standardized "
            "frameworks."
        ),
        (
            "The analysis framework organizes findings across four pillars: attack taxonomy "
            "and classification, risk analysis and impact assessment, detection techniques, "
            "and prevention strategies. Each pillar draws from multiple sources to enable "
            "cross-validation and identify areas of consensus and disagreement. The taxonomy "
            "was constructed through iterative synthesis, beginning with established categories "
            "from Greshake et al. (2023) and extending to incorporate emerging threat vectors "
            "documented in 2024-2025 publications."
        ),
        (
            "Limitations of this methodology include publication bias toward well-documented "
            "attack vectors, the rapid pace of development in the field which may render some "
            "findings outdated, and the difficulty of verifying effectiveness claims for "
            "defensive tools in the absence of standardized benchmarks. The survey scope is "
            "limited to prompt injection specifically and does not cover other LLM security "
            "concerns such as training data poisoning or model extraction attacks."
        ),
    ]
    for text in paras:
        _add_body_paragraph(doc, text)


def _add_discussion(doc: Document):
    """Add the Discussion section."""
    print("Writing section: Discussion...")
    doc.add_heading("Discussion", level=1)

    paras = [
        (
            "The synthesis of findings across the four pillars reveals several critical insights "
            "about the current state of prompt injection as a cybersecurity threat. First, the "
            "attack taxonomy demonstrates a clear trajectory of increasing sophistication — from "
            "simple direct injection techniques that emerged in 2022 to complex autonomous "
            "propagating threats documented in 2024-2025. This evolution parallels the expansion "
            "of LLM capabilities, particularly the addition of tool use, web browsing, and "
            "multi-agent orchestration that dramatically increase the attack surface."
        ),
        (
            "Second, the risk analysis reveals that prompt injection has crossed the threshold "
            "from a theoretical AI safety concern to a practical cybersecurity vulnerability with "
            "real-world impact. The ability to cause data exfiltration, unauthorized actions, and "
            "system compromise through prompt injection places it alongside traditional "
            "vulnerability classes such as SQL injection and cross-site scripting — but with "
            "the added complexity that the vulnerability exists in natural language processing "
            "rather than structured data parsing."
        ),
        (
            "Third, the detection landscape shows promising but insufficient progress. While "
            "multi-layered detection architectures combining heuristic, ML-based, and LLM-as-judge "
            "approaches achieve reasonable detection rates for known attack patterns, the "
            "fundamental challenge remains: novel injection techniques can be constructed more "
            "quickly than detection systems can adapt. The analogy to the antivirus industry's "
            "signature-based detection era is instructive — reactive detection alone cannot "
            "provide adequate security against a motivated adversary."
        ),
        (
            "Fourth, the prevention strategy assessment suggests that no single defense mechanism "
            "is sufficient. The instruction hierarchy approach (Wallace et al., 2024) represents "
            "the most theoretically promising model-level defense, but it requires training-time "
            "modifications that are unavailable to application developers. Application-level "
            "controls such as input sanitization and guardrail frameworks provide practical "
            "defense-in-depth but cannot guarantee complete protection. System-level architectural "
            "patterns offer the strongest containment through sandboxing and privilege restriction, "
            "but at the cost of reduced LLM autonomy and capability."
        ),
        (
            "The implications for practitioners are clear: organizations deploying LLM-integrated "
            "systems must adopt defense-in-depth strategies that combine multiple prevention layers "
            "rather than relying on any single mitigation. The principle of least privilege should "
            "govern all tool access granted to LLM agents. Human-in-the-loop confirmation should "
            "be required for irreversible or high-impact operations. And security teams should "
            "treat prompt injection with the same rigor applied to traditional web application "
            "vulnerabilities, including regular testing, monitoring, and incident response planning."
        ),
    ]
    for text in paras:
        _add_body_paragraph(doc, text)


def _add_conclusion(doc: Document):
    """Add the Conclusion section."""
    print("Writing section: Conclusion...")
    doc.add_heading("Conclusion", level=1)

    paras = [
        (
            "This survey has examined prompt injection attacks across four dimensions: "
            "taxonomy, risks, detection, and prevention. The analysis reveals that prompt "
            "injection represents a fundamental and largely unsolved challenge in LLM security, "
            "rooted in the architectural inability of current language models to reliably "
            "distinguish between instructions and data within their context window."
        ),
        (
            "The attack taxonomy has grown from simple direct injection techniques to encompass "
            "indirect injection through external data sources, multimodal attacks exploiting "
            "vision and audio channels, tool and agent-based exploitation of agentic AI systems, "
            "hybrid chained attacks that combine multiple vectors, and autonomous propagating "
            "threats that can spread without continued attacker involvement. Each new category "
            "reflects the expanding capabilities and deployment contexts of modern LLMs."
        ),
        (
            "The current state of detection and prevention offers practical defenses but no "
            "complete solutions. Defense-in-depth strategies combining instruction hierarchy, "
            "input and output filtering, guardrail frameworks, and architectural sandboxing "
            "provide meaningful risk reduction. However, the fundamental vulnerability persists "
            "as an inherent property of the transformer architecture's treatment of all context "
            "window content as equally authoritative."
        ),
        (
            "Future research directions include the development of formal verification methods "
            "for LLM instruction compliance, standardized benchmarks for evaluating prompt "
            "injection defenses, and architectural innovations that create genuine separation "
            "between instruction and data processing pathways. Until such advances materialize, "
            "the cybersecurity community must treat prompt injection as a persistent threat "
            "requiring continuous monitoring, testing, and adaptive defense strategies."
        ),
    ]
    for text in paras:
        _add_body_paragraph(doc, text)


def _add_references(doc: Document):
    """Add the References section with APA hanging indent."""
    print("Writing section: References...")
    doc.add_page_break()
    doc.add_heading("References", level=1)

    for ref in REFERENCES:
        para = doc.add_paragraph(ref)
        # Hanging indent: 0.5 inch left indent, -0.5 inch first line (net: first line at 0)
        para.paragraph_format.left_indent = Inches(0.5)
        para.paragraph_format.first_line_indent = Inches(-0.5)
        para.paragraph_format.space_after = Pt(0)


def generate_paper():
    """Generate the complete research paper and write to output/research_paper.docx."""
    print("Generating research paper...")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "research_paper.docx"

    doc = Document()
    _set_apa_defaults(doc)
    _add_title_page(doc)
    _add_abstract(doc)
    _add_introduction(doc)
    _add_literature_review(doc)
    _add_methodology(doc)
    _add_discussion(doc)
    _add_conclusion(doc)
    _add_references(doc)

    doc.save(str(output_path))
    print(f"Paper saved to {output_path}")
    print(f"File size: {output_path.stat().st_size:,} bytes")
    return output_path


if __name__ == "__main__":
    generate_paper()
