# Filament rack add-on brackets

[![Latest release](https://img.shields.io/github/v/release/csmarshall/filament-rack-addon-brackets)](https://github.com/csmarshall/filament-rack-addon-brackets/releases/latest)
[![Designs: CC BY-NC-SA 4.0](https://img.shields.io/badge/designs-CC%20BY--NC--SA%204.0-lightgrey)](LICENSE.md)
[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-cs__marshall-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/cs_marshall)

3D-printable add-on parts for the 9-tier, 54-spool modular 3D printer filament
storage rack sold on Amazon as the
[Hizypaixin 9-Tier 3D Printer Filament Storage Rack](https://www.amazon.com/dp/B0FFZ8SSQX)
(ASIN B0FFZ8SSQX).

> **Use at your own risk.** These are untested hobby designs shared for
> educational purposes, with no warranty and no load rating. Read the
> [disclaimer](DISCLAIMER.md) before printing or installing anything.
>
> **Do not print these parts in PLA.** They carry a constant load, and PLA
> slowly deforms under constant load and softens when warm.

## Does your rack match?

Racks like this are sold under several brand names. These parts are modelled on
the stock plastic bracket from the listing above. Measure yours before printing:

- 305 mm long, 18 mm thick.
- A straight rail 18 mm tall with one flat edge, and an 18 mm long leg at each
  end that drops to 40 mm with a curved inside corner.
- 12 mm metal tubes for both uprights and horizontal bars.
- Four bar holes on one face, 2 mm in from the flat edge, with centres at
  26, 110, 194 and 278 mm from the end (84 mm pitch).
- An upright socket in each leg from both ends: one opens on the flat edge, one
  on the leg end, centred in the leg.
- Upright sockets are 18 mm deep and bar sockets 16 mm. The two upright sockets in a leg are separated by
  a 4 mm divider with a 4 mm through-hole.

If any of these differ on your rack, change the values in the part's source and
regenerate.

## Parts

| Part | What it does | Status |
|---|---|---|
| [Shared-wall bracket](shared-wall-bracket/) | Joins two or more racks into one unit with shared centre walls. Two layouts: in line (36 mm thick) and staggered (18 mm thick, the stock width). | Modelled from measurements; socket fit not yet test-printed. |
| [Anti-tip wall plate](anti-tip-wall-plate/) | Wall plate with a saddle for a zip-tie tether from a bracket's tie slit (or a rack upright). | Modelled; not printed or load tested. |

[View the shared-wall bracket in 3D](shared-wall-bracket/README.md#interactive-3d-view), or open any `.stl` under `shared-wall-bracket/models/` for GitHub's built-in viewer.

## Download

Each [release](https://github.com/csmarshall/filament-rack-addon-brackets/releases/latest)
has two archives:

- `filament-rack-addon-brackets-prints-vX.Y.Z.zip`: for every part, the STL and
  3MF print files, STEP, the drawing and the README, with the print settings,
  disclaimer and licences. Take this one to print.
- `filament-rack-addon-brackets-source-vX.Y.Z.zip`: everything in the
  repository, including the scripts.

## Print settings

[PRINT_SETTINGS.md](PRINT_SETTINGS.md) lists every slicer setting to change
from the defaults, with where to find each one. Start there if you import an
STL: only the `.3mf` projects carry the settings, and only when opened as a
project. Each part's README has the same table with the reasons.

- [Shared-wall bracket settings](shared-wall-bracket/README.md#settings-to-change-from-the-slicers-defaults)
- [Anti-tip wall plate settings](anti-tip-wall-plate/README.md#printing)

## Repository layout

| Path | Contents |
|---|---|
| `shared-wall-bracket/` | Source, STL/STEP/3MF models and notes for the shared-wall bracket. |
| `anti-tip-wall-plate/` | Source and STL/STEP models for the anti-tip wall plate. |
| `tools/make_u1_project.py` | Packages an STL as a Snapmaker Orca project for the Snapmaker U1. |
| `PRINT_SETTINGS.md` | Slicer settings for every part, in one place. |
| `docs/claude-code-handoff.md` | Project brief with the bracket source inline. |
| `docs/MAINTAINING.md` | How the repo is run: process, releases, licence map, rebuilding the models. |

## Setup

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
```

## Versions

Releases are numbered `MAJOR.MINOR.PATCH`. The patch number goes up
automatically with every change merged to `main`. Major and minor bumps are a
deliberate manual choice, made by running the Publish workflow by hand, for a
change that alters how a part fits or is used.

## Licence

The designs are free to print and remix for non-commercial use, with credit:
[CC BY-NC-SA 4.0](LICENSES/CC-BY-NC-SA-4.0.txt). **Selling these files, or prints made
from them, needs permission.** The scripts and other code are
[MIT](LICENSES/MIT.txt). [LICENSE.md](LICENSE.md) says which file is under which.
See also the [disclaimer](DISCLAIMER.md).

**Why these licences:** so that anyone can print these parts and improve on
them, and nobody sells them as their own. The models are share-alike and
non-commercial so they stay credited, open and off the marketplaces; the code
is MIT so it can be reused anywhere. The reasoning is set out in
[LICENSE.md](LICENSE.md#why-these-licences).

If these parts saved you some filament or a toppled rack, you can
[buy me a coffee](https://buymeacoffee.com/cs_marshall).
