# Workflow Contracts

Each phase has an input, an output, and an explicit failure path. A phase that
cannot run must emit a status and a diagnosis; it must not silently disappear
from the report.

## Phase A - Scope

Inputs: user request, existing config, workspace conventions.

Outputs:

- target identity and expected hash
- analysis question and falsifier
- authorization statement and boundaries
- VM identity, snapshot, and access method
- evidence root and report format

Failure path: missing authorization or an ambiguous target stops execution.
Static-only work may continue if it stays inside scope.

## Phase B - Preflight

Inputs: parameters from Phase A.

Outputs: `metadata/capabilities.json` with one record per dependency:

```json
{
  "name": "ssh",
  "status": "supported",
  "evidence": "absolute path resolves; read-only login returned exit 0",
  "limitations": []
}
```

Checks are read-only. Do not start drivers, install packages, or modify boot
configuration here.

Failure path: blocking dependency -> stop the dependent phase; optional
dependency -> choose a documented fallback.

## Phase C - REA static analysis

Inputs: target path, provider candidates.

Process:

1. Call `binary_session` with an empty object and read provider availability.
2. Open the target with `open_binary`; pass an explicit provider only when the
   user requires it and it is available.
3. Use focused operations (`binary_overview`, `list_segments`,
   `search_procedures`, `analyze_function`, `procedure_pseudo_code`).
4. Record Evidence IDs and the exact target digest.

Outputs: provider identity, analysis profile, findings, Evidence IDs, and
testable hypotheses.

Failure path: provider unavailable -> state it; do not invent a provider.
Static-only results remain valid but cannot support runtime claims.

## Phase D - SSH and VM

Inputs: host, user, key path, expected OS, and authorized actions.

Process:

1. Resolve the real SSH binary; reject wrappers that return fixed text.
2. Run a read-only command and capture exit status.
3. Probe guest OS, architecture, shell, privileges, and required tools.
4. Transfer files with SFTP/SCP; verify SHA-256 on both sides.
5. Prefer file-based scripts over long inline commands.

Outputs: channel evidence, guest inventory, transfer hashes.

Failure path: connection refused/timeout -> distinguish listener, auth, and
network causes; do not retry blindly. If a hypervisor console is the only
channel, record that deviation.

## Phase E - Dynamic analysis

Inputs: hypotheses, VM state, available debuggers, snapshot.

Process:

1. Confirm the snapshot exists before state-changing steps.
2. Translate each hypothesis into a probe, breakpoint, or functional check.
3. Run a baseline, a negative control, the target transition, and a restore
   check where applicable.
4. Capture tool output and timestamps; separate observation from inference.
5. Stop at the first unsafe condition (real security product, production
   volume, missing rollback).

Outputs: ordered observations, raw logs, and a list of unverified items.

Failure path: no debugger -> use supported observation or stop; missing
snapshot -> stop before driver/boot changes.

## Phase F - IDA evidence

Inputs: addresses/functions mapped from REA or dynamic findings.

Process:

1. Discover the actual IDA surface: REA `ida` provider, `ida-pro-mcp`, or the
   IDA application itself.
2. If using headless IDA, verify the script executed and the output file
   exists before citing it.
3. If using GUI screenshots, capture the real application window from the same
   interactive session and verify the image is non-empty.
4. Record path, time, address/function, and the claim the evidence supports.

Outputs: verified decompiler/disassembly output and/or real screenshots.

Failure path: no screenshot capability -> use text evidence and label it as
text; never synthesize an image.

## Phase G - Evidence normalization

Inputs: outputs from C-F.

Process:

1. Create the evidence tree.
2. Hash every artifact.
3. Build an index with claim -> evidence -> status.
4. Keep negative and blocked results.

Outputs: `evidence/index.json` or `evidence/INDEX.md`.

Failure path: missing artifact -> mark the claim unsupported.

## Phase H - Report

Inputs: normalized evidence and the report format.

Process:

1. Probe PaperJSX tools/packages.
2. Build the JSON payload for the installed version.
3. Generate and validate the artifact (exists, non-zero, opens, referenced
   assets resolve).
4. If PaperJSX is unavailable, render the Markdown template and mark the
   degradation.

Outputs: final report path plus a validation record.

Failure path: schema mismatch -> fix the exact field path reported by the
validator; do not guess aliases.

## Phase I - Cleanup

Inputs: VM state, temporary files, running services.

Process:

1. Revert or stop test services.
2. Remove one-time tasks and temporary credentials.
3. Preserve samples and evidence.
4. Run skill structure checks.

Outputs: cleanup record and final handoff.

Failure path: cannot clean safely -> report the residual state and the exact
recovery action.
