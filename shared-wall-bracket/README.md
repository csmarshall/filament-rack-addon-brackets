# Shared-wall bracket

Lets two columns of the rack stand side by side and share one centre wall,
instead of standing as two separate towers.

![Preview](preview.png)

An interactive 3D view is [at the bottom of this page](#interactive-3d-view).
GitHub also shows a rotatable viewer when you open any file in `models/` ending in `.stl`.

The stock bracket has bar sockets on one face only. This part is two stock
brackets back to back in one piece, with bar sockets on both faces and a single
centred row of upright sockets. Nine make a full-height shared wall, and free
up nine stock brackets and a set of uprights from the second kit.

> **Use at your own risk.** Untested hobby design, no warranty, no load rating.
> See the [disclaimer](../DISCLAIMER.md).

## Two layouts

![In-line and staggered brackets](layouts.png)

| | In line | Staggered |
|---|---|---|
| Size | 40 x 305 x 40 mm | 18 x 320 x 40 mm (the stock bracket's width) |
| Rail height | 18 mm, as stock | 27 mm |
| Ends | Fully rounded, a 20 mm radius across the whole width | Fully rounded around the upright sockets, as stock |
| Bar sockets | 16 mm deep, as measured on the stock part; the two faces end to end with an 8 mm web between | 16 mm deep, as measured on the stock part; one face's set is shifted 16 mm along the bracket so the two pass side by side |
| Columns | Line up front and back | Neighbouring columns stand 16 mm apart front to back |
| Parts | One design, plus an anchor variant | A mirror-image pair, A and B, each with an anchor variant; anchored end brackets, left and right |
| Solid volume | 220 cm3 | 138 cm3 |
| Printed, estimated (ABS, 5 walls, 15% infill) | about 129 g | about 98 g |
| Rail bending strength, vertical | 1.00 | 1.01 |
| Rail stiffness, vertical | 1.00 | 1.52 |
| Rail stiffness, sideways | 1.00 | 0.14 |
| Wall around upright sockets | 2.85 mm at the end, 10.6 mm at the sides | 2.85 mm all round, as stock |

**Why the staggered rail is taller.** A shared wall carries two columns. The
staggered rail is under half as wide as the in-line one, and bending strength
goes with width x height squared, so its rail is 27 mm tall where the stock
rail is 18: 18 x 27 squared equals 40 x 18 squared. The extra 9 mm is on the
side away from the flat edge, in the open space between the two legs. The bar
sockets stay 8 mm from the flat edge and the upright divider does not move, so
bars and tiers still line up with the stock walls.

**Where the staggered bracket is not as strong.** Sideways it is much less
stiff, and its upright sockets have the stock 2.85 mm wall all round where the
in-line bracket has 10.6 mm at the sides. The bars brace the wall sideways and
the stock brackets work with that same wall, but the in-line bracket has more
margin. These figures are section-property ratios, not test results; neither
layout has been load tested.

**Staggered A and B.** Facing the rack, an A bracket sets the column on its
right 16 mm further back; a B bracket sets the column on its left further
back. Turning a bracket end for end changes nothing. Turning one upside down
does not make an A into a B: the bars would sit at the wrong height. Use the
B models.

**Tethering a staggered wall.** Each staggered bracket has an anchor variant
and there is an anchored end bracket for each end of the row; see
[Anchor variants](#anchor-variants). Without them, loop the zip tie around a
rear upright tube just under the top bracket and through the
[wall plate](../anti-tip-wall-plate/).

### A row of columns

![Plan view of a row of five columns in each layout](row_of_five.png)

For a row of five columns, each tier needs four shared-wall brackets and two
stock brackets at the ends:

- **In line:** 4 in-line brackets. Every column lines up.
- **Staggered, alternating:** 2 A and 2 B. Columns 2 and 4 sit 16 mm back.
- **Staggered, A only:** 4 A. Each column steps a further 16 mm back, 64 mm
  across the row.

**Staggered rows: use an odd number of columns, three or more.** Alternate
the brackets so every tier has the same number of A and B. The two end columns
then stand the same distance from the wall. With an even number of columns, or
with two columns on a single bracket, one end of the row sits 16 mm further
out than the other. Start with B at the left (B, A, B, A, ...) so the end
columns are the ones nearest the wall; that is where the anchored end brackets
go.

In the staggered layouts some columns stand off the wall. The zip-tie tether
bridges that gap; add a spacer only if you want every column bearing on the
wall. `make_layout_diagram.py --columns N` redraws the diagram for any row.

## Status

- Geometry is built from caliper measurements of a stock bracket (see the
  [top-level README](../README.md#does-your-rack-match)).
- **Socket fit is untested.** Sockets are 12.3 mm for a 12 mm tube. Print
  `models/fit_test_coupon_v2.stl` first and adjust `--fit-clearance`.
- Two values are judged from photos, not measured: the 20 mm inside corner
  radius and the upright socket centre at 9 mm from the end.
- The `.3mf` projects were generated by script and pass a strict 3MF read, but
  have **not been opened in Snapmaker Orca**. Check the wall count, wall
  generator and slot 1 filament after loading.

## Load warning

The shared uprights carry both columns, roughly double the stock load on those
two tubes. Reviews of this rack report tubes buckling and the tower tipping at
nine loaded tiers. Anchor the rack to a wall and keep heavy spools low. Use
an anchor variant on the top tier: it has a zip-tie saddle on its rear end,
in the style of a furniture anti-tip kit. A zip tie runs through that saddle
and through the [anti-tip wall plate](../anti-tip-wall-plate/) screwed to the
wall.

## Files

| Path | What it is |
|---|---|
| `shared_wall_bracket.py` | Parametric CadQuery source. Writes STEP and STL. |
| `models/shared_wall_bracket_v2.*` | The in-line bracket (STL, STEP, Snapmaker U1 project). |
| `models/shared_wall_bracket_v2_anchor.*` | The in-line bracket with a zip-tie saddle on the rear end. |
| `models/shared_wall_bracket_staggered_a.*`, `_b.*` | The staggered bracket, A and its mirror image B. |
| `models/shared_wall_bracket_staggered_a_anchor.*`, `_b_anchor.*` | The staggered brackets with a zip-tie collar on the rear end. |
| `models/end_bracket_left_anchor.*`, `_right_anchor.*` | A stock-size bracket for the end of a row, sockets on one face only, with the zip-tie collar. Left and right are named facing the rack. |
| `models/fit_test_coupon_v2.*` | One upright socket and one bar socket, for tuning fit. |
| `blueprint.svg` | Dimensioned drawing of the in-line bracket, generated by `make_blueprint.py` on [common-blueprint-generator](https://github.com/csmarshall/common-blueprint-generator). |
| `blueprint_staggered.svg`, `blueprint_end.svg`, `blueprint_coupon.svg` | The drawings of the staggered A/B brackets, the end brackets and the fit test coupon, from `make_blueprint_staggered.py`, `make_blueprint_end.py` and `make_blueprint_coupon.py`. They share `sheet_parts.py` and `../tools/blueprint_helpers.py`. |
| `make_layout_diagram.py` | Draws `row_of_five.png`, the plan view of a row of columns. |
| `make_readme_stl.py` | Rewrites the small viewer mesh embedded at the bottom of this page. |
| `legacy/` | First version, drawn from listing photos before measuring. Not for printing. |

## Drawing

<!-- blueprint:blueprint -->
[![Blueprint of the shared-wall bracket](blueprint.svg)](blueprint.svg)

<sub>Drawing generated from `shared_wall_bracket.py` by [common-blueprint-generator](https://github.com/csmarshall/common-blueprint-generator) on every change to the model · [Buy me a coffee](https://buymeacoffee.com/cs_marshall)</sub>
<!-- /blueprint -->

Top, front, bottom and end views, a section through a bar socket, an
isometric, and a detail of the anchor variant's saddle. Every view is projected
from the CAD model, and the dimensions come from the same parameters, so the
sheet matches what is printed. The Publish workflow redraws it whenever the
model changes.

### Staggered bracket, A and B

Both faces of A, the plan, a section through a bar socket, and the anchor
variant's collar as a detail. B is A's mirror image and is described on the
sheet, not drawn.

<!-- blueprint:blueprint_staggered -->
[![Blueprint of the staggered bracket, A and B](blueprint_staggered.svg)](blueprint_staggered.svg)

<sub>Drawing generated from `shared_wall_bracket.py` by [common-blueprint-generator](https://github.com/csmarshall/common-blueprint-generator) on every change to the model · [Buy me a coffee](https://buymeacoffee.com/cs_marshall)</sub>
<!-- /blueprint -->

### End bracket, left and right

The anchored left bracket, with a section and the anchor detail. The right
bracket is its mirror image.

<!-- blueprint:blueprint_end -->
[![Blueprint of the end bracket, left and right](blueprint_end.svg)](blueprint_end.svg)

<sub>Drawing generated from `shared_wall_bracket.py` by [common-blueprint-generator](https://github.com/csmarshall/common-blueprint-generator) on every change to the model · [Buy me a coffee](https://buymeacoffee.com/cs_marshall)</sub>
<!-- /blueprint -->

### Fit test coupon

<!-- blueprint:blueprint_coupon -->
[![Blueprint of the fit-test coupon](blueprint_coupon.svg)](blueprint_coupon.svg)

<sub>Drawing generated from `shared_wall_bracket.py` by [common-blueprint-generator](https://github.com/csmarshall/common-blueprint-generator) on every change to the model · [Buy me a coffee](https://buymeacoffee.com/cs_marshall)</sub>
<!-- /blueprint -->

## Design

The drawing and the points below describe the in-line bracket. The staggered
one shares its leg height, bar socket position and divider.

- 40 x 305 x 40 mm: two 16 mm bar sockets and an 8 mm centre web.
- A 4 mm vent runs through the web between each pair of opposite bar sockets,
  like the hole in the upright divider, so a bar is not pushed in against
  trapped air. The bar still seats on the 4 mm of web around the vent.
- The upright divider is 4 mm to match the stock part. It sets tier height, so
  it must not change, or the centre wall drifts out of level with the outer
  walls on every tier.
- Bar positions and height match the stock bracket, because the far end of
  every bar sits in a stock bracket.
- Seen from above, each end is rounded off completely, like the stock part: a
  20 mm radius across the 40 mm width. The wall at the tip of the upright
  socket is still 2.85 mm, and the bar sockets all open on the straight sides.

## Anchor variants

Each is for the top tier, with a zip tie through the
[wall plate](../anti-tip-wall-plate/). The slot is 13 x 3.2 mm, for a tie up
to 7.6 mm wide, behind a 6 mm bar, and runs 22 mm up from the flat edge. Every
variant is 9.2 mm longer at the back than its plain bracket.

**In line.** A saddle on the rear end face. The slot is wider than the upright
socket, so the saddle's legs join solid plastic either side of the socket. The
2.85 mm wall behind the socket is unchanged and carries none of the tether
load.

**Staggered A and B, and the end brackets.** At 18 mm wide the slot would
leave no room for legs, so the saddle becomes a collar: the rear 26 mm of the
bracket widens to 23 mm, 22 mm up from the flat edge, and tapers back to 18.
The collar's legs run down both sides of the rear upright socket and take the
side wall there from 2.85 to 5.35 mm. The wall between the socket and the tie
slot stays 2.85 mm. The collar stops short of the last bar socket.

**End brackets.** The stock bracket's size and 18 mm rail, with bar sockets on
one face only and the collar on the rear end. They replace the stock bracket
at each end of the top tier, so a staggered row can be tethered at its ends as
well as, or instead of, at its shared walls. They carry one column, as the
stock bracket does. Left and right are a mirror pair.

All of them print as one profile rising from the bed, so the layers run
unbroken through the legs and the bar, and a pull toward the wall loads the
plastic along the layers. The tether leaves a gap to the wall, so the rack
does not have to sit flush. None has been load tested.

## Printing

### Settings to change from the slicer's defaults

If you **import** an STL, or import a `.3mf` instead of opening it as a
project, none of these are set for you. Set them by hand. The location is
where each one sits in Snapmaker Orca and OrcaSlicer.

| Setting | Set it to | Where (tab / group) | U1 stock value |
|---|---|---|---|
| Wall loops | **5** | Strength / Walls | 2 |
| Wall generator | **Arachne** | Quality / Wall generator | Classic |
| Sparse infill pattern | **Gyroid** | Strength / Infill | Grid |
| Sparse infill density | **15%** | Strength / Infill | 15% (unchanged) |
| Bottom shell layers | **5** | Strength / Top/bottom shells | 3 |
| Brim type | **Outer brim only** | Others / Brim | Auto |
| Brim width | **5 to 10 mm** (see below) | Others / Brim | 5 mm |
| Filament | **ABS, ASA or PETG. Not PLA.** | Filament slot | PLA |
| Layer height | 0.20 mm | Quality / Layer height | 0.20 mm (unchanged) |

Then, on the plate:

1. Lay the part with its **flat edge on the bed** (the long straight edge, with
   the legs pointing up). No supports.
2. **Rotate it 45 degrees** about the vertical and centre it. It only fits a
   270 mm bed corner to corner, one per plate.
3. A 10 mm brim fits a 270 x 270 mm bed on every version except the anchored
   staggered brackets, which use 5 mm (a 10 mm brim would leave only 3.9 mm to
   the bed edge).

The reasons for each value are in [Why these settings](#why-these-settings).
The `.3mf` projects in `models/` carry all of this, but only when opened with
**File > Open Project**.

### Notes


- Orientation: flat edge on the bed, no supports.
- Snapmaker U1 (270 x 270 mm bed): every version only fits rotated 45 degrees,
  one per plate. Clear to the bed edge: in line 21 mm (anchor 18 mm); staggered
  19 mm. The anchored staggered brackets are the tightest, 329 mm long: with
  the 5 mm brim in their project files they clear the bed edge by 8.9 mm. The
  end brackets clear it by 9.2 mm.
- 5 wall loops with the Arachne wall generator, so the 1.85, 2.85 and 3.85 mm
  socket walls print as solid perimeters.
- 15% gyroid infill and 5 bottom shell layers. See
  [Why these settings](#why-these-settings).
- **Not PLA.** The bracket is under constant load, and PLA slowly deforms
  under constant load and softens when warm.
- PETG or ABS. A 305 mm ABS part is prone to warping; use a brim and keep
  draughts off it.

## Why these settings

Snapmaker Orca is a fork of OrcaSlicer, so the OrcaSlicer wiki is the reference
for these settings. The stock U1 `0.20mm Standard` process uses 2 wall loops,
the Classic wall generator, 15% grid infill and 3 bottom shell layers.

| Setting | Stock | Here | Basis |
|---|---|---|---|
| Wall loops | 2 | 5 | Calculated. Each socket wall gets loops from both faces, so loops needed = (wall / 2) / line width. At the stock 0.42 mm outer and 0.45 mm inner line widths, 5 loops fill the thickest socket wall (3.85 mm). |
| Wall generator | Classic | Arachne | Varies line width to close the slivers a fixed-width wall would leave. |
| Infill pattern | Grid | Gyroid | Documented. The [OrcaSlicer patterns page](https://www.orcaslicer.com/wiki/print_settings/strength/strength_settings_patterns.html) says grid's overlapping points may cause noise or artifacts, and describes gyroid as isotropic, with curved geometry that helps reduce warping. |
| Bottom shell layers | 3 | 5 | Precaution, not documented behaviour. The [shells page](https://www.orcaslicer.com/wiki/print_settings/strength/strength_settings_top_bottom_shells.html) says more shell layers increase part strength. The specific aim is to make the 1.85 mm wall between the bed face and each bar socket print fully solid; check that in the slicer preview. |
| Brim | Slicer default | Outer, 10 mm (5 mm on the anchored staggered brackets) | A long ABS part lifts at the ends. The width is what fits inside the bed margin. |

With 5 wall loops the walls carry nearly all the load, so the infill choice is
mostly about print reliability.

## Opening the U1 projects

Use **File > Open Project** (or drag the `.3mf` in and choose to open it as a
project). **Import** loads the geometry only and discards every setting in the
file, including the ones stored on the part.

## Regenerating

From this folder, with the virtual environment from the top-level README active:

```sh
pip install -r ../requirements.txt "common-blueprint-generator @ git+https://github.com/csmarshall/common-blueprint-generator"
python3 shared_wall_bracket.py --out models             # rebuilds every STL and STEP
python3 shared_wall_bracket.py --fit-clearance 0.35      # looser sockets
python3 make_blueprint.py                                # redraws blueprint.svg and the embed above
python3 make_blueprint_staggered.py                      # likewise for the staggered A/B sheet
python3 make_blueprint_end.py                            # the end bracket sheet
python3 make_blueprint_coupon.py                         # the fit test coupon sheet
python3 make_layout_diagram.py                           # redraws row_of_five.png
python3 make_readme_stl.py                               # refreshes the 3D view below
```

To rebuild a U1 project you also need the `Snapmaker` folder from
[snapmaker-profiles](https://github.com/Snapmaker/snapmaker-profiles):

```sh
python3 ../tools/make_u1_project.py \
  --stl out_v2/shared_wall_bracket_v2.stl \
  --profiles /path/to/snapmaker-profiles/Snapmaker \
  --out models/shared_wall_bracket_v2_U1_ABS.3mf \
  --brim-width 10
```

The project selects the stock `Snapmaker U1 (0.4 nozzle)` printer, the
`0.20mm Standard` process and `Generic ABS @U1 0.4 nozzle` in slot 1. It
overrides wall loops (5), wall generator (Arachne), infill (15% gyroid) and
bottom shell layers (5), and adds a 10 mm outer brim (`--brim-width`; 5 for the
anchored staggered brackets).
These settings are written both to the process and to the part itself.

## Interactive 3D view

Drag to rotate. This is a simplified mesh for viewing only (square corners, no
lead-in chamfers or vent holes); print from the files in `models/`. If no
viewer appears here, open
[`models/shared_wall_bracket_v2.stl`](models/shared_wall_bracket_v2.stl), which
GitHub displays in its own 3D viewer.

```stl
solid shared_wall_bracket
facet normal -0.00 -0.00 -1.00
outer loop
vertex 5.4 6.1 0.0
vertex 20.0 0.0 0.0
vertex 3.5 3.9 0.0
endloop
endfacet
facet normal 0.00 0.00 -1.00
outer loop
vertex 0.7 2.9 0.0
vertex 3.5 3.9 0.0
vertex 20.0 0.0 0.0
endloop
endfacet
facet normal -0.00 -0.00 -1.00
outer loop
vertex 6.2 9.0 0.0
vertex 20.0 0.0 0.0
vertex 5.4 6.1 0.0
endloop
endfacet
facet normal -0.00 -0.00 -1.00
outer loop
vertex 5.4 11.9 0.0
vertex 20.0 0.0 0.0
vertex 6.2 9.0 0.0
endloop
endfacet
facet normal -0.00 -0.00 -1.00
outer loop
vertex 3.5 14.1 0.0
vertex 20.0 0.0 0.0
vertex 5.4 11.9 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex -20.0 0.0 0.0
vertex -4.6 13.1 0.0
vertex -6.0 10.5 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex -20.0 0.0 0.0
vertex -6.0 10.5 0.0
vertex -6.0 7.5 0.0
endloop
endfacet
facet normal 0.00 0.00 -1.00
outer loop
vertex -20.0 0.0 0.0
vertex -6.0 7.5 0.0
vertex -4.6 4.9 0.0
endloop
endfacet
facet normal 0.00 0.00 -1.00
outer loop
vertex -20.0 0.0 0.0
vertex -4.6 4.9 0.0
vertex -2.2 3.2 0.0
endloop
endfacet
facet normal 0.00 0.00 -1.00
outer loop
vertex -20.0 0.0 0.0
vertex -2.2 3.2 0.0
vertex 0.7 2.9 0.0
endloop
endfacet
facet normal 0.00 0.00 -1.00
outer loop
vertex -20.0 0.0 0.0
vertex 0.7 2.9 0.0
vertex 20.0 0.0 0.0
endloop
endfacet
facet normal 0.00 0.00 -1.00
outer loop
vertex 3.5 290.9 0.0
vertex 20.0 305.0 0.0
vertex 20.0 0.0 0.0
endloop
endfacet
facet normal -0.00 -0.00 -1.00
outer loop
vertex 3.5 290.9 0.0
vertex 20.0 0.0 0.0
vertex 3.5 14.1 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex 5.4 293.1 0.0
vertex 20.0 305.0 0.0
vertex 3.5 290.9 0.0
endloop
endfacet
facet normal -0.00 -0.00 -1.00
outer loop
vertex 0.7 289.9 0.0
vertex 3.5 14.1 0.0
vertex 0.7 15.1 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex 0.7 289.9 0.0
vertex 0.7 15.1 0.0
vertex -2.2 14.8 0.0
endloop
endfacet
facet normal 0.00 0.00 -1.00
outer loop
vertex 0.7 289.9 0.0
vertex 3.5 290.9 0.0
vertex 3.5 14.1 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex 6.2 296.0 0.0
vertex 20.0 305.0 0.0
vertex 5.4 293.1 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex -2.2 290.2 0.0
vertex -2.2 14.8 0.0
vertex -4.6 13.1 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex -2.2 290.2 0.0
vertex 0.7 289.9 0.0
vertex -2.2 14.8 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex 5.4 298.9 0.0
vertex 20.0 305.0 0.0
vertex 6.2 296.0 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex -4.6 291.9 0.0
vertex -2.2 290.2 0.0
vertex -4.6 13.1 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex 3.5 301.1 0.0
vertex 20.0 305.0 0.0
vertex 5.4 298.9 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex 0.7 302.1 0.0
vertex 20.0 305.0 0.0
vertex 3.5 301.1 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex -20.0 305.0 0.0
vertex 0.7 302.1 0.0
vertex -2.2 301.8 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex -20.0 305.0 0.0
vertex -2.2 301.8 0.0
vertex -4.6 300.1 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex -20.0 305.0 0.0
vertex -4.6 300.1 0.0
vertex -6.0 297.5 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex -20.0 305.0 0.0
vertex -6.0 297.5 0.0
vertex -6.0 294.5 0.0
endloop
endfacet
facet normal 0.00 0.00 -1.00
outer loop
vertex -20.0 305.0 0.0
vertex -6.0 294.5 0.0
vertex -4.6 291.9 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex -20.0 305.0 0.0
vertex 20.0 305.0 0.0
vertex 0.7 302.1 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex -20.0 305.0 0.0
vertex -4.6 291.9 0.0
vertex -20.0 0.0 0.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex -4.6 291.9 0.0
vertex -4.6 13.1 0.0
vertex -20.0 0.0 0.0
endloop
endfacet
facet normal 0.00 -1.00 0.00
outer loop
vertex -20.0 0.0 0.0
vertex 20.0 0.0 40.0
vertex -20.0 0.0 40.0
endloop
endfacet
facet normal 0.00 -1.00 0.00
outer loop
vertex -20.0 0.0 0.0
vertex 20.0 0.0 0.0
vertex 20.0 0.0 40.0
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 283.4 5.1
vertex 20.0 281.5 2.9
vertex 20.0 305.0 0.0
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 20.0 278.7 1.9
vertex 20.0 305.0 0.0
vertex 20.0 281.5 2.9
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 284.1 8.0
vertex 20.0 283.4 5.1
vertex 20.0 305.0 0.0
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 283.4 10.9
vertex 20.0 284.1 8.0
vertex 20.0 305.0 0.0
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 281.1 23.9
vertex 20.0 281.5 13.1
vertex 20.0 283.4 10.9
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 281.1 23.9
vertex 20.0 278.7 14.1
vertex 20.0 281.5 13.1
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 285.5 30.3
vertex 20.0 281.1 23.9
vertex 20.0 283.4 10.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 285.5 30.3
vertex 20.0 305.0 0.0
vertex 20.0 305.0 40.0
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 285.5 30.3
vertex 20.0 283.4 10.9
vertex 20.0 305.0 0.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 274.7 19.5
vertex 20.0 275.8 13.8
vertex 20.0 278.7 14.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 274.7 19.5
vertex 20.0 273.4 12.1
vertex 20.0 275.8 13.8
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 274.7 19.5
vertex 20.0 278.7 14.1
vertex 20.0 281.1 23.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 287.0 38.0
vertex 20.0 285.5 30.3
vertex 20.0 305.0 40.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 267.0 18.0
vertex 20.0 272.0 9.5
vertex 20.0 273.4 12.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 267.0 18.0
vertex 20.0 272.0 6.5
vertex 20.0 272.0 9.5
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 267.0 18.0
vertex 20.0 273.4 12.1
vertex 20.0 274.7 19.5
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 287.0 40.0
vertex 20.0 287.0 38.0
vertex 20.0 305.0 40.0
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 20.0 197.5 2.9
vertex 20.0 275.8 2.2
vertex 20.0 273.4 3.9
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 199.4 5.1
vertex 20.0 272.0 6.5
vertex 20.0 267.0 18.0
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 20.0 199.4 5.1
vertex 20.0 273.4 3.9
vertex 20.0 272.0 6.5
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 199.4 5.1
vertex 20.0 197.5 2.9
vertex 20.0 273.4 3.9
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 194.7 1.9
vertex 20.0 275.8 2.2
vertex 20.0 197.5 2.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 200.2 8.0
vertex 20.0 199.4 5.1
vertex 20.0 267.0 18.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 199.4 10.9
vertex 20.0 200.2 8.0
vertex 20.0 267.0 18.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 197.5 13.1
vertex 20.0 199.4 10.9
vertex 20.0 267.0 18.0
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 20.0 113.5 2.9
vertex 20.0 191.8 2.2
vertex 20.0 189.4 3.9
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 20.0 115.4 5.1
vertex 20.0 189.4 3.9
vertex 20.0 188.0 6.5
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 115.4 5.1
vertex 20.0 113.5 2.9
vertex 20.0 189.4 3.9
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 110.7 1.9
vertex 20.0 191.8 2.2
vertex 20.0 113.5 2.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 116.2 8.0
vertex 20.0 188.0 6.5
vertex 20.0 188.0 9.5
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 116.2 8.0
vertex 20.0 115.4 5.1
vertex 20.0 188.0 6.5
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 115.4 10.9
vertex 20.0 188.0 9.5
vertex 20.0 189.4 12.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 115.4 10.9
vertex 20.0 116.2 8.0
vertex 20.0 188.0 9.5
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 113.5 13.1
vertex 20.0 189.4 12.1
vertex 20.0 191.8 13.8
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 113.5 13.1
vertex 20.0 115.4 10.9
vertex 20.0 189.4 12.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 110.7 14.1
vertex 20.0 113.5 13.1
vertex 20.0 191.8 13.8
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 20.0 29.5 2.9
vertex 20.0 107.8 2.2
vertex 20.0 105.4 3.9
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 20.0 31.4 5.1
vertex 20.0 105.4 3.9
vertex 20.0 104.0 6.5
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 31.4 5.1
vertex 20.0 29.5 2.9
vertex 20.0 105.4 3.9
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 26.7 1.9
vertex 20.0 107.8 2.2
vertex 20.0 29.5 2.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 38.0 18.0
vertex 20.0 105.4 12.1
vertex 20.0 107.8 13.8
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 38.0 18.0
vertex 20.0 104.0 9.5
vertex 20.0 105.4 12.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 38.0 18.0
vertex 20.0 104.0 6.5
vertex 20.0 104.0 9.5
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 38.0 18.0
vertex 20.0 31.4 10.9
vertex 20.0 32.1 8.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 38.0 18.0
vertex 20.0 31.4 5.1
vertex 20.0 104.0 6.5
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 38.0 18.0
vertex 20.0 32.1 8.0
vertex 20.0 31.4 5.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 29.5 13.1
vertex 20.0 31.4 10.9
vertex 20.0 38.0 18.0
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 30.3 19.5
vertex 20.0 26.7 14.1
vertex 20.0 29.5 13.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 30.3 19.5
vertex 20.0 29.5 13.1
vertex 20.0 38.0 18.0
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 0.0 0.0
vertex 20.0 20.0 6.5
vertex 20.0 20.0 9.5
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 0.0 0.0
vertex 20.0 21.4 3.9
vertex 20.0 20.0 6.5
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 0.0 0.0
vertex 20.0 23.8 2.2
vertex 20.0 21.4 3.9
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 0.0 0.0
vertex 20.0 26.7 1.9
vertex 20.0 23.8 2.2
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 23.9 23.9
vertex 20.0 23.8 13.8
vertex 20.0 26.7 14.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 23.9 23.9
vertex 20.0 21.4 12.1
vertex 20.0 23.8 13.8
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 23.9 23.9
vertex 20.0 26.7 14.1
vertex 20.0 30.3 19.5
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 19.5 30.3
vertex 20.0 21.4 12.1
vertex 20.0 23.9 23.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 19.5 30.3
vertex 20.0 20.0 9.5
vertex 20.0 21.4 12.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 19.5 30.3
vertex 20.0 0.0 0.0
vertex 20.0 20.0 9.5
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 0.0 40.0
vertex 20.0 0.0 0.0
vertex 20.0 19.5 30.3
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 20.0 0.0 40.0
vertex 20.0 19.5 30.3
vertex 20.0 18.0 38.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 0.0 40.0
vertex 20.0 18.0 38.0
vertex 20.0 18.0 40.0
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 0.0 0.0
vertex 20.0 305.0 0.0
vertex 20.0 194.7 1.9
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 20.0 194.7 1.9
vertex 20.0 305.0 0.0
vertex 20.0 278.7 1.9
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 194.7 1.9
vertex 20.0 278.7 1.9
vertex 20.0 275.8 2.2
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 0.0 0.0
vertex 20.0 194.7 1.9
vertex 20.0 191.8 2.2
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 0.0 0.0
vertex 20.0 191.8 2.2
vertex 20.0 110.7 1.9
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 0.0 0.0
vertex 20.0 110.7 1.9
vertex 20.0 107.8 2.2
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 20.0 0.0 0.0
vertex 20.0 107.8 2.2
vertex 20.0 26.7 1.9
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 267.0 18.0
vertex 20.0 38.0 18.0
vertex 20.0 110.7 14.1
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 110.7 14.1
vertex 20.0 38.0 18.0
vertex 20.0 107.8 13.8
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 20.0 267.0 18.0
vertex 20.0 110.7 14.1
vertex 20.0 194.7 14.1
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 194.7 14.1
vertex 20.0 110.7 14.1
vertex 20.0 191.8 13.8
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 20.0 267.0 18.0
vertex 20.0 194.7 14.1
vertex 20.0 197.5 13.1
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -20.0 283.4 5.1
vertex -20.0 305.0 0.0
vertex -20.0 281.5 2.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 278.7 1.9
vertex -20.0 281.5 2.9
vertex -20.0 305.0 0.0
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -20.0 284.1 8.0
vertex -20.0 305.0 0.0
vertex -20.0 283.4 5.1
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -20.0 283.4 10.9
vertex -20.0 305.0 0.0
vertex -20.0 284.1 8.0
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -20.0 281.1 23.9
vertex -20.0 283.4 10.9
vertex -20.0 281.5 13.1
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -20.0 281.1 23.9
vertex -20.0 281.5 13.1
vertex -20.0 278.7 14.1
endloop
endfacet
facet normal -1.00 -0.00 0.00
outer loop
vertex -20.0 285.5 30.3
vertex -20.0 283.4 10.9
vertex -20.0 281.1 23.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 285.5 30.3
vertex -20.0 305.0 40.0
vertex -20.0 305.0 0.0
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -20.0 285.5 30.3
vertex -20.0 305.0 0.0
vertex -20.0 283.4 10.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 274.7 19.5
vertex -20.0 278.7 14.1
vertex -20.0 275.8 13.8
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 274.7 19.5
vertex -20.0 275.8 13.8
vertex -20.0 273.4 12.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 274.7 19.5
vertex -20.0 281.1 23.9
vertex -20.0 278.7 14.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 287.0 38.0
vertex -20.0 305.0 40.0
vertex -20.0 285.5 30.3
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 267.0 18.0
vertex -20.0 273.4 12.1
vertex -20.0 272.0 9.5
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 267.0 18.0
vertex -20.0 272.0 9.5
vertex -20.0 272.0 6.5
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 267.0 18.0
vertex -20.0 274.7 19.5
vertex -20.0 273.4 12.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 287.0 40.0
vertex -20.0 305.0 40.0
vertex -20.0 287.0 38.0
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 197.5 2.9
vertex -20.0 273.4 3.9
vertex -20.0 275.8 2.2
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 199.4 5.1
vertex -20.0 267.0 18.0
vertex -20.0 272.0 6.5
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 199.4 5.1
vertex -20.0 272.0 6.5
vertex -20.0 273.4 3.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 199.4 5.1
vertex -20.0 273.4 3.9
vertex -20.0 197.5 2.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 194.7 1.9
vertex -20.0 197.5 2.9
vertex -20.0 275.8 2.2
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 200.2 8.0
vertex -20.0 267.0 18.0
vertex -20.0 199.4 5.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 199.4 10.9
vertex -20.0 267.0 18.0
vertex -20.0 200.2 8.0
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 197.5 13.1
vertex -20.0 267.0 18.0
vertex -20.0 199.4 10.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 113.5 2.9
vertex -20.0 189.4 3.9
vertex -20.0 191.8 2.2
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 115.4 5.1
vertex -20.0 188.0 6.5
vertex -20.0 189.4 3.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 115.4 5.1
vertex -20.0 189.4 3.9
vertex -20.0 113.5 2.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 110.7 1.9
vertex -20.0 113.5 2.9
vertex -20.0 191.8 2.2
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 116.2 8.0
vertex -20.0 188.0 9.5
vertex -20.0 188.0 6.5
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 116.2 8.0
vertex -20.0 188.0 6.5
vertex -20.0 115.4 5.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 115.4 10.9
vertex -20.0 189.4 12.1
vertex -20.0 188.0 9.5
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 115.4 10.9
vertex -20.0 188.0 9.5
vertex -20.0 116.2 8.0
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 113.5 13.1
vertex -20.0 191.8 13.8
vertex -20.0 189.4 12.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 113.5 13.1
vertex -20.0 189.4 12.1
vertex -20.0 115.4 10.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 110.7 14.1
vertex -20.0 191.8 13.8
vertex -20.0 113.5 13.1
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 29.5 2.9
vertex -20.0 105.4 3.9
vertex -20.0 107.8 2.2
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 31.4 5.1
vertex -20.0 104.0 6.5
vertex -20.0 105.4 3.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 31.4 5.1
vertex -20.0 105.4 3.9
vertex -20.0 29.5 2.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 26.7 1.9
vertex -20.0 29.5 2.9
vertex -20.0 107.8 2.2
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 38.0 18.0
vertex -20.0 107.8 13.8
vertex -20.0 105.4 12.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 38.0 18.0
vertex -20.0 105.4 12.1
vertex -20.0 104.0 9.5
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 38.0 18.0
vertex -20.0 104.0 9.5
vertex -20.0 104.0 6.5
endloop
endfacet
facet normal -1.00 -0.00 0.00
outer loop
vertex -20.0 38.0 18.0
vertex -20.0 32.1 8.0
vertex -20.0 31.4 10.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 38.0 18.0
vertex -20.0 104.0 6.5
vertex -20.0 31.4 5.1
endloop
endfacet
facet normal -1.00 -0.00 0.00
outer loop
vertex -20.0 38.0 18.0
vertex -20.0 31.4 5.1
vertex -20.0 32.1 8.0
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 29.5 13.1
vertex -20.0 38.0 18.0
vertex -20.0 31.4 10.9
endloop
endfacet
facet normal -1.00 -0.00 0.00
outer loop
vertex -20.0 30.3 19.5
vertex -20.0 29.5 13.1
vertex -20.0 26.7 14.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 30.3 19.5
vertex -20.0 38.0 18.0
vertex -20.0 29.5 13.1
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 0.0 0.0
vertex -20.0 20.0 9.5
vertex -20.0 20.0 6.5
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 0.0 0.0
vertex -20.0 20.0 6.5
vertex -20.0 21.4 3.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 0.0 0.0
vertex -20.0 21.4 3.9
vertex -20.0 23.8 2.2
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 0.0 0.0
vertex -20.0 23.8 2.2
vertex -20.0 26.7 1.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 23.9 23.9
vertex -20.0 26.7 14.1
vertex -20.0 23.8 13.8
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 23.9 23.9
vertex -20.0 23.8 13.8
vertex -20.0 21.4 12.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 23.9 23.9
vertex -20.0 30.3 19.5
vertex -20.0 26.7 14.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 19.5 30.3
vertex -20.0 23.9 23.9
vertex -20.0 21.4 12.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 19.5 30.3
vertex -20.0 21.4 12.1
vertex -20.0 20.0 9.5
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 19.5 30.3
vertex -20.0 20.0 9.5
vertex -20.0 0.0 0.0
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -20.0 0.0 40.0
vertex -20.0 19.5 30.3
vertex -20.0 0.0 0.0
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 0.0 40.0
vertex -20.0 18.0 38.0
vertex -20.0 19.5 30.3
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 0.0 40.0
vertex -20.0 18.0 40.0
vertex -20.0 18.0 38.0
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 0.0 0.0
vertex -20.0 194.7 1.9
vertex -20.0 305.0 0.0
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 194.7 1.9
vertex -20.0 278.7 1.9
vertex -20.0 305.0 0.0
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 194.7 1.9
vertex -20.0 275.8 2.2
vertex -20.0 278.7 1.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 0.0 0.0
vertex -20.0 191.8 2.2
vertex -20.0 194.7 1.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 0.0 0.0
vertex -20.0 110.7 1.9
vertex -20.0 191.8 2.2
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 0.0 0.0
vertex -20.0 107.8 2.2
vertex -20.0 110.7 1.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -20.0 0.0 0.0
vertex -20.0 26.7 1.9
vertex -20.0 107.8 2.2
endloop
endfacet
facet normal -1.00 -0.00 0.00
outer loop
vertex -20.0 267.0 18.0
vertex -20.0 110.7 14.1
vertex -20.0 38.0 18.0
endloop
endfacet
facet normal -1.00 -0.00 0.00
outer loop
vertex -20.0 110.7 14.1
vertex -20.0 107.8 13.8
vertex -20.0 38.0 18.0
endloop
endfacet
facet normal -1.00 -0.00 0.00
outer loop
vertex -20.0 267.0 18.0
vertex -20.0 194.7 14.1
vertex -20.0 110.7 14.1
endloop
endfacet
facet normal -1.00 -0.00 0.00
outer loop
vertex -20.0 194.7 14.1
vertex -20.0 191.8 13.8
vertex -20.0 110.7 14.1
endloop
endfacet
facet normal -1.00 -0.00 0.00
outer loop
vertex -20.0 267.0 18.0
vertex -20.0 197.5 13.1
vertex -20.0 194.7 14.1
endloop
endfacet
facet normal -0.00 1.00 0.00
outer loop
vertex -20.0 305.0 40.0
vertex 20.0 305.0 40.0
vertex 20.0 305.0 0.0
endloop
endfacet
facet normal 0.00 1.00 0.00
outer loop
vertex -20.0 305.0 40.0
vertex 20.0 305.0 0.0
vertex -20.0 305.0 0.0
endloop
endfacet
facet normal -0.97 -0.24 0.00
outer loop
vertex 5.4 11.9 0.0
vertex 6.2 9.0 0.0
vertex 6.2 9.0 18.0
endloop
endfacet
facet normal -0.97 -0.24 0.00
outer loop
vertex 5.4 11.9 0.0
vertex 6.2 9.0 18.0
vertex 5.4 11.9 18.0
endloop
endfacet
facet normal -0.75 -0.66 0.00
outer loop
vertex 3.5 14.1 0.0
vertex 5.4 11.9 18.0
vertex 3.5 14.1 18.0
endloop
endfacet
facet normal -0.75 -0.66 0.00
outer loop
vertex 3.5 14.1 0.0
vertex 5.4 11.9 0.0
vertex 5.4 11.9 18.0
endloop
endfacet
facet normal -0.35 -0.94 0.00
outer loop
vertex 0.7 15.1 0.0
vertex 3.5 14.1 18.0
vertex 0.7 15.1 18.0
endloop
endfacet
facet normal -0.35 -0.94 0.00
outer loop
vertex 0.7 15.1 0.0
vertex 3.5 14.1 0.0
vertex 3.5 14.1 18.0
endloop
endfacet
facet normal 0.12 -0.99 0.00
outer loop
vertex -2.2 14.8 0.0
vertex 0.7 15.1 18.0
vertex -2.2 14.8 18.0
endloop
endfacet
facet normal 0.57 -0.82 0.00
outer loop
vertex -2.2 14.8 0.0
vertex -2.2 14.8 18.0
vertex -4.6 13.1 18.0
endloop
endfacet
facet normal 0.12 -0.99 0.00
outer loop
vertex -2.2 14.8 0.0
vertex 0.7 15.1 0.0
vertex 0.7 15.1 18.0
endloop
endfacet
facet normal 0.57 -0.82 0.00
outer loop
vertex -4.6 13.1 0.0
vertex -2.2 14.8 0.0
vertex -4.6 13.1 18.0
endloop
endfacet
facet normal 0.89 -0.46 0.00
outer loop
vertex -6.0 10.5 0.0
vertex -4.6 13.1 18.0
vertex -6.0 10.5 18.0
endloop
endfacet
facet normal 0.89 -0.46 0.00
outer loop
vertex -6.0 10.5 0.0
vertex -4.6 13.1 0.0
vertex -4.6 13.1 18.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex -6.0 7.5 0.0
vertex -6.0 10.5 18.0
vertex -6.0 7.5 18.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex -6.0 7.5 0.0
vertex -6.0 10.5 0.0
vertex -6.0 10.5 18.0
endloop
endfacet
facet normal 0.89 0.46 0.00
outer loop
vertex -4.6 4.9 0.0
vertex -6.0 7.5 18.0
vertex -4.6 4.9 18.0
endloop
endfacet
facet normal 0.89 0.46 -0.00
outer loop
vertex -4.6 4.9 0.0
vertex -6.0 7.5 0.0
vertex -6.0 7.5 18.0
endloop
endfacet
facet normal 0.57 0.82 0.00
outer loop
vertex -2.2 3.2 0.0
vertex -4.6 4.9 18.0
vertex -2.2 3.2 18.0
endloop
endfacet
facet normal 0.12 0.99 -0.00
outer loop
vertex -2.2 3.2 0.0
vertex -2.2 3.2 18.0
vertex 0.7 2.9 18.0
endloop
endfacet
facet normal 0.57 0.82 -0.00
outer loop
vertex -2.2 3.2 0.0
vertex -4.6 4.9 0.0
vertex -4.6 4.9 18.0
endloop
endfacet
facet normal 0.12 0.99 0.00
outer loop
vertex 0.7 2.9 0.0
vertex -2.2 3.2 0.0
vertex 0.7 2.9 18.0
endloop
endfacet
facet normal -0.35 0.94 0.00
outer loop
vertex 3.5 3.9 0.0
vertex 0.7 2.9 18.0
vertex 3.5 3.9 18.0
endloop
endfacet
facet normal -0.75 0.66 0.00
outer loop
vertex 3.5 3.9 0.0
vertex 3.5 3.9 18.0
vertex 5.4 6.1 18.0
endloop
endfacet
facet normal -0.35 0.94 0.00
outer loop
vertex 3.5 3.9 0.0
vertex 0.7 2.9 0.0
vertex 0.7 2.9 18.0
endloop
endfacet
facet normal -0.97 0.24 0.00
outer loop
vertex 5.4 6.1 0.0
vertex 5.4 6.1 18.0
vertex 6.2 9.0 18.0
endloop
endfacet
facet normal -0.75 0.66 0.00
outer loop
vertex 5.4 6.1 0.0
vertex 3.5 3.9 0.0
vertex 5.4 6.1 18.0
endloop
endfacet
facet normal -0.97 0.24 0.00
outer loop
vertex 6.2 9.0 0.0
vertex 5.4 6.1 0.0
vertex 6.2 9.0 18.0
endloop
endfacet
facet normal -0.97 -0.24 0.00
outer loop
vertex 5.4 298.9 0.0
vertex 6.2 296.0 0.0
vertex 6.2 296.0 18.0
endloop
endfacet
facet normal -0.97 -0.24 0.00
outer loop
vertex 5.4 298.9 0.0
vertex 6.2 296.0 18.0
vertex 5.4 298.9 18.0
endloop
endfacet
facet normal -0.75 -0.66 0.00
outer loop
vertex 3.5 301.1 0.0
vertex 5.4 298.9 18.0
vertex 3.5 301.1 18.0
endloop
endfacet
facet normal -0.75 -0.66 0.00
outer loop
vertex 3.5 301.1 0.0
vertex 5.4 298.9 0.0
vertex 5.4 298.9 18.0
endloop
endfacet
facet normal -0.35 -0.94 0.00
outer loop
vertex 0.7 302.1 0.0
vertex 3.5 301.1 18.0
vertex 0.7 302.1 18.0
endloop
endfacet
facet normal -0.35 -0.94 0.00
outer loop
vertex 0.7 302.1 0.0
vertex 3.5 301.1 0.0
vertex 3.5 301.1 18.0
endloop
endfacet
facet normal 0.12 -0.99 0.00
outer loop
vertex -2.2 301.8 0.0
vertex 0.7 302.1 18.0
vertex -2.2 301.8 18.0
endloop
endfacet
facet normal 0.57 -0.82 0.00
outer loop
vertex -2.2 301.8 0.0
vertex -2.2 301.8 18.0
vertex -4.6 300.1 18.0
endloop
endfacet
facet normal 0.12 -0.99 0.00
outer loop
vertex -2.2 301.8 0.0
vertex 0.7 302.1 0.0
vertex 0.7 302.1 18.0
endloop
endfacet
facet normal 0.57 -0.82 0.00
outer loop
vertex -4.6 300.1 0.0
vertex -2.2 301.8 0.0
vertex -4.6 300.1 18.0
endloop
endfacet
facet normal 0.89 -0.46 0.00
outer loop
vertex -6.0 297.5 0.0
vertex -4.6 300.1 18.0
vertex -6.0 297.5 18.0
endloop
endfacet
facet normal 0.89 -0.46 0.00
outer loop
vertex -6.0 297.5 0.0
vertex -4.6 300.1 0.0
vertex -4.6 300.1 18.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex -6.0 294.5 0.0
vertex -6.0 297.5 18.0
vertex -6.0 294.5 18.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex -6.0 294.5 0.0
vertex -6.0 297.5 0.0
vertex -6.0 297.5 18.0
endloop
endfacet
facet normal 0.89 0.46 0.00
outer loop
vertex -4.6 291.9 0.0
vertex -6.0 294.5 18.0
vertex -4.6 291.9 18.0
endloop
endfacet
facet normal 0.89 0.46 -0.00
outer loop
vertex -4.6 291.9 0.0
vertex -6.0 294.5 0.0
vertex -6.0 294.5 18.0
endloop
endfacet
facet normal 0.57 0.82 0.00
outer loop
vertex -2.2 290.2 0.0
vertex -4.6 291.9 18.0
vertex -2.2 290.2 18.0
endloop
endfacet
facet normal 0.12 0.99 -0.00
outer loop
vertex -2.2 290.2 0.0
vertex -2.2 290.2 18.0
vertex 0.7 289.9 18.0
endloop
endfacet
facet normal 0.57 0.82 -0.00
outer loop
vertex -2.2 290.2 0.0
vertex -4.6 291.9 0.0
vertex -4.6 291.9 18.0
endloop
endfacet
facet normal 0.12 0.99 0.00
outer loop
vertex 0.7 289.9 0.0
vertex -2.2 290.2 0.0
vertex 0.7 289.9 18.0
endloop
endfacet
facet normal -0.35 0.94 0.00
outer loop
vertex 3.5 290.9 0.0
vertex 0.7 289.9 18.0
vertex 3.5 290.9 18.0
endloop
endfacet
facet normal -0.75 0.66 0.00
outer loop
vertex 3.5 290.9 0.0
vertex 3.5 290.9 18.0
vertex 5.4 293.1 18.0
endloop
endfacet
facet normal -0.35 0.94 0.00
outer loop
vertex 3.5 290.9 0.0
vertex 0.7 289.9 0.0
vertex 0.7 289.9 18.0
endloop
endfacet
facet normal -0.97 0.24 0.00
outer loop
vertex 5.4 293.1 0.0
vertex 5.4 293.1 18.0
vertex 6.2 296.0 18.0
endloop
endfacet
facet normal -0.75 0.66 0.00
outer loop
vertex 5.4 293.1 0.0
vertex 3.5 290.9 0.0
vertex 5.4 293.1 18.0
endloop
endfacet
facet normal -0.97 0.24 0.00
outer loop
vertex 6.2 296.0 0.0
vertex 5.4 293.1 0.0
vertex 6.2 296.0 18.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex 5.4 11.9 40.0
vertex 20.0 18.0 40.0
vertex 3.5 14.1 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex 0.7 15.1 40.0
vertex 3.5 14.1 40.0
vertex 20.0 18.0 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex 6.2 9.0 40.0
vertex 20.0 0.0 40.0
vertex 20.0 18.0 40.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex 6.2 9.0 40.0
vertex 20.0 18.0 40.0
vertex 5.4 11.9 40.0
endloop
endfacet
facet normal -0.00 -0.00 1.00
outer loop
vertex 5.4 6.1 40.0
vertex 20.0 0.0 40.0
vertex 6.2 9.0 40.0
endloop
endfacet
facet normal -0.00 -0.00 1.00
outer loop
vertex 3.5 3.9 40.0
vertex 20.0 0.0 40.0
vertex 5.4 6.1 40.0
endloop
endfacet
facet normal -0.00 -0.00 1.00
outer loop
vertex 0.7 2.9 40.0
vertex 20.0 0.0 40.0
vertex 3.5 3.9 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex -20.0 18.0 40.0
vertex -2.2 14.8 40.0
vertex 0.7 15.1 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex -20.0 18.0 40.0
vertex -4.6 13.1 40.0
vertex -2.2 14.8 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex -20.0 18.0 40.0
vertex -6.0 10.5 40.0
vertex -4.6 13.1 40.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex -20.0 0.0 40.0
vertex -6.0 7.5 40.0
vertex -6.0 10.5 40.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex -20.0 0.0 40.0
vertex -4.6 4.9 40.0
vertex -6.0 7.5 40.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex -20.0 0.0 40.0
vertex -2.2 3.2 40.0
vertex -4.6 4.9 40.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex -20.0 0.0 40.0
vertex 0.7 2.9 40.0
vertex -2.2 3.2 40.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex -20.0 0.0 40.0
vertex -6.0 10.5 40.0
vertex -20.0 18.0 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex -20.0 18.0 40.0
vertex 0.7 15.1 40.0
vertex 20.0 18.0 40.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 20.0 0.0 40.0
vertex 0.7 2.9 40.0
vertex -20.0 0.0 40.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex 5.4 298.9 40.0
vertex 20.0 305.0 40.0
vertex 3.5 301.1 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex 0.7 302.1 40.0
vertex 3.5 301.1 40.0
vertex 20.0 305.0 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex 6.2 296.0 40.0
vertex 20.0 287.0 40.0
vertex 20.0 305.0 40.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex 6.2 296.0 40.0
vertex 20.0 305.0 40.0
vertex 5.4 298.9 40.0
endloop
endfacet
facet normal -0.00 -0.00 1.00
outer loop
vertex 5.4 293.1 40.0
vertex 20.0 287.0 40.0
vertex 6.2 296.0 40.0
endloop
endfacet
facet normal -0.00 -0.00 1.00
outer loop
vertex 3.5 290.9 40.0
vertex 20.0 287.0 40.0
vertex 5.4 293.1 40.0
endloop
endfacet
facet normal -0.00 -0.00 1.00
outer loop
vertex 0.7 289.9 40.0
vertex 20.0 287.0 40.0
vertex 3.5 290.9 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex -20.0 305.0 40.0
vertex -2.2 301.8 40.0
vertex 0.7 302.1 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex -20.0 305.0 40.0
vertex -4.6 300.1 40.0
vertex -2.2 301.8 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex -20.0 305.0 40.0
vertex -6.0 297.5 40.0
vertex -4.6 300.1 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex -20.0 305.0 40.0
vertex -6.0 294.5 40.0
vertex -6.0 297.5 40.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex -20.0 287.0 40.0
vertex -4.6 291.9 40.0
vertex -6.0 294.5 40.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex -20.0 287.0 40.0
vertex -2.2 290.2 40.0
vertex -4.6 291.9 40.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex -20.0 287.0 40.0
vertex 0.7 289.9 40.0
vertex -2.2 290.2 40.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex -20.0 287.0 40.0
vertex -6.0 294.5 40.0
vertex -20.0 305.0 40.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 20.0 287.0 40.0
vertex 0.7 289.9 40.0
vertex -20.0 287.0 40.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex -20.0 305.0 40.0
vertex 0.7 302.1 40.0
vertex 20.0 305.0 40.0
endloop
endfacet
facet normal -0.00 1.00 0.00
outer loop
vertex -20.0 18.0 40.0
vertex 20.0 18.0 40.0
vertex 20.0 18.0 38.0
endloop
endfacet
facet normal 0.00 1.00 0.00
outer loop
vertex -20.0 18.0 40.0
vertex 20.0 18.0 38.0
vertex -20.0 18.0 38.0
endloop
endfacet
facet normal 0.00 -1.00 0.00
outer loop
vertex -20.0 287.0 38.0
vertex 20.0 287.0 38.0
vertex 20.0 287.0 40.0
endloop
endfacet
facet normal 0.00 -1.00 0.00
outer loop
vertex -20.0 287.0 38.0
vertex 20.0 287.0 40.0
vertex -20.0 287.0 40.0
endloop
endfacet
facet normal -0.00 0.20 0.98
outer loop
vertex -20.0 30.3 19.5
vertex 20.0 30.3 19.5
vertex 20.0 38.0 18.0
endloop
endfacet
facet normal 0.00 0.20 0.98
outer loop
vertex -20.0 30.3 19.5
vertex 20.0 38.0 18.0
vertex -20.0 38.0 18.0
endloop
endfacet
facet normal -0.00 0.56 0.83
outer loop
vertex -20.0 23.9 23.9
vertex 20.0 23.9 23.9
vertex 20.0 30.3 19.5
endloop
endfacet
facet normal 0.00 0.83 0.56
outer loop
vertex -20.0 23.9 23.9
vertex 20.0 19.5 30.3
vertex 20.0 23.9 23.9
endloop
endfacet
facet normal 0.00 0.56 0.83
outer loop
vertex -20.0 23.9 23.9
vertex 20.0 30.3 19.5
vertex -20.0 30.3 19.5
endloop
endfacet
facet normal -0.00 0.83 0.56
outer loop
vertex -20.0 19.5 30.3
vertex 20.0 19.5 30.3
vertex -20.0 23.9 23.9
endloop
endfacet
facet normal -0.00 0.98 0.20
outer loop
vertex -20.0 18.0 38.0
vertex 20.0 18.0 38.0
vertex 20.0 19.5 30.3
endloop
endfacet
facet normal 0.00 0.98 0.20
outer loop
vertex -20.0 18.0 38.0
vertex 20.0 19.5 30.3
vertex -20.0 19.5 30.3
endloop
endfacet
facet normal 0.00 -0.98 0.20
outer loop
vertex -20.0 285.5 30.3
vertex 20.0 285.5 30.3
vertex 20.0 287.0 38.0
endloop
endfacet
facet normal 0.00 -0.98 0.20
outer loop
vertex -20.0 285.5 30.3
vertex 20.0 287.0 38.0
vertex -20.0 287.0 38.0
endloop
endfacet
facet normal 0.00 -0.83 0.56
outer loop
vertex -20.0 281.1 23.9
vertex 20.0 281.1 23.9
vertex 20.0 285.5 30.3
endloop
endfacet
facet normal 0.00 -0.56 0.83
outer loop
vertex -20.0 281.1 23.9
vertex 20.0 274.7 19.5
vertex 20.0 281.1 23.9
endloop
endfacet
facet normal 0.00 -0.83 0.56
outer loop
vertex -20.0 281.1 23.9
vertex 20.0 285.5 30.3
vertex -20.0 285.5 30.3
endloop
endfacet
facet normal 0.00 -0.56 0.83
outer loop
vertex -20.0 274.7 19.5
vertex 20.0 274.7 19.5
vertex -20.0 281.1 23.9
endloop
endfacet
facet normal 0.00 -0.20 0.98
outer loop
vertex -20.0 267.0 18.0
vertex 20.0 267.0 18.0
vertex 20.0 274.7 19.5
endloop
endfacet
facet normal 0.00 -0.20 0.98
outer loop
vertex -20.0 267.0 18.0
vertex 20.0 274.7 19.5
vertex -20.0 274.7 19.5
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex -20.0 38.0 18.0
vertex 20.0 38.0 18.0
vertex 20.0 267.0 18.0
endloop
endfacet
facet normal 0.00 -0.00 1.00
outer loop
vertex -20.0 38.0 18.0
vertex 20.0 267.0 18.0
vertex -20.0 267.0 18.0
endloop
endfacet
facet normal 0.00 -0.97 -0.24
outer loop
vertex 4.0 284.1 8.0
vertex 20.0 284.1 8.0
vertex 20.0 283.4 10.9
endloop
endfacet
facet normal 0.00 -0.75 -0.66
outer loop
vertex 4.0 283.4 10.9
vertex 20.0 283.4 10.9
vertex 20.0 281.5 13.1
endloop
endfacet
facet normal 0.00 -0.97 -0.24
outer loop
vertex 4.0 283.4 10.9
vertex 4.0 284.1 8.0
vertex 20.0 283.4 10.9
endloop
endfacet
facet normal 0.00 -0.75 -0.66
outer loop
vertex 4.0 281.5 13.1
vertex 4.0 283.4 10.9
vertex 20.0 281.5 13.1
endloop
endfacet
facet normal 0.00 -0.35 -0.94
outer loop
vertex 4.0 278.7 14.1
vertex 20.0 281.5 13.1
vertex 20.0 278.7 14.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex 4.0 278.7 14.1
vertex 20.0 278.7 14.1
vertex 20.0 275.8 13.8
endloop
endfacet
facet normal 0.00 -0.35 -0.94
outer loop
vertex 4.0 278.7 14.1
vertex 4.0 281.5 13.1
vertex 20.0 281.5 13.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex 4.0 275.8 13.8
vertex 4.0 278.7 14.1
vertex 20.0 275.8 13.8
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex 4.0 273.4 12.1
vertex 20.0 275.8 13.8
vertex 20.0 273.4 12.1
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex 4.0 273.4 12.1
vertex 4.0 275.8 13.8
vertex 20.0 275.8 13.8
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex 4.0 272.0 9.5
vertex 20.0 273.4 12.1
vertex 20.0 272.0 9.5
endloop
endfacet
facet normal -0.00 1.00 0.00
outer loop
vertex 4.0 272.0 9.5
vertex 20.0 272.0 9.5
vertex 20.0 272.0 6.5
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex 4.0 272.0 9.5
vertex 4.0 273.4 12.1
vertex 20.0 273.4 12.1
endloop
endfacet
facet normal -0.00 1.00 0.00
outer loop
vertex 4.0 272.0 6.5
vertex 4.0 272.0 9.5
vertex 20.0 272.0 6.5
endloop
endfacet
facet normal 0.00 0.89 0.46
outer loop
vertex 4.0 273.4 3.9
vertex 20.0 272.0 6.5
vertex 20.0 273.4 3.9
endloop
endfacet
facet normal -0.00 0.89 0.46
outer loop
vertex 4.0 273.4 3.9
vertex 4.0 272.0 6.5
vertex 20.0 272.0 6.5
endloop
endfacet
facet normal 0.00 0.57 0.82
outer loop
vertex 4.0 275.8 2.2
vertex 20.0 273.4 3.9
vertex 20.0 275.8 2.2
endloop
endfacet
facet normal -0.00 0.57 0.82
outer loop
vertex 4.0 275.8 2.2
vertex 4.0 273.4 3.9
vertex 20.0 273.4 3.9
endloop
endfacet
facet normal 0.00 0.12 0.99
outer loop
vertex 4.0 278.7 1.9
vertex 20.0 275.8 2.2
vertex 20.0 278.7 1.9
endloop
endfacet
facet normal -0.00 0.12 0.99
outer loop
vertex 4.0 278.7 1.9
vertex 4.0 275.8 2.2
vertex 20.0 275.8 2.2
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex 4.0 281.5 2.9
vertex 20.0 278.7 1.9
vertex 20.0 281.5 2.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex 4.0 281.5 2.9
vertex 20.0 281.5 2.9
vertex 20.0 283.4 5.1
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex 4.0 281.5 2.9
vertex 4.0 278.7 1.9
vertex 20.0 278.7 1.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex 4.0 283.4 5.1
vertex 4.0 281.5 2.9
vertex 20.0 283.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex 4.0 284.1 8.0
vertex 20.0 283.4 5.1
vertex 20.0 284.1 8.0
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex 4.0 284.1 8.0
vertex 4.0 283.4 5.1
vertex 20.0 283.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 -0.24
outer loop
vertex 4.0 200.2 8.0
vertex 20.0 200.2 8.0
vertex 20.0 199.4 10.9
endloop
endfacet
facet normal 0.00 -0.75 -0.66
outer loop
vertex 4.0 199.4 10.9
vertex 20.0 199.4 10.9
vertex 20.0 197.5 13.1
endloop
endfacet
facet normal 0.00 -0.97 -0.24
outer loop
vertex 4.0 199.4 10.9
vertex 4.0 200.2 8.0
vertex 20.0 199.4 10.9
endloop
endfacet
facet normal 0.00 -0.75 -0.66
outer loop
vertex 4.0 197.5 13.1
vertex 4.0 199.4 10.9
vertex 20.0 197.5 13.1
endloop
endfacet
facet normal 0.00 -0.35 -0.94
outer loop
vertex 4.0 194.7 14.1
vertex 20.0 197.5 13.1
vertex 20.0 194.7 14.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex 4.0 194.7 14.1
vertex 20.0 194.7 14.1
vertex 20.0 191.8 13.8
endloop
endfacet
facet normal 0.00 -0.35 -0.94
outer loop
vertex 4.0 194.7 14.1
vertex 4.0 197.5 13.1
vertex 20.0 197.5 13.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex 4.0 191.8 13.8
vertex 4.0 194.7 14.1
vertex 20.0 191.8 13.8
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex 4.0 189.4 12.1
vertex 20.0 191.8 13.8
vertex 20.0 189.4 12.1
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex 4.0 189.4 12.1
vertex 4.0 191.8 13.8
vertex 20.0 191.8 13.8
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex 4.0 188.0 9.5
vertex 20.0 189.4 12.1
vertex 20.0 188.0 9.5
endloop
endfacet
facet normal -0.00 1.00 0.00
outer loop
vertex 4.0 188.0 9.5
vertex 20.0 188.0 9.5
vertex 20.0 188.0 6.5
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex 4.0 188.0 9.5
vertex 4.0 189.4 12.1
vertex 20.0 189.4 12.1
endloop
endfacet
facet normal -0.00 1.00 0.00
outer loop
vertex 4.0 188.0 6.5
vertex 4.0 188.0 9.5
vertex 20.0 188.0 6.5
endloop
endfacet
facet normal 0.00 0.89 0.46
outer loop
vertex 4.0 189.4 3.9
vertex 20.0 188.0 6.5
vertex 20.0 189.4 3.9
endloop
endfacet
facet normal -0.00 0.89 0.46
outer loop
vertex 4.0 189.4 3.9
vertex 4.0 188.0 6.5
vertex 20.0 188.0 6.5
endloop
endfacet
facet normal 0.00 0.57 0.82
outer loop
vertex 4.0 191.8 2.2
vertex 20.0 189.4 3.9
vertex 20.0 191.8 2.2
endloop
endfacet
facet normal -0.00 0.57 0.82
outer loop
vertex 4.0 191.8 2.2
vertex 4.0 189.4 3.9
vertex 20.0 189.4 3.9
endloop
endfacet
facet normal 0.00 0.12 0.99
outer loop
vertex 4.0 194.7 1.9
vertex 20.0 191.8 2.2
vertex 20.0 194.7 1.9
endloop
endfacet
facet normal -0.00 0.12 0.99
outer loop
vertex 4.0 194.7 1.9
vertex 4.0 191.8 2.2
vertex 20.0 191.8 2.2
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex 4.0 197.5 2.9
vertex 20.0 194.7 1.9
vertex 20.0 197.5 2.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex 4.0 197.5 2.9
vertex 20.0 197.5 2.9
vertex 20.0 199.4 5.1
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex 4.0 197.5 2.9
vertex 4.0 194.7 1.9
vertex 20.0 194.7 1.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex 4.0 199.4 5.1
vertex 4.0 197.5 2.9
vertex 20.0 199.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex 4.0 200.2 8.0
vertex 20.0 199.4 5.1
vertex 20.0 200.2 8.0
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex 4.0 200.2 8.0
vertex 4.0 199.4 5.1
vertex 20.0 199.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 -0.24
outer loop
vertex 4.0 116.2 8.0
vertex 20.0 116.2 8.0
vertex 20.0 115.4 10.9
endloop
endfacet
facet normal 0.00 -0.75 -0.66
outer loop
vertex 4.0 115.4 10.9
vertex 20.0 115.4 10.9
vertex 20.0 113.5 13.1
endloop
endfacet
facet normal 0.00 -0.97 -0.24
outer loop
vertex 4.0 115.4 10.9
vertex 4.0 116.2 8.0
vertex 20.0 115.4 10.9
endloop
endfacet
facet normal 0.00 -0.75 -0.66
outer loop
vertex 4.0 113.5 13.1
vertex 4.0 115.4 10.9
vertex 20.0 113.5 13.1
endloop
endfacet
facet normal 0.00 -0.35 -0.94
outer loop
vertex 4.0 110.7 14.1
vertex 20.0 113.5 13.1
vertex 20.0 110.7 14.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex 4.0 110.7 14.1
vertex 20.0 110.7 14.1
vertex 20.0 107.8 13.8
endloop
endfacet
facet normal 0.00 -0.35 -0.94
outer loop
vertex 4.0 110.7 14.1
vertex 4.0 113.5 13.1
vertex 20.0 113.5 13.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex 4.0 107.8 13.8
vertex 4.0 110.7 14.1
vertex 20.0 107.8 13.8
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex 4.0 105.4 12.1
vertex 20.0 107.8 13.8
vertex 20.0 105.4 12.1
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex 4.0 105.4 12.1
vertex 4.0 107.8 13.8
vertex 20.0 107.8 13.8
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex 4.0 104.0 9.5
vertex 20.0 105.4 12.1
vertex 20.0 104.0 9.5
endloop
endfacet
facet normal -0.00 1.00 0.00
outer loop
vertex 4.0 104.0 9.5
vertex 20.0 104.0 9.5
vertex 20.0 104.0 6.5
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex 4.0 104.0 9.5
vertex 4.0 105.4 12.1
vertex 20.0 105.4 12.1
endloop
endfacet
facet normal -0.00 1.00 0.00
outer loop
vertex 4.0 104.0 6.5
vertex 4.0 104.0 9.5
vertex 20.0 104.0 6.5
endloop
endfacet
facet normal 0.00 0.89 0.46
outer loop
vertex 4.0 105.4 3.9
vertex 20.0 104.0 6.5
vertex 20.0 105.4 3.9
endloop
endfacet
facet normal -0.00 0.89 0.46
outer loop
vertex 4.0 105.4 3.9
vertex 4.0 104.0 6.5
vertex 20.0 104.0 6.5
endloop
endfacet
facet normal 0.00 0.57 0.82
outer loop
vertex 4.0 107.8 2.2
vertex 20.0 105.4 3.9
vertex 20.0 107.8 2.2
endloop
endfacet
facet normal -0.00 0.57 0.82
outer loop
vertex 4.0 107.8 2.2
vertex 4.0 105.4 3.9
vertex 20.0 105.4 3.9
endloop
endfacet
facet normal 0.00 0.12 0.99
outer loop
vertex 4.0 110.7 1.9
vertex 20.0 107.8 2.2
vertex 20.0 110.7 1.9
endloop
endfacet
facet normal -0.00 0.12 0.99
outer loop
vertex 4.0 110.7 1.9
vertex 4.0 107.8 2.2
vertex 20.0 107.8 2.2
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex 4.0 113.5 2.9
vertex 20.0 110.7 1.9
vertex 20.0 113.5 2.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex 4.0 113.5 2.9
vertex 20.0 113.5 2.9
vertex 20.0 115.4 5.1
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex 4.0 113.5 2.9
vertex 4.0 110.7 1.9
vertex 20.0 110.7 1.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex 4.0 115.4 5.1
vertex 4.0 113.5 2.9
vertex 20.0 115.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex 4.0 116.2 8.0
vertex 20.0 115.4 5.1
vertex 20.0 116.2 8.0
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex 4.0 116.2 8.0
vertex 4.0 115.4 5.1
vertex 20.0 115.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 -0.24
outer loop
vertex 4.0 32.1 8.0
vertex 20.0 32.1 8.0
vertex 20.0 31.4 10.9
endloop
endfacet
facet normal 0.00 -0.75 -0.66
outer loop
vertex 4.0 31.4 10.9
vertex 20.0 31.4 10.9
vertex 20.0 29.5 13.1
endloop
endfacet
facet normal 0.00 -0.97 -0.24
outer loop
vertex 4.0 31.4 10.9
vertex 4.0 32.1 8.0
vertex 20.0 31.4 10.9
endloop
endfacet
facet normal 0.00 -0.75 -0.66
outer loop
vertex 4.0 29.5 13.1
vertex 4.0 31.4 10.9
vertex 20.0 29.5 13.1
endloop
endfacet
facet normal 0.00 -0.35 -0.94
outer loop
vertex 4.0 26.7 14.1
vertex 20.0 29.5 13.1
vertex 20.0 26.7 14.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex 4.0 26.7 14.1
vertex 20.0 26.7 14.1
vertex 20.0 23.8 13.8
endloop
endfacet
facet normal 0.00 -0.35 -0.94
outer loop
vertex 4.0 26.7 14.1
vertex 4.0 29.5 13.1
vertex 20.0 29.5 13.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex 4.0 23.8 13.8
vertex 4.0 26.7 14.1
vertex 20.0 23.8 13.8
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex 4.0 21.4 12.1
vertex 20.0 23.8 13.8
vertex 20.0 21.4 12.1
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex 4.0 21.4 12.1
vertex 4.0 23.8 13.8
vertex 20.0 23.8 13.8
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex 4.0 20.0 9.5
vertex 20.0 21.4 12.1
vertex 20.0 20.0 9.5
endloop
endfacet
facet normal -0.00 1.00 0.00
outer loop
vertex 4.0 20.0 9.5
vertex 20.0 20.0 9.5
vertex 20.0 20.0 6.5
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex 4.0 20.0 9.5
vertex 4.0 21.4 12.1
vertex 20.0 21.4 12.1
endloop
endfacet
facet normal -0.00 1.00 0.00
outer loop
vertex 4.0 20.0 6.5
vertex 4.0 20.0 9.5
vertex 20.0 20.0 6.5
endloop
endfacet
facet normal 0.00 0.89 0.46
outer loop
vertex 4.0 21.4 3.9
vertex 20.0 20.0 6.5
vertex 20.0 21.4 3.9
endloop
endfacet
facet normal -0.00 0.89 0.46
outer loop
vertex 4.0 21.4 3.9
vertex 4.0 20.0 6.5
vertex 20.0 20.0 6.5
endloop
endfacet
facet normal 0.00 0.57 0.82
outer loop
vertex 4.0 23.8 2.2
vertex 20.0 21.4 3.9
vertex 20.0 23.8 2.2
endloop
endfacet
facet normal -0.00 0.57 0.82
outer loop
vertex 4.0 23.8 2.2
vertex 4.0 21.4 3.9
vertex 20.0 21.4 3.9
endloop
endfacet
facet normal 0.00 0.12 0.99
outer loop
vertex 4.0 26.7 1.9
vertex 20.0 23.8 2.2
vertex 20.0 26.7 1.9
endloop
endfacet
facet normal -0.00 0.12 0.99
outer loop
vertex 4.0 26.7 1.9
vertex 4.0 23.8 2.2
vertex 20.0 23.8 2.2
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex 4.0 29.5 2.9
vertex 20.0 26.7 1.9
vertex 20.0 29.5 2.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex 4.0 29.5 2.9
vertex 20.0 29.5 2.9
vertex 20.0 31.4 5.1
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex 4.0 29.5 2.9
vertex 4.0 26.7 1.9
vertex 20.0 26.7 1.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex 4.0 31.4 5.1
vertex 4.0 29.5 2.9
vertex 20.0 31.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex 4.0 32.1 8.0
vertex 20.0 31.4 5.1
vertex 20.0 32.1 8.0
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex 4.0 32.1 8.0
vertex 4.0 31.4 5.1
vertex 20.0 31.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 -0.24
outer loop
vertex -4.0 284.1 8.0
vertex -20.0 283.4 10.9
vertex -20.0 284.1 8.0
endloop
endfacet
facet normal 0.00 -0.75 -0.66
outer loop
vertex -4.0 283.4 10.9
vertex -20.0 281.5 13.1
vertex -20.0 283.4 10.9
endloop
endfacet
facet normal -0.00 -0.97 -0.24
outer loop
vertex -4.0 283.4 10.9
vertex -20.0 283.4 10.9
vertex -4.0 284.1 8.0
endloop
endfacet
facet normal -0.00 -0.75 -0.66
outer loop
vertex -4.0 281.5 13.1
vertex -20.0 281.5 13.1
vertex -4.0 283.4 10.9
endloop
endfacet
facet normal -0.00 -0.35 -0.94
outer loop
vertex -4.0 278.7 14.1
vertex -20.0 278.7 14.1
vertex -20.0 281.5 13.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex -4.0 278.7 14.1
vertex -20.0 275.8 13.8
vertex -20.0 278.7 14.1
endloop
endfacet
facet normal 0.00 -0.35 -0.94
outer loop
vertex -4.0 278.7 14.1
vertex -20.0 281.5 13.1
vertex -4.0 281.5 13.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex -4.0 275.8 13.8
vertex -20.0 275.8 13.8
vertex -4.0 278.7 14.1
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex -4.0 273.4 12.1
vertex -20.0 273.4 12.1
vertex -20.0 275.8 13.8
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex -4.0 273.4 12.1
vertex -20.0 275.8 13.8
vertex -4.0 275.8 13.8
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex -4.0 272.0 9.5
vertex -20.0 272.0 9.5
vertex -20.0 273.4 12.1
endloop
endfacet
facet normal 0.00 1.00 -0.00
outer loop
vertex -4.0 272.0 9.5
vertex -20.0 272.0 6.5
vertex -20.0 272.0 9.5
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex -4.0 272.0 9.5
vertex -20.0 273.4 12.1
vertex -4.0 273.4 12.1
endloop
endfacet
facet normal 0.00 1.00 -0.00
outer loop
vertex -4.0 272.0 6.5
vertex -20.0 272.0 6.5
vertex -4.0 272.0 9.5
endloop
endfacet
facet normal 0.00 0.89 0.46
outer loop
vertex -4.0 273.4 3.9
vertex -20.0 273.4 3.9
vertex -20.0 272.0 6.5
endloop
endfacet
facet normal -0.00 0.89 0.46
outer loop
vertex -4.0 273.4 3.9
vertex -20.0 272.0 6.5
vertex -4.0 272.0 6.5
endloop
endfacet
facet normal 0.00 0.57 0.82
outer loop
vertex -4.0 275.8 2.2
vertex -20.0 275.8 2.2
vertex -20.0 273.4 3.9
endloop
endfacet
facet normal -0.00 0.57 0.82
outer loop
vertex -4.0 275.8 2.2
vertex -20.0 273.4 3.9
vertex -4.0 273.4 3.9
endloop
endfacet
facet normal 0.00 0.12 0.99
outer loop
vertex -4.0 278.7 1.9
vertex -20.0 278.7 1.9
vertex -20.0 275.8 2.2
endloop
endfacet
facet normal -0.00 0.12 0.99
outer loop
vertex -4.0 278.7 1.9
vertex -20.0 275.8 2.2
vertex -4.0 275.8 2.2
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex -4.0 281.5 2.9
vertex -20.0 281.5 2.9
vertex -20.0 278.7 1.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex -4.0 281.5 2.9
vertex -20.0 283.4 5.1
vertex -20.0 281.5 2.9
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex -4.0 281.5 2.9
vertex -20.0 278.7 1.9
vertex -4.0 278.7 1.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex -4.0 283.4 5.1
vertex -20.0 283.4 5.1
vertex -4.0 281.5 2.9
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex -4.0 284.1 8.0
vertex -20.0 284.1 8.0
vertex -20.0 283.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex -4.0 284.1 8.0
vertex -20.0 283.4 5.1
vertex -4.0 283.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 -0.24
outer loop
vertex -4.0 200.2 8.0
vertex -20.0 199.4 10.9
vertex -20.0 200.2 8.0
endloop
endfacet
facet normal 0.00 -0.75 -0.66
outer loop
vertex -4.0 199.4 10.9
vertex -20.0 197.5 13.1
vertex -20.0 199.4 10.9
endloop
endfacet
facet normal -0.00 -0.97 -0.24
outer loop
vertex -4.0 199.4 10.9
vertex -20.0 199.4 10.9
vertex -4.0 200.2 8.0
endloop
endfacet
facet normal -0.00 -0.75 -0.66
outer loop
vertex -4.0 197.5 13.1
vertex -20.0 197.5 13.1
vertex -4.0 199.4 10.9
endloop
endfacet
facet normal -0.00 -0.35 -0.94
outer loop
vertex -4.0 194.7 14.1
vertex -20.0 194.7 14.1
vertex -20.0 197.5 13.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex -4.0 194.7 14.1
vertex -20.0 191.8 13.8
vertex -20.0 194.7 14.1
endloop
endfacet
facet normal 0.00 -0.35 -0.94
outer loop
vertex -4.0 194.7 14.1
vertex -20.0 197.5 13.1
vertex -4.0 197.5 13.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex -4.0 191.8 13.8
vertex -20.0 191.8 13.8
vertex -4.0 194.7 14.1
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex -4.0 189.4 12.1
vertex -20.0 189.4 12.1
vertex -20.0 191.8 13.8
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex -4.0 189.4 12.1
vertex -20.0 191.8 13.8
vertex -4.0 191.8 13.8
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex -4.0 188.0 9.5
vertex -20.0 188.0 9.5
vertex -20.0 189.4 12.1
endloop
endfacet
facet normal 0.00 1.00 -0.00
outer loop
vertex -4.0 188.0 9.5
vertex -20.0 188.0 6.5
vertex -20.0 188.0 9.5
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex -4.0 188.0 9.5
vertex -20.0 189.4 12.1
vertex -4.0 189.4 12.1
endloop
endfacet
facet normal 0.00 1.00 -0.00
outer loop
vertex -4.0 188.0 6.5
vertex -20.0 188.0 6.5
vertex -4.0 188.0 9.5
endloop
endfacet
facet normal 0.00 0.89 0.46
outer loop
vertex -4.0 189.4 3.9
vertex -20.0 189.4 3.9
vertex -20.0 188.0 6.5
endloop
endfacet
facet normal -0.00 0.89 0.46
outer loop
vertex -4.0 189.4 3.9
vertex -20.0 188.0 6.5
vertex -4.0 188.0 6.5
endloop
endfacet
facet normal 0.00 0.57 0.82
outer loop
vertex -4.0 191.8 2.2
vertex -20.0 191.8 2.2
vertex -20.0 189.4 3.9
endloop
endfacet
facet normal -0.00 0.57 0.82
outer loop
vertex -4.0 191.8 2.2
vertex -20.0 189.4 3.9
vertex -4.0 189.4 3.9
endloop
endfacet
facet normal 0.00 0.12 0.99
outer loop
vertex -4.0 194.7 1.9
vertex -20.0 194.7 1.9
vertex -20.0 191.8 2.2
endloop
endfacet
facet normal -0.00 0.12 0.99
outer loop
vertex -4.0 194.7 1.9
vertex -20.0 191.8 2.2
vertex -4.0 191.8 2.2
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex -4.0 197.5 2.9
vertex -20.0 197.5 2.9
vertex -20.0 194.7 1.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex -4.0 197.5 2.9
vertex -20.0 199.4 5.1
vertex -20.0 197.5 2.9
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex -4.0 197.5 2.9
vertex -20.0 194.7 1.9
vertex -4.0 194.7 1.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex -4.0 199.4 5.1
vertex -20.0 199.4 5.1
vertex -4.0 197.5 2.9
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex -4.0 200.2 8.0
vertex -20.0 200.2 8.0
vertex -20.0 199.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex -4.0 200.2 8.0
vertex -20.0 199.4 5.1
vertex -4.0 199.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 -0.24
outer loop
vertex -4.0 116.2 8.0
vertex -20.0 115.4 10.9
vertex -20.0 116.2 8.0
endloop
endfacet
facet normal 0.00 -0.75 -0.66
outer loop
vertex -4.0 115.4 10.9
vertex -20.0 113.5 13.1
vertex -20.0 115.4 10.9
endloop
endfacet
facet normal -0.00 -0.97 -0.24
outer loop
vertex -4.0 115.4 10.9
vertex -20.0 115.4 10.9
vertex -4.0 116.2 8.0
endloop
endfacet
facet normal -0.00 -0.75 -0.66
outer loop
vertex -4.0 113.5 13.1
vertex -20.0 113.5 13.1
vertex -4.0 115.4 10.9
endloop
endfacet
facet normal -0.00 -0.35 -0.94
outer loop
vertex -4.0 110.7 14.1
vertex -20.0 110.7 14.1
vertex -20.0 113.5 13.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex -4.0 110.7 14.1
vertex -20.0 107.8 13.8
vertex -20.0 110.7 14.1
endloop
endfacet
facet normal 0.00 -0.35 -0.94
outer loop
vertex -4.0 110.7 14.1
vertex -20.0 113.5 13.1
vertex -4.0 113.5 13.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex -4.0 107.8 13.8
vertex -20.0 107.8 13.8
vertex -4.0 110.7 14.1
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex -4.0 105.4 12.1
vertex -20.0 105.4 12.1
vertex -20.0 107.8 13.8
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex -4.0 105.4 12.1
vertex -20.0 107.8 13.8
vertex -4.0 107.8 13.8
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex -4.0 104.0 9.5
vertex -20.0 104.0 9.5
vertex -20.0 105.4 12.1
endloop
endfacet
facet normal 0.00 1.00 -0.00
outer loop
vertex -4.0 104.0 9.5
vertex -20.0 104.0 6.5
vertex -20.0 104.0 9.5
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex -4.0 104.0 9.5
vertex -20.0 105.4 12.1
vertex -4.0 105.4 12.1
endloop
endfacet
facet normal 0.00 1.00 -0.00
outer loop
vertex -4.0 104.0 6.5
vertex -20.0 104.0 6.5
vertex -4.0 104.0 9.5
endloop
endfacet
facet normal 0.00 0.89 0.46
outer loop
vertex -4.0 105.4 3.9
vertex -20.0 105.4 3.9
vertex -20.0 104.0 6.5
endloop
endfacet
facet normal -0.00 0.89 0.46
outer loop
vertex -4.0 105.4 3.9
vertex -20.0 104.0 6.5
vertex -4.0 104.0 6.5
endloop
endfacet
facet normal 0.00 0.57 0.82
outer loop
vertex -4.0 107.8 2.2
vertex -20.0 107.8 2.2
vertex -20.0 105.4 3.9
endloop
endfacet
facet normal -0.00 0.57 0.82
outer loop
vertex -4.0 107.8 2.2
vertex -20.0 105.4 3.9
vertex -4.0 105.4 3.9
endloop
endfacet
facet normal 0.00 0.12 0.99
outer loop
vertex -4.0 110.7 1.9
vertex -20.0 110.7 1.9
vertex -20.0 107.8 2.2
endloop
endfacet
facet normal -0.00 0.12 0.99
outer loop
vertex -4.0 110.7 1.9
vertex -20.0 107.8 2.2
vertex -4.0 107.8 2.2
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex -4.0 113.5 2.9
vertex -20.0 113.5 2.9
vertex -20.0 110.7 1.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex -4.0 113.5 2.9
vertex -20.0 115.4 5.1
vertex -20.0 113.5 2.9
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex -4.0 113.5 2.9
vertex -20.0 110.7 1.9
vertex -4.0 110.7 1.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex -4.0 115.4 5.1
vertex -20.0 115.4 5.1
vertex -4.0 113.5 2.9
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex -4.0 116.2 8.0
vertex -20.0 116.2 8.0
vertex -20.0 115.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex -4.0 116.2 8.0
vertex -20.0 115.4 5.1
vertex -4.0 115.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 -0.24
outer loop
vertex -4.0 32.1 8.0
vertex -20.0 31.4 10.9
vertex -20.0 32.1 8.0
endloop
endfacet
facet normal 0.00 -0.75 -0.66
outer loop
vertex -4.0 31.4 10.9
vertex -20.0 29.5 13.1
vertex -20.0 31.4 10.9
endloop
endfacet
facet normal -0.00 -0.97 -0.24
outer loop
vertex -4.0 31.4 10.9
vertex -20.0 31.4 10.9
vertex -4.0 32.1 8.0
endloop
endfacet
facet normal -0.00 -0.75 -0.66
outer loop
vertex -4.0 29.5 13.1
vertex -20.0 29.5 13.1
vertex -4.0 31.4 10.9
endloop
endfacet
facet normal -0.00 -0.35 -0.94
outer loop
vertex -4.0 26.7 14.1
vertex -20.0 26.7 14.1
vertex -20.0 29.5 13.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex -4.0 26.7 14.1
vertex -20.0 23.8 13.8
vertex -20.0 26.7 14.1
endloop
endfacet
facet normal 0.00 -0.35 -0.94
outer loop
vertex -4.0 26.7 14.1
vertex -20.0 29.5 13.1
vertex -4.0 29.5 13.1
endloop
endfacet
facet normal 0.00 0.12 -0.99
outer loop
vertex -4.0 23.8 13.8
vertex -20.0 23.8 13.8
vertex -4.0 26.7 14.1
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex -4.0 21.4 12.1
vertex -20.0 21.4 12.1
vertex -20.0 23.8 13.8
endloop
endfacet
facet normal 0.00 0.57 -0.82
outer loop
vertex -4.0 21.4 12.1
vertex -20.0 23.8 13.8
vertex -4.0 23.8 13.8
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex -4.0 20.0 9.5
vertex -20.0 20.0 9.5
vertex -20.0 21.4 12.1
endloop
endfacet
facet normal 0.00 1.00 -0.00
outer loop
vertex -4.0 20.0 9.5
vertex -20.0 20.0 6.5
vertex -20.0 20.0 9.5
endloop
endfacet
facet normal 0.00 0.89 -0.46
outer loop
vertex -4.0 20.0 9.5
vertex -20.0 21.4 12.1
vertex -4.0 21.4 12.1
endloop
endfacet
facet normal 0.00 1.00 -0.00
outer loop
vertex -4.0 20.0 6.5
vertex -20.0 20.0 6.5
vertex -4.0 20.0 9.5
endloop
endfacet
facet normal 0.00 0.89 0.46
outer loop
vertex -4.0 21.4 3.9
vertex -20.0 21.4 3.9
vertex -20.0 20.0 6.5
endloop
endfacet
facet normal -0.00 0.89 0.46
outer loop
vertex -4.0 21.4 3.9
vertex -20.0 20.0 6.5
vertex -4.0 20.0 6.5
endloop
endfacet
facet normal 0.00 0.57 0.82
outer loop
vertex -4.0 23.8 2.2
vertex -20.0 23.8 2.2
vertex -20.0 21.4 3.9
endloop
endfacet
facet normal -0.00 0.57 0.82
outer loop
vertex -4.0 23.8 2.2
vertex -20.0 21.4 3.9
vertex -4.0 21.4 3.9
endloop
endfacet
facet normal 0.00 0.12 0.99
outer loop
vertex -4.0 26.7 1.9
vertex -20.0 26.7 1.9
vertex -20.0 23.8 2.2
endloop
endfacet
facet normal -0.00 0.12 0.99
outer loop
vertex -4.0 26.7 1.9
vertex -20.0 23.8 2.2
vertex -4.0 23.8 2.2
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex -4.0 29.5 2.9
vertex -20.0 29.5 2.9
vertex -20.0 26.7 1.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex -4.0 29.5 2.9
vertex -20.0 31.4 5.1
vertex -20.0 29.5 2.9
endloop
endfacet
facet normal 0.00 -0.35 0.94
outer loop
vertex -4.0 29.5 2.9
vertex -20.0 26.7 1.9
vertex -4.0 26.7 1.9
endloop
endfacet
facet normal 0.00 -0.75 0.66
outer loop
vertex -4.0 31.4 5.1
vertex -20.0 31.4 5.1
vertex -4.0 29.5 2.9
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex -4.0 32.1 8.0
vertex -20.0 32.1 8.0
vertex -20.0 31.4 5.1
endloop
endfacet
facet normal 0.00 -0.97 0.24
outer loop
vertex -4.0 32.1 8.0
vertex -20.0 31.4 5.1
vertex -4.0 31.4 5.1
endloop
endfacet
facet normal 0.00 0.00 -1.00
outer loop
vertex 3.5 3.9 18.0
vertex -6.0 7.5 18.0
vertex -6.0 10.5 18.0
endloop
endfacet
facet normal 0.00 0.00 -1.00
outer loop
vertex 3.5 3.9 18.0
vertex -4.6 4.9 18.0
vertex -6.0 7.5 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 3.5 3.9 18.0
vertex -2.2 3.2 18.0
vertex -4.6 4.9 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 3.5 3.9 18.0
vertex 0.7 2.9 18.0
vertex -2.2 3.2 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 0.7 15.1 18.0
vertex -4.6 13.1 18.0
vertex -2.2 14.8 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 0.7 15.1 18.0
vertex -6.0 10.5 18.0
vertex -4.6 13.1 18.0
endloop
endfacet
facet normal 0.00 0.00 -1.00
outer loop
vertex 5.4 11.9 18.0
vertex 5.4 6.1 18.0
vertex 3.5 3.9 18.0
endloop
endfacet
facet normal 0.00 -0.00 -1.00
outer loop
vertex 5.4 11.9 18.0
vertex 6.2 9.0 18.0
vertex 5.4 6.1 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 5.4 11.9 18.0
vertex 3.5 3.9 18.0
vertex -6.0 10.5 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 5.4 11.9 18.0
vertex -6.0 10.5 18.0
vertex 0.7 15.1 18.0
endloop
endfacet
facet normal -0.00 -0.00 -1.00
outer loop
vertex 3.5 14.1 18.0
vertex 5.4 11.9 18.0
vertex 0.7 15.1 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 3.5 290.9 18.0
vertex -2.2 290.2 18.0
vertex -4.6 291.9 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 3.5 290.9 18.0
vertex 0.7 289.9 18.0
vertex -2.2 290.2 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 5.4 293.1 18.0
vertex -4.6 291.9 18.0
vertex -6.0 294.5 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 5.4 293.1 18.0
vertex 3.5 290.9 18.0
vertex -4.6 291.9 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 6.2 296.0 18.0
vertex -6.0 294.5 18.0
vertex -6.0 297.5 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 6.2 296.0 18.0
vertex 5.4 293.1 18.0
vertex -6.0 294.5 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 5.4 298.9 18.0
vertex -6.0 297.5 18.0
vertex -4.6 300.1 18.0
endloop
endfacet
facet normal -0.00 -0.00 -1.00
outer loop
vertex 5.4 298.9 18.0
vertex 6.2 296.0 18.0
vertex -6.0 297.5 18.0
endloop
endfacet
facet normal 0.00 0.00 -1.00
outer loop
vertex 3.5 301.1 18.0
vertex -2.2 301.8 18.0
vertex 0.7 302.1 18.0
endloop
endfacet
facet normal -0.00 0.00 -1.00
outer loop
vertex 3.5 301.1 18.0
vertex -4.6 300.1 18.0
vertex -2.2 301.8 18.0
endloop
endfacet
facet normal -0.00 -0.00 -1.00
outer loop
vertex 3.5 301.1 18.0
vertex 5.4 298.9 18.0
vertex -4.6 300.1 18.0
endloop
endfacet
facet normal -0.97 -0.24 0.00
outer loop
vertex 5.4 11.9 22.0
vertex 6.2 9.0 22.0
vertex 6.2 9.0 40.0
endloop
endfacet
facet normal -0.97 -0.24 0.00
outer loop
vertex 5.4 11.9 22.0
vertex 6.2 9.0 40.0
vertex 5.4 11.9 40.0
endloop
endfacet
facet normal -0.75 -0.66 0.00
outer loop
vertex 5.4 11.9 22.0
vertex 5.4 11.9 40.0
vertex 3.5 14.1 40.0
endloop
endfacet
facet normal -0.35 -0.94 0.00
outer loop
vertex 3.5 14.1 22.0
vertex 3.5 14.1 40.0
vertex 0.7 15.1 40.0
endloop
endfacet
facet normal -0.75 -0.66 0.00
outer loop
vertex 3.5 14.1 22.0
vertex 5.4 11.9 22.0
vertex 3.5 14.1 40.0
endloop
endfacet
facet normal 0.12 -0.99 0.00
outer loop
vertex 0.7 15.1 22.0
vertex 0.7 15.1 40.0
vertex -2.2 14.8 40.0
endloop
endfacet
facet normal -0.35 -0.94 0.00
outer loop
vertex 0.7 15.1 22.0
vertex 3.5 14.1 22.0
vertex 0.7 15.1 40.0
endloop
endfacet
facet normal 0.12 -0.99 0.00
outer loop
vertex -2.2 14.8 22.0
vertex 0.7 15.1 22.0
vertex -2.2 14.8 40.0
endloop
endfacet
facet normal 0.57 -0.82 0.00
outer loop
vertex -4.6 13.1 22.0
vertex -2.2 14.8 40.0
vertex -4.6 13.1 40.0
endloop
endfacet
facet normal 0.57 -0.82 0.00
outer loop
vertex -4.6 13.1 22.0
vertex -2.2 14.8 22.0
vertex -2.2 14.8 40.0
endloop
endfacet
facet normal 0.89 -0.46 0.00
outer loop
vertex -6.0 10.5 22.0
vertex -4.6 13.1 40.0
vertex -6.0 10.5 40.0
endloop
endfacet
facet normal 0.89 -0.46 0.00
outer loop
vertex -6.0 10.5 22.0
vertex -4.6 13.1 22.0
vertex -4.6 13.1 40.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex -6.0 7.5 22.0
vertex -6.0 10.5 40.0
vertex -6.0 7.5 40.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex -6.0 7.5 22.0
vertex -6.0 10.5 22.0
vertex -6.0 10.5 40.0
endloop
endfacet
facet normal 0.89 0.46 0.00
outer loop
vertex -4.6 4.9 22.0
vertex -6.0 7.5 40.0
vertex -4.6 4.9 40.0
endloop
endfacet
facet normal 0.89 0.46 -0.00
outer loop
vertex -4.6 4.9 22.0
vertex -6.0 7.5 22.0
vertex -6.0 7.5 40.0
endloop
endfacet
facet normal 0.57 0.82 0.00
outer loop
vertex -2.2 3.2 22.0
vertex -4.6 4.9 40.0
vertex -2.2 3.2 40.0
endloop
endfacet
facet normal 0.57 0.82 -0.00
outer loop
vertex -2.2 3.2 22.0
vertex -4.6 4.9 22.0
vertex -4.6 4.9 40.0
endloop
endfacet
facet normal 0.12 0.99 0.00
outer loop
vertex 0.7 2.9 22.0
vertex -2.2 3.2 40.0
vertex 0.7 2.9 40.0
endloop
endfacet
facet normal -0.35 0.94 0.00
outer loop
vertex 0.7 2.9 22.0
vertex 0.7 2.9 40.0
vertex 3.5 3.9 40.0
endloop
endfacet
facet normal 0.12 0.99 -0.00
outer loop
vertex 0.7 2.9 22.0
vertex -2.2 3.2 22.0
vertex -2.2 3.2 40.0
endloop
endfacet
facet normal -0.35 0.94 0.00
outer loop
vertex 3.5 3.9 22.0
vertex 0.7 2.9 22.0
vertex 3.5 3.9 40.0
endloop
endfacet
facet normal -0.75 0.66 0.00
outer loop
vertex 5.4 6.1 22.0
vertex 3.5 3.9 40.0
vertex 5.4 6.1 40.0
endloop
endfacet
facet normal -0.75 0.66 0.00
outer loop
vertex 5.4 6.1 22.0
vertex 3.5 3.9 22.0
vertex 3.5 3.9 40.0
endloop
endfacet
facet normal -0.97 0.24 0.00
outer loop
vertex 6.2 9.0 22.0
vertex 5.4 6.1 40.0
vertex 6.2 9.0 40.0
endloop
endfacet
facet normal -0.97 0.24 0.00
outer loop
vertex 6.2 9.0 22.0
vertex 5.4 6.1 22.0
vertex 5.4 6.1 40.0
endloop
endfacet
facet normal -0.97 -0.24 0.00
outer loop
vertex 5.4 298.9 22.0
vertex 6.2 296.0 22.0
vertex 6.2 296.0 40.0
endloop
endfacet
facet normal -0.97 -0.24 0.00
outer loop
vertex 5.4 298.9 22.0
vertex 6.2 296.0 40.0
vertex 5.4 298.9 40.0
endloop
endfacet
facet normal -0.75 -0.66 0.00
outer loop
vertex 5.4 298.9 22.0
vertex 5.4 298.9 40.0
vertex 3.5 301.1 40.0
endloop
endfacet
facet normal -0.35 -0.94 0.00
outer loop
vertex 3.5 301.1 22.0
vertex 3.5 301.1 40.0
vertex 0.7 302.1 40.0
endloop
endfacet
facet normal -0.75 -0.66 0.00
outer loop
vertex 3.5 301.1 22.0
vertex 5.4 298.9 22.0
vertex 3.5 301.1 40.0
endloop
endfacet
facet normal 0.12 -0.99 0.00
outer loop
vertex 0.7 302.1 22.0
vertex 0.7 302.1 40.0
vertex -2.2 301.8 40.0
endloop
endfacet
facet normal -0.35 -0.94 0.00
outer loop
vertex 0.7 302.1 22.0
vertex 3.5 301.1 22.0
vertex 0.7 302.1 40.0
endloop
endfacet
facet normal 0.12 -0.99 0.00
outer loop
vertex -2.2 301.8 22.0
vertex 0.7 302.1 22.0
vertex -2.2 301.8 40.0
endloop
endfacet
facet normal 0.57 -0.82 0.00
outer loop
vertex -4.6 300.1 22.0
vertex -2.2 301.8 40.0
vertex -4.6 300.1 40.0
endloop
endfacet
facet normal 0.57 -0.82 0.00
outer loop
vertex -4.6 300.1 22.0
vertex -2.2 301.8 22.0
vertex -2.2 301.8 40.0
endloop
endfacet
facet normal 0.89 -0.46 0.00
outer loop
vertex -6.0 297.5 22.0
vertex -4.6 300.1 40.0
vertex -6.0 297.5 40.0
endloop
endfacet
facet normal 0.89 -0.46 0.00
outer loop
vertex -6.0 297.5 22.0
vertex -4.6 300.1 22.0
vertex -4.6 300.1 40.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex -6.0 294.5 22.0
vertex -6.0 297.5 40.0
vertex -6.0 294.5 40.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex -6.0 294.5 22.0
vertex -6.0 297.5 22.0
vertex -6.0 297.5 40.0
endloop
endfacet
facet normal 0.89 0.46 0.00
outer loop
vertex -4.6 291.9 22.0
vertex -6.0 294.5 40.0
vertex -4.6 291.9 40.0
endloop
endfacet
facet normal 0.89 0.46 -0.00
outer loop
vertex -4.6 291.9 22.0
vertex -6.0 294.5 22.0
vertex -6.0 294.5 40.0
endloop
endfacet
facet normal 0.57 0.82 0.00
outer loop
vertex -2.2 290.2 22.0
vertex -4.6 291.9 40.0
vertex -2.2 290.2 40.0
endloop
endfacet
facet normal 0.57 0.82 -0.00
outer loop
vertex -2.2 290.2 22.0
vertex -4.6 291.9 22.0
vertex -4.6 291.9 40.0
endloop
endfacet
facet normal 0.12 0.99 0.00
outer loop
vertex 0.7 289.9 22.0
vertex -2.2 290.2 40.0
vertex 0.7 289.9 40.0
endloop
endfacet
facet normal -0.35 0.94 0.00
outer loop
vertex 0.7 289.9 22.0
vertex 0.7 289.9 40.0
vertex 3.5 290.9 40.0
endloop
endfacet
facet normal 0.12 0.99 -0.00
outer loop
vertex 0.7 289.9 22.0
vertex -2.2 290.2 22.0
vertex -2.2 290.2 40.0
endloop
endfacet
facet normal -0.35 0.94 0.00
outer loop
vertex 3.5 290.9 22.0
vertex 0.7 289.9 22.0
vertex 3.5 290.9 40.0
endloop
endfacet
facet normal -0.75 0.66 0.00
outer loop
vertex 5.4 293.1 22.0
vertex 3.5 290.9 40.0
vertex 5.4 293.1 40.0
endloop
endfacet
facet normal -0.75 0.66 0.00
outer loop
vertex 5.4 293.1 22.0
vertex 3.5 290.9 22.0
vertex 3.5 290.9 40.0
endloop
endfacet
facet normal -0.97 0.24 0.00
outer loop
vertex 6.2 296.0 22.0
vertex 5.4 293.1 40.0
vertex 6.2 296.0 40.0
endloop
endfacet
facet normal -0.97 0.24 0.00
outer loop
vertex 6.2 296.0 22.0
vertex 5.4 293.1 22.0
vertex 5.4 293.1 40.0
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 283.4 10.9
vertex 4.0 283.4 5.1
vertex 4.0 284.1 8.0
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 4.0 273.4 3.9
vertex 4.0 275.8 2.2
vertex 4.0 278.7 1.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 273.4 3.9
vertex 4.0 278.7 1.9
vertex 4.0 281.5 2.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 273.4 3.9
vertex 4.0 281.5 2.9
vertex 4.0 283.4 5.1
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 4.0 278.7 14.1
vertex 4.0 283.4 10.9
vertex 4.0 281.5 13.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 278.7 14.1
vertex 4.0 283.4 5.1
vertex 4.0 283.4 10.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 278.7 14.1
vertex 4.0 273.4 3.9
vertex 4.0 283.4 5.1
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 4.0 272.0 9.5
vertex 4.0 272.0 6.5
vertex 4.0 273.4 3.9
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 4.0 273.4 12.1
vertex 4.0 278.7 14.1
vertex 4.0 275.8 13.8
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 273.4 12.1
vertex 4.0 273.4 3.9
vertex 4.0 278.7 14.1
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 4.0 273.4 12.1
vertex 4.0 272.0 9.5
vertex 4.0 273.4 3.9
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 4.0 189.4 3.9
vertex 4.0 191.8 2.2
vertex 4.0 194.7 1.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 189.4 3.9
vertex 4.0 194.7 1.9
vertex 4.0 197.5 2.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 189.4 3.9
vertex 4.0 197.5 2.9
vertex 4.0 199.4 5.1
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 4.0 197.5 13.1
vertex 4.0 200.2 8.0
vertex 4.0 199.4 10.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 197.5 13.1
vertex 4.0 199.4 5.1
vertex 4.0 200.2 8.0
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 4.0 188.0 9.5
vertex 4.0 188.0 6.5
vertex 4.0 189.4 3.9
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 4.0 188.0 9.5
vertex 4.0 199.4 5.1
vertex 4.0 197.5 13.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 188.0 9.5
vertex 4.0 189.4 3.9
vertex 4.0 199.4 5.1
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 4.0 189.4 12.1
vertex 4.0 197.5 13.1
vertex 4.0 194.7 14.1
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 4.0 189.4 12.1
vertex 4.0 194.7 14.1
vertex 4.0 191.8 13.8
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 189.4 12.1
vertex 4.0 188.0 9.5
vertex 4.0 197.5 13.1
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 4.0 105.4 3.9
vertex 4.0 107.8 2.2
vertex 4.0 110.7 1.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 105.4 3.9
vertex 4.0 110.7 1.9
vertex 4.0 113.5 2.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 105.4 3.9
vertex 4.0 113.5 2.9
vertex 4.0 115.4 5.1
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 4.0 113.5 13.1
vertex 4.0 116.2 8.0
vertex 4.0 115.4 10.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 113.5 13.1
vertex 4.0 115.4 5.1
vertex 4.0 116.2 8.0
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 4.0 104.0 9.5
vertex 4.0 104.0 6.5
vertex 4.0 105.4 3.9
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 4.0 104.0 9.5
vertex 4.0 115.4 5.1
vertex 4.0 113.5 13.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 104.0 9.5
vertex 4.0 105.4 3.9
vertex 4.0 115.4 5.1
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 4.0 105.4 12.1
vertex 4.0 113.5 13.1
vertex 4.0 110.7 14.1
endloop
endfacet
facet normal 1.00 0.00 -0.00
outer loop
vertex 4.0 105.4 12.1
vertex 4.0 110.7 14.1
vertex 4.0 107.8 13.8
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 105.4 12.1
vertex 4.0 104.0 9.5
vertex 4.0 113.5 13.1
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 4.0 26.7 14.1
vertex 4.0 31.4 10.9
vertex 4.0 29.5 13.1
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 4.0 20.0 9.5
vertex 4.0 20.0 6.5
vertex 4.0 21.4 3.9
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 4.0 20.0 9.5
vertex 4.0 21.4 3.9
vertex 4.0 23.8 2.2
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 4.0 23.8 13.8
vertex 4.0 32.1 8.0
vertex 4.0 31.4 10.9
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 4.0 23.8 13.8
vertex 4.0 23.8 2.2
vertex 4.0 26.7 1.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 23.8 13.8
vertex 4.0 26.7 1.9
vertex 4.0 29.5 2.9
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 23.8 13.8
vertex 4.0 29.5 2.9
vertex 4.0 31.4 5.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 23.8 13.8
vertex 4.0 31.4 5.1
vertex 4.0 32.1 8.0
endloop
endfacet
facet normal 1.00 0.00 0.00
outer loop
vertex 4.0 23.8 13.8
vertex 4.0 20.0 9.5
vertex 4.0 23.8 2.2
endloop
endfacet
facet normal 1.00 -0.00 -0.00
outer loop
vertex 4.0 23.8 13.8
vertex 4.0 31.4 10.9
vertex 4.0 26.7 14.1
endloop
endfacet
facet normal 1.00 -0.00 0.00
outer loop
vertex 4.0 21.4 12.1
vertex 4.0 20.0 9.5
vertex 4.0 23.8 13.8
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 283.4 10.9
vertex -4.0 284.1 8.0
vertex -4.0 283.4 5.1
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -4.0 273.4 3.9
vertex -4.0 278.7 1.9
vertex -4.0 275.8 2.2
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 273.4 3.9
vertex -4.0 281.5 2.9
vertex -4.0 278.7 1.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 273.4 3.9
vertex -4.0 283.4 5.1
vertex -4.0 281.5 2.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 278.7 14.1
vertex -4.0 281.5 13.1
vertex -4.0 283.4 10.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 278.7 14.1
vertex -4.0 283.4 10.9
vertex -4.0 283.4 5.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 278.7 14.1
vertex -4.0 283.4 5.1
vertex -4.0 273.4 3.9
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -4.0 272.0 9.5
vertex -4.0 273.4 3.9
vertex -4.0 272.0 6.5
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 273.4 12.1
vertex -4.0 275.8 13.8
vertex -4.0 278.7 14.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 273.4 12.1
vertex -4.0 278.7 14.1
vertex -4.0 273.4 3.9
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -4.0 273.4 12.1
vertex -4.0 273.4 3.9
vertex -4.0 272.0 9.5
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -4.0 189.4 3.9
vertex -4.0 194.7 1.9
vertex -4.0 191.8 2.2
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 189.4 3.9
vertex -4.0 197.5 2.9
vertex -4.0 194.7 1.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 189.4 3.9
vertex -4.0 199.4 5.1
vertex -4.0 197.5 2.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 197.5 13.1
vertex -4.0 199.4 10.9
vertex -4.0 200.2 8.0
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 197.5 13.1
vertex -4.0 200.2 8.0
vertex -4.0 199.4 5.1
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -4.0 188.0 9.5
vertex -4.0 189.4 3.9
vertex -4.0 188.0 6.5
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 188.0 9.5
vertex -4.0 197.5 13.1
vertex -4.0 199.4 5.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 188.0 9.5
vertex -4.0 199.4 5.1
vertex -4.0 189.4 3.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 189.4 12.1
vertex -4.0 194.7 14.1
vertex -4.0 197.5 13.1
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 189.4 12.1
vertex -4.0 191.8 13.8
vertex -4.0 194.7 14.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 189.4 12.1
vertex -4.0 197.5 13.1
vertex -4.0 188.0 9.5
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -4.0 105.4 3.9
vertex -4.0 110.7 1.9
vertex -4.0 107.8 2.2
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 105.4 3.9
vertex -4.0 113.5 2.9
vertex -4.0 110.7 1.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 105.4 3.9
vertex -4.0 115.4 5.1
vertex -4.0 113.5 2.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 113.5 13.1
vertex -4.0 115.4 10.9
vertex -4.0 116.2 8.0
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 113.5 13.1
vertex -4.0 116.2 8.0
vertex -4.0 115.4 5.1
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -4.0 104.0 9.5
vertex -4.0 105.4 3.9
vertex -4.0 104.0 6.5
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 104.0 9.5
vertex -4.0 113.5 13.1
vertex -4.0 115.4 5.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 104.0 9.5
vertex -4.0 115.4 5.1
vertex -4.0 105.4 3.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 105.4 12.1
vertex -4.0 110.7 14.1
vertex -4.0 113.5 13.1
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 105.4 12.1
vertex -4.0 107.8 13.8
vertex -4.0 110.7 14.1
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 105.4 12.1
vertex -4.0 113.5 13.1
vertex -4.0 104.0 9.5
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 26.7 14.1
vertex -4.0 29.5 13.1
vertex -4.0 31.4 10.9
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -4.0 20.0 9.5
vertex -4.0 21.4 3.9
vertex -4.0 20.0 6.5
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -4.0 20.0 9.5
vertex -4.0 23.8 2.2
vertex -4.0 21.4 3.9
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 23.8 13.8
vertex -4.0 31.4 10.9
vertex -4.0 32.1 8.0
endloop
endfacet
facet normal -1.00 -0.00 -0.00
outer loop
vertex -4.0 23.8 13.8
vertex -4.0 26.7 1.9
vertex -4.0 23.8 2.2
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 23.8 13.8
vertex -4.0 29.5 2.9
vertex -4.0 26.7 1.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 23.8 13.8
vertex -4.0 31.4 5.1
vertex -4.0 29.5 2.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 23.8 13.8
vertex -4.0 32.1 8.0
vertex -4.0 31.4 5.1
endloop
endfacet
facet normal -1.00 -0.00 0.00
outer loop
vertex -4.0 23.8 13.8
vertex -4.0 23.8 2.2
vertex -4.0 20.0 9.5
endloop
endfacet
facet normal -1.00 0.00 0.00
outer loop
vertex -4.0 23.8 13.8
vertex -4.0 26.7 14.1
vertex -4.0 31.4 10.9
endloop
endfacet
facet normal -1.00 0.00 -0.00
outer loop
vertex -4.0 21.4 12.1
vertex -4.0 23.8 13.8
vertex -4.0 20.0 9.5
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 3.5 3.9 22.0
vertex -6.0 10.5 22.0
vertex -6.0 7.5 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 3.5 3.9 22.0
vertex -6.0 7.5 22.0
vertex -4.6 4.9 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 3.5 3.9 22.0
vertex -4.6 4.9 22.0
vertex -2.2 3.2 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 3.5 3.9 22.0
vertex -2.2 3.2 22.0
vertex 0.7 2.9 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 0.7 15.1 22.0
vertex -2.2 14.8 22.0
vertex -4.6 13.1 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 0.7 15.1 22.0
vertex -4.6 13.1 22.0
vertex -6.0 10.5 22.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex 5.4 11.9 22.0
vertex 3.5 3.9 22.0
vertex 5.4 6.1 22.0
endloop
endfacet
facet normal -0.00 0.00 1.00
outer loop
vertex 5.4 11.9 22.0
vertex 5.4 6.1 22.0
vertex 6.2 9.0 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 5.4 11.9 22.0
vertex -6.0 10.5 22.0
vertex 3.5 3.9 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 5.4 11.9 22.0
vertex 0.7 15.1 22.0
vertex -6.0 10.5 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 3.5 14.1 22.0
vertex 0.7 15.1 22.0
vertex 5.4 11.9 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 3.5 290.9 22.0
vertex -4.6 291.9 22.0
vertex -2.2 290.2 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 3.5 290.9 22.0
vertex -2.2 290.2 22.0
vertex 0.7 289.9 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 5.4 293.1 22.0
vertex -6.0 294.5 22.0
vertex -4.6 291.9 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 5.4 293.1 22.0
vertex -4.6 291.9 22.0
vertex 3.5 290.9 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 6.2 296.0 22.0
vertex -6.0 297.5 22.0
vertex -6.0 294.5 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 6.2 296.0 22.0
vertex -6.0 294.5 22.0
vertex 5.4 293.1 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 5.4 298.9 22.0
vertex -4.6 300.1 22.0
vertex -6.0 297.5 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 5.4 298.9 22.0
vertex -6.0 297.5 22.0
vertex 6.2 296.0 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 3.5 301.1 22.0
vertex 0.7 302.1 22.0
vertex -2.2 301.8 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 3.5 301.1 22.0
vertex -2.2 301.8 22.0
vertex -4.6 300.1 22.0
endloop
endfacet
facet normal 0.00 0.00 1.00
outer loop
vertex 3.5 301.1 22.0
vertex -4.6 300.1 22.0
vertex 5.4 298.9 22.0
endloop
endfacet
endsolid shared_wall_bracket
```
