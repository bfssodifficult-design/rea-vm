# Evidence and Reporting

## Evidence levels

1. **Static direct evidence** - code, constants, imports, or call chains from
   the artifact. Does not prove execution.
2. **Real runtime observation** - a tool or kernel actually produced the state
   change, with the exact object and command recorded.
3. **Mechanism-equivalent evidence** - a self-owned canary exercises the same
   primitive. Supports the mechanism, not the real target's behavior.
4. **Unverified** - no direct static or runtime evidence, or a step was
   blocked.

Every report claim carries one of these labels. Never merge levels to make a
result look stronger.

## Screenshot rules

A screenshot is evidence only when it is a real capture of the application
state that supports the claim.

- Capture the actual window or screen from the session where the application
  runs.
- A black frame, an empty console, a desktop-only image, or a synthetic
  rendering is not a substitute.
- For D3D/overlay windows, try window capture (`PrintWindow`) and, if needed,
  run the capture inside the interactive session.
- Record: file path, capture time, application, address/function, and purpose.
- Validate: file exists, non-zero, expected dimensions, and visually contains
  the claimed content.

If only text is available (for example, a headless decompiler), cite it as
text with the exact command. Do not label text as a screenshot.

## Memory images

- Record module base, image size, source process/kernel, and dump method.
- A PE memory image is RVA-addressed. Before loading it in a disassembler,
  patch each section's `PointerToRawData` to its `VirtualAddress` (and
  `SizeOfRawData` to `VirtualSize`) in a copy; keep the original.
- Verify section entropy and compare `.text` with the on-disk file.
- A zeroed protected section is a finding (release/anti-dump), not proof that
  the payload was empty.

## IDA-specific evidence

- Headless: verify the script ran, the output file exists, and the requested
  address/function was actually resolved.
- If the function is not defined by auto-analysis, create it explicitly before
  decompiling; record that step.
- GUI: capture the real IDA window. If the automation cannot run the GUI
  script, do not claim a GUI result.
- Distinguish disassembly, pseudocode, and raw memory views.

## Report content

Minimum sections:

1. Purpose and question
2. Scope and authorization
3. Environment and versions
4. Sample identity and hashes
5. Method
6. Static findings
7. VM and dynamic observations
8. IDA analysis and screenshots
9. Results and evidence grading
10. Limitations and blocked stages
11. Detection or defensive implications
12. Reproduction and cleanup
13. Evidence index

## PaperJSX

Probe before generating:

- MCP mode: call the actual `generate_report*` tool with validated JSON.
- Package mode: import `@paperjsx/json-to-pdf` (or docx/pptx) and render.

Rules:

- Validate JSON against the installed schema; fix the exact field path on
  error.
- Do not invent components or aliases.
- Confirm the output file exists, is non-zero, opens, and references existing
  images.
- If unavailable, use `templates/experiment-report.md` and state
  "PaperJSX unavailable; Markdown fallback".

## Honesty checklist

- [ ] Every screenshot path was checked.
- [ ] Every cited command was actually run.
- [ ] Every "verified" claim has a matching artifact.
- [ ] Blocked and unverified items are visible.
- [ ] No credentials, keys, or personal paths are included.
