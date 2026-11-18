# Local setup

Instructions for a Claude Code session on Charles's machine picking this repo
up from the cloud session that built it (2026-11-18). Read this before doing
anything else. Don't merge, rebase, push or edit until asked.

## 1. Get the repo

- Clone to `~/work/claude/filament-rack-addon-brackets`. If it exists, run
  `git fetch --all --prune` and fast-forward `main` only if that is a clean
  fast-forward. If there are local changes or branches have diverged, stop and
  say so.
- Make one worktree per open PR branch under
  `~/work/claude/filament-rack-addon-brackets-worktrees/`, tracking origin.
  Get the list from `gh pr list`. Skip any that exist.

## 2. State when this note was written

| PR | Branch | Head | Notes |
|---|---|---|---|
| #2 | `1-common-blueprint` | moving | From the common-blueprint-generator session. Not ours to edit. |
| #4 | `in-line-round-ends` | `fe6a3a0` | Full-round ends on the in-line bracket. |
| #6 | `align-baseline` | `11a5e07` | Licences, release zips, tag-based versions, funding link. |
| #8 | `row-of-five-sheets` | `0589e83` | Assembly sheets for a row of five. |
| #10 | `end-brackets-and-staggered-anchor` | `3e320ba` | Stacked on #4. Staggered anchors and anchored end brackets. |

`main` was `7af6a10`, release `v1.0.0`. This note is on `local-setup-notes`.
Report each branch's head and flag any that differ, then `gh pr checks` each
PR.

Planned merge order: #6, #4, #10, #8. Squash-merge, and only when Charles says
"merge". Retarget #10 to `main` after #4 merges. Each merge cuts a patch
release.

## 3. Rules that still stand

- Don't edit `shared-wall-bracket/make_blueprint.py`, `blueprint.png` or
  `blueprint.svg` until PR #2 lands. The drawing is stale on purpose.
- Keep `shared_wall_bracket.Params` and `build_bracket(p)` stable, along with
  the fields the drawing reads: length, height, thickness, rail_height,
  leg_length, bar_y, bar_z, bore, bar_depth, chamfer, corner_radius,
  plan_round, upright_from_end, upright_depth_leg, upright_depth_flat, web,
  divider, upright_vent_d, tube_od. If one has to change, say so in the PR.
  PR #10 adds `bar_faces` and `Params.end(side)`; it changes none of those.
- Process: issue first, a branch in a worktree, a PR with `Closes #n`, CI as
  the gate, squash-merge. Earlier commits went straight to `main`; don't
  repeat that.
- Models, print files, drawings and docs are CC BY-NC-SA 4.0. Every script and
  `.github/` is MIT (PR #6 makes this true).

## 4. Rebuilding

```
pip install -r requirements.txt
python shared-wall-bracket/shared_wall_bracket.py      # STL and STEP
python anti-tip-wall-plate/wall_plate.py
```

The `_U1_ABS.3mf` projects need Snapmaker's printer profiles, which are not in
this repo:

```
git clone https://github.com/Snapmaker/snapmaker-profiles ~/work/claude/snapmaker-profiles
# built against commit ba75baf (2026-11-12)
python3 -I tools/make_u1_project.py \
  --stl shared-wall-bracket/models/NAME.stl \
  --profiles ~/work/claude/snapmaker-profiles/Snapmaker \
  --out shared-wall-bracket/models/NAME_U1_ABS.3mf \
  --name "NAME" --brim-width 10
```

The committed `.3mf` files are usable as they are; only clone the profiles to
regenerate them.

## 5. Not verified

- Nothing has been printed. Socket fit (12.3 mm for a 12 mm tube) is untested;
  the fit coupon comes first.
- Nothing has been load tested. Strength figures are section-property ratios.
- The `.3mf` projects pass a strict 3MF read but have not been confirmed in
  Snapmaker Orca. They must be opened with File > Open Project, not Import.
  Charles has the U1; ask him what loads.
- The embedded STL viewer in `shared-wall-bracket/README.md` was reported not
  working; cause unknown.
- The release workflow in PR #6 has not run on GitHub.

## 6. Open loose ends

- Preview images, `row_of_five*.png` and the claude.ai 3D viewer don't show
  the PR #10 parts.
- `REUSE.toml` is to be added once the central session agrees the format.
- Remove the local `release.yml` when the shared release workflow lands.
- Repo description and topics are unset. Commit author on existing history is
  `Claude <noreply@anthropic.com>`.
- Staggered anchors clear the U1 bed edge by only 3.9 mm with a 10 mm brim.

Delete this file once the PRs above are merged and the notes no longer apply.
