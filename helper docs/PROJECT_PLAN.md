# Final Project — Full Execution Plan

**Course:** Introduction to Data Science, Semester 2, תשפ״ו (2025/2026)
**Team:** Stav Tchizik (316062835), Or Cohen (206631509)
**Question (final wording):** Which Israeli local authorities achieve **higher or lower Meitzav scores than their socio-economic standing predicts**, and what authority-level characteristics distinguish them?

This document is organized **by the sections of `Final_project_instructions_1.pdf`**. Inside each section, every
relevant correction from `Proposal_Response_English_Translation.pdf` is addressed explicitly and marked
`[Correction N]`. The nine corrections are the main grading lever for the final submission — the proposal grade
(92/100) is frozen, but *not* implementing these recommendations will lower the report grade.

> **Format decision: one self-contained notebook.** The instructions permit either a report plus a notebook
> zipped together, *or* "a notebook alone if it contains everything (in which case no zipping is required)".
> **This project takes the single-notebook route:** `DS_final_project_Or_and_Stav.ipynb` carries the full
> report narrative in markdown cells alongside the code that produces every figure and table. There is no
> separate PDF/DOCX. Wherever this document says "the report", it means **the report-level markdown cells
> inside the notebook** — see §3.
>
> The one thing a notebook cannot absorb is the two source data files. See §3.5 for how to keep the submission
> genuinely self-contained.

**Decisions already locked in (deviating from the proposal):**

| Topic | Proposal said | Final project does | Why |
| --- | --- | --- | --- |
| Years of education data | "multiple years" (2015–2019, unspecified) | **2016, 2017, 2018 only** | Centres the panel on the SES index year → `[Correction 8]` |
| CBS socio-economic index edition | 2021 edition | **2017 edition** (`datasets/t01_2017.xls`) | Removes the temporal mismatch the instructor flagged → `[Correction 8]` |
| Submission format | not specified | **Single self-contained notebook** (report + code in one `.ipynb`) | Allowed by §3 of the instructions; see §3 below |

With 2016–2018 education data and the 2017 index, the datasets are aligned to within ±1 year. This is a much
stronger answer to Correction 8 than merely "acknowledging a mismatch", and it must be *stated as a deliberate
design choice* in the notebook's Methods narrative, not left implicit.

---

## 0. Correction tracker (quick reference)

| # | Correction | Where it is implemented | Status |
| --- | --- | --- | --- |
| 1 | Split by local authority, not by row (`GroupShuffleSplit` / `GroupKFold`) | §3.3 Step 6 | ☐ |
| 2 | Remove causal wording ("affects" → "is associated with" / "predicts") | §2.1, §3.1, §4 | ☐ |
| 3 | Name and discuss the **ecological fallacy** | §3.1 Discussion, §4 | ☐ |
| 4 | Make deviation/outlier analysis the **central theme** | §2.1, §3.3 Steps 8–10 | ☐ |
| 5 | Define classification threshold precisely (within subject × grade) | §3.3 Step 11 | ☐ |
| 6 | Expand predictor set from CBS; pick **one** of CLUSTER / INDEX VALUE per use | §3.3 Steps 4b, 7 | ☐ |
| 7 | Grouped CV + baselines + weighting by `n_students_tested` | §3.3 Steps 6, 7, 12 | ☐ |
| 8 | Specify and align the years (2016–2018 × index 2017) | §2.2, §3.3 Step 2 | ☐ |
| 9 | AI-use statement (tools, purposes, prompts) | §5 → notebook section 9 | ☐ |

Section references of the form "§3.3 Step *n*" point at this document's pipeline; the notebook section each
step is written into is given in §3.2.

---

## 1. Timeline & Grade Weights

| Milestone | Deadline | Weight | Status |
| --- | --- | --- | --- |
| Project proposal | 15/8/2026 | 20% | ✅ Submitted, graded **92/100**, approved |
| Final submission — single self-contained Jupyter notebook (report narrative + code) | **18/10/2026** | 40% | ☐ In progress |
| Final presentation (scheduled meeting) | Within 2 weeks after 18/10/2026 | 40% | ☐ Not started |

### Working schedule (≈3 working days per person)

| Day | Owner split | Deliverable |
| --- | --- | --- |
| 1 | Both | Load + clean both files, resolve the authority-ID join, lock the analysis table (§3.3 Steps 1–4b) |
| 2 | Both | EDA + correlation + grouped split skeleton (§3.3 Steps 5–6) |
| 3 | Split | Regression track + residual/deviation analysis (§3.3 Steps 7–10) |
| 4 | Split | Clustering + classification + feature importance (§3.3 Steps 9, 11–13) |
| 5 | Both | Write the report-level markdown cells (Background, Question, Methods, Results, Discussion) into the notebook; figure polish |
| 6 | Both | Notebook cleanup + Restart & Run All, AI statement cell, slide deck, rehearsal |

Missing a deadline without prior approval = late submission per course policy. The notebook must be
**frozen and re-run end-to-end** at least one day before 18/10/2026.

---

## 2. Project Proposal (20%) — already graded, kept here as the requirements baseline

The proposal grade is final (92/100: Question 40/40, Dataset 27/30, Methods 25/30). This section records what
was promised and exactly how the final report changes it, because the report is graded partly on whether the
feedback was absorbed.

### 2.1 Research question — reframed

**Old (proposal):** "How does the socio-economic status (SES) of a local authority in Israel **impact** the
academic achievements of its students across different subjects and grade levels?"

`[Correction 2]` **Drop the causal verb.** The data are observational and cross-sectional; nothing here
identifies a causal effect. Use one of these verb forms consistently in the report, the notebook headers, and
the slides:

- "is **associated with**"
- "**predicts**"
- "**differences in** … **are accompanied by** differences in …"

`[Correction 4]` **Lead with the deviation question, not the main effect.** The SES-cluster ↔ achievement
gradient in Israel is already published (RAMA multi-year authority-level achievement reports broken down by
cluster; Knesset Research and Information Center analyses of the socio-economic index). Reproducing it is not
a contribution. So the question hierarchy for the final report is:

- **Primary (the contribution):** *Which local authorities score systematically above or below what their
  socio-economic profile predicts, and which authority-level characteristics separate the over-performers from
  the under-performers?*
- **Secondary (the calibration step, expected to confirm known results):** How strongly is the 2017 CBS
  socio-economic index associated with 2016–2018 Meitzav scores, by subject and grade?
- **Tertiary (the "two cluster worlds" comparison the instructor called the most interesting part):** Do
  data-driven clusters of authorities built from achievement profiles align with the official CBS 1–10
  clusters, and who are the mismatches?

The regression and classification models are **instruments for producing the primary answer**, not the
headline result. The report needs a short paragraph citing RAMA / the Knesset Research Center and stating
precisely what this analysis adds beyond them (the residual/deviation layer and the cluster-vs-cluster
comparison).

### 2.2 Dataset — restated with verified numbers

Two official government sources, merged. The merge is itself a substantive piece of data work, and the
instructor credited it as such.

**Dataset 1 — Ministry of Education Meitzav scores by authority** (`datasets/performances_by_areas_years_2015_2019.csv`)

| Property | Verified value |
| --- | --- |
| Rows | 3,067 |
| Columns | 12 |
| Grain | `year` × `rashut` (authority) × `norm_id` (sector) × `shichva` (grade) × `subject_id` |
| Years | 2015–2019 → **restricted to 2016–2018: 2,087 rows** `[Correction 8]` |
| Distinct authorities | 251 overall; **250** within 2016–2018 |
| Grades (`shichva`) | 5, 8 |
| Subjects (`subject_id`) | A (Arabic), E (English), H (Hebrew), M (Math), S (Science & Technology) |
| Target | `score` — mean standardized test score (range 396–695, mean ≈ 546, sd ≈ 39) |
| Missing | `score` 142 nulls; `n_students` 9 nulls; all other columns complete |
| Sample-size columns | `n_students_tested` (1–1,357, median 242), `n_students`, `n_schools_tested`, `n_schools`, `p_response` (response %, min 1 → suspicious) |

**Dataset 2 — CBS Socio-Economic Index of Local Authorities, 2017 edition** (`datasets/t01_2017.xls`, sheet `t01`)

| Property | Verified value |
| --- | --- |
| Layout | Multi-row bilingual header (metadata rows 0–9), data from row 10, 5 footnote rows at the end |
| Authorities | **255** (201 with a locality code + 54 regional councils) |
| Columns | 50 — identity block + 14 component variables, each as a (value, standardized value, rank) triple |
| Index columns | `INDEX VALUE` (continuous, mean 0, in sd units), `RANK` (1–255), `CLUSTER` (1–10) |

`[Correction 6]` **CLUSTER and INDEX VALUE are two encodings of the same measurement** — this redundancy cost
a point in the proposal. The rule for the final project, stated once in the report and enforced in code:

| Use case | Encoding used | Reason |
| --- | --- | --- |
| Model predictor (regression / classification) | **`INDEX VALUE`** (continuous) | Keeps full resolution; no artificial bins |
| Grouping / stratification / plots / comparison against data-driven clusters | **`CLUSTER`** (1–10) | The official grouping the instructor wants compared against |
| Both in the same model | ❌ Never | Same underlying measurement → collinear and uninterpretable |

`[Correction 6]` **Expand the predictor set.** The proposal effectively had three predictors (SES, grade,
subject), which makes a Random Forest and its feature importances near-vacuous. `t01_2017.xls` carries the
following authority-level variables, all available from the same file:

| Block | Variable (English header) |
| --- | --- |
| Identity | `MUNICIPAL STATUS` (0 = municipality, 99 = local council, other = regional council number), `POPULATION` |
| Demography | `MEDIAN AGE`, `DEPENDENCY RATIO`, `% OF FAMILIES WITH 4+ CHILDREN` |
| Schooling | `AVERAGE YEARS OF SCHOOLING (25–54)`, `% WITH ACADEMIC DEGREE (25–54)` |
| Employment | `% WITH INCOME FROM WORK`, `% OF WOMEN 25–54 WITHOUT INCOME`, `% WITH INCOME ABOVE / BELOW THRESHOLD`, `% RECEIVING INCOME SUPPORT` |
| Standard of living | `AVERAGE MONTHLY INCOME PER CAPITA`, `VEHICLES PER 100`, `AVERAGE VEHICLE LICENCE FEE`, `AVERAGE DAYS ABROAD` |

Plus derived predictors from the education file itself: `norm_id` (Hebrew-language, Arabic-language, or combined
for the 19 mixed authorities — see Step 3),
`n_students_tested`, `n_schools_tested`, `p_response`, `year`.

⚠️ The instructor named **district** and **peripherality index** specifically — these are **not** in table
`t01`. Two options; pick one and say which in the report:

1. Use the rich set above from `t01` only (sufficient — 14 variables, not 3), and note in the report that
   district/peripherality live in other CBS tables.
2. Download one more CBS table (e.g. the peripherality index / district listing by authority) and join it on
   the same locality code. Preferred if time allows, since geography adds a genuinely different signal rather
   than more SES-correlated variables.

⚠️ **Beware of circularity:** `AVERAGE YEARS OF SCHOOLING` and `% WITH ACADEMIC DEGREE` are *inputs to the
CBS index itself* and are adult-education measures, strongly correlated with the index. Including them is
legitimate but must be flagged: feature importance will partly reflect index construction, not independent
information. Report the correlation matrix among predictors and discuss it.

### 2.3 Methods — what changes from the proposal

| Proposal step | Final-project change | Correction |
| --- | --- | --- |
| EDA & cleaning | Unchanged in spirit; add the `norm_id` double-counting fix and small-cell handling | `[7]` |
| Correlation analysis | Unchanged; add within-subject × grade correlations, not just pooled | `[5]` |
| 50/30/20 random split | **Replaced** by a *grouped* 50/30/20 split with `rashut` as the group | `[1]` |
| K-Means clustering | Kept and **promoted** to a headline result (cluster-vs-cluster comparison) | `[4]` |
| Regression (LR vs RF) | Kept; add a **mean baseline**, grouped CV hyperparameter tuning, and sample weights | `[7]` |
| Classification (LogReg vs RF) | Kept; threshold defined **within subject × grade**, plus a **majority-class baseline** | `[5]`, `[7]` |
| Feature importance | Kept; now meaningful because the predictor set is wide | `[6]` |
| — | **New:** residual / deviation analysis as the primary deliverable | `[4]` |
| — | **New:** explicit ecological-fallacy and causality limitations | `[2]`, `[3]` |

---

## 3. Final Report + Jupyter Notebook (40%)

**One deliverable: `DS_final_project_Or_and_Stav.ipynb`.** The instructions allow "a notebook alone if it
contains everything", and that is the route taken. The notebook must therefore do two jobs at once, and the
grading rubric still scores them separately (Report readability 8% + Notebook organization 8%):

| Job | Carried by | Rubric item |
| --- | --- | --- |
| The **report** — background, question, methods, results, discussion, AI statement | **Report-level markdown cells**, written as continuous prose a reader can follow top to bottom without reading any code | Report readability (8%) + Discussion & interpretation (16%) |
| The **notebook** — reproducible code, figures, tables | Code cells, each introduced by a short *what and why* markdown cell | Notebook organization (8%) |

**The rule that keeps both jobs intact:** the two kinds of markdown cell are visually distinct and never
blended. Report-level cells use `##` / `###` headings and are written in finished report prose, with no
reference to variable names or cell mechanics. Step-level cells are one or two italic lines above a code cell,
explaining what that code does and why. A reader who skips every code cell and every italic line must still
read a complete 3–5 page report; a reader who reads everything must get a clean technical walkthrough.

**What "self-contained" does and does not cover.** The notebook contains everything the *report* needs —
all narrative, every figure, every table. It cannot contain the two source data files, so the submission
still has to make the data reachable; §3.5 sets out the options.

**Two risks created by merging the two deliverables, and the mitigations:**

| Risk | Mitigation |
| --- | --- |
| The report voice gets chopped into fragments by interleaved code, costing readability marks | Each report-level section is written as **one** markdown cell of continuous prose, placed *before* the code it describes — not split across the code cells |
| Results prose drifts out of sync with re-run outputs (numbers change, text doesn't) | Keep hard numbers in the **Results** narrative to the handful that matter, and quote them from printed cell output; re-read the Results and Discussion cells after the final Restart & Run All |

### 3.1 Report content — section-by-section writing brief

Each row below is one report-level markdown cell in the notebook. Total report prose target: **the equivalent
of 3–5 pages**, excluding code, figures, tables, and appendix sections.

The figures and tables each section draws on are fixed in the **figure and table register** in §3.3, and each
pipeline step there ends with a **→ Report** line naming what it must hand over. Write these cells *from* those
lines — if a step produced nothing a narrative cell needs, it does not belong in the notebook.

| Report section | Notebook location | What to write | Corrections to land here |
| --- | --- | --- | --- |
| **Background** | §1, before any code | Meitzav as the national standardized assessment; CBS socio-economic index as the standard authority-level SES measure; why authority-level gaps matter for budgeting and targeted intervention; who the audience is (Ministry of Education, RAMA, municipal leadership, policy makers) | — |
| **Question** | §1, immediately after Background | The three-level hierarchy from §2.1. **State explicitly that the question changed from the proposal** — the causal verb was removed and the emphasis moved from the SES↔achievement gradient to deviations from it — and say why (the gradient is already documented; cite RAMA and the Knesset Research and Information Center) | `[2]`, `[4]` |
| **Methods** | §2, as an upfront overview; the per-step detail then appears above each code block | The pipeline of §3.3 in order, naming **packages and parameters**: pandas, numpy, matplotlib/seaborn, scikit-learn (`GroupShuffleSplit`, `GroupKFold`, `GridSearchCV`/`RandomizedSearchCV`, `LinearRegression`, `RandomForestRegressor`, `LogisticRegression`, `RandomForestClassifier`, `KMeans`, `StandardScaler`, `permutation_importance`), scipy.stats. Spell out the join rule, the year restriction, the grouped split, the threshold rule, the weighting rule, and the random seed | `[1]`, `[5]`, `[6]`, `[7]`, `[8]` |
| **Results** | §7, after the modeling code, as a single narrative cell that refers back to the figures above it | Lead with the deviation / over- and under-performer findings; the SES gradient is presented as a validated calibration step, not the punchline. Built around the seven ⭐ headline items in the §3.3 register (Fig 8, Fig 10, Fig 11, Fig 13, Table 7, Table 10, Table 11), referring to each by its register ID. Oversized tables (ranked gaps A1, hyperparameter grids A3) are rendered in the §10 appendix, not here | `[4]` |
| **Discussion** | §8 | (a) What the results mean for the stated audience. (b) **Causality** — observational, cross-sectional data; associations only; confounding by composition, sector, geography `[2]`. (c) **Ecological fallacy** — *named explicitly*, one full paragraph: the data are authority aggregates, so an authority-level association says nothing about any individual student; a high-SES authority can contain low-achieving students and vice versa, and the authority-level correlation is typically *larger* than the individual-level one; the findings license decisions about *authorities* (where to target resources), not inferences about *students* `[3]`. (d) Whether the approach was appropriate, what would be done differently (student-level data, more years, a true panel / fixed-effects design), what remains unknown, and how to address it | `[2]`, `[3]` |
| **AI usage statement** | §9 | See §5 | `[9]` |

### 3.2 Notebook layout — where the report prose sits relative to the code

The instructions require the notebook to be organized in report order (background/EDA → methods → results →
discussion) with markdown cells as section headers. This skeleton satisfies that and leaves the report
readable as a unit. Build the notebook in this order; the pipeline steps referenced are from §3.3.

| Notebook section | Cell type | Content | §3.3 steps |
| --- | --- | --- | --- |
| Title cell | MD | Title, both names + IDs, course, date, and a 3–4 line **abstract** stating the question and the headline finding | — |
| **§1 Background & Question** | MD (report) | The Background and Question cells from §3.1 | — |
| **§2 Methods overview** | MD (report) | The Methods narrative from §3.1 — the whole pipeline in prose, up front, so the reader knows what is coming | — |
| **§3 Data loading & preparation** | MD + code | Setup, load both files, year restriction, `norm_id` fix, the join, post-merge cleaning, with verification output | Steps 1–4b |
| **§4 Exploratory data analysis** | MD + code | Distributions, small-cell diagnostics, missingness, correlation heatmap | Step 5 |
| **§5 Modeling** | MD + code | Grouped split, baselines, regression track, classification track | Steps 6, 7, 11 |
| **§6 Deviation analysis & clustering** | MD + code | Residuals per authority, over/under-performer characterization, K-Means vs official clusters, feature importance, sensitivity table | Steps 8–10, 12–13 |
| **§7 Results** | MD (report) | The Results narrative from §3.1 — pulls the findings of §4–§6 into one coherent account | — |
| **§8 Discussion** | MD (report) | The Discussion cell from §3.1. **Worth 16% on its own — the single most valuable cell in the notebook** | — |
| **§9 AI usage statement** | MD (report) | Tools, purposes, prompts (§5) | — |
| **§10 Appendix** | MD + code | Full authority residual ranking, hyperparameter grids, full correlation matrix, prompt log if long | — |

**Formatting requirements for the report-level cells:**

- [ ] Report prose totals the equivalent of ~3–5 pages, excluding code, figures, tables, and §10
- [ ] All five required report sections present (Background, Question, Methods, Results, Discussion) + AI statement
- [ ] Figures numbered and captioned in markdown, and referred to by number from the Results narrative
- [ ] Figures legible, axes labelled, units stated, colour-blind-safe palette
- [ ] Oversized tables rendered in §10, not inline
- [ ] Report cells readable on their own — no `df_merged`-style variable names, no "as shown in the cell below"

### 3.3 Notebook pipeline — the actual steps

These are the code-bearing steps that fill notebook sections §3–§6 of the skeleton above. Every non-trivial
step gets a short *what and why* markdown cell immediately above its code — distinct from the report-level
prose cells, which are written per §3.1. One random seed defined once at the top and reused everywhere.

Each step below carries three blocks:

| Block | What it is | What to do with it |
| --- | --- | --- |
| **→ Report** | The numbered figures and tables the step must produce, and which narrative cell consumes them | The specification — check against it when reconciling the register (§3.4) |
| **Prompt** | A ready-to-use prompt for implementing the step | Paste it into the AI tool; **copy it verbatim into the §9 AI-use statement** `[Correction 9]` |
| **For the report** | Short plain-language sentences to write into the notebook's report cells | Fill the `___` blanks after running the code |

Nothing should reach the Results or Discussion narrative that is not produced by a step here, and no step should
produce a figure no narrative cell ever mentions — if a figure has no reader, cut it.

**About the prompts.** They are written to be submitted, so each one states *why* the step is done the way it is,
not just what to compute — the reasoning is the part that shows the work is understood. Two consequences:

- **Edit them as you go.** If you change a prompt while working, submit the version you actually used. A prompt
  log that does not match the code is worse than no log.
- **A prompt is not a substitute for understanding the output.** Everything in the notebook has to be explainable
  in the meeting (§4), and these prompts are deliberately short enough that the explanation has to come from you.

**About the `___` blanks.** A blank marks text that depends on a result that does not exist yet. Leave it as a
literal blank until the code has run, then fill it in from the printed output. Do not guess what the result will
be and do not delete the blank — an unfilled `___` in the submitted notebook is a visible reminder; a deleted one
is a silent gap in the report.

#### Figure and table register

Fix these numbers once and use them everywhere (figure captions, Results prose, slides). ⭐ marks the
**headline** items the Results narrative must discuss; the rest are supporting evidence that can be referred to
in one clause or left for the reader to inspect.

**Reconciled against the notebook on 18/10/2026**, after Steps 1–9 were implemented. The numbering below is the
notebook's actual numbering, which drifted from this plan's first draft; where they differed, the notebook won.
Steps 11–13 are not written yet, so their rows are the numbers reserved for them.

| ID | Content | Produced by | Consumed by |
| --- | --- | --- | --- |
| Table 1 | Dataset summary: both sources, rows, columns, grain, coverage | Step 1 | Methods (§2) |
| Fig 1 | `score` distribution overall and by subject × grade | Step 5 | Methods (§2), justifies the Correction 5 threshold rule |
| Fig 2 | `score` vs `n_students_tested` | Step 5 | Methods (§2), justifies the small-cell decision |
| Fig 3 | `score` by CBS cluster, faceted by subject × grade | Step 5 | Results (§7), the known gradient as calibration |
| Fig 4 | `score` vs `ses_index` scatter, one panel per subject × grade | Step 5 | Results (§7) |
| Fig 5 | Correlation heatmap of the CBS variables | Step 5 | Discussion (§8), collinearity / circularity caveat |
| Table 4 | Split sizes in rows, authorities **and clusters**, with the zero-overlap assertion | Step 6 | Methods (§2) |
| Table 5 | Regression validation results: two baselines vs Linear vs Random Forest, weighted and unweighted | Step 7 | Results (§7) |
| Fig 6 | Predicted vs actual, and residuals vs predicted, both models | Step 7 | Discussion (§8), model adequacy |
| Fig 7 | Residual checks: distribution, by subject × grade, against the index | Step 7 | Discussion (§8) |
| Table 6 | Test-set results for the chosen model, used once | Step 7 | Results (§7) |
| ⭐ Fig 8 | **Signature figure:** `ses_index` vs mean standardized gap, extreme authorities labelled | Step 8 | Results (§7), the lead result |
| ⭐ Table 7 | **Each variable against the gap**, model-used and never-seen variables together, plus the two groups' medians | Step 8 | Results (§7) + Discussion (§8) |
| Fig 9 | Elbow + silhouette for *k*, both clustering inputs | Step 9 | Methods (§2) |
| ⭐ Fig 10 | Achievement groups vs official CBS clusters, crosstab heatmaps for both inputs | Step 9 | Results (§7) |
| Table 8 | Cluster agreement: ARI, NMI, Spearman, for scores and for gaps | Step 9 | Results (§7) |
| ⭐ Fig 11 | Gap-group profiles: uniform vs subject-specific deviation | Step 9 | Results (§7) + Discussion (§8) |
| Table 9 | Classification results: majority baseline vs Logistic vs Random Forest | Step 11 *(pending)* | Results (§7) |
| Fig 12 | Confusion matrix for the chosen classifier | Step 11 *(pending)* | Results (§7), supporting |
| ⭐ Fig 13 | Feature importance: impurity vs permutation, dummies summed back | Step 12 | Results (§7) + Discussion (§8) |
| ⭐ Table 10 | Block permutation: socio-economic block vs test-identity block | Step 12 | Results (§7), answers the proposal's question |
| ⭐ Table 11 | Sensitivity / robustness summary | Step 13 *(pending)* | Discussion (§8) |
| A1 | Ranked gaps for all 243 authorities (`data/authority_gaps.xlsx`) | Step 8 | Notebook §10 |
| A2 | Group assignments per authority (`data/authority_clusters.xlsx`) | Step 9 | Notebook §10 |
| A3 | Hyperparameter grids | Steps 7, 11 | Notebook §10 |
| A4 | Full CBS correlation matrix | Step 5 | Notebook §10 |
| A5 | Prompt log | §5 | Notebook §10 |

⚠️ **Tables 2 and 3 do not exist.** This plan reserved them for the cleaning counts (Steps 2, 3, 4b) and the
join coverage (Step 4a), but the notebook reports both as printed output rather than numbered tables. Either
number them when writing the Methods narrative, or leave the numbering with the gap and do not refer to
"Table 2" in the report. Do not renumber Tables 4–10 to close it; they are already referenced in notebook prose.

⚠️ **No PCA figure.** The first draft reserved one for Step 9; the implementation used the gap-group profile
plot (Fig 11) instead, which answers a sharper question. Nothing is missing.

That is 7 headline items (Fig 8, Fig 10, Fig 11, Fig 13, Table 7, Table 10, Table 11). Fig 11 was added after Step 9
found that deviation is sometimes subject-specific rather than uniform, which Step 8's single gap per authority
could not show. These are the set the Results and Discussion are built around, and the set the slide deck draws
on (§4).

#### Cleaning: what happens before the merge and what happens after

The data-cleaning rules come from *Lec 2 — Data Cleansing*: remove unnecessary data (irrelevant columns,
duplicate rows), handle missing values (row / column / impute, with the >40% column guideline), fix formats,
encode categoricals, and investigate outliers rather than deleting them — plus the framing rules: inspect
before changing, document every trade-off, and expect to iterate.

Cleaning is split across the merge, not done entirely on one side of it. The governing rule:

> **Clean before the merge whatever the merge depends on or would corrupt. Clean after the merge whatever the
> merge creates or reveals.**

| Cleaning task | Stage | Why there | Lecture rule |
| --- | --- | --- | --- |
| CBS structural fixes — footnotes, national-average rows, `..` → `NaN`, types, column names | **Pre** (Step 1) | The join is impossible until the key column is numeric | Wrong formats |
| Authority-name normalisation | **Pre** (Step 4a) | It is an input *to* the join, used to verify matches | Wrong formats |
| Year restriction to 2016–2018 | **Pre** (Step 2) | Row filter on one file; no reason to carry 980 doomed rows through a join | Remove unnecessary data |
| `norm_id` double-counting | **Pre** (Step 3) | Merging first attaches CBS attributes to duplicate rows, so the largest cities enter every later statistic at double weight | Duplicate records |
| Missingness **created by the join** | **Post** (Step 4b) | Cannot exist until the files are joined | Missing values (merge gaps) |
| Dropping redundant columns (`_z`, `_rank`, CLUSTER vs INDEX VALUE) | **Post** (Step 4b) | Relevance is judged against the target, which needs both files | Irrelevant features |
| Per-column missingness audit (>40% rule) | **Post** (Step 4b) | Rates differ on the merged subset — the analysed authorities are a subset of the 255 in the CBS file | When to remove a column |
| Missingness-bias check | **Post** (Step 4b) | "Is missingness related to socio-economic cluster?" is only askable once joined | Bias results |
| Row-level decisions — small cells, missing target | **Post** (Step 5) | Judged against the merged distribution | When to remove a row |
| Outliers | **Post** (Steps 5, 8) | The ones that matter are bivariate: a score is only extreme *given* the authority's index | Outliers |
| Encoding (one-hot `subject_id`, etc.) | **Post** (Step 7) | Operates on the final feature set | Data must be numeric |

⚠️ **Do not clean the same thing on both sides of the merge.** If types are coerced in Step 1 and again in
Step 4b, it becomes impossible to say where a value changed — which defeats the documentation the lecture asks
for. Each task above appears at exactly one stage.

⚠️ **The join itself is a cleaning decision.** It silently drops any authority that fails to match, so the
coverage counts in **Table 3** are not optional bookkeeping — they are the record of what the merge removed.

#### Step 1 — Setup and load

- Imports, `RANDOM_STATE = 42`, display options, plotting defaults.
- Load the education CSV; load the CBS `.xls` with `pandas.read_excel(..., sheet_name='t01', header=None, skiprows=10)` — `xlrd` is required for legacy `.xls`.
- Drop the 5 trailing CBS footnote rows (identified by a non-numeric / empty cluster value) and the two national
  summary rows (AVERAGE, NATIONWIDE VALUE).
- Assign explicit English column names to the CBS block instead of relying on the bilingual multi-row header.

**→ Report:** produce **Table 1** (dataset summary — source, rows, columns, grain, years, coverage for both
files). The Methods narrative needs from this step: the two source names and what each measures, the package
list, and the `RANDOM_STATE` value. Also state the data route chosen in §3.5.

**Prompt:**

> load two files: a csv of ministry of education test scores (meitzav), one row per authority, year, grade and
> subject, and a cbs excel file with the 2017 socio-economic index. the excel header runs over several rows in hebrew
> and english, real data starts at row 10, the last 5 rows are footnotes, and two rows near the top are national
> averages, so drop all of those and give the columns proper english names. set a random seed of 42 to use
> everywhere. print a summary of both files: rows, columns, years, number of authorities.

**For the report:**

- We use two official government datasets: Ministry of Education Meitzav scores by local authority, and the
  CBS socio-economic index of local authorities (2017 edition).
- The education file has 3,067 rows and 12 columns. Each row is one authority, year, grade and subject.
- The CBS file lists 255 local authorities with 50 columns, including the socio-economic index value, the rank,
  the 1–10 cluster, and 14 variables the index is built from.
- All analysis uses pandas, numpy, matplotlib/seaborn and scikit-learn, with a fixed random seed of 42 so the
  results can be reproduced.

#### Step 2 — Restrict years `[Correction 8]`

- Keep `year ∈ {2016, 2017, 2018}` → 2,087 rows, 250 authorities.
- Markdown cell justifying it: the 2017 CBS index edition is the SES measure, so the education window is
  centred on it (±1 year). Record the discarded 2015 and 2019 rows and say that extending the window would
  reintroduce the mismatch the instructor flagged.
- Sanity-check that scores do not drift materially across 2016–2018 (if they do, keep `year` as a model
  covariate and say so).

**→ Report:** first row of **Table 2** (rows and authorities before/after the year filter). The Methods
narrative must state the window and the alignment rationale explicitly in one or two sentences — this *is*
Correction 8, and a grader looking for it should find it without hunting. The Discussion notes the cost: three
years is a short window and cannot support a trend claim.

**Prompt:**

> keep only 2016–2018 in the education data, since our socio-economic index is the 2017 one and we don't want to
> compare scores to an index measured years off. print rows and authorities before and after, and check whether the
> average score moves much between the three years, if it does we should keep year as a variable later.

**For the report:**

- We limited the education data to 2016–2018 because the socio-economic index we use is the 2017 edition. This
  keeps the two datasets within one year of each other.
- This left 2,087 rows covering 250 local authorities, out of 3,067 rows in the original file.
- `___` *(fill in after running: whether average scores were stable across the three years, and therefore
  whether `year` was kept as a variable in the models.)*
- The cost of this choice is that three years is too short a window to say anything about trends over time.

#### Step 3 — Fix the double-counting in `norm_id` ⚠️ **(not in the proposal — discovered in the data)**

`norm_id` is the sector / language of instruction: **3 = Hebrew-language education, 9 = Arabic-language
education, 1 = authority-wide total for mixed authorities.** For the 19 mixed authorities (Haifa, Tel
Aviv-Yafo, Lod, Akko, Be'er Sheva, …) the file contains **both** the `norm_id = 1` total **and** the
`norm_id ∈ {3, 9}` sector rows, and the total is the aggregate of the parts — verified: Haifa 2015 grade-5
English `n_students_tested` 664 = 537 (sector 3) + 127 (sector 9). There are 416 rows that duplicate a
`(year, authority, grade, subject)` key for exactly this reason.

Pick **one** grain and state it in the report. ⚠️ Note `norm_id = 1` is **not** a universal total — it exists only
for the 19 authorities that have both sectors, so "keep only the totals" is not an available option: it would
leave 207 rows and 19 authorities out of 250.

- **Option B — authority totals (chosen):** use `norm_id = 1` where it exists, otherwise the single sector row.
  One row per authority × year × grade × subject; 1,793 rows, all 250 authorities. Simplest grain, and it matches
  the research question, which is about authorities. Cost: for mixed authorities it averages the two sectors
  together and hides any gap between them, and `norm_id` becomes an authority-type marker (combined / Hebrew /
  Arabic) rather than a clean sector variable.
- **Option A — sector-level rows only:** drop `norm_id = 1`, keep 3 and 9; 1,880 rows, all 250 authorities. Keeps
  the Hebrew/Arabic distinction as a predictor and gives a within-authority contrast for the 15 mixed cities that
  have both sectors — same socio-economic index, different scores. Retained as the **sensitivity variation** in
  Step 13 rather than the main grain.

Whichever is chosen, **never keep both** — it double-counts the largest cities and silently weights them twice.

**→ Report:** second row of **Table 2**, plus the verification number that proves the aggregation (the Haifa
check, or the equivalent on your chosen cell). The Methods narrative gets a short paragraph: what `norm_id`
encodes, that the file mixes totals with parts, which grain was kept and why. This is not in the proposal or
the feedback, so it reads as independent data work — worth stating plainly rather than burying in a comment.
The Discussion notes the cost of the chosen grain: combining the sectors in mixed authorities averages over any
gap between them, which is exactly what the sector-rows variation in **Table 11** is there to test.

**Prompt:**

> `norm_id` is the education sector: 3 is hebrew-language schools, 9 is arabic-language, and 1 is the two combined —
> but the 1 rows only exist for the 19 authorities that have both sectors. so those authorities are currently counted
> twice, once as a total and once per sector: haifa's grade 5 english total of 664 students tested is just 537 + 127
> from the two sectors. check that on a couple of authorities, then build one row per authority, year, grade and
> subject by taking the `norm_id = 1` row where it exists and the single sector row everywhere else. print rows and
> authorities left.

**For the report:**

- The column `norm_id` marks the education sector: Hebrew-language, Arabic-language, or the two combined. The
  combined rows exist only for the 19 authorities that have both sectors.
- For those authorities the file contains both the combined total and the two sector rows, so they appear twice.
  We confirmed this: Haifa's grade 5 English total of 664 tested students equals the 537 and 127 of its two
  sectors added together.
- Keeping both would count the largest cities twice and give them double weight. We therefore used the combined
  row where it exists and the single sector row everywhere else, giving one row per authority, year, grade and
  subject.
- `___` *(fill in after running: rows and authorities remaining.)*
- The cost of this choice is that for mixed authorities it averages the two sectors together, hiding any gap
  between them. We test the alternative — keeping the sector rows instead — in the sensitivity analysis.

#### Step 4a — Join the two datasets

**Pre-merge.** The last step before the files become one table; everything in it exists to make the join
correct and verifiable.

The two systems use different authority numbering (the proposal correctly flagged Ofakim = `315` in education
vs `31` in CBS). The verified rule, which covers 247 of 251 authorities with no hand-built dictionary:

| Authority type | Detection | Join key |
| --- | --- | --- |
| Municipality / local council | `rashut % 100000 != 0` | `rashut // 10` → CBS `CODE OF LOCALITY` (193/197 matched) |
| Regional council | `rashut >= 100000 and rashut % 100000 == 0` | `rashut // 100000` → CBS `MUNICIPAL STATUS` (54/54 matched; regional councils have **no** locality code in `t01` — their council number sits in the municipal-status column) |

Four merged municipalities need a manual override (their education codes are not `CBS code × 10 + check digit`):

| `rashut` | Authority | CBS `CODE OF LOCALITY` |
| --- | --- | --- |
| 13508 | קדימה-צורן | 195 |
| 13516 | מודיעין-מכבים-רעות | 1200 |
| 13524 | בנימינה-גבעת עדה | 9800 |
| 13573 | יהוד - מונוסון | 9400 (listed as "יהוד") |

Also normalize three renamed/respelled authorities before any name-based verification:
מג'אר / מגאר, נוף הגליל / נצרת עילית, ערערה בנגב / ערערה-בנגב.

**Verification cells (required):** assert that 100% of education authorities match after the overrides; print
any unmatched rows; cross-check matched pairs by normalized Hebrew name and list the mismatches; report how many
of the 255 CBS authorities have no education data (these are legitimately absent — small authorities with no
Meitzav reporting — and should be reported as coverage, not as an error).

**→ Report:** produce **Table 3** (join coverage: matched by the locality rule, by the regional-council rule,
by manual override, unmatched, and CBS authorities with no education data). The Methods narrative needs the two
join rules in one sentence each plus the count of manual overrides — the instructor singled this merge out as
"genuine data work", so it earns a short paragraph, not a footnote. The Discussion notes which authorities the
analysis therefore does *not* cover, since that bounds who the conclusions apply to.

**Prompt:**

> the two files number authorities differently so i need to build the merge key. for cities and local councils the
> education code is the cbs code with an extra digit on the end, so dividing by 10 gives the cbs code (ofakim is 315
> vs 31). regional councils have no locality code in the cbs file, their council number is in the municipal status
> column, and their education code is that number times 100,000. set up both rules, then fix four merged cities by
> hand: 13508→195, 13516→1200, 13524→9800, 13573→9400. then verify: fail if any education authority didn't match,
> print the ones that didn't, compare names on both sides to catch wrong matches, and tell me how many cbs
> authorities have no education data.

**For the report:**

- The two datasets number local authorities differently, so merging them required building a key.
- For municipalities and local councils, the education code is the CBS locality code plus one extra digit
  (Ofakim is 315 in the education data and 31 in the CBS data), so dividing by 10 gives the CBS code. This
  matched 193 of 197 authorities.
- Regional councils have no locality code in the CBS file; their council number is in the municipal status
  column, and their education code is that number times 100,000. This matched all 54.
- Four merged municipalities follow neither rule and were mapped by hand. Three authorities have been renamed or
  are spelled differently between the files, so names were normalised before checking the merge.
- We verified the merge by requiring every education authority to find a match and by comparing names on both
  sides.
- `___` *(fill in after running: how many CBS authorities have no education data, and therefore which
  authorities the analysis does not cover.)*

#### Step 4b — Clean the merged table `[Correction 6]`

**Post-merge.** Four cleaning tasks that could not be done on either file alone. This is also where the
analysis table is finalised, so the column inventory at the end of this step is the feature set everything
downstream uses.

1. **Handle the gaps the merge created.** The lecture names data merging as a *cause* of missing values. Decide
   and state the join semantics: education rows with no CBS match (should be none after the Step 4a overrides)
   and CBS authorities with no education data (legitimately absent — small authorities with no Meitzav
   reporting). Drop what cannot be used and record the counts rather than letting an inner join remove them
   silently.
2. **Drop redundant columns** `[Correction 6]`. 28 of the 50 CBS columns are the `_z` (standardized) and
   `_rank` variants of the same 14 variables — keep the raw values and drop the other two forms. Then apply the
   §2.2 rule: `INDEX VALUE` (continuous) for models, `CLUSTER` (1–10) for grouping and the Step 9 comparison,
   never both in one model. State the final column count.
3. **Audit missingness per column on the merged table**, not on the raw CBS file. The ~250 authorities with
   education data are a *subset* of the 255 in the file, so the rates genuinely differ — a variable can be well
   populated across all 255 and mostly missing among the ones we analyse, or the reverse. Judging it on the raw
   file answers the wrong question. Flag anything over 40% missing as a removal candidate per the lecture, and
   note that 250 CBS cells are suppressed (`..`, "not for publication") rather than absent by accident.
4. **Check whether missingness is biased.** Cross-tabulate the remaining missing values against `ses_cluster`
   and sector. If they concentrate in particular clusters, dropping them does not merely shrink the data, it
   tilts it — and since our question is *about* differences between clusters, that would bias the headline
   result directly. Report the check either way.

⚠️ Row-level decisions — the small-cell cutoff and the 142 rows with no `score` — belong to Step 5, not here.
Keeping them separate is what stops the same rule being applied twice.

**→ Report:** records the post-merge column inventory (50 CBS columns in, how many kept after
dropping the `_z` / `_rank` variants, how many flagged over 40% missing) and the final
analysis-table shape.

| Narrative cell | What this step supplies |
| --- | --- |
| Methods (§2) | One paragraph: that cleaning was split across the merge and why, the redundancy that was dropped, and the one-encoding-per-use rule `[6]` |
| Discussion (§8) | The missingness-bias result — whether what we dropped was spread evenly or concentrated in particular socio-economic clusters |

**Prompt:**

> clean the merged table. first, the merge creates its own gaps, so tell me which education authorities found no cbs
> match and which cbs authorities have no education data, then drop what we can't use. second, 28 of the 50 cbs
> columns are just standardised (_z) and rank copies of the same 14 variables, so keep the raw values, the
> continuous index for models and the 1 to 10 cluster for grouping. last, check the missing rate per column on the
> merged table, not the raw file, since we analyse only a subset of the 255 authorities, flag anything over 40%, and
> say whether the missing values concentrate in particular clusters, which would bias our comparison.

**For the report:**

- Cleaning was split around the merge: anything the merge depended on was fixed first, and anything the merge
  created or revealed was fixed after.
- The merge itself creates missing values where records do not match. `___` *(fill in after running: how many
  rows or authorities were dropped for this reason.)*
- The CBS file gives each of its 14 variables three times — the raw value, a standardised value and a rank — so
  we kept the raw values and dropped the other two forms. We also use only one encoding of the socio-economic
  measure per purpose: the continuous index value in the models, and the 1–10 cluster for grouping and for
  comparing against our own clusters. `___` *(fill in after running: columns before and after.)*
- We checked the share of missing values in each column on the merged table rather than the original file,
  because the authorities we analyse are only a subset of those in the CBS file. `___` *(fill in after running:
  whether any column exceeded 40% missing, and what was done about it.)*
- `___` *(fill in after running: whether the missing values were spread evenly or concentrated in particular
  socio-economic clusters. This matters because concentrated missingness would bias exactly the comparison the
  project is about.)*

#### Step 5 — EDA `[Correction 7]`

- `.info()`, `.describe()`, null counts per column.
- Target distribution: `score` histogram overall and by subject × grade — this is what motivates Correction 5.
  Subject and grade shift the score level, so a single pooled median is not a meaningful threshold.
- **Small-cell diagnostics** (the issue the instructor credited and wants carried into modeling): 80 rows with
  `n_students_tested < 30`, 221 with `< 50`, minimum 1. Plot `score` against `n_students_tested` and show the
  variance funnel (tiny cells are noisy in both directions). Decide and record the rule:
  - exclude cells with `n_students_tested < 30` (sensitivity-check at 20 and 50), **and**
  - weight the remaining observations by `n_students_tested` in modeling (Step 7).
- `p_response` has a minimum of 1% — investigate and either drop implausibly low response rates or justify
  keeping them.
- Missing `score` (142 rows): check whether missingness is related to `n_students_tested` or sector (i.e.
  whether it is plausibly MCAR). Drop rows with no target and report the count; never impute the target.
- Boxplots of `score` by CBS `CLUSTER`, faceted by subject and grade. Boxplots by `norm_id`.
- Scatter of `score` vs `INDEX VALUE`, one panel per subject × grade.
- Correlation heatmap of **all** CBS predictors against each other — this is where the collinearity warning
  from §2.2 gets evidence.

**→ Report:** produce **Fig 1** (score distribution by subject × grade), **Fig 2** (variance funnel), **Fig 3**
(score by CBS cluster), **Fig 4** (score vs `INDEX VALUE`), **Fig 5** (predictor correlation heatmap), and the
remaining rows of **Table 2** (rows dropped for small cells and for missing target). Full correlation matrix →
appendix **A3**.

The narrative cells draw on this step as follows:

| Narrative cell | What this step supplies |
| --- | --- |
| Methods (§2) | The small-cell cutoff and the weighting decision, each with the count it affects (80 rows < 30, 221 < 50); the missing-target count (142) and that it was dropped, never imputed; Fig 1 as the justification for a *within-group* classification threshold `[5]` |
| Results (§7) | Fig 3 and Fig 4 as the **calibration** result — the SES gradient reproduced, explicitly framed as the known finding the project does not claim credit for `[4]` |
| Discussion (§8) | Fig 5 — predictors are heavily intercorrelated, and the schooling/degree variables feed the CBS index itself, so feature importance is partly structural `[6]` |

**Prompt:**

> explore the merged data. show the score distribution overall and by subject and grade, since they sit at different
> levels and that matters for how we label high/low later. plot score against number of students tested and tell me
> how many rows have under 20, 30 and 50, small cells are noisy. check whether the rows with no score are mostly
> small samples or one sector, then drop them. then show score by socio-economic cluster split by subject and grade,
> score against the continuous index value, and a correlation heatmap of the cbs variables.

**For the report:**

- Different subjects and grades sit at different score levels, so scores are not directly comparable across
  them. This is why the high/low label later is defined within each subject and grade rather than once overall.
- The number of students tested per row ranges from 1 to 1,357. Small cells are noisy, so we excluded rows with
  fewer than 30 students tested and weighted the remaining rows by the number tested in the models.
- 142 rows have no score. We dropped them rather than filling them in, because the score is what we are
  predicting.
- `___` *(fill in after running: what the plots show — how clearly scores rise with the socio-economic index,
  and how strongly the CBS variables correlate with each other.)*
- Several CBS variables, such as average years of schooling and the share with an academic degree, are
  themselves used to build the socio-economic index, so they are expected to overlap with it heavily.

#### Step 6 — Grouped train / validation / test split `[Correction 1]` `[Correction 7]`

This is the single highest-value correction (4 of the 5 methodology points deducted).

- The cleaned analysis table has **1,749 rows from only 243 authorities** (median 7 rows each, range 1–25), so
  rows are **not independent**. A row-level random split would put the same authority in train and test; the
  model would memorize authority means and the reported accuracy would be inflated.
- Use `rashut` as the group:
  - `GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=RANDOM_STATE)` → hold out test (30%).
  - Apply `GroupShuffleSplit` again on the remaining 70% to carve out validation (20% of total ⇒
    `test_size = 0.2/0.7 ≈ 0.2857`), leaving ≈50% train — preserving the proposal's 50/30/20 intent at the
    authority level.
  - Use `GroupKFold(n_splits=5)` inside `GridSearchCV` / `RandomizedSearchCV` (`cv=GroupKFold(5)`,
    `groups=rashut`) for all hyperparameter tuning.
- ⚠️ **Watch cluster coverage.** Cluster 10 holds only **4** authorities and cluster 1 holds **9**, so a plain
  grouped split can leave a whole cluster out of a set (expected cluster-10 authorities in a 20% validation set:
  0.8). Stratify the grouped split by `ses_cluster` where possible — `StratifiedGroupKFold` does this for the CV
  folds — and print the per-cluster breakdown of each set either way.
- ⚠️ Rows per authority range 1–25, so a 50/30/20 split *by authority* will not be 50/30/20 *by row*. Report both.
- **Assert zero authority overlap** between the three sets, and print set sizes in both rows and authorities.
- **Report both numbers side by side:** metrics under a naive row-level split vs the grouped split. The drop is
  the evidence that the correction was understood. The instructor said it outright: "the results may become
  worse after doing this, and that is exactly the point."

**→ Report:** produce **Table 4** (split sizes in rows *and* authorities, plus the printed zero-overlap
assertion). The Methods narrative must name `GroupShuffleSplit` / `GroupKFold` with `rashut` as the group and
explain in two or three sentences *why* rows are not independent — this is the most heavily weighted single
correction, so it needs prose, not just a function call. The row-level-vs-grouped comparison goes into
**Table 11** (Step 13) and is quoted in the Discussion as an honesty point: state the inflated number, the honest
number, and that the honest one is the one being reported `[1]`.

**Prompt:**

> split into train, validation and test by authority, not by row. the cleaned table has 1,749 rows from only 243
> authorities, so if an authority lands in both train and test the model can memorise its average score and accuracy
> looks better than it is. use `GroupShuffleSplit` with authority as the group, roughly 50/30/20, and `GroupKFold` by
> authority for tuning later. cluster 10 has only 4 authorities and cluster 1 has 9, so a plain split can leave a
> cluster out of a set, stratify by cluster if you can. rows per authority run from 1 to 25, so print each set size in
> rows, authorities and clusters, and fail if an authority turns up in two sets. also run a plain row split once so we
> can show the difference.

**For the report:**

- Our rows are not independent: the analysis table has 1,749 rows from only 243 local authorities, a median of 7
  rows each, so each authority appears many times.
- A random split by row would put the same authority in both the training and test sets. The model could then
  memorise that authority's average score, and the accuracy we report would be too optimistic.
- We therefore split by authority using `GroupShuffleSplit`, about 50% training, 30% test and 20% validation,
  and used `GroupKFold` by authority for tuning. We checked that no authority appears in two sets.
- Because the smallest clusters hold very few authorities (4 in cluster 10, 9 in cluster 1), we also checked that
  every cluster is represented in each set rather than trusting a random split to spread them.
- Splitting by authority does not split the rows in the same proportions, because authorities contribute between
  1 and 25 rows each, so we report both counts. `___` *(fill in after running.)*
- `___` *(fill in after running: the size of each set in rows and authorities, and how much lower the scores are
  with the grouped split than with a random row split. The grouped-split numbers are the ones we report.)*

#### Step 7 — Regression track `[Correction 7]`

- **Baseline (required):** predict the training-set mean `score`; also a smarter baseline predicting the
  subject × grade mean. Report R² and RMSE for both. Every model must be reported against these.
- **Model A — Linear Regression / Ridge:** predictors = `INDEX VALUE` + the expanded CBS variables + `shichva`
  + `subject_id` (one-hot) + `norm_id` + `year`. Report coefficients, significance, R² on validation.
  Standardize continuous predictors (`StandardScaler` inside a `Pipeline` so the scaler is fit on train folds
  only).
- **Model B — RandomForestRegressor:** tuned via `GridSearchCV` with `GroupKFold` over `n_estimators`,
  `max_depth`, `min_samples_leaf`, `max_features`.
- **Sample weighting `[Correction 7]`:** pass `sample_weight = n_students_tested` (after the small-cell
  exclusion) to both models. Report weighted vs unweighted metrics and say which is the headline and why.
- Evaluation on validation for model selection; the **test set is touched once**, at the end, for the final
  chosen model. Metrics: R², RMSE, MAE.
- Residual diagnostics: residuals vs fitted, residuals vs `INDEX VALUE`, residuals by sector, QQ plot.

**→ Report:** produce **Table 5** (both baselines vs Linear vs Random Forest, weighted and unweighted, with R²,
RMSE, MAE on validation and the single final test-set number for the chosen model) and **Fig 6** (residual
diagnostics). Hyperparameter grids → appendix **A2**.

| Narrative cell | What this step supplies |
| --- | --- |
| Methods (§2) | Model families, the predictor list, the tuning procedure (grouped CV), the weighting rule, and the statement that the test set was used exactly once `[7]` |
| Results (§7) | Table 5 read against the baselines — how much of the variance in authority-level scores the SES profile actually explains. State the baseline numbers first, then the models; a model that barely beats the subject × grade mean is a finding, not a failure |
| Discussion (§8) | Fig 6 — whether the linear form was adequate, heteroscedasticity, which sector or cluster the model fits worst, and what that implies for the residual analysis in Step 8 |

**Prompt:**

> build models to predict an authority's average score. start with two baselines so we know what counts as doing well:
> always guess the overall average, and guess the average for that subject and grade. then fit a linear regression and
> a random forest using the socio-economic index plus the other cbs variables, grade, subject, sector and year. keep
> the scaling inside a pipeline so it only learns from training data. tune the forest with `GroupKFold` by authority.
> weight rows by students tested, since a row from 1,000 students is better evidence than one from 20, and show
> results with and without weighting. compare on validation only and use the test set once at the end. give me r²,
> rmse, mae and residual plots.

**For the report:**

- We compared two baselines (predicting the overall mean, and predicting the mean for each subject and grade)
  against a linear regression and a random forest, so that model quality is judged against something.
- Predictors were the socio-economic index value plus the other CBS authority variables, along with grade,
  subject, sector and year.
- Rows were weighted by the number of students tested, because rows based on few students are less reliable.
- Model choice used the validation set; the test set was used only once, at the end.
- `___` *(fill in after running: R² and RMSE for the baselines and both models, how much the models beat the
  baselines, and which model was chosen.)*
- `___` *(fill in after running: what the residual plots show about whether the model fits some sectors or
  clusters worse than others.)*

#### Step 8 — Deviation / residual analysis `[Correction 4]` ⭐ **primary deliverable**

- Use the model chosen in Step 7: the **unweighted Random Forest** (validation R² 0.463, test 0.530). Note
  weighting by `n_students_tested` was *rejected* there (0.463 → 0.413), so the per-authority aggregate is
  unweighted too; report the weighted version only as a robustness line.
- ⚠️ **Residuals must be out-of-fold.** Step 7 leaves honest residuals only for the 48 validation and 74
  test authorities; the 121 training authorities' residuals are shrunk because the model was fitted to them.
  Ranking all 243 together would mix two different quantities and flatter the training set. Use
  `cross_val_predict` with `GroupKFold` on `rashut` across the whole table so every authority is predicted by a
  model that never saw it.
- ⚠️ **Standardize residuals within subject × grade before averaging.** The notebook's residual
  diagnostics show the residual SD runs from 17 points (Hebrew grade 5) to 38 (Science grade 8), so a +30
  residual is a far rarer event in one test than another. Averaging raw residuals would let the high-variance
  tests dominate.
- Aggregate **per authority** across its subjects and grades: mean standardized residual, plus the standard
  error and the consistency of sign across that authority's rows.
- Rank authorities. Produce the signature figure: `ses_index` on x, **mean standardized residual** on y, with
  the most extreme authorities labelled. ⚠️ Not mean *score* on y: authorities are tested on different
  subject mixes (group medians run 519–604), so raw mean scores are not comparable across authorities.
- **Separate signal from noise:** an authority counts as an over/under-performer only if its residual is
  consistent across its subjects and grades and large relative to its own uncertainty. Report how many
  authorities pass that bar. ⚠️ Consistency is across **subjects and grades, not years**: Meitzav rotates
  schools through three national groups tested once every three years, so 215 of the 243 authorities appear in
  a single year. Year-to-year consistency is a bonus check for the 28 that span two or more. The 5 authorities
  with a single row cannot be assessed at all and are excluded by name.
- **Characterize the two groups:** compare over-performers vs under-performers on the expanded CBS variables
  (population, median age, dependency ratio, % 4+ children, income, sector, municipal status, and
  district/peripherality if added), **plus variables the model never saw** (school count, school size, cohort
  size, response rate), since the model's own predictors are near-orthogonal to its residuals and a null there
  would prove nothing. Measure it as the **correlation between the continuous gap and each variable** across all
  eligible authorities: it uses every authority rather than only the flagged ones, keeps the size of each gap,
  and stays within methods used elsewhere in the project. *This table is the project's actual contribution.*
- Add the short literature paragraph here or in Background: RAMA's multi-year authority-level achievement
  reports by cluster and the Knesset Research and Information Center's index analyses document the gradient;
  this analysis adds the residual layer and the group characterization.

**→ Report:** this step carries the report. Produce ⭐ **Fig 8** (the signature figure) and ⭐ **Table 7** (each
variable against the gap). Full ranked gaps for all authorities → appendix **A1**.

| Narrative cell | What this step supplies |
| --- | --- |
| Results (§7) | **The opening paragraph of the Results.** Name the authorities that over- and under-perform, how many clear the consistency bar out of 243, how large the typical deviation is in score points, and what Table 7 says distinguishes the two groups `[4]` |
| Discussion (§8) | What the characterization implies for the audience — where targeted intervention would be aimed, and what the over-performers might be doing that is worth studying. Immediately followed by the two limits: this is association, not cause `[2]`, and it is an authority-level statement, not a student-level one `[3]` |
| Background / Question (§1) | The literature paragraph (RAMA, Knesset Research and Information Center) and the one-sentence statement of what this adds beyond them `[4]` |

⚠️ The residual is only as trustworthy as the model it comes from. State in the Results which model the
residuals are taken from, and confirm the over/under-performer lists do not change materially if the residuals
come from the linear model instead, a one-line check that pre-empts the obvious Q&A question.

Step 8's outputs are **Fig 8** and **Table 7** in the §3.3 register, which was reconciled against the notebook.

**Prompt:**

> the main part, using the unweighted forest we chose. first get an honest gap for every authority:
> `cross_val_predict` with `GroupKFold` on rashut across all 243, so each authority is predicted by a model that
> never saw it. standardize the gaps within subject and grade before averaging, since the residual sd runs from 17 to
> 38 points depending on the test. average per authority and report the consistency of sign across its rows plus the
> standard error. only call an authority an over or under-performer if the gap is consistent and large next to that
> uncertainty, and skip the 5 authorities with a single row. most authorities appear in one year only, so consistency
> is across subjects and grades, not years. then plot the index against the mean standardized gap with the extremes
> labelled, correlate the gap against each of the cbs variables and against a few the model never saw (school count,
> school size, cohort size, response rate), and check the lists hold with the linear model's gaps.

**For the report:**

- The main question is not whether richer authorities score higher, which is already known, but which
  authorities do better or worse than their socio-economic level predicts.
- For each authority we averaged the gap between its actual and predicted scores. The gaps were first
  standardized within each subject and grade, because the size of a typical gap varies by test (a spread of 17
  points in Hebrew grade 5 against 38 in Science grade 8).
- Every authority's gap was taken from a model that had never seen that authority, so the gaps are comparable
  across all 243 rather than being smaller for the ones the model was trained on.
- We only treated an authority as an over- or under-performer when its gap was consistent across its subjects
  and grades and large compared with its own uncertainty, so that we are not reporting noise. Most authorities
  are tested in a single year, because the Meitzav rotates schools on a three-year cycle, so consistency could
  not be checked across years except for the 28 authorities that appear in more than one.
- `___` *(fill in after running: how many authorities out of 243 passed that test, which authorities are the
  clearest over- and under-performers, and how large the typical gap is in score points.)*
- `___` *(fill in after running: what distinguishes the two groups, i.e. which variables correlate with the gap.
  Include variables the model never used, since its own predictors cannot explain its residuals. This is the
  project's main finding, and a null result here is a legitimate one.)*
- `___` *(fill in after running: whether the lists stay the same when the gaps are taken from the other model.)*
- This association is not evidence of cause. It shows where the usual pattern does not hold, and those
  authorities are worth looking at more closely, but it does not tell us why.

#### Step 9 — Clustering `[Correction 4]`

Step 8 raised the stakes here. Its characterization table found **nothing**: none of 22 variables separates
over- from under-performers. Clustering is now the remaining chance to find structure among the 64 flagged
authorities, so this step is no longer a side exhibit.

- Build one row per authority: achievement profile across subject × grade, standardized.
- ⚠️ **The profile matrix is 69.5% full, and the holes are structural, not random.** Of 243 authorities only
  **10** have all 9 subject × grade combinations, and all 10 are mixed (`norm_id = 1`) cities. So the plan's
  earlier instruction to "restrict to authorities with a complete profile" is unusable: it would reduce the
  analysis to 10 authorities. The fill rates:

| Combination | Fill | | Combination | Fill |
| --- | --- | --- | --- | --- |
| English gr 8 | 94.7% | | Hebrew gr 5 | 65.0% |
| Math gr 8 | 93.8% | | Hebrew gr 8 | 60.1% |
| Science gr 8 | 92.6% | | Arabic gr 5 | 39.5% |
| Math gr 5 | 70.4% | | Arabic gr 8 | 39.5% |
| English gr 5 | 70.0% | | | |

- ⚠️ **Do not include Arabic or Hebrew in the profile.** Arabic is present for 100% of Arabic-language
  authorities and 0% of Hebrew-language ones; Hebrew is the mirror image. Including either column makes the
  distance matrix encode the sector, so K-Means would "discover" the Hebrew/Arabic split, which is already
  known from `norm_id` and is not a finding.
- ⚠️ **The tempting ">50% fill" core is a trap.** Taking the 7 combinations present for more than half of
  authorities (E5, E8, H5, H8, M5, M8, S8) leaves 105 authorities complete, of which **zero are
  Arabic-language** — Hebrew gr 5/8 silently removes all 84 of them. Any clustering built on it would describe
  Jewish authorities only while appearing to describe the country.
- **Use the sector-neutral grade-8 core: English, Math, Science grade 8.** 223 of 243 authorities are complete
  on it (19 mixed, 126 Hebrew-language, 78 Arabic-language), so coverage is near-full and all three sectors are
  represented. The wider sector-neutral set (adding English and Math grade 5) is defensible but drops to 160
  authorities, because grade 5 English and Math were not tested in 2018.
- ⚠️ **Standardize within each combination before clustering.** The three levels are English gr 8 ≈ 517,
  Math gr 8 ≈ 536, Science gr 8 ≈ 574, so unstandardized distances would be dominated by which test an
  authority happens to sit high on, exactly as in Steps 8 and 11.
- **Run it twice, on two different inputs, and say which answers which question:**
  - **On standardized scores** — this is the plan's original clustering. Expect it to partly recover sector and
    socio-economic level (on the neutral core, English gr 8 averages 529 in Hebrew-language authorities against
    496 in Arabic-language ones), so a cluster-to-cluster match is partly built in.
  - **On the Step 8 gaps** (`per_authority["gap"]` per combination) — these are already orthogonal to the index
    (r = 0.011) and net of subject and grade. Clustering them asks whether authorities deviate in *patterns*
    (strong in Math, weak in English) rather than uniformly. Given Step 8's null, this is the variant most
    likely to find something new.
- `KMeans`; choose *k* with the elbow method and silhouette score; report both plots. Try `k = 10` as well so
  the comparison with the official 1–10 clusters is direct, and note that the elbow-optimal *k* may differ.
- Optionally add a second algorithm (hierarchical / Ward, or a Gaussian Mixture) and compare — the rubric
  rewards a wider toolkit.
- **Compare data-driven clusters with the official CBS `CLUSTER`:** contingency / crosstab heatmap, Adjusted
  Rand Index, normalized mutual information, Spearman correlation between the achievement-cluster ordering and
  the SES cluster.
- Pull out the **mismatched authorities** (high achievement cluster, low SES cluster, and vice versa) and check
  the overlap against Step 8's concrete list: **64 flagged authorities, 33 over and 31 under**, named in
  `data/authority_gaps.xlsx`. Report the overlap as a count and a crosstab, not as an impression. Agreement
  between two independent methods is a strong result; disagreement is an honest and interesting finding. Either
  way, discuss it.
- ⚠️ Expect partial agreement by construction: Step 8's gaps correlate 0.75 with an authority's raw mean
  score, and the clustering input is built from those same scores. State that rather than presenting the overlap
  as independent confirmation.
- PCA (2 components) for a visual of the achievement space coloured by official CBS cluster.

**→ Report:** produce **Fig 9** (elbow + silhouette), ⭐ **Fig 10** (crosstab heatmaps), **Table 8** (ARI, NMI,
Spearman) and ⭐ **Fig 11** (gap-group profiles, uniform vs subject-specific).

| Narrative cell | What this step supplies |
| --- | --- |
| Methods (§2) | How the achievement profile was built, how missing subject × grade combinations were handled, how *k* was chosen, and which agreement metrics were used |
| Results (§7) | The instructor called this the most interesting part of the proposal, so it gets its own Results paragraph: how closely the two cluster systems agree (quote ARI/NMI), where they diverge, and **how many of Step 8's 64 flagged authorities fall in the mismatched set**. With Step 8's characterization null, this is the project's remaining chance to find structure, so report it either way |
| Discussion (§8) | What a persistent mismatch implies — the official cluster is not a sufficient summary of educational outcomes for those authorities |

**Prompt:**

> group the authorities by how they score, without using the socio-economic index, so we can compare our groups to
> the official ones. build one row per authority from grade 8 english, math and science only: those three are taught
> in both sectors and 223 of the 243 authorities have all three. don't use arabic or hebrew, since arabic only exists
> in arabic-language authorities and hebrew only in hebrew-language ones, so including either would just make the
> clusters rediscover the sector. standardize each of the three columns first, their levels are about 517, 536 and 574.
> run k-means, pick k with an elbow plot and silhouette, and also run k=10 to line up against the official 1 to 10
> clusters. compare the two with a crosstab heatmap, adjusted rand index and mutual information. then do the same
> clustering on the step 8 gaps instead of the raw scores, since those are already net of socio-economic level, and
> tell me which version separates the 64 flagged authorities better.

**For the report:**

- We also grouped authorities using only their achievement scores, without the socio-economic index, so that the
  grouping is independent of the official one.
- The profile had to be built carefully. Only 10 of the 243 authorities are tested in all nine subject and grade
  combinations, and Arabic is tested only in Arabic-language authorities while Hebrew is tested only in
  Hebrew-language ones. Including either subject would have made the groups reproduce the sector rather than
  describe achievement. We therefore used grade 8 English, Mathematics and Science, which are taught in both
  sectors and which 223 of the 243 authorities have in full, and standardized each before grouping.
- We chose the number of groups using an elbow plot and silhouette scores, and also ran it with 10 groups so it
  could be compared directly with the official 1–10 clusters.
- `___` *(fill in after running: how closely the two grouping systems agree, with the Adjusted Rand Index and
  mutual information values.)*
- `___` *(fill in after running: which authorities the two systems disagree about, and whether these are the same
  authorities found to over- or under-perform in the previous step. If the two methods agree, that is strong
  evidence; if they disagree, say so.)*
- Where the two systems disagree, the official socio-economic cluster is not a complete summary of how an
  authority's students actually perform.

#### Step 10 — Who sits in the tails (optional, but now has a specific question)

Step 9 turned this from a vague descriptive sweep into one concrete question. Six of the eight authorities
furthest *below* their official cluster are regional councils (Yo'av, Hagalil Haelyon, Matte Yehuda, Be'er
Tuveya, Hof Ashqelon, Sha'ar HaNegev), yet Table 7 found authority type almost unrelated to the gap on average.
Both are true, and the reconciliation is in the spread rather than the mean:

| Authority type | n | mean gap | SD of gap |
| --- | --- | --- | --- |
| City | 75 | +0.043 | 0.610 |
| Local council | 112 | +0.007 | 0.771 |
| Regional council | 51 | −0.087 | **0.821** |

- **The question:** regional councils are not worse on average, but are they more *variable*? Compare the
  spread of the gap by authority type, not just the mean. A plausible mechanism, worth stating as a hypothesis
  rather than a conclusion: a regional council averages several small separate communities under one
  administration, so its single figure hides more internal variation than a town's does.
- **Second question, from Fig 11:** do the subject-tilted gap groups concentrate anywhere? Group 4 (15
  authorities, strong in English and weak in Maths/Science) and group 5 (29 authorities, the reverse) are the
  new finding from Step 9. Crosstab them against sector and authority type. If the English-tilted group is
  mostly one sector, that is a concrete, policy-relevant result.
- A sorted bar chart or a small table is enough. **A map is not required** and is a time sink.
- ⚠️ District and peripherality are **not** in `t01_2017.xls` (§2.2), so a district breakdown needs a second CBS
  table. Skip it unless that table is already loaded; the two questions above use columns already in hand.

**→ Report:** still optional, but if done it earns a sentence in the Results and feeds the Discussion's
reconciliation of the Table 7 null with the Step 9 tails. If it is cut, cut it cleanly — do not leave an
unreferenced figure in the notebook.

**Prompt:**

> optional. compare the spread of the authority gaps by authority type, not just the mean: regional councils look
> no worse on average but their sd is 0.82 against 0.61 for cities, and most of the extreme under-performers are
> regional councils. then crosstab the two subject-tilted gap groups from fig 11 against sector and authority type
> to see if either concentrates anywhere. a small table or sorted bar chart is enough, no map.

**For the report:** *(only if this step is done, otherwise leave it out entirely)*

- `___` *(fill in after running: whether the gap is more variable for regional councils than for cities and local
  councils, and whether that explains their presence at both extremes while the averages stay flat.)*
- `___` *(fill in after running: whether the authorities tilted towards English, or away from it, concentrate in
  one sector or authority type.)*

#### Step 11 — Classification track `[Correction 5]`

- **Threshold rule — state it verbatim in the Methods narrative (notebook §2) and again above the code:**
  > A row is labelled **High** if its `score` is above the median `score` of its own
  > `(subject_id, shichva)` group, computed **on the training set only**, and **Low** otherwise.

  Equivalently (preferred, and worth implementing): z-score each `score` within its `(subject_id, shichva)`
  group using **training-set** means and standard deviations, then split at 0.
- Why: one overall median would mostly encode which subject and grade a row belongs to (subjects and grades sit
  at different score levels), so the classifier would learn the subject rather than anything about SES.
  Demonstrate this with a crosstab of the naive-median label against subject × grade — showing the problem is
  worth more than asserting it. Fig 1 already quantifies it: at one pooled median, 87% of Arabic grade 5 rows
  would be "high" against 18% of English grade 8 rows.
- **What counts as a good result here.** The regression reached test R² 0.530, i.e. about half the variation in
  an authority's score is predictable. A classifier on the same features should land somewhere near 70–80%
  accuracy against a 50% baseline; much higher would be a sign the label is leaking something. State the
  expectation before running so the result can be judged rather than just reported.
- ⚠️ Compute group medians / means **inside the training fold** and apply them to validation/test. Using the
  full-sample median leaks test information into the label definition.
- **Baseline (required):** majority-class predictor. With a within-group median the classes are ~50/50 by
  construction, so baseline accuracy is ~0.5. Say so, and note that this makes accuracy a weak metric on its
  own; report precision, recall, F1 and the confusion matrix alongside it.
- ⚠️ ROC-AUC was in an earlier draft of this plan and has been dropped, on the same grounds as Mann-Whitney:
  it was not covered in the course. Accuracy, precision, recall, F1 and the confusion matrix are enough, and if
  you do want AUC, the instructions allow uncovered methods only when the idea behind them is explained.
- **Model A — Logistic Regression** (standardized predictors, in a `Pipeline`).
- **Model B — RandomForestClassifier**, tuned with `GridSearchCV` + `GroupKFold`.
- Optionally a third (Gradient Boosting / HistGradientBoosting) for the breadth the rubric rewards.
- Reuse what Step 7 already built: the cluster-stratified `train_set` / `val_set` / `test_set`, the
  `make_pipeline()` helper (which already does median imputation, scaling and one-hot in the right order), the
  20-column `FEATURES` list, and `TUNING_CV` for the grid search. The test set is opened once, at the end.
- ⚠️ **No sample weighting.** Step 7 tested it and rejected it (forest R² 0.463 → 0.413, and worse on the
  weighted scoring too). Carrying it into the classifier would contradict our own result. Mention it was tried
  and dropped rather than silently omitting it.

**→ Report:** produce **Table 9** (majority baseline vs Logistic vs Random Forest: accuracy, precision,
recall, F1) and **Fig 12** (confusion matrix for the chosen model), plus the naive-median crosstab that
demonstrates *why* the within-group threshold is needed.

Numbering: the notebook has used Fig 1–11 and Tables 1, 4–8, so Step 11's outputs are **Table 9** and **Fig 12**.

| Narrative cell | What this step supplies |
| --- | --- |
| Methods (§2) | The threshold rule **quoted verbatim**, the statement that medians are computed on the training fold only, and the baseline definition. Correction 5 is judged on whether the rule is stated unambiguously — write the sentence, do not gesture at the code `[5]` |
| Results (§7) | Table 9 read against the ~0.5 baseline, with the note that accuracy is weak here by construction, so precision, recall and the confusion matrix carry the information `[7]` |
| Discussion (§8) | Whether binarizing cost anything relative to the regression — if the classifier adds no insight the regression did not already give, say so; that is a legitimate finding and better than overselling it |

**Prompt:**

> turn the score into a high/low label, worked out within each subject and grade: above its own group's median is
> high. one overall median would just encode which subject the row is, so the classifier would learn the subject
> instead of anything socio-economic. show a crosstab of that naive label against subject and grade to demonstrate
> it. compute the medians on the training set only, otherwise the label leaks. then train a logistic regression and a
> random forest, reusing the same split, features and `make_pipeline` helper from the regression, against a
> majority-class baseline. no sample weighting, we tested it earlier and it made things worse. give me accuracy,
> precision, recall, f1 and a confusion matrix.

**For the report:**

- We also treated the problem as classification, labelling each row "high" or "low" against the median score of
  its own subject and grade group, using medians calculated on the training data only.
- We did not use one overall median: because subjects and grades sit at different score levels, a single median
  would largely record which subject a row belongs to, and the model would learn the subject rather than anything
  about socio-economic status. `___` *(fill in after running: the crosstab showing this.)*
- Because the label splits each group at its own median, the classes are close to 50/50 and a majority-class
  baseline scores about 0.5. Accuracy alone is therefore a weak measure, so we also report precision, recall, F1
  and the confusion matrix.
- Weighting rows by the number of students tested was tested in the regression and made results worse, so it is
  not used here either.
- `___` *(fill in after running: results for the baseline, logistic regression and random forest, and which
  performed best.)*
- `___` *(fill in after running: whether the classification added anything the regression did not already show.)*

#### Step 12 — Feature importance `[Correction 6]` `[Correction 7]`

**Which models to read.** The two chosen models disagree about family, so take importance from both:
the **Random Forest regressor** from Step 7 (test R² 0.530) and the **logistic regression** from Step 11
(test accuracy 0.706). The linear regression is not the one to use for coefficients any more, because the
classifier that won was logistic.

- Random Forest `feature_importances_` **and** `permutation_importance` on the validation set. Impurity-based
  importance is biased toward continuous features with many distinct values, so report both and explain the
  difference.
- Standardized logistic coefficients as the second view, from the model that actually won Step 11.
- ⚠️ **Sum the one-hot dummies back to their original variable.** `subject_id`, `shichva`, `norm_id` and `year`
  enter the pipeline as separate dummy columns, so their importance arrives split across 5, 2, 3 and 3 columns
  respectively. Reporting dummy-level importance would make every categorical look weak purely because it was
  encoded. Add them up per original variable before ranking anything.
- ⚠️ **Per-variable permutation understates correlated predictors**, and Fig 5 showed `ses_index` correlating
  above 0.8 with eight of the CBS variables. Permuting one of them leaves the others carrying the same
  information, so each looks individually unimportant while the block as a whole matters. Per-variable
  importance therefore cannot answer the proposal's question on its own.
- **So add a block permutation.** Permute the whole 16-variable socio-economic block together (`ses_index`,
  `population` and the 14 CBS variables), then the 4 test-identity variables together (`subject_id`, `shichva`,
  `norm_id`, `year`), and compare the drop in R². That is the comparison the proposal actually asked for, and
  collinearity cannot distort it because correlated variables are permuted at the same time.
- **State the expectation before running.** Step 7's subject × grade baseline alone reached R² 0.297, against
  0.537 for the full out-of-fold model. So more than half the explained variance is already accounted for by
  *which test a row is*, and test identity will probably outweigh socio-economic standing. If so, say it
  plainly: the honest answer to the proposal's question is likely **no**, the index does not outweigh grade and
  subject, and that is a finding rather than a disappointment.
- Explicitly discuss the circularity flagged in §2.2 (the schooling-years and academic-degree variables feed
  the CBS index itself).

**→ Report:** produce ⭐ **Fig 13** (impurity-based vs permutation importance, side by side).

| Narrative cell | What this step supplies |
| --- | --- |
| Methods (§2) | Why two importance measures are reported rather than one, why dummies are summed back, and why a block permutation is needed on top of the per-variable one |
| Results (§7) | The direct answer to the question the proposal posed: does the socio-economic index outweigh grade, subject, sector and population? Quote the block permutation, since that is the version collinearity cannot distort, and name where the two per-variable measures disagree `[6]` |
| Discussion (§8) | The circularity caveat — schooling and degree variables are index inputs, so part of the importance ranking is structural rather than substantive; and the collinearity from Fig 5 means importance is shared across correlated predictors and should not be read as "this variable matters and that one doesn't" |

**Prompt:**

> show which variables matter most in the forest: built-in importance and permutation importance side by side,
> since the built-in one favours continuous variables. sum the one-hot dummies back per variable first. add the
> standardised logistic coefficients too. then permute the 16 socio-economic variables as one block against the 4
> test-identity ones, since they're too correlated to permute one at a time.

**For the report:**

- We measured variable importance two ways, the random forest's built-in importance and permutation importance,
  because the built-in measure tends to favour continuous variables with many values and the two can disagree.
  The categorical variables enter the model as separate dummy columns, so their importance was added back up per
  variable before ranking.
- Because the socio-economic variables are strongly correlated with each other (Fig 5), permuting them one at a
  time makes each look unimportant while the group still carries the information. We therefore also permuted the
  whole socio-economic block together and compared it against the four variables describing the test.
- `___` *(fill in after running: the ranking of variables, and which block matters more, socio-economic standing
  or which test the row is. Note the subject and grade baseline alone reached an R² of 0.297 out of the full
  model's 0.537, so test identity carrying more weight would be consistent with that.)*
- `___` *(fill in after running: where the two per-variable measures disagree.)*
- These numbers should be read with care. Several CBS variables are used to build the socio-economic index
  itself, so part of their importance reflects how the index is constructed rather than independent information.
- The predictors are also strongly correlated with each other, so importance is shared between them. A low score
  for one variable does not mean it is irrelevant.

#### Step 13 — Sensitivity / robustness summary

One compact table. Three of these are already computed earlier in the notebook, so this step mostly collects
them; four need a fresh run.

| Variation | Where it stands |
| --- | --- |
| Row-level split vs grouped split | **Done** (Step 6): 236 of 243 authorities land in two sets, and authority averages alone give R² 0.30 |
| Weighted vs unweighted by `n_students_tested` | **Done** (Step 7, Table 5): forest 0.463 → 0.413, linear 0.364 → 0.271 |
| Forest vs linear gaps for the 64 | **Done** (Step 8): Spearman 0.849, 98% keep their sign |
| Small-cell cutoff **30 vs 50** | ⚠️ Not 20/30/50: after the no-score rows are dropped, **0** rows fall under 20 and **2** under 30, so those cutoffs are no-ops. Only 50 bites, at 96 rows (5.5%) |
| Sector rows (`norm_id` 3, 9) vs authority totals (`norm_id` 1) | The Step 3 choice, never tested |
| Years 2016–2018 vs all of 2015–2019 | Untested |
| `ses_index` vs `ses_cluster` as the measure | Expect no change: Step 12 found `ses_index` has 15 near-substitutes |

**→ Report:** this is ⭐ **Table 11**, and it belongs in the Discussion, not the Results — it is the evidence that
the headline findings are not artefacts of arbitrary choices. The metric that matters is **whether the 64
over- and under-performers from Step 8 survive**, not just whether R² moves. Name the variation that moved the
results most, and report anything that did *not* survive as not surviving; that is the difference between a
sensitivity analysis and decoration.

**Prompt:**

> re-run the analysis under each of these and put it in one table: sector rows vs combined totals, 2015–2019 vs
> 2016–2018, small-cell cutoff 30 vs 50, and ses_index vs ses_cluster. the split, the weighting and the
> forest-vs-linear gap comparison are already computed earlier, so just collect those numbers into the same table.
> for each one give me the main metric and how many of the 64 over and under-performers change.

**For the report:**

- We re-ran the analysis under several different choices to check that the findings are not an artefact of
  decisions we made along the way: splitting by row rather than authority, with and without weighting, two
  small-cell cutoffs, sector rows versus combined totals, the continuous index versus the cluster, and the
  shorter versus longer year range.
- `___` *(fill in after running: which variation changed the results most, and how many of the 64 over- and
  under-performing authorities stayed on the list. Anything that did not hold up must be reported as not
  holding up.)*

### 3.4 Notebook requirements checklist

- [ ] Kernel → Restart & Run All completes with **no errors**
- [ ] Section order follows the §3.2 skeleton (Background/Question → Methods → data/EDA/modeling → Results → Discussion)
- [ ] Markdown headers for every section; a short *what and why* cell above every non-trivial code step
- [ ] Report-level cells and step-level cells visually distinct and never blended (§3 rule)
- [ ] Abandoned attempts and debug output removed — final version only
- [ ] Every figure and table referenced in the report prose is produced by a cell in the same notebook
- [ ] **Register reconciled both ways:** every ID in the §3.3 register exists in the notebook with that caption,
      and every figure in the notebook appears in the register — no orphan figures, no promised-but-missing ones
- [ ] All seven ⭐ headline items are actually discussed in the Results or Discussion prose, not merely plotted
- [ ] `RANDOM_STATE` set once and reused; results reproducible on re-run
- [ ] No test-set usage before the final evaluation; no label or scaler leakage across folds
- [ ] A package-version cell at the top (`xlrd` is needed for the legacy `.xls`)
- [ ] **After the final Restart & Run All:** re-read the Results and Discussion cells and confirm every number
      quoted in the prose still matches the printed output above it

### 3.5 Submission — keeping one file genuinely self-contained

The notebook holds the whole report, but it cannot hold `performances_by_areas_years_2015_2019.csv` and
`t01_2017.xls`. Pick one route and state it in a markdown cell at the top of §3 of the notebook:

| Route | What to do | Trade-off |
| --- | --- | --- |
| **A — zip with the data** (recommended) | Submit `.ipynb` + `datasets/` in one zip; load with relative paths (`datasets/…`) | Not literally one file, but explicitly allowed, and it always runs. The notebook is still the only document |
| **B — download in-notebook** | First code cell fetches both files from the official gov.il / CBS URLs into `datasets/`, with a relative-path fallback if they already exist | Truly one file, but breaks without internet or if either URL moves — and CBS does move files between editions |
| **C — embed the data** | Base64-embed both files in a code cell that writes them to disk | Truly one file and offline-safe, but bloats the notebook and makes it unpleasant to read |

Route A is the recommended default: the instructions explicitly permit a zip, and the thing being graded —
one document containing report and code — is unchanged. If you want to avoid the zip entirely, Route B with a
local fallback is the next best, and its fallback means it still runs for a grader who has the folder.

**Final checklist:**

- [ ] All five report sections + AI usage statement present as markdown cells (§3.2 skeleton)
- [ ] Notebook runs top-to-bottom with no errors from a fresh kernel
- [ ] Notebook organized and commented per §3.4
- [ ] Figures legible, numbered, captioned, and referenced from the Results narrative
- [ ] Data route (A/B/C) chosen, implemented, and stated in the notebook
- [ ] Verified by re-running from a **clean copy of the submission** (unzip elsewhere, Restart & Run All) —
      catches absolute paths and files that only exist on your machine
- [ ] All nine corrections visibly addressed — §0 tracker fully ticked

---

## 4. Final Presentation (40%)

Formal slide deck, up to 10 minutes inside a 30-minute slot, ~8–10 slides. Submitted before the assigned slot.

| # | Slide | Content |
| --- | --- | --- |
| 1 | Title | Project title, both names, course |
| 2 | Motivation & audience | Authority-level achievement gaps; Ministry of Education / RAMA / municipal leadership; what decision this informs |
| 3 | Question | The three-level hierarchy, with the **deviation question first**. Non-causal wording throughout `[2]` `[4]` |
| 4 | Data | Two official sources; 2016–2018 × the 2017 index with the alignment rationale `[8]`; the authority-ID join and the `norm_id` double-counting fix — a 30-second "real data work" slide |
| 5 | Methods | One diagram: grouped split → baselines → regression + classification → residuals → clustering. Name the grouped split explicitly `[1]` `[7]` |
| 6 | Key result 1 | **Fig 8**, the gap against the socio-economic index with the extremes labelled (Step 8) |
| 7 | Key result 2 | **Fig 10** (groups vs official clusters) + **Fig 11** (subject-specific deviation), the two Step 9 findings (Steps 8–9) |
| 8 | Conclusions | What the findings support for the stated audience, stated as association |
| 9 | Limitations | **Ecological fallacy by name** `[3]`; no causal claim `[2]`; aggregation; unmeasured confounders; honest statement of what the grouped split cost in measured performance |
| 10 | Backup | **Table 11** (sensitivity), **Fig 13** (feature importance), **A1** ranked gaps, **A3** hyperparameter grids |

### 4.1 Presentation checklist

- [ ] Covers motivation, question, dataset/methods, key results, conclusions/limitations
- [ ] Rehearsed to fit in 10 minutes
- [ ] Figures readable at presentation size — regenerate at presentation resolution, do not shrink notebook PNGs
- [ ] Submitted before the assigned slot
- [ ] **Both partners can explain every choice** — this component is 40% and is graded primarily on demonstrated understanding

---

## 5. Using AI — required statement `[Correction 9]`

Not required at the proposal stage; **required in the final report**, which here means a markdown cell at
**notebook §9**. Keep a running log from now on — it cannot be reconstructed later.

The statement must cover:

1. **Which tools** — e.g. Claude (Claude Code), ChatGPT; name them and note roughly when and for what.
2. **What they were used for** — e.g. debugging a merge, drafting report prose, suggesting a method, explaining
   a scikit-learn API, planning the project structure (including this document).
3. **The prompts used** — actual prompt text. Long prompt logs go in notebook §10 (appendix); the §9 statement
   summarizes and points to it.

**The prompt log is already mostly written.** Each step in §3.3 carries a **Prompt** block; those are the prompts
for implementing the analysis, and they go into the log as-is — *provided you submit the version you actually
used*, including any edits made while working. What still has to be added by hand:

- Prompts used for things outside the pipeline — debugging an error, asking how a scikit-learn function works,
  drafting or tightening report prose, planning the project (this document included).
- Which tool answered each one, if more than one was used.
- Anything an AI tool wrote that ended up in the notebook unchanged.

Code or text that is clearly not the authors' own and is unaccompanied by prompt information is treated as
cheating. Everything submitted must be understood well enough to walk through on request. **Action: start
`helper docs/AI_USAGE_LOG.md` now and append every prompt as it happens.**

---

## 6. General Requirements

- [ ] **Pairs** — Stav + Or ✅
- [ ] **Be concise** — only what is needed to understand what was done and why; no padding in the report
- [ ] **Own code** — do not copy published analyses of these datasets. The residual/deviation framing and the
      achievement-cluster vs CBS-cluster comparison are the differentiators `[Correction 4]`
- [ ] **Complexity affects the score** — overly simple projects are marked down regardless of correctness. This
      plan clears that bar: two tracks (regression + classification), two models per track plus baselines,
      clustering, residual analysis, feature importance, and a sensitivity study
- [ ] **A wider toolkit is rewarded** — the clustering layer, the multi-model comparison, and the permutation
      importance are each explicitly named in the rubric as rewarded behaviours

---

## 7. Grading Rubric — self-audit before submission

| Component | Sub-criterion | Weight | How this plan earns it |
| --- | --- | --- | --- |
| Proposal | Question clarity | 8% | ✅ Locked (40/40) |
| Proposal | Dataset description | 6% | ✅ Locked (27/30) |
| Proposal | Soundness of methods | 6% | ✅ Locked (25/30) |
| Report + Notebook | **Project design** (variety/appropriateness of tools) | 8% | Two supervised tracks + baselines + clustering + residual analysis + feature importance + sensitivity study |
| Report + Notebook | **Notebook organization** | 8% | §3.2 skeleton; *what and why* cell above every code step; Restart & Run All clean; §3.4 checklist |
| Report + Notebook | **Report readability** | 8% | §3.1 writing brief; report-level cells kept separate from step-level cells (§3 rule) so the prose reads as one 3–5 page report; numbered figures; large tables in §10 |
| Report + Notebook | **Discussion & interpretation** | **16%** | The largest single report item. Ecological fallacy `[3]`, causality `[2]`, honest grouped-split cost `[1]`, differentiation from the RAMA / Knesset literature `[4]`, limitations and next steps |
| Presentation | Understanding of own work | **16%** | Both partners rehearse Appendix A |
| Presentation | Clarity of explanation | 8% | Slide flow question → method → result → conclusion |
| Presentation | Quality of responses | **16%** | Appendix A below |

**Highest-leverage items:** Discussion & interpretation (16%) and the two 16% presentation items. Together they
are 48% of the project grade, and all three reward the same thing — understanding and honesty about limitations
rather than impressive numbers.

---

## Appendix A — Q&A preparation

Graded on: understanding of own work (16), clarity (8), quality of responses (16). Short direct answers are
fine; qualitative reasoning is acceptable; an honest "I don't know" on a genuinely advanced point is not
penalized. Nervousness and delivery style are not graded. Each partner should be able to answer all of these.

**Expected questions, straight out of the feedback:**

1. Why a grouped split, and what did it cost you? → Rows are authority × grade × subject × year from ~250
   authorities, so they are not independent; a row split leaks authority means into the test set. Quote the
   before/after metrics from Step 6.
2. What is the ecological fallacy and where does it bite your conclusions? → The paragraph from §3.1(c), plus
   the concrete implication: the findings support decisions about authorities, not claims about students.
3. Why can't you say the socio-economic index *causes* lower achievement? → Observational, cross-sectional,
   confounded; name a plausible confounder (sector/composition, geography, school-level resourcing).
4. What does your project add over RAMA's published cluster reports? → The residual layer and the
   over/under-performer characterization; the achievement-cluster vs CBS-cluster comparison.
5. Exactly how is the classification label defined, and why not a single median? → The verbatim rule from
   Step 11, plus the crosstab showing a pooled median mostly encodes subject and grade.
6. Why `INDEX VALUE` here and `CLUSTER` there? → Two encodings of one measurement; continuous for modeling,
   categorical for grouping and for the cluster comparison; never both in one model.
7. Why weight by `n_students_tested`? What changed? → Cell sizes run from 1 to 1,357; small cells are noisy;
   quote the weighted/unweighted rows of the Step 13 table.
8. Why 2016–2018 and not all five years? → The index edition is 2017; this centres the panel on it. Quote the
   last row of the Step 13 table for what happens with all five years.
9. How did you join two files with different authority codes? → The two-rule mapping in Step 4a plus four manual
   overrides, verified by name match and a 100%-coverage assertion.
10. What would you do differently / what remains unknown? → Student- or school-level data to escape the
    ecological fallacy; a true multi-year panel with authority fixed effects; district/peripherality and
    school-resourcing covariates; a design that could support causal claims.

---

## Appendix B — Verified data facts (from inspecting the files)

Everything below was confirmed directly against the two files in `datasets/` and should be reused rather than
re-derived.

**Education file** (`performances_by_areas_years_2015_2019.csv`): 3,067 × 12. Columns: `year`, `rashut`,
`rashut_teur`, `norm_id`, `shichva`, `subject_id`, `score`, `n_students_tested`, `n_schools_tested`,
`n_students`, `n_schools`, `p_response`. Years 2015–2019 (row counts 734 / 813 / 752 / 522 / 246 — note 2018
and 2019 are thinner). 251 authorities; 250 in 2016–2018 with 2,087 rows. Grades 5 and 8. Subjects A/E/H/M/S.
`score` 396–695, mean 545.9, sd 39.0, **142 nulls**. `n_students_tested` 1–1,357, median 242; 80 rows < 30 and
221 rows < 50. `p_response` min 1, median 90. `n_students` has 9 nulls. Unique on
`(year, rashut, norm_id, shichva, subject_id)`; **416 duplicates** on the same key without `norm_id`.

**`norm_id` is sector / language of instruction:** 3 = Hebrew-language (167 authorities), 9 = Arabic-language
(99 authorities), 1 = authority-wide total for the **19 mixed authorities**. For mixed authorities the
`norm_id = 1` row is the sum of the 3 and 9 rows — verified on Haifa (2015, grade 5, English: 664 = 537 + 127).
Keeping all three values double-counts the largest cities. Subject coverage differs by sector: A appears under
`norm_id` 1 and 9 only; H under 1 and 3 only.

**CBS file** (`t01_2017.xls`, sheet `t01`): 271 × 50. Metadata/header rows 0–9 (bilingual, three header rows
deep), data from row 10, 5 footnote rows at the end. Rows 8–9 are the national AVERAGE and NATIONWIDE VALUE
rows — exclude them. **255 authorities**: 201 with a numeric `CODE OF LOCALITY`, 54 regional councils with a
blank code whose council number sits in `MUNICIPAL STATUS`. `MUNICIPAL STATUS`: 0 = municipality, 99 = local
council, any other value = regional council number. `CLUSTER` 1–10, `RANK` 1–255, `INDEX VALUE` standardized
to mean 0 in sd units. 14 component variables, each as a (value, standardized value, rank) triple. `DISTRICT`
and `PERIPHERALITY INDEX` are **not** in this table.

**Join rule (verified):** `rashut // 10` → `CODE OF LOCALITY` matches 193/197 localities; `rashut // 100000` →
`MUNICIPAL STATUS` matches 54/54 regional councils; four merged municipalities need manual overrides
(13508 → 195, 13516 → 1200, 13524 → 9800, 13573 → 9400). Three name normalizations are needed for name-based
verification: מג'אר / מגאר, נוף הגליל / נצרת עילית, ערערה בנגב / ערערה-בנגב. The example from the proposal is
confirmed: Ofakim = `315` in education, `31` in CBS.

**Environment note:** `xlrd` is required for the legacy `.xls` file, and `pypdf` was installed to read the
project PDFs — both were added to `.venv` during planning.
