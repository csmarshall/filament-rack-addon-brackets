#!/usr/bin/env python3
"""
Draw the blueprint of the fit-test coupon on the shared house sheet of common-blueprint-generator
(https://github.com/csmarshall/common-blueprint-generator), which the Blueprint workflow installs.

Every view is a hidden-line projection of the CAD model, and every number is read from the Params and the CouponLayout the model is built from.

Usage:
    python3 make_blueprint_coupon.py          # writes blueprint_coupon.svg and refreshes the README embed
    python3 make_blueprint_coupon.py --log-level DEBUG
"""
import logging
import sys
from pathlib import Path

import cadquery as cq

from blueprint import Sheet, View, fmt, project, section_loops

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import blueprint_helpers as bh  # noqa: E402
import sheet_parts as sp  # noqa: E402
from shared_wall_bracket import Params, build_coupon, coupon_layout  # noqa: E402

log = logging.getLogger("blueprint")

SCALE = 2.5   # sheet mm per model mm: the coupon is small
DEFAULT_OUT = Path(__file__).with_name("blueprint_coupon")


def section(sheet: Sheet, solid: cq.Solid, y_cut: float, corner: tuple[float, float], title: str, detail: str) -> View:
    """Section of the coupon at model Y = y_cut, seen from -Y (view x = model X, view y = model Z), lower-left corner at `corner`."""
    slab = solid.intersect(cq.Solid.makeBox(200, sp.SLAB, 200, pnt=cq.Vector(-100, y_cut - sp.SLAB / 2, -50)))
    proj = project(slab.wrapped, (0, -1, 0), (0, 0, 1))
    proj.hidden = []
    view = View.at_corner(sheet, proj, corner, SCALE).draw()
    view.hatch(section_loops(solid.wrapped, (0, y_cut, 0), (0, -1, 0), (1, 0, 0)))
    view.caption(title, detail, below=16)
    return view


def draw(p: Params, out_stem: Path) -> None:
    ctx = bh.Context(Path(__file__), out_stem)
    c = coupon_layout(p)
    solid = build_coupon(p).val()
    log.info("projecting views of a %.1f x %.1f x %.1f mm coupon", c.size_x, c.size_y, c.size_z)
    sheet = Sheet("B")
    x_left = 40.0

    # Front: the +X face, with the bar socket face on. View x = model Y, view y = model Z.
    front = View.at_corner(sheet, project(solid.wrapped, (1, 0, 0), (0, 0, 1)), (x_left, 200.0), SCALE).draw()
    front.caption("FRONT (+X face)", "bar socket", below=24)
    ys = [0.0, c.upright_y, c.bar_y, c.slit_y, c.size_y]
    for a, b in zip(ys, ys[1:]):
        front.dim_h(a, b, 0, -9)
    front.dim_h(0, c.size_y, 0, -17)
    front.dim_v(0, c.size_z, c.size_y, 9)
    front.dim_v(0, c.bar_z, c.size_y, 17)
    x0, y0, x1, y1 = front.box()
    front.leader((c.bar_y + p.bore / 2 * 0.7, c.bar_z + p.bore / 2 * 0.7), (x1 + 12, y1 - 6), f"{fmt(p.bore)} dia, {fmt(p.bar_depth)} deep", ha="left")
    front.leader((c.slit_y + p.tie_slit_mouth[1] / 2, c.slit_z + p.tie_slit_height / 2 * 0.5), (x1 + 12, y1 - 16),
                 f"{fmt(p.tie_slit_height)} x {fmt(p.tie_slit_width)} tie slit, through", ha="left")

    # Top: the upright socket. View x = model Y, view y = -model X.
    top = View.at_corner(sheet, project(solid.wrapped, (0, 0, 1), (-1, 0, 0)), (x_left, 102.0), SCALE).draw()
    top.caption("TOP", "upright socket", below=17)
    top.dim_h(0, c.size_y, -c.size_x, -9)
    top.dim_v(-c.size_x, 0, c.size_y, 9)
    x0, y0, x1, y1 = top.box()
    top.leader((c.upright_y + p.bore / 2 * 0.7, -c.upright_x + p.bore / 2 * 0.7), (x1 + 12, y1 - 8), f"{fmt(p.bore)} dia, {fmt(c.upright_depth)} deep", ha="left")

    # Cutting planes, lettered on the top view (view x = model Y).
    sp.cut_line(sheet, top, (c.bar_y, -c.size_x - 4), (c.bar_y, 3), "A")
    sp.cut_line(sheet, top, (c.upright_y, -c.size_x - 4), (c.upright_y, 3), "B")
    sp.cut_line(sheet, top, (c.slit_y, -c.size_x - 4), (c.slit_y, 3), "C")

    # Sections, right of the main views.
    x_sec = x_left + c.size_y * SCALE + 80
    a = section(sheet, solid, c.bar_y, (x_sec, 175.0), "SECTION A-A", "bar socket")
    a.dim_h(c.size_x - p.bar_depth, c.size_x, c.size_z, 6)
    a.dim_h(0, c.size_x - p.bar_depth, c.size_z, 6)
    a.dim_h(0, c.size_x, 0, -8)
    a.dim_v(0, c.size_z, 0, -8)
    b = section(sheet, solid, c.upright_y, (x_sec + c.size_x * SCALE + 25, 175.0), "SECTION B-B", "upright socket")
    b.dim_h(0, c.upright_x - p.bore / 2, c.size_z, 6)
    b.dim_h(c.upright_x + p.bore / 2, c.size_x, c.size_z, 6)
    b.dim_h(0, c.size_x, 0, -8)
    b.dim_v(c.size_z - c.upright_depth, c.size_z, c.size_x, 8)
    b.dim_v(0, c.size_z - c.upright_depth, c.size_x, 8)
    s = section(sheet, solid, c.slit_y, (x_sec + 2 * (c.size_x * SCALE + 25), 175.0), "SECTION C-C", "tie slit")
    mh = p.tie_slit_mouth[0]
    s.dim_v(c.slit_z - p.tie_slit_height / 2, c.slit_z + p.tie_slit_height / 2, c.size_x / 2, 0, ext=False)   # inside the opening: its height
    s.dim_v(c.slit_z - mh / 2, c.slit_z + mh / 2, c.size_x, 8)
    s.dim_h(0, c.size_x, 0, -8)
    s.leader((c.size_x - p.tie_slit_lead_in * 0.5, c.slit_z + p.tie_slit_height / 2 + p.tie_slit_lead_in * 0.5),
             (float(s.origin[0]) + 2, float(s.to_sheet((0, c.size_z))[0][1]) + 12), f"{fmt(p.tie_slit_lead_in)} x 45 deg lead-in", ha="left")

    bh.finish(
        sheet, ctx, out_stem, DEFAULT_OUT, title="FIT TEST COUPON", number="FRB-005", source="shared-wall-bracket/shared_wall_bracket.py",
        for_="Tuning the socket fit before printing a bracket", material="As the brackets will be.", scale=SCALE, detail_scales=(),
        notes=[
            f"One upright socket, one bar socket and one tie slit at production size: tube {fmt(p.tube_od)} dia plus {fmt(p.fit_clearance)} clearance gives {fmt(p.bore)} dia.",
            f"Bar socket {fmt(p.bar_depth)} deep, centred {fmt(c.bar_z)} up; upright socket {fmt(c.upright_depth)} deep from the top.",
            f"Tie slit {fmt(p.tie_slit_height)} x {fmt(p.tie_slit_width)} with rounded ends and a {fmt(p.tie_slit_lead_in)} x 45 deg lead-in on both faces, through the {fmt(c.size_x)} thickness, "
            "the same as on the brackets. Push a zip tie through it as well as the tubes into their sockets.",
            "Tune fit_clearance in shared_wall_bracket.py until a tube pushes in by hand and does not rock.",
            "Untested hobby design. No load rating. See DISCLAIMER.md.",
        ],
        readme=Path(__file__).with_name("README.md"), alt="Blueprint of the fit-test coupon", source_file=Path(__file__).with_name("shared_wall_bracket.py"),
    )


if __name__ == "__main__":
    bh.run(__doc__, lambda out: draw(Params(), out), DEFAULT_OUT, quiet=("shared_wall_v2",))
