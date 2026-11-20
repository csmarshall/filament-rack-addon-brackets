#!/usr/bin/env python3
"""
Draw the README header previews of the shared-wall bracket with common-blueprint-generator's preview(): the in-line, staggered (A and B) and end
brackets side by side at one scale, built from the same Params as the models. Replaces the hand-made preview.png.

Usage:
    python3 make_preview.py       # writes preview.svg and refreshes its README embed
"""
import logging
from pathlib import Path

from blueprint import preview

from shared_wall_bracket import Params, build_bracket

HERE = Path(__file__).resolve().parent
FRONT, UP = "-Y", "+Z"   # the model's axes the preview shows; -Y is the length axis, so the brackets lie along the page


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parts = [
        (build_bracket(Params()), "IN LINE"),
        (build_bracket(Params.staggered()), "STAGGERED A"),
        (build_bracket(Params.staggered(mirror=True)), "STAGGERED B"),
        (build_bracket(Params.end()), "END"),
    ]
    preview(parts, HERE / "preview", front=FRONT, up=UP, readme=HERE / "README.md",
            title="The in-line, staggered A and B, and end brackets", source="shared_wall_bracket.py")


if __name__ == "__main__":
    main()
