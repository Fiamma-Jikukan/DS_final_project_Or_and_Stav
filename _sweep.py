import io

p = "helper docs/PROJECT_PLAN.md"
s = io.open(p, encoding="utf-8").read()

start = s.index("#### Figure and table register")
end = s.index("#### Cleaning: what happens before the merge and what happens after")
old_block = s[start:end]

new_block = """#### Figure and table register

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
| ⭐ Fig 13 | Feature importance: impurity-based vs permutation, side by side | Step 12 *(pending)* | Results (§7) + Discussion (§8) |
| ⭐ Table 10 | Sensitivity / robustness summary | Step 13 *(pending)* | Discussion (§8) |
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

That is 6 headline items (Fig 8, Fig 10, Fig 11, Fig 13, Table 7, Table 10). Fig 11 was added after Step 9
found that deviation is sometimes subject-specific rather than uniform, which Step 8's single gap per authority
could not show. These are the set the Results and Discussion are built around, and the set the slide deck draws
on (§4).

"""

s = s[:start] + new_block + s[end:]

# downstream references to the old numbering
fixes = [
    ("⭐ **Fig 7** (the signature figure) and ⭐ **Table 6** (the\nover- vs under-performer characterization). Full ranked residual table for all authorities → appendix **A1**.",
     "⭐ **Fig 8** (the signature figure) and ⭐ **Table 7** (each\nvariable against the gap). Full ranked gaps for all authorities → appendix **A1**."),
    ("Name the authorities that over- and under-perform, how many clear the consistency bar out of 243, how large the typical deviation is in score points, and what Table 6 says distinguishes the two groups `[4]`",
     "Name the authorities that over- and under-perform, how many clear the consistency bar out of 243, how large the typical deviation is in score points, and what Table 7 says distinguishes the two groups `[4]`"),
    ("**→ Report:** produce **Fig 8** (elbow + silhouette), ⭐ **Fig 9** (crosstab heatmap, achievement clusters vs\nofficial CBS clusters), **Table 7** (ARI, NMI, Spearman + the list of mismatched authorities), and **Fig 10**\n(PCA, supporting).",
     "**→ Report:** produce **Fig 9** (elbow + silhouette), ⭐ **Fig 10** (crosstab heatmaps), **Table 8** (ARI, NMI,\nSpearman) and ⭐ **Fig 11** (gap-group profiles, uniform vs subject-specific)."),
    ("**→ Report:** produce ⭐ **Fig 12** (impurity-based vs permutation importance, side by side).",
     "**→ Report:** produce ⭐ **Fig 13** (impurity-based vs permutation importance, side by side)."),
    ("**→ Report:** this is ⭐ **Table 9**, and it belongs in the Discussion",
     "**→ Report:** this is ⭐ **Table 10**, and it belongs in the Discussion"),
    ("| Results (§7) | Fig 12 read", "| Results (§7) | Fig 13 read"),
    ("⭐ Fig 12 | Feature importance", "⭐ Fig 13 | Feature importance"),
    ("The row-level-vs-grouped comparison goes into\n**Table 9** (Step 13)", "The row-level-vs-grouped comparison goes into\n**Table 10** (Step 13)"),
    ("which the sector-rows variation in **Table 9** is there to test", "which the sector-rows variation in **Table 10** is there to test"),
    ("| 6 | Key result 1 | **Fig 7** — the SES ↔ achievement scatter with over/under-performers labelled (Step 8) |",
     "| 6 | Key result 1 | **Fig 8**, the gap against the socio-economic index with the extremes labelled (Step 8) |"),
    ("| 7 | Key result 2 | **Fig 9** (clusters vs official CBS clusters) + **Table 6** (over/under-performer characterization), trimmed to its most striking rows (Steps 8–9) |",
     "| 7 | Key result 2 | **Fig 10** (groups vs official clusters) + **Fig 11** (subject-specific deviation), the two Step 9 findings (Steps 8–9) |"),
    ("| 10 | Backup | **Table 9** (sensitivity), **Fig 12** (feature importance), **A1** full residual ranking, **A2** hyperparameter grids |",
     "| 10 | Backup | **Table 10** (sensitivity), **Fig 13** (feature importance), **A1** ranked gaps, **A3** hyperparameter grids |"),
    ("the five ⭐ headline items in the §3.3 register (Fig 7, Fig 9, Fig 12, Table 6, Table 9)",
     "the six ⭐ headline items in the §3.3 register (Fig 8, Fig 10, Fig 11, Fig 13, Table 7, Table 10)"),
    ("Oversized tables (full authority residual ranking A1, hyperparameter grids A2)",
     "Oversized tables (ranked gaps A1, hyperparameter grids A3)"),
    ("- [ ] All five ⭐ headline items are actually discussed in the Results or Discussion prose, not merely plotted",
     "- [ ] All six ⭐ headline items are actually discussed in the Results or Discussion prose, not merely plotted"),
    ("extends **Table 3** with the post-merge column inventory", "records the post-merge column inventory"),
    ("and **Table 2** with the final\nanalysis-table shape", "and the final\nanalysis-table shape"),
]

applied, missed = 0, []
for old, new in fixes:
    if s.count(old) >= 1:
        s = s.replace(old, new)
        applied += 1
    else:
        missed.append(old[:60])

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print(f"register rewritten; {applied} of {len(fixes)} downstream refs updated")
for m in missed:
    print("  NOT FOUND:", m)
