#!/usr/bin/env python3
"""
Shared-wall end frame, v2: modelled on the measured stock bracket.

Stock bracket (Hizypaixin 9-tier filament rack, Amazon B0FFZ8SSQX), as measured:
    305 mm long, 18 mm thick, a straight 18 mm tall rail with one flat edge,
    and an 18 mm long leg at each end that drops to 40 mm with a curved inside
    corner.  Four 12 mm bar holes on one face, starting 2 mm in from the flat
    edge, at 84 mm pitch.  Upright tubes plug into each leg from both ends.

This part is two stock brackets back to back in one piece: same side profile,
40 mm thick, 16 mm deep bar sockets on BOTH faces with an 8 mm web between, and
a single centred row of upright sockets, so two rack columns can share one wall.
Upright sockets are 18 mm deep and bar sockets 16 mm, as on the stock part; the upright divider is 4 mm
with a 4 mm through-hole, and each pair of opposite bar sockets is joined by a
4 mm vent through the web.

Coordinate system (also the print orientation: flat edge on the bed):
    X = thickness (direction the horizontal bars run)
    Y = length, front to back
    Z = height (direction the upright tubes run); z=0 is the flat edge

Every bracket has two zip-tie slits through its rail, face to face, for
tethering the rack to a wall plate (see ../anti-tip-wall-plate).  They are
sized so the rail is no weaker there than at its weakest bar socket;
check_tie_slit_strength measures that on the model whenever a bracket is built.

Two layouts are built.  In line (40 mm thick): the two faces' bar sockets sit
end to end, and both columns line up front and back.  Staggered (18 mm thick
like the stock bracket, 320 mm long, with a 27 mm rail): one face's sockets are
shifted 16 mm along the bracket so the two sets pass side by side; it uses less
plastic, but the two columns stand 16 mm apart front to back.  The staggered bracket comes as a mirror-image pair, A
and B, so a row can alternate them and zigzag instead of stepping back.

The end bracket (Params.end) is a single-sided stand-in for the stock bracket at
either end of a row; turned end for end it serves the other end.

Usage:
    python3 shared_wall_bracket.py
    python3 shared_wall_bracket.py --log-level DEBUG --fit-clearance 0.35
"""

import argparse
import logging
from dataclasses import dataclass, field
from pathlib import Path

import cadquery as cq
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(name)s: %(message)s"
log = logging.getLogger("shared_wall_v2")

SECTION_SLAB = 0.2         # thickness of the slice a cross-section is measured on, mm
SECTION_TOLERANCE = 1e-6   # relative slack so equal sections are not failed by rounding


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
    bar_depth: float = 16.0           # bar socket depth, measured on the stock bracket
    # In-line bracket only: a small hole through the centre web joining each
    # pair of opposite bar sockets, like the one in the upright divider.  It
    # lets air out as a bar is pushed home.  0 disables it.
    bar_vent_d: float = 4.0
    # The solid divider between the two upright sockets is
    # height - upright_depth_flat - upright_depth_leg.  It sets tier pitch and
    # MUST equal the stock part's divider.

    # --- Assumed (not yet measured) ------------------------------------------
    upright_from_end: float = 9.0    # upright socket centre from the end (centred in leg)
    corner_radius: float = 20.0      # curved inside corner between leg and rail

    # --- Design choices -------------------------------------------------------
    # Two 16 mm bar sockets plus an 8 mm centre web.  Bars seat exactly as deep
    # as in a stock bracket, so column width matches a stock rack.
    thickness: float = 40.0
    # Staggered layout (see Params.staggered): 0 keeps the two faces' bar
    # sockets in line.  A positive value lengthens the bracket by that much and
    # shifts the +X face's sockets along it, so the two sets pass side by side
    # and the bracket only needs to be one socket deep.
    stagger: float = 0.0
    # Staggered brackets come as a mirror-image pair.  A (mirror=False): facing
    # the rack, the column on the right sits `face_offset` further back.
    # B (mirror=True): the column on the left sits further back.  Alternating
    # A and B along a row keeps it from stepping back at every wall.
    mirror: bool = False
    # Which faces carry bar sockets: -1 is the -X face, +1 the +X face.  A
    # shared wall has both.  An end wall has one, on +X; the same bracket turned
    # end for end serves the other end of a row.
    bar_faces: tuple = (-1, 1)
    stock_length: float = 305.0      # length of the stock bracket the bar positions are measured on
    fit_clearance: float = 0.3       # added to socket DIAMETER; tune with the coupon
    chamfer: float = 0.8             # lead-in on socket mouths
    # Rounding is confined to plastic that carries no load: the four outer
    # vertical corners of the legs.  Every socket wall is left at full thickness.
    plan_round: float = 20.0         # radius on the four outer vertical corners; half the
                                     # thickness rounds each end off completely, like the stock part
    # Optional light break on the leg and inside-corner edges.  OFF by default:
    # the CAD kernel carries a fillet along every tangent edge, so it runs on
    # across the leg end and along the rail top and shaves 0.1-0.4 mm off the
    # walls at the socket mouths.  Cosmetic only; enable knowing that cost.
    edge_round: float = 0.0
    # Zip-tie slits: two obround slots through the rail, face to face, centred
    # tie_slit_from_end from each end at half the rail height.  The size comes
    # from the strength rule in check_tie_slit_strength.  0 height disables them.
    tie_slit_height: float = 9.0     # along Z; the slit is rounded top and bottom
    tie_slit_width: float = 3.2      # along Y; clears a 1.9 mm thick tie, and is the end-round diameter
    tie_slit_lead_in: float = 0.8    # 45 degree lead-in on both faces, as on the sockets
    tie_slit_from_end: float = 60.0  # slit centre from each end
    tie_slit_min_wall: float = 3.0   # solid rail kept above and below the slit's mouth

    @property
    def bore(self) -> float:
        return self.tube_od + self.fit_clearance

    @property
    def bar_z(self) -> float:
        return self.bar_edge_offset + self.tube_od / 2

    @property
    def tie_slit_z(self) -> float:
        """Height of the slit centres: halfway up the rail."""
        return self.rail_height / 2

    @property
    def tie_slit_ys(self) -> list:
        """Slit centres along the length, the same distance from each end."""
        if self.tie_slit_height <= 0:
            return []
        return [self.tie_slit_from_end, self.length - self.tie_slit_from_end]

    @property
    def tie_slit_mouth(self) -> tuple:
        """(height, width) of a slit at the face, lead-in included."""
        return self.tie_slit_height + 2 * self.tie_slit_lead_in, self.tie_slit_width + 2 * self.tie_slit_lead_in

    @property
    def divider(self) -> float:
        return self.height - self.upright_depth_flat - self.upright_depth_leg

    @property
    def web(self) -> float:
        """Solid plastic between the left-face and right-face bar sockets.

        Negative in the staggered layout, where the sockets overlap in depth."""
        return self.thickness - 2 * self.bar_depth

    @property
    def bar_y_right(self) -> list:
        """Bar socket centres on the +X face.

        In line: the same as the -X face.  Staggered: the -X set mirrored end
        for end, so the part is unchanged by turning it round (180 degrees
        about the vertical), and there is no way to fit it back to front."""
        return self._face_sets()[1]

    @property
    def bar_y_left(self) -> list:
        """Bar socket centres on the -X face."""
        return self._face_sets()[0]

    def _face_sets(self):
        near = list(self.bar_y)                               # stock positions from the front end
        if self.stagger <= 0:
            return near, near
        far = sorted(self.length - y for y in self.bar_y)     # the same set, measured from the rear end
        return (far, near) if self.mirror else (near, far)

    @property
    def face_offset(self) -> float:
        """Smallest centre distance between a -X socket and a +X socket."""
        return min(abs(a - b) for a in self.bar_y_left for b in self.bar_y_right)

    @property
    def plan_round_used(self) -> float:
        """The corner radius actually cut.

        Half the thickness (or more) rounds each end off completely, as on the
        stock bracket.  That is allowed when it leaves at least 2.5 mm around
        the upright socket: the round's centre sits on the bracket's centre
        line, half a thickness in from the end, so the thinnest plastic is
        between the socket and the arc along that line.  Otherwise the radius
        is reduced to keep 3 mm between the socket and the bracket's side."""
        half = self.thickness / 2
        if self.plan_round >= half - 0.01:
            wall = half - abs(half - self.upright_from_end) - self.bore / 2
            if wall >= 2.5:
                return half - 0.05      # a hair under half, so a sliver of flat end face remains
        return max(0.0, min(self.plan_round, half - self.bore / 2 - 3.0, self.leg_length - 2.0))

    @classmethod
    def staggered(cls, stagger: float = 15.0, back_wall: float = 2.0, bar_depth: float = 16.0,
                  rail_height: float = 27.0, **kwargs) -> "Params":
        """Parameters for the thin, staggered bracket.

        It matches the stock bracket's 18 mm width and fully rounded ends: the
        bar sockets are 16 mm deep, as measured on the stock part, with a 2 mm
        back wall.  15 mm of extra length puts the two faces' sockets 16 mm
        apart, leaving 3.7 mm of plastic between neighbouring 12.3 mm sockets.

        The rail is 27 mm tall where the stock rail is 18; the extra height is
        on the side away from the flat edge, between the legs.  A shared wall
        carries two columns on a rail less than half as wide as the in-line
        bracket's.  Bending strength goes with width x height^2 and stiffness
        with width x height^3, so 27 mm matches the in-line rail's strength
        (18 x 27^2 against 40 x 18^2) and exceeds its stiffness by half."""
        base = cls(**kwargs)
        thickness = bar_depth + back_wall
        values = {
            "stagger": stagger,
            "length": base.stock_length + stagger,
            "thickness": thickness,
            "bar_depth": bar_depth,
            "rail_height": rail_height,
            "corner_radius": min(base.corner_radius, base.height - rail_height),
            "plan_round": thickness / 2,
        }
        return cls(**{**kwargs, **values})

    @classmethod
    def end(cls, **kwargs) -> "Params":
        """Parameters for an end-wall bracket: bar sockets on one face only.

        It is a printed stand-in for a stock bracket at either end of a row:
        the stock 18 mm width, 16 mm bar sockets with a 2 mm back wall, the
        stock 18 mm rail and fully rounded ends.  The sockets are on the +X
        face.  One part serves both ends of a row: turned end for end it is
        the other end's bracket, with its sockets shifted 1 mm along the
        length (the stock pattern is 26 mm from one end and 27 from the
        other), as with a stock bracket turned around."""
        base = cls(**kwargs)
        thickness = base.bar_depth + 2.0
        values = {"thickness": thickness, "plan_round": thickness / 2, "bar_faces": (1,)}
        return cls(**{**kwargs, **values})

    def validate(self) -> None:
        if self.divider < 1.0:
            raise ValueError(f"upright sockets leave a {self.divider:.1f} mm divider; need >= 1 mm")
        if self.bar_vent_d >= self.bore:
            raise ValueError("bar_vent_d must be smaller than the socket, or the bar has nothing to stop against")
        if not self.bar_faces or any(f not in (-1, 1) for f in self.bar_faces):
            raise ValueError("bar_faces must hold -1, 1 or both")
        if len(self.bar_faces) == 1 and self.thickness - self.bar_depth < 1.5:
            raise ValueError("end bracket leaves less than 1.5 mm behind each bar socket")
        if len(self.bar_faces) == 2 and self.stagger <= 0 and self.web < 2.0:
            raise ValueError(f"bar sockets leave a {self.web:.1f} mm centre web; need >= 2 mm")
        if self.stagger > 0:
            if self.thickness - self.bar_depth < 1.5:
                raise ValueError("staggered bracket leaves less than 1.5 mm behind each bar socket")
            if self.face_offset - self.bore < 3.0:
                raise ValueError(f"staggered sockets are {self.face_offset:.1f} mm apart; "
                                 f"need at least {self.bore + 3.0:.1f} mm")
        if self.corner_radius > self.height - self.rail_height:
            raise ValueError("corner_radius is larger than the step between rail and leg")
        if self.bar_z + self.bore / 2 > self.rail_height - 1.0:
            raise ValueError("bar socket breaks out of the top of the rail")
        if self.thickness / 2 - self.bore / 2 < 2.5:
            raise ValueError("bracket is too thin to leave 2.5 mm either side of an upright socket")
        if self.edge_round > self.rail_height - (self.bar_z + self.bore / 2) - 2.0:
            raise ValueError("edge_round would thin the wall over a bar socket below 2 mm")
        if self.tie_slit_height > 0:
            mouth_h, mouth_w = self.tie_slit_mouth
            if self.tie_slit_width > self.tie_slit_height:
                raise ValueError("tie slit is wider than it is tall; it must be rounded top and bottom")
            wall = (self.rail_height - mouth_h) / 2
            if wall < self.tie_slit_min_wall:
                raise ValueError(f"tie slit leaves {wall:.2f} mm of rail above and below its mouth; need >= {self.tie_slit_min_wall:g} mm")
            for y in self.tie_slit_ys:
                if not mouth_w / 2 + 1.5 < y < self.length - mouth_w / 2 - 1.5:
                    raise ValueError(f"tie slit at y={y} is outside the bracket")
                for centre in (self.upright_from_end, self.length - self.upright_from_end):
                    if abs(y - centre) < self.bore / 2 + mouth_w / 2 + 1.5:
                        raise ValueError(f"tie slit at y={y} runs into the upright socket at y={centre}")
                for sign, ys in ((-1, self.bar_y_left), (1, self.bar_y_right)):
                    if sign in self.bar_faces:
                        for sy in ys:
                            if abs(y - sy) < self.bore / 2 + mouth_w / 2 + 1.5:
                                raise ValueError(f"tie slit at y={y} runs into the bar socket at y={sy}")
        # Bar sockets and upright sockets must not meet anywhere along the length.
        up_lo = self.upright_from_end - self.bore / 2
        up_hi = self.upright_from_end + self.bore / 2
        if up_lo < 1.5 or up_hi > self.leg_length - 1.5:
            raise ValueError("upright socket leaves less than 1.5 mm of wall in the leg")
        for y in self.bar_y_left + self.bar_y_right:   # checked for both faces, used or not
            for centre in (self.upright_from_end, self.length - self.upright_from_end):
                if abs(y - centre) < self.bore + 1.5:
                    raise ValueError(f"bar socket at y={y} runs into the upright socket at y={centre}")


def _cone(origin, direction, r_mouth: float, r_inner: float, depth: float) -> cq.Workplane:
    """Truncated cone starting at `origin` (a socket mouth) and narrowing along `direction`."""
    solid = cq.Solid.makeCone(r_mouth, r_inner, depth, pnt=cq.Vector(*origin), dir=cq.Vector(*direction))
    return cq.Workplane("XY").add(solid)


def tie_slit_cutter(p: Params, y: float, z: float, thickness: float, x0: float | None = None) -> cq.Workplane:
    """The solid a tie slit removes: an obround through-slot along X (rounded top and bottom), with a 45 degree lead-in pocket on each face.

    The slit runs the full `thickness` from x = `x0` (default: the -X face of a bracket centred on x = 0).  The lead-in is the same slot, a
    lead-in larger all round, narrowing at 45 degrees to the slit's own size."""
    x0 = -thickness / 2 if x0 is None else x0
    lead = p.tie_slit_lead_in
    h, w = p.tie_slit_height, p.tie_slit_width
    overrun = 1.0                                   # the through-slot starts and ends clear of the faces
    core = cq.Workplane("YZ", origin=(x0 - overrun, 0, 0)).center(y, z).slot2D(h, w, 90).extrude(thickness + 2 * overrun)
    for x_face, direction in (((x0, 1), (x0 + thickness, -1)) if lead > 0 else ()):   # no lead-in pocket if there is no lead-in
        mouth = (cq.Workplane("YZ", origin=(x_face, 0, 0)).center(y, z) if direction > 0
                 else cq.Workplane("ZY", origin=(x_face, 0, 0)).center(z, y))
        mouth = mouth.slot2D(h + 2 * lead, w + 2 * lead, 90 if direction > 0 else 0).extrude(lead, taper=45)
        core = core.union(mouth)
    return core


def _section_properties(body: cq.Workplane, y: float, thickness: float, height: float) -> tuple:
    """(area, vertical second moment, sideways second moment) of the body's cross-section at length position y, from a thin slab.

    The moments are about the section's own centroid: vertical is bending about X (resisting a load along Z), sideways about Z. They come from
    the inertia matrix of the slab divided by its thickness, which for a slab this thin is the section's own second moment."""
    slab = cq.Workplane("XY").box(thickness + 2, SECTION_SLAB, height + 2).translate((0, y, height / 2))
    solid = body.intersect(slab).val()
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(solid.wrapped, props)
    inertia = props.MatrixOfInertia()
    return props.Mass() / SECTION_SLAB, inertia.Value(1, 1) / SECTION_SLAB, inertia.Value(3, 3) / SECTION_SLAB


def tie_slit_strength(p: Params, body: cq.Workplane) -> dict:
    """The numbers the slit size rule compares: the weakest bar-socket section and the section through a slit, each as (area, vertical I,
    sideways I), plus the wall left above and below the slit's mouth."""
    socket_ys = sorted({y for sign, ys in ((-1, p.bar_y_left), (1, p.bar_y_right)) if sign in p.bar_faces for y in ys})
    sockets = [_section_properties(body, y, p.thickness, p.height) for y in socket_ys]
    weakest = tuple(min(s[i] for s in sockets) for i in range(3))
    slits = [_section_properties(body, y, p.thickness, p.height) for y in p.tie_slit_ys]
    slit = tuple(min(s[i] for s in slits) for i in range(3))
    return {"socket": weakest, "slit": slit, "wall": (p.rail_height - p.tie_slit_mouth[0]) / 2}


def check_tie_slit_strength(p: Params, body: cq.Workplane) -> None:
    """Fail the build if a tie slit weakens the rail: its cross-section must be no weaker than the weakest bar-socket section in area, vertical
    second moment and sideways second moment, and must keep tie_slit_min_wall of solid rail above and below its mouth.

    This is section properties only.  It says nothing about the stress concentration at the slit's ends, and nothing here is load tested."""
    if not p.tie_slit_ys:
        return
    r = tie_slit_strength(p, body)
    names = ("area (mm^2)", "vertical I (mm^4)", "sideways I (mm^4)")
    log.info("Tie slit check, %.1f x %.1f mm slit: wall above and below %.2f mm (need >= %.1f)", p.tie_slit_height, p.tie_slit_width,
             r["wall"], p.tie_slit_min_wall)
    failed = []
    for name, sock, slit in zip(names, r["socket"], r["slit"]):
        ok = slit >= sock * (1 - SECTION_TOLERANCE)
        log.info("  %-18s weakest bar socket %9.1f   slit %9.1f   %s", name, sock, slit, "ok" if ok else "TOO WEAK")
        if not ok:
            failed.append(name)
    if r["wall"] < p.tie_slit_min_wall:
        failed.append("wall above and below")
    if failed:
        raise ValueError(f"the {p.tie_slit_height:g} mm tie slit weakens the rail: {', '.join(failed)}")


def build_bracket(p: Params) -> cq.Workplane:
    """Build the double-sided end frame from the stock side profile."""
    p.validate()
    log.info("Building bracket: %.1f x %.1f x %.1f mm (X x Y x Z), tie slits at y=%s",
             p.thickness, p.length, p.height, p.tie_slit_ys)
    log.info("Upright divider %.1f mm, bar-socket centre web %.1f mm", p.divider, p.web)
    log.debug("bore=%.2f bar_z=%.2f bar_y=%s", p.bore, p.bar_z, p.bar_y)

    L, H, R, G, r = p.length, p.height, p.rail_height, p.leg_length, p.corner_radius
    k = r * (1 - 0.5 ** 0.5)   # offset of the 45-degree point on each corner arc

    # Side profile in the YZ plane (local x = Y, local y = Z), extruded along X.
    profile = cq.Workplane("YZ").moveTo(0, 0).lineTo(L, 0).lineTo(L, H).lineTo(L - G, H)
    straight = H - (R + r) > 1e-6       # a straight piece of leg above each curve, if the curve leaves room
    if straight:
        profile = profile.lineTo(L - G, R + r)
    profile = (
        profile.threePointArc((L - G - k, R + k), (L - G - r, R))
        .lineTo(G + r, R)
        .threePointArc((G + k, R + k), (G, R + r))
    )
    if straight:
        profile = profile.lineTo(G, H)
    body = profile.lineTo(0, H).close().extrude(p.thickness / 2, both=True)

    # Round the ends in plan (looking down).  The side profile is intersected
    # with a rounded outline, which works for any radius, including one longer
    # than the leg, where filleting the leg's own edges would fail.
    plan_round = p.plan_round_used
    if plan_round > 0:
        try:
            outline = (
                cq.Workplane("XY")
                .box(p.thickness, L, H, centered=(True, False, False))
                .edges("|Z").fillet(plan_round)
            )
            body = body.intersect(outline)
            log.debug("ends rounded in plan at r=%.2f", plan_round)
        except Exception as exc:
            log.error("End rounding failed, leaving the ends square: %s", exc)

    # Break the top edges in one pass: the side and corner edges of each leg top, plus
    # the side-face edges down the inside corner curves.  One fillet call keeps
    # the rounds continuous.  The rail top is left square (see below).
    if p.edge_round > 0:
        try:
            # Leg-top edges, except the two that run across the thickness
            # (end edge and inner edge): those border the 2.85 mm walls
            # around the upright socket mouth, so they stay square.
            edges = [e for f in body.faces(">Z").vals() for e in f.Edges()
                     if abs(e.Center().x) > p.thickness / 2 - plan_round - 0.5]
            for face in body.faces(">X").vals() + body.faces("<X").vals():
                for e in face.Edges():
                    c = e.Center()
                    is_bed_edge = c.z < 1.0
                    is_vertical_corner_seam = min(c.y, L - c.y) < plan_round + 1.0 and c.z < H - 1.0
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

    # Bar sockets: blind from each face, bar_depth deep.  In line they stop
    # either side of the centre web; staggered they overlap in depth and pass
    # side by side.
    face_ys = tuple((sign, ys) for sign, ys in ((-1, p.bar_y_left), (1, p.bar_y_right)) if sign in p.bar_faces)
    for sign, ys in face_ys:
        for y in ys:
            sock = (
                cq.Workplane("YZ")
                .workplane(offset=sign * p.web / 2)
                .center(y, p.bar_z)
                .circle(p.bore / 2)
                .extrude(sign * p.bar_depth)
            )
            body = body.cut(sock)

    # Vent through the centre web between each pair of opposite bar sockets.
    if p.stagger <= 0 and len(p.bar_faces) == 2 and p.bar_vent_d > 0:
        for y in p.bar_y:
            vent = cq.Solid.makeCylinder(p.bar_vent_d / 2, p.web + 2.0,
                                         pnt=cq.Vector(-p.web / 2 - 1.0, y, p.bar_z), dir=cq.Vector(1, 0, 0))
            body = body.cut(cq.Workplane("XY").add(vent))
        log.debug("bar-socket vents: %d x %.1f mm through the %.1f mm web", len(p.bar_y), p.bar_vent_d, p.web)

    # Lead-in on every socket mouth, cut as a short cone.
    if p.chamfer > 0:
        c, rb = p.chamfer, p.bore / 2
        for y in upright_ys:
            body = body.cut(_cone((0, y, 0), (0, 0, 1), rb + c, rb, c))
            body = body.cut(_cone((0, y, H), (0, 0, -1), rb + c, rb, c))
        for sign, ys in face_ys:
            for y in ys:
                body = body.cut(_cone((sign * p.thickness / 2, y, p.bar_z), (-sign, 0, 0), rb + c, rb, c))

    # Zip-tie slits, through the rail face to face.
    for y in p.tie_slit_ys:
        body = body.cut(tie_slit_cutter(p, y, p.tie_slit_z, p.thickness))
    check_tie_slit_strength(p, body)
    return body


@dataclass(frozen=True)
class CouponLayout:
    """Where everything on the fit-test coupon is, so the model and its blueprint read the same numbers."""
    size_x: float
    size_y: float
    size_z: float
    upright_depth: float
    upright_x: float      # the upright socket's centre
    upright_y: float
    bar_y: float          # the bar socket's centre, on the +X face
    bar_z: float
    slit_y: float         # the tie slit's centre; it runs through the coupon along X
    slit_z: float


COUPON_MARGIN = 3.0           # plastic around and between the sockets and the slit
COUPON_UPRIGHT_DEPTH = 12.0   # how deep the coupon's upright socket goes from its top
COUPON_MIN_HEIGHT = 14.0      # the coupon is at least this tall, or as tall as the rail


def coupon_layout(p: Params) -> CouponLayout:
    """The fit-test coupon's dimensions: one upright socket, one bar socket and one tie slit at production size, side by side along Y."""
    size_x = p.bar_depth + COUPON_MARGIN
    slit_mouth = p.tie_slit_mouth[1]
    size_y = 2 * p.bore + slit_mouth + 4 * COUPON_MARGIN
    size_z = max(p.rail_height, COUPON_MIN_HEIGHT)
    return CouponLayout(size_x, size_y, size_z, COUPON_UPRIGHT_DEPTH, size_x / 2, COUPON_MARGIN + p.bore / 2,
                        2 * COUPON_MARGIN + 1.5 * p.bore, size_z / 2,
                        size_y - COUPON_MARGIN - slit_mouth / 2, size_z / 2)


def build_coupon(p: Params) -> cq.Workplane:
    """Fit-test piece: one upright socket, one bar socket and one tie slit at production size."""
    log.info("Building fit-test coupon (bore=%.2f, tie slit %.1f x %.1f)", p.bore, p.tie_slit_height, p.tie_slit_width)
    c = coupon_layout(p)
    body = cq.Workplane("XY").box(c.size_x, c.size_y, c.size_z, centered=(False, False, False))
    upright = (
        cq.Workplane("XY").workplane(offset=c.size_z - c.upright_depth)
        .center(c.upright_x, c.upright_y).circle(p.bore / 2).extrude(c.upright_depth)
    )
    bar = (
        cq.Workplane("YZ").workplane(offset=c.size_x)
        .center(c.bar_y, c.bar_z).circle(p.bore / 2)
        .extrude(-p.bar_depth)
    )
    body = body.cut(upright).cut(bar)
    if p.tie_slit_height > 0:
        body = body.cut(tie_slit_cutter(p, c.slit_y, c.slit_z, c.size_x, x0=0.0))
    return body


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
    ap.add_argument("--tie-slit-height", type=float, default=d.tie_slit_height, help="0 leaves the tie slits out")
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
        tie_slit_height=args.tie_slit_height,
    )
    log.info("Parameters: %s", base)
    try:
        export(build_bracket(Params(**base)), args.out, "shared_wall_bracket_v2")
        export(build_coupon(Params(**base)), args.out, "fit_test_coupon_v2")
        stag = {k: v for k, v in base.items() if k != "bar_depth"}
        for letter, mirror in (("a", False), ("b", True)):
            export(build_bracket(Params.staggered(**stag, mirror=mirror)), args.out, f"shared_wall_bracket_staggered_{letter}")
        export(build_bracket(Params.end(**base)), args.out, "end_bracket")
    except ValueError as exc:
        log.error("Invalid parameters: %s", exc)
        raise SystemExit(2)
    except Exception:
        log.exception("Model generation failed")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
