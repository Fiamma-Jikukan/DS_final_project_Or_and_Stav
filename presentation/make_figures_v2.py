"""Redraw the two EDA figures the v2 deck needs, at the size they occupy on the slide.

Only the loading, cleaning and EDA cells are replayed (no models), so this runs in seconds.
The four figures the v2 deck shares with deck 1 (fig08, fig10, fig11, fig13) come from
make_figures.py and are not rebuilt here.
"""
import builtins
import io
import json
import sys
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT = Path(r"C:\Users\User\PycharmProjects\DS_final_project_Or_and_Stav")
OUT = PROJECT / "presentation" / "figures"
NB = PROJECT / "DS_final_project_Or_and_Stav.ipynb"
LAST_CELL = 56           # through the EDA and the correlation scatter; no model fitting

warnings.filterwarnings("ignore")
plt.show = lambda *a, **k: None
builtins.display = lambda *a, **k: None

import os
os.chdir(PROJECT)

ns = {"__name__": "__main__", "display": builtins.display}
cells = json.loads(io.open(NB, encoding="utf-8").read())["cells"]
for i, cell in enumerate(cells[:LAST_CELL + 1]):
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell["source"])
    if not src.strip():
        continue
    try:
        exec(compile(src, f"<cell {i}>", "exec"), ns)
    except Exception as exc:
        print(f"cell {i} failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
    plt.close("all")
print("pipeline ran to cell", LAST_CELL)

data, GROUPS = ns["data"], ns["GROUPS"]
GROUP_LABELS, BOX_STYLE, rows_of = ns["GROUP_LABELS"], ns["BOX_STYLE"], ns["rows_of"]
INK, INK_MUTED, SURFACE, BLUE = ns["INK"], ns["INK_MUTED"], ns["SURFACE"], ns["BLUE"]

plt.rcParams.update({
    "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8,
    "figure.dpi": 200, "savefig.dpi": 200,
})


def save(fig, name):
    path = OUT / name
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)


# ------------------------------------------------------------------ Fig 1
fig, (ax_all, ax_grp) = plt.subplots(1, 2, figsize=(7.5, 3.3),
                                     gridspec_kw={"width_ratios": [1, 1.45]})
overall_median = data["score"].median()

ax_all.hist(data["score"], bins=40, color=BLUE, edgecolor=SURFACE, linewidth=0.5)
ax_all.axvline(overall_median, color=INK_MUTED, linestyle="--", linewidth=1)
ax_all.annotate(f"median {overall_median:.0f}", (overall_median, 1),
                xycoords=("data", "axes fraction"), xytext=(4, -4),
                textcoords="offset points", va="top", color=INK_MUTED, fontsize=8)
ax_all.set(title="All rows", xlabel="Mean score", ylabel="Rows")

ax_grp.boxplot([rows_of(s, g)["score"] for s, g in GROUPS], orientation="horizontal",
               tick_labels=[GROUP_LABELS[k] for k in GROUPS], widths=0.55, **BOX_STYLE)
ax_grp.invert_yaxis()
ax_grp.axvline(overall_median, color=INK_MUTED, linestyle="--", linewidth=1)
ax_grp.set(title="By subject \u00d7 grade (dashed: overall median)", xlabel="Mean score")
ax_grp.grid(axis="y", visible=False)
fig.tight_layout()
save(fig, "v2_fig01.png")

# ------------------------------------------------------------------ Fig 4
fig, axes = plt.subplots(3, 3, figsize=(7.5, 4.25), sharex=True, sharey=True)
index_grid = np.linspace(data["ses_index"].min(), data["ses_index"].max(), 50)

for ax, (subject, grade) in zip(axes.flat, GROUPS):
    rows = rows_of(subject, grade)
    ax.scatter(rows["ses_index"], rows["score"], s=7, color=BLUE, alpha=0.45, linewidths=0)
    slope, intercept = np.polyfit(rows["ses_index"], rows["score"], 1)
    ax.plot(index_grid, intercept + slope * index_grid, color=INK, linewidth=1.6)
    r = rows["ses_index"].corr(rows["score"])
    ax.set_title(f"{subject} gr {grade}   r = {r:.2f}", fontsize=8.5)
    ax.tick_params(labelsize=7.5)

for ax in axes[-1]:
    ax.set_xlabel("Socio-economic index (SD)", fontsize=8)
for ax in axes[:, 0]:
    ax.set_ylabel("Mean score", fontsize=8)
fig.tight_layout()
save(fig, "v2_fig04.png")

print("done")
