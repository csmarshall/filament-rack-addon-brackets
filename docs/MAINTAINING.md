# Picking this repo up

A short note for whoever (or whichever session) works on this next. The [README](../README.md) and the part READMEs say what the parts are and how to print them; this says how the repo is run.

## The parts today

- **In-line bracket**: 36 x 305 x 40 mm, bar sockets on both faces with a 4 mm web between, fully rounded ends. One design.
- **Staggered brackets A and B**: 18 mm wide (the stock width), 27 mm rail, a mirror-image pair. Neighbouring columns stand 16 mm apart front to back.
- **End bracket**: one design for either end of a row, sockets on one face. Used as modelled at the right end, turned end for end at the left.
- **Fit test coupon** and the **anti-tip wall plate**.
- Every bracket has two zip-tie slits through its rail, for a tether to the wall plate. There are no anchor variants and no left/right end brackets.

## Orientation

Brackets are described as installed: **flat edge up**, seen from the room facing the wall. The models and drawings show the part as printed, flat edge down. Installed, A sets the column on its left 16 mm further back and B the column on its right; a staggered row is A, B, A, B from the left, so columns 1, 3 and 5 sit nearer the wall. `shared_wall_bracket.Params` is the source of every dimension, and `make_layout_diagram.py` shows the row.

## Process

Issue first, then a branch in a worktree, then a PR with `Closes #n`. CI is the gate. Squash-merge only when Charles says to. Don't push to `main`, and don't rebase or force-push a PR branch: bring it up to date by merging `main` into it. The old rule that froze the blueprint script and `Params` is gone; change them as the work needs, and say so in the PR.

## Publish and releases

`.github/workflows/publish.yml` runs on every push to `main`. It redraws the blueprint sheets and their README embeds with the shared [common-blueprint-generator](https://github.com/csmarshall/common-blueprint-generator) workflow, commits them as `blueprint: re-render from <sha>`, and then cuts a release from that tip. Every merge is a patch release; run Publish by hand (Actions > Publish > Run workflow) to pick a minor or major bump. A release has the prints archive and the source archive. Don't commit rendered blueprint SVGs or their embeds in a PR; CI owns them, and a hand-rendered copy only creates a conflict. If you add a blueprint sheet, add it to `render-command`, `commit-paths` and `prints-paths` in that file.

## Licences

`REUSE.toml` is the licence map: models, print files, drawings and docs are CC BY-NC-SA 4.0, and scripts and code (every `.py` file, `tools/` and `.github/`) are MIT. The blueprint generator reads it to print the licence on each drawing, so keep it accurate and add any new kind of file to it. Check with `uvx -q --from "reuse[charset-normalizer]==6.3.0" reuse lint`; the licence texts are in `LICENSES/`.

## Rebuilding the models and the U1 projects

`python3 shared_wall_bracket.py --out models` in `shared-wall-bracket/` rebuilds every STL and STEP (the setup is in the part README). The U1 `.3mf` projects were built against [snapmaker-profiles](https://github.com/Snapmaker/snapmaker-profiles) at commit `ba75baf`, which is not vendored: clone it, check out that commit, and run, for each part:

```sh
python3 -I tools/make_u1_project.py --stl shared-wall-bracket/models/<part>.stl --profiles /path/to/snapmaker-profiles/Snapmaker --out shared-wall-bracket/models/<part>_U1_ABS.3mf --brim-width 10
```

The 3MF files are not rebuilt by CI. Regenerate them whenever an STL changes, and use the same profiles commit so the diff shows only the real change.

## What is not verified

- **Nothing has been printed and nothing has been load tested.** Every strength figure is a section-property ratio from the model, not a test result.
- The fit coupon is still to be printed, so socket clearance (12.3 mm for a 12 mm tube) is untested.
- The `.3mf` projects pass a strict 3MF read and slice in Snapmaker Orca's command line, but nobody has confirmed the settings carry in when a project is opened in the GUI (File > Open Project, not Import).
- The upright socket centre (9 mm from the end) and the 20 mm inside corner radius are judged from photos, not measured.
- The rack's tier spacing, tier count and width come from the retail listing, not measurement.
