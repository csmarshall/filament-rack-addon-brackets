#!/usr/bin/env python3
"""
Draw the blueprint of the end bracket, left and right, on the shared house sheet of common-blueprint-generator
(https://github.com/csmarshall/common-blueprint-generator), which the Blueprint workflow installs.

The left bracket (Params.end("left"), anchored) is drawn. The right bracket is its mirror image, so it is described, with its socket face read
from the same Params, not drawn. Every view is a hidden-line projection of the CAD model, and every number is read from the Params object the
model is built from.

Usage:
    python3 make_blueprint_end.py             # writes blueprint_end.svg and refreshes the README embed
    python3 make_blueprint_end.py --log-level DEBUG
"""
import logging
import sys
from pathlib import Path

from blueprint import Sheet, View, fmt, project

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import blueprint_helpers as bh  # noqa: E402
import sheet_parts as sp  # noqa: E402
from shared_wall_bracket import Params, build_bracket  # noqa: E402

log = logging.getLogger("blueprint")

SCALE = 0.75   # sheet mm per model mm for the main views
DETAIL = 1.5   # sheet mm per model mm for the section and the anchor detail
DEFAULT_OUT = Path(__file__).with_name("blueprint_end")


def draw(out_stem: Path) -> None:
    ctx = bh.Context(Path(__file__), out_stem)
    p = Params.end("left", anchor=True)
    mirror = Params.end("right", anchor=True)
    solid = build_bracket(p).val()
    L, H, T = p.length, p.height, p.thickness
    face = p.bar_faces[0]                                  # the one face with sockets (+X for the left bracket)
    ys = p.bar_y_right if face > 0 else p.bar_y_left
    log.info("projecting views of a %.0f x %.0f x %.0f mm part", T, L, H)
    sheet = Sheet("B")
    x_left = 34.0

    front = sp.face_view(sheet, p, solid, x_left, 200.0, face, ys, SCALE, "FRONT (+X face)", "socket face, left bracket", full=True)
    top = View.at_corner(sheet, project(solid.wrapped, (0, 0, 1), (-1, 0, 0)), (x_left, 120.0), SCALE).draw()
    top.caption("TOP", "leg ends; the rear collar is on the right", below=5)
    top.dim_v(-T / 2, T / 2, 0, -9)

    x_det = x_left + L * SCALE + 50
    cut = ys[0]
    sp.face_section(sheet, p, solid, face, cut, (x_det + 6, 181.0), DETAIL, "SECTION A-A")
    sp.cut_line(sheet, front, (cut, -4), (cut, H + 3), "A")

    ox, top_y = sp.anchor_extent(p)
    z = p.saddle_height / 2
    sp.cut_line(sheet, front, (L - p.leg_length + 7, z), (top_y + 1, z), "B")
    sp.anchor_plan(sheet, p, solid, x_det - 4, 131.0, DETAIL, "DETAIL B: ANCHOR")
    sp.anchor_rear(sheet, p, solid, (x_det + 78, 107.0), 1.0, "VIEW C")

    side = "+X" if face > 0 else "-X"
    other = "-X" if mirror.bar_faces[0] < 0 else "+X"
    sheet_notes = [
        f"Tubes are {fmt(p.tube_od)} dia. All sockets are {fmt(p.bore)} dia, {fmt(p.bar_depth)} deep, with a {fmt(p.chamfer)} lead-in.",
        f"Bar sockets: {len(ys)} on the {side} face only, centred {fmt(p.bar_z)} above the flat edge, {fmt(p.thickness - p.bar_depth)} of plastic behind each.",
        f"The right bracket is the mirror image of the left, with its sockets on the {other} face. Left and right are named facing the rack. "
        "They are not interchangeable: the anchor must stay at the back.",
        f"Upright sockets: one from each end of each leg, on the centre line, {fmt(p.divider)} divider between.",
        sp.anchor_notes(p),
        "Print flat edge down, no supports. Untested hobby design. No load rating. See DISCLAIMER.md.",
    ]
    bh.finish(sheet, ctx, out_stem, DEFAULT_OUT, title="END BRACKET LEFT / RIGHT", number="FRB-003", source="shared-wall-bracket/shared_wall_bracket.py",
              for_=bh.FOR_RACK, material="ABS or PETG. Not PLA.", scale=SCALE, detail_scales=(DETAIL,), notes=sheet_notes,
              readme=Path(__file__).with_name("README.md"), alt="Blueprint of the end bracket, left and right",
              source_file=Path(__file__).with_name("shared_wall_bracket.py"))


if __name__ == "__main__":
    bh.run(__doc__, draw, DEFAULT_OUT, quiet=("shared_wall_v2",))
