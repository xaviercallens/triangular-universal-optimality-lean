# Changelog

## v0.2.0: physical use case on real data (2026-10-11), pre-release

- **`physics/`: real-data consistency check (Tier X) of the D2 energy bound.** The data are measured skyrmion-lattice
  positions from Zenodo doi:10.5281/zenodo.4450305 (CC-BY-4.0; arXiv:2004.09244), downloaded with an md5 check.
  - **P2 (Voronoi density estimator): gate PASS.** Both snapshots (1,618 and 4,224 skyrmions) lie above the
    triangular-lattice bound for all seven completely monotone potentials, with every gap above tolerance.
  - The controls reproduce theory: square vs triangle is +4.2% for Riesz s = 4, against 4.21% from closed forms.
  - The earlier P1 (preregistered) and P1b (post-hoc) runs failed their control-sensitivity gates. They are kept
    unchanged and still reproduce exactly.
  - Every run was preregistered before it ran; the commit order is the audit trail.
- **D3 docstrings corrected** in `UniversalOptimality.lean`, with an in-place Disclosure note; statements and proofs
  are unchanged. This closes the v0.1.0 open item. The file now differs from the Zenodo and LeanMaster v3.48.1 copies
  in comments only.
- **Clean rebuild of every module, axiom gate PASS:** `verification/rebuild_v0.2.0/`.

**Not claimed:** the physical check does not validate the upstream theorem. Perturbed triangular lattices are already
predicted to lie above the bound by lattice-only and local optimality.


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
