**# AI usage statement

Required by §5 of the project instructions.

## Which tool

**Claude (used through Claude Code)**, a single assistant across the whole project.

## What it was used for

- **Writing the analysis code.** Each section of the notebook was produced from one of the prompts below.
- **Checking the data.** Reading the two source files to establish facts the proposal had not pinned down: the
  authority-code mapping rule, the duplicate sector rows, and how complete the subject coverage is.
- **Drafting prose.** The markdown cells that explain each figure and table, and the Background and Discussion.

## The prompts

One per section, in the order the notebook runs.

## 1. Exploratory Data Analysis and Data Cleaning

**Loading the two files**

> load two files: a csv of ministry of education test scores (meitzav), one row per authority, year, grade and
> subject, and a cbs excel file with the 2017 socio-economic index. the excel header runs over several rows in
> hebrew and english, real data starts at row 10, the last 5 rows are footnotes, and two rows near the top are
> national averages, so drop all of those and give the columns proper english names. set a random seed of 42 to
> use everywhere. print a summary of both files: rows, columns, years, number of authorities.

**Restricting the years**

> keep only 2016–2018 in the education data, since our socio-economic index is the 2017 one and we don't want
> to compare scores to an index measured years off. print rows and authorities before and after, and check
> whether the average score moves much between the three years, if it does we should keep year as a variable
> later.

**One row per authority, year, grade and subject**

> `norm_id` is the education sector: 3 is hebrew-language schools, 9 is arabic-language, and 1 is the two
> combined — but the 1 rows only exist for the 19 authorities that have both sectors. so those authorities are
> currently counted twice, once as a total and once per sector: haifa's grade 5 english total of 664 students
> tested is just 537 + 127 from the two sectors. check that on a couple of authorities, then build one row per
> authority, year, grade and subject by taking the `norm_id = 1` row where it exists and the single sector row
> everywhere else. print rows and authorities left.

**Joining the two datasets**

> the two files number authorities differently so i need to build the merge key. for cities and local councils
> the education code is the cbs code with an extra digit on the end, so dividing by 10 gives the cbs code
> (ofakim is 315 vs 31). regional councils have no locality code in the cbs file, their council number is in
> the municipal status column, and their education code is that number times 100,000. set up both rules, then
> fix four merged cities by hand: 13508→195, 13516→1200, 13524→9800, 13573→9400. then verify: fail if any
> education authority didn't match, print the ones that didn't, compare names on both sides to catch wrong
> matches, and tell me how many cbs authorities have no education data.

**Cleaning the merged table**

> clean the merged table. first, the merge creates its own gaps, so tell me which education authorities found no
> cbs match and which cbs authorities have no education data, then drop what we can't use. second, 28 of the 50
> cbs columns are just standardised (_z) and rank copies of the same 14 variables, so keep the raw values, the
> continuous index for models and the 1 to 10 cluster for grouping. last, check the missing rate per column on
> the merged table, not the raw file, since we analyse only a subset of the 255 authorities, flag anything over
> 40%, and say whether the missing values concentrate in particular clusters, which would bias our comparison.

**Exploring the data** — the last sentence of this prompt produced the two figures that now sit in section 2.

> explore the merged data. show the score distribution overall and by subject and grade, since they sit at
> different levels and that matters for how we label high/low later. plot score against number of students
> tested and tell me how many rows have under 20, 30 and 50, small cells are noisy. check whether the rows with
> no score are mostly small samples or one sector, then drop them. then show score by socio-economic cluster
> split by subject and grade, score against the continuous index value, and a correlation heatmap of the cbs
> variables.

---

## 3. Data Splitting

> split into train, validation and test by authority, not by row. the cleaned table has 1,749 rows from only
> 243 authorities, so if an authority lands in both train and test the model can memorise its average score and
> accuracy looks better than it is. use `GroupShuffleSplit` with authority as the group, roughly 50/30/20, and
> `GroupKFold` by authority for tuning later. cluster 10 has only 4 authorities and cluster 1 has 9, so a plain
> split can leave a cluster out of a set, stratify by cluster if you can. rows per authority run from 1 to 25,
> so print each set size in rows, authorities and clusters, and fail if an authority turns up in two sets. also
> run a plain row split once so we can show the difference.

---

## 4.1 Regression

> build models to predict an authority's average score. start with two baselines so we know what counts as
> doing well: always guess the overall average, and guess the average for that subject and grade. then fit a
> linear regression and a random forest using the socio-economic index plus the other cbs variables, grade,
> subject, sector and year. keep the scaling inside a pipeline so it only learns from training data. tune the
> forest with `GroupKFold` by authority. weight rows by students tested, since a row from 1,000 students is
> better evidence than one from 20, and show results with and without weighting. compare on validation only and
> use the test set once at the end. give me r², rmse, mae and residual plots.

## 4.2 Classification

> turn the score into a high/low label, worked out within each subject and grade: above its own group's median
> is high. one overall median would just encode which subject the row is, so the classifier would learn the
> subject instead of anything socio-economic. show a crosstab of that naive label against subject and grade to
> demonstrate it. compute the medians on the training set only, otherwise the label leaks. then train a logistic
> regression and a random forest, reusing the same split, features and `make_pipeline` helper from the
> regression, against a majority-class baseline. no sample weighting, we tested it earlier and it made things
> worse. give me accuracy, precision, recall, f1 and a confusion matrix.

## 4.3 Over- and under-performing authorities

> the main part, using the unweighted forest we chose. first get an honest gap for every authority:
> `cross_val_predict` with `GroupKFold` on rashut across all 243, so each authority is predicted by a model that
> never saw it. standardize the gaps within subject and grade before averaging, since the residual sd runs from
> 17 to 38 points depending on the test. average per authority and report the consistency of sign across its
> rows. only call an authority an over or under-performer if every one of its rows falls on the same side of its
> prediction, and skip the 5 authorities with a single row. most authorities appear in one year only, so
> consistency is across subjects and grades, not years. then plot the index against the mean standardized gap
> with the extremes labelled, correlate the gap against each of the cbs variables and against a few the model
> never saw (school count, school size, cohort size, response rate), and check the lists hold with the linear
> model's gaps.

---

## 5. Unsupervised Learning: Clustering

> group the authorities by how they score, without using the socio-economic index, so we can compare our groups
> to the official ones. build one row per authority from grade 8 english, math and science only: those three are
> taught in both sectors and 223 of the 243 authorities have all three. don't use arabic or hebrew, since arabic
> only exists in arabic-language authorities and hebrew only in hebrew-language ones, so including either would
> just make the clusters rediscover the sector. standardize each of the three columns first, their levels are
> about 517, 536 and 574. run k-means, pick k with an elbow plot and silhouette, and also run k=10 to line up
> against the official 1 to 10 clusters. compare the two with a crosstab heatmap and the average distance
> between the two cluster numbers, against a shuffled baseline. then do the same clustering on the gaps instead
> of the raw scores, since those are already net of socio-economic level, and tell me which version separates
> the 65 flagged authorities better.

---

## 6. Feature Importance

> show which variables matter most in the forest: built-in importance and permutation importance side by side,
> since the built-in one favours continuous variables. sum the one-hot dummies back per variable first. add the
> standardised logistic coefficients too. then permute the 16 socio-economic variables as one block against the
> 4 test-identity ones, since they're too correlated to permute one at a time.

---

## 7. Robustness

> re-run the analysis under each of these and put it in one table: sector rows vs combined totals, 2015–2019 vs
> 2016–2018, small-cell cutoff 30 vs 50, and ses_index vs ses_cluster. the split, the weighting and the
> forest-vs-linear gap comparison are already computed earlier, so just collect those numbers into the same
> table. for each one give me the main metric and how many of the 65 over and under-performers change.

---

## Responsibility

Everything submitted was read, run and checked. Where the assistant's output was wrong it was corrected.
