"""
Drawing pieces the shared-wall bracket's blueprint sheets have in common (make_blueprint.py, make_blueprint_staggered.py,
make_blueprint_end.py): the anchor detail and the section through a bar socket. Every view is projected from the CAD model and every number is
read from the Params it was built from.
"""
import cadquery as cq

from blueprint import View, fmt, project, section_loops
from shared_wall_bracket import Params

PLAN_MARGIN = 1.0   # model mm of leg shown ahead of the anchor in the plan section; it must stay clear of the last bar socket
SLAB = 0.4          # thickness of the slice projected for a section, model mm


def anchor_extent(p: Params) -> tuple[float, float]:
    """(half the saddle's outer width, rearmost face of the saddle bar), the same numbers build_bracket uses."""
    return p.tie_slot_width / 2 + p.saddle_leg, p.length + p.tie_slot_depth + p.saddle_bar


def anchor_plan(sheet, p: Params, solid: cq.Solid, left: float, mid_y: float, scale: float, title: str) -> View:
    """Plan section through the anchor at half the saddle height, enlarged: sheet x runs along the bracket (rear end at the right).

    `left` is the sheet x of the section's left edge and `mid_y` the sheet y of the bracket's centre line."""
    ox, top = anchor_extent(p)
    half = p.thickness / 2
    y0 = p.length - p.leg_length - PLAN_MARGIN
    z = p.saddle_height / 2
    reach = max(ox, half) + 1.0
    slab = solid.intersect(cq.Solid.makeBox(2 * reach, top + 1.0 - y0, SLAB, pnt=cq.Vector(-reach, y0, z)))
    proj = project(slab.wrapped, (0, 0, 1), (-1, 0, 0))   # view x = model Y, view y = -model X, as in the TOP views
    proj.hidden = []
    view = View(sheet, proj, (left - y0 * scale, mid_y), scale)
    view.draw()
    view.hatch(section_loops(slab.wrapped, (0, y0, z + SLAB / 2), (0, 0, 1), (0, 1, 0)))
    L, sd = p.length, p.tie_slot_depth
    view.dim_h(L, L + sd, ox, 6)
    view.dim_h(L + sd, top, ox, 6)
    view.dim_v(-p.tie_slot_width / 2, p.tie_slot_width / 2, top, 6)
    view.dim_v(-ox, ox, top, 15)
    view.dim_v(-half, half, y0, -6)
    view.caption(title, f"at {fmt(z)} above the flat edge", below=ox * scale + 8)
    return view


def anchor_rear(sheet, p: Params, solid: cq.Solid, centre: tuple[float, float], scale: float, title: str) -> View:
    """Rear view of the anchored bracket: the saddle's width and height. `centre` is the sheet position of the model's X=0, Z=0 point."""
    ox, _ = anchor_extent(p)
    proj = project(solid.wrapped, (0, 1, 0), (0, 0, 1))   # view x = -model X
    view = View(sheet, proj, centre, scale).draw()
    view.dim_h(-ox, ox, 0, -7)
    view.dim_v(0, p.saddle_height, ox, 7)
    view.dim_v(0, p.height, -ox, -8)
    view.caption(title, "rear end", below=14)
    return view


def anchor_notes(p: Params) -> str:
    """The anchor's note line, from the same parameters."""
    ox, _ = anchor_extent(p)
    wide = "collar around the rear leg" if ox > p.thickness / 2 else "saddle on the rear end"
    return (f"Anchor: {wide}, {fmt(p.saddle_height)} high, {fmt(p.saddle_leg)} legs, {fmt(p.saddle_bar)} bar behind a {fmt(p.tie_slot_width)} x "
            f"{fmt(p.tie_slot_depth)} tie slot. Zip tie runs through the slot and round a tube or to the wall plate.")


def face_view(sheet, p: Params, solid: cq.Solid, left: float, base: float, face: int, ys: list, scale: float, title: str, detail: str,
              full: bool = False) -> View:
    """Look at one long face of the bracket (face +1 is the +X face, -1 the -X face) with its bar sockets dimensioned along the length.

    `left` and `base` are the sheet position of the view's lower-left corner. The -X face is seen from the other side, so the length runs the
    other way and the dimensions are mirrored with it. `full` adds the leg, height, rail and corner dimensions."""
    L, H, R, G = p.length, p.height, p.rail_height, p.leg_length

    def f(y: float) -> float:   # model Y to view x
        return y if face > 0 else -y

    view = View.at_corner(sheet, project(solid.wrapped, (face, 0, 0), (0, 0, 1)), (left, base), scale).draw()
    pts = sorted(f(y) for y in [0.0, *ys, L])
    for a, b in zip(pts, pts[1:]):
        view.dim_h(a, b, 0, -9)
    view.dim_h(pts[0], pts[-1], 0, -17)
    x0, y0, x1, y1 = view.box()
    if full:
        view.dim_h(f(0), f(G), H, 7)
        view.dim_v(0, H, f(L), 9 * face)
        view.dim_v(0, R, f(L), 17 * face)
        view.leader((f(G + p.corner_radius * 0.29), R + p.corner_radius * 0.29), (x0 + 14, y1 + 14), f"R{fmt(p.corner_radius)}")
    if ys:
        y = ys[min(1, len(ys) - 1)]
        view.leader((f(y) + p.bore / 2 * 0.7, p.bar_z + p.bore / 2 * 0.7), (x0 + 100, y1 + 14),
                    f"{len(ys)}x {fmt(p.bore)} dia, {fmt(p.bar_depth)} deep on this face")
    view.caption(title, detail, below=21)
    return view


def face_section(sheet, p: Params, solid: cq.Solid, face: int, y_cut: float, origin: tuple[float, float], scale: float, title: str) -> View:
    """Section through a bar socket on a bracket with sockets on one side only, enlarged. `origin` is the sheet position of model X=0, Z=0."""
    half, R = p.thickness / 2, p.rail_height
    slab = solid.intersect(cq.Solid.makeBox(200, SLAB, 200, pnt=cq.Vector(-100, y_cut - SLAB / 2, -50)))
    proj = project(slab.wrapped, (0, -1, 0), (0, 0, 1))   # view x = model X
    proj.hidden = []
    view = View(sheet, proj, origin, scale).draw()
    view.hatch(section_loops(solid.wrapped, (0, y_cut, 0), (0, -1, 0), (1, 0, 0)))
    near, far = face * half, -face * half                 # the socket face and the back face
    back = near - face * p.bar_depth                      # the bottom of the socket
    view.dim_h(far, back, R, 6)
    view.dim_h(back, near, R, 6)
    view.dim_h(-half, half, 0, -8)
    view.dim_v(0, R, far, -8 * face)
    lower, upper = p.bar_z - p.bore / 2, R - p.bar_z - p.bore / 2
    sx, sy = view.origin
    view.leader((near - face * 3, lower / 2), (sx + half * scale + 8, sy - 11), f"{fmt(lower)} wall")
    view.leader((near - face * 3, R - upper / 2), (sx + half * scale + 8, sy + R * scale + 6), f"{fmt(upper)} wall")
    view.caption(title, "through a bar socket", below=16)
    return view


def cut_line(sheet, view: View, a: tuple, b: tuple, letter: str) -> None:
    """A cutting-plane line between two model points of `view`, lettered at both ends."""
    pa, pb = view.to_sheet(a)[0], view.to_sheet(b)[0]
    sheet.centre_line(tuple(pa), tuple(pb))
    for q, other in ((pa, pb), (pb, pa)):
        d = (q - other) / max(float(((q - other) ** 2).sum() ** 0.5), 1e-9)
        sheet.text(q[0] + d[0] * 2.5, q[1] + d[1] * 2.5, letter, 7, ha="center", va="center", weight="bold")
