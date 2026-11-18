#!/usr/bin/env python3
"""
Build the two release archives from the files committed in this repository.

    <name>-prints-v<version>.zip    for every part: STL and 3MF print files, STEP,
                                    the drawing and the README, plus the print
                                    settings, the disclaimer and the licences
    <name>-source-v<version>.zip    every tracked file

Nothing is regenerated: the archives hold exactly what is committed, so a
release always matches its tag.

Usage:
    python3 tools/make_release.py --version 1.0.3
    python3 tools/make_release.py --version 1.0.3 --out dist --log-level DEBUG
"""
import argparse
import logging
import subprocess
import zipfile
from pathlib import Path

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(name)s: %(message)s"
log = logging.getLogger("release")

REPO = Path(__file__).resolve().parent.parent
NAME = "filament-rack-addon-brackets"
PRINT_SUFFIXES = {".stl", ".3mf", ".step"}
# Drawings and READMEs travel with the print files.
PRINT_NAMES = {"README.md", "blueprint.svg", "blueprint.png"}
# Shipped alongside so the archive stands on its own.
PRINT_EXTRAS = ["PRINT_SETTINGS.md", "DISCLAIMER.md", "LICENSE.md", "LICENSE-DESIGNS.md", "LICENSE-CODE"]


def tracked_files() -> list:
    """Every file git tracks, as repo-relative paths."""
    out = subprocess.run(["git", "-C", str(REPO), "ls-files", "-z"], check=True, capture_output=True).stdout
    return sorted(Path(p) for p in out.decode().split("\0") if p)


def write_zip(path: Path, files: list, root: str) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in files:
            z.write(REPO / rel, f"{root}/{rel.as_posix()}")
            log.debug("added %s", rel)
    log.info("wrote %s: %d files, %d bytes", path, len(files), path.stat().st_size)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", required=True, help="release version without the leading v, e.g. 1.0.3")
    ap.add_argument("--out", type=Path, default=REPO / "dist")
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)

    files = tracked_files()
    if not files:
        log.error("git reports no tracked files under %s", REPO)
        raise SystemExit(1)
    missing = [f for f in PRINT_EXTRAS if Path(f) not in files]
    if missing:
        log.error("print archive needs these tracked files: %s", ", ".join(missing))
        raise SystemExit(1)

    print_files = [f for f in files
                   if (f.suffix.lower() in PRINT_SUFFIXES or f.name in PRINT_NAMES) and "legacy" not in f.parts]
    if not any(f.suffix.lower() in {".stl", ".3mf"} for f in print_files):
        log.error("no STL or 3MF files are tracked")
        raise SystemExit(1)
    print_files += [Path(f) for f in PRINT_EXTRAS if Path(f) not in print_files]

    args.out.mkdir(parents=True, exist_ok=True)
    for kind, members in (("prints", print_files), ("source", files)):
        stem = f"{NAME}-{kind}-v{args.version}"
        write_zip(args.out / f"{stem}.zip", members, stem)


if __name__ == "__main__":
    main()
