# Changelog

## v0.3.0: physicist guide and tool for your own data (2026-10-11), pre-release

- **Physicist guide, `docs/physicist_guide/guide.pdf` (6 pages, TeX source included).**
  - The bound in physics language, and which interactions it covers, with tiers.
  - Exact floor values: Epstein-zeta closed forms and theta series.
  - The evidence status, the numerical improvement (box count vs Voronoi, Figure 1), the estimator against exact
    theory (Figure 2) and the skyrmion case study (Figure 3).
  - Every number and figure is generated from `physics/results/` by `make_figures.py`; `build.sh` rebuilds the PDF.
- **`physics/ubound.py`: test the bound on any 2D point file.**
  - Uses the P2 Voronoi estimator and controls C1–C4, and gives each potential a verdict.
  - Supports Gaussian and Riesz (Tier A) and Yukawa (Tier C, labelled as such).
  - `--self-test` passes: the square-vs-triangle gap for Riesz s = 4 is 0.0421, against 0.0421 from closed forms.
  - On the skyrmion data it reproduces the P2 gaps exactly.
- **Correction.** The skyrmion counts are 1,619 and 4,225; v0.2.0 docs said 1,618 and 4,224. The data files and all
  results JSON were always right. The P1 preregistration text keeps the old numbers as a historical record.


## v0.2.0: physical use case on real data (2026-10-11), pre-release

- **`physics/`: real-data consistency check (Tier X) of the D2 energy bound.** The data are measured skyrmion-lattice
  positions from Zenodo doi:10.5281/zenodo.4450305 (CC-BY-4.0; arXiv:2004.09244), downloaded with an md5 check.
  - **P2 (Voronoi density estimator): gate PASS.** Both snapshots (1,619 and 4,225 skyrmions) lie above the
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
