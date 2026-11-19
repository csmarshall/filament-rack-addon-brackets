"""
Drawing pieces the shared-wall bracket's blueprint sheets have in common (make_blueprint.py, make_blueprint_staggered.py,
make_blueprint_end.py): the face views, the section through a bar socket and the tie slit. Every view is projected from the CAD model and every number is
read from the Params it was built from.
"""
import cadquery as cq

from blueprint import View, fmt, project, section_loops
from shared_wall_bracket import Params

END_LABEL_DROP = 22.0   # sheet mm under a view where the end labels sit, clear of its dimension lines
END_LABEL_SIZE = 5.0
SLAB = 0.4          # thickness of the slice projected for a section, model mm
SLIT_DETAIL_PAD = 2.5   # model mm of plastic shown round the slit's mouth in its detail
SLIT_NOTE_DROP = 14.0   # sheet mm above a face view where the slit callout sits, level with the socket callout


INSTALLED_NOTE = "Installed, the flat edge is on top; the views show the part as printed, flat edge down."


def end_labels(sheet, view: View, p: Params, flip: bool = False, drop: float = END_LABEL_DROP) -> None:
    """Name the two ends of the bracket `drop` sheet mm under a view that shows its length: the FRONT END is Y = 0, which faces the room when the rack
    stands against the wall, and the BACK END is Y = length, against the wall. `flip` is for a view from the -X side, where Y runs right to left."""
    x0, y0, x1, y1 = view.box()
    y = y0 - drop
    front_x = float(view.to_sheet((-0.0, 0))[0][0])
    back_x = float(view.to_sheet((-p.length if flip else p.length, 0))[0][0])
    a, b = ("FRONT END", "BACK END") if not flip else ("BACK END", "FRONT END")
    sheet.text(min(front_x, back_x), y, a, END_LABEL_SIZE, ha="left", va="center", weight="bold")
    sheet.text(max(front_x, back_x), y, b, END_LABEL_SIZE, ha="right", va="center", weight="bold")


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
    slit_leader(view, p, flip=face < 0)
    view.caption(title, detail, below=21)
    end_labels(sheet, view, p, flip=face < 0)
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


def slit_text(p: Params) -> str:
    """The slit callout, from the same parameters the slits are cut from."""
    return f"{len(p.tie_slit_ys)}x {fmt(p.tie_slit_height)} x {fmt(p.tie_slit_width)} tie slit"


def slit_leader(view: View, p: Params, flip: bool = False) -> None:
    """Call out the tie slit on a face view, from the top of the right-most slit to text above the view."""
    if not p.tie_slit_ys:
        return
    y = max(p.tie_slit_ys, key=lambda v: -v if flip else v)
    x_view = -y if flip else y
    x0, y0, x1, y1 = view.box()
    at = float(view.to_sheet((x_view, 0))[0][0])
    view.leader((x_view, p.tie_slit_z + p.tie_slit_mouth[0] / 2), (at - 3, y1 + SLIT_NOTE_DROP), slit_text(p))


def slit_position_dims(view: View, p: Params, offset: float = -9.0) -> None:
    """Dimension where the slits are along the length, under a top view (view x = model Y): from the front end to the first slit, between the
    slits, and from the last slit to the back end. The extension lines drop from the part's edge, over the slit's hidden outline."""
    half = p.thickness / 2
    pts = [0.0, *p.tie_slit_ys, p.length]
    for a, b in zip(pts, pts[1:]):
        view.dim_h(a, b, -half, offset)


def slit_detail(sheet, p: Params, solid: cq.Solid, corner: tuple[float, float], scale: float, title: str, callout: bool = True) -> View:
    """The first tie slit seen face on, enlarged, with its size and lead-in. The projection is of the part cut down to a window round the slit, so
    its outline is the window's. `corner` is the sheet position of the window's lower-left corner."""
    y, zc = p.tie_slit_ys[0], p.tie_slit_z
    mh, mw = p.tie_slit_mouth
    y0, y1 = y - mw / 2 - SLIT_DETAIL_PAD, y + mw / 2 + SLIT_DETAIL_PAD
    z0, z1 = zc - mh / 2 - SLIT_DETAIL_PAD, zc + mh / 2 + SLIT_DETAIL_PAD
    reach = p.thickness / 2 + 1.0
    window = solid.intersect(cq.Solid.makeBox(2 * reach, y1 - y0, z1 - z0, pnt=cq.Vector(-reach, y0, z0)))
    proj = project(window.wrapped, (1, 0, 0), (0, 0, 1))   # view x = model Y, view y = model Z
    proj.hidden = []
    view = View.at_corner(sheet, proj, corner, scale).draw(centre_marks=False)
    side = (mw / 2 + SLIT_DETAIL_PAD) * scale
    view.dim_v(zc - p.tie_slit_height / 2, zc + p.tie_slit_height / 2, y, side + 6)
    view.dim_v(zc - mh / 2, zc + mh / 2, y, side + 15)
    view.dim_h(y - p.tie_slit_width / 2, y + p.tie_slit_width / 2, zc, 0, ext=False)
    lead = f"{fmt(p.tie_slit_lead_in)} x 45 deg lead-in"
    if callout:
        bx, by = view.to_sheet((y + mw / 2, zc + mh / 2 * 0.6))[0]
        view.leader((y + mw / 2 - p.tie_slit_lead_in * 0.5, zc + p.tie_slit_height / 2 * 0.6 + p.tie_slit_lead_in * 0.3),
                    (bx + 6, float(view.box()[3]) + 5), f"{lead}, both faces")
        view.caption(title, f"{fmt(mw)} wide at the face", below=8)
    else:   # a short caption for a sheet with no room for the callout
        view.caption(title, lead, below=8)
    return view


def slit_notes(p: Params) -> str:
    """The slits' note line, from the same parameters."""
    return (f"Tie slits: {len(p.tie_slit_ys)}, face to face, {fmt(p.tie_slit_height)} x {fmt(p.tie_slit_width)}, rounded ends, {fmt(p.tie_slit_from_end)} from each end, "
            f"{fmt(p.tie_slit_z)} above the flat edge, {fmt(p.tie_slit_lead_in)} x 45 deg lead-in both faces. Zip tie through either slit to the wall plate. "
            "No weaker than a bar socket (checked on every build).")
