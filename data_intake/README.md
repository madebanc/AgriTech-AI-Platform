# Data Intake — Real Field Data

This folder is the only place real farm data lands before verification.

Structure:

- data_intake/review — Drop raw field data here when collected, with source notes.
- data_intake/verified — Move a file here only after you personally confirm it against your field visit or trusted extension source.
- Do not point the live app at review. The live app reads only from verified.

Review checklist before a file moves to verified:

1. Source stated, who collected it, which LGA, which season, and which market.
2. Sample size noted, how many farms or market points.
3. Units stated, hectare versus acre versus plot, and kilograms versus bags.
4. Price dates stated, week and year.
5. Your cross check with at least one independent point.
6. Indicative label removed only after the above five are met.

Until a file is in verified, the live site keeps its synthetic example ranges and the honesty labels from Day 21 remain.