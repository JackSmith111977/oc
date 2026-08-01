# Version governance

`VERSION` is the only authoritative package version. Current value: `3.1.2`.

Mirrors checked by `scripts/release_guard.py`: README title, SKILL metadata, first changelog entry, module registry and manifest.

Independent contracts do not need to equal the package version:

| Contract | Version |
|---|---:|
| Canon schema | 3.1 |
| Workspace | 1.1 |
| Question batch | 1.0 |
| Answer batch | 1.0 |
| Sheet page | 1.0 |
| Character-bible template | 1.1.0 |

Generated PDF/PNG files are release artifacts, not source-of-truth files, and are excluded from the repository.
