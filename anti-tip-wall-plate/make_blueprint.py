#!/usr/bin/env python3
"""
Draw the blueprint of the anti-tip wall plate on the shared house sheet of common-blueprint-generator
(https://github.com/csmarshall/common-blueprint-generator), which the Blueprint workflow installs.

Every view is a hidden-line projection of the CAD model, and every number is read from the same Params object the model is built from.

Usage:
    python3 make_blueprint.py                 # writes blueprint.svg and refreshes the README embed
    python3 make_blueprint.py --log-level DEBUG
"""
import logging
import math
import sys
from pathlib import Path

import numpy as np

from blueprint import Sheet, View, fmt, project

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import blueprint_helpers as bh  # noqa: E402
from wall_plate import Params, build_wall_plate  # noqa: E402

log = logging.getLogger("blueprint")

SCALE = 2.5    # sheet mm per model mm for the main views
ISO = 1.4      # the isometric is not to scale
PLAN_Y = 166.0  # sheet y of the plan view
DEFAULT_OUT = Path(__file__).with_name("blueprint")  # the README embed is only refreshed for this output


def draw(p: Params, out_stem: Path) -> None:
    ctx = bh.Context(Path(__file__), out_stem)
    shape = build_wall_plate(p).val().wrapped
    half, t, top, W = p.plate_length / 2, p.plate_thickness, p.height, p.plate_width
    leg_out = p.slot_u / 2 + p.leg                       # half the saddle's outer width, as the model computes it
    log.info("projecting views of a %.0f x %.1f x %.0f mm part", p.plate_length, top, W)
    sheet = Sheet("B")

    # --- Profile: looking along the width (W). Model (U, N) -> sheet. This is the face that stands on the print bed. ---
    prof = View(sheet, project(shape, (0, 0, 1), (0, 1, 0)), (110.0, 205.0), SCALE).draw()
    prof.caption("PROFILE", "print face: stands on the bed", below=22)
    prof.dim_h(-half, half, 0, -9)
    prof.dim_v(0, top, -half, -8)
    prof.dim_v(0, t, half, 7)
    prof.dim_v(t + p.slot_n, top, leg_out, 7)
    prof.dim_h(-leg_out, -p.slot_u / 2, top, 7)
    prof.dim_h(-leg_out, leg_out, top, 15)
    prof.dim_h(-p.slot_u / 2, p.slot_u / 2, t + p.slot_n / 2, 0, ext=False)      # inside the slot: the tie's width
    prof.dim_v(t, t + p.slot_n, -p.slot_u / 2, -6)                              # the tie's thickness, across the slot's left wall
    x0, y0, x1, y1 = prof.box()
    prof.leader((-leg_out - p.gusset * 0.5, t + p.gusset * 0.3), (x0 + 14, y0 + 21), f"{fmt(p.gusset)} 45 deg foot", ha="left")
    prof.leader((-leg_out + p.corner * 0.3, top - p.corner * 0.3), (x0 + 14, y1 + 8), f"{fmt(p.corner)} 45 deg break", ha="left")

    # --- Plan: looking at the face the tie sits on. Model (U, -W) -> sheet, so the plate's width runs down the page. ---
    plan = View(sheet, project(shape, (0, 1, 0), (0, 0, -1)), (110.0, PLAN_Y), SCALE).draw()
    plan.caption("PLAN", "tie-side face", below=22)
    xs = [-half, -p.screw_offset, p.screw_offset, half]
    for a, b in zip(xs, xs[1:]):
        plan.dim_h(a, b, -W, -9)
    plan.dim_v(-W, 0, half, 7)
    plan.leader((p.screw_offset + p.screw_d / 2 * 0.7, -W / 2 + p.screw_d / 2 * 0.7), (110.0 + half * SCALE + 6, PLAN_Y + 8),
                f"2x {fmt(p.screw_d)} dia, through the plate")

    # --- End: looking along the plate. Model (-W, N) -> sheet. ---
    end = View(sheet, project(shape, (1, 0, 0), (0, 1, 0)), (255.0 + W * SCALE, 205.0), SCALE).draw()
    end.caption("END", below=22)
    end.dim_h(-W, 0, 0, -9)
    end.dim_v(0, top, 0, 8)

    # --- Isometric. ---
    n = np.array([1.0, 0.9, 1.1])
    n /= np.linalg.norm(n)
    x_dir = np.array([1.0, 0.0, -1.0]) / math.sqrt(2)
    up = np.cross(n, x_dir)
    iso_proj = project(shape, tuple(n), tuple(up))
    iso_proj.hidden = []
    iso = View.at_corner(sheet, iso_proj, (300.0, 120.0), ISO).draw(hidden=False, centre_marks=False)
    iso.caption("ISOMETRIC", "not to scale", below=6)

    bh.finish(
        sheet, ctx, out_stem, DEFAULT_OUT, title="ANTI-TIP WALL PLATE", number="FRB-004", source="anti-tip-wall-plate/wall_plate.py",
        for_="Zip-tie tether for the filament rack (Amazon B0FFZ8SSQX)", material="PETG, ABS or ASA. Not PLA.", scale=SCALE, detail_scales=(),
        notes=[
            f"Tie slot {fmt(p.slot_u)} x {fmt(p.slot_n)}: {fmt(p.tie_width)} x {fmt(p.tie_thickness)} tie plus {fmt(p.slot_clearance)} clearance "
            "(and 0.6 extra in width).",
            f"One profile extruded {fmt(W)} along the width. Print standing on the profile, no supports, 4 or more wall loops.",
            f"Screw holes {fmt(p.screw_d)} dia for a #8 / 4 mm pan-head screw, {fmt(p.screw_offset)} either side of the centre.",
            "Untested hobby design. No load rating. See DISCLAIMER.md.",
        ],
        readme=Path(__file__).with_name("README.md"), alt="Blueprint of the anti-tip wall plate", source_file=Path(__file__).with_name("wall_plate.py"),
    )


if __name__ == "__main__":
    bh.run(__doc__, lambda out: draw(Params(), out), DEFAULT_OUT, quiet=("wall_plate",))
