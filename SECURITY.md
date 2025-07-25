# Security Policy

## Supported Versions

| Version | Status      | Supported Until |
|---------|-------------|-----------------|
| 0.1.x   | **Current** | Next minor bump |
| < 0.1   | End‑of‑life | —               |

Only the latest tagged **minor** release receives security fixes.  
Nightly / main branch is best‑effort; update to the latest tag before filing a report.

---

## Reporting a Vulnerability

1. **Do not create a public issue or pull request.**  
2. Email the maintainers at **security@reaper‑engine.org**  
   - Use the subject line `[SECURITY] <short description>`  
   - Include version, platform, reproduction steps, and if possible a minimal test asset or patch.  
3. You will receive an acknowledgment within **48 hours**, and a more detailed response within **14 days**.  
4. We prefer **encrypted reports**. Retrieve the PGP key here:  
   `https://reaper-engine.org/pgp/security.asc`

---

## Disclosure Process

1. Triage and confirm the vulnerability.  
2. Assign a CVE (or internal ID if CVE not appropriate).  
3. Develop a fix and prepare a patched release.  
4. Coordinate an embargo period (typically up to 30 days) if the issue is severe.  
5. Publish:  
   - Updated release on GitHub / PyPI  
   - Security advisory in `SECURITY.md` and GitHub advisories  
   - Credit to the reporter (unless anonymity requested)

---

## Scope

_What’s covered_  
- Engine runtime (C‑Python code, WGSL shaders)  
- Default demo assets / scripts  
- Build and packaging scripts

_Not covered_  
- Third‑party dependencies (report upstream if appropriate)  
- User‑generated code or assets built with Reaper Engine  
- Forks or unofficial binary distributions

---

## Preferred Languages

We can respond in **English**.

Thank you for helping keep Reaper Engine users safe.
 