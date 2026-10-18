#!/usr/bin/env python3
"""Read-only capability probe for the REA VM analysis pipeline.

Prints a JSON capability matrix. Never prints secrets or key material.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path


def record(name, status, evidence, limitations=None, blocking=False):
    return {
        "name": name,
        "status": status,
        "evidence": evidence,
        "limitations": limitations or [],
        "blocking": blocking,
    }


def load_config(path):
    if not path:
        return {}
    text = Path(path).read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text) or {}
    except Exception:
        return minimal_yaml(text)


def minimal_yaml(text):
    """Parse the small nested key/value subset used by the example config."""
    root = {}
    stack = [(-1, root)]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.split(" #", 1)[0].strip().strip("'\"")
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value == "":
            child = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = value
    return root


def probe_ssh():
    candidates = []
    path_hit = shutil.which("ssh")
    if path_hit:
        candidates.append(Path(path_hit))
    for candidate in (
        r"C:\Windows\System32\OpenSSH\ssh.exe",
        "/usr/bin/ssh",
        "/bin/ssh",
        "/usr/local/bin/ssh",
    ):
        p = Path(candidate)
        if p.exists() and p not in candidates:
            candidates.append(p)

    real = None
    shim = None
    for p in candidates:
        try:
            size = p.stat().st_size
        except OSError:
            continue
        if p.suffix.lower() in (".bat", ".cmd") or size < 4096:
            shim = str(p)
            continue
        real = str(p)
        break

    if real:
        note = f"client={real}"
        if shim:
            note += f"; PATH shim ignored: {shim}"
        return record("ssh", "supported", note, [note] if shim else [])
    if shim:
        return record(
            "ssh",
            "unavailable",
            f"only wrapper found: {shim}",
            ["Resolve a real OpenSSH client by absolute path."],
            blocking=True,
        )
    return record("ssh", "unavailable", "ssh not found", [], blocking=True)


def probe_ida():
    home = os.environ.get("REA_IDA_HOME")
    candidates = []
    if home:
        candidates.append(Path(home))
    patterns = [
        "C:/Program Files/IDA*",
        "C:/Program Files (x86)/IDA*",
        "C:/Users/*/AppData/Local/Programs/IDA*",
        "/opt/ida*",
        "/Applications/IDA*",
    ]
    for pattern in patterns:
        for p in Path("/").glob(pattern.lstrip("/")) if pattern.startswith("/") else []:
            candidates.append(p)
    if os.name == "nt":
        for base in (
            Path("C:/Program Files"),
            Path("C:/Program Files (x86)"),
            Path.home() / "AppData/Local/Programs",
        ):
            if base.exists():
                candidates.extend(base.glob("IDA*"))
    if not candidates:
        return record("ida", "unavailable", "no IDA installation found")

    for root in candidates:
        exe = None
        for name in ("ida64.exe", "ida.exe", "idat64", "idat"):
            p = root / name
            if p.exists():
                exe = p
                break
        if not exe:
            continue
        plugin = root / "plugins" / "idapython3.dll"
        python_dll = root / "python3.dll"
        notes = [f"root={root}", f"exe={exe.name}"]
        if plugin.exists():
            notes.append("idapython plugin present")
        if python_dll.exists():
            notes.append("python3.dll in root")
        return record("ida", "supported", "; ".join(notes))
    return record("ida", "unavailable", "IDA directories found but no executable")


def probe_ida_mcp():
    config = os.environ.get("REA_IDA_MCP_CONFIG")
    try:
        import importlib.util

        spec = importlib.util.find_spec("ida_pro_mcp")
    except Exception:
        spec = None
    if spec:
        evidence = "python package ida_pro_mcp importable"
        if config:
            evidence += "; REA_IDA_MCP_CONFIG set"
        return record("ida_mcp", "supported", evidence)
    if config:
        return record(
            "ida_mcp",
            "unknown",
            "REA_IDA_MCP_CONFIG set but package not importable",
        )
    return record("ida_mcp", "unavailable", "package and config not found")


def resolve_path(value, base):
    p = Path(value)
    return p if p.is_absolute() else (base / p)


def probe_vm(config, base):
    vm = (config or {}).get("vm", {}) or {}
    host = vm.get("host") or os.environ.get("REA_VM_HOST")
    user = vm.get("user") or os.environ.get("REA_VM_USER")
    key = vm.get("key") or os.environ.get("REA_VM_KEY")
    vmx = vm.get("vmx") or os.environ.get("REA_VM_VMX")
    notes = []
    if host:
        notes.append(f"host={host}")
    if user:
        notes.append(f"user={user}")
    if key:
        notes.append(f"key={'present' if resolve_path(key, base).exists() else 'missing'}")
    if vmx:
        notes.append(f"vmx={'present' if resolve_path(vmx, base).exists() else 'missing'}")
    hypervisor = shutil.which("vmrun") or shutil.which("VBoxManage") or shutil.which("virsh")
    if hypervisor:
        notes.append(f"hypervisor={hypervisor}")
    if not notes:
        return record("vm", "unknown", "no VM parameters configured")
    return record("vm", "unknown", "; ".join(notes), ["State requires an actual probe."])


def probe_debuggers():
    found = [n for n in ("cdb", "windbg", "kd", "gdb", "lldb", "rizin", "frida") if shutil.which(n)]
    if found:
        return record("debuggers", "supported", "found: " + ", ".join(found))
    return record("debuggers", "unavailable", "no supported debugger on PATH")


def probe_paperjsx():
    node = shutil.which("node")
    if not node:
        return record("paperjsx", "unavailable", "node not found")
    locations = [Path.cwd() / "node_modules" / "@paperjsx"]
    if os.name == "nt":
        locations.append(Path.home() / "AppData/Roaming/npm/node_modules/@paperjsx")
    for loc in locations:
        if loc.exists():
            return record("paperjsx", "supported", f"node={node}; packages={loc}")
    return record(
        "paperjsx",
        "unavailable",
        "node present; no @paperjsx packages in cwd/global",
        ["Use MCP tools if connected, otherwise Markdown fallback."],
    )


def probe_evidence(config, base):
    root = (config or {}).get("evidence", {}).get("root")
    if not root:
        return record("evidence_root", "unknown", "evidence.root not configured")
    p = resolve_path(root, base)
    try:
        p.mkdir(parents=True, exist_ok=True)
        probe = p / ".write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return record("evidence_root", "supported", f"writable: {p}")
    except Exception as exc:
        return record("evidence_root", "unavailable", f"not writable: {exc}", blocking=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    base = Path(args.config).resolve().parent if args.config else Path.cwd()
    capabilities = [
        record("host", "supported", f"{platform.system()} {platform.release()} {platform.machine()}"),
        record("python", "supported", sys.version.split()[0]),
    ]

    rea = shutil.which("rea")
    if rea:
        capabilities.append(record("rea", "supported", f"cli={rea}"))
    else:
        capabilities.append(record("rea", "unknown", "rea CLI not on PATH; check MCP tools"))

    capabilities.extend(
        [
            probe_ssh(),
            probe_ida(),
            probe_ida_mcp(),
            probe_vm(config, base),
            probe_debuggers(),
            probe_paperjsx(),
            probe_evidence(config, base),
        ]
    )

    blocking = [c["name"] for c in capabilities if c["blocking"]]
    optional = [c["name"] for c in capabilities if c["status"] in ("unavailable", "unknown") and not c["blocking"]]
    result = {
        "host": {
            "os": platform.system(),
            "release": platform.release(),
            "arch": platform.machine(),
            "python": sys.version.split()[0],
        },
        "capabilities": capabilities,
        "blocking": blocking,
        "optional": optional,
        "limitations": [
            "This probe is read-only; unknown states require an actual stage test.",
        ],
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
