# Quality gates

1. Package versions agree.
2. All JSON parses and validates structurally.
3. No old `visual_canon` or `oc_profile` path exists in active contracts.
4. S0–S8 are accepted by the question schema.
5. A batch either commits completely or writes nothing.
6. Root Canon changes require explicit revision evidence.
7. Index, chapters and active context rebuild from Canon.
8. Handoff hashes verify before downstream use.
9. Generated binary outputs are reproducible and excluded from source control.
