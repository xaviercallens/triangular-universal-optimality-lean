# Changelog

## v0.1.0: red-team round 1 (2026-10-11), pre-release

The first public release, opened for red-team review by citizen scientists. It is not peer reviewed.

- **Lean 4 corollaries** of openai/math `OAI.AtomicTriangular.universal_energy_minimum` (pinned at `adc7f124`; the
  triangular files are identical at `fd4aeeb2`, which was still upstream HEAD on release day):
  - D1 Riesz optimality;
  - D1b finiteness for `s > 2`;
  - D2 every density;
  - D3 CKMRV-style universal optimality (lower energy) and vacancy non-uniqueness;
  - D4 open disks, including the hypothesis-free identities in `OpenDiskAny.lean`.
- **Clean rebuild of every module** against the pinned stack, with stale oleans removed and the axiom gate passing
  (`verification/rebuild_2026-10-11/`). The sha256 of upstream's challenge file matches the audited one.
- **Verification material:**
  - four independent AI-agent verification reports (D1, D2, D3, D4);
  - the statement-fidelity audit and the manuscript audit;
  - preregistrations and the claim ledger;
  - the axiom audits (`Axioms.lean`, plus the supplementary `AxiomsD4.lean`) with planted controls.
- **Red-team setup:** targets T1–T7, issue templates, a public log, and provenance.
- **Fixed since the first public commit `064cfa9`:** `OpenDiskAny.lean` was missing, so `Axioms.lean` did not compile
  from the repo. Our own rebuild caught this before the release.

**Known open items at release:**
- Three outdated docstrings in `UniversalOptimality.lean` (see RED_TEAM_LOG).
- No rebuild from a fresh clone on another machine.
- Only a first-pass literature search ([LITERATURE.md](LITERATURE.md)); no systematic review yet.
- No human has checked statement fidelity.
