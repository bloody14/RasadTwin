# RasadTwin Change Control

## Protected changes

The following require explicit human authorization:
- problem interpretation;
- hypothesis wording;
- primary/secondary metrics;
- baselines;
- statistical tests;
- tuning protocol;
- test-set policy;
- data classification policy;
- security policy;
- model family changes that alter experiment meaning;
- routing objective or priority weights when they affect comparability;
- disruption/re-optimization definitions;
- result schema used by reports or figures.

## Required change record

For an approved change, append to `docs/CHANGELOG.md`:
- Date/time
- Human approver
- Files changed
- Before
- After
- Reason
- Impact on prior results
- Whether affected experiments must be rerun

## No silent migration

Do not overwrite old experimental data when a definition changes. Create a new run/config/schema version.
