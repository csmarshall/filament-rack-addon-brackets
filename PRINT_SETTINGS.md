# Print settings

Every slicer setting these parts need changed from the defaults, in one place.
The `.3mf` projects carry the bracket settings, but only when opened with
**File > Open Project**. If you import an STL, or import a `.3mf`, set these by
hand.

**Do not print these parts in PLA.** They carry a constant load, and PLA slowly
deforms under constant load and softens when warm. Use ABS, ASA or PETG. Read
the [disclaimer](DISCLAIMER.md) first.

The "where" column is the tab and group in Snapmaker Orca and OrcaSlicer.

## Shared-wall brackets (in line and staggered)

| Setting | Set it to | Where (tab / group) | U1 stock value |
|---|---|---|---|
| Wall loops | **5** | Strength / Walls | 2 |
| Wall generator | **Arachne** | Quality / Wall generator | Classic |
| Sparse infill pattern | **Gyroid** | Strength / Infill | Grid |
| Sparse infill density | **15%** | Strength / Infill | 15% (unchanged) |
| Bottom shell layers | **5** | Strength / Top/bottom shells | 3 |
| Brim type | **Outer brim only** | Others / Brim | Auto |
| Brim width | **5 to 10 mm** | Others / Brim | 5 mm |
| Layer height | 0.20 mm | Quality / Layer height | 0.20 mm (unchanged) |

On the plate:

1. Lay the part with its **flat edge on the bed** (the long straight edge, with
   the legs pointing up). No supports.
2. **Rotate it 45 degrees** about the vertical and centre it. It only fits a
   270 mm bed corner to corner, one per plate.
3. Largest brim that fits a 270 x 270 mm bed: 10 mm for the in-line and
   staggered brackets, 5 mm for the in-line anchor variant.

## Anti-tip wall plate

| Setting | Set it to | Where (tab / group) |
|---|---|---|
| Wall loops | **4 or more** | Strength / Walls |

Print it standing on its profile: the T-shaped face on the bed, the 22 mm
width pointing up. No supports.

## Fit-test coupon

Print it first, with the same settings as the brackets, and check how a tube
goes into each socket before printing a full bracket.
