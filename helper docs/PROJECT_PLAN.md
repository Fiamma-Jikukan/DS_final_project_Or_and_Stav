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
| 6 | Expand predictor set from CBS; pick **one** of CLUSTER / INDEX VALUE per use | §3.3 Steps 3–4 | ☐ |
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
| 1 | Both | Load + clean both files, resolve the authority-ID join, lock the analysis table (§3.3 Steps 1–4) |
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

Plus derived predictors from the education file itself: `norm_id` (sector / language of instruction),
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
| **Results** | §7, after the modeling code, as a single narrative cell that refers back to the figures above it | Lead with the deviation / over- and under-performer findings; the SES gradient is presented as a validated calibration step, not the punchline. Built around the five ⭐ headline items in the §3.3 register (Fig 7, Fig 9, Fig 12, Table 6, Table 9), referring to each by its register ID. Oversized tables (full authority residual ranking A1, hyperparameter grids A2) are rendered in the §10 appendix, not here | `[4]` |
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
| **§3 Data loading & preparation** | MD + code | Setup, load both files, year restriction, `norm_id` fix, the join, with verification output | Steps 1–4 |
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

| ID | Content | Produced by | Consumed by |
| --- | --- | --- | --- |
| Table 1 | Dataset summary — both sources, rows, columns, grain, coverage | Step 1 | Methods (§2) |
| Table 2 | Row/authority counts after each cleaning decision (years, `norm_id` grain, small cells, missing target) | Steps 2, 3, 5 | Methods (§2) |
| Table 3 | Join coverage and verification — matched by rule, by override, unmatched, CBS authorities with no education data | Step 4 | Methods (§2) |
| Fig 1 | `score` distribution overall and by subject × grade | Step 5 | Methods (§2) — justifies the Correction 5 threshold rule |
| Fig 2 | `score` vs `n_students_tested` variance funnel | Step 5 | Methods (§2) — justifies small-cell exclusion + weighting |
| Fig 3 | `score` by CBS `CLUSTER`, faceted by subject × grade | Step 5 | Results (§7) — the known gradient, as calibration |
| Fig 4 | `score` vs `INDEX VALUE` scatter, one panel per subject × grade | Step 5 | Results (§7) |
| Fig 5 | Correlation heatmap of CBS predictors | Step 5 | Discussion (§8) — collinearity / circularity caveat |
| Table 4 | Split sizes in **both** rows and authorities, with the zero-overlap assertion | Step 6 | Methods (§2) |
| Table 5 | Regression results: both baselines vs Linear vs Random Forest, weighted and unweighted | Step 7 | Results (§7) |
| Fig 6 | Residual diagnostics (residuals vs fitted, vs `INDEX VALUE`, by sector) | Step 7 | Discussion (§8) — model adequacy |
| ⭐ Fig 7 | **Signature figure:** `INDEX VALUE` vs mean score, fitted line, extreme over/under-performers labelled | Step 8 | Results (§7) — the lead result |
| ⭐ Table 6 | **Over- vs under-performer characterization** across the expanded CBS variables, with tests | Step 8 | Results (§7) + Discussion (§8) — the project's contribution |
| Fig 8 | Elbow + silhouette for *k* | Step 9 | Methods (§2) |
| ⭐ Fig 9 | Data-driven achievement clusters vs official CBS `CLUSTER` — crosstab heatmap | Step 9 | Results (§7) |
| Table 7 | Cluster agreement metrics (ARI, NMI, Spearman) + the mismatched authorities | Step 9 | Results (§7) |
| Fig 10 | PCA of the achievement space, coloured by official CBS cluster | Step 9 | Results (§7), supporting |
| Table 8 | Classification results: majority baseline vs Logistic vs Random Forest (accuracy, ROC-AUC, precision/recall, F1) | Step 11 | Results (§7) |
| Fig 11 | ROC curves + confusion matrix for the chosen classifier | Step 11 | Results (§7), supporting |
| ⭐ Fig 12 | Feature importance: impurity-based vs permutation, side by side | Step 12 | Results (§7) + Discussion (§8) |
| ⭐ Table 9 | Sensitivity / robustness summary | Step 13 | Discussion (§8) |
| A1–A4 | Appendix: full authority residual ranking, hyperparameter grids, full correlation matrix, prompt log | Steps 8, 7/11, 5, §5 | Notebook §10 |

That is 5 headline items (Fig 7, Fig 9, Fig 12, Table 6, Table 9) — the set the Results and Discussion
narrative is built around, and the same set the slide deck draws on (§4).

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
> and english — real data starts at row 10, the last 5 rows are footnotes, and two rows near the top are national
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
> average score moves much between the three years — if it does we should keep year as a variable later.

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

Pick **one** grain and state it in the report:

- **Option A (recommended): sector-level rows only** — drop `norm_id = 1`, keep 3 and 9, and use `norm_id` as a
  predictor. Richer, keeps the Hebrew/Arabic education distinction (a strong and policy-relevant signal), and
  gives a within-authority contrast for mixed cities. Requires the grouped split to group on `rashut` so a
  mixed city's two sector rows cannot straddle train and test.
- **Option B: authority totals only** — use `norm_id = 1` where it exists, otherwise the single sector row.
  Simpler, one row per authority × year × grade × subject, but throws away the sector signal.

Whichever is chosen, **never keep both** — it double-counts the largest cities and silently weights them twice.

**→ Report:** second row of **Table 2**, plus the verification number that proves the aggregation (the Haifa
check, or the equivalent on your chosen cell). The Methods narrative gets a short paragraph: what `norm_id`
encodes, that the file mixes totals with parts, which grain was kept and why. This is not in the proposal or
the feedback, so it reads as independent data work — worth stating plainly rather than burying in a comment.
If Option A is chosen, the Discussion notes that mixed authorities contribute two sector rows, which the
grouped split keeps on the same side of the split.

**Prompt:**

> `norm_id` is the education sector: 3 is hebrew-language schools, 9 is arabic-language, and 1 is both added together
> for mixed cities. so mixed cities get counted twice — haifa's grade 5 english total of 664 students tested is just
> 537 + 127 from the two sectors. check that on a couple of authorities, then drop the `norm_id = 1` rows so each row
> is one sector and we can use sector as a variable. print rows and authorities left.

**For the report:**

- The column `norm_id` marks the education sector: Hebrew-language, Arabic-language, or a combined total for
  authorities that have both.
- For mixed authorities the file contains both the total and the two sector rows, so those authorities appear
  twice. We confirmed this: Haifa's grade 5 English total of 664 tested students equals the 537 and 127 of its
  two sectors added together.
- Keeping both would count the largest cities twice and give them double weight. We therefore kept only the
  sector rows and dropped the totals, which also lets us use the sector as a variable in the models.
- `___` *(fill in after running: rows and authorities remaining after dropping the total rows.)*

#### Step 4 — Join the two datasets `[Correction 6]`

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
> vs 31). regional councils have no locality code in the cbs file — their council number is in the municipal status
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
> how many rows have under 20, 30 and 50 — small cells are noisy. check whether the rows with no score are mostly
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

- The 2,087 rows come from only ~250 authorities, so rows are **not independent**. A row-level random split
  would put the same authority in train and test; the model would memorize authority means and the reported
  accuracy would be inflated.
- Use `rashut` as the group:
  - `GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=RANDOM_STATE)` → hold out test (30%).
  - Apply `GroupShuffleSplit` again on the remaining 70% to carve out validation (20% of total ⇒
    `test_size = 0.2/0.7 ≈ 0.2857`), leaving ≈50% train — preserving the proposal's 50/30/20 intent at the
    authority level.
  - Use `GroupKFold(n_splits=5)` inside `GridSearchCV` / `RandomizedSearchCV` (`cv=GroupKFold(5)`,
    `groups=rashut`) for all hyperparameter tuning.
- **Assert zero authority overlap** between the three sets, and print set sizes in both rows and authorities.
- **Report both numbers side by side:** metrics under a naive row-level split vs the grouped split. The drop is
  the evidence that the correction was understood. The instructor said it outright: "the results may become
  worse after doing this, and that is exactly the point."

**→ Report:** produce **Table 4** (split sizes in rows *and* authorities, plus the printed zero-overlap
assertion). The Methods narrative must name `GroupShuffleSplit` / `GroupKFold` with `rashut` as the group and
explain in two or three sentences *why* rows are not independent — this is the most heavily weighted single
correction, so it needs prose, not just a function call. The row-level-vs-grouped comparison goes into
**Table 9** (Step 13) and is quoted in the Discussion as an honesty point: state the inflated number, the honest
number, and that the honest one is the one being reported `[1]`.

**Prompt:**

> split into train, validation and test by authority, not by row. our 2,087 rows come from only ~250 authorities, so
> if the same authority lands in both train and test the model can memorise its average score and accuracy looks
> better than it is. use `GroupShuffleSplit` with authority as the group, roughly 50/30/20, and `GroupKFold` by
> authority for tuning later. fail if an authority appears in two sets, and print each set size in rows and
> authorities. also run it once with a plain random row split so we can show the difference.

**For the report:**

- Our rows are not independent: 2,087 rows come from only about 250 local authorities, so each authority appears
  many times.
- A random split by row would put the same authority in both the training and test sets. The model could then
  memorise that authority's average score, and the accuracy we report would be too optimistic.
- We therefore split by authority using `GroupShuffleSplit`, about 50% training, 30% test and 20% validation,
  and used `GroupKFold` by authority for tuning. We checked that no authority appears in two sets.
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

- Fit the SES-only (or SES + structural controls) model and compute each authority's **residual**: observed
  score minus predicted score. Aggregate residuals **per authority** across subjects, grades, and the three
  years (mean residual, weighted by `n_students_tested`; also report the standard error / consistency of each
  authority's residual).
- Rank authorities. Produce the signature figure: `INDEX VALUE` on x, mean score on y, regression line, with
  the most extreme positive and negative residual authorities labelled.
- **Separate signal from noise:** an authority counts as an over/under-performer only if its residual is
  consistent across subjects, grades, and years, and large relative to its own uncertainty. Report how many
  authorities pass that bar. This is what makes the finding defensible under Q&A.
- **Characterize the two groups:** compare over-performers vs under-performers on the expanded CBS variables
  (population, median age, dependency ratio, % 4+ children, income, sector, municipal status, and
  district/peripherality if added). Use t-tests / Mann-Whitney with a note on multiple comparisons, plus a
  compact comparison table. *This table is the project's actual contribution.*
- Add the short literature paragraph here or in Background: RAMA's multi-year authority-level achievement
  reports by cluster and the Knesset Research and Information Center's index analyses document the gradient;
  this analysis adds the residual layer and the group characterization.

**→ Report:** this step carries the report. Produce ⭐ **Fig 7** (the signature figure) and ⭐ **Table 6** (the
over- vs under-performer characterization). Full ranked residual table for all authorities → appendix **A1**.

| Narrative cell | What this step supplies |
| --- | --- |
| Results (§7) | **The opening paragraph of the Results.** Name the authorities that over- and under-perform, how many clear the consistency bar out of ~250, how large the typical deviation is in score points, and what Table 6 says distinguishes the two groups `[4]` |
| Discussion (§8) | What the characterization implies for the audience — where targeted intervention would be aimed, and what the over-performers might be doing that is worth studying. Immediately followed by the two limits: this is association, not cause `[2]`, and it is an authority-level statement, not a student-level one `[3]` |
| Background / Question (§1) | The literature paragraph (RAMA, Knesset Research and Information Center) and the one-sentence statement of what this adds beyond them `[4]` |

⚠️ The residual is only as trustworthy as the model it comes from. State in the Results which model Fig 7's
residuals are taken from, and confirm the over/under-performer lists do not change materially if the residuals
come from the other model — a one-line check that pre-empts the obvious Q&A question.

**Prompt:**

> main part. for each row, get the gap between the actual score and what the model predicted from the authority's
> socio-economic profile. average that per authority across subjects, grades and years, weighted by students tested.
> also measure how consistent each gap is — only count an authority as an over or under-performer if the gap holds
> across subjects and years and is large next to its own uncertainty, and tell me how many pass. then the main figure:
> index on x, average score on y, fitted line, extreme authorities labelled. finally compare over- and under-performers
> across the cbs variables with a test for each, and check whether the lists change using gaps from the other model.

**For the report:**

- The main question is not whether richer authorities score higher, which is already known, but which
  authorities do better or worse than their socio-economic level predicts.
- For each authority we averaged the gap between its actual and predicted scores across all subjects, grades and
  years, weighted by the number of students tested.
- We only treated an authority as an over- or under-performer when its gap was consistent across subjects,
  grades and years and large compared with its own uncertainty, so that we are not reporting noise.
- `___` *(fill in after running: how many authorities out of ~250 passed that test, which authorities are the
  clearest over- and under-performers, and how large the typical gap is in score points.)*
- `___` *(fill in after running: what distinguishes the two groups — which CBS variables differ significantly
  between over- and under-performers. This is the project's main finding.)*
- `___` *(fill in after running: whether the lists stay the same when the gaps are taken from the other model.)*
- This association is not evidence of cause. It shows where the usual pattern does not hold, and those
  authorities are worth looking at more closely, but it does not tell us why.

#### Step 9 — Clustering `[Correction 4]`

- Build one row per authority: achievement profile across subject × grade (mean score per combination over
  2016–2018), standardized.
- Handle authorities with missing subject × grade combinations explicitly (restrict to authorities with a
  complete profile for the core combinations, or impute and say so). Note that subject coverage differs by
  sector — Arabic (A) is absent from `norm_id = 3` and Hebrew (H) from `norm_id = 9` — so the profile must be
  built on comparable columns.
- `KMeans`; choose *k* with the elbow method and silhouette score; report both plots. Try `k = 10` as well so
  the comparison with the official 1–10 clusters is direct, and note that the elbow-optimal *k* may differ.
- Optionally add a second algorithm (hierarchical / Ward, or a Gaussian Mixture) and compare — the rubric
  rewards a wider toolkit.
- **Compare data-driven clusters with the official CBS `CLUSTER`:** contingency / crosstab heatmap, Adjusted
  Rand Index, normalized mutual information, Spearman correlation between the achievement-cluster ordering and
  the SES cluster.
- Pull out the **mismatched authorities** — high achievement cluster, low SES cluster, and vice versa — and
  check whether they overlap with the Step 8 residual extremes. Agreement between two independent methods is a
  strong result; disagreement is an honest and interesting finding. Either way, discuss it.
- PCA (2 components) for a visual of the achievement space coloured by official CBS cluster.

**→ Report:** produce **Fig 8** (elbow + silhouette), ⭐ **Fig 9** (crosstab heatmap, achievement clusters vs
official CBS clusters), **Table 7** (ARI, NMI, Spearman + the list of mismatched authorities), and **Fig 10**
(PCA, supporting).

| Narrative cell | What this step supplies |
| --- | --- |
| Methods (§2) | How the achievement profile was built, how missing subject × grade combinations were handled, how *k* was chosen, and which agreement metrics were used |
| Results (§7) | The instructor called this the most interesting part of the proposal, so it gets its own Results paragraph: how closely the two cluster systems agree (quote ARI/NMI), where they diverge, and **whether the mismatched authorities are the same ones Step 8 flagged**. Two independent methods agreeing is the strongest claim this project can make; if they disagree, say so and say what that means |
| Discussion (§8) | What a persistent mismatch implies — the official cluster is not a sufficient summary of educational outcomes for those authorities |

**Prompt:**

> group the authorities by how they score, without the socio-economic index, so we can compare our groups to the
> official ones. one row per authority with its average score per subject and grade over 2016–2018, standardised. note
> the subjects differ by sector — arabic isn't tested in hebrew-language schools and vice versa — so only use comparable
> columns and tell me what you did about missing combinations. run k-means, pick k with an elbow plot and silhouette,
> and also run k=10 to line up against the official 1–10 clusters. compare the two with a crosstab heatmap, adjusted
> rand index and mutual information, list the authorities they disagree about, and check whether those are the same
> ones flagged as over/under-performers.

**For the report:**

- We also grouped authorities using only their achievement scores, without the socio-economic index, so that the
  grouping is independent of the official one.
- We chose the number of groups using an elbow plot and silhouette scores, and also ran it with 10 groups so it
  could be compared directly with the official 1–10 clusters.
- `___` *(fill in after running: how closely the two grouping systems agree, with the Adjusted Rand Index and
  mutual information values.)*
- `___` *(fill in after running: which authorities the two systems disagree about, and whether these are the same
  authorities found to over- or under-perform in the previous step. If the two methods agree, that is strong
  evidence; if they disagree, say so.)*
- Where the two systems disagree, the official socio-economic cluster is not a complete summary of how an
  authority's students actually perform.

#### Step 10 — Geographic / descriptive layer (optional, if time allows)

- Table or simple chart of over/under-performers by district or sector. A map is not required and is a time
  sink; a sorted bar chart communicates the same thing.

**→ Report:** optional, so it earns at most one clause in the Results and one row in **Table 6**. If it is cut,
cut it cleanly — do not leave an unreferenced figure in the notebook. If district/peripherality were added per
§2.2, this is where they pay off and the Results should say so.

**Prompt:**

> optional: sorted bar chart of the over and under-performers by district or sector, to see whether they cluster
> anywhere. no map needed.

**For the report:** *(only if this step is done — otherwise leave it out entirely)*

- `___` *(fill in after running: whether the over- and under-performers are concentrated in particular districts
  or sectors, or spread out.)*

#### Step 11 — Classification track `[Correction 5]`

- **Threshold rule — state it verbatim in the Methods narrative (notebook §2) and again above the code:**
  > A row is labelled **High** if its `score` is above the median `score` of its own
  > `(subject_id, shichva)` group, computed **on the training set only**, and **Low** otherwise.

  Equivalently (preferred, and worth implementing): z-score each `score` within its `(subject_id, shichva)`
  group using **training-set** means and standard deviations, then split at 0.
- Why: one overall median would mostly encode which subject and grade a row belongs to (subjects and grades sit
  at different score levels), so the classifier would learn the subject rather than anything about SES.
  Demonstrate this with a crosstab of the naive-median label against subject × grade — showing the problem is
  worth more than asserting it.
- ⚠️ Compute group medians / means **inside the training fold** and apply them to validation/test. Using the
  full-sample median leaks test information into the label definition.
- **Baseline (required):** majority-class predictor. With a within-group median the classes are ~50/50 by
  construction, so baseline accuracy is ~0.5 — say so, and note that this makes accuracy a weak metric; report
  ROC-AUC, precision/recall, F1, and the confusion matrix too.
- **Model A — Logistic Regression** (standardized predictors, in a `Pipeline`).
- **Model B — RandomForestClassifier**, tuned with `GridSearchCV` + `GroupKFold`.
- Optionally a third (Gradient Boosting / HistGradientBoosting) for the breadth the rubric rewards.
- Same grouped split, same sample weights, same single use of the test set.

**→ Report:** produce **Table 8** (majority baseline vs Logistic vs Random Forest — accuracy, ROC-AUC,
precision, recall, F1) and **Fig 11** (ROC curves + confusion matrix for the chosen model), plus the
naive-median crosstab that demonstrates *why* the within-group threshold is needed.

| Narrative cell | What this step supplies |
| --- | --- |
| Methods (§2) | The threshold rule **quoted verbatim**, the statement that medians are computed on the training fold only, and the baseline definition. Correction 5 is judged on whether the rule is stated unambiguously — write the sentence, do not gesture at the code `[5]` |
| Results (§7) | Table 8 read against the ~0.5 baseline, with the note that accuracy is weak here by construction and ROC-AUC is the metric to read `[7]` |
| Discussion (§8) | Whether binarizing cost anything relative to the regression — if the classifier adds no insight the regression did not already give, say so; that is a legitimate finding and better than overselling it |

**Prompt:**

> turn the score into a high/low label, worked out within each subject and grade — above its own group's median is high.
> one overall median would just encode which subject the row is, so the classifier would learn the subject instead of
> anything socio-economic. show a crosstab of that naive label against subject and grade to demonstrate it. compute the
> medians on training data only, otherwise the label leaks. then train a logistic regression and a random forest on the
> same grouped split against a majority-class baseline, and give me accuracy, roc-auc, precision, recall, f1 and a
> confusion matrix.

**For the report:**

- We also treated the problem as classification, labelling each row "high" or "low" against the median score of
  its own subject and grade group, using medians calculated on the training data only.
- We did not use one overall median: because subjects and grades sit at different score levels, a single median
  would largely record which subject a row belongs to, and the model would learn the subject rather than anything
  about socio-economic status. `___` *(fill in after running: the crosstab showing this.)*
- Because the label splits each group at its own median, the classes are close to 50/50 and a majority-class
  baseline scores about 0.5. Accuracy is therefore a weak measure here and ROC-AUC is the more informative one.
- `___` *(fill in after running: results for the baseline, logistic regression and random forest, and which
  performed best.)*
- `___` *(fill in after running: whether the classification added anything the regression did not already show.)*

#### Step 12 — Feature importance `[Correction 6]` `[Correction 7]`

- Random Forest `feature_importances_` **and** `permutation_importance` on the validation set — impurity-based
  importance is biased toward high-cardinality / continuous features, so report both and explain the
  difference.
- Linear / logistic standardized coefficients as a third view.
- Answer the question the proposal posed, now with a wide predictor set: does the socio-economic index outweigh
  grade level, subject, sector, population, and the other CBS variables?
- Explicitly discuss the circularity flagged in §2.2 (the schooling-years and academic-degree variables feed
  the CBS index itself).

**→ Report:** produce ⭐ **Fig 12** (impurity-based vs permutation importance, side by side).

| Narrative cell | What this step supplies |
| --- | --- |
| Methods (§2) | Why two importance measures are reported rather than one |
| Results (§7) | The direct answer to the question the proposal posed: does the socio-economic index outweigh grade, subject, sector, population and the rest? Give the ranking, and name where the two measures disagree `[6]` |
| Discussion (§8) | The circularity caveat — schooling and degree variables are index inputs, so part of the importance ranking is structural rather than substantive; and the collinearity from Fig 5 means importance is shared across correlated predictors and should not be read as "this variable matters and that one doesn't" |

**Prompt:**

> show which variables matter most in the random forest, with built-in importance and permutation importance side by
> side — the built-in one favours continuous variables with many values, so they can disagree. add the standardised
> linear coefficients as a third view. i want to know whether the socio-economic index matters more than grade,
> subject, sector and population.

**For the report:**

- We measured variable importance two ways, the random forest's built-in importance and permutation importance,
  because the built-in measure tends to favour continuous variables with many values and the two can disagree.
- `___` *(fill in after running: the ranking of variables, whether the socio-economic index outranks grade,
  subject, sector and the other authority variables, and where the two measures disagree.)*
- These numbers should be read with care. Several CBS variables are used to build the socio-economic index
  itself, so part of their importance reflects how the index is constructed rather than independent information.
- The predictors are also strongly correlated with each other, so importance is shared between them. A low score
  for one variable does not mean it is irrelevant.

#### Step 13 — Sensitivity / robustness summary

One compact table, because it answers most of the predictable Q&A:

| Variation | Headline metric | Conclusion changes? |
| --- | --- | --- |
| Row-level split vs grouped split | | |
| Weighted vs unweighted by `n_students_tested` | | |
| Small-cell cutoff 20 / 30 / 50 | | |
| Sector rows (`norm_id` 3, 9) vs authority totals (`norm_id` 1) | | |
| `INDEX VALUE` vs `CLUSTER` as the SES encoding | | |
| Years 2016–2018 vs all of 2015–2019 | | |

**→ Report:** this is ⭐ **Table 9**, and it belongs in the Discussion, not the Results — it is the evidence that
the headline findings are not artefacts of six arbitrary choices. The Discussion paragraph should name which
variation moved the results most and state plainly whether the over/under-performer lists from Step 8 survived
all six. Anything that did *not* survive must be reported as not surviving; that is the difference between a
sensitivity analysis and decoration.

**Prompt:**

> re-run the main analysis under each of these and put it in one table: row split vs authority split, with and without
> weighting by students tested, small-cell cutoff at 20/30/50, sector rows vs combined totals, 1–10 cluster vs
> continuous index, and 2015–2019 vs 2016–2018. for each, the main metric and whether the list of over and
> under-performing authorities changes.

**For the report:**

- We re-ran the analysis under six different choices to check that the findings are not an artefact of decisions
  we made along the way: splitting by row rather than authority, with and without weighting, three small-cell
  cutoffs, sector rows versus combined totals, cluster versus continuous index, and the shorter versus longer
  year range.
- `___` *(fill in after running: which variation changed the results most, and whether the list of over- and
  under-performing authorities stayed the same. Anything that did not hold up must be reported as not holding
  up.)*

### 3.4 Notebook requirements checklist

- [ ] Kernel → Restart & Run All completes with **no errors**
- [ ] Section order follows the §3.2 skeleton (Background/Question → Methods → data/EDA/modeling → Results → Discussion)
- [ ] Markdown headers for every section; a short *what and why* cell above every non-trivial code step
- [ ] Report-level cells and step-level cells visually distinct and never blended (§3 rule)
- [ ] Abandoned attempts and debug output removed — final version only
- [ ] Every figure and table referenced in the report prose is produced by a cell in the same notebook
- [ ] **Register reconciled both ways:** every ID in the §3.3 register exists in the notebook with that caption,
      and every figure in the notebook appears in the register — no orphan figures, no promised-but-missing ones
- [ ] All five ⭐ headline items are actually discussed in the Results or Discussion prose, not merely plotted
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
| 6 | Key result 1 | **Fig 7** — the SES ↔ achievement scatter with over/under-performers labelled (Step 8) |
| 7 | Key result 2 | **Fig 9** (clusters vs official CBS clusters) + **Table 6** (over/under-performer characterization), trimmed to its most striking rows (Steps 8–9) |
| 8 | Conclusions | What the findings support for the stated audience, stated as association |
| 9 | Limitations | **Ecological fallacy by name** `[3]`; no causal claim `[2]`; aggregation; unmeasured confounders; honest statement of what the grouped split cost in measured performance |
| 10 | Backup | **Table 9** (sensitivity), **Fig 12** (feature importance), **A1** full residual ranking, **A2** hyperparameter grids |

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
9. How did you join two files with different authority codes? → The two-rule mapping in Step 4 plus four manual
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
