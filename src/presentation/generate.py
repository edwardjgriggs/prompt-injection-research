"""Generate a dark-themed conference presentation on prompt injection.

Composes structured research data from src.research modules into a
~13-slide .pptx with dark backgrounds, speaker notes, and embedded figures.

Usage:
    python -m src.presentation.generate
"""

import os
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from src.research.taxonomy import ATTACK_TAXONOMY
from src.research.risks import RISK_CATEGORIES
from src.research.detection import DETECTION_TECHNIQUES
from src.research.prevention import PREVENTION_STRATEGIES
from src.research.references import REFERENCES

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
FIGURES_DIR = PROJECT_ROOT / "results" / "figures"

# Theme colors
BG_COLOR = RGBColor(30, 30, 30)
TEXT_COLOR = RGBColor(230, 230, 230)
HEADING_COLOR = RGBColor(100, 180, 255)
ACCENT_COLOR = RGBColor(255, 170, 60)
SUBTITLE_COLOR = RGBColor(180, 180, 180)

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


def _set_dark_bg(slide):
    """Apply solid dark background fill to a slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR


def _add_textbox(slide, left, top, width, height):
    """Add a textbox and return it."""
    return slide.shapes.add_textbox(left, top, width, height)


def _set_text(textbox, text, *, font_size=18, color=TEXT_COLOR, bold=False, alignment=PP_ALIGN.LEFT):
    """Set text on a textbox's first paragraph."""
    tf = textbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.alignment = alignment


def _add_heading(slide, text, top=Inches(0.4)):
    """Add a heading textbox at the top of a slide."""
    tb = _add_textbox(slide, Inches(0.8), top, Inches(11.5), Inches(0.8))
    _set_text(tb, text, font_size=32, color=HEADING_COLOR, bold=True)
    return tb


def _add_bullets(slide, items, *, left=Inches(0.8), top=Inches(1.5), width=Inches(11.5),
                 height=Inches(5.0), font_size=18, color=TEXT_COLOR, max_items=None):
    """Add a bulleted list to a slide."""
    tb = _add_textbox(slide, left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    display_items = items[:max_items] if max_items else items
    for i, item in enumerate(display_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {item}"
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.space_after = Pt(6)


def _add_notes(slide, text):
    """Add speaker notes to a slide."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = text


def _add_figure(slide, filename, left=Inches(1.0), top=Inches(1.5),
                width=Inches(5.5), height=None):
    """Embed a figure image on a slide. Returns True if successful."""
    path = FIGURES_DIR / filename
    if not path.exists():
        print(f"  WARNING: Figure not found: {path}")
        return False
    if height:
        slide.shapes.add_picture(str(path), left, top, width, height)
    else:
        slide.shapes.add_picture(str(path), left, top, width)
    print(f"  Embedded figure: {filename}")
    return True


def generate_presentation() -> Path:
    """Build and save the presentation, returning the output path."""
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    blank_layout = prs.slide_layouts[6]  # blank layout

    # --- Slide 1: Title ---
    print("Creating slide 1: Title")
    slide = prs.slides.add_slide(blank_layout)
    _set_dark_bg(slide)
    tb = _add_textbox(slide, Inches(1), Inches(2), Inches(11), Inches(2))
    _set_text(tb, "Prompt Injection Attacks in Large Language Models",
              font_size=36, color=HEADING_COLOR, bold=True, alignment=PP_ALIGN.CENTER)
    tb2 = _add_textbox(slide, Inches(1), Inches(4.2), Inches(11), Inches(1))
    _set_text(tb2, "A Survey of Attack Taxonomies, Risks, Detection, and Prevention",
              font_size=22, color=SUBTITLE_COLOR, alignment=PP_ALIGN.CENTER)
    tb3 = _add_textbox(slide, Inches(1), Inches(5.5), Inches(11), Inches(0.6))
    _set_text(tb3, "Cybersecurity Research Division",
              font_size=18, color=SUBTITLE_COLOR, alignment=PP_ALIGN.CENTER)

    # --- Slide 2: Agenda / Overview ---
    print("Creating slide 2: Agenda")
    slide = prs.slides.add_slide(blank_layout)
    _set_dark_bg(slide)
    _add_heading(slide, "Presentation Overview")
    _add_bullets(slide, [
        "What is prompt injection?",
        "Attack taxonomy — direct and indirect vectors",
        "Real-world risks and impact categories",
        "Detection techniques and tools",
        "Prevention strategies and defense architecture",
        "Key references and future directions",
    ])
    _add_notes(slide, "[~30s] Welcome audience. Outline the four research pillars: taxonomy, risks, detection, prevention. Set expectation for 5-8 min talk.")

    # --- Slide 3: What is Prompt Injection? ---
    print("Creating slide 3: Introduction")
    slide = prs.slides.add_slide(blank_layout)
    _set_dark_bg(slide)
    _add_heading(slide, "What is Prompt Injection?")
    _add_bullets(slide, [
        "Adversarial inputs that hijack LLM behavior by overriding system instructions",
        "Analogous to SQL injection — exploits the blurred boundary between code and data",
        "Ranked #1 on the OWASP Top 10 for LLM Applications (LLM01)",
        "Affects all major LLM platforms: ChatGPT, Claude, Gemini, Copilot",
        "Two primary vectors: direct injection (user input) and indirect injection (external data)",
    ])
    _add_notes(slide, "[~45s] Define prompt injection clearly. Emphasize the SQL injection analogy — audience likely familiar with web security. Mention OWASP ranking to establish severity.")

    # --- Slides 4-5: Attack Taxonomy ---
    print("Creating slides 4-5: Attack Taxonomy")
    for idx, category in enumerate(ATTACK_TAXONOMY[:2]):
        slide = prs.slides.add_slide(blank_layout)
        _set_dark_bg(slide)
        _add_heading(slide, f"Attack Taxonomy: {category['category']}")
        subcats = category.get("subcategories", [])
        bullet_items = []
        for sub in subcats[:5]:
            name = sub.get("name", sub.get("technique", ""))
            desc = sub.get("description", "")
            # Truncate description for slide readability
            short = desc[:120] + "..." if len(desc) > 120 else desc
            bullet_items.append(f"{name}: {short}")
        _add_bullets(slide, bullet_items, font_size=16)
        _add_notes(slide, f"[~45s] Cover {category['category']} injection. Highlight key subcategories and give one concrete example for each.")

    # --- Slide 6: Attack Taxonomy Figure ---
    print("Creating slide 6: Taxonomy figure")
    slide = prs.slides.add_slide(blank_layout)
    _set_dark_bg(slide)
    _add_heading(slide, "Attack Taxonomy Visualization")
    _add_figure(slide, "attack_taxonomy.png", left=Inches(2), top=Inches(1.5),
                width=Inches(9), height=Inches(5.2))
    _add_notes(slide, "[~30s] Walk through the taxonomy diagram. Point out the hierarchy from category to specific technique.")

    # --- Slides 7-8: Risks ---
    print("Creating slides 7-8: Risks")
    # Slide 7: Critical risks
    slide = prs.slides.add_slide(blank_layout)
    _set_dark_bg(slide)
    _add_heading(slide, "Real-World Risks: Critical Impact")
    critical = [r for r in RISK_CATEGORIES if r.get("severity") == "critical"]
    bullet_items = []
    for r in critical[:4]:
        examples = r.get("examples", [])
        ex = examples[0][:100] + "..." if examples else ""
        bullet_items.append(f"{r['category']}: {ex}")
    _add_bullets(slide, bullet_items, font_size=16)
    _add_notes(slide, "[~45s] Emphasize data exfiltration and unauthorized actions as highest-severity outcomes. Give the markdown image exfiltration example — it's vivid and memorable.")

    # Slide 8: Other risks
    slide = prs.slides.add_slide(blank_layout)
    _set_dark_bg(slide)
    _add_heading(slide, "Risks: Broader Impact Categories")
    other = [r for r in RISK_CATEGORIES if r.get("severity") != "critical"]
    bullet_items = [f"{r['category']} ({r.get('severity', 'N/A')}): {r['description'][:100]}..." for r in other[:5]]
    _add_bullets(slide, bullet_items, font_size=16)
    _add_notes(slide, "[~30s] Cover remaining risk categories briefly. Highlight that impact scales with agent permission scope.")

    # --- Slide 9: Detection Techniques ---
    print("Creating slide 9: Detection")
    slide = prs.slides.add_slide(blank_layout)
    _set_dark_bg(slide)
    _add_heading(slide, "Detection Techniques")
    bullet_items = []
    for t in DETECTION_TECHNIQUES[:5]:
        tools = ", ".join(t.get("tools_examples", [])[:2])
        bullet_items.append(f"{t['technique']} ({t.get('approach_type', '')}): {tools}")
    _add_bullets(slide, bullet_items, font_size=16)
    _add_notes(slide, "[~45s] Compare static vs learned approaches. Note that no single detection method is sufficient — defense in depth is required.")

    # --- Slide 10: Defense Flow Figure ---
    print("Creating slide 10: Defense flow figure")
    slide = prs.slides.add_slide(blank_layout)
    _set_dark_bg(slide)
    _add_heading(slide, "Detection & Defense Pipeline")
    _add_figure(slide, "defense_flow.png", left=Inches(2), top=Inches(1.5),
                width=Inches(9), height=Inches(5.2))
    _add_notes(slide, "[~30s] Walk through the defense pipeline diagram — input sanitization, detection, response filtering, monitoring.")

    # --- Slide 11: Prevention Strategies ---
    print("Creating slide 11: Prevention")
    slide = prs.slides.add_slide(blank_layout)
    _set_dark_bg(slide)
    _add_heading(slide, "Prevention Strategies")
    bullet_items = []
    for s in PREVENTION_STRATEGIES[:5]:
        bullet_items.append(f"{s['strategy']} ({s.get('implementation_level', '')}): {s['effectiveness'][:100]}...")
    _add_bullets(slide, bullet_items, font_size=15)
    _add_notes(slide, "[~45s] Cover the layered defense approach. Emphasize that no single prevention strategy is complete — instruction hierarchy + input sanitization + output filtering together.")

    # --- Slide 12: Defense Architecture Figure ---
    print("Creating slide 12: Defense architecture figure")
    slide = prs.slides.add_slide(blank_layout)
    _set_dark_bg(slide)
    _add_heading(slide, "Layered Defense Architecture")
    _add_figure(slide, "defense_architecture.png", left=Inches(2), top=Inches(1.5),
                width=Inches(9), height=Inches(5.2))
    _add_notes(slide, "[~30s] Show the architecture diagram. Highlight how multiple defense layers interact to provide defense in depth.")

    # --- Slide 13: Key References & Conclusion ---
    print("Creating slide 13: References & Conclusion")
    slide = prs.slides.add_slide(blank_layout)
    _set_dark_bg(slide)
    _add_heading(slide, "Key References & Conclusion")
    # Show top 6 references
    ref_items = [ref[:120] + "..." if len(ref) > 120 else ref for ref in REFERENCES[:6]]
    _add_bullets(slide, ref_items, font_size=13, top=Inches(1.3), height=Inches(4.5))
    # Conclusion line
    tb = _add_textbox(slide, Inches(0.8), Inches(6.0), Inches(11.5), Inches(0.8))
    _set_text(tb, "Prompt injection remains an open problem — defense in depth is essential.",
              font_size=20, color=ACCENT_COLOR, bold=True)
    _add_notes(slide, "[~30s] Highlight 2-3 foundational references. Close with the key takeaway: no silver bullet, defense in depth required. Thank audience, invite questions.")

    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "presentation.pptx"
    prs.save(str(output_path))
    print(f"\nPresentation saved: {output_path}")
    print(f"Total slides: {len(prs.slides)}")
    return output_path


if __name__ == "__main__":
    generate_presentation()
