# Presentation

`Presentation_Or_and_Stav.pptx` — 13 slides, 16:9, no speaker notes.

Slides 1 to 11 are the talk, about 9 minutes at the pace below, which leaves margin
inside the 10-minute limit. Slides 12 and 13 are backup, for questions only.

| # | Slide | Target |
| --- | --- | --- |
| 1 | Beyond the Cluster (title) | 20s |
| 2 | Why ask this at the authority level | 40s |
| 3 | The question | 35s |
| 4 | Two official sources, and the work to join them | 40s |
| 5 | How the analysis is built | 55s |
| 6 | Deviation does not follow socio-economic standing (Fig 8) | 80s |
| 7 | The official clusters are not interchangeable (Fig 10) | 45s |
| 8 | Deviation is not the same in every subject (Fig 11) | 45s |
| 9 | The twenty authorities that survive everything | 40s |
| 10 | What we can say | 80s |
| 11 | What this cannot say | 50s |
| 12 | Backup: which variables carry the model (Fig 13, Table 10) | — |
| 13 | Backup: every rebuild of the pipeline (Table 11) | — |

Slide 6 is the lead result and slide 10 is the close; those two carry the talk. Slide 11
has to name the ecological fallacy out loud, since that was correction 3 in the feedback.

## Figures

`make_figures.py` re-runs the notebook's pipeline and redraws the four deck figures at
**the exact size they occupy on the slide**, so the point sizes in that script are the
point sizes the audience sees. They differ from the notebook's versions in three ways:

- no in-figure title, because the slide carries a caption
- **Fig 10** shows the achievement-score panel only. The gap panel is a null result by
  construction, so it is quoted as a number on the slide instead
- **Fig 11** labels group 4 and group 5 on the lines rather than in a legend, and names
  the subjects on the x axis instead of showing `(2, 8)` style codes

```
python presentation/make_figures.py          # ~4 minutes, re-runs the pipeline
python presentation/make_figures.py --cached # seconds, reuses the last run
python presentation/build_deck.py            # rebuilds the .pptx
```

`make_figures.py` writes nothing except the four PNGs and a cache file in the system temp
directory. It does re-execute the notebook's export cells, which rewrite the files in
`data/` with byte-identical content.

## Before the slot

- Open it once in PowerPoint. The layout was checked by measurement and by rendering the
  slides here, but font metrics on the presenting machine are the real test
- Rehearse to 10 minutes and check the figures from the back of the room
- Both partners need to be able to defend every choice. The Q&A list is Appendix A of
  `helper docs/PROJECT_PLAN.md`
- Every number on the slides comes from the notebook's printed output. If the notebook
  changes, the slide text has to be changed by hand
