"""Build version 2 of the deck: one slide per notebook section.

Nine slides - an opening slide plus the eight numbered sections of the report. Each
section slide carries the notebook's own heading verbatim, one sentence on what the
section is for, the figures that matter, and one sentence of conclusion.

Design helpers and palette are imported from build_deck.py, so both decks look alike.
Deck 1 is never touched: this writes its own file.
"""
import sys
from pathlib import Path

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_deck import (  # noqa: E402
    BODY, CLAY, COL, COL2_X, CW, DARK, DEEPCLAY, HEAD, INK, L, MUTED, MUTED_D,
    OUT_DIR, PAPER, SAGE, SAND, SLATE, TITLE_Y, W,
    blank, bullets, caption, card, circle, fill_bg, footer, grid_table, new_deck,
    picture, stat, text,
)

OUT = OUT_DIR / "Presentation_v2_Or_and_Stav.pptx"

# Section titles are the notebook's own headings, word for word.
HEADINGS = {
    1: "1. Exploratory Data Analysis and Data Cleaning",
    2: "2. Correlation Analysis",
    3: "3. Data Splitting",
    4: "4. Supervised Learning: Regression and Classification",
    5: "5. Unsupervised Learning: Clustering",
    6: "6. Feature Importance",
    7: "7. Robustness and Limitations",
    8: "8. Discussion",
}

PURPOSE_Y = 1.02
BODY_TOP = 1.62


def section(prs, slide_number, heading, purpose, dark=False):
    """Title (the notebook heading, verbatim) plus the one-sentence purpose line."""
    s = blank(prs)
    if dark:
        fill_bg(s, DARK)
    text(s, L, TITLE_Y, CW, 0.56,
         [{"text": heading, "font": HEAD, "size": 28, "bold": True,
           "color": PAPER if dark else INK}])
    text(s, L, PURPOSE_Y, CW, 0.5,
         [{"text": purpose, "size": 14.5, "color": MUTED_D if dark else SLATE,
           "line": 1.04}])
    footer(s, slide_number, dark=dark)
    return s


def conclusion(slide, x, y, w, h, sentence, dark=False):
    """The one-sentence conclusion, in the same place and style on every slide."""
    if not dark:
        card(slide, x, y, w, h)
    text(slide, x + (0.3 if not dark else 0.0), y + 0.17, w - 0.6, h - 0.34,
         [{"runs": [{"text": "Conclusion.   ", "bold": True,
                     "color": SAGE if dark else CLAY},
                    {"text": sentence, "color": MUTED_D if dark else INK}],
           "size": 13.5, "line": 1.04}])


# ================================================================ slides
def s1_opening(prs):
    s = blank(prs)
    fill_bg(s, DARK)
    text(s, 0.9, 1.5, 11.5, 1.0,
         [{"text": "Beyond the Cluster", "font": HEAD, "size": 50, "bold": True,
           "color": PAPER}])
    text(s, 0.9, 2.6, 10.9, 1.25,
         [{"text": "Which Israeli local authorities out- and under-perform "
                   "their socio-economic standing in national achievement tests?",
           "size": 19, "color": MUTED_D, "line": 1.12}])

    for i in range(10):                       # the official 1 to 10 cluster strip
        sq = s.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.9 + i * 0.52), Inches(4.18),
            Inches(0.42), Inches(0.34))
        sq.fill.solid()
        sq.fill.fore_color.rgb = SAGE
        sq.fill.fore_color.brightness = 0.75 - 0.11 * i
        sq.line.fill.background()
        sq.shadow.inherit = False
    text(s, 0.9, 4.62, 6.0, 0.3,
         [{"text": "official socio-economic cluster, 1 to 10", "size": 10.5,
           "color": MUTED_D}])

    text(s, 0.9, 5.25, 10.9, 0.35,
         [{"text": "The report in eight sections, one slide each", "size": 14,
           "color": SAGE}])
    text(s, 0.9, 5.72, 10.9, 0.4,
         [{"text": "Stav Tchizik (316062835)   ·   Or Cohen (206631509)",
           "size": 15, "color": PAPER}])
    text(s, 0.9, 6.12, 10.9, 0.75,
         [{"text": "Introduction to Data Science, Final Project", "size": 13,
           "color": MUTED_D, "space_after": 4},
          {"text": "Ministry of Education Meitzav scores, 2016 to 2018   ×   "
                   "CBS Socio-Economic Index of Local Authorities, 2017 edition",
           "size": 12, "color": MUTED_D}])
    return s


def s2_question(prs):
    """The question, the two sources, and how they were joined."""
    s = blank(prs)
    text(s, L, TITLE_Y, CW, 0.56,
         [{"text": "Research question, and the two sources behind it", "font": HEAD,
           "size": 28, "bold": True, "color": INK}])
    text(s, L, PURPOSE_Y, CW, 0.5,
         [{"text": "What we investigate, the two files it takes, and the work to join them.",
           "size": 14.5, "color": SLATE, "line": 1.04}])

    card(s, L, 1.58, CW, 1.0)
    text(s, L + 0.32, 1.74, CW - 0.64, 0.72,
         [{"text": "Which local authorities in Israel score higher or lower on "
                   "national tests than their socio-economic level would predict, "
                   "and what sets those authorities apart?",
           "font": HEAD, "size": 19, "bold": True, "color": DEEPCLAY, "line": 1.08}])

    text(s, L, 2.80, COL, 0.28,
         [{"text": "TWO SUPPORTING QUESTIONS", "size": 10.5, "bold": True,
           "color": CLAY}])
    supporting = [
        ("How closely does the index track the score?",
         "The baseline every gap is measured against."),
        ("Do achievement groups reproduce the official clusters?",
         "If they did, the official bands would already say it all."),
    ]
    y = 3.10
    for q, why in supporting:
        text(s, L, y, COL, 0.3,
             [{"text": q, "size": 14, "bold": True, "color": INK, "line": 1.03}])
        text(s, L, y + 0.31, COL, 0.3,
             [{"text": why, "size": 11.5, "color": MUTED, "line": 1.03}])
        y += 0.85

    text(s, COL2_X, 2.80, COL, 0.28,
         [{"text": "TWO OFFICIAL SOURCES", "size": 10.5, "bold": True, "color": CLAY}])
    sources = [
        ("Ministry of Education: Meitzav",
         "Grades 5 and 8, five subjects. 3,067 rows, 251 authorities, 2015 to 2019."),
        ("CBS: Socio-Economic Index, 2017",
         "255 authorities, 14 background variables, as a value and as ten clusters."),
    ]
    y = 3.10
    for head, bodytext in sources:
        card(s, COL2_X, y, COL, 0.78)
        text(s, COL2_X + 0.28, y + 0.13, COL - 0.56, 0.28,
             [{"text": head, "size": 13.5, "bold": True, "color": DEEPCLAY}])
        text(s, COL2_X + 0.28, y + 0.43, COL - 0.56, 0.28,
             [{"text": bodytext, "size": 11.5, "line": 1.03}])
        y += 0.95

    text(s, L, 5.08, CW, 0.28,
         [{"text": "AND THE WORK TO JOIN THEM", "size": 10.5, "bold": True,
           "color": CLAY}])
    joins = [
        ("Two code systems",
         "Matched by rule, four merged cities by hand. All 250 matched."),
        ("The same pupils twice",
         "Mixed authorities also get a combined row; we keep that and drop the parts."),
        ("Years that miss the index",
         "The index is a 2017 edition, so we keep 2016 to 2018."),
    ]
    y = 5.42
    for i, (head, bodytext) in enumerate(joins, start=1):
        circle(s, L, y + 0.01, 0.3, str(i), size=11)
        text(s, L + 0.42, y, 2.5, 0.28,
             [{"text": head, "size": 12.5, "bold": True, "color": SLATE}])
        text(s, L + 3.05, y - 0.01, CW - 3.05, 0.28,
             [{"text": bodytext, "size": 11.5, "line": 1.02}])
        y += 0.44

    footer(s, 2)
    return s


def s2_eda(prs):
    s = section(prs, 3, HEADINGS[1],
                "Load both files, repair what stops them merging, and look at how the "
                "scores are spread.")
    h = picture(s, "v2_fig01.png", L, BODY_TOP, 7.5)
    caption(s, L, BODY_TOP + h + 0.08, 7.5, "Fig 1. ",
            "Distribution of authority mean scores, 2016 to 2018.")

    stat(s, 8.35, BODY_TOP, 4.36, "3,067 → 1,749",
         "rows, after the year window, the double-counting fix and the join",
         num_size=28)
    stat(s, 8.35, BODY_TOP + 1.4, 4.36, "251 → 243",
         "authorities, each matched to the index by a key we built",
         color=SLATE, num_size=28)
    stat(s, 8.35, BODY_TOP + 2.8, 4.36, "44",
         "rows carry no score; 40 are groups under 30 pupils, which the Ministry "
         "suppresses", color=DEEPCLAY, num_size=28)

    conclusion(s, L, 5.45, CW, 1.05,
               "Scores are not one population — medians run from 519 in English "
               "grade 8 to 604 in Arabic grade 5 — so every later step works "
               "inside a subject and grade.")
    return s


def s3_correlation(prs):
    s = section(prs, 4, HEADINGS[2],
                "Measure how closely the index tracks the score, test by test, and how "
                "far the socio-economic variables overlap.")
    h = picture(s, "v2_fig04.png", L, BODY_TOP, 6.6)
    caption(s, L, BODY_TOP + h + 0.08, 6.6, "Fig 4. ",
            "Score against the index, with a least-squares line.")

    stat(s, 7.4, BODY_TOP, 5.31, "0.76 and 0.17",
         "the strongest and weakest of the nine correlations — English grade 8, "
         "at about 29 points per SD, against English grade 5", num_size=28)

    card(s, 7.4, BODY_TOP + 1.65, 5.31, 1.6)
    text(s, 7.7, BODY_TOP + 1.83, 4.71, 1.3,
         [{"text": "Fig 5. The variables repeat each other", "size": 13.5,
           "bold": True, "color": DEEPCLAY, "space_after": 4},
          {"text": "ses_index correlates above 0.8 with eight CBS variables, led "
                   "by income per capita at 0.96. So linear coefficients are "
                   "unstable, and forest importances split arbitrarily between "
                   "near-duplicates.",
           "size": 12, "line": 1.04}])

    conclusion(s, L, 5.80, CW, 1.05,
               "The index explains much in some tests and little in others, so gaps "
               "are measured inside a subject and grade — and because the "
               "variables are near-duplicates, no single one's importance can be read "
               "alone.")
    return s


def s4_splitting(prs):
    s = section(prs, 5, HEADINGS[3],
                "Split the table so the models are judged on authorities they have "
                "never seen.")

    panels = [
        (L, "Split by row — rejected", CLAY,
         ["236 of 243 authorities land in more than one set",
          "97% of test rows come from an authority already seen",
          "an authority's own training average alone gives R² = 0.30"]),
        (COL2_X, "Split by authority — used", SLATE,
         ["50 / 20 / 30 over authorities, stratified by cluster",
          "0 of 74 test authorities appear in training",
          "GroupKFold(5) applies the same rule when tuning"]),
    ]
    for x, head, colour, items in panels:
        card(s, x, BODY_TOP, COL, 2.5)
        text(s, x + 0.3, BODY_TOP + 0.22, COL - 0.6, 0.32,
             [{"text": head, "size": 16, "bold": True, "color": colour}])
        bullets(s, x + 0.3, BODY_TOP + 0.66, COL - 0.6, 1.7, items, size=13, gap=6)

    stat(s, L, 4.45, 5.6, "69%",
         "of 1,000 seeds lose a whole cluster from a set without stratifying, "
         "usually cluster 10 or 1, which hold 4 and 9 authorities", num_size=30)
    stat(s, COL2_X, 4.45, 5.6, "R² = 0.30",
         "the shortcut the grouped split removes, and why our numbers are lower "
         "than a row split would give", color=SLATE, num_size=30)

    conclusion(s, L, 5.80, CW, 1.0,
               "Splitting whole authorities removes a shortcut worth R² = 0.30, "
               "and stratifying keeps all ten clusters in all three sets.")
    return s


def s5_supervised(prs):
    s = section(prs, 6, HEADINGS[4],
                "Predict the score, check it again as a High / Low label, and turn what "
                "the models miss into a gap per authority.")
    h = picture(s, "deck_fig08.png", L, BODY_TOP, 6.5)
    caption(s, L, BODY_TOP + h + 0.08, 6.5, "Fig 8. ",
            "Mean standardized gap against the socio-economic index.")

    stat(s, 7.3, BODY_TOP, 5.41, "R² = 0.530",
         "the forest on unseen authorities, against 0.281 for a subject-and-grade "
         "baseline", num_size=28)
    stat(s, 7.3, BODY_TOP + 1.4, 5.41, "0.706",
         "logistic accuracy on the High / Low label, against 0.567 for the "
         "majority class", color=SLATE, num_size=28)
    stat(s, 7.3, BODY_TOP + 2.8, 5.41, "65 of 238",
         "authorities whose every row falls the same side of its prediction: "
         "33 above, 32 below", color=DEEPCLAY, num_size=28)

    conclusion(s, L, 5.84, CW, 1.05,
               "About half of an authority's score is predictable, and the half "
               "that is not identifies 65 authorities that beat or miss their "
               "prediction in every test they sit.")
    return s


def s6_clustering(prs):
    s = section(prs, 7, HEADINGS[5],
                "Run K-Means twice: once on grade 8 achievement scores, to compare "
                "against the official clusters, and once on the gaps.")
    h = picture(s, "deck_fig10.png", L, BODY_TOP, 4.5)
    caption(s, L, BODY_TOP + h + 0.08, 4.5, "Fig 10. ",
            "Groups against official clusters, 223 authorities.")

    stat(s, 5.45, BODY_TOP, 7.26, "1.54 against 2.70",
         "average distance between an authority's official cluster and its "
         "achievement group, against the distance if the two were unrelated",
         num_size=28)
    stat(s, 5.45, BODY_TOP + 1.45, 7.26, "55 of 223",
         "land on the same number, while 43 sit three or more clusters away",
         color=SLATE, num_size=28)

    card(s, 5.45, BODY_TOP + 2.5, 7.26, 1.35)
    text(s, 5.75, BODY_TOP + 2.64, 6.66, 1.1,
         [{"text": "Fig 11. The same K-Means run on the gaps", "size": 13.5,
           "bold": True, "color": DEEPCLAY, "space_after": 4},
          {"text": "2.59 against 2.78 — no relationship, which is the check "
                   "working. Six of its ten groups tilt by subject: group 4 (n = 15) "
                   "is above prediction in English, below it in Mathematics and "
                   "Science.",
           "size": 12, "line": 1.04}])

    conclusion(s, L, 5.80, CW, 1.05,
               "The two runs answer different questions: achievement groups track "
               "the official clusters in direction but not in detail, while gap "
               "groups show no socio-economic pattern at all and often deviate in one "
               "subject rather than evenly.")
    return s


def s7_importance(prs):
    s = section(prs, 8, HEADINGS[6],
                "Ask whether the index outweighs grade and subject, with the dummies "
                "summed back per variable.")
    h = picture(s, "deck_fig13.png", L, BODY_TOP, 7.3)
    caption(s, L, BODY_TOP + h + 0.08, 7.3, "Fig 13. ",
            "Variable importance two ways, permutation against impurity.")

    text(s, 8.2, BODY_TOP, 4.5, 0.3,
         [{"text": "Table 10. Block permutation", "size": 14, "bold": True,
           "color": DEEPCLAY}])
    grid_table(s, 8.2, BODY_TOP + 0.38, [2.7, 0.75, 1.05],
               [["Block shuffled", "Vars", "R² lost"],
                ["Test identity", 10, "0.609"],
                ["Subject and grade only", 6, "0.602"],
                ["Socio-economic block", 16, "0.374"],
                ["ses_index alone", 1, "0.012"]],
               SLATE, PAPER, row_h=0.3, size=11)

    card(s, 8.2, BODY_TOP + 2.2, 4.5, 1.6)
    text(s, 8.5, BODY_TOP + 2.36, 3.9, 1.3,
         [{"text": "Why both measures are needed", "size": 13.5, "bold": True,
           "color": DEEPCLAY, "space_after": 4},
          {"text": "ses_index has eight near-twins, so removing it alone costs "
                   "almost nothing — the twins cover for it. Per-variable "
                   "permutation ranks it ninth at 0.011; the block says 0.374.",
           "size": 12, "line": 1.04}])

    conclusion(s, L, 5.78, CW, 1.05,
               "No — what matters most is which exam a row is: hiding that costs "
               "the model 0.609 of its R² while hiding every socio-economic "
               "variable at once costs 0.374, so background matters a great deal but "
               "comes second to the test being sat.")
    return s


def s8_robustness(prs):
    s = section(prs, 9, HEADINGS[7],
                "Rebuild the analysis seven ways to see who survives every "
                "version, and say what it cannot support.")

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
    colw = [2.15, 0.8, 1.0]

    text(s, L, BODY_TOP, sum(colw), 0.3,
         [{"text": "Over-performing: 13", "size": 15, "bold": True,
           "color": DEEPCLAY}])
    grid_table(s, L, BODY_TOP + 0.34, colw,
               [head] + [[n, c, g] for n, c, g in over], SAGE, INK)

    text(s, 4.77, BODY_TOP, sum(colw), 0.3,
         [{"text": "Under-performing: 7", "size": 15, "bold": True,
           "color": DEEPCLAY}])
    grid_table(s, 4.77, BODY_TOP + 0.34, colw,
               [head] + [[n, c, g] for n, c, g in under], CLAY, PAPER)

    card(s, 8.95, BODY_TOP, 3.76, 1.75)
    text(s, 9.22, BODY_TOP + 0.16, 3.22, 1.45,
         [{"text": "What the seven rebuilds changed", "size": 13.5, "bold": True,
           "color": CLAY, "space_after": 4},
          {"text": "The grain, the years, the small-cell cut-off, the "
                   "socio-economic measure, the model family. Flagged counts move "
                   "between 44 and 68; no authority ever changes direction.",
           "size": 11.5, "line": 1.04}])

    card(s, 8.95, BODY_TOP + 1.88, 3.76, 1.75)
    text(s, 9.22, BODY_TOP + 2.04, 3.22, 1.45,
         [{"text": "The ecological fallacy", "size": 13.5, "bold": True,
           "color": CLAY, "space_after": 4},
          {"text": "Every number describes an authority, not a pupil. An "
                   "over-performing town still holds weak results we never see, and "
                   "links between averages look stronger than between individuals.",
           "size": 11.5, "line": 1.04}])

    conclusion(s, L, 5.72, CW, 1.0,
               "Twenty authorities stay flagged under every rebuild and none ever "
               "changes direction, but every number describes an authority, not a "
               "pupil.")
    return s


def s9_discussion(prs):
    s = section(prs, 10, HEADINGS[8],
                "What we found, what we could not explain, and what we would do next.",
                dark=True)

    items = [
        ("About half of an authority's score is predictable",
         "R² = 0.530 on unseen authorities against 0.281 for a subject-and-grade "
         "baseline. The gradient is real, strongest in English grade 8."),
        ("Which test it is outweighs what we know about the authority",
         "0.609 of R² against 0.374. So the proposal's question is answered no, "
         "though background is still one of two large blocks."),
        ("Twenty authorities depart dependably, and none ever flips",
         "65 under the original rules, 20 across all seven rebuilds: 13 above "
         "prediction, 7 below. The strongest claim we can make."),
        ("Nothing we measured explains why",
         "Across 22 variables, six never given to the model, the strongest link to "
         "an authority's gap is r = 0.162. The explanation is plausibly "
         "school-level."),
    ]
    y = 1.68
    for i, (head, bodytext) in enumerate(items, start=1):
        circle(s, L, y + 0.02, 0.4, str(i), fill=SAGE, color=DARK, size=14)
        text(s, L + 0.6, y, 11.4, 0.3,
             [{"text": head, "size": 15, "bold": True, "color": PAPER}])
        text(s, L + 0.6, y + 0.33, 11.4, 0.6,
             [{"text": bodytext, "size": 12.5, "color": MUTED_D, "line": 1.03}])
        y += 1.08

    conclusion(s, L, 6.05, CW, 0.8,
               "Socio-economic standing predicts about half of an authority's "
               "result, twenty authorities depart from it dependably, and nothing we "
               "measured explains which ones.", dark=True)
    return s


def main():
    prs = new_deck()
    for fn in (s1_opening, s2_question, s2_eda, s3_correlation, s4_splitting,
               s5_supervised,
               s6_clustering, s7_importance, s8_robustness, s9_discussion):
        fn(prs)
    prs.core_properties.title = "Beyond the Cluster, version 2"
    prs.core_properties.author = "Stav Tchizik; Or Cohen"
    prs.core_properties.subject = (
        "One slide per notebook section: which Israeli local authorities out- and "
        "under-perform their socio-economic standing in national achievement tests"
    )
    prs.save(OUT)
    print("wrote", OUT, "with", len(prs.slides._sldIdLst), "slides")


if __name__ == "__main__":
    main()
