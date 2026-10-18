# Distillation Design

This skill was distilled from a real REA + Windows VM session. The goal is to
keep the reusable decisions and remove the sample-specific data.

## Sources actually read

- The active Codex session history: tool calls, outputs, errors, and fixes.
- The prior REA technical report and validation results in the lab workspace.
- Local environment probes: REA CLI, MCP provider list, IDA/IDAPython
  installation, SSH client resolution, VMware process state, PaperJSX package
  discovery.
- The PaperJSX GitHub README and skill description (document-generation
  semantics), not a local PaperJSX installation.

## Generic capabilities extracted

| Capability | Why it is generic |
|---|---|
| Runtime capability matrix | Every environment differs; state must be probed. |
| Real-SSH resolution | Wrappers and shims silently break automation. |
| File-based remote scripts | Inline quoting is fragile across shells. |
| Snapshot-gated execution | Driver/boot work needs rollback. |
| Memory image normalization | RVA layout must be fixed before disassembly. |
| Headless IDA verification | Script success must be proven by output files. |
| Evidence grading | Static, runtime, mechanism-equivalent, and unverified differ. |
| Report degradation | PaperJSX may be absent; Markdown fallback is honest. |

## Sample-specific values excluded

The skill intentionally contains none of:

- sample hashes or filenames
- VM IP addresses, usernames, key paths, or VMX paths
- function addresses, module bases, section sizes, or IOCTL values
- device names, symbol links, or authentication blobs
- captured command output from the original target

The example configuration uses documentation addresses and placeholders.

## Optional modules

- REA static analysis (required when the task is REA-driven)
- SSH/VM execution (optional if static-only)
- Dynamic debugging (optional; depends on debugger and authorization)
- IDA/IDA MCP screenshots (optional; text evidence is allowed with labeling)
- PaperJSX reporting (optional; Markdown fallback)

## User configuration

All target, VM, evidence, timeout, and report values are configuration. The
skill never silently substitutes a default host, user, key, or path.

## Deliberately not encoded

- Any target-specific exploit, bypass, or capability-building step.
- Any instruction to weaken a real security product or production system.
- Any claim that a specific tool is always present.
- Any auto-run behavior: the skill requires explicit invocation.
