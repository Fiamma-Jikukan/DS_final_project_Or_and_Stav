# Prepare: questions the lecturer is likely to ask

Ten "why did you choose this?" questions, with an answer to say out loud, the numbers to reach for if pushed,
and the weak spot to concede rather than defend. **Five basic**, then **five detail**.

A rule for all ten: give the choice, then the alternative we rejected, then the number that decided it. Never
answer with only the number.

---

# Basic

## 1. Why did we choose the local authority as the unit, rather than schools or pupils?

**Say:** Because that is the level decisions are made at — school budgets, staffing and intervention
programmes in Israel are allocated to local authorities. A finding about an authority is something somebody
can act on.

**If pushed:** It is also the level both files publish at. The Meitzav extract and the CBS index are both per
authority, so school- or pupil-level work was not available to us, not just not chosen.

**Concede:** It is the project's main limitation, and slide 11 says so. Every number describes a town, not a
child, and the thing that most likely explains the gaps is probably happening inside individual schools, where
neither dataset can see.

---

## 2. Why did we choose to keep only 2016 to 2018?

**Say:** The socio-economic index we use is the 2017 edition, a single snapshot. Keeping 2015 and 2019 would
mean judging a score against circumstances measured two years before or after it.

**If pushed:** The filter drops 980 rows, 734 from 2015 and 246 from 2019, leaving 2,087 before the join. We did
not simply assume it was harmless: slide 13 rebuilds the whole analysis on all five years. The model actually
scores slightly better (R² 0.570), but only 38 of the 65 flagged authorities survive.

**Concede:** Scores still drift within the three years we kept — a median of 13.5 points across subjects — so
the window does not remove the time problem, it only shrinks it. That is why `year` stays in the models as a
variable.

---

## 3. Why did we choose to split by authority instead of splitting rows at random?

**Say:** Because the rows are not independent. 1,749 rows come from only 243 authorities, so the same town
appears many times. A random row split puts the same town on both sides, and the model can score well by
recognising towns rather than learning anything.

**If pushed:** We measured the size of that shortcut rather than asserting it. Under a row split, 236 of the
243 authorities land in more than one set, and predicting each test row from nothing but its own authority's
training average — with no socio-economic variable at all — already reaches R² = 0.30. Under our split, 0 of
the 74 test authorities had been seen in training.

**Concede:** It cost us a better-looking headline. A row split would have scored higher, and we are reporting
the smaller, honest number on purpose.

---

## 4. Why did we choose a random forest as the main model?

**Say:** We did not assume it; we ran both tracks. Linear regression and a forest were fitted on the same
features and compared on validation, and the forest won. The relationships here are not straight lines — the
socio-economic gradient is strong in English grade 8 and nearly flat in Arabic grade 5 — so a model that can
bend was likely to help.

**If pushed:** R² = 0.530 on the held-out authorities against 0.281 for a baseline that knows only the subject
and grade. The settings came from a 27-point grid search (depth, leaf size, features per split) scored with
`GroupKFold(5)`, which picked unlimited depth, leaves of one, and `sqrt` features, with 400 trees. We also
tested weighting rows by students tested and rejected it, because it scored worse.

**Concede:** The forest is harder to interpret, which is exactly why slide 12 exists — we had to do extra work
(summing dummies back per variable, and block permutation) to say anything about which variables matter.

---

## 5. Why did we choose to report 20 authorities when 65 were flagged?

**Say:** Because the 65 is fragile and the 20 is not. The flagging rule is all-or-nothing — every one of an
authority's results has to point the same way — so a single mixed result drops a town off the list.

**If pushed:** Dropping the two smallest rows in the whole dataset moves eight of the 65 on or off. The 20 are
the towns still flagged after all seven rebuilds of the analysis, including ones that change the model family
and the year window. Across every rebuild, the "changed direction" column is zero: no authority ever flipped
from above prediction to below.

**Concede:** 20 is a small list to build conclusions on, and it is not a random sample of anything — it is
whoever survived our particular robustness test.

---

# Detail

## 6. Why did we choose to one-hot encode subject and sector during cleaning, when grade and year are encoded inside the pipeline?

**Say:** Because subject and sector are also the things we group by throughout the analysis — the score
distributions, the gap standardization, the clustering profile, the High/Low threshold. Encoding them early
means the indicator columns exist everywhere they are needed, and the models get a consistent set of columns.

**If pushed:** Grade and year are encoded inside the `ColumnTransformer` with `handle_unknown="ignore"`, which
is the safer pattern: a fold that happens to be missing a category still produces aligned columns. Subject and
sector do not have that risk here — every subject and every sector appears in every fold — and `drop_first`
for the linear and logistic models is handled by selecting a subset of the indicator columns, so it means the
same thing it would have meant inside the pipeline.

**Concede:** Encoding before the split does fix the category set from the whole dataset, so it is the less
defensive choice of the two. We keep it where the risk is zero and use the pipeline where it is not.

> Related, if they notice the columns: `subject_id` and `norm_id` are **dropped** after encoding. Exactly one
> indicator is 1 in every row, so the label is always recoverable, and `group_key()` is the one helper that
> recovers it. Keeping both forms would have been duplicate state.

---

## 7. Why did we choose to stratify the split by socio-economic cluster?

**Say:** Because the clusters are very unevenly sized and the split is over authorities, not rows. Cluster 1
holds 9 authorities and cluster 10 holds 4. A plain grouped split can easily put all four cluster-10 towns in
one set, and then we would be testing on a kind of town the model never saw.

**If pushed:** We checked instead of guessing: repeating the unstratified grouped split over 1,000 seeds, at
least one set is missing a cluster entirely in 688 of them — 69%, almost always cluster 10 or cluster 1. We
draw the 50/20/30 inside each cluster and combine the parts.

**Concede:** Stratifying by cluster does not guarantee balance on anything else — sector, authority type or
size could still land unevenly, and we did not stratify on those.

---

## 8. Why did we choose to standardize the gaps within subject and grade before averaging them per authority?

**Say:** Because the tests are not on a common scale. The spread of residuals runs from 18.5 points in Hebrew
grade 5 to 34.0 in Science grade 8. Averaging raw residuals would let the noisiest test dominate an
authority's gap, so a town would look extreme mainly because of which exams it happened to sit.

**If pushed:** We z-score within each subject × grade, so a gap of 1.0 means one standard deviation better
than predicted *for that test*, roughly 26 score points. It also makes the consistency rule meaningful: "all
rows point the same way" only compares like with like once the scales match.

**Concede:** Standardizing hides absolute size. A town one SD above prediction in Hebrew grade 5 has beaten it
by fewer points than one SD in Science grade 8, and our headline number does not show that.

---

## 9. Why did we choose block permutation when we already had per-variable permutation importance?

**Say:** Because per-variable permutation answers the wrong question when predictors are near-duplicates.
`ses_index` correlates above 0.8 with eight CBS variables, so shuffling it alone barely hurts — the other
fifteen rebuild it. It ranks ninth at 0.011, which reads as "socio-economic standing barely matters" and is
not true.

**If pushed:** Shuffling the whole socio-economic block at once costs 0.374 of R², against 0.609 for the block
that says which test a row is. Both numbers are correct and they say different things: no single
socio-economic variable is irreplaceable, but the information collectively is substantial. Reporting only the
first would have answered the proposal's question wrongly.

**Concede:** Block permutation is not something the course taught — per-variable permutation is, one feature
at a time. We added it because the wider predictor set created the collinearity that made the taught version
uninformative, and we report both rather than replacing one with the other.

---

## 10. Why did we choose the combined-sector row for mixed authorities, instead of the separate sector rows?

**Say:** Because the file contains both, and keeping both counts the same pupils twice. For the 19 authorities
with Hebrew and Arabic schools there is a combined row plus the two sector rows, and the combined row is the
two added together — Haifa, grade 5 English, 2016: 859 = 768 + 91. Left alone, the biggest cities enter every
average at double weight.

**If pushed:** We chose authority totals because the question is asked about authorities, so one row per
authority per test is the matching grain. The alternative is a real choice, not an obvious error, so slide 13
rebuilds everything on sector rows instead: 1,826 rows, R² 0.515, 53 flagged, and 52 of our 65 kept — the
finding holds, with fewer towns.

**Concede:** Averaging the two sectors into one number hides any gap *between* them inside a mixed authority,
and `sector` then becomes an authority-type marker rather than a true sector variable.

---

## Also worth rehearsing

Three more in the same form, if there is time: **why k = 10** for the clustering (to compare like with like
against the official ten bands, with k = 2 as a coarse check), **why `rashut` is not a feature** (243 values
would let the model memorise the very identity the grouped split exists to remove), and **why median
imputation inside the pipeline** (three authorities have suppressed CBS values, and fitting the median inside
each fold keeps the held-out part out of it).
