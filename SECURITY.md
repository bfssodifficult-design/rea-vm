# Security Policy

## Scope

`rea-vm` is an orchestration skill. It does not contain exploits, payloads, or
credentials. Security-relevant areas include:

- credential handling in SSH/VM workflows
- unsafe command construction
- evidence paths that could leak local data
- misleading "success" states

## Reporting

Please report suspected issues privately to the repository owner rather than
opening a public issue. Include the affected file, a minimal reproduction, and
the impact.

## Safe use

Only use the skill against systems you are authorized to analyze. Prefer
disposable VMs and snapshots. Never commit keys, tokens, or personal data.
