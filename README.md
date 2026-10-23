# Energy modeling lab

Personal energy-modeling research by Christopher John Nichols. This initial package documents a hypothetical 2030 PJM technology comparison and contains small reusable preparation utilities. No affiliation with or endorsement by PJM, Johns Hopkins, GenX, or an employer is implied.

The study has nine zones, 798 resources and 8,760 chronological hours, using ATB 2025 Moderate assumptions for the 2030 cost year and global 20 GW technology cost tiers. **There is no validated annual baseline, forecast, or scientific result in this repository.**

Start with [methodology](studies/pjm-2030/METHODOLOGY.md), [reproduction scope](studies/pjm-2030/REPRODUCIBILITY.md), [provenance and licenses](studies/pjm-2030/provenance/LICENSES.md), and [evidence status](studies/pjm-2030/STATUS.md).

The first tree intentionally contains no model input datasets, upstream GenX source, model outputs, infrastructure scripts, or raw logs. The included tests validate preparation logic only. Full annual reproduction remains blocked by source-version reconciliation, attribution review, portable integration, and validation of the annual model.

## Quick check

From this repository root, run `python -B -m unittest discover -s studies/pjm-2030/tools -p test_tiers.py -v`. Only the Python standard library is needed. This does not run GenX or contact a cloud service.

## Rights and citation

The original Python preparation scripts are licensed under MIT; newly prepared documentation is licensed under CC BY 4.0. See [RIGHTS.md](RIGHTS.md) for exact scope and upstream exclusions. Citation metadata identifies this personal study package and does not claim authorship of upstream software or datasets. No release DOI exists.
