# Session handoff: everything the cloud session knew

Written 2026-11-18 by the claude.ai session that built this repo, for the
Claude Code session on Charles's machine. `LOCAL_SETUP.md` is the checklist;
this is the background. Where this file and the code disagree, the code on the
newest PR branch wins. Delete both files when they stop being useful.

## 1. Who you are working for and how he works

- Charles Marshall, GitHub `csmarshall`. 20+ years SRE and systems; not a
  software developer by title but reads code fluently. Skip the basics.
- Prints on a Snapmaker U1 (270 x 270 bed, 0.4 nozzle, Snapmaker Orca on
  macOS). Prints these parts in ABS.
- Often on his phone. Lead with the answer; keep replies short. He types fast
  with typos; read for intent.
- He wants diagrams and multiple-choice polls for questions about geometry,
  not prose. "Show me" means draw it.
- Don't ask permission for obvious steps. Do ask before anything irreversible.
  **Never merge without the word "merge".**
- When he corrects something, fix it and move on. No long apologies.
- Code style: complete code, never "re-implement here" stubs; logging with
  timestamps and configurable levels; comments on non-obvious logic; keep
  existing comments.
- Drafted messages for him to send: short, in his voice, and after any edit
  show the whole draft again.
- AI framing in docs: human-directed, AI-assisted.
- Commits end with `Co-Authored-By:` for the model. PR bodies end with the
  Claude Code line.

## 2. What this is

Add-on parts for the Hizypaixin 9-tier filament rack, Amazon ASIN B0FFZ8SSQX.
The seller name is a throwaway brand; the repo is named for findability
(`filament-rack-addon-brackets`). The kit's only plastic part is one bracket,
used top and bottom of every tier, that joins 12 mm steel tubes. Each column
is self-standing. The goal: neighbouring columns share one wall.

Parts:
- **In-line shared-wall bracket** (`shared_wall_bracket_v2`): two stock
  brackets back to back, 40 wide.
- **Staggered shared-wall bracket** A and B: stock width, sockets offset.
- **Anchor variants** of all of the above, for a zip-tie tether to the wall.
- **End brackets** left and right, with anchor (PR #10).
- **Anti-tip wall plate** (`anti-tip-wall-plate/`): screws to the wall, takes
  the other end of the zip tie.
- **Fit test coupon**: one upright socket, one bar socket.

## 3. The stock bracket, as measured

Charles measured with calipers. Treat these as ground truth:

- 305 long, 18 thick, legs 40 tall and 18 long at each end, rail 18 tall
  between them, flush with one flat edge (top and bottom are interchangeable).
- Tubes 12 mm.
- Four bar holes on one face, 2 mm in from the flat edge (centre 8 mm from
  it), centres 26 / 110 / 194 / 278 (84 pitch). **16 mm deep.**
- Upright sockets: 18 deep from the flat edge and 18 deep from the leg end,
  with a 4 mm divider between and a 4 mm through-hole in the divider.
- Ends fully rounded in plan. Underside is skeletonised (injection moulded).

Judged from photos, **not measured**: inside corner radius about 20 mm where
the leg meets the rail; upright socket centre 9 mm from the end.

History of wrong numbers, so you don't reintroduce them:
- "33 mm" rail height was a misreading. It is 18.
- Bar socket depth was first given as 18. It is 16. The in-line bracket was
  built on 18 for a while; fixed.
- A "2 mm divider" in the upright was an early guess. It is 4.
- The `legacy/` folder is v1, drawn from listing photos. Not for printing.

Kit facts from the listing: 9 tiers, about 2040 mm tall, tier pitch 250 used
in the row sheets, stock column width 17.3 in. Uprights and horizontals are
two different tube lengths.

## 4. Design decisions and why

**In line (40 x 305 x 40).** Bar sockets 16 deep on both faces, 8 mm web
between, 4 mm vent through the web (Charles's idea: so you are not pushing a
tube against trapped air). Upright sockets 18 / 4 / 18 as stock. Sockets
12.3 mm (`fit_clearance` 0.3), untested.

**Staggered (18 x 320 x 40).** Charles asked whether offsetting the holes
would avoid doubling the width. One face's bar set is shifted 16 mm along the
bracket (left 26/110/194/278, right 42/126/210/294) so opposite sockets pass
side by side. 16 deep leaves a 2 mm back wall. Length grows to 320. He then
asked that it be stock width and profile, and "just as strong as the wider
one": the rail is 27 mm tall because 18 x 27^2 = 40 x 18^2. The extra 9 mm is
on the side away from the flat edge, so socket heights still match stock.
Corner radius drops to 13 to fit. It is still far less stiff sideways (0.14)
and has only the stock 2.85 mm upright wall; the README says so.

**A and B.** Mirror pair. Facing the rack, A sets the column on its right
16 mm back; B the column on its left. End-for-end changes nothing. Upside
down does not turn A into B (bars end up at the wrong height).

**Row rule.** Staggered rows should have an odd number of columns, three or
more, alternating B, A, B, A from the left, so both end columns sit nearest
the wall. Two columns on one bracket leaves the ends 16 mm apart in depth.

**Rounding.** Kernel fillets on the top edges thinned socket walls and made
degenerate triangles, because OpenCascade propagates fillets along tangent
edges. `edge_round` defaults to 0 and should stay there. Lead-in chamfers are
cut as cones (`cq.Solid.makeCone`), not kernel chamfers, for the same reason.
Plan rounding on PR #4 is an intersection with a rounded outline.

**Lightening.** Considered and dropped. Skeletonising suits moulding, not
FDM; walls and infill already do that job. Real saving would be about 26 to
30 percent, not the 45 first estimated.

**Anchor.** Charles wanted it to copy the common furniture anti-tip kit: a
plate on the furniture, a plate on the wall, a zip tie between. First attempt
had screw ears; he rejected it. He floated a print-in-place zip tie, then
dropped it: use a bought nylon tie. Saddle: slot 13 x 3.2, 6 mm bar, 22 high,
5 mm legs, printed as one profile from the bed so layers run through legs and
bar. On 18 mm brackets the legs don't fit, so PR #10 widens the rear 26 mm to
23 mm as a collar (side wall 5.35, wall toward the slot 2.85).

**End brackets** (PR #10). "End brackets for the staggered version that
include the anchor" could mean two things. Both were built: anchor variants of
A and B, and stock-size single-sided brackets (`Params.end("left"|"right")`,
new field `bar_faces`). Charles has not yet confirmed which he meant.

**Wall plate.** 60 x 22 x 14.2, saddle slot 9.5 x 3.2, two 4.8 mm screw
holes, printed standing on its profile.

## 5. Print settings and where they came from

5 wall loops, Arachne, 15 percent gyroid, 5 bottom shell layers, 10 mm outer
brim, ABS / ASA / PETG, flat edge down, no supports, rotated 45 degrees, one
per plate. **Not PLA**: constant load, creep, softens warm. Charles
specifically does not want someone printing in PLA and blaming him.

- Wall loops: he asked whether loops should match the 2 mm hole offset. Five
  loops at 0.42 make every socket wall (1.85, 2.85, 3.85) solid perimeter.
  He once said "6?"; five is what shipped and he accepted it.
- Gyroid was checked against the OrcaSlicer wiki and kept; links are in the
  part README's "Why these settings".
- Orca UI names: Strength > Walls, Quality > Wall generator, Strength >
  Infill, Strength > Top/bottom shells, Others > Brim. `PRINT_SETTINGS.md`
  is the reference for people importing bare STLs.

## 6. The U1 3MF projects: what was learned

`tools/make_u1_project.py` writes an Orca-style project by hand.

- `Metadata/project_settings.config` is JSON: `printer_settings_id`,
  `print_settings_id`, `filament_settings_id`, `filament_colour`,
  `different_settings_to_system`, `inherits_group`. Keys not listed are taken
  from the installed system presets.
- Presets: `Snapmaker U1 (0.4 nozzle)`, `0.20mm Standard @Snapmaker U1 (0.4
  nozzle)`, `Generic ABS @U1 0.4 nozzle`.
- Charles reported the settings did not carry in. Two fixes since: overrides
  are also written per object in `Metadata/model_settings.config`, and the
  Application tag is `BambuStudio-02.00.00.00` with `BambuStudio:3mfVersion`
  so the loader treats it as a project. **Neither fix is confirmed.** File >
  Import brings geometry only and discards settings; File > Open Project is
  required. First thing to do locally: have him open one and report the wall
  count, generator, infill, brim and slot 1 filament. You have his machine; if
  Snapmaker Orca is installed, save a real project from it and diff against
  ours.
- Profile JSON has a BOM; read as `utf-8-sig`. lib3mf strict read rejects
  undeclared metadata prefixes and a `printable` attribute.
- He has a separate project on U1 print-settings optimisation; its findings
  about Snapmaker Orca's file formats may help here.

## 7. Repo mechanics

- `shared_wall_bracket.py`: `Params` dataclass, `build_bracket(p)`,
  `build_coupon(p)`, `Params.staggered(...)`, `Params.end(side)`. `main()`
  exports everything. `docs/claude-code-handoff.md` embeds a copy of the
  script; resync its python block whenever the script changes (or propose
  deleting it now that you have the repo).
- `make_readme_stl.py` rewrites the ASCII STL block in the part README that
  GitHub renders as a 3D viewer. Charles said it "isn't working" and never
  said what he saw. Mesh was halved to 684 triangles with real normals. It
  may be the GitHub mobile app, which does not render STL blocks. Ask.
- `make_layout_diagram.py`, `make_row_sheets.py` (PR #8): matplotlib sheets.
  Row of five: about 2213 mm wide in line, 2125 staggered; per row 36 in-line
  brackets or 18 A + 18 B, 18 stock brackets, 96 uprights, 180 bars.
- `tools/make_release.py` and `.github/workflows/release.yml`: two zips per
  release. PR #6 renames them `-prints-vX.Y.Z.zip` and `-source-vX.Y.Z.zip`,
  bumps patch from the newest tag on every push to main, and adds a manual
  dispatch for minor and major. Untested on GitHub.
- In the cloud sandbox `gh` GraphQL was blocked, so everything used
  `gh api repos/...`. You probably have normal `gh`.

## 8. Cross-repo baseline (from the common-blueprint-generator session)

Standing for every part repo of his:

- Drawings come from `csmarshall/common-blueprint-generator` in one house
  style. Never hand-edit a sheet. README embeds the SVG between
  `<!-- blueprint:NAME -->` and `<!-- /blueprint -->`; don't edit between the
  markers. Commit the SVG only, no PNG.
- Licensing: models, print files and drawings CC BY-NC-SA 4.0; scripts and
  code MIT. Reason: he does not want these resold on Etsy. Known consequence,
  accepted: MIT scripts can lawfully generate models. The README explains why
  the licences were picked (PR #6).
- Releases: every merge to main cuts a patch; minor and major by hand. A
  shared reusable release workflow is being built in the generator repo and
  runs after the blueprint render. Remove the local workflow when it lands.
- Support: shields badge, `.github/FUNDING.yml` custom link to
  https://buymeacoffee.com/cs_marshall, link on the credit line under
  drawings.
- Process: issue, branch in a worktree under
  `~/work/claude/<repo>-worktrees/`, PR with `Closes #n`, CI gate, a rev-s
  review, squash-merge.
- Proposed, not yet agreed: a `REUSE.toml` in each repo as the machine-
  readable licence map, read by the blueprint generator to print the right
  licence on each sheet. Charles was given prompts to take to the generator
  session and to the tag-clip session (whose models are likelier to be
  resold). Check with him where that landed before adding one here.

## 9. Liability wording

He wants to be protected: `DISCLAIMER.md` is a hold-harmless, as-is,
no-warranty notice; the READMEs carry a load warning and the PLA warning. Not
legal advice and not reviewed by a lawyer. Keep the warnings prominent in
anything new, and say plainly that nothing has been load tested.

## 10. Waiting on Charles

1. "merge" for #6, #4, #10, #8, #13.
2. Fit coupon result (adjust `--fit-clearance`).
3. Whether the 3MF settings load via Open Project.
4. What the README STL viewer shows, and in which app.
5. Which reading of "end brackets" he wanted, or both.
6. Whether to drop the staggered-anchor brim to 5 mm (3.9 mm bed margin now).

## 11. Offered, never requested

Vents on the staggered bracket; an assembly STEP for a house-style assembly
drawing; rewriting commit author on old history; repo description and topics;
updating previews and row diagrams for the PR #10 parts.

## 12. Things only on claude.ai

- 3D viewer artifact: https://claude.ai/artifact/Cide5AAxKab6GvvGpy5jUo
  (in line, anchor, staggered, coupon; not the PR #10 parts). Its source is
  not in the repo. Rebuild from the STLs if wanted.
- The photos Charles sent of the stock bracket are in that chat only.
