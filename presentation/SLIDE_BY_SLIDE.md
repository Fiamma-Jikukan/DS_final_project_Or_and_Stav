# Presentation, slide by slide

A speaking aid for `Presentation_Or_and_Stav.pptx`. Everything here is deliberately worded **differently from
the slides** and in plainer language, so you can look at an element and say it out loud in your own words
instead of reading the screen.

Each slide gets one line on what it is for, then a bullet per thing on the slide. Numbers are exact — those
have to stay right.

13 slides: **1 to 11 are spoken** (about 9 minutes), **12 and 13 are backup** for questions. The Fig and Table
numbers are the same as in the notebook, so any question can be traced back to the cell that made it.

---

## Slide 1 — Title

**One line:** Who we are, what we asked, and which two files we used.

- **"Beyond the Cluster"** — the name plays on the official 1-to-10 ranking. Our point is that the ranking
  leaves something out.
- **Subtitle** — the question, in one sentence.
- **Ten shaded squares** — a picture of the official ranking, light to dark. It comes back on later slides, so
  introducing it here saves explaining it twice.
- **Caption under the squares** — tells the room what the squares are, so nobody spends the next slide
  wondering.
- **Names, IDs, course** — Stav Tchizik (316062835), Or Cohen (206631509).
- **Bottom line** — says which two files and which years. The year range is a decision we defend on slide 4,
  so it is worth putting on screen early.

---

## Slide 2 — Why ask this at the authority level

**One line:** Why the town is the right unit to study, and why nobody has answered our version of the question.

- **Point 1 — money moves by authority** — school budgets and programmes in Israel are decided per town. If a
  finding cannot be acted on by somebody, it is not useful; towns are who acts.
- **Point 2 — the easy finding already exists** — RAMA already sends every town a report comparing it to
  similar towns. Showing again that wealthier places score higher would be repeating published work.
- **Point 3 — nobody lists the exceptions** — our question is who breaks the pattern, how reliably, and
  whether anything explains it.
- **"What this project adds" strip** — one sentence on the contribution: a ranked list of the exceptions, plus
  a check on what separates them.
- **"Who the answer is for"** — three readers who could act on it. Keeps the project a policy question rather
  than a curiosity.
- **Stat "243"** — how many towns we ended up with, and how many rows they produced. Scale, before any result.
- **Stat "2 sources"** — two files that do not share an ID, so we had to build the link ourselves. Slide 4
  shows how.

---

## Slide 3 — The question

**One line:** The question, the two things that have to be settled first, and a warning about the word "cause".

- **Big question box** — the whole project in one sentence. Everything after this answers a piece of it.
- **Supporting question 1 — how well does wealth predict scores?** — we cannot call a town "better than
  expected" until we have a prediction worth trusting. This is that prediction.
- **Supporting question 2 — would grouping towns by results give the official ranking back?** — if yes, the
  official numbers already contain everything and there is nothing to add. Slide 7 settles it.
- **Line at the bottom** — we only ever say two things move together, never that one causes the other. The
  data are a snapshot of towns nobody assigned to anything, so cause is out of reach. Saying it once here
  keeps the rest of the talk readable.

---

## Slide 4 — Two official sources, and the work to join them

**One line:** What is in each file, and the three messes we had to clean before anything could be measured.

- **Left card, the test data** — national exams in grades 5 and 8, five subjects. One line per town, year,
  school system, grade and subject.
- **Right card, the wealth index** — one score per town, built by CBS from 14 background measures, given both
  as a number and as a 1-to-10 band.
- **Mess 1 — two different ID systems** — the two files number towns differently. Usually one file's code is the
  other's with an extra digit on the end; regional councils follow another rule; four
  towns that merged we matched by hand. Everything matched in the end, and we checked by comparing names.
- **Mess 2 — some pupils counted twice** — towns with both Hebrew and Arabic schools get three lines: each
  system separately, plus a combined line. Keeping all three counts those pupils twice and makes big cities
  weigh double in every average. We keep one line per town. The Haifa figures on the slide show the combined
  line really is the two parts added up.
- **Mess 3 — years that do not match the index** — the wealth index is a 2017 edition. We keep the three
  nearest years and drop 2015 and 2019 rather than compare a 2019 score to 2017 circumstances. Scores still
  creep upward across the kept years, so the year is given to the model as a variable.
- **Bottom line** — how many rows and towns survived, and why 44 rows have no score at all: the Ministry hides
  results for very small groups of pupils.

---

## Slide 5 — How the analysis is built

**One line:** The whole method in five boxes, plus the one decision that changes every number we report.

- **The five boxes** — read left to right, this is the order things happen in.
  - *Split by authority* — a town is never half in training and half in testing.
  - *Baselines* — two dumb predictors to beat, so a score has something to be compared against.
  - *Two model tracks* — we predict the score, and separately predict a simple above/below label, so the
    finding is checked twice by different means.
  - *Out-of-fold gaps* — every town is judged by a model that was trained without it.
  - *Clustering* — group towns by their results, and separately by their gaps.
- **"Why split by authority, and what it cost"** — we have 1,749 rows but only 243 towns, so the same town turns up
  again and again. If we split rows at random, almost every town appears on both sides, and the model can score
  well just by remembering a town's own average — worth R² = 0.30 on its own, with no background data at all.
  Splitting whole towns kills that, and the same rule is applied inside the tuning folds.
- **"Set-up at a glance"** — the reproducibility details, parked in a box so they do not have to be said out
  loud: feature count, split sizes, tuning, libraries, seed.
- **Stat "R² = 0.30"** — the size of the cheat we removed.
- **Stat "0 of 74"** — proof it is gone: none of the towns we tested on had been seen before.
- **Stat "R² = 0.530"** — what the model actually achieves on towns it has never met, next to 0.281 for
  guessing the subject-and-grade average. The honest headline.

> **If asked about "stratified by cluster":** we draw the split inside each of the ten wealth bands separately
> and then put the pieces together, so all ten bands show up in all three sets. Without it, the smallest bands
> (9 and 4 towns) go missing from a set about two thirds of the time, and we would be testing on a kind of
> town the model never saw.

---

## Slide 6 — Deviation does not follow socio-economic standing

**One line:** First real result — being rich or poor tells you nothing about whether a town beats its own
prediction.

- **Fig 8** — one dot per town: wealth across the bottom, gap up the side. The dots form a flat band, and the
  named towns at the top and bottom come from all along the wealth range.
- **Line under the figure** — the sentence this slide exists to say.
- **Stat "r = 0.011"** — the correlation between a town's gap and its wealth. Zero for practical purposes.
- **Stat "65 of 238"** — towns whose every single result points the same way. Careful here: this counts
  *consistency*, not size. A town qualifies when it is above prediction in all of its subjects, or below in
  all of them, never mixed. The other 173 are the mixed ones, which is what random noise looks like.
- **Stat "20"** — how many of those 65 are still there after we rebuild the analysis seven different ways.
  Previews slide 9.
- **Method note** — what a gap is and what it is worth: one unit is one standard deviation, roughly 26 points
  on the test.

---

## Slide 7 — The official clusters are not interchangeable

**One line:** Grouping towns by their results does not give you the official wealth ranking back.

- **Fig 10** — a grid: our groups down the side, official bands across the top.
  - *"Achievement group" means our own grouping*: we let K-Means sort the 223 towns into ten groups using
    their three grade-8 subject scores, then renumber the groups worst to best so they line up against the
    official 1-to-10 scale.
  - *Every square is a head count of towns.* Row 3, column 5 showing 7 means seven towns that our grouping put
    in group 3 are in official band 5. Blank means nobody, darker means more, and all the squares add to 223.
  - *What to look for*: if the two systems were the same thing, everything would sit on the diagonal. It does
    not.
- **Stat "1.54 clusters"** — on average a town sits one and a half bands away from where its results put it.
  Shuffling the labels at random would give 2.70, so the two are related but clearly not the same.
- **Stat "55 of 223"** — how many land on the exact same number, and how many are miles off. Same story said a
  second way.
- **"The same test on the gaps"** — repeating the exercise on gaps instead of scores gives almost exactly the
  shuffled number. That is a good sign, not a disappointment: gaps were built to have the wealth effect
  removed, so finding no wealth pattern means the construction worked.
- **Note about regional councils** — most of the worst mismatches are councils that lump several villages into
  one number, so their single figure describes nobody in particular. A data-shape explanation, not a
  performance one.

---

## Slide 8 — Deviation is not the same in every subject

**One line:** A town is not simply "good" or "bad" against prediction — it can be ahead in one subject and
behind in another.

- **Fig 11** — each line is a group of towns; the three points on a line are its average gap in English,
  Mathematics and Science. A sloping line means the group's result depends on the subject; a level line means
  it is the same across all three.
  - *These groups come from the gaps, not the scores.* It is a second, separate K-Means run on the same 223
    towns, so group 4 here has nothing to do with group 4 on slide 7.
  - *Numbered worst to best*, which here means most-below-prediction first.
- **Line under the figure** — the point in four words.
- **Stat "15"** — the size of group 4: ahead in English, behind in the other two, with a wide spread between
  them. Group 5 is the same picture flipped.
- **Stat "6 of 10"** — most groups slope rather than sit level. And when we ask for only two groups, both come
  out level — so this only shows up if you look closely enough. Worth saying out loud; it is the honest
  version.
- **Why it matters card** — the practical reading: a town behind in Mathematics but ahead in English needs a
  different response from one behind in everything. Averaging a town into a single number would have hidden
  that completely.

---

## Slide 9 — The twenty authorities that survive everything

**One line:** The actual list of names, and why it is twenty rather than sixty-five.

- **Left table, 13 towns above prediction** — name, official band, and how far above, biggest first.
- **Right table, 7 towns below prediction** — same three columns.
- **"Why twenty and not sixty-five"** — the rule for the 65 demands that every one of a town's results points
  the same way, so a single mixed result drops a town off the list. Drop just the two tiniest results in the whole
  dataset and eight towns move. That is too fragile to put a name to. The 20 are the ones that stay flagged
  however we rebuild the analysis, so those are the names we are willing to say in public.
- **"Both lists mix sectors, clusters and authority types"** — the lists are not all Arab towns, not all poor
  towns, not all one type. Nothing we measured tells the two lists apart, and that is both the result and its
  limit.
- **Small print** — what the gap column means, and where the full ranking of all 243 towns lives.

---

## Slide 10 — What we can say

**One line:** The four claims we are prepared to defend. Dark background because this is where evidence turns
into conclusions.

- **Claim 1 — roughly half of a town's score is predictable** — the model explains about half the variation in
  towns it has never seen, well above the simple baseline. The known wealth pattern is there, strong in
  English grade 8 and nearly absent in Arabic grade 5.
- **Claim 2 — which exam it is matters more than who is sitting it** — our proposal asked whether a town's
  background beats grade and subject. It does not: scramble the columns saying which exam a row is and the
  model loses far more than when every background column is scrambled at once. Say the question out loud
  before the answer, or "no" hangs in the air. And both losses are big — background comes second of two, not
  nowhere.
- **Claim 3 — twenty towns deviate dependably, and none ever switches side** — 65 under the original rules, 20
  across every rebuild, and in no rebuild did any town flip from above to below. This is the strongest thing
  we can say.
- **Claim 4 — we cannot explain why** — we checked 22 variables, including six the model never used, and the
  best relationship with a town's gap is very weak. Whatever is going on is probably inside schools, and
  neither file can see inside schools. A negative result, reported as a result.

---

## Slide 11 — What this cannot say

**One line:** The limits, said by us before anybody in the room says them.

- **The ecological fallacy box** — every number describes a town, not a child. A town being above prediction
  does not mean its pupils are; it contains good and bad results we never see apart. Patterns between town
  averages also look stronger than the same patterns between individual people, so our correlations overstate
  what is true of any one pupil.
- **"No causality"** — a snapshot of towns nobody assigned to anything. Things that could be behind the
  pattern and that we cannot rule out: which school system, where the town is, how schools are funded.
- **"What the grouped split cost"** — splitting by row would have produced a better-looking score, but a third
  of it would have been memorisation. We publish the smaller, real number.
- **"Coverage and years"** — the smallest towns are missing, because their results are withheld. And most
  towns appear in one year only, so we can check year-to-year steadiness for just 28 of them.
- **"A sharp threshold"** — three towns have a filled-in background value, and the flagging rule is
  all-or-nothing, which is exactly why we report the 20 and not the 65.
- **"What we would do differently"** — data at school or pupil level to get under the averaging problem, a
  proper multi-year panel, and location variables we simply do not have.

---

## Slide 12 — Backup: which variables carry the model

**Not presented.** Keep for: "so does wealth matter or not?"

- **Fig 13** — two rankings of the same variables side by side: what the model falls apart without, and what
  it used while growing. `subject` and `sector` on the chart are stand-ins for several 0/1 columns added back
  together, not real columns.
- **Headline text** — knowing the subject is worth far more than anything else; the wealth index on its own
  lands ninth.
- **Table 10** — the fair comparison: whole groups of variables removed at once rather than one at a time.
- **"Why both numbers are needed"** — the wealth index has eight near-twins in the data. Take it away alone
  and the twins cover for it, so it looks worthless; take the whole family away and the damage is large. Both
  numbers are true, and quoting only the first would have misled the room.

---

## Slide 13 — Backup: every rebuild of the pipeline

**Not presented.** Keep for: "would you get the same answer if you had done it differently?"

- **Table 11** — seven complete reruns from the raw files, one per row, each changing a single decision.
  - *Separate school systems instead of one line per town* — tests the double-counting fix from slide 4.
  - *All five years* — tests the year window.
  - *Drop groups under 30, and under 50, pupils* — tests the small-group cut-off, twice.
  - *Bands instead of the continuous index* — tests how wealth is fed in.
  - *Plain linear model instead of the forest* — tests whether the model type matters.
- **"The last column is zero on every row"** — the thing to point at. Nothing we changed ever turned a town
  from above-prediction to below. Everything else wobbles: swapping the wealth measure barely matters, the
  cleaning choices cost a few towns each, and widening the years has the biggest effect by far — that leaves
  only 38, purely because extra years give each town extra results, and all of them have to agree.

---

# Glossary

Plain-language meaning of every term that comes up, in the sense this project uses it.

## The data

- **Meitzav** — the national exams these scores come from, sat in grades 5 and 8.
- **RAMA** — the Ministry of Education body that runs those exams and publishes per-town reports.
- **CBS** — the Central Bureau of Statistics, who publish the wealth index.
- **Socio-economic index** — one number summarising how well-off a town is, built by CBS from 14 background
  measures. Comes as a number and as a 1-to-10 band.
- **Factor analysis** — the statistical trick CBS uses to squash 14 measures into one. We use the result, we
  do not redo it.
- **Cluster / band (1 to 10)** — the official wealth grouping, 1 poorest to 10 richest. The ten squares on the
  title slide. Not the same thing as our K-Means groups.
- **Local authority** — a town, village council or regional council. Our unit throughout.
- **Regional council** — an authority covering several separate communities, so one number describes a mixture
  of places.
- **Mixed authority** — a town with both Hebrew and Arabic school systems. There are 19.
- **Sector** — which school system: Hebrew, Arabic, or both reported together.
- **Suppressed result** — a score the Ministry withholds because too few pupils sat it, usually under 30.

## Rows and columns

- **Row** — one town, in one year, one school system, one grade, one subject. 1,749 of them.
- **Grain** — what one row stands for. Fixing the grain is the slide-4 double-counting problem.
- **`rashut`** — the town's code. Deliberately kept out of the models: with 243 values a model could use it to
  memorise instead of learn.
- **`shichva`** — grade, 5 or 8.
- **`norm_id` / `subject_id`** — the raw codes for school system and subject. Turned into 0/1 columns during
  cleaning and then removed from the table.
- **0/1 column (indicator, dummy)** — a column that is 1 when a row is that category and 0 otherwise, e.g.
  `subject_math`.
- **One-hot encoding** — replacing a category with one 0/1 column per value, so the model cannot read the
  codes as a size order.
- **`group_key()`** — the helper that rebuilds the (subject, grade) label from those 0/1 columns, used
  wherever the notebook groups results.
- **Feature** — a column the model is allowed to see. We use 20.
- **Target** — the thing being predicted: the score, or the above/below label.

## Splitting and checking

- **Train / validation / test** — three piles: one to learn from, one to choose between models with, one
  touched only at the very end.
- **Grouped split** — whole towns go to one pile, never split across piles.
- **Stratified by cluster** — the split is made inside each wealth band and then combined, so no band goes
  missing from a pile.
- **Cross-validation** — fitting repeatedly on most of the data and checking on the part left out.
- **`GroupKFold`** — cross-validation that keeps each town inside one fold, for the same reason as the grouped
  split.
- **Out-of-fold prediction** — a town's prediction made by a model trained without it. This is what makes a
  gap mean anything.
- **Leakage** — when the model gets a peek at the answer. Ours would have been town identity.
- **Seed** — a fixed number (42) that makes every random step repeat identically.

## Models

- **Baseline** — a deliberately stupid predictor to beat: the overall average, and the average of that subject
  and grade.
- **Linear regression** — the simple, straight-line model.
- **Random forest** — the main model: hundreds of decision trees averaged together.
- **The chosen forest** — the one configuration we settled on and used for everything afterwards: forest
  rather than linear, unweighted rather than weighted, with the tuned settings.
- **Logistic regression** — the simple model for the above/below question.
- **High / Low label** — above or below the training median of the row's own subject and grade.
- **Hyperparameter** — a setting chosen before training, not learned from the data.
- **`GridSearchCV`** — trying every combination on a list of settings and keeping the best by
  cross-validation. We tried 27.
- **Trees / depth / leaf size / features per split** — the forest's four settings: 400 trees, no depth limit,
  leaves as small as one row, and a random handful of features considered at each split.
- **Sample weighting** — letting bigger pupil groups count for more. Tried; it made things worse, so it was
  dropped.
- **Median imputation** — filling a missing background value with the middle value of that column, done inside
  the pipeline so it only ever learns from the training part.
- **Pipeline** — encoding, filling, scaling and the model bundled as one unit, so every step is refitted
  inside each fold.

## Scores

- **R²** — how much of the variation the model explains. 0 is no better than always guessing the average, 1 is
  perfect, and it can go below 0.
- **RMSE** — typical error in test points, with big misses punished harder.
- **MAE** — typical error in test points, plainly averaged.
- **r** — how tightly two things move together, from −1 to +1.
- **Residual** — actual minus predicted, in test points.

## Gaps and the list

- **Gap** — how far a result sits above or below its prediction, rescaled so a gap means the same in every
  subject and grade. Positive is above.
- **Standardizing (z-score)** — subtracting the average and dividing by the spread, so different tests become
  comparable.
- **Standard deviation (SD)** — the unit gaps are in. One SD is about 26 test points.
- **Consistent** — all of a town's results point the same way, never mixed.
- **Flagged** — a town with at least two results, all pointing the same way: 65 of them.
- **Eligible** — towns with enough results to be testable at all: 238 of 243.
- **The 65 / the 20** — the consistent towns under the original rules, and the ones that stay consistent under
  every rebuild.
- **Rebuild** — running the whole analysis again from the raw files with one decision changed. Seven in all.
- **Changed direction** — a town switching from above-prediction to below between rebuilds. It never happened.

## Grouping towns

- **K-Means** — an algorithm that sorts items into a chosen number of groups by similarity.
- **k** — how many groups we ask for. We use 10, to compare against the official ten bands, and 2 as a coarse
  check.
- **Profile** — the three grade-8 subjects used to describe each town for grouping: scores for one run, gaps
  for the other.
- **Achievement group** — a group built from scores (slide 7).
- **Gap group** — a group built from gaps (slide 8). Separate run, so the numbers do not match slide 7's.
- **Group centre** — the group's average profile; one line in Fig 11.
- **Spread** — a group's highest subject average minus its lowest. Above 0.5 we call the group tilted.
- **Tilted vs level** — tilted means the group's gap depends on the subject; level means it is the same in
  all three.

## Which variables matter

- **Permutation importance** — scramble one variable and see how much worse the model gets. Shows what it
  really leans on.
- **Impurity importance** — the forest's own built-in measure, taken from how useful each variable was while
  the trees were grown.
- **Block permutation** — scrambling a whole family of related variables at once, because scrambling one of
  eight near-identical variables proves nothing.
- **Collinearity** — several variables carrying the same information, which is why the wealth index looks
  worthless alone and substantial as a group.
- **Test identity** — the four variables saying which exam a row is: subject, grade, school system, year.

## Caveats

- **Association, not cause** — we can show two things move together; we cannot show one makes the other
  happen.
- **Observational** — nobody was assigned to anything; we are reading records that already existed.
- **Cross-sectional** — a snapshot, not the same towns followed over time.
- **Confounder** — something we did not measure that could be producing the pattern we see.
- **Ecological fallacy** — treating a fact about a group as a fact about its members. A town above prediction
  does not mean its pupils are.
- **Aggregation effect** — relationships between averages look stronger than the same relationships between
  individuals.
