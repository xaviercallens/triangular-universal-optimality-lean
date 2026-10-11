# Physical use case P1: the D2 energy bound against measured skyrmion lattices

**Tier X (consistency evidence). This is not a validation of the upstream proof.**

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

[`results/P1_skyrmion.md`](results/P1_skyrmion.md) is the run as preregistered.
[`results/P1b_skyrmion.md`](results/P1b_skyrmion.md) is the run under the amendment.

| | P1 (as preregistered) | P1b (post-hoc amendment, not blind) |
|---|---|---|
| Tolerance | one tol across all potentials (0.25–0.31) | per-potential tol (3–39%) |
| Data below the bound | **none** (all 14 gaps positive) | **none** (all 14 gaps positive, also after bias correction) |
| Gate | **FAIL**: the control-sensitivity criterion failed | **FAIL**: 8 of the 14 potential–snapshot pairs failed a control check (13 failed checks in all) |

**Outcome.** Neither measured configuration falls below the triangular-lattice bound, for any of the seven
potentials. But the experiment, as preregistered, did not pass its own sensitivity checks. The finite-window density
estimate gives a perfect lattice an apparent energy error of about 3–10%. That is larger than the true square-vs-triangle
difference for soft potentials (about 1–4%). So for those potentials the test cannot distinguish a triangular from a
square arrangement, and their data gaps are not evidence either way.

Some potential–snapshot pairs pass all controls:

- 338 K: gauss α = 1, α = 2 and α = 4, and Riesz s = 6;
- 330 K: gauss α = 2 and α = 4.

In those pairs the data sit clearly above the bound. For α = 1 the gap is +15%; for Riesz s = 6 it is +18%. The
very large α = 2 and α = 4 gaps mostly measure the scatter of nearest-neighbour spacings.

**Exploratory, not gated.** We correlated each skyrmion's local energy excess with its measured |ψ₆|. The correlation
is −0.058 (p = 0.002) at 338 K, which is the expected sign. At 330 K it is +0.037 (p = 0.30), the opposite sign and not
significant.

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
```

This needs numpy, scipy and mpmath, and takes about 20 s.

## Possible next step

A preregistered P2 with a better density estimator, for example a Voronoi-based or count-in-many-windows estimate, or
larger fields of view. It would need to bring the perfect-lattice error below about 1% before soft potentials can be
resolved.
