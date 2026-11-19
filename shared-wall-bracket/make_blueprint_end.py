#!/usr/bin/env python3
"""
Draw the blueprint of the end bracket on the shared house sheet of common-blueprint-generator
(https://github.com/csmarshall/common-blueprint-generator), which the Blueprint workflow installs.

One part serves both ends of a row, turned end for end as needed, so there is one drawing. Every view is a hidden-line projection of the CAD model, and every number is read from the Params object the
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
DETAIL = 1.5   # sheet mm per model mm for the section
SLIT_DETAIL = 3.5   # sheet mm per model mm for the tie slit detail
TOP_LABEL_DROP = 13.0   # the end labels sit under the top view's slit dimensions, beside its caption
DEFAULT_OUT = Path(__file__).with_name("blueprint_end")


def draw(out_stem: Path) -> None:
    ctx = bh.Context(Path(__file__), out_stem)
    p = Params.end()
    solid = build_bracket(p).val()
    L, H, T = p.length, p.height, p.thickness
    face = p.bar_faces[0]                                  # the one face with sockets (+X)
    ys = p.bar_y_right if face > 0 else p.bar_y_left
    log.info("projecting views of a %.0f x %.0f x %.0f mm part", T, L, H)
    sheet = Sheet("B")
    x_left = 34.0

    front = sp.face_view(sheet, p, solid, x_left, 200.0, face, ys, SCALE, "FACE +X (model frame)", "socket face; installed, it faces left", full=True)
    top = View.at_corner(sheet, project(solid.wrapped, (0, 0, 1), (-1, 0, 0)), (x_left, 120.0), SCALE).draw()
    top.caption("LEG-END VIEW", "slits hidden", below=TOP_LABEL_DROP)
    top.dim_v(-T / 2, T / 2, 0, -9)
    sp.slit_position_dims(top, p)
    sp.end_labels(sheet, top, p, drop=TOP_LABEL_DROP)

    x_det = x_left + L * SCALE + 50
    cut = ys[0]
    sp.face_section(sheet, p, solid, face, cut, (x_det + 6, 181.0), DETAIL, "SECTION A-A")
    sp.cut_line(sheet, front, (cut, -4), (cut, H + 3), "A")

    sp.slit_detail(sheet, p, solid, (x_det + 4, 94.0), SLIT_DETAIL, "DETAIL B: TIE SLIT")

    side = "+X" if face > 0 else "-X"
    turned = sorted(L - y for y in ys)   # the sockets seen from the front end once the bracket is turned end for end
    sheet_notes = [
        f"Tubes are {fmt(p.tube_od)} dia. All sockets are {fmt(p.bore)} dia, {fmt(p.bar_depth)} deep, with a {fmt(p.chamfer)} lead-in.",
        f"Bar sockets: {len(ys)} on the {side} face only, centred {fmt(p.bar_z)} above the flat edge, {fmt(p.thickness - p.bar_depth)} of plastic behind each.",
        "One part serves both ends of a row. Installed, its sockets (the +X face, in the model frame) face left: use it as modelled at the right end "
        "of a row, and turned end for end at the left end. Turned, its sockets sit at "
        f"{', '.join(fmt(y) for y in turned)} from the front end instead of {', '.join(fmt(y) for y in ys)}: a 1 mm shift, "
        "the same as a stock bracket turned around.",
        f"Upright sockets: one from each end of each leg, on the centre line, {fmt(p.divider)} divider between.",
        sp.slit_notes(p),
        sp.INSTALLED_NOTE,
        "Print flat edge down, no supports. Untested hobby design. No load rating. See DISCLAIMER.md.",
    ]
    bh.finish(sheet, ctx, out_stem, DEFAULT_OUT, title="END BRACKET", number="FRB-003", source="shared-wall-bracket/shared_wall_bracket.py",
              for_=bh.FOR_RACK, material="ABS or PETG. Not PLA.", scale=SCALE, detail_scales=(DETAIL, SLIT_DETAIL), notes=sheet_notes,
              readme=Path(__file__).with_name("README.md"), alt="Blueprint of the end bracket",
              source_file=Path(__file__).with_name("shared_wall_bracket.py"))


if __name__ == "__main__":
    bh.run(__doc__, draw, DEFAULT_OUT, quiet=("shared_wall_v2",))
