# Launch Copy

Replace `<link>` with the repository URL. Keep the safety sentence.

## X / Twitter (English)

```text
Published rea-vm: a VM interface layer for REA.

Static analysis -> authorized VM -> dynamic evidence -> IDA screenshots -> graded report.

It probes what is actually available and says "unavailable" instead of faking a result.

MIT. Authorized, disposable VMs only.
<link>
```

## X / Twitter (Chinese)

```text
开源了 rea-vm：给 REA 的虚拟机接口层。

静态分析 -> 授权 VM -> 动态证据 -> IDA 截图 -> 分级报告。

缺 SSH / IDA / PaperJSX 会明确报 unavailable，不会伪造成功。

MIT，仅用于授权的一次性虚拟机。
<link>
```

## LinkedIn

```text
Most reverse-engineering workflows break at the handoff between static
analysis and a real VM. rea-vm makes that handoff explicit: capability probe,
authorized SSH/VM access, dynamic evidence, IDA screenshots, and a report that
separates verified facts from unverified hypotheses.

It is intentionally honest about missing tools: unsupported or unavailable
stages are reported, not hidden.

Open source, MIT, for authorized and disposable environments.
<link>
```

## Show HN

```text
Show HN: rea-vm - a VM interface layer for REA workflows

I kept rebuilding the same glue between REA static findings and a Windows VM:
probe SSH, snapshot, run a probe, capture evidence, then write a report that
does not overclaim.

rea-vm packages that glue as an Agent Skill with a runtime capability matrix.
It reports unsupported/unavailable instead of pretending. The report layer can
use PaperJSX or fall back to Markdown.

It is for authorized, disposable VMs only. Feedback on the capability model
and evidence grading is welcome.
<link>
```

## Reddit (r/ReverseEngineering)

```text
Title: rea-vm: a VM interface layer for REA (capability checks + graded evidence)

I published a small skill that connects REA static analysis to an authorized
VM, captures dynamic evidence and IDA screenshots, and produces a report that
labels verified facts vs unverified hypotheses.

It is deliberately conservative: missing SSH/IDA/PaperJSX is reported as
unavailable. No exploit content, no production targets.

Docs and preflight script: <link>
```

## 知乎 / V2EX（中文）

```text
标题：把 REA 的静态结论送进虚拟机：rea-vm 开源

做逆向时最费时间的往往不是分析本身，而是从“静态看起来会这样”到“运行时
确实这样”的那段胶水：连 VM、打快照、跑探针、截 IDA、写报告。

rea-vm 把这套流程做成一个 Agent Skill：先探测能力矩阵，再按需连接授权的
VM，动态取证、IDA 截图，最后生成分级报告。缺工具会明确写 unavailable，
不会伪造成功。

MIT，仅用于授权的一次性虚拟机。仓库：<link>
```
