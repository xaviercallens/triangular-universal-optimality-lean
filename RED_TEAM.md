# Red-team review: please try to break this

**Round 1 (citizen scientists): open now, running about four weeks from the first public post.**
**Round 2 (Lean and mathematics community): after round 1 fixes are in.**

Breaking a claim is the most useful thing you can do here. A report that turns out to be wrong still helps, because
it shows where the explanation is unclear. You do not need to know Lean to contribute: targets T1, T3 and T6 mostly
need careful reading.

## Targets, roughly from most to least likely to find something

| ID | Target | What a "hit" looks like | Where to look |
|---|---|---|---|
| **T1** | **Statement fidelity.** Do upstream's definitions mean what Cohn–Kumar / CKMRV mean? | A row of `verification/statement_fidelity.md` marked "yes" that is actually a mismatch, such as the density notion, the energy normalisation, centred disks, `ℝ≥0∞` junk values, `C^∞` vs completely monotone, or the lattice scaling. | upstream `OAI/Analysis/Triangular/Energy/Basic.lean`, CKMRV §1 |
| T2 | **D3's definition.** Is `UniversallyOptimal` a fair reading of CKMRV Def. 1.3, apart from the stated liminf gap? | Another gap, or a witness that the liminf version is *strictly* weaker. | `lean/Triangular/UniversalOptimality.lean` |
| **T3** | **Overclaiming.** Any sentence in this repo, the Zenodo records or the posts that says more than the Lean proves. | A quote plus the weaker statement it should be. | everything |
| T4 | **Axiom or `sorry` leakage.** Anything besides the three standard axioms in a real theorem, or a proof that only goes through because of a junk value. | `#print axioms` output showing it. | `lean/Triangular/*.lean` |
| T5 | **Reproduction on another machine.** Fresh clone, pinned stack, every file compiles, and the audit output matches `verification/rebuild_2026-10-11/`. | A build failure, a different axiom list, or a stale-olean effect. | [BUILD.md](BUILD.md) |
| T6 | **Literature.** Is the 2D Cohn–Kumar conjecture still open apart from the upstream claim? Has anyone published an assessment of the upstream proof? | A citation. | arXiv, MathOverflow, Lean Zulip |
| T7 | **D4 scope.** Does the open/closed result say anything beyond upstream's centred-disk liminf observables? We say no. | A case where we overstate it, or a window convention under which it fails. | `lean/Triangular/OpenDisk*.lean`, `verification/D4/` |

Out of scope: checking the upstream proof line by line. The Lean kernel already accepted it. The question for
upstream is whether its *statement* means what it claims (T1).

## How to report

Open an issue using a template: **Statement mismatch** (T1, T2), **Reproduction or axiom problem** (T4, T5, T7) or
**Overclaim** (T3). For T6 a plain issue with links is fine. Please include exact file names, line numbers and tool
output. Do not paste output you did not run yourself.

## What happens to a report

Every report is recorded in [RED_TEAM_LOG.md](RED_TEAM_LOG.md) with one of these outcomes:

- **ACCEPTED, fixed:** the claim or text changed, and you are credited.
- **ACCEPTED, scope:** the limitation is now in LIMITATIONS.md.
- **DECLINED, with reason:** the report stays visible.

Reports that change a claim will be acknowledged by name (with your permission) in the next Zenodo version.

## Rules

Be kind and be specific. Attack claims, not people. AI-generated reports are welcome if you say so and have run any
tool output yourself.
