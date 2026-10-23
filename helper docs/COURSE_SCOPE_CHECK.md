# What in the notebook is outside the course scope

Checked 22/10/2026. Nothing in the notebook was changed.

**How this was checked.** All 12 lecture PDFs were extracted to text (296 slides, ~26,800 words) and searched
term by term. Separately, every `sklearn`/`scipy` import and every statistical method in the notebook's 61 code
cells was listed, then each one tested against the lecture text. Counts below are occurrences across all 12
lectures.

**The headline.** The analysis is mostly inside the course. **Nine things are genuinely absent** from every
lecture, and four more are borderline. None of them is wrong or needs removing — the instructions permit them:

> *"You are welcome to use methods not covered in class (e.g., additional clustering or prediction
> algorithms), provided you explain the general idea behind them and why you chose them."* — §2.3

So this is a list of **things that need one explanatory sentence each**, not a list of problems.

---

## ⚠️ First: one earlier decision was wrong

**ROC-AUC is core course content.** It is the subject of most of Lecture 12 ("Beyond Accuracy"), which covers
the ROC curve, FPR/TPR, and AUC with interpretation bands (0.5 random, 0.7 acceptable, 0.8 good, ≥0.9
excellent). We removed ROC-AUC from the classification section on the belief it had not been taught. **That was
my mistake, based on an assumption rather than a check.**

If you want it back in Table 9, it is squarely in scope and is the better metric for a near-balanced label.
Mann-Whitney and Bonferroni, removed at the same time, genuinely are absent (`t-test` 0, `confidence interval`
0, `mannwhitneyu` 0) — that part of the decision was right.

---

## Out of scope: absent from all 12 lectures

The last column is the important one: **five of the nine were not optional.** Three were demanded by the
instructor's corrections, one came from your own approved proposal, and one implements a rule Lecture 6 teaches.

| # | What | Why it's in the project | Where it's used in the notebook | Can it be removed? | Cost of removing it | Evidence it's not taught |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **`GroupShuffleSplit` / `GroupKFold`** | **Required by Correction 1**, which names these exact functions: *"Use a grouped split, such as GroupShuffleSplit or GroupKFold, with the local authority as the grouping variable."* | **Split by authority** (`GroupShuffleSplit`), **Folds for tuning** (`TUNING_CV`), both grid searches, and every `cross_val_predict` call in the gap analysis and the sensitivity rebuilds | **No** | Reverting to a row split reintroduces exactly the leakage that cost 4 of the 5 methodology points. The notebook measures it: 236 of 243 authorities would sit in two sets, 97% of test rows would come from authorities already seen, and authority averages alone would give a fake R² of 0.30. Every headline number becomes inflated | `GroupKFold` **0**. Lectures teach `train_test_split` (8) and `KFold` (2) only |
| 2 | **`cross_val_predict` / out-of-fold predictions** | **Our addition, forced by Correction 1.** A single split gives honest residuals only for the 122 authorities in validation and test; the 121 training authorities' residuals are shrunk because the model was fitted to them | **Over- and under-performing authorities** (the out-of-fold gaps), the forest-vs-linear check, and every rebuild in **Does any of this depend on the choices we made?** | Technically yes | The deviation analysis halves. You could only rank the 122 validation and test authorities, so "64 of 238 eligible" becomes roughly 30 of 120, and the robust core of 20 would shrink with it. The alternative — using in-sample residuals for the training authorities — is the dishonest option that flatters them | `cross_val_predict` **0**, "out-of-fold" **0**. CV is taught for *scoring* and for `GridSearchCV`, never to generate per-row predictions |
| 3 | **Adjusted Rand Index and Normalized Mutual Information** | **Needed for Correction 4**, which asks for *"the comparison between the clusters you generate from the data and the official clusters."* Silhouette, which is taught, measures how tight a clustering is, not whether two clusterings agree | **Grouping authorities by achievement** only — the ARI and NMI columns of **Table 8** | **Yes** | You lose the sharpest result in the clustering section. The finding is that the two systems **rank alike (Spearman 0.618) but group differently (ARI 0.086)** — and it takes both numbers to say that. With the crosstab heatmap alone you could show the disagreement but not quantify it, so Correction 4 gets a weaker answer | "adjusted rand" **0**, "rand index" **0**, "mutual information" **0**. Lec 8/9 teach *internal* cluster metrics (silhouette 35, elbow 10) but no external agreement measure |
| 4 | **Spearman rank correlation** | **Our choice, because the data is ordinal.** Cluster numbers 1–10 are ranks, not quantities, so Pearson would assume the gap from cluster 1 to 2 equals the gap from 9 to 10 | Three places: the ρ in each **Fig 3** panel title, the Spearman column of **Table 8**, and the forest-vs-linear agreement check after **Fig 8** | **Yes**, swap in Pearson | Low. The conclusions would not change much. The defect is conceptual: the clusters are unequally wide (cluster 5 spans 0.30 of the index, cluster 1 spans 0.89), so Pearson on cluster numbers treats unequal steps as equal. Fig 3's titles would also stop being robust to a non-linear rise | "spearman" **0**. Pearson correlation is taught (5) |
| 5 | **`LogisticRegression` as a model** | **From your own proposal**, which promised to *"compare the performance of multiple classifiers (e.g., Random Forest Classifier vs. Logistic Regression)"* — approved at 92/100 | **High or low: the same question as a classification** — **Table 9**, **Fig 12** and the test table. Its coefficients also form the third view in **Fig 13** | **Yes**, swap in KNN, SVM or Gradient Boosting, all taught | You lose the current winner. Logistic beats the forest 0.702 to 0.669, so Table 9's best number drops unless the substitute does better, and the observation that *logistic won the classification while the forest won the regression* disappears. It also breaks a promise the instructor approved, which is the bigger cost | **1** mention in 296 slides, an aside in Lec 10's SHAP section ("when the model is not tree-based — e.g. logistic regression") — never taught as a classifier |
| 6 | **`ColumnTransformer`** | **Implements a rule Lecture 6 does teach:** preprocessing must sit inside a `Pipeline` or it leaks into the CV folds. Our 16 numeric columns need imputing and scaling while the 4 categoricals need one-hot | Inside the `make_pipeline` helper in **Predicting the score**, so it runs in every model: linear, forest, logistic, forest classifier, and every sensitivity rebuild | **Not really** | The alternatives are worse. Preprocessing the whole frame before splitting leaks into every fold, which is the error Lec 6 warns about by name. Building and stacking two pipelines by hand is more code, more fragile, and still uses the same sklearn classes | **0**. `Pipeline` itself is taught (Lec 6, as the fix for CV leakage) but not column-wise transformers |
| 7 | **`sample_weight`** | **Required by Correction 7:** *"consider either weighting observations according to this variable or excluding particularly small cells."* We tested it, it made results worse, and we report that | **Linear regression** and **Random forest** cells — the weighted rows of **Table 5**, and the weighted columns of the test table. Used nowhere else | **Yes**, trivially | You lose the evidence that weighting was actually tried. Correction 7 offers weighting *or* excluding small cells, and the Ministry's own suppression means the exclusion route removes almost nothing (2 rows at a cutoff of 30). So dropping the weighted rows would leave Correction 7 answered by neither route | "sample weight" **0**, "class weight" **0** |
| 8 | **The t-statistic flagging rule** (mean gap ÷ standard error ≥ 2) | **Our addition, for defensibility.** Without it the over/under-performer list would be the top and bottom of a noisy ranking, mostly small authorities with few rows | **Over- and under-performing authorities** — the `t` column, the rule-count table that justifies the threshold, and the flagging itself. Reapplied in each sensitivity rebuild | **Yes — the easiest one to drop** | Near zero, and this is worth knowing. Once "every row must agree in sign" is required, the `t` threshold barely does anything: the count is 65, 64, 64 as `t` moves 1.5 → 2.0 → 2.5. Dropping the `t` requirement entirely would likely leave ~65 authorities instead of 64. ⚠️ Verify that count before relying on it, as it was never computed | "standard error" **1**, only as an item in a list of what a `statsmodels` OLS summary prints. No t-tests, no confidence intervals, no threshold rule |
| 9 | **Block permutation importance** (shuffling 16 columns jointly) | **Our addition, forced by Correction 6.** The wider predictor set created the collinearity that makes per-variable permutation uninformative | **Which variables actually matter** — **Table 10**, and now also the per-variable permutation column, where `subject_id` and `norm_id` are shuffled as dummy groups because they are pre-encoded | **Yes**, but don't | The answer to the proposal's own question flips to a **wrong** one. Per-variable permutation puts `ses_index` ninth at 0.011, which reads as "socio-economic standing barely matters". The block says 0.374, second only to test identity. Removing this means either dropping the question or answering it incorrectly | Custom. Permutation importance *is* taught (Lec 10, 5 mentions) but only one feature at a time |

**Reading the column:** items 1, 3 and 7 trace directly to the instructor's corrections and item 5 to your
approved proposal, so four of the nine were effectively assigned. Item 6 is an implementation detail of a
taught rule. The four genuinely discretionary ones are **2, 4, 8 and 9** — and each exists because a simpler,
taught alternative would have given a misleading answer, which is the argument to make if asked.

---

## Borderline: the idea is taught, the specific tool is not

**None of these four is discretionary.** Two come from your approved proposal, one from the project
instructions, and one from Correction 6. In every case the lectures teach the idea and the notebook uses the
sklearn class that implements it.

| # | What | Why it's in the project | Where it's used in the notebook | Can it be removed? | Cost of removing it | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 10 | **`RandomForestRegressor`** | **From your own proposal**, which promised *"a Random Forest Regressor and a Linear Regression model to predict the continuous `score`... compare their performance metrics."* The feedback praised exactly this: *"a regression track and a classification track with two competing models in each"* | Tuned in the **Random forest** cell, then reused as `chosen_model` for the gaps, for **Fig 13**, and in all seven sensitivity rebuilds | **Yes**, keep linear regression only | High. You lose the better model: test R² 0.530 against linear's 0.400. The gaps get noisier, and the sensitivity table shows the linear version keeps only 34 of the 64 flagged authorities, so the robust core shrinks too. It also breaks the two-models-per-track structure the instructor praised | Lec 6 says *"For regression, the predictions are averaged"* and advises `min_samples_leaf ≥ 5 for regression`, so forests for regression are acknowledged. But only `RandomForestClassifier` is demonstrated (2 mentions), and no regression example is worked |
| 11 | **`SimpleImputer`** | **Forced by Correction 6.** The wider predictor set brought in the 14 CBS variables, which the CBS suppresses for 3 authorities under 2,000 residents. The class keeps the median inside the pipeline so it comes from the training fold only, per Lec 6's leakage rule | The numeric branch of `make_pipeline` in **Predicting the score**, so it runs in every model and every rebuild | **Yes**, drop those 3 authorities instead | Low to moderate. 243 authorities becomes 240, and one of the three is Kefar Shemaryahu — one of only **four** authorities in cluster 10. That thins the top of the socio-economic range, exactly where over-performance claims are already weakest. Filling the medians by hand instead would leak | Median imputation is core Lec 2 material ("median" 21, "imputation" 8). The sklearn class is never shown (**0**) |
| 12 | **`OneHotEncoder`** | **Unavoidable given the feature set.** (`subject_id` and `norm_id` are now encoded in the cleaning step instead, leaving this for grade and year.) Four predictors are unordered categories (subject, grade, sector, year) and Lec 2 teaches one-hot for exactly that | The categorical branch of `make_pipeline` in **Predicting the score**, so it runs in every model and every rebuild | **Yes**, use `pd.get_dummies` | Low but with no upside. Encoding before the split fixes the category set from the whole dataset, and a CV fold missing a category would then misalign the columns. `handle_unknown="ignore"` inside the pipeline is what prevents that | One-hot encoding is core Lec 2 material (6 mentions). The sklearn class is never shown (**0**) |
| 13 | **Three-way train / validation / test split** | **Required by the instructions and named in the feedback.** §2.3 lists *"Splitting the data into training / testing / validation sets (e.g., 50%-30%-20%)"*, the proposal promised 50/30/20, and the feedback listed *"train/validation/test splitting"* among what the work plan got right | **Split by authority** creates it; **Predicting the score** fits on train and compares on validation; **The test set, used once** and the classification test cell open the test set | **No** | It contradicts §2.3 directly. Worse, with only train and test, the three decisions made on validation — forest over linear, weighting rejected, logistic over forest — would have to be made on the test set, which destroys the one honest final estimate you have | "validation set" **0**, "three-way" **0**. Lectures use an 80/20 train/test split plus k-fold CV |

**Reading the column:** these are the easiest four to defend, because in each case the lectures supply the
concept and the only gap is which function performs it. If challenged, the honest answer for 11 and 12 is that
the sklearn class was chosen over the manual alternative *specifically* to satisfy Lecture 6's rule that
preprocessing must live inside the pipeline — so the unfamiliar tool is there in service of a taught principle.

---

## Confirmed in scope

Worth knowing what needs no defending:

- **Cleaning** (Lec 2): missing values (55), imputation, median, outliers (32), IQR, z-score, encoding (17)
- **EDA** (Lec 2–3): correlation (21), Pearson, heatmaps, boxplots, histograms
- **Supervised learning** (Lec 4–6): KNN (25), decision trees (27), random forest (21), gradient boosting (16),
  SVM (12), overfitting (30), ensembles/bagging
- **Tuning** (Lec 6): `GridSearchCV` (16), `RandomizedSearchCV` (7), k-fold CV (8), the `Pipeline`-prevents-
  leakage point (leakage 4)
- **Regression** (Lec 7): linear regression (8), R² (8), RMSE (4), MAE (7), residuals (20), coefficients (20),
  `statsmodels` OLS with p-values
- **Classification metrics** (Lec 3, 11, 12): accuracy (82), precision (97), recall (103), F1 (38), confusion
  matrix (7), **ROC/AUC**, class imbalance, SMOTE (9)
- **Clustering** (Lec 8–9): K-means (40+20), silhouette (35), elbow (10), `StandardScaler` (6), PCA (19), t-SNE
- **Explainability** (Lec 10): feature importance (19), MDI vs permutation importance, SHAP (115), LIME (28)

---

## What to do about it

Ranked by how likely a grader is to stop on it. **None of these require code changes** — each needs a clause or
a sentence in the Methods narrative saying what the tool does and why it was chosen.

1. **The grouped split (#1).** Highest priority, because it is both the most-used unfamiliar tool and the thing
   Correction 1 demanded. It cannot be removed. One sentence: it is an ordinary train/test split except whole
   authorities move together, because rows from one authority are not independent.
2. **Logistic regression (#5).** It is your winning classifier and it is effectively untaught. Two sentences on
   what it is (a linear model predicting the probability of a class) and why it suits a binary target.
3. **ARI and NMI (#3).** One sentence: both compare two groupings of the same items, 0 meaning no better than
   chance agreement. Silhouette, which *is* taught, answers a different question and cannot replace them.
4. **Out-of-fold predictions (#2).** One sentence: ordinary cross-validation, but keeping each fold's
   predictions so every authority is scored by a model that never saw it.
5. **The t-statistic rule (#8).** One sentence on why the gap is divided by its standard error, i.e. judging a
   gap against its own uncertainty rather than against a fixed cut-off.
6. **Block permutation (#9).** One sentence: the taught permutation importance, applied to a group of columns
   at once because the socio-economic variables substitute for each other.
7. **Spearman (#4), `ColumnTransformer` (#6), `sample_weight` (#7), `SimpleImputer`/`OneHotEncoder` (#11–12).**
   Minor. Spearman deserves a half-sentence ("correlation of the ranks rather than the values"); the three
   sklearn classes are just implementations of taught ideas and need nothing.
8. **`RandomForestRegressor` (#10).** Probably needs nothing, since Lec 6 states the regression case directly,
   but it is worth one clause noting that the forest averages its trees' predicted numbers.

**A word of caution for the meeting.** The presentation is graded mainly on being able to defend every choice.
Items 1, 2, 3, 8 and 9 are the ones most likely to prompt "we didn't cover that — explain it", so each of you
should be able to give the one-sentence version without notes.
