# Troubleshooting

These are failure modes observed in real REA/VM sessions. Diagnose the symptom
before changing configuration.

## SSH

### Every command returns the same literal text

Symptom: `whoami` returns something like `off\exit /b 1`.

Cause: `ssh` on `PATH` resolves to a wrapper/shim, not the real client.

Fix: resolve the real binary (`C:\Windows\System32\OpenSSH\ssh.exe`,
/usr/bin/ssh) and call it by absolute path. Verify with `-V`.

### Port open but exec kills the listener

Symptom: SFTP works, then SSH times out after an exec attempt; the service log
shows no new start.

Fix: check for a stale foreground `sshd` or a scheduled task that is already
running. Stop all instances and restart the task/service. Verify the TCP
listener, not just the service state.

### Windows scheduled task says success but nothing starts

Symptom: `SUCCESS: Attempted to run` but no new process or log line.

Cause: an instance is already running, or the task is stale.

Fix: stop/delete the task, re-register, then run it. Check the task action,
working directory, and last result.

### Inline command quoting breaks

Symptom: PowerShell sees stray braces, `/encodedCommand`, or split arguments.

Fix: upload a `.ps1`/`.cmd`/`.sh` file and execute it by path. Keep inline
commands to a single simple verb.

## VM and hypervisor

### Encrypted VM blocks `vmrun`

Symptom: `vmrun` asks for a password or refuses to open the VMX.

Fix: use the GUI for snapshot/screenshot operations, or supply the encryption
password through an approved local mechanism. Never print it.

### Suspend/resume keeps drivers loaded

Symptom: after "power on", previously loaded demand-start drivers still show
RUNNING.

Cause: the VM was resumed, not rebooted.

Fix: perform a full guest reboot before claiming a clean state; verify service
states.

### Driver file is locked during rebuild

Symptom: linker cannot write `*.sys`.

Cause: the driver is still loaded.

Fix: stop the service if it supports unload, otherwise reboot. A driver
without `DriverUnload` cannot be replaced in place.

## IDA and IDAPython

### `LoadLibrary(...idapython3.dll) failed`

Cause: the plugin exists but its Python dependencies are not on the DLL search
path.

Fix:

```text
cd <IDA dir>
copy python311\python3.dll .
copy python311\python311.dll .
copy python311\vcruntime140.dll .
copy python311\vcruntime140_1.dll .
init_idapython.bat   (runs idapyswitch --force-path ./python311/python3.dll)
```

Verify in IDA Output: a Python version and `IDAPython ... final`.

### `-S` script does not run in GUI mode

Symptom: no output file, no message; the GUI is open.

Fix: use `-A -S<path>` for headless execution, or drive the GUI with a real
interactive automation path. Do not assume the script ran.

### `-S"<path>"` is treated as an input file

Symptom: `unknown file extension`.

Fix: use the attached form `-S<path>` without quotes when the path has no
spaces.

### Database dialogs block automation

Symptoms: "Database ... is not closed", "Load a new file", "Please confirm".

Fix: handle them explicitly, or start from a fresh input copy and delete stale
`.id0/.id1/.id2/.nam/.til` files. Never assume a dialog was dismissed.

### Function not found at the expected address

Symptom: `get_func()` returns none; decompilation returns none.

Cause: auto-analysis did not define a function at that address.

Fix: `ida_funcs.add_func(ea)`, then `get_func` and
`ida_hexrays.decompile_func`. Record the manual boundary creation.

## Memory images

### Disassembler reads wrong bytes

Cause: a memory image stores sections at RVAs, but the PE header still points
to on-disk file offsets.

Fix: in a copy, set `PointerToRawData = VirtualAddress` and
`SizeOfRawData = VirtualSize` for each section. Keep the original untouched.

### Protected section is all zero

Interpretation: the stub released or wiped the section after initialization.
This is a finding, not evidence that the payload was empty. Capture earlier
(before init completes) if the payload is required.

## Screenshots

### Black VM console

Cause: hardware/D3D surface not captured by GDI.

Fix: capture inside the guest's interactive session, use window capture, or
use the hypervisor's screenshot API.

### Capture process cannot see the window

Cause: the capture runs in a different session/window station.

Fix: run the capture from an interactive task in the target session.

## PaperJSX

- GitHub API 403: rate limit or policy. Retry later or use the repository page.
- Package missing: use the MCP server if connected, otherwise Markdown
  fallback.
- Schema error: read the exact field path from the validator; do not guess.
