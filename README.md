# Triangular-lattice universal optimality: kernel-checked Lean corollaries (open for red-team review)

**Status: open red-team review, round 1 (citizen scientists). Not peer reviewed.**
We are asking people to try to break these claims. See [RED_TEAM.md](RED_TEAM.md).

## The claim, stated exactly

This repository contains Lean 4 proofs of named corollaries of one upstream theorem,
`OAI.AtomicTriangular.universal_energy_minimum`, from the [openai/math](https://github.com/openai/math) repository
(commit `adc7f124`; the triangular files are unchanged at `fd4aeeb2`). That theorem says the covolume-one triangular
lattice `A` minimises the lower `g`-energy among all locally finite density-one configurations in the plane, for
every smooth completely monotone `g` of squared distance. An AI system wrote the upstream proof. The Lean kernel
accepts it, with only the standard axioms.

On top of that theorem, this repository proves the following in the Lean kernel, with only `propext`,
`Classical.choice` and `Quot.sound`:

| ID | Lean name | Statement (informal) | Verification |
|---|---|---|---|
| D1 | `TriangularRiesz.triangular_riesz_optimal` | For every `s > 0`, `t ↦ t^(-s/2)` is admissible, so `A` minimises the Riesz `s`-energy among all locally finite density-one configurations. | confirmed with corrections |
| D1b | `TriangularRiesz.latticeEnergy_riesz_lt_top` | For `s > 2` the lattice's Riesz energy is finite, so D1 is a real comparison and not `∞ ≤ ∞`. | confirmed with corrections |
| D2 | `TriangularDensity.triangular_optimal_any_density` | For every density `ρ > 0`, the rescaled lattice `ρ^(-1/2) A` has density `ρ` and attains the minimum. Without the rescaling the claim is false (`unscaled_false`). | confirmed with corrections |
| D3 | `TriangularUniversalOptimality.triangular_universally_optimal` | `ρ^(-1/2) A` is universally optimal in the sense of CKMRV Def. 1.3, **using lower energy (liminf)**, which is a weaker notion. | confirmed with corrections |
| D3 | `TriangularUniversalOptimality.universal_optimum_not_unique` | The lattice with one point removed is also a universal optimum (lower-energy sense) and is not an isometric copy of `A`. So "particles always arrange into a triangular lattice" is false as a uniqueness statement over *all* configurations. This is the remark after CKMRV Thm 1.4. | confirmed with corrections |
| D4 | `TriangularOpenDisk.universal_energy_minimum_open` | Upstream's theorem holds unchanged if density and energy are counted in open disks instead of closed ones. | **preregistered; no compile log or axiom audit on record; treat as unverified** |

"Confirmed with corrections" means a separate AI-agent instance recompiled the proofs, audited the axioms and checked
the wording. It does **not** mean a human checked them. See [METHODOLOGY.md](METHODOLOGY.md).

## What this is **not**

- **It does not settle the Cohn–Kumar conjecture.** Every result here rests on two things that no human has checked:
  1. **Statement fidelity:** do upstream's Lean definitions (`AdmissiblePotential`, `LocallyFinite`, `DensityOne`,
     `energy`, `latticeEnergy`) faithfully express Cohn–Kumar / CKMRV? Only an AI audit exists:
     [verification/statement_fidelity.md](verification/statement_fidelity.md).
  2. **The upstream proof and manuscript:** they are AI-generated and have not been peer reviewed.
- Upstream itself does not claim the stronger per-potential form (a sharp auxiliary function for each potential).
- Uniqueness among *periodic* configurations (the form CKMRV prove in dimensions 8 and 24) is not claimed by
  upstream for dimension 2, and is not addressed here.
- D1 is the kernel-checked form of a case the upstream manuscript already states ("includes every inverse power").
  It is not new mathematics. D2 is a standard rescaling. What these files add is a formal, auditable statement with
  named corollaries, controls and an audit trail.

Full list: [LIMITATIONS.md](LIMITATIONS.md).

## Repository layout

```
lean/Triangular/        Lean sources (Riesz, RieszFinite, AnyDensity, Controls, UniversalOptimality, OpenDisk, Axioms)
verification/           axiom-audit output, statement-fidelity audit, independent verification reports, ledger
prereg/                 preregistrations (hypothesis + kill criterion, written before the Lean file)
tools/lean_pinned.py    the compile wrapper used, with machine paths replaced by environment variables
BUILD.md                how to reproduce against the pinned upstream stack
METHODOLOGY.md          pipeline, controls, and exactly who checked what
LIMITATIONS.md          scope limits and known gaps
RED_TEAM.md             what to attack and how to report it
RED_TEAM_LOG.md         every report received and what we did about it
PROVENANCE.md           source commit and sha256 of every copied file
```

`lean/Triangular/Axioms.lean` contains a deliberate `sorry` and a deliberate `axiom` (`ctl_sorry`, `ctl_cheat`).
They are planted negative controls that show the axiom audit catches cheating. A "no sorry" grep will flag them, by
design.

## Publications

- D1, D1b, D2: *Riesz-energy, finiteness and every-density corollaries of the openai/math planar universal-optimality
  theorem, kernel-checked in Lean 4*, doi:[10.5281/zenodo.23285631](https://doi.org/10.5281/zenodo.23285631)
- D3 and the claim ledger: tiered universal-optimality preprint,
  doi:[10.5281/zenodo.23293429](https://doi.org/10.5281/zenodo.23293429) (v2; v1 is 10.5281/zenodo.23293112)
- The D1–D3 Lean files (not D4) also ship in LeanMaster (`contrib/openai_math_corollaries/`, releases v3.47.0–v3.48.1), on a
  separate toolchain, outside LeanMaster's own proof gates.

## Credits and AI use

The upstream theorem and its proof are by the openai/math project (Apache-2.0); we do not claim them. The corollaries,
audits and controls in this repository were produced by Claude (Anthropic) AI agents under the direction of Xavier
Callens, following the Elenchus method ([SocrateAI-Scientific-Elenchus](https://github.com/xaviercallens/SocrateAI-Scientific-Elenchus)).
DeepSeek-Prover-V2 was queried during D3; none of its output was used.

References: H. Cohn, A. Kumar, *Universally optimal distribution of points on spheres*, JAMS 20 (2007).
H. Cohn, A. Kumar, S. D. Miller, D. Radchenko, M. Viazovska, *Universal optimality of the E8 and Leech lattices and
interpolation formulas*, Ann. of Math. 196 (2022) ("CKMRV").

## Licence

Lean code and tools: MIT (see [LICENSE](LICENSE)). Documentation: CC-BY-4.0. Upstream openai/math is Apache-2.0; no
upstream file is copied into this repository.
