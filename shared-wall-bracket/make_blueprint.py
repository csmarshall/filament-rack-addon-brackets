#!/usr/bin/env python3
"""
Draw the blueprint of the shared-wall bracket on the shared house sheet of common-blueprint-generator
(https://github.com/csmarshall/common-blueprint-generator), which the Blueprint workflow installs.

The views are hand-placed because the bracket needs a section through a bar socket, chain dimensions along the sockets and callouts that an
automatic layout cannot choose. Every view is a hidden-line projection of the CAD model, and every number is read from the same Params object the
model is built from.

Usage:
    python3 make_blueprint.py                 # writes blueprint.svg and refreshes the README embed
    python3 make_blueprint.py --log-level DEBUG
"""
import argparse
import logging
import math
from datetime import date
from pathlib import Path

import cadquery as cq
import numpy as np

from blueprint import Sheet, TitleInfo, View, fmt, git_dates, project, revisions, section_loops
from blueprint.readme import embed, update
from blueprint.reuse_lookup import licence_for
from shared_wall_bracket import Params, build_bracket

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(name)s: %(message)s"
log = logging.getLogger("blueprint")

SCALE = 0.75   # sheet mm per model mm for the main views
DETAIL = 1.5   # sheet mm per model mm for the section
ISO = 0.36     # the isometric is not to scale
DEFAULT_OUT = Path(__file__).with_name("blueprint")  # the README embed is only refreshed for this output


def draw(p: Params, out_stem: Path) -> None:
    dates = git_dates(Path(__file__).resolve().parent)  # before anything is written, so this run's own output does not read as a local edit
    # The drawing's own licence and copyright, from REUSE.toml for the SVG this run writes (not the script's): fails if REUSE.toml does not cover it.
    licence = licence_for(out_stem.with_name(f"{out_stem.name}.svg"))
    solid = build_bracket(p).val()
    shape = solid.wrapped
    L, H, T, R, G = p.length, p.height, p.thickness, p.rail_height, p.leg_length
    half_t = T / 2
    log.info("projecting views of a %.0f x %.0f x %.0f mm part", T, L, H)
    sheet = Sheet("B")
    x_left = 34.0
    per_face = len(p.bar_y)                               # bar sockets on each long face
    cut = p.bar_y[min(1, per_face - 1)]                   # section A-A goes through the second socket (the first if there is only one)
    dim_at = p.bar_y[min(2, per_face - 1)]                # where the socket-height dimension is drawn
    has_vent = p.stagger <= 0 and p.bar_vent_d > 0        # the same condition the model cuts the web vent under

    # --- Front: looking at a hole face. Model (Y, Z) -> sheet. ---------------------
    front = View(sheet, project(shape, (1, 0, 0), (0, 0, 1)), (x_left, 150.0), SCALE).draw()
    front.caption("FRONT", "bar-socket face; the back is identical", below=24)
    xs = [0.0] + list(p.bar_y) + [L]
    for a, b in zip(xs, xs[1:]):
        front.dim_h(a, b, 0, -9)
    front.dim_h(0, L, 0, -17)
    front.dim_h(0, G, H, 7)
    front.dim_v(0, H, L, 9)
    front.dim_v(0, R, L, 17)
    front.dim_v(0, p.bar_z, dim_at, -14, ext=False)
    front.leader((cut + p.bore / 2 * 0.7, p.bar_z + p.bore / 2 * 0.7), (x_left + 70, 186),
                 f"{2 * per_face}x {fmt(p.bore)} dia, {fmt(p.bar_depth)} deep ({per_face} per face)")
    front.leader((G + p.corner_radius * 0.29, R + p.corner_radius * 0.29), (x_left + 22, 186), f"R{fmt(p.corner_radius)}")
    # Cutting plane A-A.
    sy = cut
    a, b = front.to_sheet((sy, -4))[0], front.to_sheet((sy, H + 3))[0]
    sheet.centre_line(tuple(a), tuple(b))
    for q in (a, b):
        sheet.text(q[0] - 2.2, q[1], "A", 7, ha="right", va="center", weight="bold")

    # --- Top: looking down on the leg ends. ------------------------------------------
    top = View(sheet, project(shape, (0, 0, 1), (-1, 0, 0)), (x_left, 226.0), SCALE).draw()
    top.caption("TOP", "leg ends", below=4)
    top.dim_v(-half_t, half_t, 0, -9)
    top.dim_h(0, p.upright_from_end, half_t, 7)
    top.leader((L - p.upright_from_end + p.bore / 2 * 0.7, p.bore / 2 * 0.7), (x_left + 150, 255),
               f"4x {fmt(p.bore)} dia, {fmt(p.upright_depth_leg)} deep (2 here, 2 on the flat edge)")  # one per leg end and one per leg on the flat edge: two legs by design
    top.leader((p.plan_round * 0.29, half_t - p.plan_round * 0.29), (x_left + 22, 255), f"R{fmt(p.plan_round)}")

    # --- Bottom: the flat edge that sits on the print bed. ---------------------------
    bottom = View(sheet, project(shape, (0, 0, -1), (1, 0, 0)), (x_left, 97.0), SCALE).draw()
    bottom.caption("BOTTOM", "flat edge; print bed face", below=4)

    # --- Right end. -------------------------------------------------------------------
    end_x = x_left + L * SCALE + 46
    end = View(sheet, project(shape, (0, 1, 0), (0, 0, 1)), (end_x, 150.0), SCALE).draw()
    end.caption("END", below=24)
    end.dim_h(-half_t, half_t, 0, -9)
    end.dim_v(H - p.upright_depth_leg, H, half_t, 8)
    end.dim_v(p.upright_depth_flat, H - p.upright_depth_leg, half_t, 16)

    # --- Section A-A through a bar socket, enlarged. ---------------------------------
    # Project a thin slice at the cut plane, so the view shows the cut face alone and not the leg beyond it.
    slab = solid.intersect(cq.Solid.makeBox(200, 0.4, 200, pnt=cq.Vector(-100, sy, -50)))
    sec = View(sheet, project(slab.wrapped, (0, -1, 0), (0, 0, 1)), (end_x + 62, 198.0), DETAIL)
    sec.proj.hidden = []
    sec.draw()
    sec.hatch(section_loops(shape, (0, sy, 0), (0, -1, 0), (1, 0, 0)))
    sec.caption("SECTION A-A", "bar sockets", below=16)
    sec.dim_h(-half_t, -p.web / 2, R, 6)
    sec.dim_h(-p.web / 2, p.web / 2, R, 6)
    sec.dim_h(p.web / 2, half_t, R, 6)
    sec.dim_h(-half_t, half_t, 0, -8)
    sec.dim_v(0, R, half_t, 8)
    lower_wall = p.bar_z - p.bore / 2
    upper_wall = R - p.bar_z - p.bore / 2
    sx, sy0 = sec.origin
    sec.leader((-half_t + 9, lower_wall / 2), (sx - 38, sy0 - 11), f"{fmt(lower_wall)} wall", ha="right")
    sec.leader((-half_t + 9, R - upper_wall / 2), (sx - 38, sy0 + R * DETAIL + 4), f"{fmt(upper_wall)} wall", ha="right")

    # --- Isometric. ---------------------------------------------------------------------
    n = np.array([1.0, -1.0, 0.8])
    n /= np.linalg.norm(n)
    x_dir = np.array([1.0, 1.0, 0.0]) / math.sqrt(2)
    up = np.cross(n, x_dir)
    iso_proj = project(shape, tuple(n), tuple(up))
    iso_proj.hidden = []
    iso = View.at_corner(sheet, iso_proj, (end_x + 2, 92.0), ISO).draw(hidden=False, centre_marks=False)
    iso.caption("ISOMETRIC", "not to scale", below=6)

    rendered = date.today()
    sheet.title_block(TitleInfo(
        title="SHARED-WALL BRACKET", drawing_number="FRB-001", for_="9-tier modular filament storage rack (Amazon B0FFZ8SSQX)",
        material="ABS or PETG. Not PLA.", source="shared-wall-bracket/shared_wall_bracket.py", drawn_by="C. MARSHALL", company="Shermer Works",
        started=dates.started, updated=rendered, revisions=revisions(dates, rendered), licence=licence.licence, copyright=licence.copyright,
    ), SCALE, detail_scales=(DETAIL,))
    sheet.notes([
        f"Tubes are {fmt(p.tube_od)} dia. All sockets are {fmt(p.bore)} dia, {fmt(p.bar_depth)} deep, with a {fmt(p.chamfer)} lead-in.",
        f"Bar sockets: {per_face} on each long face, centred {fmt(p.bar_z)} above the flat edge, {fmt(p.web)} web between opposite pairs"
        + (f" with a {fmt(p.bar_vent_d)} dia vent through it." if has_vent else "."),
        f"Upright sockets: one from each end of each leg, on the centre line, {fmt(p.divider)} divider between, "
        f"{fmt(p.upright_vent_d)} dia hole through the divider.",
        "Print flat edge down, no supports. 5 wall loops (Arachne), 15% gyroid infill.",
        "Untested hobby design. No load rating. See DISCLAIMER.md.",
    ])
    (svg,) = sheet.save(out_stem, formats=("svg",))
    if out_stem == DEFAULT_OUT:
        # Keep the drawing and its credit line current in this folder's README, between <!-- blueprint:blueprint --> and <!-- /blueprint -->.
        readme = Path(__file__).with_name("README.md")
        update(readme, "blueprint", embed(readme, svg, "Blueprint of the shared-wall bracket", Path(__file__).with_name("shared_wall_bracket.py")))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output path without extension (the README embed is refreshed only for the default)")
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)
    logging.getLogger("shared_wall_v2").setLevel(logging.WARNING)
    try:
        draw(Params(), args.out)
    except Exception:
        log.exception("Blueprint generation failed")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
