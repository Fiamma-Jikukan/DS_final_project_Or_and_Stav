# What's left to do

Checked against the notebook on 18/10/2026. The notebook has 141 cells, runs top to bottom in ~240s, and all
13 analysis steps are implemented.

**No more analysis is needed. What's left is six markdown cells.** Because we chose the single-notebook route,
the notebook *is* the report — there is no separate .docx or PDF to write. The analysis prose is already there
(every figure has its interpretation cell). What's missing is the report-level framing around it: a Background
and Methods at the top, and Results, Discussion, AI statement and Appendix at the bottom. Section 2 below says
exactly what goes in each. Total new prose: the equivalent of 3–5 pages.

Plus two small technical items (§4) and the presentation (§3).

---

## 1. The nine corrections

| # | Correction | Status |
| --- | --- | --- |
| 1 | Split by authority, not by row | ✅ Done. Cluster-stratified grouped split, plus the row-split comparison showing authority averages alone give R² 0.30 |
| 2 | Remove causal wording | 🟡 Mostly. The question and all analysis prose are non-causal. The explicit causality paragraph belongs in the Discussion, which isn't written |
| 3 | **Name the ecological fallacy** | ❌ **Not done.** The phrase appears nowhere in the notebook. Needs its own paragraph in the Discussion |
| 4 | Make deviation analysis central | ✅ Done. Steps 8, 9 and 13 are the core of the notebook |
| 5 | Define the classification threshold | ✅ Done. Rule stated verbatim, plus the crosstab proving a pooled median would encode the subject (87% vs 18%) |
| 6 | Expand predictors, one encoding per use | ✅ Done. 20 features; `ses_index` for models and `ses_cluster` for grouping; the block permutation in Step 12 |
| 7 | CV, baselines, weighting | ✅ Done. `GroupKFold` tuning, two regression baselines, majority-class baseline, weighting tested and rejected |
| 8 | Specify and align the years | ✅ Done. 2016–2018 against the 2017 index, with the reasoning stated |
| 9 | **AI usage statement** | ❌ **Not done.** No statement cell, and no prompt log file exists yet |

**Two corrections are outstanding: 3 and 9.** Both are writing tasks.

---

## 2. The six cells to write

Each row is one markdown cell. Lengths are rough targets, not rules.

| # | Cell | Goes | Length |
| --- | --- | --- | --- |
| 1 | Background | top of cell 0, above the research question | ~200 words |
| 2 | Methods overview | new section before "Loading the data" | ~350 words |
| 3 | Results | after Step 13, before Discussion | ~600 words |
| 4 | Discussion | after Results | ~700 words |
| 5 | AI usage statement | after Discussion | ~150 words + the prompt log |
| 6 | Appendix | last cell | ~100 words |

### 1. Background

What the reader needs before the question makes sense.

- Meitzav is Israel's national school assessment. RAMA rotates schools through three national groups, each
  tested once every three years, which is why 215 of our 243 authorities appear in a single year.
- The CBS socio-economic index ranks all 255 local authorities, published as a continuous value and as 1–10
  clusters. 2017 edition.
- Why authority-level gaps matter: budget allocation and targeted intervention are decided at this level.
- The audience: Ministry of Education, RAMA, municipal leadership, policy makers.
- One sentence citing RAMA's own authority reports, which already compare each authority to socio-economically
  similar ones, and saying what this project adds (a cross-authority ranking of deviations, and what
  distinguishes them).

### 2. Methods overview

The whole pipeline in prose, up front, so the reader knows what is coming. Name the packages (pandas, numpy,
matplotlib, scikit-learn) and the seed (42). Then, one or two sentences each:

- Two official sources, merged on a key we built: `rashut // 10` for cities and local councils, the council
  number for regional councils, four merged cities by hand.
- 2016–2018 only, to sit around the 2017 index.
- Combined-total rows where they exist, because mixed cities otherwise appear twice.
- 3,067 rows → 1,749; 251 → 243 authorities.
- Split by authority, stratified by cluster, roughly 50/20/30, because rows from the same authority are not
  independent.
- Random forest and linear regression against two baselines; forest won (test R² 0.530).
- Gaps computed out-of-fold and standardized within subject × grade.
- The High/Low rule, quoted verbatim.
- Weighting by students tested was tested and rejected.

### 3. Results

Numbers are all computed — this is assembling them into an argument. **Order matters:** lead with what was
found, not with the nulls.

1. **The deviation finding.** 64 authorities deviate consistently (33 over, 31 under); **21 survive every one
   of seven rebuilds** and **no authority ever changed direction**. Name the 21. Typical gap ~1 SD ≈ 26 points.
2. **The gradient, as calibration.** The known result reproduced: Spearman up to 0.73 by subject, and the gaps
   left over carry no socio-economic signal (r = 0.011) — which is what makes them interpretable.
3. **Two cluster systems that rank alike but group differently.** Spearman 0.618, ARI 0.086; 43 of 223
   authorities sit 3+ clusters from where achievement puts them. The extremes overlap with the Step 8 list.
4. **Deviation is sometimes subject-specific.** Fig 11: one group of 15 authorities is above prediction in
   English and below it in Maths and Science.
5. **Then the nulls, as what they rule out.** Nothing among 22 variables separates over- from
   under-performers (largest r = 0.162). Subject and grade outweigh the whole socio-economic block (R² loss
   0.609 vs 0.374). The classifier adds nothing over the regression (70.6% vs 70.9%).

Refer to figures by register number. Oversized tables go to the Appendix.

### 4. Discussion

**The largest single item in the grade (16%).** Five things to cover:

- **The ecological fallacy, by name** `[Correction 3]`. One full paragraph: the data are authority averages, so
  an authority-level association says nothing about any individual student; a high-scoring authority contains
  low-scoring students and vice versa; the authority-level correlation is typically larger than the
  individual-level one. The findings license decisions about *authorities*, not claims about students. Contrast
  with RAMA, whose figures are student-level.
- **No causality** `[Correction 2]`. Observational and cross-sectional; name a plausible confounder.
- **What the nulls mean.** Whatever drives the gaps is plausibly school-level and organisational (teaching
  quality, school leadership, municipal policy, specific programmes) and is in neither dataset. Say what it
  would take to test that: school-level or student-level data.
- **Limitations.** Five CBS authorities have no education data and four of them are Haredi, so the coverage gap
  is systematic. 215 of 243 authorities appear in one year, so year-to-year consistency was only checkable for
  28. The gap correlates 0.75 with raw mean score, so the list is partly "far from the middle". The flagging
  threshold is sharp — removing 2 rows changes 8 of the 64, which is why the 21 is the list to name. Three
  authorities have median-imputed CBS variables, one of them in cluster 10 of only four.
- **What we'd do differently.** Student- or school-level data, a true multi-year panel with authority fixed
  effects, district and peripherality variables.

### 5. AI usage statement

Required by instructions §5, and **Correction 9**.

- Which tools, and what for: debugging, drafting prose, suggesting methods, explaining APIs, planning.
- The actual prompts. The 14 step prompts in `PROJECT_PLAN.md` cover the analysis and can be pasted in.
- ⚠️ **Not yet logged:** the debugging, explanation and planning prompts from the working sessions. These
  cannot be reconstructed later — write down what you remember now, and keep a running log from here.

### 6. Appendix

Point to the four exported files and the oversized tables: `authority_gaps.xlsx` (all 243 ranked),
`robust_authorities.xlsx` (the 21), `authority_clusters.xlsx`, `cleaned_dataset.xlsx`, the hyperparameter grids,
the full correlation matrix, and the prompt log.

## 3. Presentation (40% of the grade)

Not started. Due within two weeks after 18/10/2026.

- ~8–10 slides: motivation, question, data/methods, 1–2 key figures, conclusions, limitations
- The plan's §4 has a slide-by-slide outline; the headline figures are Fig 8, Fig 10, Fig 11, Fig 13
- Rehearse to 10 minutes. **Both partners must be able to defend every choice** — this is graded mostly on
  demonstrated understanding, and §Appendix A of the plan has the ten likely questions

---

## 4. Two technical items

- **Package versions cell.** Not present. The notebook needs `xlrd` (for the legacy `.xls`) and `openpyxl` (for
  the Excel writes). `scipy` is no longer used.
- **Variable shadowing.** Step 11 reassigns `y_train` / `y_val` / `y_test` from the score to the High/Low
  label, so any later cell using them expecting scores silently gets 0s and 1s. Step 12 works around it by
  re-deriving `score_val`. Renaming Step 11's to `y_train_label` etc. would remove the hazard.

---

## 5. Before submitting

- [ ] Real **Kernel → Restart & Run All** in Jupyter. The 240s timing comes from running the cells in a script;
      it has never been run in an actual kernel end to end
- [ ] Re-read Results and Discussion against the printed output, so no quoted number has drifted
- [ ] Decide and state the **data route**: ship the `.ipynb` with `datasets/` in one zip (simplest, allowed), or
      have the notebook download the files
- [ ] Name the **21 robust authorities** rather than the 64 in the report. The cutoff-at-30 variation removes
      only 2 rows yet changes 8 of the 64, so the 64's membership is a snapshot
- [ ] Figures legible at presentation size
- [ ] Decide whether Step 10 (who sits in the tails) stays skipped. If it stays skipped, nothing to clean up
      since it was never written

---

## Already decided, no action needed

- Step 10 skipped (optional)
- Mann-Whitney, Bonferroni and ROC-AUC removed as not covered in the course
- Weighting by students tested tested and rejected
- Option B grain (combined totals where they exist)
- Figure and table numbering reconciled: Fig 1–13, Tables 1 and 4–11. Tables 2 and 3 do not exist — don't refer
  to them
