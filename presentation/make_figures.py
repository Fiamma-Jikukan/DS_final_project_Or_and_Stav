"""Re-run the notebook's pipeline, then redraw the four deck figures at slide size.

Each figure is authored at the exact size it occupies on the slide, so the point
sizes set here are the point sizes the audience sees.
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

PROJECT = Path(r"C:\Users\User\PycharmProjects\DS_final_project_Or_and_Stav")
OUT = PROJECT / "presentation" / "figures"
NB = PROJECT / "DS_final_project_Or_and_Stav.ipynb"
LAST_CELL = 141          # everything the deck needs; the sensitivity rebuilds come later

warnings.filterwarnings("ignore")
plt.show = lambda *a, **k: None
builtins.display = lambda *a, **k: None

NEEDED = ["eligible", "flagged", "is_flagged", "score_groups", "official_cluster",
          "gap_profile", "gap_groups", "importance", "diverging",
          "INK", "INK_MUTED", "NEUTRAL", "GRID", "BLUE", "RED", "ORANGE"]
import tempfile
CACHE = Path(tempfile.gettempdir()) / "deck_figure_inputs.pkl"

import os
import pickle
os.chdir(PROJECT)

if "--cached" in sys.argv and CACHE.exists():
    blob = pickle.loads(CACHE.read_bytes())
    ns = blob["ns"]
    matplotlib.rcParams.update(blob["rc"])   # the notebook's plot style, set in cell 40
    print("loaded cached pipeline output")
else:
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
    rc = {k: v for k, v in matplotlib.rcParams.items()
          if k not in ("backend", "figure.dpi", "savefig.dpi")}
    CACHE.write_bytes(pickle.dumps({"ns": {k: ns[k] for k in NEEDED}, "rc": rc}))

# ------------------------------------------------------------------ styling
import numpy as np
import pandas as pd

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 11.5,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9.5,
    "figure.dpi": 200,
    "savefig.dpi": 200,
})

INK = ns["INK"]
INK_MUTED = ns["INK_MUTED"]
NEUTRAL = ns["NEUTRAL"]
GRID = ns["GRID"]
BLUE = ns["BLUE"]
RED = ns["RED"]
ORANGE = ns["ORANGE"]


def save(fig, name):
    path = OUT / name
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)


# ------------------------------------------------------------------ Fig 8
eligible, flagged = ns["eligible"], ns["flagged"]
is_flagged = ns["is_flagged"]

fig, ax = plt.subplots(figsize=(7.3, 4.25))
ax.axhline(0, color=INK_MUTED, linestyle="--", linewidth=1, zorder=1)
rest = eligible[~is_flagged]
ax.scatter(rest["ses_index"], rest["gap"], s=16, color=NEUTRAL, edgecolor=GRID,
           linewidths=0.5, zorder=2,
           label=f"not consistent enough to call ({len(rest)})")
for group, colour in [("over-performer", BLUE), ("under-performer", RED)]:
    part = flagged[flagged["group"] == group]
    ax.scatter(part["ses_index"], part["gap"], s=26, color=colour, alpha=0.85,
               linewidths=0, zorder=3, label=f"{group} ({len(part)})")
NUDGE = {"Basmat Tab'Un": (6, -12), "Haarava Hatikhona": (-6, 0)}
for _, r in pd.concat([flagged.nlargest(5, "gap"),
                       flagged.nsmallest(5, "gap")]).iterrows():
    name = r["name_en"].title()
    dx, dy = NUDGE.get(name, (6, 0))
    ax.annotate(name, (r["ses_index"], r["gap"]), xytext=(dx, dy),
                textcoords="offset points", fontsize=9, va="center", color=INK,
                ha="right" if dx < 0 else "left")
ax.set(xlabel="CBS socio-economic index (SD units)",
       ylabel="Mean gap, in SDs of its own test")
ax.set_ylim(eligible["gap"].min() - 0.3, eligible["gap"].max() + 0.3)
ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0),
          ncol=3, fontsize=9, columnspacing=1.4, handletextpad=0.4)
fig.tight_layout()
save(fig, "deck_fig08.png")

# ------------------------------------------------------------------ Fig 10
# One panel only: the achievement-score groups. The gap panel is a null result
# and is quoted as a number on the slide instead.
score_groups, official_cluster = ns["score_groups"], ns["official_cluster"]
diverging = ns["diverging"]

table = pd.crosstab(score_groups[10], official_cluster.loc[score_groups[10].index])
table = table.reindex(index=range(1, 11), columns=range(1, 11), fill_value=0)

fig, ax = plt.subplots(figsize=(5.5, 4.55))
ax.imshow(table, cmap="Blues", vmin=0, vmax=table.values.max())
ax.set(xticks=range(10), yticks=range(10),
       xticklabels=range(1, 11), yticklabels=range(1, 11),
       xlabel="Official CBS cluster",
       ylabel="Our group from achievement (weakest first)")
ax.grid(False)
for i in range(10):
    for j in range(10):
        count = table.iat[i, j]
        if count:
            ax.text(j, i, count, ha="center", va="center", fontsize=9.5,
                    color="white" if count > table.values.max() * 0.6 else INK)
fig.tight_layout()
save(fig, "deck_fig10.png")

# ------------------------------------------------------------------ Fig 11
gap_profile, gap_groups = ns["gap_profile"], ns["gap_groups"]
gap_centres = gap_profile.groupby(gap_groups[10]).mean()
counts = gap_groups[10].value_counts().sort_index()

# The profile columns are keyed by the notebook's subject names; only Math is renamed for the slide.
SUBJECT_TICKS = {"Math": "Mathematics"}
spreads = (gap_centres.max(axis=1) - gap_centres.min(axis=1)).sort_values()
named = [g for g in (4, 5) if g in gap_centres.index]   # the pair the notebook names
assert len(named) == 2, named

fig, ax = plt.subplots(figsize=(7.9, 4.0))
positions = np.arange(len(gap_centres.columns))
for group, centre in gap_centres.iterrows():
    uniform = spreads.loc[group] < 0.5
    ax.plot(positions, centre.to_numpy(), marker="o", markersize=5,
            linewidth=2.8 if group in named else (1.8 if not uniform else 1.2),
            alpha=0.95 if group in named else (0.45 if not uniform else 0.3),
            color=ORANGE if not uniform else INK_MUTED,
            zorder=3 if group in named else 2)
    if group in named:
        ax.annotate(f"group {group}  (n={counts.loc[group]})",
                    (positions[0], centre.iloc[0]),
                    xytext=(10, 13 if centre.iloc[0] > 0 else -18),
                    textcoords="offset points", fontsize=10.5, fontweight="bold",
                    color=ORANGE)
ax.axhline(0, color=INK_MUTED, linestyle="--", linewidth=1)
ax.set(xticks=positions,
       xticklabels=[SUBJECT_TICKS.get(c[0], c[0]) for c in gap_centres.columns],
       ylabel="Mean gap, in SDs of its own test")
ax.tick_params(axis="x", labelsize=11)
ax.margins(x=0.07)
fig.tight_layout()
save(fig, "deck_fig11.png")

# ------------------------------------------------------------------ Fig 13
importance = ns["importance"]
TOP = 10
top_variables = importance.head(TOP).index[::-1]
positions = np.arange(len(top_variables))

fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.45), sharey=True)
for ax, (column, colour, title) in zip(axes, [
        ("permutation (forest)", BLUE, "Permutation: R\u00b2 lost"),
        ("impurity (forest)", ORANGE, "Impurity: built-in")]):
    values = importance.loc[top_variables, column]
    ax.barh(positions, values, color=colour, height=0.7)
    ax.axvline(0, color=INK_MUTED, linewidth=1)
    ax.set(yticks=positions, yticklabels=top_variables, title=title)
    ax.grid(axis="y", visible=False)
    ax.tick_params(labelsize=9)
    ax.title.set_size(10.5)
fig.tight_layout()
save(fig, "deck_fig13.png")

print("done")
