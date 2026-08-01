---
name: oc-character-designer
description: Build and persist an original character through concept-guided staged question batches, body/face Root Canon, strong references, approved variants, landscape setting sheets, and a file-backed character bible.
metadata:
  version: "3.1.2"
  language: "zh-CN"
  canon_schema: "3.1"
  workspace_format: "1.1"
  character_bible_template: "1.1.0"
  downstream_compatibility: "oc-illustration-director >=2.0.0,<3.0.0"
---

# OC Character Designer

## Authority hierarchy

`root_canon.body_core -> root_canon.face_core -> root_canon.identity_details -> strong_reference -> variants -> presentation`

- Root Canon defines the body, face and permanent identity of the character.
- Strong Reference defines default hair, costume, accessories and palette, with explicit change boundaries.
- Variants contain approved reusable alternatives.
- Presentation contains scene, camera, lighting, style and effects; it never rewrites identity.

## Runtime

1. Read `ACTIVE_CONTEXT.md`, then the active batch and only the required chapter.
2. Extract all facts already supplied by the user before asking anything.
3. Ask 1–3 tightly related questions from one stage as a batch.
4. Prefer a native Ask UI only when the runtime exposes it; otherwise use structured options plus custom input.
5. Persist the entire answer batch through a dry-run and one transactional commit.
6. Never silently replace a non-empty fact. Revision requires `expected_old` and a reason.
7. Generate clean visual assets first; add formal text, measurements and callouts through deterministic PDF/vector composition.

## Stages

- S0 goal and deliverable
- S1 character concept
- S2 body Root Canon
- S3 face Root Canon
- S4 permanent identity details
- S5 hair, costume, palette and accessories as strong references
- S6 approved variants, expression and acting range
- S7 production and character-bible specification
- S8 review, conflicts and lock

Use `references/staged-interview.md` and `references/questionnaire.md`.

## Required setting sheets

For a stable recurring OC, prefer landscape pages for body core, silhouette/proportion, head construction, facial-feature breakdown, expression stability, permanent details, hair reference, costume reference, full turnaround and consistency errors.

## Handoff

Export Root Canon, strong references, approved variants, consistency lock, source revision and hashes. The downstream illustration skill may direct the image but may not redefine Root Canon.

## Governance

`VERSION` is the sole package-version source. Run `python scripts/release_guard.py --check` before publishing.
