# Illustration Handoff Contract

## Authority map

| Data | Authority | Downstream behavior |
|---|---|---|
| root body | upstream | read-only |
| root face | upstream | read-only |
| permanent identity details | upstream | read-only |
| default hair/costume | upstream | select, do not redefine |
| approved variants | upstream | select by ID |
| scene/camera/light/style | downstream | writable |
| reusable new variant | upstream approval | submit change request |

## Revision rule

Every project stores `source_character_revision`. A refreshed handoff with a different revision must be diffed before further generation. Root changes invalidate prior identity QA; strong-reference-only changes invalidate prompts using the affected state.
