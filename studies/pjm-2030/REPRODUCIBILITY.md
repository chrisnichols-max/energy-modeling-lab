# Reproduction scope

## Included, independently runnable check

From the repository root: `python -B -m unittest discover -s studies/pjm-2030/tools -p test_tiers.py -v`.

The standard-library utilities are retained as small preparation examples. `xlsx_read.py` reads cached workbook cell values; it neither recalculates formulas nor verifies economic interpretation. The tier tests are historical preparation tests, not the final GenX integration suite.

## Annual model restoration plan - blocked, not a runnable pipeline

1. Reconcile the local ICARUS Base archive hash in `provenance/sources.json` to an immutable upstream commit. The recorded geography commit must not be silently assigned to the Base archive. Inspect archive/file attribution and the GenX conversion README.
2. Download the ATB 2025 workbook from its official catalog and match the recorded SHA-256. Resolve the precise workbook revision; retain cell-level parameter provenance. Obtain PJM hourly forecasts, EPA network/potential data, and any other required inputs directly after terms review. No bulk inputs are supplied here.
3. Use a separate isolated environment with Julia 1.9.4 and GenX v0.4.5. Preserve HiGHS.jl 1.20.1 and HiGHS_jll 1.12.0+0 (native 1.12.0). `environment/Manifest.provenance.toml` is the local dependency record, not an installable standalone project. Verify the upstream tag and local modifications before restoring its environment; do not upgrade the solver silently.
4. Port and review the excluded preparation/integration routines, replace machine paths with explicit arguments, preserve GPL notices for GenX adaptations, and produce a deterministic build graph. Pin the three demand cases and every generated-input checksum. The selected scenario JSON alone cannot reconstruct the model.
5. Run static input checks and small Julia formulation tests, including units/scaling, resource/demand counts, pool sharing, equivalence, bounds and recurrence. Then build the annual model in an independently authorized run; report all solver statuses honestly.

No annual command is provided because the portable, rights-cleared build chain is not yet established. No software was installed or environment instantiated while preparing this package.
