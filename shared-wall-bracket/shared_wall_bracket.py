#!/usr/bin/env python3
"""
Shared-wall end frame, v2: modelled on the measured stock bracket.

Stock bracket (Hizypaixin 9-tier filament rack, Amazon B0FFZ8SSQX), as measured:
    305 mm long, 18 mm thick, a straight 18 mm tall rail with one flat edge,
    and an 18 mm long leg at each end that drops to 40 mm with a curved inside
    corner.  Four 12 mm bar holes on one face, starting 2 mm in from the flat
    edge, at 84 mm pitch.  Upright tubes plug into each leg from both ends.

This part is two stock brackets back to back in one piece: same side profile,
40 mm thick, 18 mm deep bar sockets on BOTH faces with a 4 mm web between, and
a single centred row of upright sockets, so two rack columns can share one wall.
Every socket is 18 mm deep, as on the stock part; the upright divider is 4 mm
with a 4 mm through-hole.

Coordinate system (also the print orientation: flat edge on the bed):
    X = thickness (direction the horizontal bars run)
    Y = length, front to back
    Z = height (direction the upright tubes run); z=0 is the flat edge

Usage:
    python3 shared_wall_bracket.py
    python3 shared_wall_bracket.py --log-level DEBUG --fit-clearance 0.35
"""

import argparse
import logging
from dataclasses import dataclass, field
from pathlib import Path

import cadquery as cq

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(name)s: %(message)s"
log = logging.getLogger("shared_wall_v2")


@dataclass
class Params:
    # --- Measured on the stock bracket ---------------------------------------
    length: float = 305.0            # overall, front to back
    height: float = 40.0             # full height at the legs
    rail_height: float = 18.0        # height of the rail between the legs
    leg_length: float = 18.0         # how far each leg runs along the length
    stock_thickness: float = 18.0    # one stock bracket (reference only)
    tube_od: float = 12.0            # uprights and bars
    bar_edge_offset: float = 2.0     # flat edge to the near side of a bar hole
    # Bar hole centres from the front end: first hole starts 20 mm in, 84 mm pitch.
    bar_y: list = field(default_factory=lambda: [26.0, 110.0, 194.0, 278.0])
    upright_depth_flat: float = 18.0  # upright socket depth from the flat edge
    upright_depth_leg: float = 18.0   # upright socket depth from the leg end
    upright_vent_d: float = 4.0       # small through-hole in the divider, as on the stock part
    bar_depth: float = 18.0           # bar socket depth, same as every other socket
    # The solid divider between the two upright sockets is
    # height - upright_depth_flat - upright_depth_leg.  It sets tier pitch and
    # MUST equal the stock part's divider.

    # --- Assumed (not yet measured) ------------------------------------------
    upright_from_end: float = 9.0    # upright socket centre from the end (centred in leg)
    corner_radius: float = 20.0      # curved inside corner between leg and rail

    # --- Design choices -------------------------------------------------------
    # Two 18 mm bar sockets plus a 4 mm centre web.  Bars seat exactly as deep
    # as in a stock bracket, so column width matches a stock rack.
    thickness: float = 40.0
    fit_clearance: float = 0.3       # added to socket DIAMETER; tune with the coupon
    chamfer: float = 0.8             # lead-in on socket mouths
    # Rounding is confined to plastic that carries no load: the four outer
    # vertical corners of the legs.  Every socket wall is left at full thickness.
    plan_round: float = 10.0         # radius on the four outer vertical corners
    # Optional light break on the leg and inside-corner edges.  OFF by default:
    # the CAD kernel carries a fillet along every tangent edge, so it runs on
    # across the leg end and along the rail top and shaves 0.1-0.4 mm off the
    # walls at the socket mouths.  Cosmetic only; enable knowing that cost.
    edge_round: float = 0.0
    anchor: bool = False             # add rear ears with screw holes for wall anchoring
    anchor_ear: float = 16.0         # how far each ear sticks out sideways
    anchor_thickness: float = 4.0
    anchor_screw_d: float = 5.0

    @property
    def bore(self) -> float:
        return self.tube_od + self.fit_clearance

    @property
    def bar_z(self) -> float:
        return self.bar_edge_offset + self.tube_od / 2

    @property
    def divider(self) -> float:
        return self.height - self.upright_depth_flat - self.upright_depth_leg

    @property
    def web(self) -> float:
        """Solid plastic between the left-face and right-face bar sockets."""
        return self.thickness - 2 * self.bar_depth

    def validate(self) -> None:
        if self.divider < 1.0:
            raise ValueError(f"upright sockets leave a {self.divider:.1f} mm divider; need >= 1 mm")
        if self.web < 2.0:
            raise ValueError(f"bar sockets leave a {self.web:.1f} mm centre web; need >= 2 mm")
        if self.corner_radius > self.height - self.rail_height:
            raise ValueError("corner_radius is larger than the step between rail and leg")
        if self.bar_z + self.bore / 2 > self.rail_height - 1.0:
            raise ValueError("bar socket breaks out of the top of the rail")
        if self.plan_round > min(self.thickness / 2 - self.bore / 2 - 3.0, self.leg_length - 2.0):
            raise ValueError("plan_round would thin the wall around an upright socket below 3 mm")
        if self.edge_round > self.rail_height - (self.bar_z + self.bore / 2) - 2.0:
            raise ValueError("edge_round would thin the wall over a bar socket below 2 mm")
        # Bar sockets and upright sockets must not meet anywhere along the length.
        up_lo = self.upright_from_end - self.bore / 2
        up_hi = self.upright_from_end + self.bore / 2
        if up_lo < 1.5 or up_hi > self.leg_length - 1.5:
            raise ValueError("upright socket leaves less than 1.5 mm of wall in the leg")
        for y in self.bar_y:
            for centre in (self.upright_from_end, self.length - self.upright_from_end):
                if abs(y - centre) < self.bore + 1.5:
                    raise ValueError(f"bar socket at y={y} runs into the upright socket at y={centre}")


def _cone(origin, direction, r_mouth: float, r_inner: float, depth: float) -> cq.Workplane:
    """Truncated cone starting at `origin` (a socket mouth) and narrowing along `direction`."""
    solid = cq.Solid.makeCone(r_mouth, r_inner, depth, pnt=cq.Vector(*origin), dir=cq.Vector(*direction))
    return cq.Workplane("XY").add(solid)


def build_bracket(p: Params) -> cq.Workplane:
    """Build the double-sided end frame from the stock side profile."""
    p.validate()
    log.info("Building bracket: %.1f x %.1f x %.1f mm (X x Y x Z), anchor=%s",
             p.thickness, p.length, p.height, p.anchor)
    log.info("Upright divider %.1f mm, bar-socket centre web %.1f mm", p.divider, p.web)
    log.debug("bore=%.2f bar_z=%.2f bar_y=%s", p.bore, p.bar_z, p.bar_y)

    L, H, R, G, r = p.length, p.height, p.rail_height, p.leg_length, p.corner_radius
    k = r * (1 - 0.5 ** 0.5)   # offset of the 45-degree point on each corner arc

    # Side profile in the YZ plane (local x = Y, local y = Z), extruded along X.
    body = (
        cq.Workplane("YZ")
        .moveTo(0, 0).lineTo(L, 0).lineTo(L, H).lineTo(L - G, H)
        .lineTo(L - G, R + r)
        .threePointArc((L - G - k, R + k), (L - G - r, R))
        .lineTo(G + r, R)
        .threePointArc((G + k, R + k), (G, R + r))
        .lineTo(G, H).lineTo(0, H).close()
        .extrude(p.thickness / 2, both=True)
    )

    # Round the four outer vertical corners (the only full-height Z edges).
    if p.plan_round > 0:
        try:
            corners = [e for e in body.edges("|Z").vals() if e.Length() > H - 0.5]
            log.debug("rounding %d vertical corners at r=%.1f", len(corners), p.plan_round)
            body = body.newObject(corners).fillet(p.plan_round)
        except Exception as exc:
            log.error("Corner rounding failed, leaving corners square: %s", exc)

    # Break the top edges in one pass: the side and corner edges of each leg top, plus
    # the side-face edges down the inside corner curves.  One fillet call keeps
    # the rounds continuous.  The rail top is left square (see below).
    if p.edge_round > 0:
        try:
            # Leg-top edges, except the two that run across the thickness
            # (end edge and inner edge): those border the 2.85 mm walls
            # around the upright socket mouth, so they stay square.
            edges = [e for f in body.faces(">Z").vals() for e in f.Edges()
                     if abs(e.Center().x) > p.thickness / 2 - p.plan_round - 0.5]
            for face in body.faces(">X").vals() + body.faces("<X").vals():
                for e in face.Edges():
                    c = e.Center()
                    is_bed_edge = c.z < 1.0
                    is_vertical_corner_seam = min(c.y, L - c.y) < p.plan_round + 1.0 and c.z < H - 1.0
                    is_leg_top = c.z > H - 0.5      # already collected above
                    # The rail-top edges run over the bar socket mouths, where the
                    # wall carries bar load, so they stay square.
                    is_rail_top = abs(c.z - R) < 0.5
                    if not (is_bed_edge or is_vertical_corner_seam or is_leg_top or is_rail_top):
                        edges.append(e)
            log.debug("rounding %d top edges at r=%.1f", len(edges), p.edge_round)
            body = body.newObject(edges).fillet(p.edge_round)
        except Exception as exc:
            log.error("Top-edge rounding failed, leaving those edges sharp: %s", exc)

    # Optional rear ears: thin plates flush with the back of the rack, one each
    # side of the rear leg, above bar level, each with a screw hole.
    if p.anchor:
        inset = p.plan_round   # reach back past the rounded corner into solid plastic
        for sign in (-1, 1):
            x0 = sign * p.thickness / 2
            ear = (
                cq.Workplane("XY")
                .box(p.anchor_ear + inset, p.anchor_thickness, H - R, centered=(False, False, False))
                .translate((x0 - inset if sign > 0 else x0 - p.anchor_ear, L - p.anchor_thickness, R))
            )
            body = body.union(ear)
            hole = (
                cq.Workplane("XZ")
                .workplane(offset=-(L + 1))
                .center(x0 + sign * p.anchor_ear / 2, (R + H) / 2)
                .circle(p.anchor_screw_d / 2)
                .extrude(p.anchor_thickness + 2)
            )
            body = body.cut(hole)
        log.debug("anchor ears added at y=%.1f", L - p.anchor_thickness)

    # Upright sockets: one row down the centre (x=0), blind from each end of the leg.
    upright_ys = [p.upright_from_end, L - p.upright_from_end]
    for y in upright_ys:
        from_flat = cq.Workplane("XY").center(0, y).circle(p.bore / 2).extrude(p.upright_depth_flat)
        from_leg = (
            cq.Workplane("XY").workplane(offset=H - p.upright_depth_leg)
            .center(0, y).circle(p.bore / 2).extrude(p.upright_depth_leg)
        )
        body = body.cut(from_flat).cut(from_leg)
        if p.upright_vent_d > 0:
            vent = cq.Workplane("XY").center(0, y).circle(p.upright_vent_d / 2).extrude(H)
            body = body.cut(vent)

    # Bar sockets: blind from each face, stopping at the centre web.
    for y in p.bar_y:
        for sign in (-1, 1):
            sock = (
                cq.Workplane("YZ")
                .workplane(offset=sign * p.web / 2)
                .center(y, p.bar_z)
                .circle(p.bore / 2)
                .extrude(sign * p.bar_depth)
            )
            body = body.cut(sock)

    # Lead-in on every socket mouth, cut as a short cone.
    if p.chamfer > 0:
        c, rb = p.chamfer, p.bore / 2
        for y in upright_ys:
            body = body.cut(_cone((0, y, 0), (0, 0, 1), rb + c, rb, c))
            body = body.cut(_cone((0, y, H), (0, 0, -1), rb + c, rb, c))
        for y in p.bar_y:
            for sign in (-1, 1):
                body = body.cut(_cone((sign * p.thickness / 2, y, p.bar_z), (-sign, 0, 0), rb + c, rb, c))

    return body


def build_coupon(p: Params) -> cq.Workplane:
    """Fit-test piece: one upright socket and one bar socket at production size."""
    log.info("Building fit-test coupon (bore=%.2f)", p.bore)
    size_x = p.bar_depth + 3.0
    size_y = 2 * p.bore + 9.0
    size_z = max(p.rail_height, 14.0)
    body = cq.Workplane("XY").box(size_x, size_y, size_z, centered=(False, False, False))
    upright = (
        cq.Workplane("XY").workplane(offset=size_z - 12.0)
        .center(size_x / 2, 3.0 + p.bore / 2).circle(p.bore / 2).extrude(12.0)
    )
    bar = (
        cq.Workplane("YZ").workplane(offset=size_x)
        .center(size_y - 3.0 - p.bore / 2, size_z / 2).circle(p.bore / 2)
        .extrude(-p.bar_depth)
    )
    return body.cut(upright).cut(bar)


def _clean_stl(path: Path) -> None:
    """Drop zero-area triangles the tessellator leaves where three rounds meet.

    They are harmless to the shape but make the mesh report open edges, which
    some slicers warn about.  Requires trimesh; skipped with a warning if absent."""
    try:
        import trimesh
    except ImportError:
        log.warning("trimesh not installed; skipping STL clean-up for %s", path.name)
        return
    mesh = trimesh.load(str(path))
    before = len(mesh.faces)
    mesh.merge_vertices()
    mesh.update_faces(mesh.nondegenerate_faces())
    mesh.remove_unreferenced_vertices()
    mesh.export(str(path))
    level = logging.INFO if mesh.is_watertight else logging.ERROR
    log.log(level, "%s: removed %d degenerate triangles, watertight=%s",
            path.name, before - len(mesh.faces), mesh.is_watertight)


def export(shape: cq.Workplane, out_dir: Path, name: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for ext in ("step", "stl"):
        path = out_dir / f"{name}.{ext}"
        cq.exporters.export(shape, str(path), tolerance=0.02, angularTolerance=0.1)
        log.info("Wrote %s (%d bytes)", path, path.stat().st_size)
    _clean_stl(out_dir / f"{name}.stl")
    bb = shape.val().BoundingBox()
    log.info("%s: bbox %.1f x %.1f x %.1f mm, solid volume %.1f cm^3",
             name, bb.xlen, bb.ylen, bb.zlen, shape.val().Volume() / 1000.0)


def parse_args() -> argparse.Namespace:
    d = Params()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=Path("out_v2"))
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    ap.add_argument("--tube-od", type=float, default=d.tube_od)
    ap.add_argument("--fit-clearance", type=float, default=d.fit_clearance)
    ap.add_argument("--bar-depth", type=float, default=d.bar_depth)
    ap.add_argument("--upright-depth-flat", type=float, default=d.upright_depth_flat)
    ap.add_argument("--upright-depth-leg", type=float, default=d.upright_depth_leg)
    ap.add_argument("--upright-from-end", type=float, default=d.upright_from_end)
    ap.add_argument("--corner-radius", type=float, default=d.corner_radius)
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)
    base = dict(
        tube_od=args.tube_od,
        fit_clearance=args.fit_clearance,
        bar_depth=args.bar_depth,
        upright_depth_flat=args.upright_depth_flat,
        upright_depth_leg=args.upright_depth_leg,
        upright_from_end=args.upright_from_end,
        corner_radius=args.corner_radius,
    )
    log.info("Parameters: %s", base)
    try:
        export(build_bracket(Params(**base)), args.out, "shared_wall_bracket_v2")
        export(build_bracket(Params(**base, anchor=True)), args.out, "shared_wall_bracket_v2_anchor")
        export(build_coupon(Params(**base)), args.out, "fit_test_coupon_v2")
    except ValueError as exc:
        log.error("Invalid parameters: %s", exc)
        raise SystemExit(2)
    except Exception:
        log.exception("Model generation failed")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
