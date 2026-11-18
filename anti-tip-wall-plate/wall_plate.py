#!/usr/bin/env python3
"""
Anti-tip wall plate for a zip-tie tether.

Modelled on the common two-plate furniture anti-tip kit: a small plate screwed
to the wall with a raised saddle, and a zip tie that runs through the saddle
and around the furniture.  On the filament rack the tie goes straight around a
steel upright tube, so only this wall plate needs printing.

The part is one 2D profile extruded along its width.  Print it standing on
that profile (the profile on the bed, width pointing up).  The layers then run
continuously through the plate, the saddle legs and the saddle bar, so a pull
away from the wall loads the plastic along the layers, not across them.

Coordinates:
    U = along the plate (vertical on the wall)
    N = out from the wall
    W = across the plate; the tie runs through the saddle along W

Usage:
    python3 wall_plate.py
    python3 wall_plate.py --tie-width 4.8 --tie-thickness 1.4 --log-level DEBUG
"""

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path

import cadquery as cq

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(name)s: %(message)s"
log = logging.getLogger("wall_plate")


@dataclass
class Params:
    tie_width: float = 7.6        # heavy-duty tie (typically rated around 120 lb)
    tie_thickness: float = 1.9
    slot_clearance: float = 1.3   # added to tie width and thickness for the slot
    plate_length: float = 60.0    # U
    plate_width: float = 22.0     # W; also the length of the saddle tunnel
    plate_thickness: float = 5.0  # N
    leg: float = 4.75             # saddle leg thickness (U)
    bar: float = 6.0              # saddle bar thickness (N)
    gusset: float = 3.0           # 45 degree foot where each leg meets the plate
    corner: float = 2.0           # 45 degree break on the bar's outer corners
    screw_d: float = 4.8          # clearance for a #8 / 4 mm pan-head screw
    screw_offset: float = 21.0    # each screw's distance from the plate centre (U)

    @property
    def slot_u(self) -> float:
        return self.tie_width + self.slot_clearance + 0.6

    @property
    def slot_n(self) -> float:
        return self.tie_thickness + self.slot_clearance

    @property
    def height(self) -> float:
        return self.plate_thickness + self.slot_n + self.bar

    def validate(self) -> None:
        saddle_half = self.slot_u / 2 + self.leg + self.gusset
        if self.screw_offset - self.screw_d / 2 - 3.0 < saddle_half:
            raise ValueError("screw holes are too close to the saddle; lengthen the plate or move the screws out")
        if self.screw_offset + self.screw_d / 2 + 3.0 > self.plate_length / 2:
            raise ValueError("screw holes are too close to the plate ends")
        if self.screw_d + 6.0 > self.plate_width:
            raise ValueError("plate is too narrow for the screw hole")


def build_wall_plate(p: Params) -> cq.Workplane:
    p.validate()
    half = p.plate_length / 2
    t = p.plate_thickness
    leg_out = p.slot_u / 2 + p.leg
    top = p.height
    log.info("Building wall plate: %.1f x %.1f x %.1f mm (U x N x W), slot %.1f x %.1f mm",
             p.plate_length, top, p.plate_width, p.slot_u, p.slot_n)

    # Outer profile: plate with a saddle hump, 45 degree feet and top corners.
    profile = [
        (-half, 0), (half, 0), (half, t),
        (leg_out + p.gusset, t), (leg_out, t + p.gusset),
        (leg_out, top - p.corner), (leg_out - p.corner, top),
        (-leg_out + p.corner, top), (-leg_out, top - p.corner),
        (-leg_out, t + p.gusset), (-leg_out - p.gusset, t),
        (-half, t),
    ]
    body = cq.Workplane("XY").polyline(profile).close().extrude(p.plate_width)

    # Tie slot: a tunnel through the saddle along W, sitting on the plate face.
    slot = (
        cq.Workplane("XY")
        .center(0, t + p.slot_n / 2)
        .rect(p.slot_u, p.slot_n)
        .extrude(p.plate_width)
    )
    body = body.cut(slot)

    # Screw holes through the plate, one each side of the saddle.
    for sign in (-1, 1):
        hole = cq.Solid.makeCylinder(
            p.screw_d / 2, t + 2,
            pnt=cq.Vector(sign * p.screw_offset, -1, p.plate_width / 2), dir=cq.Vector(0, 1, 0),
        )
        body = body.cut(cq.Workplane("XY").add(hole))
        log.debug("screw hole at U=%.1f", sign * p.screw_offset)
    return body


def export(shape: cq.Workplane, out_dir: Path, name: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for ext in ("step", "stl"):
        path = out_dir / f"{name}.{ext}"
        cq.exporters.export(shape, str(path), tolerance=0.02, angularTolerance=0.1)
        log.info("Wrote %s (%d bytes)", path, path.stat().st_size)
    bb = shape.val().BoundingBox()
    log.info("%s: bbox %.1f x %.1f x %.1f mm, volume %.1f cm^3, valid=%s",
             name, bb.xlen, bb.ylen, bb.zlen, shape.val().Volume() / 1000.0, shape.val().isValid())


def main() -> None:
    d = Params()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=Path("models"))
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    ap.add_argument("--tie-width", type=float, default=d.tie_width)
    ap.add_argument("--tie-thickness", type=float, default=d.tie_thickness)
    ap.add_argument("--screw-d", type=float, default=d.screw_d)
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)
    try:
        params = Params(tie_width=args.tie_width, tie_thickness=args.tie_thickness, screw_d=args.screw_d)
        export(build_wall_plate(params), args.out, "anti_tip_wall_plate")
    except ValueError as exc:
        log.error("Invalid parameters: %s", exc)
        raise SystemExit(2)
    except Exception:
        log.exception("Model generation failed")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
