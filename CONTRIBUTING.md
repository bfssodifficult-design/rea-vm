# Contributing to rea-vm

Thanks for helping. Please keep changes small, testable, and honest.

## Before you open a PR

```bash
python -m py_compile scripts/preflight_check.py
python scripts/preflight_check.py --json
```

Also check:

- `SKILL.md` frontmatter parses and `name` matches the directory.
- Every path referenced from `SKILL.md` exists.
- No credentials, private IPs, personal paths, or sample-specific values are
  added.
- Any behavior change updates `references/` and the README.

## Style

- Prefer explicit statuses over silent fallbacks.
- Keep commands copy-pasteable.
- Do not claim a tool ran unless it did.
- Keep the skill usable without REA, IDA, or PaperJSX; degrade, do not fail
  silently.

## Security reports

Do not open a public issue for a vulnerability. See `SECURITY.md`.
