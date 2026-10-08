# UCBP Phase 0 + Phase 1 Completion Record

Status: `NON_CANONICAL_RESEARCH_CANDIDATE`  
Backup role: `BACKUP_ONLY_NON_CANONICAL`  
Parent research artifact commit: `a4eb06c5fb5b7f844ee3978f4da3bae9e2e111f4`

## Completed scope

The bounded work unit from `FORENSIC_ANALYSIS_AND_IMPLEMENTATION_PLAN.md` is complete:

- UCBP session schema;
- hypothesis-lattice schema;
- intervention-authorization schema;
- semantic-promotion state machine;
- synthetic hidden-protocol benchmark specification;
- red-team test matrix;
- reference synthetic-agent generator;
- passive decoder;
- constrained expected-information-gain active decoder;
- reproducible evaluation harness and CLI;
- safety/reproducibility tests;
- reference benchmark result;
- integrity manifest.

## Validation

`PYTHONPATH=src python -m unittest discover -s tests -v`

Result: **6/6 PASS**.

Reference benchmark:

`PYTHONPATH=src python run_benchmark.py --trials 100 --budget 12 --meanings 6 --noise 0.10 --output BENCHMARK_RESULT.json`

Observed candidate evidence:

- passive mean mapping accuracy: `0.9533333333333334`;
- active mean mapping accuracy: `0.9816666666666667`;
- active minus passive: `+0.02833333333333332`;
- unauthorized interventions: `0`.

This is a reference result, not a claim of universal superiority. The plan still requires variation across budgets, noise levels, protocol families, and independent implementations before scientific promotion.

## Safety properties exercised

The reference runtime fails closed when:

- no intervention authorization is supplied;
- the intervention budget is exhausted;
- the requested synthetic context is outside scope.

It has no network I/O and performs no human, animal, or unknown-external-system interaction.

## Preservation

The exact implementation package is stored as `ucbp_phase0_phase1.tar.gz.b64`. Decode Base64, then decompress the gzip tar archive. File-level SHA-256 values are recorded in `IMPLEMENTATION_MANIFEST.json` inside the package.

The package remains non-canonical. No project authority, policy, accepted state, external-contact permission, or field-experiment permission is changed by this artifact.
