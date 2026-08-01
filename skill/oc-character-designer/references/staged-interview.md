# Staged interview

## Modes

- Rapid: resolve only fields required for the current deliverable.
- Standard: complete stable body, face, strong references and production rules.
- Deep: add detailed measurements, acting systems, production and rigging notes.

## Stages and readiness

| Stage | Purpose | Key paths |
|---|---|---|
| S0 | goal and deliverable | `production_spec.intended_use`, `production_spec.requested_pages` |
| S1 | concept | `root_canon.identity.*` |
| S2 | body | `root_canon.body_core.*` |
| S3 | face | `root_canon.face_core.*` |
| S4 | permanent details | `root_canon.identity_details.*` |
| S5 | strong references | `strong_reference.*` |
| S6 | reusable variations | `variants.*` |
| S7 | publication/production | `production_spec.*`, `presentation.*` |
| S8 | review and lock | `consistency_lock`, `qa.*` |

Questions are dependency-ordered. Do not ask decorative details before height/proportion, face geometry and identity anchors. One answer may fan out to several paths. Stop when the requested deliverable is ready.
