# Physical use case P1: the D2 energy bound against measured skyrmion lattices

**Tier X (consistency evidence). This is not a validation of the upstream proof. Headline: P2, gate PASS.**

## Data

The data are two Kerr-microscopy snapshots of a 2D skyrmion lattice in a thin-film multilayer:

| Snapshot | Skyrmions | Mean spacing |
|---|---|---|
| 330 K, 40 µT | 1,618 | 9.2 µm |
| 338 K, 20 µT | 4,224 | 5.7 µm |

Each file gives positions in µm and the measured local order |ψ₆|. Source:

- *Data for the article "Skyrmion Lattice Phases in Thin Film Multilayer"*, Zenodo,
  doi:[10.5281/zenodo.4450305](https://doi.org/10.5281/zenodo.4450305), licence CC-BY-4.0.
- Files used: `fig3/FIG_snap_absPsi6_330K_40uT.dat` and `fig3/FIG_snap_absPsi6_338K_20uT.dat`.
- Article: [arXiv:2004.09244](https://arxiv.org/abs/2004.09244). All credit for the measurements goes to its authors.
- The script downloads the archive from Zenodo and checks its md5 against the Zenodo API before using it. The data are
  not redistributed here.

## What is tested

The test rests on D2 together with upstream's `universal_energy_minimum`:

> For every completely monotone potential g of the squared distance, and every configuration of density ρ, the energy
> per point is at least that of the triangular lattice at density ρ.

The bound holds for *any* configuration and *any* such g. So a measured point pattern is a valid input, whatever the
skyrmions' true interaction. We test seven potentials:

- short-range Gaussians e^{−παt} with α ∈ {0.5, 1, 2, 4} (density-1 units);
- Riesz t^{−s/2} with s ∈ {3, 4, 6}, which is informative for s > 2 (D1b).

A finite window is only a proxy for the theorem's liminf over growing disks. The estimator (density from an inner box,
cutoff R_c = 6) and the controls C1–C4 were fixed in [`prereg/P1_skyrmion.json`](../prereg/P1_skyrmion.json) before the
data were analysed.

## Results

[`results/P2_skyrmion.md`](results/P2_skyrmion.md) is the headline. Earlier runs are kept unchanged:
[`results/P1_skyrmion.md`](results/P1_skyrmion.md) (as preregistered) and [`results/P1b_skyrmion.md`](results/P1b_skyrmion.md)
(post-hoc amendment).

| | P1 (as preregistered) | P1b (post-hoc amendment) | **P2 (new preregistration)** |
|---|---|---|---|
| Density estimator | point count in an inner box | point count in an inner box | **Voronoi cells of the averaged points** |
| Tolerance | one value across potentials (0.25–0.31) | per potential (3–39%) | per potential (1e-14 for Gaussians; 1e-4 to 1.2e-2 for Riesz) |
| Data below the bound | none | none | **none** |
| Gate | FAIL (controls) | FAIL (8 of 14 pairs unresolved) | **PASS (all 14 pairs resolved)** |

**Why P1 and P1b failed.** Counting points in a box gave a perfect lattice an apparent energy error of 3–10%. That
is more than the 1–4% square-vs-triangle difference for soft potentials, so those potentials could not be resolved.

**Why P2 resolves them.** The Voronoi estimator gives every cell of a perfect lattice an area of exactly 1/ρ. That
drops the calibration error to rounding level for Gaussians. For Riesz the remaining error is the R_c = 6 tail
approximation.

The controls in P2 behave as theory predicts:

- **Square lattice:** for Riesz s = 4 it sits +4.18–4.20% above the triangular lattice; the closed forms give 4.21%.
  For the Gaussian with α = 0.5 it sits +0.643% above; the theta-function value is about 0.65%.
- **Jittered lattices:** every jitter series increases with σ.
- **Density mismatch:** evaluating the data against the lattice at 1.3 ρ̂ violates the bound, so the test can fail.

**Outcome (Tier X).** Both measured skyrmion configurations lie above the triangular-lattice bound for all seven
completely monotone potentials, and every gap exceeds its tolerance:

- 330 K: +4.2% (Gaussian α = 0.5), +4.3% (Riesz s = 3), +10.6% (s = 4), +32% (s = 6);
- 338 K: +3.0%, +2.7%, +6.5% and +19% for the same four potentials.

The very large α = 2 and α = 4 gaps mostly measure the scatter of nearest-neighbour spacings. The colder, lower-field
330 K snapshot sits further above the bound than the 338 K one for every potential.

**Exploratory, not gated.** The local energy excess correlates with the measured |ψ₆| at −0.057 (p = 0.002) at 338 K,
the expected sign. At 330 K the correlation is +0.037 (p = 0.30), the opposite sign and not significant.

**Honesty notes.**
- P2 was designed after P1 and P1b were seen. Its data verdict was therefore not blind, because every data gap was
  already positive. What P2 had to pass were its controls, and it did.
- No estimator was changed after the P2 run.

## What this does not show

- It does not test the upstream proof or its statement fidelity (red-team target T1).
- It does not show that skyrmions interact through a completely monotone potential.
- It cannot separate the global theorem from results that were already known. These configurations are perturbed
  triangular lattices, and lattice-only optimality plus local optimality
  ([arXiv:2511.03353](https://arxiv.org/abs/2511.03353)) already predict that they sit above the lattice.

## Reproduce

```bash
python3 physics/skyrmion_check.py                                              # P1, as preregistered
python3 physics/skyrmion_check.py --tol-mode per-potential --seed 20261012 --tag P1b
python3 physics/skyrmion_check.py --tol-mode per-potential --seed 20261013 --density voronoi --tag P2   # headline
```

This needs numpy, scipy and mpmath, and takes about 20 s.

## Possible next steps

- Use more snapshots across the paper's temperature and field series (only the two `fig3` snapshots are position data
  in this record).
- Try a system whose interaction is known to be completely monotone, such as dipolar colloids (1/r³, which is Riesz
  s = 3), so the energy gap has a direct physical meaning.
