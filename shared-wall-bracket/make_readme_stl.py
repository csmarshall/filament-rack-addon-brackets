#!/usr/bin/env python3
"""
Write the small ASCII STL that is embedded in this folder's README.

GitHub renders an ASCII STL inside a fenced `stl` block in Markdown as an
interactive viewer.  The text has to live in the Markdown file itself, so this
builds a simplified bracket (square corners, no lead-in chamfers, no vent
holes), tessellates it coarsely and writes compact ASCII with real normals.

Usage:
    python3 make_readme_stl.py              # rewrites the block in README.md
    python3 make_readme_stl.py --out x.stl  # just write the STL
"""
import argparse
import logging
import re
from pathlib import Path

import numpy as np
import trimesh

from shared_wall_bracket import Params, build_bracket

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(name)s: %(message)s"
log = logging.getLogger("readme_stl")
BLOCK = re.compile(r"```stl\n.*?\n```", re.S)


def ascii_stl(mesh: trimesh.Trimesh, name: str) -> str:
    lines = [f"solid {name}"]
    for (a, b, c), n in zip(mesh.faces, mesh.face_normals):
        lines.append(f"facet normal {n[0]:.2f} {n[1]:.2f} {n[2]:.2f}")
        lines.append("outer loop")
        for i in (a, b, c):
            x, y, z = mesh.vertices[i]
            lines.append(f"vertex {x:.1f} {y:.1f} {z:.1f}")
        lines.append("endloop")
        lines.append("endfacet")
    lines.append(f"endsolid {name}")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=None, help="write the STL here instead of into README.md")
    ap.add_argument("--readme", type=Path, default=Path(__file__).with_name("README.md"))
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)
    logging.getLogger("shared_wall_v2").setLevel(logging.WARNING)

    shape = build_bracket(Params(chamfer=0, upright_vent_d=0, bar_vent_d=0, plan_round=0, tie_slit_lead_in=0)).val()
    verts, tris = shape.tessellate(1.0, 1.0)
    mesh = trimesh.Trimesh(np.array([[p.x, p.y, p.z] for p in verts]), np.array(tris), process=True)
    mesh.fix_normals()
    text = ascii_stl(mesh, "shared_wall_bracket")
    log.info("simplified mesh: %d triangles, %d bytes of ASCII STL, watertight=%s",
             len(mesh.faces), len(text), mesh.is_watertight)

    if args.out:
        args.out.write_text(text + "\n")
        log.info("wrote %s", args.out)
        return
    readme = args.readme.read_text()
    if len(BLOCK.findall(readme)) != 1:
        log.error("expected exactly one ```stl block in %s", args.readme)
        raise SystemExit(1)
    args.readme.write_text(BLOCK.sub(lambda _: "```stl\n" + text + "\n```", readme))
    log.info("updated the stl block in %s (%d bytes total)", args.readme, args.readme.stat().st_size)


if __name__ == "__main__":
    main()
