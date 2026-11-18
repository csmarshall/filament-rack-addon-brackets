#!/usr/bin/env python3
"""
Shared-wall end frame for the Hizypaixin 9-tier filament rack (Amazon B0FFZ8SSQX).

The stock rack is a "shoe rack" style frame: each tier has two plastic end
frames (running front-to-back) with sockets for vertical tubes at the corners
and sockets on ONE face for the four horizontal bars.  This part is a
double-sided replacement end frame: bar sockets on BOTH faces, so two columns
can share a single centre wall (one set of vertical tubes instead of two).

Coordinate system (as printed, flat on the bed):
    X = across the rack (direction the horizontal bars run)
    Y = front-to-back (the long axis of this part)
    Z = vertical (direction the upright tubes run)

Usage:
    python3 shared_wall_bracket.py                # writes STEP + STL to ./out
    python3 shared_wall_bracket.py --log-level DEBUG
    python3 shared_wall_bracket.py --tube-od 12.9 --post-spacing 281.5

EVERY dimension marked MEASURE below is a best guess from the listing photos.
Measure the stock end frame with calipers and print the test coupon first.
"""

import argparse
import logging
from dataclasses import dataclass, field
from pathlib import Path

import cadquery as cq

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(name)s: %(message)s"
log = logging.getLogger("shared_wall")


@dataclass
class Params:
    # --- MEASURE: tubes ------------------------------------------------------
    tube_od_v: float = 12.7        # OD of the upright (vertical) tubes
    tube_od_h: float = 12.7        # OD of the horizontal bars
    fit_clearance: float = 0.25    # added to socket DIAMETER; tune with the coupon

    # --- MEASURE: stock end frame geometry -----------------------------------
    post_spacing: float = 280.0    # centre-to-centre, front upright to back upright
    # Y position of every horizontal bar, measured from the FRONT upright centre.
    # Stock frame has 4 bars: front, two intermediates, back.
    bar_y: list = field(default_factory=lambda: [0.0, 145.0, 219.0, 280.0])
    v_socket_depth_bottom: float = 20.0   # how far the tube BELOW seats into the frame
    v_socket_depth_top: float = 20.0      # how far the tube ABOVE seats into the frame
    # Solid stop between the upper and lower upright sockets.  This MUST match
    # the stock part (stock corner height - top depth - bottom depth) or the
    # shared wall grows/shrinks relative to the outer walls on every tier.
    v_stop: float = 3.0
    bar_z: float = 21.5            # bar centreline height above the frame's bottom face
    h_socket_depth: float = 18.0   # how far each horizontal bar seats into the frame

    # --- Design choices (safe to leave alone) --------------------------------
    wall: float = 3.2              # plastic wall around every socket
    core_wall: float = 2.4         # min plastic between a bar socket and an upright socket
    rail_width: float = 10.0       # X thickness of the rail between sockets
    chamfer: float = 0.8           # lead-in on socket mouths
    anchor: bool = False           # add a rear screw flange for wall anchoring
    anchor_screw_d: float = 5.0    # clearance hole for a #10 / M5 screw
    anchor_thickness: float = 4.0

    # --- Derived --------------------------------------------------------------
    @property
    def height(self) -> float:
        """Overall Z height of the upright bosses (= stock corner height)."""
        return self.v_socket_depth_bottom + self.v_stop + self.v_socket_depth_top

    @property
    def bore_v(self) -> float:
        return self.tube_od_v + self.fit_clearance

    @property
    def bore_h(self) -> float:
        return self.tube_od_h + self.fit_clearance

    @property
    def boss_r_v(self) -> float:
        return self.bore_v / 2 + self.wall

    @property
    def boss_r_h(self) -> float:
        return self.bore_h / 2 + self.wall

    @property
    def web(self) -> float:
        """X thickness of the solid centre web between left and right bar sockets.

        Wide enough that a bar socket can never break into an upright socket,
        whatever bar_z is."""
        return self.bore_v + 2 * self.core_wall

    @property
    def x_total(self) -> float:
        return self.web + 2 * self.h_socket_depth

    def validate(self) -> None:
        if self.bar_z - self.bore_h / 2 < 1.2:
            raise ValueError("bar_z too low: bar socket would break through the bottom face")
        if min(self.bar_y) < 0 or max(self.bar_y) > self.post_spacing:
            raise ValueError("bar_y entries must lie between 0 and post_spacing")
        if self.fit_clearance < 0:
            raise ValueError("fit_clearance must be >= 0")
        if self.anchor and self.height - (self.bar_z + self.boss_r_h) < self.anchor_screw_d + 3:
            raise ValueError("not enough room above the bar boss for the anchor screw")


def _x_cylinder(radius: float, length: float, y: float, z: float) -> cq.Workplane:
    """Cylinder with its axis along X, centred on x=0."""
    return (
        cq.Workplane("YZ")
        .workplane(offset=-length / 2)
        .center(y, z)
        .circle(radius)
        .extrude(length)
    )


def _cone(origin, direction, r_mouth: float, r_inner: float, depth: float) -> cq.Workplane:
    """Truncated cone starting at `origin` (the socket mouth) and narrowing along `direction`."""
    solid = cq.Solid.makeCone(r_mouth, r_inner, depth, pnt=cq.Vector(*origin), dir=cq.Vector(*direction))
    return cq.Workplane("XY").add(solid)


def build_bracket(p: Params) -> cq.Workplane:
    """Build the double-sided end frame."""
    p.validate()
    log.info(
        "Building bracket: %.1f x %.1f x %.1f mm (X x Y x Z), anchor=%s",
        p.x_total, p.post_spacing + 2 * p.boss_r_v, p.height, p.anchor,
    )
    log.debug("bore_v=%.2f bore_h=%.2f web=%.2f boss_r_v=%.2f boss_r_h=%.2f",
              p.bore_v, p.bore_h, p.web, p.boss_r_v, p.boss_r_h)

    rail_top = p.bar_z + p.boss_r_h
    post_ys = [0.0, p.post_spacing]

    # Centre rail tying front and back uprights together.
    body = (
        cq.Workplane("XY")
        .box(min(p.rail_width, p.web), p.post_spacing, rail_top, centered=(True, False, False))
    )

    # Upright bosses (full height).
    for y in post_ys:
        body = body.union(
            cq.Workplane("XY").center(0, y).circle(p.boss_r_v).extrude(p.height)
        )
        # Square the web out to full height around the post so the bar bosses
        # at the corners have something solid to grow out of.
        body = body.union(
            cq.Workplane("XY").center(0, y).rect(p.web, 2 * p.boss_r_v).extrude(p.height)
        )

    # Bar bosses: a cylinder along X, with a box underneath down to the bed so
    # the part prints flat with no supports.
    for y in p.bar_y:
        log.debug("bar boss at y=%.1f", y)
        body = body.union(_x_cylinder(p.boss_r_h, p.x_total, y, p.bar_z))
        body = body.union(
            cq.Workplane("XY")
            .center(0, y)
            .rect(p.x_total, 2 * p.boss_r_h)
            .extrude(p.bar_z)
        )

    # Optional rear flange: two screw holes above the back bar bosses, flush
    # with the rear plane of the rack, for anchoring to a wall/stud.
    if p.anchor:
        y_back = p.post_spacing + p.boss_r_v
        flange = (
            cq.Workplane("XY")
            .box(p.x_total, p.anchor_thickness, p.height, centered=(True, False, False))
            .translate((0, y_back - p.anchor_thickness, 0))
        )
        body = body.union(flange)
        screw_x = (p.boss_r_v + p.x_total / 2) / 2
        screw_z = (rail_top + p.height) / 2
        for sx in (-screw_x, screw_x):
            hole = (
                cq.Workplane("XZ")
                .workplane(offset=-(y_back + 1))
                .center(sx, screw_z)
                .circle(p.anchor_screw_d / 2)
                .extrude(p.anchor_thickness + 2)
            )
            body = body.cut(hole)
        log.debug("anchor holes at x=+/-%.1f z=%.1f", screw_x, screw_z)

    # Upright sockets: blind from the bottom and from the top, solid stop between.
    for y in post_ys:
        lower = cq.Workplane("XY").center(0, y).circle(p.bore_v / 2).extrude(p.v_socket_depth_bottom)
        upper = (
            cq.Workplane("XY")
            .workplane(offset=p.height - p.v_socket_depth_top)
            .center(0, y)
            .circle(p.bore_v / 2)
            .extrude(p.v_socket_depth_top)
        )
        body = body.cut(lower).cut(upper)

    # Bar sockets: blind from each X face, stopping at the centre web.
    for y in p.bar_y:
        for sign in (-1, 1):
            sock = (
                cq.Workplane("YZ")
                .workplane(offset=sign * p.web / 2)
                .center(y, p.bar_z)
                .circle(p.bore_h / 2)
                .extrude(sign * p.h_socket_depth)
            )
            body = body.cut(sock)

    # Lead-in on every socket mouth, cut as a short cone (more robust than
    # asking the kernel to chamfer edges on a heavily booleaned solid).
    if p.chamfer > 0:
        c = p.chamfer
        for y in post_ys:
            body = body.cut(_cone((0, y, 0), (0, 0, 1), p.bore_v / 2 + c, p.bore_v / 2, c))
            body = body.cut(_cone((0, y, p.height), (0, 0, -1), p.bore_v / 2 + c, p.bore_v / 2, c))
        for y in p.bar_y:
            for sign in (-1, 1):
                body = body.cut(_cone((sign * p.x_total / 2, y, p.bar_z), (-sign, 0, 0),
                                      p.bore_h / 2 + c, p.bore_h / 2, c))

    return body


def build_coupon(p: Params) -> cq.Workplane:
    """Small fit-test piece: one upright socket and one bar socket.

    Print this first, test it on a real tube, adjust fit_clearance, repeat."""
    log.info("Building fit-test coupon (bore_v=%.2f, bore_h=%.2f)", p.bore_v, p.bore_h)
    depth_v = min(p.v_socket_depth_top, 12.0)
    block_x = p.boss_r_v + p.core_wall + p.h_socket_depth
    height = max(depth_v + 2.0, 2 * p.boss_r_h)
    body = (
        cq.Workplane("XY").circle(p.boss_r_v).extrude(height)
        .union(cq.Workplane("XY").box(block_x, 2 * p.boss_r_h, height, centered=(False, True, False)))
    )
    upright = (
        cq.Workplane("XY").workplane(offset=height - depth_v)
        .circle(p.bore_v / 2).extrude(depth_v)
    )
    bar = (
        cq.Workplane("YZ").workplane(offset=block_x)
        .center(0, height / 2).circle(p.bore_h / 2)
        .extrude(-p.h_socket_depth)
    )
    return body.cut(upright).cut(bar)


def export(shape: cq.Workplane, out_dir: Path, name: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for ext in ("step", "stl"):
        path = out_dir / f"{name}.{ext}"
        cq.exporters.export(shape, str(path), tolerance=0.02, angularTolerance=0.1)
        log.info("Wrote %s (%d bytes)", path, path.stat().st_size)
    bb = shape.val().BoundingBox()
    volume_cm3 = shape.val().Volume() / 1000.0
    log.info("%s: bbox %.1f x %.1f x %.1f mm, solid volume %.1f cm^3",
             name, bb.xlen, bb.ylen, bb.zlen, volume_cm3)


def parse_args() -> argparse.Namespace:
    d = Params()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=Path("out"))
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    ap.add_argument("--tube-od", type=float, help="set both upright and bar OD")
    ap.add_argument("--tube-od-v", type=float, default=d.tube_od_v)
    ap.add_argument("--tube-od-h", type=float, default=d.tube_od_h)
    ap.add_argument("--fit-clearance", type=float, default=d.fit_clearance)
    ap.add_argument("--post-spacing", type=float, default=d.post_spacing)
    ap.add_argument("--bar-y", type=float, nargs="+", default=None,
                    help="Y of each bar from the front upright centre, e.g. 0 145 219 280")
    ap.add_argument("--v-depth-bottom", type=float, default=d.v_socket_depth_bottom)
    ap.add_argument("--v-depth-top", type=float, default=d.v_socket_depth_top)
    ap.add_argument("--v-stop", type=float, default=d.v_stop)
    ap.add_argument("--bar-z", type=float, default=d.bar_z)
    ap.add_argument("--h-depth", type=float, default=d.h_socket_depth)
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)

    bar_y = args.bar_y
    if bar_y is None:
        # Scale the default intermediate-bar guesses if only post spacing changed.
        scale = args.post_spacing / Params().post_spacing
        bar_y = [round(y * scale, 2) for y in Params().bar_y]

    base = dict(
        tube_od_v=args.tube_od or args.tube_od_v,
        tube_od_h=args.tube_od or args.tube_od_h,
        fit_clearance=args.fit_clearance,
        post_spacing=args.post_spacing,
        bar_y=bar_y,
        v_socket_depth_bottom=args.v_depth_bottom,
        v_socket_depth_top=args.v_depth_top,
        v_stop=args.v_stop,
        bar_z=args.bar_z,
        h_socket_depth=args.h_depth,
    )
    log.info("Parameters: %s", base)

    try:
        export(build_bracket(Params(**base)), args.out, "shared_wall_bracket")
        export(build_bracket(Params(**base, anchor=True)), args.out, "shared_wall_bracket_anchor")
        export(build_coupon(Params(**base)), args.out, "fit_test_coupon")
    except ValueError as exc:
        log.error("Invalid parameters: %s", exc)
        raise SystemExit(2)
    except Exception:
        log.exception("Model generation failed")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
