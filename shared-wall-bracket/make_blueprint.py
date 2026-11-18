#!/usr/bin/env python3
"""
Draw a blueprint-style sheet of the shared-wall bracket.

Every view is projected from the CAD model with hidden-line removal, so the
geometry on the sheet is the geometry that gets printed.  Dimensions are
taken from the same Params object the model is built from.

Views (third-angle projection): top, front, bottom, right end, an enlarged
section through a bar socket, and an isometric.

Usage:
    python3 make_blueprint.py                 # writes blueprint.png and blueprint.svg
    python3 make_blueprint.py --log-level DEBUG
"""
import argparse
import logging
import math
from pathlib import Path

import cadquery as cq
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path as MplPath
from OCP.BRepLib import BRepLib
from OCP.BRepTools import BRepTools_WireExplorer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape

from shared_wall_bracket import Params, build_bracket

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(name)s: %(message)s"
log = logging.getLogger("blueprint")

PAPER = "#0b3a82"       # blueprint blue
GRID = "#1d4f9c"
INK = "#f4f8ff"
DIM = "#9fd0ff"
SHEET_W, SHEET_H = 420.0, 297.0   # A3 landscape, in sheet millimetres
SCALE = 0.75                      # sheet mm per model mm for the main views
DETAIL = 1.5                      # sheet mm per model mm for the section
FONT = "DejaVu Sans Mono"


# ----------------------------------------------------------------------------
# Projection
# ----------------------------------------------------------------------------
def _sample(edge: cq.Edge) -> np.ndarray:
    n = 2 if edge.geomType() == "LINE" else 28
    return np.array([[*edge.positionAt(t).toTuple()] for t in np.linspace(0, 1, n)])


def project(shape: cq.Shape, toward_viewer, x_dir):
    """Hidden-line projection.  Returns (visible, hidden) lists of Nx2 polylines."""
    hlr = HLRBRep_Algo()
    hlr.Add(shape.wrapped)
    hlr.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*toward_viewer), gp_Dir(*x_dir))))
    hlr.Update()
    hlr.Hide()
    out = HLRBRep_HLRToShape(hlr)

    def polylines(compounds):
        lines = []
        for comp in compounds:
            if comp is None or comp.IsNull():
                continue
            BRepLib.BuildCurves3d_s(comp)
            for edge in cq.Shape.cast(comp).Edges():
                lines.append(_sample(edge)[:, :2])
        return lines

    visible = polylines([out.VCompound(), out.OutLineVCompound()])
    hidden = polylines([out.HCompound(), out.OutLineHCompound()])
    log.debug("projection %s: %d visible, %d hidden edges", toward_viewer, len(visible), len(hidden))
    return visible, hidden


def section_loops(shape: cq.Shape, y: float):
    """Closed loops (in X, Z) of the cut face at the given Y."""
    plane = cq.Face.makePlane(400, 400, basePnt=(0, y, 0), dir=(0, 1, 0))
    loops = []
    for face in plane.intersect(shape).Faces():
        for wire in [face.outerWire()] + face.innerWires():
            pts, first = [], None
            explorer = BRepTools_WireExplorer(wire.wrapped)
            while explorer.More():
                seg = _sample(cq.Edge(explorer.Current()))
                # Chain edges head to tail whatever their stored orientation.
                if first is not None:
                    # Orient the first edge so that it ends where the second begins.
                    if min(np.linalg.norm(first[0] - seg[0]), np.linalg.norm(first[0] - seg[-1])) < \
                       min(np.linalg.norm(first[-1] - seg[0]), np.linalg.norm(first[-1] - seg[-1])):
                        first = first[::-1]
                    pts.extend(first)
                    first = None
                if not pts:
                    first = seg
                else:
                    if np.linalg.norm(pts[-1] - seg[0]) > np.linalg.norm(pts[-1] - seg[-1]):
                        seg = seg[::-1]
                    pts.extend(seg)
                explorer.Next()
            if first is not None:      # a wire made of a single closed edge
                pts.extend(first)
            loops.append(np.array(pts)[:, [0, 2]])
    return loops


# ----------------------------------------------------------------------------
# Drawing helpers (all coordinates in sheet millimetres)
# ----------------------------------------------------------------------------
class View:
    """Places model-space 2D geometry on the sheet."""

    def __init__(self, ax, origin, scale, flip_x=False):
        self.ax, self.origin, self.scale, self.flip_x = ax, np.array(origin, float), scale, flip_x

    def to_sheet(self, pts):
        pts = np.atleast_2d(np.array(pts, float)).copy()
        if self.flip_x:
            pts[:, 0] = -pts[:, 0]
        return self.origin + pts * self.scale

    def lines(self, visible, hidden):
        for line in hidden:
            s = self.to_sheet(line)
            self.ax.plot(s[:, 0], s[:, 1], color=INK, lw=0.45, alpha=0.75, dashes=(4, 2.5), solid_capstyle="butt")
        for line in visible:
            s = self.to_sheet(line)
            self.ax.plot(s[:, 0], s[:, 1], color=INK, lw=1.15, solid_capstyle="round")

    def label(self, text, model_xy, dy=-7.0):
        s = self.to_sheet(model_xy)[0]
        self.ax.text(s[0], s[1] + dy, text, color=INK, fontsize=7.5, fontfamily=FONT, ha="center", va="top", weight="bold")

    def dim_h(self, x0, x1, y_ref, offset, text=None, ext=True):
        """Horizontal dimension between model x0 and x1, drawn `offset` sheet mm from model y_ref."""
        a, b = self.to_sheet((x0, y_ref))[0], self.to_sheet((x1, y_ref))[0]
        y = a[1] + offset
        _dim(self.ax, (a[0], y), (b[0], y), text or _fmt(abs(x1 - x0)))
        if ext:
            for p in (a, b):
                self.ax.plot([p[0], p[0]], [p[1] + math.copysign(1.2, offset), y + math.copysign(1.5, offset)], color=DIM, lw=0.4)

    def dim_v(self, y0, y1, x_ref, offset, text=None, ext=True):
        a, b = self.to_sheet((x_ref, y0))[0], self.to_sheet((x_ref, y1))[0]
        x = a[0] + offset
        _dim(self.ax, (x, a[1]), (x, b[1]), text or _fmt(abs(y1 - y0)), vertical=True)
        if ext:
            for p in (a, b):
                self.ax.plot([p[0] + math.copysign(1.2, offset), x + math.copysign(1.5, offset)], [p[1], p[1]], color=DIM, lw=0.4)

    def leader(self, model_xy, text_xy, text, ha="left"):
        s = self.to_sheet(model_xy)[0]
        self.ax.annotate(text, xy=s, xytext=text_xy, color=DIM, fontsize=6.2, fontfamily=FONT, ha=ha, va="center",
                         arrowprops=dict(arrowstyle="-|>", color=DIM, lw=0.5, shrinkA=1.5, shrinkB=0, mutation_scale=6))


def _fmt(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _dim(ax, p0, p1, text, vertical=False):
    ax.annotate("", xy=p0, xytext=p1, arrowprops=dict(arrowstyle="<|-|>", color=DIM, lw=0.5, shrinkA=0, shrinkB=0, mutation_scale=6))
    mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    ax.text(mid[0], mid[1], text, color=DIM, fontsize=6.2, fontfamily=FONT, ha="center", va="center",
            rotation=90 if vertical else 0,
            bbox=dict(boxstyle="square,pad=0.15", fc=PAPER, ec="none"))


def sheet(ax):
    ax.add_patch(Rectangle((0, 0), SHEET_W, SHEET_H, fc=PAPER, ec="none", zorder=-10))
    for x in np.arange(10, SHEET_W, 10):
        ax.plot([x, x], [8, SHEET_H - 8], color=GRID, lw=0.25, zorder=-9)
    for y in np.arange(10, SHEET_H, 10):
        ax.plot([8, SHEET_W - 8], [y, y], color=GRID, lw=0.25, zorder=-9)
    ax.add_patch(Rectangle((8, 8), SHEET_W - 16, SHEET_H - 16, fc="none", ec=INK, lw=1.4))
    ax.add_patch(Rectangle((10, 10), SHEET_W - 20, SHEET_H - 20, fc="none", ec=INK, lw=0.5))


def title_block(ax, p: Params):
    x0, y0, w, h = 262.0, 10.0, 148.0, 46.0
    ax.add_patch(Rectangle((x0, y0), w, h, fc=PAPER, ec=INK, lw=1.0, zorder=5))
    for y in (y0 + 12, y0 + 22, y0 + 32):
        ax.plot([x0, x0 + w], [y, y], color=INK, lw=0.5, zorder=6)
    ax.plot([x0 + 82, x0 + 82], [y0, y0 + 22], color=INK, lw=0.5, zorder=6)

    def cell(x, y, head, body, size=7.5):
        ax.text(x, y + 7.6, head, color=DIM, fontsize=4.6, fontfamily=FONT, va="top", zorder=7)
        ax.text(x, y + 1.6, body, color=INK, fontsize=size, fontfamily=FONT, va="bottom", zorder=7)

    ax.text(x0 + 3, y0 + 39, "SHARED-WALL BRACKET", color=INK, fontsize=13, fontfamily=FONT, weight="bold", va="center", zorder=7)
    cell(x0 + 3, y0 + 22, "FOR", "9-tier modular filament storage rack (Amazon B0FFZ8SSQX)", 6.0)
    cell(x0 + 3, y0 + 12, "SCALE", "1:1.33 (section 1.5:1)", 6.5)
    cell(x0 + 85, y0 + 12, "UNITS / PROJECTION", "mm, third angle", 6.5)
    cell(x0 + 3, y0, "MATERIAL", "ABS or PETG. Not PLA.", 6.5)
    cell(x0 + 85, y0, "SOURCE", "shared_wall_bracket.py", 6.5)


def notes(ax, p: Params):
    text = (
        "NOTES\n"
        f"1. Tubes are {_fmt(p.tube_od)} dia. All sockets are {_fmt(p.bore)} dia, {_fmt(p.bar_depth)} deep, with a {_fmt(p.chamfer)} lead-in.\n"
        f"2. Bar sockets: 4 on each long face, centred {_fmt(p.bar_z)} above the flat edge.\n"
        f"3. Upright sockets: one from each end of each leg, on the centre line, {_fmt(p.divider)} divider between,\n"
        f"   {_fmt(p.upright_vent_d)} dia hole through the divider.\n"
        "4. Print flat edge down, no supports. 5 wall loops (Arachne), 15% gyroid infill.\n"
        "5. Untested hobby design. No load rating. See DISCLAIMER.md."
    )
    ax.text(14, 54, text, color=INK, fontsize=5.8, fontfamily=FONT, va="top", linespacing=1.45)


# ----------------------------------------------------------------------------
# Sheet
# ----------------------------------------------------------------------------
def draw(p: Params, out_stem: Path) -> None:
    solid = build_bracket(p).val()
    L, H, T, R, G = p.length, p.height, p.thickness, p.rail_height, p.leg_length
    half_t = T / 2
    log.info("projecting views of a %.0f x %.0f x %.0f mm part", T, L, H)

    fig = plt.figure(figsize=(SHEET_W / 25.4, SHEET_H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, SHEET_W)
    ax.set_ylim(0, SHEET_H)
    ax.set_aspect("equal")
    ax.axis("off")
    sheet(ax)

    x_left = 34.0
    # --- Front view: looking at a hole face.  Model (Y, Z) -> sheet. ---------
    front = View(ax, (x_left, 150.0), SCALE)
    front.lines(*project(solid, (1, 0, 0), (0, 1, 0)))
    front.label("FRONT (bar-socket face; the back is identical)", (L / 2, 0), dy=-26)
    xs = [0.0] + list(p.bar_y) + [L]
    for a, b in zip(xs, xs[1:]):
        front.dim_h(a, b, 0, -9)
    front.dim_h(0, L, 0, -17)
    front.dim_h(0, G, H, 7)
    front.dim_v(0, H, L, 9)
    front.dim_v(0, R, L, 17)
    front.dim_v(0, p.bar_z, p.bar_y[2], -14, ext=False)
    front.leader((p.bar_y[1] + p.bore / 2 * 0.7, p.bar_z + p.bore / 2 * 0.7), (x_left + 70, 186),
                 f"8x {_fmt(p.bore)} dia, {_fmt(p.bar_depth)} deep (4 per face)")
    front.leader((G + p.corner_radius * 0.29, R + p.corner_radius * 0.29), (x_left + 22, 186), f"R{_fmt(p.corner_radius)}")
    # Section marker through the second bar socket.
    sy = p.bar_y[1]
    a, b = front.to_sheet((sy, -4))[0], front.to_sheet((sy, H + 3))[0]
    ax.plot([a[0], a[0]], [a[1], b[1]], color=INK, lw=0.7, dashes=(9, 2, 2, 2))
    for q in (a, b):
        ax.text(q[0] - 2.2, q[1], "A", color=INK, fontsize=7, fontfamily=FONT, weight="bold", ha="right", va="center")

    # --- Top view: looking down on the leg ends.  Model (Y, -X). -------------
    top = View(ax, (x_left, 232.0), SCALE)
    top.lines(*project(solid, (0, 0, 1), (0, 1, 0)))
    top.label("TOP (leg ends)", (L / 2, -half_t), dy=-5)
    top.dim_v(-half_t, half_t, 0, -9)
    top.dim_h(0, p.upright_from_end, half_t, 7)
    top.leader((L - p.upright_from_end + p.bore / 2 * 0.7, p.bore / 2 * 0.7), (x_left + 150, 262),
               f"4x {_fmt(p.bore)} dia, {_fmt(p.upright_depth_leg)} deep (2 here, 2 on the flat edge)", ha="left")
    top.leader((p.plan_round * 0.29, half_t - p.plan_round * 0.29), (x_left + 22, 262), f"R{_fmt(p.plan_round)}")

    # --- Bottom view: the flat edge that sits on the print bed. --------------
    bottom = View(ax, (x_left, 88.0), SCALE)
    bottom.lines(*project(solid, (0, 0, -1), (0, 1, 0)))
    bottom.label("BOTTOM (flat edge; print bed face)", (L / 2, -half_t), dy=-5)

    # --- Right end view.  Model (-X, Z). --------------------------------------
    end_x = x_left + L * SCALE + 46
    end = View(ax, (end_x, 150.0), SCALE)
    end.lines(*project(solid, (0, 1, 0), (-1, 0, 0)))
    end.label("END", (0, 0), dy=-26)
    end.dim_h(-half_t, half_t, 0, -9)
    end.dim_v(H - p.upright_depth_leg, H, half_t, 8, ext=True)
    end.dim_v(p.upright_depth_flat, H - p.upright_depth_leg, half_t, 16, ext=True)

    # --- Section A-A through a bar socket, enlarged.  Model (X, Z). -----------
    sec_origin = (end_x + 62, 208.0)
    sec = View(ax, sec_origin, DETAIL)
    # Project a thin slice at the cut plane, so the view shows the cut face
    # alone and not the leg that lies beyond it.
    slab = solid.intersect(cq.Solid.makeBox(200, 0.4, 200, pnt=cq.Vector(-100, sy, -50)))
    sec.lines(project(slab, (0, -1, 0), (1, 0, 0))[0], [])
    codes, verts = [], []
    for loop in section_loops(solid, sy):
        s = sec.to_sheet(loop)
        verts.extend(s.tolist())
        codes.extend([MplPath.MOVETO] + [MplPath.LINETO] * (len(s) - 2) + [MplPath.CLOSEPOLY])
    if verts:
        ax.add_patch(PathPatch(MplPath(verts, codes), fc="none", ec=DIM, lw=0, hatch="////", alpha=0.9))
    sec.label("SECTION A-A (bar sockets)", (0, 0), dy=-22)
    sec.dim_h(-half_t, -p.web / 2, R, 6)
    sec.dim_h(-p.web / 2, p.web / 2, R, 6)
    sec.dim_h(p.web / 2, half_t, R, 6)
    sec.dim_h(-half_t, half_t, 0, -8)
    sec.dim_v(0, R, half_t, 8)
    lower_wall = p.bar_z - p.bore / 2
    upper_wall = R - p.bar_z - p.bore / 2
    sec.leader((-half_t + 9, lower_wall / 2), (sec_origin[0] - 38, sec_origin[1] - 11), f"{_fmt(lower_wall)} wall", ha="right")
    sec.leader((-half_t + 9, R - upper_wall / 2), (sec_origin[0] - 38, sec_origin[1] + R * DETAIL + 4), f"{_fmt(upper_wall)} wall", ha="right")

    # --- Isometric. ------------------------------------------------------------
    n = np.array([1.0, -1.0, 0.8])
    n /= np.linalg.norm(n)
    x_dir = np.array([1.0, 1.0, 0.0]) / math.sqrt(2)
    iso = View(ax, (end_x + 8, 92.0), 0.36)
    visible, _ = project(solid, tuple(n), tuple(x_dir))
    iso.lines(visible, [])
    ax.text(end_x + 52, 64, "ISOMETRIC (not to scale)", color=INK, fontsize=7.5, fontfamily=FONT, ha="center", weight="bold")

    title_block(ax, p)
    notes(ax, p)

    for ext, dpi in (("png", 200), ("svg", None)):
        path = out_stem.with_suffix(f".{ext}")
        fig.savefig(path, dpi=dpi, facecolor=PAPER)
        log.info("wrote %s (%d bytes)", path, path.stat().st_size)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=Path(__file__).with_name("blueprint"),
                    help="output path without extension")
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
