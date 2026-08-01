# File-backed persistence

## Workspace

```text
character/
├── INDEX.md
├── ACTIVE_CONTEXT.md
├── canon/
│   ├── canon.json
│   └── chapters/
├── interview/
│   ├── pending.json
│   └── batches/
├── history/
│   ├── events.ndjson
│   └── commits/
├── snapshots/
└── handoff/
```

`canon/canon.json` is the single machine fact source. Chapters and compact context are regenerated projections.

## Transaction

`questions.json -> user batch reply -> answers.json -> dry-run -> atomic Canon replacement -> commit record -> projections`

The CLI accepts files, not nested JSON shell parameters. A stale `base_revision`, unknown path or failed explicit-revision check rejects the whole batch.
