#!/usr/bin/env python3
"""
Draw a plan view (looking down) of a row of rack columns joined by shared-wall
brackets, for each bracket layout: in line, staggered A/B alternating, and
staggered A only.

Left and right are as seen from the room, facing the wall (the wall is at the
top of the page).  The brackets are drawn as installed, flat edge up: an A
bracket sets the column on its LEFT further back, a B bracket the column on its
right.  In the model's own frame (printed flat edge down) A's far-set face is
+X; rolling the part over its length axis puts that face on the left.

The depths, socket positions and stagger come from the bracket's Params, so
the diagram follows the model.  The column width is schematic: the horizontal
bars are shortened to fit the page.

Usage:
    python3 make_layout_diagram.py              # writes row_of_five.png
    python3 make_layout_diagram.py --columns 3
"""
import argparse
import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from shared_wall_bracket import Params

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(name)s: %(message)s"
log = logging.getLogger("layout")

PAPER, GRID, INK, DIM = "#0b3a82", "#1d4f9c", "#f4f8ff", "#9fd0ff"
SHARED, STOCK = "#ffd166", "#8fb8ff"
FONT = "DejaVu Sans Mono"
COLUMN_CLEAR = 150.0      # schematic clear width between brackets (real racks are about 400 mm)
STOCK_THICK = 18.0


def column_offsets(walls, step: float) -> list:
    """How far back from the front line each column of a row sits, least 0. `walls` lists the shared walls left to right as seen from the room,
    each 'I', 'A' or 'B'. Installed (flat edge up), an A wall sets the column on its left further back than the one on its right, and a B wall the
    other way round. make_row_sheets.py draws its rows from this same function."""
    offsets = [0.0]
    for kind in walls:
        offsets.append(offsets[-1] + {"I": 0.0, "A": -step, "B": step}[kind])
    low = min(offsets)
    return [o - low for o in offsets]


def plan(ax, y_top, title, note, walls, columns, inline: Params, stag: Params):
    """Draw one row.  `walls` is a list of 'I', 'A' or 'B', one per shared wall."""
    offsets = column_offsets(walls, stag.face_offset)
    depth = inline.stock_length
    back = max(o + depth for o in offsets)
    front_y = y_top - back - 40          # sheet y of the front line; the wall is at the top

    ax.text(20, y_top + 30, title, color=INK, fontsize=10, fontfamily=FONT, weight="bold", va="bottom")
    ax.text(20, y_top + 12, note, color=DIM, fontsize=7, fontfamily=FONT, va="bottom")
    wall_y = front_y + back + 14
    x = 30.0
    xs = []                                  # (x_left, x_right) clear span of each column
    brackets = []                            # (x, thickness, y0, length, kind)
    brackets.append((x, STOCK_THICK, offsets[0], depth, "stock"))
    x += STOCK_THICK
    for i in range(columns):
        xs.append((x, x + COLUMN_CLEAR))
        x += COLUMN_CLEAR
        if i < columns - 1:
            kind = walls[i]
            p = inline if kind == "I" else stag
            y0 = min(offsets[i], offsets[i + 1])
            brackets.append((x, p.thickness, y0, p.length, kind))
            x += p.thickness
    brackets.append((x, STOCK_THICK, offsets[-1], depth, "stock"))
    right = x + STOCK_THICK

    ax.plot([20, right + 10], [wall_y, wall_y], color=INK, lw=2.2)
    ax.text(right + 14, wall_y, "WALL", color=INK, fontsize=7, fontfamily=FONT, va="center")
    ax.plot([20, right + 10], [front_y, front_y], color=DIM, lw=0.5, dashes=(6, 3))
    ax.text(right + 14, front_y, "front line", color=DIM, fontsize=6, fontfamily=FONT, va="center")

    for bx, t, y0, length, kind in brackets:
        colour = STOCK if kind == "stock" else SHARED
        ax.add_patch(Rectangle((bx, front_y + y0), t, length, fc=colour, ec=INK, lw=0.6, alpha=0.95))
        label = {"stock": "stock", "I": "in line", "A": "A", "B": "B"}[kind]
        ax.text(bx + t / 2, front_y + y0 - 8, label, color=colour, fontsize=7 if kind in "AB" else 6,
                fontfamily=FONT, ha="center", va="top", weight="bold")

    for i, (x0, x1) in enumerate(xs):
        o = offsets[i]
        for by in inline.bar_y:              # the four horizontal bars of this column
            ax.plot([x0 - 6, x1 + 6], [front_y + o + by] * 2, color=INK, lw=1.0, alpha=0.8)
        ax.text((x0 + x1) / 2, front_y + o + depth / 2, f"column {i + 1}", color=INK, fontsize=7,
                fontfamily=FONT, ha="center", va="center",
                bbox=dict(boxstyle="square,pad=0.2", fc=PAPER, ec="none"))
        gap = wall_y - 14 - (front_y + o + depth) + 14
        if o > 0:
            ax.text((x0 + x1) / 2, front_y + o - 6, f"{o:g} mm back", color=DIM, fontsize=6,
                    fontfamily=FONT, ha="center", va="top")
        if gap > 14.5:
            ax.annotate("", xy=((x0 + x1) / 2, wall_y), xytext=((x0 + x1) / 2, front_y + o + depth),
                        arrowprops=dict(arrowstyle="<|-|>", color=DIM, lw=0.5, shrinkA=0, shrinkB=0, mutation_scale=5))
    log.info("%s: column offsets %s", title, [f"{o:g}" for o in offsets])
    return front_y


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--columns", type=int, default=5)
    ap.add_argument("--out", type=Path, default=Path(__file__).with_name("row_of_five.png"))
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)
    if args.columns < 2:
        raise SystemExit("need at least 2 columns")

    inline, stag = Params(), Params.staggered()
    n = args.columns
    shared = n - 1
    step = stag.face_offset
    rows = [
        ("IN LINE", f"{shared} in-line brackets per tier. Every column lines up, front and back.", ["I"] * shared),
        ("STAGGERED, ALTERNATING A AND B",
         f"{(shared + 1) // 2} A and {shared // 2} B per tier, A at the left. Columns alternate {step:g} mm back and forward.",
         [("A" if i % 2 == 0 else "B") for i in range(shared)]),
        ("STAGGERED, A ONLY",
         f"{shared} A per tier. Each column sits {step:g} mm further back than the one on its right: {step * shared:g} mm across the row.",
         ["A"] * shared),
    ]
    width = 30 + 2 * STOCK_THICK + n * COLUMN_CLEAR + shared * inline.thickness + 110
    row_h = inline.stock_length + step * shared + 130
    height = row_h * len(rows) + 70
    fig = plt.figure(figsize=(width / 72, height / 72))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), width, height, fc=PAPER, ec="none", zorder=-10))
    for gx in range(0, int(width), 20):
        ax.plot([gx, gx], [0, height], color=GRID, lw=0.25, zorder=-9)
    for gy in range(0, int(height), 20):
        ax.plot([0, width], [gy, gy], color=GRID, lw=0.25, zorder=-9)

    y_top = height - 70
    for title, note, walls in rows:
        plan(ax, y_top, title, note, walls, n, inline, stag)
        y_top -= row_h

    ax.text(20, 46, f"PLAN VIEW: A ROW OF {n} COLUMNS, LOOKING DOWN. ONE TIER SHOWN; EVERY TIER IS THE SAME.",
            color=INK, fontsize=8, fontfamily=FONT, weight="bold")
    ax.text(20, 62, "Seen from the room, facing the wall; left and right are the installer's. Brackets are drawn as installed, flat edge up: A sets the "
                    "column on its left further back, B the column on its right.", color=DIM, fontsize=6.5, fontfamily=FONT)
    ax.text(20, 30, "Yellow: shared-wall brackets. Light blue: stock brackets at the two ends. White lines: the four bars of each column.",
            color=DIM, fontsize=6.5, fontfamily=FONT)
    ax.text(20, 16, "Depth and stagger are to scale; column width is shortened. Arrows mark columns that stand off the wall.",
            color=DIM, fontsize=6.5, fontfamily=FONT)
    fig.savefig(args.out, dpi=170, facecolor=PAPER)
    log.info("wrote %s (%d bytes)", args.out, args.out.stat().st_size)


if __name__ == "__main__":
    main()
