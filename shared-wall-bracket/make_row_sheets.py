#!/usr/bin/env python3
"""
Draw an assembly sheet of a row of rack columns for each bracket layout:
top view, front view and end view, with a parts count.

Writes row_of_five_in_line.png and row_of_five_staggered.png.

What is to scale, and where the numbers come from:
- Bracket sizes, socket positions and the stagger come from the bracket's
  Params, the same values the models are built from. Which way each A or B
  steps comes from make_layout_diagram.column_offsets: installed, flat edge
  up, an A sets the column on its left back.
- The rack's tier spacing, tier count and bar length are NOT measured.  They
  are taken from the retail listing (9 tiers, 9.9 in apart, 17.3 in wide) and
  can be overridden on the command line.

This is an assembly diagram, not a part blueprint: it is drawn from those
numbers, not projected from a CAD assembly.

Usage:
    python3 make_row_sheets.py
    python3 make_row_sheets.py --columns 3 --tiers 5
"""
import argparse
import logging
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

from make_layout_diagram import column_offsets
from shared_wall_bracket import Params

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(name)s: %(message)s"
log = logging.getLogger("row_sheets")

PAPER, GRID, INK, DIM = "#0b3a82", "#1d4f9c", "#f4f8ff", "#9fd0ff"
SHARED, STOCK, TUBE = "#ffd166", "#8fb8ff", "#dfe9ff"
FONT = "DejaVu Sans Mono"
INCH = 25.4


@dataclass
class Rack:
    """The stock rack, from the retail listing."""
    tiers: int = 9
    overall_height: float = 80.3 * INCH  # listed height of the 9-tier rack
    tier_pitch: float = 250.0            # vertical distance between tiers: the listed height
                                         # less one bracket height (Params.height), over the 8 gaps of 9 tiers
    stock_width: float = 17.3 * INCH     # outside width of one stock rack
    stock_thickness: float = 18.0        # a stock bracket
    stock_bar_depth: float = 16.0        # how far a bar seats in a stock bracket
    tube: float = Params().tube_od       # the tube diameter the brackets are drawn for

    @property
    def bar_length(self) -> float:
        """Bar length implied by the stock rack's outside width."""
        return self.stock_width - 2 * (self.stock_thickness - self.stock_bar_depth)


@dataclass
class Wall:
    x: float            # left face
    thickness: float
    back: float         # how far back from the front line its front end sits
    length: float
    kind: str           # "stock", "I", "A" or "B"


def build_row(kinds, rack: Rack, inline: Params, stag: Params):
    """Lay out the walls of a row.  `kinds` has one entry per shared wall."""
    offsets = column_offsets(kinds, stag.face_offset)

    walls, spans = [], []
    x = 0.0
    walls.append(Wall(x, rack.stock_thickness, offsets[0], inline.stock_length, "stock"))
    x += rack.stock_thickness
    for i in range(len(kinds) + 1):
        # A column's clear span: the bar, less what is seated in each wall.
        left_seat = rack.stock_bar_depth if i == 0 else (inline if kinds[i - 1] == "I" else stag).bar_depth
        right_seat = rack.stock_bar_depth if i == len(kinds) else (inline if kinds[i] == "I" else stag).bar_depth
        clear = rack.bar_length - left_seat - right_seat
        spans.append((x, x + clear, offsets[i]))
        x += clear
        if i < len(kinds):
            p = inline if kinds[i] == "I" else stag
            if kinds[i] == "I":
                walls.append(Wall(x, p.thickness, offsets[i], p.length, "I"))
                x += p.thickness
            else:
                # Staggered sockets overlap in depth: the next column's bars
                # start inside this wall, so the wall is only one thickness wide.
                walls.append(Wall(x, p.thickness, min(offsets[i], offsets[i + 1]), p.length, kinds[i]))
                x += p.thickness
    walls.append(Wall(x, rack.stock_thickness, offsets[-1], inline.stock_length, "stock"))
    return walls, spans, x + rack.stock_thickness


def colour(kind):
    return STOCK if kind == "stock" else SHARED


def text(ax, x, y, s, size=9, c=INK, **kw):
    ax.text(x, y, s, color=c, fontsize=size, fontfamily=FONT, **kw)


def dim(ax, p0, p1, label, vertical=False):
    ax.annotate("", xy=p0, xytext=p1, arrowprops=dict(arrowstyle="<|-|>", color=DIM, lw=0.8, shrinkA=0, shrinkB=0, mutation_scale=9))
    text(ax, (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, label, 8.5, DIM, ha="center", va="center",
         rotation=90 if vertical else 0, bbox=dict(boxstyle="square,pad=0.2", fc=PAPER, ec="none"))


def draw_sheet(title, subtitle, kinds, rack: Rack, inline: Params, stag: Params, out: Path, parts_lines):
    walls, spans, width = build_row(kinds, rack, inline, stag)
    depth = max(w.back + w.length for w in walls)
    foot = 0.0                                # the bottom brackets stand on their own legs
    height = foot + (rack.tiers - 1) * rack.tier_pitch + inline.height
    levels = [foot + k * rack.tier_pitch for k in range(rack.tiers)]

    m, gap = 260.0, 330.0
    fx, fy = m, 760.0                         # front view origin
    tx, ty = m, fy + height + gap             # top view origin
    sx, sy = fx + width + gap, fy             # end view origin
    sheet_w = sx + depth + m + 120
    sheet_h = ty + depth + 300

    fig = plt.figure(figsize=(sheet_w / 190, sheet_h / 190))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, sheet_w)
    ax.set_ylim(0, sheet_h)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), sheet_w, sheet_h, fc=PAPER, ec="none", zorder=-10))
    for gx in range(0, int(sheet_w), 50):
        ax.plot([gx, gx], [0, sheet_h], color=GRID, lw=0.3, zorder=-9)
    for gy in range(0, int(sheet_h), 50):
        ax.plot([0, sheet_w], [gy, gy], color=GRID, lw=0.3, zorder=-9)
    ax.add_patch(Rectangle((40, 40), sheet_w - 80, sheet_h - 80, fc="none", ec=INK, lw=2.0))

    # ---- Front view ---------------------------------------------------------
    text(ax, fx, fy - 70, "FRONT VIEW", 11, weight="bold")
    ax.plot([fx - 60, fx + width + 60], [fy, fy], color=INK, lw=1.6)            # floor
    for w in walls:
        for z in levels:
            ax.add_patch(Rectangle((fx + w.x, fy + z), w.thickness, inline.height, fc=colour(w.kind), ec=INK, lw=0.5))
        for z0, z1 in zip(levels, levels[1:]):
            ax.add_patch(Rectangle((fx + w.x + w.thickness / 2 - rack.tube / 2, fy + z0 + inline.height),
                                   rack.tube, z1 - z0 - inline.height, fc=TUBE, ec="none", alpha=0.85))
        ax.add_patch(Rectangle((fx + w.x + w.thickness / 2 - rack.tube / 2, fy), rack.tube, foot, fc=TUBE, ec="none", alpha=0.85))
    bar_z = inline.height - inline.bar_z          # legs down: bars hang bar_z (9 mm) below the flat top edge
    for x0, x1, _ in spans:
        for z in levels:
            ax.add_patch(Rectangle((fx + x0, fy + z + bar_z - rack.tube / 2), x1 - x0, rack.tube, fc=TUBE, ec="none", alpha=0.85))
    for i, (x0, x1, back) in enumerate(spans):
        label = f"column {i + 1}" + (f"\n{back:g} mm back" if back > 0 else "")
        text(ax, fx + (x0 + x1) / 2, fy + height + 55, label, 9, ha="center", va="bottom", linespacing=1.4)
    for k, z in enumerate(levels):
        text(ax, fx - 30, fy + z + inline.height / 2, f"tier {k + 1}", 7.5, DIM, ha="right", va="center")
    dim(ax, (fx, fy - 150), (fx + width, fy - 150), f"about {width:.0f} mm ({width / INCH:.1f} in)")
    dim(ax, (fx + width + 130, fy), (fx + width + 130, fy + height), f"about {height:.0f} mm ({height / INCH:.1f} in)", vertical=True)
    dim(ax, (fx - 150, fy + levels[0]), (fx - 150, fy + levels[1]), f"{rack.tier_pitch:.0f}", vertical=True)

    # ---- Top view -----------------------------------------------------------
    text(ax, tx, ty + depth + 150, "TOP VIEW (one tier; every tier is the same)", 11, weight="bold")
    wall_y = ty + depth + 45
    ax.plot([tx - 60, tx + width + 60], [wall_y, wall_y], color=INK, lw=3.0)
    text(ax, tx + width + 80, wall_y, "WALL", 9, va="center")
    ax.plot([tx - 60, tx + width + 60], [ty, ty], color=DIM, lw=0.7, dashes=(8, 4))
    text(ax, tx + width + 80, ty, "front", 8, DIM, va="center")
    for x0, x1, back in spans:
        for by in inline.bar_y:
            ax.plot([tx + x0 - 14, tx + x1 + 14], [ty + back + by] * 2, color=TUBE, lw=1.6, alpha=0.9)
    for w in walls:
        ax.add_patch(Rectangle((tx + w.x, ty + w.back), w.thickness, w.length, fc=colour(w.kind), ec=INK, lw=0.6))
        p = inline if w.kind in ("stock", "I") else stag
        for yy in (p.upright_from_end, w.length - p.upright_from_end):
            ax.add_patch(Circle((tx + w.x + w.thickness / 2, ty + w.back + yy), rack.tube / 2, fc=PAPER, ec=INK, lw=0.5))
        name = {"stock": "stock", "I": "in line", "A": "A", "B": "B"}[w.kind]
        text(ax, tx + w.x + w.thickness / 2, ty - 26, name, 9 if w.kind in "AB" else 7.5, colour(w.kind), ha="center", va="top", weight="bold")
    dim(ax, (tx - 150, ty), (tx - 150, ty + depth), f"{depth:.0f}", vertical=True)

    # ---- End view -----------------------------------------------------------
    text(ax, sx, sy - 70, "END VIEW", 11, weight="bold")
    ax.plot([sx - 50, sx + depth + 110], [sy, sy], color=INK, lw=1.6)
    wall_x = sx + depth + 45
    ax.plot([wall_x, wall_x], [sy, sy + height + 60], color=INK, lw=3.0)
    text(ax, wall_x + 22, sy + height / 2, "WALL", 9, ha="left", va="center")
    backs = sorted({s[2] for s in spans})
    for back in backs:
        near = back == backs[0]
        style = dict(fc=STOCK if near else "none", ec=INK, lw=0.5 if near else 0.9, ls="-" if near else (0, (4, 3)))
        length = inline.stock_length
        for z in levels:
            ax.add_patch(Rectangle((sx + back, sy + z + inline.height - inline.rail_height), length, inline.rail_height, **style))
            for y0 in (0.0, length - inline.leg_length):
                ax.add_patch(Rectangle((sx + back + y0, sy + z), inline.leg_length, inline.height, **style))
        for yy in (inline.upright_from_end, length - inline.upright_from_end):
            for z0, z1 in zip([-(inline.height - foot)] + levels, levels):
                ax.add_patch(Rectangle((sx + back + yy - rack.tube / 2, sy + max(z0 + inline.height, 0)), rack.tube,
                                       z1 - max(z0 + inline.height, 0), fc=TUBE if near else "none", ec=INK if not near else "none",
                                       lw=0.6, ls="-" if near else (0, (4, 3)), alpha=0.85 if near else 1.0))
    if len(backs) > 1:
        text(ax, sx + depth / 2, sy + height + 75, f"dashed: columns set {backs[-1] - backs[0]:g} mm back", 8, DIM, ha="center", va="bottom")
    dim(ax, (sx, sy - 150), (sx + depth, sy - 150), f"{depth:.0f}")

    # ---- Title and parts ----------------------------------------------------
    text(ax, m, 420, title, 17, weight="bold", va="center")
    text(ax, m, 350, subtitle, 9.5, DIM, va="center")
    for i, line in enumerate(parts_lines):
        text(ax, m, 285 - i * 46, line, 8.8, INK if i == 0 else DIM, va="center", weight="bold" if i == 0 else "normal")
    note = ("Brackets and stagger are to scale, from the model. Tier spacing, tier count and width come from the\n"
            "retail listing, not from measurement. Untested hobby design: see DISCLAIMER.md. CC BY-NC-SA 4.0, not for resale.")
    text(ax, m, 135, note, 7.6, DIM, ha="left", va="center", linespacing=1.5)

    fig.savefig(out, dpi=150, facecolor=PAPER)
    plt.close(fig)
    log.info("wrote %s: row %.0f mm wide, %.0f mm deep, %.0f mm tall", out, width, depth, height)
    return width, depth, height


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--columns", type=int, default=5)
    ap.add_argument("--tiers", type=int, default=Rack.tiers)
    ap.add_argument("--tier-pitch", type=float, default=Rack.tier_pitch, help="mm between tiers")
    ap.add_argument("--stock-width", type=float, default=Rack.stock_width, help="outside width of one stock rack, mm")
    ap.add_argument("--out-dir", type=Path, default=Path(__file__).parent)
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)
    if args.columns < 2:
        raise SystemExit("need at least 2 columns")

    inline, stag = Params(), Params.staggered()
    rack = Rack(tiers=args.tiers, tier_pitch=args.tier_pitch, stock_width=args.stock_width,
                stock_thickness=inline.stock_thickness, stock_bar_depth=inline.bar_depth)
    n, shared = args.columns, args.columns - 1
    t = rack.tiers
    # What a row uses, against what n stock kits supply (2 brackets per tier,
    # 4 bars per tier and 4 uprights between each pair of tiers, per kit).
    uprights_used = (n + 1) * 2 * (t - 1)
    kit = dict(brackets=n * 2 * t, uprights=n * 4 * (t - 1), bars=n * 4 * t)
    common = (f"From {n} stock kits: {2 * t} of {kit['brackets']} stock brackets (the two end walls), "
              f"{uprights_used} of {kit['uprights']} uprights, all {kit['bars']} bars.")

    a_count, b_count = (shared + 1) // 2, shared // 2
    sheets = [
        ("in_line", f"ROW OF {n}: IN-LINE BRACKETS",
         f"Shared walls {inline.thickness:g} mm thick. Every column lines up, front and back.",
         ["I"] * shared,
         [f"Print: {shared * t} in-line brackets ({shared} per tier x {t} tiers). Every bracket has two zip-tie slits.", common]),
        ("staggered", f"ROW OF {n}: STAGGERED BRACKETS, A AND B ALTERNATING",
         f"Shared walls {stag.thickness:g} mm thick. Installed, flat edge up: A sets the column on its left {stag.face_offset:g} mm back, "
         f"B the column on its right. A, B, A, B from the left.",
         [("A" if i % 2 == 0 else "B") for i in range(shared)],
         [f"Print: {a_count * t} A and {b_count * t} B brackets ({a_count} A + {b_count} B per tier x {t} tiers). Every bracket has two zip-tie slits.", common]),
    ]
    try:
        for stem, title, subtitle, kinds, parts in sheets:
            draw_sheet(title, subtitle, kinds, rack, inline, stag, args.out_dir / f"row_of_five_{stem}.png", parts)
    except Exception:
        log.exception("Drawing failed")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
