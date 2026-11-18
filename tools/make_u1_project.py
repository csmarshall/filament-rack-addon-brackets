#!/usr/bin/env python3
"""
Package an STL as a Snapmaker Orca project (.3mf) for the Snapmaker U1.

The project selects stock system presets by name and overrides a handful of
process settings.  Snapmaker Orca's loader (PresetCollection::load_external_preset)
takes every setting NOT named in "different_settings_to_system" from the presets
installed on the machine opening the file, so machine G-code, temperatures and
so on come from the user's own install; the flattened values written here are
only a fallback.

Usage:
    python3 -I make_u1_project.py --stl part.stl --profiles /path/to/snapmaker-profiles/Snapmaker --out part.3mf
"""
import argparse
import json
import logging
import math
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
import trimesh

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(name)s: %(message)s"
log = logging.getLogger("u1_project")

PRINTER = "Snapmaker U1 (0.4 nozzle)"
PROCESS = "0.20mm Standard @Snapmaker U1 (0.4 nozzle)"
FILAMENT_SLOT_1 = "Generic ABS @U1 0.4 nozzle"
FILAMENT_OTHER_SLOTS = "Generic PLA @U1 0.4 nozzle"   # the U1 system default

# Process overrides.  Walls: 5 loops with Arachne, so every socket wall (1.85,
# 2.85 and 3.85 mm) prints as solid perimeters at the stock 0.42 / 0.45 mm
# line widths.  Brim: an outer brim to hold a long ABS part down; its width is
# set per file from --brim-width because it has to fit inside the bed margin.
PROCESS_OVERRIDES = {
    "wall_loops": "5",
    "wall_generator": "arachne",
    "sparse_infill_density": "15%",
    # Gyroid in place of the stock grid: the OrcaSlicer wiki describes grid as
    # perpendicular lines whose overlapping points may cause noise or artifacts,
    # and gyroid as isotropic, with curves that help reduce warping.
    "sparse_infill_pattern": "gyroid",
    # 5 bottom layers (1.0 mm) in place of 3, as a precaution for the 1.85 mm
    # wall between the bed face and each bar socket.
    "bottom_shell_layers": "5",
    "brim_type": "outer_only",
    "brim_width": "5",
}

# The wall and brim settings again as per-object settings, so they show on the
# part itself and survive switching to a different process preset.
OBJECT_KEYS = ("wall_loops", "wall_generator", "sparse_infill_density", "sparse_infill_pattern",
               "bottom_shell_layers", "brim_type", "brim_width")

# Keys that describe a preset file rather than a setting.
META_KEYS = {"type", "name", "inherits", "from", "setting_id", "instantiation", "filament_id",
             "description", "renamed_from", "version", "url", "is_custom_defined",
             "compatible_printers", "compatible_printers_condition",
             "compatible_prints", "compatible_prints_condition"}
APP_TAG = "Snapmaker_Orca-2.0.0"     # the loader only checks the "Snapmaker_Orca-" prefix
# Snapmaker Orca writes the "Snapmaker_Orca:3mfVersion" metadata name without
# declaring the prefix.  Declaring it (any URI) keeps strict 3MF readers happy.


def resolve(profile_dir: Path, kind: str, name: str) -> dict:
    """Load a preset and merge in everything it inherits."""
    path = profile_dir / kind / f"{name}.json"
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    parent = data.get("inherits")
    merged = resolve(profile_dir, kind, parent) if parent else {}
    merged.update(data)
    log.debug("resolved %s/%s (%d keys, inherits %s)", kind, name, len(merged), parent)
    return merged


def build_project_settings(profile_dir: Path, slots: int, overrides: dict) -> dict:
    printer = resolve(profile_dir, "machine", PRINTER)
    process = resolve(profile_dir, "process", PROCESS)
    filament_names = [FILAMENT_SLOT_1] + [FILAMENT_OTHER_SLOTS] * (slots - 1)
    filaments = [resolve(profile_dir, "filament", n) for n in filament_names]

    for key, value in overrides.items():
        # A key missing from the preset files just means the preset uses the
        # slicer's built-in default for it.
        log.info("override %s: %s -> %s", key, process.get(key, "(slicer default)"), value)

    cfg = {}
    cfg.update({k: v for k, v in printer.items() if k not in META_KEYS})
    cfg.update({k: v for k, v in process.items() if k not in META_KEYS})
    cfg.update(overrides)

    # Filament settings are stored one value per slot.
    filament_keys = sorted(set().union(*[set(f) for f in filaments]) - META_KEYS)
    for key in filament_keys:
        values = []
        for f in filaments:
            v = f.get(key, filaments[0].get(key))
            if v is None:
                v = next(x[key] for x in filaments if key in x)
            values.append(v[0] if isinstance(v, list) and v else v)
        if all(isinstance(v, str) for v in values):
            cfg[key] = values

    cfg["filament_ids"] = [f.get("filament_id", "") for f in filaments]
    cfg.update({
        "from": "project",
        "name": "project_settings",
        "version": "01.10.01.50",
        "printer_settings_id": PRINTER,
        "print_settings_id": PROCESS,
        "filament_settings_id": filament_names,
        "filament_colour": ["#3A3A3A"] + ["#FFFFFF"] * (slots - 1),
        # One entry for the process, one per filament slot, one for the printer.
        "different_settings_to_system": [";".join(overrides)] + [""] * (slots + 1),
        "inherits_group": [""] * (slots + 2),
    })
    return cfg, printer


def bed_rectangle(printer: dict):
    pts = np.array([[float(c) for c in p.split("x")] for p in printer["printable_area"]])
    return pts.min(0), pts.max(0)


def best_fit_angle(mesh: trimesh.Trimesh, bed_size: np.ndarray):
    """Rotation about Z that leaves the largest margin to the bed edge."""
    xy = mesh.convex_hull.vertices[:, :2]
    best = None
    for deg in np.arange(0.0, 180.0, 0.25):
        a = math.radians(deg)
        rot = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
        ext = np.ptp(xy @ rot.T, axis=0)
        margin = float(((bed_size - ext) / 2).min())
        if best is None or margin > best[1]:
            best = (deg, margin, ext)
    return best


def model_xml(mesh: trimesh.Trimesh, name: str, transform: str) -> str:
    verts = "\n".join(f'     <vertex x="{x:.4f}" y="{y:.4f}" z="{z:.4f}"/>' for x, y, z in mesh.vertices)
    tris = "\n".join(f'     <triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in mesh.faces)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:Snapmaker_Orca="http://schemas.snapmaker.com/package/2025">
 <metadata name="Application">{APP_TAG}</metadata>
 <metadata name="Snapmaker_Orca:3mfVersion">1</metadata>
 <metadata name="Title">{escape(name)}</metadata>
 <resources>
  <object id="1" name="{escape(name)}" type="model">
   <mesh>
    <vertices>
{verts}
    </vertices>
    <triangles>
{tris}
    </triangles>
   </mesh>
  </object>
 </resources>
 <build>
  <item objectid="1" transform="{transform}"/>
 </build>
</model>
'''


def model_settings_xml(name: str, overrides: dict) -> str:
    """Per-object settings, in the layout Snapmaker Orca writes (Metadata/model_settings.config).

    The object id and the part id both refer to object 1 in 3dmodel.model: a
    plain mesh object is its own single part."""
    settings = "\n".join(f'    <metadata key="{k}" value="{escape(overrides[k])}"/>' for k in OBJECT_KEYS)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<config>
  <object id="1">
    <metadata key="name" value="{escape(name)}"/>
    <metadata key="extruder" value="1"/>
{settings}
    <part id="1" subtype="normal_part">
      <metadata key="name" value="{escape(name)}"/>
      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>
    </part>
  </object>
</config>
'''


CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
 <Default Extension="config" ContentType="application/octet-stream"/>
</Types>
'''
RELS = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>
'''


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stl", type=Path, required=True)
    ap.add_argument("--profiles", type=Path, required=True, help="the 'Snapmaker' folder of snapmaker-profiles")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--name", default=None)
    ap.add_argument("--slots", type=int, default=4)
    ap.add_argument("--brim-width", type=float, default=float(PROCESS_OVERRIDES["brim_width"]),
                    help="outer brim width in mm; 0 disables the brim")
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)

    overrides = dict(PROCESS_OVERRIDES)
    if args.brim_width > 0:
        overrides["brim_width"] = f"{args.brim_width:g}"
    else:
        overrides["brim_type"] = "no_brim"
        overrides["brim_width"] = "0"
    cfg, printer = build_project_settings(args.profiles, args.slots, overrides)
    lo, hi = bed_rectangle(printer)
    bed_size = hi - lo
    log.info("U1 printable area %.1f x %.1f mm, height %s", bed_size[0], bed_size[1], printer.get("printable_height"))

    mesh = trimesh.load(str(args.stl))
    mesh.merge_vertices()
    if not mesh.is_watertight:
        raise SystemExit(f"{args.stl} is not watertight; refusing to package it")
    # Centre the mesh on the origin in XY and sit it on z=0, so the build
    # transform rotates it about its own middle.
    centre = (mesh.bounds[0] + mesh.bounds[1]) / 2
    mesh.apply_translation([-centre[0], -centre[1], -mesh.bounds[0][2]])

    deg, margin, ext = best_fit_angle(mesh, bed_size)
    log.info("best fit: rotate %.2f deg -> footprint %.1f x %.1f mm, %.1f mm clear to the nearest bed edge",
             deg, ext[0], ext[1], margin)
    if margin < 2.0:
        raise SystemExit(f"part does not fit the bed with at least 2 mm clearance (margin {margin:.1f} mm)")
    if args.brim_width > 0 and margin - args.brim_width < 2.0:
        raise SystemExit(f"a {args.brim_width:g} mm brim leaves {margin - args.brim_width:.1f} mm to the bed edge; "
                         f"use --brim-width {max(0.0, margin - 2.0):.0f} or less")
    log.info("brim %g mm leaves %.1f mm to the nearest bed edge", args.brim_width, margin - args.brim_width)
    if mesh.extents[2] > float(printer["printable_height"]):
        raise SystemExit("part is taller than the printable height")

    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    bed_centre = (lo + hi) / 2
    # 3MF transforms are row-major 4x3 for row vectors: [x y z 1] * M.
    transform = " ".join(f"{v:.6f}" for v in (c, s, 0, -s, c, 0, 0, 0, 1, bed_centre[0], bed_centre[1], 0))

    name = args.name or args.stl.stem
    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("3D/3dmodel.model", model_xml(mesh, name, transform))
        z.writestr("Metadata/project_settings.config", json.dumps(cfg, indent=4))
        z.writestr("Metadata/model_settings.config", model_settings_xml(name, overrides))
    log.info("wrote %s (%d bytes, %d settings, %d triangles)", args.out, args.out.stat().st_size, len(cfg), len(mesh.faces))


if __name__ == "__main__":
    main()
