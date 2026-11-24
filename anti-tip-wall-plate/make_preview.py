#!/usr/bin/env python3
"""
Draw the README header preview of the anti-tip wall plate with common-blueprint-generator's preview(), built from the same Params as the model.
Replaces the hand-made preview.png.

Usage:
    python3 make_preview.py       # writes preview.svg and refreshes its README embed
"""
import logging
from pathlib import Path

from blueprint import preview

from wall_plate import Params, build_wall_plate

HERE = Path(__file__).resolve().parent


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    preview([(build_wall_plate(Params()), "WALL PLATE")], HERE / "preview", front="+Z", up="+Y", readme=HERE / "README.md",
            title="The anti-tip wall plate", source="wall_plate.py")


if __name__ == "__main__":
    main()
