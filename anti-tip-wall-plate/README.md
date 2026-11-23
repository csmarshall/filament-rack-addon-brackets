# Anti-tip wall plate

A small plate that screws to the wall, with a raised saddle for a zip tie. It
follows the layout of the common two-plate furniture anti-tip kit. On the rack
side the tie goes through one of the
[shared-wall brackets' tie slits](../shared-wall-bracket/#tie-slits), or
straight around a steel upright.

<!-- blueprint-preview:preview -->
[![The anti-tip wall plate](preview.svg)](preview.svg)

<sub>Preview generated from `wall_plate.py` by [common-blueprint-generator](https://github.com/csmarshall/common-blueprint-generator) on every change to the model · [Buy me a coffee](https://buymeacoffee.com/cs_marshall)</sub>
<!-- /blueprint-preview -->

> **Use at your own risk.** This is not a tested or certified tip-over
> restraint. It has not been printed or load tested, and no load rating is
> stated or implied. See the [disclaimer](../DISCLAIMER.md).

## Use

- Fit it as high on the rack as you can: through a tie slit of a top-tier
  bracket, or around a rear upright just under the top bracket.
- Use a bought nylon zip tie, not a printed one. The slot is 9.5 x 3.2 mm, for
  ties up to 7.6 mm wide. A 250 mm tie is a reasonable length.
- Two screw holes, 4.8 mm, for #8 or 4 mm pan-head screws. Fix into a stud
  where possible; otherwise use an anchor suited to your wall.
- Use at least two tether points on a double-wide rack.

## Printing

Print it standing on its profile (the T-shaped face on the bed, the 22 mm
width pointing up). The layers then run unbroken through the plate and around
the saddle. Printed flat on its back, a pull would try to peel the saddle off
along a layer line.

| Setting | Set it to | Where (tab / group) |
|---|---|---|
| Wall loops | **4 or more** | Strength / Walls |
| Filament | **ABS, ASA or PETG. Not PLA.** | Filament slot |

No supports. At this size, 4 wall loops print nearly solid.

**Do not print it in PLA.** The tie keeps the plate under constant load, and
PLA slowly deforms under constant load and softens when warm. Use PETG, ABS or
ASA.

## Drawing

<!-- blueprint:blueprint -->
[![Blueprint of the anti-tip wall plate](blueprint.svg)](blueprint.svg)

<sub>Drawing generated from `wall_plate.py` by [common-blueprint-generator](https://github.com/csmarshall/common-blueprint-generator) on every change to the model · [Buy me a coffee](https://buymeacoffee.com/cs_marshall)</sub>
<!-- /blueprint -->

Profile, plan, end and isometric views, projected from the CAD model with the
dimensions read from the same parameters. The Publish workflow redraws it
whenever the model changes.

## Files

| Path | What it is |
|---|---|
| `wall_plate.py` | Parametric CadQuery source. |
| `make_blueprint.py` | Draws `blueprint.svg`. |
| `blueprint.svg` | Dimensioned drawing, generated on [common-blueprint-generator](https://github.com/csmarshall/common-blueprint-generator). |
| `make_preview.py`, `preview.svg` | The header image at the top of this page, drawn by common-blueprint-generator's `preview()`; the Publish workflow redraws it. |
| `models/anti_tip_wall_plate.stl` / `.step` | The plate: 60 x 22 mm, 14.2 mm tall. |

## Regenerating

```sh
python3 wall_plate.py                                   # writes models/
python3 wall_plate.py --tie-width 4.8 --tie-thickness 1.4
python3 make_blueprint.py                               # redraws blueprint.svg and the embed above
python3 make_preview.py                                 # redraws preview.svg, the header image
```
