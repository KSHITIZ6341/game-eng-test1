# Reaper Engine Community Guidelines  
_A practical code‑of‑conduct for an open‑source game‑engine project (v0.2, no‑emoji edition)_

These rules keep our dev scene collaborative and focused on shipping frames per second—not flame wars.

---

## 1. Respect the Players (That’s Us)
- No hate, no harassment, no slurs. We frag bugs, not people.  
- Healthy technical debates are welcome; personal attacks are not.

## 2. Fix Code, Not Characters
- Review pull requests with specifics (“this matrix multiply adds 3 ms”) not ad‑hominem comments.  
- If you rewrite major sections, explain why in the PR description.

## 3. Document and Test
- A new API with no docstring is like a level with no lighting—unplayable.  
- Add at least one unit test or demo scene for new features so others can run and verify.

## 4. Keep Assets Legal
- Commit only models, textures, or sounds that you own or that are CC0/CC‑BY compatible.  
- Large binary files (>20 MB) belong in a separate release or sample repository to keep `git clone` slim.

## 5. Commit Message Format
Body (optional):

what changed

why it matters

Examples:  
`render: fix NaN in PBR shader`  
`ecs: add system priority ordering`

## 6. No Unsolicited Ads
- Job postings, token sales, or “buy my asset pack” belong elsewhere.  
- Relevant links in context are fine.

## 7. Report Issues with Repro Steps
Incomplete: “It crashes”  
Actionable: “`mesh.draw()` crashes when vertex_count == 0; stacktrace below”

Use the issue template, attach minimal test assets if needed.
