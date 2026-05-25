"""
Generates decision_memo.pdf for the Drone Light Show Depot assignment.
Uses only the standard library + reportlab (or falls back to fpdf2).
Tries reportlab first, then fpdf2, then plain HTML.
"""
import subprocess, sys

def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

# Try reportlab
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    USE = "reportlab"
except ImportError:
    try:
        install("reportlab")
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        USE = "reportlab"
    except Exception:
        USE = "html"

OUT = r"C:\Users\Slayer\Desktop\IE project 3\decision_memo.pdf"

MEMO_PARAGRAPHS = [
    ("TO",      "Festival Operations Manager, Bosphorus Drone Light Festival"),
    ("FROM",    "Analytics Team — IE 306 Assignment 3"),
    ("DATE",    "May 2026"),
    ("SUBJECT", "Recommendation: Purchase of One Additional Swap Station (Policy B)"),
]

BODY = [
    ("Executive Summary",
     "Based on a rigorous discrete-event simulation output analysis of the depot system, "
     "we recommend purchasing one additional battery-swap station (Policy B: 6 stations). "
     "The investment produces a statistically significant and practically meaningful reduction "
     "in per-drone swap-queue waiting time."),

    ("Analysis Method",
     "We modelled a closed loop of 200 drones cycling between the flight pool and the "
     "depot (swap queue → swap stations → single test rig → re-launch). "
     "The system was classified as steady-state because the fleet operates continuously "
     "with no planned stop time. "
     "A warmup period of 10,000 s (≈ 2.8 h) was deleted from each replication, "
     "determined conservatively from Welch's graphical method (~8,820 s) and MSER (~3,329 s). "
     "Steady-state confidence intervals were constructed via (a) replications-with-deletion "
     "(R = 40, SIM_DUR = 12 h each) and (b) batch means on a single 30 h long run."),

    ("Key Results",
     "Under Policy A (5 stations) the mean per-drone swap-queue wait is estimated at "
     "14.5 s (95 % CI: [13.97, 15.09] s, half-width 3.9 % of point estimate ≤ 5 % target). "
     "A Common Random Numbers (CRN) paired comparison across R = 40 replications yields:\n\n"
     "  • Point estimate of A − B difference:  10.41 s\n"
     "  • 95 % confidence interval:  [9.96, 10.85] s\n"
     "  • CRN Variance-Reduction Factor (VRF):  1.75\n\n"
     "The entire CI lies strictly above zero, confirming that Policy B reduces "
     "waiting time by roughly 10–11 s per depot visit at the 5 % significance level."),

    ("Verification",
     "Two V&V checks were passed: (1) the fleet conservation invariant "
     "FLEET_SIZE = in_air + in_depot held with zero violation throughout the simulation; "
     "(2) Little's Law on the depot subsystem produced a predicted-to-observed ratio of "
     "0.9999, confirming model integrity."),

    ("Recommendation",
     "Add one swap station (Policy B). The improvement is statistically significant, "
     "the model is verified, and the VRF of 1.75 demonstrates that the CRN comparison "
     "is reliable. The cost of one additional rack should be weighed against the continuous "
     "improvement in drone turnaround during every rehearsal block."),
]

if USE == "reportlab":
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
    )
    styles = getSampleStyleSheet()
    title_style  = ParagraphStyle("title",  parent=styles["Title"],  fontSize=14, spaceAfter=6)
    header_style = ParagraphStyle("hdr",    parent=styles["Normal"], fontSize=10, fontName="Helvetica-Bold", spaceBefore=4, spaceAfter=2)
    body_style   = ParagraphStyle("body",   parent=styles["Normal"], fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=8)
    label_style  = ParagraphStyle("label",  parent=styles["Normal"], fontSize=10, fontName="Helvetica-Bold")
    value_style  = ParagraphStyle("value",  parent=styles["Normal"], fontSize=10)

    story = []
    story.append(Paragraph("MEMORANDUM", title_style))
    story.append(HRFlowable(width="100%", thickness=1, color="black"))
    story.append(Spacer(1, 6))

    for label, value in MEMO_PARAGRAPHS:
        story.append(Paragraph(f"<b>{label}:</b>  {value}", value_style))

    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.5, color="grey"))
    story.append(Spacer(1, 8))

    for heading, text in BODY:
        story.append(Paragraph(heading, header_style))
        # replace \n\n with paragraph breaks
        for part in text.split("\n\n"):
            story.append(Paragraph(part.replace("\n", "<br/>"), body_style))

    doc.build(story)
    print(f"PDF written via reportlab: {OUT}")

else:
    # Plain HTML fallback
    html_out = OUT.replace(".pdf", ".html")
    rows = "".join(f"<tr><td><b>{l}</b></td><td>{v}</td></tr>" for l, v in MEMO_PARAGRAPHS)
    sections = "".join(
        f"<h3>{h}</h3><p>{t.replace(chr(10), '<br>')}</p>" for h, t in BODY
    )
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{font-family:Arial,sans-serif;font-size:11pt;max-width:700px;margin:40px auto;}}
table{{border-collapse:collapse;width:100%;margin-bottom:20px;}}
td{{padding:4px 8px;vertical-align:top;}}h1{{font-size:16pt;}}h3{{font-size:11pt;margin-bottom:4px;}}
</style></head><body>
<h1>MEMORANDUM</h1><hr>
<table>{rows}</table><hr>
{sections}
</body></html>"""
    with open(html_out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"PDF not available; HTML memo written: {html_out}")
    print("Open in browser and Print → Save as PDF.")
