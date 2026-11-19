#!/usr/bin/env python3
"""
Draw the blueprint of the staggered bracket, A and B, on the shared house sheet of common-blueprint-generator
(https://github.com/csmarshall/common-blueprint-generator), which the Blueprint workflow installs.

A is drawn (both faces, the plan, a section through a bar socket). B is its mirror image, so it is described, with its socket positions read from the
same Params, not drawn. The two zip-tie slits are shown on both faces, with a detail. Every view is a hidden-line projection of the CAD model,
and every number is read from the Params object the model is built from.

Usage:
    python3 make_blueprint_staggered.py       # writes blueprint_staggered.svg and refreshes the README embed
    python3 make_blueprint_staggered.py --log-level DEBUG
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
DETAIL = 1.5   # sheet mm per model mm for the section
SLIT_DETAIL = 3.5   # sheet mm per model mm for the tie slit detail
TOP_LABEL_DROP = 13.0   # the end labels sit under the top view's slit dimensions, beside its caption
DEFAULT_OUT = Path(__file__).with_name("blueprint_staggered")


def draw(out_stem: Path) -> None:
    ctx = bh.Context(Path(__file__), out_stem)
    a, b = Params.staggered(), Params.staggered(mirror=True)
    solid = build_bracket(a).val()
    p = a
    L, H, T = p.length, p.height, p.thickness
    log.info("projecting views of a %.0f x %.0f x %.0f mm part", T, L, H)
    sheet = Sheet("B")
    x_left = 34.0

    right = sp.face_view(sheet, p, solid, x_left, 218.0, +1, p.bar_y_right, SCALE, "FRONT (+X face)", "A", full=True)
    sp.face_view(sheet, p, solid, x_left, 148.0, -1, p.bar_y_left, SCALE, "BACK (-X face)", "A, seen from behind")

    top = View.at_corner(sheet, project(solid.wrapped, (0, 0, 1), (-1, 0, 0)), (x_left, 104.0), SCALE).draw()
    top.caption("TOP", "leg ends; slits hidden", below=TOP_LABEL_DROP)
    top.dim_v(-T / 2, T / 2, 0, -9)
    sp.slit_position_dims(top, p)
    sp.end_labels(sheet, top, p, drop=TOP_LABEL_DROP)

    # Section through the first +X socket, enlarged, right of the main views.
    x_det = x_left + L * SCALE + 38
    cut = p.bar_y_right[0]
    sp.face_section(sheet, p, solid, +1, cut, (x_det + 6, 181.0), DETAIL, "SECTION A-A")
    xs = right.to_sheet((cut, 0))[0][0]
    sp.cut_line(sheet, right, (cut, -4), (cut, H + 3), "A")

    # Tie slit, enlarged.
    sp.slit_detail(sheet, p, solid, (x_det + 4, 94.0), SLIT_DETAIL, "DETAIL B: TIE SLIT")

    sheet_notes = [
        f"Tubes are {fmt(p.tube_od)} dia. All sockets are {fmt(p.bore)} dia, {fmt(p.bar_depth)} deep, with a {fmt(p.chamfer)} lead-in.",
        f"Bar sockets: {len(p.bar_y_left)} on each long face, centred {fmt(p.bar_z)} above the flat edge. The two faces' sets are offset "
        f"{fmt(p.face_offset)} along the bracket, so they pass side by side with {fmt(p.thickness - p.bar_depth)} of plastic behind each.",
        "B is a true mirror image of A and is printed as its own part. Turning A over does not make B (the bars land at the wrong height), and "
        "turning it end for end changes nothing. Measured from the front end (the end facing the room), "
        f"A has -X face sockets at {', '.join(fmt(y) for y in a.bar_y_left)} and +X face at {', '.join(fmt(y) for y in a.bar_y_right)}; "
        f"B has -X face at {', '.join(fmt(y) for y in b.bar_y_left)} and +X face at {', '.join(fmt(y) for y in b.bar_y_right)}. "
        "Alternate A and B along a row to zigzag.",
        f"Upright sockets: one from each end of each leg, on the centre line, {fmt(p.divider)} divider between.",
        sp.slit_notes(p),
        "Print flat edge down, no supports. Untested hobby design. No load rating. See DISCLAIMER.md.",
    ]
    bh.finish(sheet, ctx, out_stem, DEFAULT_OUT, title="STAGGERED BRACKET A / B", number="FRB-002", source="shared-wall-bracket/shared_wall_bracket.py",
              for_=bh.FOR_RACK, material="ABS or PETG. Not PLA.", scale=SCALE, detail_scales=(DETAIL, SLIT_DETAIL), notes=sheet_notes,
              readme=Path(__file__).with_name("README.md"), alt="Blueprint of the staggered bracket, A and B",
              source_file=Path(__file__).with_name("shared_wall_bracket.py"))


if __name__ == "__main__":
    bh.run(__doc__, draw, DEFAULT_OUT, quiet=("shared_wall_v2",))
