# Technical Report: <TARGET NAME>

Date: <YYYY-MM-DD>  
Target: `<sha256>`  
Analysis: REA static analysis + authorized VM dynamic validation  
Evidence levels: static direct, real runtime observation, mechanism-equivalent, unverified

## Abstract

<Question, method, strongest result, and the limits of what was proven.>

## 1. Scope and authorization

- Authorized by: <operator / policy reference>
- Target: <path and hash>
- VM: <host / snapshot / isolation>
- Explicitly out of scope: <production systems, real security products, ...>

## 2. Environment

| Item | Value | Evidence |
|---|---|---|
| Host OS | <...> | `metadata/capabilities.json` |
| Guest OS/build | <...> | `<dynamic/guest-info.txt>` |
| REA version | <...> | `<static/provider.json>` |
| IDA version | <...> | `<screenshots/ida.png>` |
| PaperJSX version | <...> | `<report/validation.json>` |

## 3. Target identity

| Property | Value |
|---|---|
| Path | `<...>` |
| SHA-256 | `<...>` |
| Size | `<...>` |
| Type | `<...>` |

## 4. Method

1. REA static analysis -> hypotheses.
2. VM preflight -> capability matrix.
3. Authorized execution with snapshot.
4. Dynamic probes and evidence capture.
5. IDA mapping and real screenshots.
6. Evidence grading and report generation.

## 5. Static findings

### 5.1 <Finding>

Observation:

```text
<evidence excerpt>
```

Evidence: `<Evidence ID / path>`  
Level: static direct

## 6. VM and dynamic observations

### 6.1 Setup

```text
<commands, service states, snapshot>
```

### 6.2 Observation

```text
<raw output>
```

Evidence: `<path>`  
Level: real runtime observation

## 7. IDA analysis

![<caption>](screenshots/<file>.png)

- Application: <IDA version / IDA MCP>
- Address/function: `<address>`
- Capture time: `<timestamp>`
- Supports claim: <claim>

## 8. Evidence grading

| Claim | Level | Evidence |
|---|---|---|
| <claim> | verified fact | `<path>` |
| <claim> | strong inference | `<path>` |
| <claim> | unverified | - |

## 9. Limitations

1. <blocked stage and reason>
2. <tool unavailable>
3. <not executed>

## 10. Defensive implications

<Detection ideas, baselines, negative controls.>

## 11. Reproduction

```text
<minimal commands / configuration>
```

## 12. Cleanup

- Snapshot reverted: <yes/no>
- Services stopped: <list>
- Temporary tasks removed: <list>
- Test signing left enabled: <yes/no; VM-only>

## Appendix: evidence index

| Artifact | SHA-256 | Purpose |
|---|---|---|
| `<path>` | `<hash>` | <purpose> |
