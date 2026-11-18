"""
What every blueprint script in this repo shares: the licence and dates a sheet needs before anything is written, the title block, and saving the
SVG and refreshing its README embed. The scripts draw their own views; this keeps the boilerplate in one place.

A drawing's README embed lives between <!-- blueprint:NAME --> and <!-- /blueprint --> where NAME is the output file name, and is refreshed only
when the output is that script's default one.
"""
import argparse
import logging
from datetime import date
from pathlib import Path
from typing import Callable, Sequence

from blueprint import Sheet, TitleInfo, git_dates, revisions
from blueprint.readme import embed, update
from blueprint.reuse_lookup import licence_for

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(name)s: %(message)s"
log = logging.getLogger("blueprint")

DRAWN_BY = "C. MARSHALL"
COMPANY = "Shermer Works"
FOR_RACK = "9-tier modular filament storage rack (Amazon B0FFZ8SSQX)"


class Context:
    """The things read before a sheet is drawn: git dates (before anything is written, so this run's own output does not read as a local
    edit) and the drawing's own licence and copyright from REUSE.toml for the SVG this run writes. Fails if REUSE.toml does not cover it."""

    def __init__(self, script: Path, out_stem: Path) -> None:
        self.script = script.resolve()
        self.dates = git_dates(self.script.parent)
        self.licence = licence_for(out_stem.with_name(f"{out_stem.name}.svg"))


def finish(sheet: Sheet, ctx: Context, out_stem: Path, default_out: Path, *, title: str, number: str, source: str, for_: str, material: str,
           scale: float, detail_scales: Sequence[float], notes: Sequence[str], readme: Path, alt: str, source_file: Path) -> None:
    """Title block, notes, save the SVG, and refresh the README embed if `out_stem` is the default output."""
    rendered = date.today()
    sheet.title_block(TitleInfo(
        title=title, drawing_number=number, for_=for_, material=material, source=source, drawn_by=DRAWN_BY, company=COMPANY,
        started=ctx.dates.started, updated=rendered, revisions=revisions(ctx.dates, rendered),
        licence=ctx.licence.licence, copyright=ctx.licence.copyright,
    ), scale, detail_scales=tuple(detail_scales))
    sheet.notes(list(notes))
    (svg,) = sheet.save(out_stem, formats=("svg",))
    if out_stem == default_out:
        update(readme, default_out.name, embed(readme, svg, alt, source_file))


def run(doc: str, draw: Callable[[Path], None], default_out: Path, quiet: Sequence[str] = ()) -> None:
    """The command line every sheet script has: --out and --log-level, then draw(out_stem)."""
    ap = argparse.ArgumentParser(description=doc, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=default_out, help="output path without extension (the README embed is refreshed only for the default)")
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)
    for name in quiet:
        logging.getLogger(name).setLevel(logging.WARNING)
    try:
        draw(args.out)
    except Exception:
        log.exception("Blueprint generation failed")
        raise SystemExit(1)
