"""
Anchor Digital — Sales Sheet PDF Generator
Outputs: anchor_digital_sales_sheet.pdf  (US Letter, single page)

Requirements:
    pip install reportlab pillow
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, HRFlowable,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus.flowables import Flowable

# ── Dimensions ────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter          # 612 × 792 pt
MARGIN_L = 0.45 * inch
MARGIN_R = 0.45 * inch
MARGIN_T = 0.40 * inch
MARGIN_B = 0.55 * inch           # room for footer
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

# ── Brand colours ─────────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#1a2b4a")
TEAL    = colors.HexColor("#1ca9c9")
WHITE   = colors.white
LIGHT   = colors.HexColor("#f0f7fa")
GREEN   = colors.HexColor("#2e7d5a")
GREEN_L = colors.HexColor("#e8f5ee")
GRAY1   = colors.HexColor("#f5f8fa")
GRAY2   = colors.HexColor("#e2eaf0")
GRAY3   = colors.HexColor("#6b7e96")
BLACK   = colors.HexColor("#1a1a1a")

# ── Styles ────────────────────────────────────────────────────────────────────
def s(name, **kw):
    base = {
        "fontName": "Helvetica", "fontSize": 8, "leading": 11,
        "textColor": BLACK, "spaceAfter": 0, "spaceBefore": 0,
    }
    base.update(kw)
    return ParagraphStyle(name, **base)

ST = {
    "co_name":   s("co_name",  fontName="Helvetica-Bold", fontSize=20, textColor=WHITE,  leading=24),
    "co_sub":    s("co_sub",   fontSize=8,  textColor=TEAL,  leading=11),
    "co_url":    s("co_url",   fontSize=8,  textColor=WHITE, alignment=TA_RIGHT, leading=11),
    "co_spec":   s("co_spec",  fontSize=8,  textColor=TEAL,  alignment=TA_RIGHT, leading=11),

    "hero_h":    s("hero_h",   fontName="Helvetica-Bold", fontSize=15, textColor=BLACK,  leading=19),
    "hero_sub":  s("hero_sub", fontSize=8,  textColor=GRAY3, leading=11),

    "stat_n":    s("stat_n",   fontName="Helvetica-Bold", fontSize=18, textColor=BLACK,  alignment=TA_CENTER, leading=22),
    "stat_l":    s("stat_l",   fontSize=7,  textColor=GRAY3, alignment=TA_CENTER, leading=9),

    "pitch_b":   s("pitch_b",  fontName="Helvetica-Bold", fontSize=9, textColor=NAVY,   leading=12),
    "pitch_s":   s("pitch_s",  fontSize=8,  textColor=TEAL, leading=11),

    "sec_h":     s("sec_h",    fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,  leading=13),
    "feat_b":    s("feat_b",   fontName="Helvetica-Bold", fontSize=8,  textColor=BLACK, leading=11),
    "feat_s":    s("feat_s",   fontSize=7,  textColor=GRAY3, leading=9),

    "card_name": s("card_name", fontName="Helvetica-Bold", fontSize=9,  textColor=BLACK,  leading=11),
    "card_pop":  s("card_pop",  fontName="Helvetica-Bold", fontSize=6.5, textColor=WHITE, alignment=TA_CENTER, leading=9),
    "card_price":s("card_price",fontName="Helvetica-Bold", fontSize=18, textColor=BLACK,  leading=22),
    "card_mo":   s("card_mo",   fontSize=7.5, textColor=GRAY3, leading=10),
    "card_feat": s("card_feat", fontSize=7.5, textColor=BLACK, leading=10),

    "guar_h":   s("guar_h",   fontName="Helvetica-Bold", fontSize=9,  textColor=GREEN,  leading=12),
    "guar_b":   s("guar_b",   fontSize=7.5, textColor=BLACK, leading=11),
    "guar_em":  s("guar_em",  fontName="Helvetica-Bold", fontSize=7.5, textColor=GREEN, leading=11),

    "tbl_hdr":  s("tbl_hdr",  fontName="Helvetica-Bold", fontSize=7.5, textColor=GRAY3,  leading=10),
    "tbl_them": s("tbl_them", fontSize=7.5, textColor=BLACK, leading=10),
    "tbl_prob": s("tbl_prob", fontSize=7.5, textColor=BLACK, leading=10),
    "tbl_anch": s("tbl_anch", fontName="Helvetica-Bold", fontSize=7.5, textColor=TEAL,  leading=10),

    "ftr_cta":  s("ftr_cta",  fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE, leading=11),
    "ftr_url":  s("ftr_url",  fontSize=8.5, textColor=TEAL, leading=11),
    "ftr_r":    s("ftr_r",    fontSize=7.5, textColor=GRAY3, alignment=TA_RIGHT, leading=10),
}


# ── Custom Flowables ───────────────────────────────────────────────────────────

class FilledRect(Flowable):
    """Solid-colour rectangle that occupies vertical space."""
    def __init__(self, w, h, fill, radius=3):
        super().__init__()
        self.w, self.h, self.fill, self.radius = w, h, fill, radius
    def wrap(self, *_):
        return self.w, self.h
    def draw(self):
        self.canv.setFillColor(self.fill)
        self.canv.roundRect(0, 0, self.w, self.h, self.radius, stroke=0, fill=1)


class HeaderBand(Flowable):
    """Navy header with company info left + right."""
    HEIGHT = 46

    def __init__(self, w):
        super().__init__()
        self.w = w

    def wrap(self, *_):
        return self.w, self.HEIGHT

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.rect(0, 0, self.w, self.HEIGHT, stroke=0, fill=1)

        # left: name
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(8, self.HEIGHT - 26, "Anchor Digital")

        # left: subtitle
        c.setFillColor(TEAL)
        c.setFont("Helvetica", 8)
        c.drawString(8, self.HEIGHT - 38, "Web Services & Innovation  |  Florida")

        # right: url + speciality
        c.setFillColor(WHITE)
        c.setFont("Helvetica", 8)
        c.drawRightString(self.w - 8, self.HEIGHT - 24, "anchordigital.com")
        c.setFillColor(TEAL)
        c.drawRightString(self.w - 8, self.HEIGHT - 36, "Specialized in Dental Practices")


class FooterBand(Flowable):
    """Dark footer bar anchored at the bottom of the frame."""
    HEIGHT = 28

    def __init__(self, w):
        super().__init__()
        self.w = w

    def wrap(self, *_):
        return self.w, self.HEIGHT

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.rect(0, 0, self.w, self.HEIGHT, stroke=0, fill=1)

        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(8, 9, "Ready to get more patients?")

        c.setFillColor(TEAL)
        c.setFont("Helvetica", 8.5)
        c.drawString(8 + c.stringWidth("Ready to get more patients?  ", "Helvetica-Bold", 8.5), 9, "anchordigital.com")

        c.setFillColor(GRAY3)
        c.setFont("Helvetica", 7.5)
        c.drawRightString(self.w - 8, 9, "Florida-based  |  Dental practice specialists  |  No contracts")


# ── Helper builders ────────────────────────────────────────────────────────────

def stat_table(cw):
    stats = [
        ("70%",   "of clicks go to\nMap Pack top 3"),
        ("69%",   "won't book below\n4 stars"),
        ("$286",  "avg cost to acquire\n1 new patient"),
        ("$2,000+","lifetime value\nper patient"),
    ]
    col = cw / 4
    data = [[
        [Paragraph(n, ST["stat_n"]), Paragraph(l, ST["stat_l"])]
        for n, l in stats
    ]]
    t = Table(data, colWidths=[col]*4, rowHeights=[36])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), GRAY1),
        ("LINEAFTER",   (0,0), (2,0),   0.5, GRAY2),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING",(0,0), (-1,-1), 4),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("BOX",         (0,0), (-1,-1), 0.5, GRAY2),
    ]))
    return t


def features_list():
    items = [
        ("Mobile-first website",          "Fast, looks great on any device"),
        ("Local SEO optimization",         '"Dentist near me" rankings'),
        ("Google Business Profile",        "Full setup + monthly management"),
        ("Online booking integration",     "Patients book 24/7 without calling"),
        ("Review generation setup",        "Systematically grow your Google stars"),
        ("Monthly performance report",     "Track every new patient inquiry"),
    ]
    rows = []
    for bold, light in items:
        rows.append(
            Paragraph(
                f'<font name="Helvetica-Bold" size="8">✓ {bold}</font>'
                f'<br/><font color="#6b7e96" size="7">{light}</font>',
                s("feat_item", leading=13, spaceAfter=3)
            )
        )
    return rows


def pricing_table(cw):
    """Three pricing cards side-by-side — never stacked."""

    def card_cell(name, price, mo, features, highlight=False):
        bg = NAVY if highlight else WHITE
        fg = WHITE if highlight else BLACK
        mo_col = TEAL if highlight else GRAY3

        paras = []
        if highlight:
            paras.append(Paragraph("MOST POPULAR", ST["card_pop"]))
            paras.append(Spacer(1, 3))
        paras.append(Paragraph(f'<font color="{"#ffffff" if highlight else "#1a1a1a"}">{name}</font>', ST["card_name"]))
        paras.append(Paragraph(
            f'<font name="Helvetica-Bold" size="18" color="{"#ffffff" if highlight else "#1a1a1a"}">{price}</font>',
            s("cp2", leading=22)
        ))
        paras.append(Paragraph(
            f'<font color="{"#1ca9c9" if highlight else "#6b7e96"}" size="7.5">+ {mo}</font>',
            s("cm2", leading=10)
        ))
        paras.append(Spacer(1, 6))
        for f in features:
            paras.append(Paragraph(
                f'<font color="{"#ffffff" if highlight else "#1a1a1a"}" size="7.5">✓ {f}</font>',
                s(f"cf_{f[:4]}", leading=11)
            ))
        return paras

    starter = card_cell(
        "Starter", "$800", "$150/mo",
        ["5-page website", "Basic SEO", "GBP setup", "Booking"]
    )
    growth = card_cell(
        "Growth", "$1,500", "$299/mo",
        ["8-page design", "Full local SEO", "GBP management",
         "Review setup", "Monthly report"],
        highlight=True
    )
    dominate = card_cell(
        "Dominate", "$3,000", "$499/mo",
        ["Everything in Growth", "Custom copy", "Google Ads",
         "Blog (2/mo)", "Competitor analysis"]
    )

    col = cw / 3
    t = Table([[starter, growth, dominate]],
              colWidths=[col, col, col],
              rowHeights=None)

    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (0,0), WHITE),
        ("BACKGROUND",   (1,0), (1,0), NAVY),
        ("BACKGROUND",   (2,0), (2,0), WHITE),
        ("BOX",          (0,0), (0,0), 1, GRAY2),
        ("BOX",          (1,0), (1,0), 1.5, TEAL),
        ("BOX",          (2,0), (2,0), 1, GRAY2),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 10),
    ]))
    return t


def competitor_table(cw):
    COL_W = [cw * 0.22, cw * 0.42, cw * 0.36]

    hdr = [
        Paragraph("Them",           ST["tbl_hdr"]),
        Paragraph("The problem",    ST["tbl_hdr"]),
        Paragraph("Anchor Digital", s("tbl_hdr_a", fontName="Helvetica-Bold",
                                      fontSize=7.5, textColor=TEAL, leading=10)),
    ]
    rows_data = [
        (
            "Generic web agencies",
            "$3K–$8K, no dental knowledge, ghost you after launch",
            "✓ Dental-specialized from day one",
        ),
        (
            "Weave / Podium",
            "$500–$1K/mo, locked contracts, tools you never fully use",
            "✓ Month-to-month, no contracts",
        ),
        (
            "DIY (Wix/Squarespace)",
            "Ranks poorly, zero local SEO, still needs maintenance",
            "✓ Professional build in 2 weeks",
        ),
    ]

    data = [hdr]
    for them, prob, anchor in rows_data:
        data.append([
            Paragraph(them,   ST["tbl_them"]),
            Paragraph(prob,   ST["tbl_prob"]),
            Paragraph(anchor, ST["tbl_anch"]),
        ])

    t = Table(data, colWidths=COL_W, repeatRows=1)
    t.setStyle(TableStyle([
        # header row
        ("BACKGROUND",   (0,0), (-1,0), GRAY1),
        ("BOTTOMPADDING",(0,0), (-1,0), 5),
        ("TOPPADDING",   (0,0), (-1,0), 5),
        ("LINEBELOW",    (0,0), (-1,0), 1, GRAY2),
        # data rows — alternating light bg
        ("BACKGROUND",   (0,1), (-1,1), WHITE),
        ("BACKGROUND",   (0,2), (-1,2), GRAY1),
        ("BACKGROUND",   (0,3), (-1,3), WHITE),
        # padding for all cells
        ("LEFTPADDING",  (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING",   (0,1), (-1,-1), 7),
        ("BOTTOMPADDING",(0,1), (-1,-1), 7),
        # borders
        ("BOX",          (0,0), (-1,-1), 0.5, GRAY2),
        ("LINEBELOW",    (0,1), (-1,-2), 0.5, GRAY2),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ]))
    return t


def guarantee_table(cw):
    body = (
        "If your new website + GBP doesn't bring at least 3 new patient inquiries within "
        "60 days of going live, we keep working for free until it does — or refund your "
        "build fee. No questions asked."
    )
    em = "One new patient = $2,000+ lifetime value. Your investment pays for itself with patient #1."
    cell = [
        Paragraph('The "New Patient or Free" Guarantee', ST["guar_h"]),
        Spacer(1, 4),
        Paragraph(body, ST["guar_b"]),
        Spacer(1, 4),
        Paragraph(f"<b>{em}</b>", ST["guar_em"]),
    ]
    t = Table([[cell]], colWidths=[cw])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), GREEN_L),
        ("BOX",           (0,0), (-1,-1), 1, GREEN),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    return t


# ── Page-level drawing (footer + header decorations) ──────────────────────────

def draw_page(canvas, doc):
    canvas.saveState()
    # Footer bar
    footer_h = 28
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, footer_h, stroke=0, fill=1)

    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 8.5)
    canvas.drawString(MARGIN_L, 9, "Ready to get more patients?")

    canvas.setFillColor(TEAL)
    canvas.setFont("Helvetica", 8.5)
    offset = canvas.stringWidth("Ready to get more patients?  ", "Helvetica-Bold", 8.5)
    canvas.drawString(MARGIN_L + offset, 9, "anchordigital.com")

    canvas.setFillColor(GRAY3)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(PAGE_W - MARGIN_R, 9,
                           "Florida-based  |  Dental practice specialists  |  No contracts")

    canvas.restoreState()


# ── Build document ────────────────────────────────────────────────────────────

def build():
    OUTPUT = "anchor_digital_sales_sheet.pdf"

    doc = BaseDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
    )

    frame = Frame(
        MARGIN_L, MARGIN_B,
        CONTENT_W, PAGE_H - MARGIN_T - MARGIN_B,
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
        id="main",
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=draw_page)])

    story = []
    SP = lambda n: Spacer(1, n)   # shorthand

    # ── Header band ───────────────────────────────────────────────────────────
    story.append(HeaderBand(CONTENT_W))
    story.append(SP(10))

    # ── Hero ──────────────────────────────────────────────────────────────────
    story.append(Paragraph(
        "Your next patient is Googling a dentist right now.",
        ST["hero_h"]
    ))
    story.append(SP(3))
    story.append(Paragraph(
        "If your practice isn't showing up, they're booking with your competitor.",
        ST["hero_sub"]
    ))
    story.append(SP(8))

    # ── Stats row ─────────────────────────────────────────────────────────────
    story.append(stat_table(CONTENT_W))
    story.append(SP(8))

    # ── Pitch block ───────────────────────────────────────────────────────────
    pitch_cell = [
        Paragraph(
            "We build dental practices a website that ranks on Google, converts visitors "
            "into booked appointments, and pays for itself with a single new patient.",
            ST["pitch_b"]
        ),
        Spacer(1, 4),
        Paragraph(
            "Not a pretty brochure — a patient acquisition system: local SEO, GBP, "
            "mobile-first design, and online booking.",
            ST["pitch_s"]
        ),
    ]
    pitch_t = Table([[pitch_cell]], colWidths=[CONTENT_W])
    pitch_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LIGHT),
        ("BOX",           (0,0), (-1,-1), 1, TEAL),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(pitch_t)
    story.append(SP(10))

    # ── Two-column: What you get | Pricing ────────────────────────────────────
    LEFT_W  = CONTENT_W * 0.32
    RIGHT_W = CONTENT_W * 0.68 - 6   # small gutter

    # Features list (left column)
    feat_items = features_list()
    feat_col = [Paragraph("What you get", ST["sec_h"])]
    feat_col += [HRFlowable(width=LEFT_W, thickness=2, color=TEAL, spaceAfter=5)]
    feat_col += feat_items

    # Pricing cards (right column) — three cards always side-by-side
    price_col = [
        Paragraph("Pricing", ST["sec_h"]),
        HRFlowable(width=RIGHT_W, thickness=2, color=TEAL, spaceAfter=6),
        pricing_table(RIGHT_W),
    ]

    two_col = Table(
        [[feat_col, price_col]],
        colWidths=[LEFT_W, RIGHT_W],
        hAlign="LEFT",
    )
    two_col.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (0,0),   6),   # gutter between columns
    ]))
    story.append(two_col)
    story.append(SP(10))

    # ── Guarantee ─────────────────────────────────────────────────────────────
    story.append(guarantee_table(CONTENT_W))
    story.append(SP(10))

    # ── Competitor table ──────────────────────────────────────────────────────
    story.append(Paragraph("Why Anchor Digital vs. the alternatives", ST["sec_h"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=2, color=TEAL, spaceAfter=6))
    story.append(competitor_table(CONTENT_W))

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story)
    print(f"✓  Generated {OUTPUT}")


if __name__ == "__main__":
    build()
