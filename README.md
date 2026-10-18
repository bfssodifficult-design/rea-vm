# rea-vm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![validate](https://github.com/bfssodifficult-design/rea-vm/actions/workflows/validate.yml/badge.svg)](https://github.com/bfssodifficult-design/rea-vm/actions/workflows/validate.yml)
[![release](https://img.shields.io/github/v/release/bfssodifficult-design/rea-vm)](https://github.com/bfssodifficult-design/rea-vm/releases)

`rea-vm` is the VM interface layer for REA. It gives an agent a controlled path
from REA static analysis to an authorized virtual machine, dynamic evidence,
IDA screenshots, and a structured report, without pretending that missing
tools worked.

## Why rea-vm

- **One contract, four stages.** Static analysis, VM access, dynamic evidence,
  and reporting stop being ad-hoc commands and become a repeatable pipeline.
- **Honest capability checks.** Missing SSH, IDA, or PaperJSX is reported as
  unavailable instead of being silently skipped or faked.
- **Evidence, not vibes.** Every runtime claim is tied to a command, a hash, a
  screenshot, or an explicit "unverified" label.

## Quick start

```bash
git clone https://github.com/bfssodifficult-design/rea-vm.git
cp -r rea-vm ~/.codex/skills/rea-vm
python ~/.codex/skills/rea-vm/scripts/preflight_check.py --json
```

Then invoke `$rea-vm` in a Codex session. Start from
`examples/example-config.yaml` and replace every placeholder.

## Demo

```text
$ python scripts/preflight_check.py --json
{"capabilities":[{"name":"rea","status":"supported"},
                 {"name":"ssh","status":"supported"},
                 {"name":"ida_mcp","status":"unavailable"},
                 {"name":"paperjsx","status":"unavailable"}], ...}

$ # REA static finding -> VM probe -> evidence -> report
$ python scripts/preflight_check.py --config my-lab.yaml --json
```

A 60-second screen recording (REA -> VM -> IDA -> report) is planned under
`docs/launch/`. Until then, the command transcript above is the honest demo.

## Who it is for

- Reverse engineers who already use REA and need a VM execution path.
- Malware and detection engineers who must separate static claims from real
  runtime observations.
- Teams that want auditable evidence and reproducible VM experiments.

## Overview / 简介

**English** - `rea-vm` is an AI Agent Skill for VM-assisted reverse engineering with REA. It guides the agent through connecting REA static analysis with an authorized virtual machine, collecting and verifying dynamic evidence and genuine IDA screenshots, and producing evidence-graded reports using PaperJSX or Markdown, subject to the available tools and environment.

**中文** - `rea-vm` 是一个用于 REA 虚拟机辅助逆向分析的 AI Agent Skill。它指导 Agent 将 REA 静态分析与授权的虚拟机环境相结合，采集并核验动态分析证据和真实的 IDA 截图，并根据可用工具和运行环境，通过 PaperJSX 或 Markdown 生成带有证据等级标注的分析报告。

**日本語** - `rea-vm` は、REA を用いた仮想マシン支援型リバースエンジニアリングのための AI Agent Skill です。利用可能なツールと実行環境に応じて、REA の静的解析と許可された仮想マシン環境を連携させ、動的解析の証拠と実際の IDA スクリーンショットの収集・検証を支援し、PaperJSX または Markdown による証拠レベル付きレポートの作成をガイドします。

**Español** - `rea-vm` es una Skill para agentes de IA orientada al análisis inverso asistido por máquinas virtuales con REA. Guía al agente para integrar el análisis estático de REA con una máquina virtual autorizada, recopilar y verificar evidencias dinámicas y capturas reales de IDA, y elaborar informes con niveles de evidencia mediante PaperJSX o Markdown, según las herramientas y el entorno disponibles.

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
