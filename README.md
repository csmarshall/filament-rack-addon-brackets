# Filament rack add-on brackets

3D-printable add-on parts for the 9-tier, 54-spool modular 3D printer filament
storage rack sold on Amazon as the
[Hizypaixin 9-Tier 3D Printer Filament Storage Rack](https://www.amazon.com/dp/B0FFZ8SSQX)
(ASIN B0FFZ8SSQX).

> **Use at your own risk.** These are untested hobby designs shared for
> educational purposes, with no warranty and no load rating. Read the
> [disclaimer](DISCLAIMER.md) before printing or installing anything.

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
- Every socket is 18 mm deep. The two upright sockets in a leg are separated by
  a 4 mm divider with a 4 mm through-hole.

If any of these differ on your rack, change the values in the part's source and
regenerate.

## Parts

| Part | What it does | Status |
|---|---|---|
| [Shared-wall bracket](shared-wall-bracket/) | Joins two racks into one double-wide unit with a shared centre wall. | Modelled from measurements; socket fit not yet test-printed. |
| [Anti-tip wall plate](anti-tip-wall-plate/) | Wall plate with a saddle for a zip-tie tether to a rack upright. | Modelled; not printed or load tested. |

[View the shared-wall bracket in 3D](shared-wall-bracket/README.md#interactive-3d-view), or open any `.stl` under `shared-wall-bracket/models/` for GitHub's built-in viewer.

## Repository layout

| Path | Contents |
|---|---|
| `shared-wall-bracket/` | Source, STL/STEP/3MF models and notes for the shared-wall bracket. |
| `anti-tip-wall-plate/` | Source and STL/STEP models for the anti-tip wall plate. |
| `tools/make_u1_project.py` | Packages an STL as a Snapmaker Orca project for the Snapmaker U1. |
| `docs/claude-code-handoff.md` | Project brief with the bracket source inline. |

## Setup

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
```

## License

MIT. See [LICENSE](LICENSE) and the [disclaimer](DISCLAIMER.md).
