# Environment Checks

Preflight is read-only and runs on every invocation. It answers "what can this
host actually do right now", not "what was true when the skill was written".

## Running the probe

```bash
python scripts/preflight_check.py --json
python scripts/preflight_check.py --config examples/example-config.yaml --json
```

Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\preflight_check.ps1
```

The probe prints JSON. It never prints secrets. A missing value is `unknown`,
not a default.

## Status semantics

| Status | Meaning |
|---|---|
| supported | Present and exercised by a read-only check |
| unsupported | Present but incompatible with this host/OS |
| unavailable | Not installed or not configured |
| unknown | Probe could not establish state |

Never promote `unknown` to `supported` by assumption.

## Host

- OS, release, architecture, Python version, shell.
- Current directory and Git worktree state when inside a repository.
- Existence and writability of the evidence root.

## REA

- `rea` on `PATH`, or a pinned `npx rea-agents@<version>`.
- MCP session reachable and `binary_session` returns provider candidates.
- Provider availability: static, Ghidra, IDA, managed, artifact, Frida, etc.
- `REA_IDA_MCP_CONFIG` or equivalent registration; note that a configured
  provider can still be `unknown` until opened.

## SSH

- Resolve `ssh` and `sftp` with absolute paths.
- Detect wrappers: a tiny script/batch file that emits fixed text is not a
  client. Verify with `--version` or a read-only login.
- Check key file existence and permissions without printing the key.
- Optional: probe the configured host and port with a short timeout.

## VM

- Hypervisor CLI presence (`vmrun`, `VBoxManage`, `virsh`).
- VMX/config path and whether it is encrypted.
- Snapshot inventory; a snapshot without memory may not be enough for a
  driver experiment.
- Disk space for dumps and snapshots.

## IDA

- `ida64.exe`/`idat64`/`ida` paths.
- IDA version and the Python runtime it ships (`python311`, etc.).
- Plugin presence: `idapython3.dll`, `mcp-plugin.py`.
- `ida-pro-mcp` package and compatible `mcp` version (the bridge may require
  `mcp<2`).
- Whether `REA_IDA_MCP_CONFIG` points at a command or URL.
- Screenshot capability: GUI capture, MCP image export, or none.

## Debuggers

- `cdb`, `windbg`, `kd`, `gdb`, `lldb`, `x64dbg`, `rizin`, `frida`.
- Kernel debugging prerequisites: test signing, boot config, transport.

## PaperJSX

- MCP tools connected (`generate_report`, `generate_report_docx`, ...).
- Or npm packages `@paperjsx/json-to-pdf|docx|pptx` resolvable locally.
- Node/npm versions.
- Output directory writability.

## Output contract

```json
{
  "host": {"os": "...", "arch": "...", "python": "..."},
  "capabilities": [
    {"name": "rea", "status": "supported", "evidence": "..."},
    {"name": "ssh", "status": "unavailable", "evidence": "PATH shim only"}
  ],
  "blocking": ["ssh"],
  "optional": ["paperjsx"],
  "limitations": ["IDA MCP not configured; IDA application present"]
}
```

Store this as `<evidence>/metadata/capabilities.json` and cite it in the
report.
