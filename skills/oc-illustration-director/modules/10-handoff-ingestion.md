# Handoff Ingestion

Required files:

- `manifest.json`
- `root-canon.json`
- `strong-reference.json`
- `approved-variants.json`
- `consistency-lock.json`
- `reference-manifest.json`

Optional:

- `ACTIVE_CONTEXT.md`
- `character-summary.md`

Validate schema version, character ID, Canon revision and SHA-256. Copy the handoff snapshot into `source/handoff/`; never edit it in place.

Compile `state/identity-contract.json` with:

- root body facts;
- root face facts;
- permanent identity details;
- selected strong reference and variant IDs;
- drift risks;
- source revision and manifest hash.
