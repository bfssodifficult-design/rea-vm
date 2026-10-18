# rea-vm

`rea-vm` is the VM interface layer for REA. It gives an agent a controlled path
from REA static analysis to an authorized virtual machine, dynamic evidence,
IDA screenshots, and a structured report, without pretending that missing
tools worked.

The repository ships as an Agent Skill: `SKILL.md` is the entry point, the
`scripts/` and `references/` directories carry the runtime checks and
operating contracts.

## Interface contract

`rea-vm` exposes four explicit contracts:

1. **Connection** - `vm.host`, `vm.user`, `vm.key`, optional `vm.vmx` and
   snapshot. Values come from configuration or the user; there are no hidden
   defaults for hosts, accounts, or keys.
2. **Capability** - `scripts/preflight_check.py --json` reports
   `supported`, `unsupported`, `unavailable`, or `unknown` for each dependency.
3. **Execution** - SSH/SFTP actions carry timeouts, exit-status checks, file
   hashes, and cleanup; complex commands run as uploaded scripts.
4. **Evidence and report** - a normalized evidence tree, real screenshots
   where available, and PaperJSX or Markdown output with explicit provenance.

The interface never invents a connection, never silently drops a blocked
stage, and never claims a report engine that did not run.

## What it covers

- REA provider discovery and static analysis
- SSH/SFTP access to an authorized VM
- Dynamic execution and debugging with snapshots
- IDA / IDA MCP evidence and real screenshots
- Evidence grading and PaperJSX or Markdown reporting

## Install

Copy the directory into the client's skill location:

```text
<codex-home>/skills/rea-vm/
```

Invoke explicitly:

```text
$rea-vm
```

## Preflight

```bash
python scripts/preflight_check.py --json
python scripts/preflight_check.py --config examples/example-config.yaml --json
```

The probe is read-only and never prints secrets. Missing capabilities are
reported as `unavailable` or `unknown`; they are not defaulted to success.

## Publish

GitHub CLI is expected at `D:\Tools\gh\bin\gh.exe` or on `PATH`.

```powershell
gh auth login
git config --global user.name "<your name>"
git config --global user.email "<your email>"
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\publish.ps1
```

The script creates a private repository named `rea-vm` and pushes `main`.
Use `-Visibility public` only when the content is intended to be public.

## Structure

```text
SKILL.md
README.md
LICENSE
.gitignore
references/
  workflow.md
  environment-checks.md
  evidence-and-reporting.md
  troubleshooting.md
scripts/
  preflight_check.py
  preflight_check.ps1
  publish.ps1
templates/
  experiment-report.md
examples/
  example-config.yaml
```

## Safety

Use only on targets you are authorized to analyze. Prefer a disposable VM with
a snapshot. Never commit credentials, keys, private addresses, or sensitive
debug data. The skill reports blocked stages instead of fabricating results.

## License

No license is declared here. Add one only with the repository owner's explicit
decision.
