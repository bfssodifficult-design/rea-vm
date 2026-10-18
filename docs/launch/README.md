# Launch Checklist

Goal: make the value visible in under 60 seconds, then let real users verify it.

## Before launch

- [ ] A 45-90 second screen recording: REA finding -> preflight -> VM probe ->
      IDA screenshot -> report. No credentials, no real target IPs.
- [ ] A short "what this is / is not" paragraph in the README.
- [ ] `python scripts/preflight_check.py --json` works on a clean machine.
- [ ] Release `v0.1.0` with notes and a source zip.
- [ ] Topics: `agent-skill`, `reverse-engineering`, `rea`, `vm`,
      `malware-analysis`, `ida`, `ghidra`, `dynamic-analysis`,
      `security-tools`, `paperjsx`.
- [ ] Issue templates and CI validation are green.

## Launch sequence

1. **Day 1 (English):** X/Twitter thread, LinkedIn post, one relevant Reddit
   community (read its rules first).
2. **Day 1 (Chinese):** 知乎/V2EX/即刻, with a Chinese demo transcript.
3. **Day 2:** Show HN, if the demo is ready and the README answers "why".
4. **Week 1:** submit to 2-3 awesome lists with a one-line description.
5. **Week 2:** publish a short technical post: "How to keep static claims and
   runtime claims separate in REA workflows".

## Metrics that matter

- clones and unique visitors, not only stars
- issues that ask for a capability (real demand)
- successful preflight runs reported by users
- inbound PRs that add a provider or a failure case

## What not to do

- Do not mass-post identical text to unrelated communities.
- Do not claim "full automation" or "EDR bypass".
- Do not publish a demo with real customer data or credentials.
