# Final Project — Full Execution Plan

**Course:** Introduction to Data Science, Semester 2, תשפ״ו (2025/2026)
**Team:** Stav Tchizik (316062835), Or Cohen (206631509)
**Question (final wording):** Which Israeli local authorities achieve **higher or lower Meitzav scores than their socio-economic standing predicts**, and what authority-level characteristics distinguish them?

This document is organized **by the sections of `Final_project_instructions_1.pdf`**. Inside each section, every
relevant correction from `Proposal_Response_English_Translation.pdf` is addressed explicitly and marked
`[Correction N]`. The nine corrections are the main grading lever for the final report — the proposal grade
(92/100) is frozen, but *not* implementing these recommendations will lower the report grade.

**Two decisions already locked in (deviating from the proposal):**

| Topic | Proposal said | Final project does | Why |
| --- | --- | --- | --- |
| Years of education data | "multiple years" (2015–2019, unspecified) | **2016, 2017, 2018 only** | Centres the panel on the SES index year → `[Correction 8]` |
| CBS socio-economic index edition | 2021 edition | **2017 edition** (`datasets/t01_2017.xls`) | Removes the temporal mismatch the instructor flagged → `[Correction 8]` |

With 2016–2018 education data and the 2017 index, the datasets are aligned to within ±1 year. This is a much
stronger answer to Correction 8 than merely "acknowledging a mismatch", and it must be *stated as a deliberate
design choice* in the report, not left implicit.

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
| 9 | AI-use statement (tools, purposes, prompts) | §5 | ☐ |

---

## 1. Timeline & Grade Weights

| Milestone | Deadline | Weight | Status |
| --- | --- | --- | --- |
| Project proposal | 15/8/2026 | 20% | ✅ Submitted, graded **92/100**, approved |
| Final report (PDF/DOCX) + Jupyter notebook | **18/10/2026** | 40% | ☐ In progress |
| Final presentation (scheduled meeting) | Within 2 weeks after 18/10/2026 | 40% | ☐ Not started |

### Working schedule (≈3 working days per person)

| Day | Owner split | Deliverable |
| --- | --- | --- |
| 1 | Both | Load + clean both files, resolve the authority-ID join, lock the analysis table (§3.3 Steps 1–4) |
| 2 | Both | EDA + correlation + grouped split skeleton (§3.3 Steps 5–6) |
| 3 | Split | Regression track + residual/deviation analysis (§3.3 Steps 7–10) |
| 4 | Split | Clustering + classification + feature importance (§3.3 Steps 9, 11–13) |
| 5 | Both | Notebook cleanup (Restart & Run All), figure polish, report draft |
| 6 | Both | Report final pass, AI statement, slide deck, rehearsal |

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

Two deliverables: a written report (PDF or DOCX, ~3–5 pages excluding figures/tables/appendices) and a single
Jupyter notebook. Submit zipped together, or the notebook alone if self-contained.

### 3.1 Report content — section-by-section writing brief

| Report section | What to write | Corrections to land here |
| --- | --- | --- |
| **Background** | Meitzav as the national standardized assessment; CBS socio-economic index as the standard authority-level SES measure; why authority-level gaps matter for budgeting and targeted intervention; who the audience is (Ministry of Education, RAMA, municipal leadership, policy makers) | — |
| **Question** | The three-level hierarchy from §2.1. **State explicitly that the question changed from the proposal** — the causal verb was removed and the emphasis moved from the SES↔achievement gradient to deviations from it — and say why (the gradient is already documented; cite RAMA and the Knesset Research and Information Center) | `[2]`, `[4]` |
| **Methods** | The pipeline of §3.3 in order, naming **packages and parameters**: pandas, numpy, matplotlib/seaborn, scikit-learn (`GroupShuffleSplit`, `GroupKFold`, `GridSearchCV`/`RandomizedSearchCV`, `LinearRegression`, `RandomForestRegressor`, `LogisticRegression`, `RandomForestClassifier`, `KMeans`, `StandardScaler`, `permutation_importance`), scipy.stats. Spell out the join rule, the year restriction, the grouped split, the threshold rule, the weighting rule, and the random seed | `[1]`, `[5]`, `[6]`, `[7]`, `[8]` |
| **Results** | Lead with the deviation / over- and under-performer findings; the SES gradient is presented as a validated calibration step, not the punchline. 4–6 figures max in-body; oversized tables (full authority residual table, full hyperparameter grid) → appendix. Each figure gets a caption naming the notebook section that produced it | `[4]` |
| **Discussion** | (a) What the results mean for the stated audience. (b) **Causality** — observational, cross-sectional data; associations only; confounding by composition, sector, geography `[2]`. (c) **Ecological fallacy** — *named explicitly*, one full paragraph: the data are authority aggregates, so an authority-level association says nothing about any individual student; a high-SES authority can contain low-achieving students and vice versa, and the authority-level correlation is typically *larger* than the individual-level one; the findings license decisions about *authorities* (where to target resources), not inferences about *students* `[3]`. (d) Whether the approach was appropriate, what would be done differently (student-level data, more years, a true panel / fixed-effects design), what remains unknown, and how to address it | `[2]`, `[3]` |
| **AI usage statement** | See §5 | `[9]` |

### 3.2 Report format checklist

- [ ] ~3–5 pages excluding figures/tables/appendices
- [ ] PDF or DOCX
- [ ] Figures/tables embedded in the relevant section; oversized tables moved to an appendix
- [ ] Every result cross-referenced to a notebook cell/section number
- [ ] Figures legible, axes labelled, units stated, colour-blind-safe palette
- [ ] All five required sections present + AI statement

### 3.3 Notebook pipeline — the actual steps

Notebook section order must mirror the report: Background/EDA → Methods → Results → Discussion. Every
non-trivial step gets a short markdown cell saying *what* and *why*. One random seed defined once at the top
and reused everywhere.

#### Step 1 — Setup and load

- Imports, `RANDOM_STATE = 42`, display options, plotting defaults.
- Load the education CSV; load the CBS `.xls` with `pandas.read_excel(..., sheet_name='t01', header=None, skiprows=10)` — `xlrd` is required for legacy `.xls`.
- Drop the 5 trailing CBS footnote rows (identified by a non-numeric / empty cluster value) and the two national
  summary rows (AVERAGE, NATIONWIDE VALUE).
- Assign explicit English column names to the CBS block instead of relying on the bilingual multi-row header.

#### Step 2 — Restrict years `[Correction 8]`

- Keep `year ∈ {2016, 2017, 2018}` → 2,087 rows, 250 authorities.
- Markdown cell justifying it: the 2017 CBS index edition is the SES measure, so the education window is
  centred on it (±1 year). Record the discarded 2015 and 2019 rows and say that extending the window would
  reintroduce the mismatch the instructor flagged.
- Sanity-check that scores do not drift materially across 2016–2018 (if they do, keep `year` as a model
  covariate and say so).

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

**Verification cells (required, and worth a table in the report):** assert that 100% of education authorities
match after the overrides; print any unmatched rows; cross-check matched pairs by normalized Hebrew name and
list the mismatches; report how many of the 255 CBS authorities have no education data (these are legitimately
absent — small authorities with no Meitzav reporting — and should be reported as coverage, not as an error).

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

#### Step 10 — Geographic / descriptive layer (optional, if time allows)

- Table or simple chart of over/under-performers by district or sector. A map is not required and is a time
  sink; a sorted bar chart communicates the same thing.

#### Step 11 — Classification track `[Correction 5]`

- **Threshold rule — state it explicitly in the report and the notebook, verbatim:**
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

#### Step 12 — Feature importance `[Correction 6]` `[Correction 7]`

- Random Forest `feature_importances_` **and** `permutation_importance` on the validation set — impurity-based
  importance is biased toward high-cardinality / continuous features, so report both and explain the
  difference.
- Linear / logistic standardized coefficients as a third view.
- Answer the question the proposal posed, now with a wide predictor set: does the socio-economic index outweigh
  grade level, subject, sector, population, and the other CBS variables?
- Explicitly discuss the circularity flagged in §2.2 (the schooling-years and academic-degree variables feed
  the CBS index itself).

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

### 3.4 Notebook requirements checklist

- [ ] Kernel → Restart & Run All completes with **no errors**
- [ ] Section order matches the report (Background/EDA → Methods → Results → Discussion)
- [ ] Markdown headers for every section; a short markdown/comment on every non-trivial step saying what and why
- [ ] Abandoned attempts and debug output removed — final version only
- [ ] Every figure/table in the report is reproducible from the notebook
- [ ] `RANDOM_STATE` set once and reused; results reproducible on re-run
- [ ] No test-set usage before the final evaluation; no label or scaler leakage across folds
- [ ] A note of the package versions used (`xlrd` is needed for the legacy `.xls`)

### 3.5 Submission checklist

- [ ] Report has all five sections + AI usage statement
- [ ] Notebook runs top-to-bottom with no errors
- [ ] Notebook organized and commented, matching the report structure
- [ ] Figures legible and correctly labelled
- [ ] Zipped together (report + notebook + `datasets/`) or a single self-contained notebook
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
| 6 | Key result 1 | The SES ↔ achievement scatter with over/under-performers labelled (Step 8) |
| 7 | Key result 2 | Data-driven clusters vs official CBS clusters, plus the over/under-performer characterization table (Steps 8–9) |
| 8 | Conclusions | What the findings support for the stated audience, stated as association |
| 9 | Limitations | **Ecological fallacy by name** `[3]`; no causal claim `[2]`; aggregation; unmeasured confounders; honest statement of what the grouped split cost in measured performance |
| 10 | Backup | Sensitivity table (Step 13), full residual ranking, hyperparameter grids |

### 4.1 Presentation checklist

- [ ] Covers motivation, question, dataset/methods, key results, conclusions/limitations
- [ ] Rehearsed to fit in 10 minutes
- [ ] Figures readable at presentation size — regenerate at presentation resolution, do not shrink notebook PNGs
- [ ] Submitted before the assigned slot
- [ ] **Both partners can explain every choice** — this component is 40% and is graded primarily on demonstrated understanding

---

## 5. Using AI — required statement `[Correction 9]`

Not required at the proposal stage; **required in the final report**. Keep a running log from now on — it
cannot be reconstructed later.

The statement must cover:

1. **Which tools** — e.g. Claude (Claude Code), ChatGPT; name them and note roughly when and for what.
2. **What they were used for** — e.g. debugging a merge, drafting report prose, suggesting a method, explaining
   a scikit-learn API, planning the project structure (including this document).
3. **The prompts used** — actual prompt text. Long prompt logs go in an appendix; the in-body statement can
   summarize and point to it.

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
| Report + Notebook | **Notebook organization** | 8% | §3.3 step order mirrors the report; markdown header per step; Restart & Run All clean; §3.4 checklist |
| Report + Notebook | **Report readability** | 8% | §3.1 writing brief; 3–5 pages; 4–6 in-body figures; large tables to appendix; notebook cross-references |
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
