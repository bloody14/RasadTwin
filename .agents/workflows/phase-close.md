# /phase-close

1. Run targeted tests.
2. Run relevant full pytest suite.
3. Run ruff on changed Python files.
4. Run secret scan / repo grep for obvious credentials.
5. Verify no prohibited-data fixture was introduced.
6. Verify Windows PowerShell reproduction command.
7. Inspect Git diff for scope drift.
8. Write reports/PHASE_<N>_REPORT.md.
9. Update docs/STATE.md with current status and next action.
10. Do not claim PASS; the human/Technical Lead reviews the report.
