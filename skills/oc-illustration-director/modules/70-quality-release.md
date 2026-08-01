# Quality and Release

Pre-generation QA compares the prompt against the identity contract. Post-generation QA compares the output against root body, root face, permanent identifiers, selected appearance state, scene brief and safety constraints.

Result statuses:

- `approved`
- `approved_with_notes`
- `revise`
- `rejected_identity_drift`
- `rejected_scene_or_safety`
