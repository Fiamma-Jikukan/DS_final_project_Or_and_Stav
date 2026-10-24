"""Build the first-draft presentation deck for the DS final project."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

HERE = Path(__file__).resolve().parent
PROJECT = Path(r"C:\Users\User\PycharmProjects\DS_final_project_Or_and_Stav")
OUT_DIR = PROJECT / "presentation"
FIG_DIR = OUT_DIR / "figures"
OUT = OUT_DIR / "Presentation_Or_and_Stav.pptx"

# ---------------------------------------------------------------- palette
INK = RGBColor(0x33, 0x30, 0x2E)        # warm charcoal, body text
DARK = RGBColor(0x2E, 0x3A, 0x3F)       # dark slide background
PAPER = RGBColor(0xFF, 0xFF, 0xFF)
SAND = RGBColor(0xEF, 0xE9, 0xE1)       # card tint on light slides
CLAY = RGBColor(0xB8, 0x50, 0x42)       # terracotta, accent / under-performing
SAGE = RGBColor(0xA7, 0xBE, 0xAE)       # sage, over-performing
SLATE = RGBColor(0x50, 0x80, 0x8E)      # neutral accent
DEEPCLAY = RGBColor(0x7A, 0x4A, 0x3F)
MUTED = RGBColor(0x8A, 0x7F, 0x76)      # captions on light
MUTED_D = RGBColor(0xC9, 0xBF, 0xB2)    # captions on dark
RULE = RGBColor(0xD9, 0xD2, 0xC7)

HEAD = "Cambria"
BODY = "Calibri"

# ---------------------------------------------------------------- geometry
W, H = 13.333, 7.5
L = 0.62                     # left margin
CW = 12.09                   # content width
COL = 5.88                   # two-column width
COL2_X = 6.83
TITLE_Y = 0.36
FOOTER_Y = 6.98

FOOTER = "Beyond the Cluster  ·  Tchizik & Cohen"


def new_deck():
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    return prs


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def fill_bg(slide, color):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Emu(0), Emu(0), Inches(W), Inches(H)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def box(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    return tf


def write(tf, blocks, first=False):
    """blocks: list of dicts {text, size, bold, color, font, space_after, align, space_before}"""
    for i, b in enumerate(blocks):
        p = tf.paragraphs[0] if (i == 0) else tf.add_paragraph()
        p.alignment = b.get("align", PP_ALIGN.LEFT)
        if b.get("space_after"):
            p.space_after = Pt(b["space_after"])
        if b.get("space_before"):
            p.space_before = Pt(b["space_before"])
        if b.get("line"):
            p.line_spacing = b["line"]
        for run_spec in b["runs"] if "runs" in b else [b]:
            r = p.add_run()
            r.text = run_spec["text"]
            f = r.font
            f.name = run_spec.get("font", b.get("font", BODY))
            f.size = Pt(run_spec.get("size", b.get("size", 14)))
            f.bold = run_spec.get("bold", b.get("bold", False))
            f.italic = run_spec.get("italic", b.get("italic", False))
            f.color.rgb = run_spec.get("color", b.get("color", INK))


def text(slide, x, y, w, h, blocks):
    tf = box(slide, x, y, w, h)
    write(tf, blocks)
    return tf


def card(slide, x, y, w, h, fill=SAND, radius=0.05):
    sh = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)
    )
    sh.adjustments[0] = radius
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.shadow.inherit = False
    sh.text_frame.text = ""
    return sh


def circle(slide, x, y, d, label, fill=CLAY, color=PAPER, size=15):
    sh = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d)
    )
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.shadow.inherit = False
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.name = HEAD
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.color.rgb = color
    return sh


def slide_title(slide, s, dark=False):
    text(
        slide, L, TITLE_Y, CW, 0.62,
        [{"text": s, "font": HEAD, "size": 32, "bold": True,
          "color": PAPER if dark else INK}],
    )


def footer(slide, number, dark=False):
    c = MUTED_D if dark else MUTED
    text(slide, L, FOOTER_Y, 8.0, 0.3,
         [{"text": FOOTER, "size": 9.5, "color": c}])
    tf = box(slide, W - L - 1.2, FOOTER_Y, 1.2, 0.3)
    write(tf, [{"text": str(number), "size": 9.5, "color": c,
                "align": PP_ALIGN.RIGHT}])


def picture(slide, name, x, y, w):
    path = FIG_DIR / name
    from PIL import Image
    with Image.open(path) as im:
        iw, ih = im.size
    h = w * ih / iw
    slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    return h


def caption(slide, x, y, w, label, rest):
    text(slide, x, y, w, 0.3,
         [{"runs": [{"text": label, "bold": True}, {"text": rest}],
           "size": 10.5, "color": MUTED}])


def stat(slide, x, y, w, number, label, color=CLAY, num_size=34):
    nh = num_size * 1.2 / 72 + 0.02
    text(slide, x, y, w, nh,
         [{"text": number, "font": HEAD, "size": num_size, "bold": True,
           "color": color}])
    text(slide, x, y + nh, w, 0.75,
         [{"text": label, "size": 11, "color": MUTED, "line": 1.05}])


def bullets(slide, x, y, w, h, items, size=14, color=INK, gap=6, hang=0.26):
    blocks = []
    for it in items:
        blocks.append({
            "runs": [{"text": "\u2022   ", "color": CLAY, "bold": True},
                     {"text": it}],
            "size": size, "color": color, "space_after": gap, "line": 1.02,
        })
    tf = text(slide, x, y, w, h, blocks)
    for p in tf.paragraphs:          # hanging indent: wrapped lines clear the bullet
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(Inches(hang)))
        pPr.set("indent", str(-Inches(hang)))
    return tf


def grid_table(slide, x, y, colw, rows, header_fill, header_color,
               row_h=0.235, size=11, header_size=11):
    nrows, ncols = len(rows), len(colw)
    shape = slide.shapes.add_table(
        nrows, ncols, Inches(x), Inches(y),
        Inches(sum(colw)), Inches(row_h * nrows)
    )
    tbl = shape.table
    tbl.first_row = True
    tbl.horz_banding = False
    for j, cwid in enumerate(colw):
        tbl.columns[j].width = Inches(cwid)
    for i, row in enumerate(rows):
        tbl.rows[i].height = Inches(row_h)
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Emu(0)
            cell.margin_bottom = Emu(0)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = header_fill if i == 0 else PAPER
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.RIGHT
            r = p.add_run()
            r.text = str(val)
            r.font.name = BODY
            r.font.size = Pt(header_size if i == 0 else size)
            r.font.bold = i == 0
            r.font.color.rgb = header_color if i == 0 else INK
    return shape


# ================================================================ slides
def s01_title(prs):
    s = blank(prs)
    fill_bg(s, DARK)
    text(s, 0.9, 1.75, 11.5, 1.0,
         [{"text": "Beyond the Cluster", "font": HEAD, "size": 50,
           "bold": True, "color": PAPER}])
    text(s, 0.9, 2.85, 10.9, 1.25,
         [{"text": "Which Israeli local authorities out- and under-perform "
                   "their socio-economic standing in national achievement tests?",
           "size": 19, "color": MUTED_D, "line": 1.12}])

    # the deck's motif: the official 1 to 10 socio-economic cluster strip
    for i in range(10):
        sq = s.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.9 + i * 0.52), Inches(4.42),
            Inches(0.42), Inches(0.34),
        )
        sq.fill.solid()
        sq.fill.fore_color.rgb = SAGE
        sq.fill.fore_color.brightness = 0.75 - 0.11 * i
        sq.line.fill.background()
        sq.shadow.inherit = False
    text(s, 0.9, 4.86, 6.0, 0.3,
         [{"text": "official socio-economic cluster, 1 to 10",
           "size": 10.5, "color": MUTED_D}])

    text(s, 0.9, 5.62, 10.9, 0.4,
         [{"text": "Stav Tchizik (316062835)   ·   Or Cohen (206631509)",
           "size": 15, "color": PAPER}])
    text(s, 0.9, 6.02, 10.9, 0.75,
         [{"text": "Introduction to Data Science, Final Project", "size": 13,
           "color": MUTED_D, "space_after": 4},
          {"text": "Ministry of Education Meitzav scores, 2016 to 2018   ×   "
                   "CBS Socio-Economic Index of Local Authorities, 2017 edition",
           "size": 12, "color": MUTED_D}])
    return s


def s02_motivation(prs):
    s = blank(prs)
    slide_title(s, "Why ask this at the authority level")
    rows = [
        ("1", "Money and staff move by authority",
         "Education budgets, staffing and intervention programmes in Israel are "
         "allocated to local authorities, so the authority is the unit a decision "
         "actually attaches to."),
        ("2", "The gradient is already known",
         "RAMA publishes a Meitzav report for every authority that already compares "
         "it against socio-economically similar authorities. Reproducing that "
         "gradient would add nothing."),
        ("3", "The open question is who departs from it",
         "Which authorities score above or below what their circumstances predict, "
         "how reliably, and what sets them apart."),
    ]
    y = 1.35
    for num, head, bodytext in rows:
        circle(s, L, y + 0.02, 0.42, num)
        text(s, L + 0.62, y, 7.0, 0.32,
             [{"text": head, "size": 16, "bold": True, "color": DEEPCLAY}])
        text(s, L + 0.62, y + 0.36, 7.0, 1.0,
             [{"text": bodytext, "size": 14, "line": 1.03}])
        y += 1.55

    card(s, L, 6.0, 7.62, 0.8)
    text(s, L + 0.3, 6.18, 7.02, 0.5,
         [{"runs": [{"text": "What this project adds: ", "bold": True,
                     "color": DEEPCLAY},
                    {"text": "a ranking of the departures from that gradient "
                             "across all authorities, and a test of what "
                             "distinguishes them.", "color": INK}],
           "size": 13.5, "line": 1.03}])

    card(s, 8.55, 1.35, 4.16, 2.1)
    text(s, 8.85, 1.56, 3.56, 0.32,
         [{"text": "Who the answer is for", "size": 16, "bold": True,
           "color": DEEPCLAY}])
    bullets(s, 8.85, 1.95, 3.56, 1.4,
            ["the Ministry of Education and RAMA",
             "heads of local authorities",
             "anyone setting policy on educational gaps"], size=13.5, gap=5)

    stat(s, 8.85, 3.75, 3.9, "243",
         "local authorities in the merged table, from 1,749 authority by year by "
         "grade by subject rows")
    stat(s, 8.85, 5.25, 3.9, "2 sources",
         "Ministry of Education test scores and the CBS socio-economic index, "
         "joined on a key we had to build", color=SLATE, num_size=28)
    footer(s, 2)
    return s


def s03_question(prs):
    s = blank(prs)
    slide_title(s, "The question")
    card(s, L, 1.3, CW, 1.75, fill=SAND)
    text(s, L + 0.35, 1.52, CW - 0.7, 1.35,
         [{"text": "Which local authorities in Israel score higher or lower on "
                   "national tests than their socio-economic level would predict, "
                   "and what sets those authorities apart?",
           "font": HEAD, "size": 23, "bold": True, "color": DEEPCLAY,
           "line": 1.12}])

    subs = [
        (L, "Supporting question",
         "How closely does the socio-economic index track test scores in the "
         "first place?",
         "That relationship is the baseline the deviations are measured against, "
         "so it has to be fitted well before any authority can be called an "
         "over- or under-performer."),
        (COL2_X, "Supporting question",
         "Does grouping authorities by their achievement profiles reproduce the "
         "official CBS clusters?",
         "If the two systems were interchangeable, the official 1 to 10 clusters "
         "would already tell us everything the test results do."),
    ]
    for x, tag, q, why in subs:
        card(s, x, 3.2, COL, 2.45)
        text(s, x + 0.3, 3.42, COL - 0.6, 0.28,
             [{"text": tag.upper(), "size": 10.5, "bold": True, "color": CLAY}])
        text(s, x + 0.3, 3.75, COL - 0.6, 0.85,
             [{"text": q, "size": 16, "bold": True, "color": INK, "line": 1.05}])
        text(s, x + 0.3, 4.65, COL - 0.6, 0.85,
             [{"text": why, "size": 13.5, "color": MUTED, "line": 1.05}])

    text(s, L, 5.95, CW, 0.6,
         [{"runs": [{"text": "Stated as association throughout. ", "bold": True,
                     "color": CLAY},
                    {"text": "The data are observational and cross-sectional, so "
                             "nothing in this design can support a claim that "
                             "socio-economic standing produces a score.",
                     "color": INK}],
           "size": 14}])
    footer(s, 3)
    return s


def s04_data(prs):
    s = blank(prs)
    slide_title(s, "Two official sources, and the work to join them")
    sources = [
        (L, "Ministry of Education: Meitzav",
         "National assessment in grades 5 and 8, in Arabic or Hebrew as a first "
         "language, English, Mathematics and Science. One row per authority, year, "
         "sector, grade and subject: 3,067 rows, 251 authorities, 2015 to 2019."),
        (COL2_X, "CBS: Socio-Economic Index, 2017",
         "All 255 local authorities ranked by factor analysis of 14 variables "
         "covering demography, schooling, employment and standard of living, "
         "published as a continuous value and as ten clusters."),
    ]
    for x, head, bodytext in sources:
        card(s, x, 1.22, COL, 1.5)
        text(s, x + 0.3, 1.4, COL - 0.6, 0.3,
             [{"text": head, "size": 15, "bold": True, "color": DEEPCLAY}])
        text(s, x + 0.3, 1.74, COL - 0.6, 0.9,
             [{"text": bodytext, "size": 12.5, "line": 1.03}])

    text(s, L, 2.92, CW, 0.3,
         [{"text": "Three things the raw files forced on us", "size": 16,
           "bold": True, "color": CLAY}])
    probs = [
        ("Two code systems",
         "The files number authorities differently. For cities and local councils "
         "the education code is the CBS code with one extra digit, so rashut // 10 "
         "recovers it; a regional council's code is its council number × 100,000; "
         "four merged cities were mapped by hand. All 250 matched, verified by name."),
        ("The same pupils twice",
         "norm_id is the sector, and value 1 is the two sectors combined, which "
         "exists only for the 19 mixed authorities. Haifa grade 5 English in 2016: "
         "859 = 768 + 91. We keep the combined row where it exists and the single "
         "sector row everywhere else."),
        ("Years that miss the index",
         "The index edition is 2017, so we keep 2016 to 2018 and drop 2015 and 2019 "
         "rather than compare scores to an index measured years off. Scores still "
         "drift a median of 13.5 points across the three years, so year stays in "
         "the models as a variable."),
    ]
    y = 3.26
    for i, (head, bodytext) in enumerate(probs, start=1):
        card(s, L, y, CW, 0.98)
        circle(s, L + 0.26, y + 0.2, 0.34, str(i), size=12)
        text(s, L + 0.72, y + 0.24, 2.3, 0.5,
             [{"text": head, "size": 14, "bold": True, "color": SLATE,
               "line": 1.03}])
        text(s, L + 3.2, y + 0.16, CW - 3.5, 0.72,
             [{"text": bodytext, "size": 13, "line": 1.03}])
        y += 1.06

    text(s, L, 6.52, CW, 0.3,
         [{"runs": [{"text": "3,067 rows to 1,749   ·   251 authorities to 243   ·   ",
                     "bold": True},
                    {"text": "44 rows have no score, almost all of them groups of "
                             "under 30 pupils the Ministry suppresses as too small to publish",
                     "color": MUTED}],
           "size": 12.5}])
    footer(s, 4)
    return s


def s05_methods(prs):
    s = blank(prs)
    slide_title(s, "How the analysis is built")
    steps = [
        ("Split by authority",
         "every row of an authority goes to one set, stratified by cluster"),
        ("Baselines",
         "the overall mean, and the mean of that subject and grade"),
        ("Two model tracks",
         "linear and forest; logistic and forest on a High / Low label"),
        ("Out-of-fold gaps",
         "every authority predicted by a model that never saw it"),
        ("Clustering",
         "K-Means on grade 8 scores, and on the gaps"),
    ]
    bw, gap = 2.25, 0.21
    x = L
    for i, (head, sub) in enumerate(steps):
        card(s, x, 1.3, bw, 1.55)
        text(s, x + 0.18, 1.45, bw - 0.36, 0.7,
             [{"text": head, "size": 13.5, "bold": True, "color": DEEPCLAY,
               "line": 1.02}])
        text(s, x + 0.18, 2.14, bw - 0.36, 0.65,
             [{"text": sub, "size": 10.5, "color": MUTED, "line": 1.02}])
        if i < len(steps) - 1:
            arrow = s.shapes.add_shape(
                MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(x + bw + 0.045),
                Inches(1.97), Inches(0.12), Inches(0.2))
            arrow.rotation = 90
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = CLAY
            arrow.line.fill.background()
            arrow.shadow.inherit = False
        x += bw + gap

    card(s, L, 3.1, 7.3, 2.1)
    text(s, L + 0.3, 3.3, 6.7, 0.3,
         [{"text": "Why split by authority, and what it cost",
           "size": 16, "bold": True, "color": DEEPCLAY}])
    text(s, L + 0.3, 3.65, 6.7, 1.4,
         [{"text": "1,749 rows come from only 243 authorities, so the rows are not "
                   "independent. In a plain split by row, 236 of the 243 "
                   "authorities land in more than one set, and predicting each test "
                   "row from nothing but its own authority's training average "
                   "already reaches R² = 0.30. Splitting by authority removes that "
                   "shortcut, and GroupKFold keeps it out of the tuning folds too.",
           "size": 13.5, "line": 1.04}])

    card(s, 8.15, 3.1, 4.56, 2.1)
    text(s, 8.45, 3.3, 3.96, 0.3,
         [{"text": "Set-up at a glance", "size": 16, "bold": True,
           "color": DEEPCLAY}])
    bullets(s, 8.45, 3.68, 3.96, 1.45,
            ["20 features: 16 about the authority, 4 about the test",
             "50 / 20 / 30 by authority, stratified by cluster",
             "GroupKFold(5) tuning, median imputation in the pipeline",
             "pandas, numpy, matplotlib, scikit-learn, seed 42"],
            size=12, gap=3)

    stat(s, L, 5.4, 3.3, "R² = 0.30",
         "what memorising an authority's average buys in a row split, with no "
         "socio-economic variable at all", num_size=28)
    stat(s, 4.3, 5.4, 3.3, "0 of 74",
         "test authorities the model had already seen, under the split we use",
         color=SLATE, num_size=28)
    stat(s, 8.15, 5.4, 4.5, "R² = 0.530",
         "the chosen forest on the held-out authorities, against 0.281 for the "
         "subject and grade baseline", color=SLATE, num_size=28)
    footer(s, 5)
    return s


def s06_result1(prs):
    s = blank(prs)
    slide_title(s, "Deviation does not follow socio-economic standing")
    h = picture(s, "deck_fig08.png", L, 1.3, 7.3)
    caption(s, L, 1.3 + h + 0.08, 7.3, "Fig 8. ",
            "Mean standardized gap against the socio-economic index, "
            "one point per authority, the extremes labelled.")
    text(s, L, 6.05, 7.3, 0.7,
         [{"text": "An authority's cluster tells you nothing about whether it "
                   "beats or misses its own prediction.",
           "font": HEAD, "size": 16, "bold": True, "color": CLAY, "line": 1.05}])

    stat(s, 8.15, 1.35, 4.56, "r = 0.011",
         "between an authority's mean gap and its socio-economic index, across all "
         "238 eligible authorities. The cloud is flat.")
    stat(s, 8.15, 2.65, 4.56, "65 of 238",
         "authorities where every single row falls on the same side of its "
         "prediction: 33 above, 32 below", color=SLATE)
    stat(s, 8.15, 3.95, 4.56, "20",
         "of those 65 survive all seven rebuilds of the analysis, and no authority "
         "ever changed direction", color=DEEPCLAY)

    card(s, 8.15, 5.25, 4.56, 1.45)
    text(s, 8.4, 5.42, 4.06, 1.1,
         [{"text": "The gaps are out-of-fold, with GroupKFold on the authority, "
                   "and standardized within subject and grade. A gap of 1.0 means "
                   "one standard deviation better than predicted for that test, "
                   "which is about 26 score points.",
           "size": 11.5, "color": INK, "line": 1.04}])
    footer(s, 6)
    return s


def s07_clusters(prs):
    s = blank(prs)
    slide_title(s, "The official clusters are not interchangeable")
    h = picture(s, "deck_fig10.png", L, 1.28, 5.5)
    caption(s, L, 1.28 + h + 0.08, 5.5, "Fig 10. ",
            "Our achievement groups (k = 10) against the official CBS clusters, "
            "223 authorities.")

    stat(s, 6.5, 1.32, 6.21, "1.54 clusters",
         "the average distance between an authority's official cluster and the "
         "group its grade 8 results put it in, against 2.70 if the two were "
         "unrelated", num_size=30)
    stat(s, 6.5, 2.72, 6.21, "55 of 223",
         "land on the same number, and 43 sit three or more clusters away. The "
         "two systems agree on direction and disagree on the details",
         color=SLATE, num_size=30)

    card(s, 6.5, 4.12, 6.21, 1.55)
    text(s, 6.8, 4.32, 5.61, 1.2,
         [{"text": "The same test on the gaps", "size": 14, "bold": True,
           "color": DEEPCLAY, "space_after": 4},
          {"text": "Clustering the gaps instead of the scores gives a distance of "
                   "2.59 against 2.78 if unrelated, which is as close to no "
                   "relationship as this measure gets. That is the check working: "
                   "the gaps were built to be independent of socio-economic "
                   "standing.",
           "size": 12, "line": 1.04}])

    text(s, 6.5, 5.9, 6.21, 0.8,
         [{"text": "Six of the eight authorities furthest below their official "
                   "cluster are regional councils, which average several separate "
                   "communities into one number.",
           "size": 13, "color": INK, "line": 1.04}])
    footer(s, 7)
    return s


def s08_subjects(prs):
    s = blank(prs)
    slide_title(s, "Deviation is not the same in every subject")
    h = picture(s, "deck_fig11.png", L, 1.42, 7.6)
    caption(s, L, 1.42 + h + 0.08, 7.6, "Fig 11. ",
            "Mean gap per achievement group across the three grade 8 subjects "
            "taught in both sectors, k = 10.")
    text(s, L, 5.9, 7.6, 0.7,
         [{"text": "Over-performing is not one thing.",
           "font": HEAD, "size": 16, "bold": True, "color": CLAY, "line": 1.05}])

    stat(s, 8.72, 1.42, 3.99, "15",
         "authorities in group 4: above prediction in English and below it in "
         "Mathematics and Science, a spread of 1.59 SD. Group 5 is its mirror "
         "image")
    stat(s, 8.72, 3.0, 3.99, "6 of 10",
         "groups are tilted rather than flat. At k = 2 both groups are flat, so "
         "at that resolution the clustering adds nothing", color=SLATE)

    card(s, 8.72, 4.6, 3.99, 1.75)
    text(s, 9.0, 4.8, 3.43, 1.4,
         [{"text": "A single gap per authority could never have shown this. For a "
                   "policy reader it matters: an authority strong in English and "
                   "weak in Mathematics needs something different from one that is "
                   "uniformly behind.",
           "size": 12, "color": INK, "line": 1.04}])
    footer(s, 8)
    return s


def s09_twenty(prs):
    s = blank(prs)
    slide_title(s, "The twenty authorities that survive everything")
    over = [
        ("Kafar Yasif", 4, "+2.12"), ("Har Hevron", 5, "+1.43"),
        ("Giv'at Shemu'el", 8, "+1.40"), ("Har Adar", 9, "+1.27"),
        ("Yirka", 3, "+1.25"), ("Kisra-Sumei", 3, "+1.00"),
        ("Arrabe", 3, "+0.99"), ("Bet Dagan", 7, "+0.96"),
        ("Yoqne'am Illit", 7, "+0.91"), ("Tel Mond", 9, "+0.87"),
        ("Efrat", 7, "+0.79"), ("Binyamina-Giv'at Ada", 9, "+0.68"),
        ("Qiryat Yam", 5, "+0.55"),
    ]
    under = [
        ("Laqye", 1, "-2.08"), ("Jisr az-Zarqa", 2, "-1.88"),
        ("Basmat Tab'un", 3, "-1.83"), ("Hagalil Haelyon", 7, "-1.69"),
        ("Lehavim", 10, "-0.69"), ("Emeq Hama'ayanot", 6, "-0.65"),
        ("Be'er Sheva", 5, "-0.56"),
    ]
    head = ["Authority", "Cluster", "Mean gap"]
    colw = [3.18, 1.0, 1.7]

    text(s, L, 1.25, COL, 0.32,
         [{"text": "Over-performing: 13", "size": 16, "bold": True,
           "color": DEEPCLAY}])
    grid_table(s, L, 1.68, colw,
               [head] + [[n, c, g] for n, c, g in over], SAGE, INK)

    text(s, COL2_X, 1.25, COL, 0.32,
         [{"text": "Under-performing: 7", "size": 16, "bold": True,
           "color": DEEPCLAY}])
    grid_table(s, COL2_X, 1.68, colw,
               [head] + [[n, c, g] for n, c, g in under], CLAY, PAPER)

    card(s, COL2_X, 3.95, COL, 1.55)
    text(s, COL2_X + 0.3, 4.14, COL - 0.6, 1.2,
         [{"text": "Why twenty and not sixty-five", "size": 14, "bold": True,
           "color": DEEPCLAY, "space_after": 4},
          {"text": "Requiring every row of an authority to agree is an "
                   "all-or-nothing test. Dropping the two smallest rows in the "
                   "whole table moves eight of the 65 on or off the list, so its "
                   "membership is a snapshot. These 20 are flagged under all seven "
                   "rebuilds, so they are the list we would stand behind.",
           "size": 12, "line": 1.04}])

    text(s, L, 5.6, CW, 0.85,
         [{"runs": [{"text": "Both lists mix sectors, clusters from 1 to 10 and all "
                             "three authority types. ", "bold": True},
                    {"text": "Nothing we measured separates them: that is the "
                             "finding, and the limit of it.", "color": INK}],
           "size": 15, "space_after": 5},
          {"text": "Mean gap is in standard deviations of that subject and grade, "
                   "averaged over the authority's rows. Positive is above "
                   "prediction. Full ranking of all 243 in data/authority_gaps.xlsx.",
           "size": 11, "color": MUTED}])
    footer(s, 9)
    return s


def s10_conclusions(prs):
    s = blank(prs)
    fill_bg(s, DARK)
    slide_title(s, "What we can say", dark=True)
    items = [
        ("About half of an authority's score is predictable",
         "The random forest reaches R² = 0.530 on authorities it has never seen, "
         "against 0.281 for a baseline that knows only the subject and the grade. "
         "The documented gradient is there, strongest in English grade 8 "
         "(r = 0.75) and weakest in Arabic grade 5 (r = 0.10)."),
        ("Which test it is outweighs everything we know about the authority",
         "Shuffling the four test-identity variables costs 0.609 of R²; shuffling "
         "all sixteen socio-economic variables costs 0.374. So the answer to the "
         "proposal's question is no, though socio-economic standing is still the "
         "second of two large blocks."),
        ("Twenty authorities deviate robustly, and none ever flips",
         "Sixty-five of 238 deviate consistently under the pre-specified analysis, "
         "33 above and 32 below. Twenty survive all seven rebuilds, and across "
         "every variation no authority ever changed direction. That is the "
         "strongest claim this project can make."),
        ("Nothing we measured explains why",
         "Across 22 variables, the 16 the model used and 6 it never saw, the "
         "strongest relationship with an authority's gap is r = 0.162. Whatever "
         "drives the gaps is plausibly school-level and organisational, and it is "
         "in neither dataset."),
    ]
    y = 1.4
    for i, (head, bodytext) in enumerate(items, start=1):
        circle(s, L, y + 0.02, 0.42, str(i), fill=SAGE, color=DARK)
        text(s, L + 0.62, y, 11.4, 0.32,
             [{"text": head, "size": 16, "bold": True, "color": PAPER}])
        text(s, L + 0.62, y + 0.36, 11.4, 0.85,
             [{"text": bodytext, "size": 13.5, "color": MUTED_D, "line": 1.03}])
        y += 1.3
    footer(s, 10, dark=True)
    return s


def s11_limits(prs):
    s = blank(prs)
    slide_title(s, "What this cannot say")
    card(s, L, 1.22, CW, 1.6)
    text(s, L + 0.35, 1.42, CW - 0.7, 1.25,
         [{"text": "The ecological fallacy", "size": 16, "bold": True,
           "color": CLAY, "space_after": 4},
          {"text": "Every number in this project describes a local authority, not "
                   "a pupil. Kafar Yasif over-performs its prediction, and that "
                   "does not mean every pupil there scores above expectation: the "
                   "authority contains strong and weak results and we never see "
                   "them separately. Relationships measured between group averages "
                   "are also usually stronger than the same relationship between "
                   "individuals, so our correlations would overstate what holds "
                   "for any one pupil. The findings support decisions about "
                   "authorities, not claims about the pupils in them.",
           "size": 13.5, "line": 1.04}])

    rows = [
        ("No causality",
         "Observational and cross-sectional data. The index and the score move "
         "together and nothing here identifies a cause: sector composition, "
         "geography and school-level resourcing are all plausible confounders."),
        ("What the grouped split cost",
         "A split by row would have scored better, and 0.30 of that R² is "
         "memorising the authority rather than anything that carries over to a new "
         "one. We report the lower, honest number."),
        ("Coverage and years",
         "Of the 44 rows with no score, 40 are groups of under 30 pupils, so the "
         "smallest authorities are under-represented. 215 of 243 authorities appear "
         "in a single year, so year-to-year consistency is only checkable for 28."),
        ("A sharp threshold",
         "Three authorities carry median-imputed CBS variables, and the all-or-"
         "nothing flagging rule is sensitive at the margin, which is why the list "
         "we report is the 20 rather than the 65."),
    ]
    y = 2.95
    for head, bodytext in rows:
        text(s, L, y, 2.5, 0.6,
             [{"text": head, "size": 14, "bold": True, "color": SLATE,
               "line": 1.03}])
        text(s, L + 2.65, y, CW - 2.65, 0.8,
             [{"text": bodytext, "size": 13.5, "line": 1.03}])
        y += 0.84

    text(s, L, 6.27, CW, 0.45,
         [{"runs": [{"text": "What we would do differently: ", "bold": True,
                     "color": DEEPCLAY},
                    {"text": "school-level or pupil-level data to escape the "
                             "aggregation problem and test the organisational "
                             "explanation, a real multi-year panel with authority "
                             "fixed effects, and district and peripherality "
                             "variables for the geography this analysis lacks.",
                     "color": MUTED}],
           "size": 12}])
    footer(s, 11)
    return s


def s12_backup_importance(prs):
    s = blank(prs)
    slide_title(s, "Backup: which variables carry the model")
    h = picture(s, "deck_fig13.png", L, 1.35, 7.6)
    caption(s, L, 1.35 + h + 0.08, 7.6, "Fig 13. ",
            "Per-variable importance, impurity against permutation, with the "
            "one-hot dummies summed back per variable.")
    text(s, L, 5.5, 7.6, 1.1,
         [{"text": "Subject and grade dominate, and it is not close. Shuffling "
                   "subject costs 0.505 of R² and grade 0.169; the next variable "
                   "down is income per capita at 0.021 and ses_index itself ranks "
                   "ninth, at 0.011.",
           "size": 13.5, "line": 1.04}])

    text(s, 8.45, 1.35, 4.26, 0.3,
         [{"text": "Table 10. Block permutation", "size": 14, "bold": True,
           "color": DEEPCLAY}])
    grid_table(s, 8.45, 1.72, [2.46, 0.8, 1.0],
               [["Block shuffled", "Vars", "R² lost"],
                ["Test identity", 10, "0.609"],
                ["Subject and grade only", 6, "0.602"],
                ["Socio-economic block", 16, "0.374"],
                ["ses_index alone", 1, "0.012"]],
               SLATE, PAPER, row_h=0.3, size=11)

    card(s, 8.45, 3.45, 4.26, 2.3)
    text(s, 8.72, 3.65, 3.72, 1.9,
         [{"text": "Why both numbers are needed", "size": 14, "bold": True,
           "color": DEEPCLAY, "space_after": 4},
          {"text": "ses_index correlates above 0.8 with eight of the CBS "
                   "variables, so shuffling it alone does almost nothing: the "
                   "other fifteen rebuild it. Per-variable permutation says "
                   "socio-economic standing is worth 0.011, the block says 0.374, "
                   "and both are correct. Reporting only the first would have been "
                   "misleading.",
           "size": 12, "line": 1.04}])
    footer(s, 12)
    return s


def s13_backup_sensitivity(prs):
    s = blank(prs)
    slide_title(s, "Backup: every rebuild of the pipeline")
    text(s, L, 1.1, CW, 0.3,
         [{"text": "Table 11. Each row rebuilds the analysis from the raw files to "
                   "the flagged list, reusing the baseline's tuned settings.",
           "size": 12, "color": MUTED}])
    rows = [
        ["Variation", "Rows", "Out-of-fold R²", "Flagged", "Kept of the 65",
         "Changed direction"],
        ["Baseline, as reported", "1,749", "0.537", "65", "65", "0"],
        ["Sector rows instead of combined totals", "1,826", "0.515", "53", "52", "0"],
        ["All years 2015 to 2019", "2,540", "0.570", "44", "38", "0"],
        ["Drop cells under 30 pupils tested", "1,747", "0.536", "64", "57", "0"],
        ["Drop cells under 50 pupils tested", "1,653", "0.560", "68", "55", "0"],
        ["ses_cluster instead of ses_index", "1,749", "0.541", "62", "61", "0"],
        ["Linear regression instead of the forest", "1,749", "0.400", "51", "36", "0"],
    ]
    grid_table(s, L, 1.5, [4.6, 1.0, 1.75, 1.3, 1.75, 1.69], rows,
               SLATE, PAPER, row_h=0.38, size=12, header_size=12)

    card(s, L, 4.75, CW, 1.75)
    text(s, L + 0.35, 4.95, CW - 0.7, 1.4,
         [{"text": "The last column is zero on every row", "size": 15,
           "bold": True, "color": CLAY, "space_after": 4},
          {"text": "Across six rebuilds, including one that changes the model "
                   "family and one that adds two years of data, no authority ever "
                   "flips from over-performing to under-performing. Everything else "
                   "is more qualified: the choice of socio-economic measure barely "
                   "matters (61 of 65 kept), the data-shape choices cost a handful "
                   "each, and the year window matters most. Adding 2015 and 2019 "
                   "keeps only 38, which is mechanical: more years means more rows "
                   "per authority, and the rule needs every one of them to agree.",
           "size": 13, "line": 1.04}])
    footer(s, 13)
    return s


def main():
    OUT_DIR.mkdir(exist_ok=True)
    prs = new_deck()
    for fn in (s01_title, s02_motivation, s03_question, s04_data, s05_methods,
               s06_result1, s07_clusters, s08_subjects, s09_twenty,
               s10_conclusions, s11_limits, s12_backup_importance,
               s13_backup_sensitivity):
        fn(prs)
    prs.core_properties.title = "Beyond the Cluster"
    prs.core_properties.author = "Stav Tchizik; Or Cohen"
    prs.core_properties.subject = (
        "Which Israeli local authorities out- and under-perform their "
        "socio-economic standing in national achievement tests"
    )
    prs.save(OUT)
    print("wrote", OUT, "with", len(prs.slides._sldIdLst), "slides")


if __name__ == "__main__":
    main()
