#!/usr/bin/env python3
"""
Build the two release archives from the files committed in this repository.

    <name>-v<version>-print-files.zip   STL and 3MF for every part, the print
                                        settings, the disclaimer and the licences
    <name>-v<version>-source.zip        every tracked file: scripts, CAD exports,
                                        drawings and documentation

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
PRINT_SUFFIXES = {".stl", ".3mf"}
# Shipped alongside the print files so the archive stands on its own.
PRINT_EXTRAS = ["PRINT_SETTINGS.md", "DISCLAIMER.md", "LICENSE.md", "LICENSE-DESIGNS.md"]


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

    print_files = [f for f in files if f.suffix.lower() in PRINT_SUFFIXES and "legacy" not in f.parts]
    if not print_files:
        log.error("no STL or 3MF files are tracked")
        raise SystemExit(1)
    print_files += [Path(f) for f in PRINT_EXTRAS]

    args.out.mkdir(parents=True, exist_ok=True)
    stem = f"{NAME}-v{args.version}"
    write_zip(args.out / f"{stem}-print-files.zip", print_files, f"{stem}-print-files")
    write_zip(args.out / f"{stem}-source.zip", files, f"{stem}-source")


if __name__ == "__main__":
    main()
