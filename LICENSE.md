# Licensing

Copyright (c) 2026 Charles Marshall.

This repository is under two licences. Which one applies depends on the file.

| What | Files | Licence |
|---|---|---|
| **The designs** | Each part's folder (`shared-wall-bracket/`, `anti-tip-wall-plate/`): the CAD source that defines the part, the STL, STEP and 3MF models, drawings and diagrams. Also `docs/` and every README. | [CC BY-NC-SA 4.0](LICENSE-DESIGNS.md) |
| **General-purpose tooling** | `tools/` and `.github/` | [MIT](LICENSE-CODE) |

## What that means in practice

**You may**, free of charge:

- print the parts for yourself, your household, your workplace or a makerspace;
- change the designs and share your versions, as long as you credit the
  original and share under the same licence;
- use the tooling in `tools/` for anything, including commercial work.

**You may not**, without written permission:

- sell these files, or prints made from them, or remixes of them. That
  includes listing them on Etsy, eBay, Amazon or any print-on-demand service,
  whether or not you credit the source.

If you would like to sell prints, open an issue on this repository to ask.

## Why the part scripts are not MIT

`shared_wall_bracket.py` and `wall_plate.py` are the designs, written as code:
running them produces the models. They are therefore licensed with the designs
(CC BY-NC-SA 4.0), not with the tooling. Models generated from them, with any
parameters, are covered by the same licence.

## No warranty

Both licences provide the material as-is, with no warranty. See also the
[disclaimer](DISCLAIMER.md).
