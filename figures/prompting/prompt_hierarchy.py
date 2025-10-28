# Adjusted version: text labels "Prompt Layers" and "increasing control" are now
# slightly separated from the arrows (moved outward horizontally).
#
# Outputs:
#   /mnt/data/figure_prompt_layers_v3.svg
#   /mnt/data/figure_prompt_layers_v3.png

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.patheffects import withStroke

plt.close("all")
fig = plt.figure(figsize=(11, 6.5), dpi=200)
ax = plt.axes([0, 0, 1, 1])
ax.set_xlim(0, 11)
ax.set_ylim(0, 10)
ax.axis("off")

# Colours
COL_SYS   = "#83A6B7"
COL_USER  = "#A8CDB1"
COL_MODEL = "#F2E0AC"

# Geometry
box_w = 9.2
box_h = 2.1
left  = 0.9
gap   = 0.75

y0 = 1.25
y1 = y0 + box_h + gap
y2 = y1 + box_h + gap

def add_box(x, y, w, h, fc, title, subtitle):
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.28,rounding_size=0.65",
        linewidth=2,
        edgecolor="black",
        facecolor=fc,
    )
    ax.add_patch(rect)
    ax.text(
        x + w/2, y + h*0.64, title,
        ha="center", va="center",
        fontsize=20, fontweight="bold",
        path_effects=[withStroke(linewidth=2, foreground="white")]
    )
    ax.text(
        x + w/2, y + h*0.32, subtitle,
        ha="center", va="center",
        fontsize=15,
        path_effects=[withStroke(linewidth=2, foreground="white")]
    )

# Draw boxes
add_box(left, y2, box_w, box_h, COL_SYS,   "System Layer", "defines global role and tone")
add_box(left, y1, box_w, box_h, COL_USER,  "User Layer",   "defines specific task and data")
add_box(left, y0, box_w, box_h, COL_MODEL, "Model Layer",  "integrates both and generates an answer")

# Arrows
left_x  = 0.55
right_x = 10.6

left_arrow = FancyArrowPatch(
    posA=(left_x, y2 + box_h*0.98),
    posB=(left_x, y0 - 0.35),
    arrowstyle='-|>',
    lw=2,
    mutation_scale=12,
    color="black"
)
ax.add_patch(left_arrow)

right_arrow = FancyArrowPatch(
    posA=(right_x, y0 - 0.35),
    posB=(right_x, y2 + box_h*0.98),
    arrowstyle='-|>',
    lw=2,
    mutation_scale=12,
    color="black"
)
ax.add_patch(right_arrow)

# Text slightly offset from arrows
offset = 0.35  # separation distance

ax.text(
    left_x - offset, (y0 + y2 + box_h) / 2,
    "Prompt Layers",
    rotation=90, ha="center", va="center",
    fontsize=18, fontweight="bold",
    path_effects=[withStroke(linewidth=3, foreground="white")]
)

ax.text(
    right_x + offset, (y0 + y2 + box_h) / 2,
    "increasing control",
    rotation=90, ha="center", va="center",
    fontsize=18, fontweight="bold",
    path_effects=[withStroke(linewidth=3, foreground="white")]
)

# Save
png_path = "figures/prompting/prompt_hierarchy.png"
fig.savefig(png_path, bbox_inches="tight")
