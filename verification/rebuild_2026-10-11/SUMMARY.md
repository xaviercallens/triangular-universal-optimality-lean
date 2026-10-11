# Clean rebuild and axiom audit

Produced by `verify_triangular_uo.sh` (results parsed from compiler output; see the JSON files here).

| Module | rc | seconds |
|---|---|---|
| AnyDensity | 0 | 14.6 |
| Axioms | 0 | 16.6 |
| AxiomsD4 | 0 | 14.1 |
| Controls | 0 | 16.0 |
| OpenDisk | 0 | 29.5 |
| OpenDiskAny | 0 | 11.9 |
| Riesz | 0 | 16.0 |
| RieszFinite | 0 | 12.5 |
| UniversalOptimality | 0 | 17.8 |

Real theorems audited: 31. Whitelist: propext, Classical.choice, Quot.sound.

| Declaration | Axioms |
|---|---|
| `OAI.AtomicTriangular.universal_energy_minimum` | Classical.choice, Quot.sound, propext |
| `OAI.SevenEighths.LatticeSummability.summable_normForm_neg_rpow` | Classical.choice, Quot.sound, propext |
| `TriangularControls.rho_one` | Classical.choice, Quot.sound, propext |
| `TriangularControls.riesz_any_density_homogeneous` | Classical.choice, Quot.sound, propext |
| `TriangularControls.riesz_lattice_homogeneous` | Classical.choice, Quot.sound, propext |
| `TriangularControls.riesz_neg_two_not_admissible` | Classical.choice, Quot.sound, propext |
| `TriangularControls.riesz_sq` | Classical.choice, Quot.sound, propext |
| `TriangularDensity.attained` | Classical.choice, Quot.sound, propext |
| `TriangularDensity.riesz_any_density` | Classical.choice, Quot.sound, propext |
| `TriangularDensity.scaled_density` | Classical.choice, Quot.sound, propext |
| `TriangularDensity.triangular_optimal_any_density` | Classical.choice, Quot.sound, propext |
| `TriangularDensity.universal_any_density` | Classical.choice, Quot.sound, propext |
| `TriangularDensity.unscaled_false` | Classical.choice, Quot.sound, propext |
| `TriangularOpenDisk.A_densityOneOpen` | Classical.choice, Quot.sound, propext |
| `TriangularOpenDisk.densityOne_iff_open` | Classical.choice, Quot.sound, propext |
| `TriangularOpenDisk.energy_eq_openEnergy` | Classical.choice, Quot.sound, propext |
| `TriangularOpenDisk.universal_energy_minimum_open` | Classical.choice, Quot.sound, propext |
| `TriangularOpenDiskAny.ctl_closed` | Classical.choice, Quot.sound, propext |
| `TriangularOpenDiskAny.ctl_open` | Classical.choice, Quot.sound, propext |
| `TriangularOpenDiskAny.densityOne_iff_open_any` | Classical.choice, Quot.sound, propext |
| `TriangularOpenDiskAny.energy_eq_openEnergy_any` | Classical.choice, Quot.sound, propext |
| `TriangularRiesz.latticeEnergy_riesz_lt_top` | Classical.choice, Quot.sound, propext |
| `TriangularRiesz.norm_sq_triangularPoint` | Classical.choice, Quot.sound, propext |
| `TriangularRiesz.riesz_admissible` | Classical.choice, Quot.sound, propext |
| `TriangularRiesz.triangular_riesz_optimal` | Classical.choice, Quot.sound, propext |
| `TriangularUniversalOptimality.triangular_universally_optimal` | Classical.choice, Quot.sound, propext |
| `TriangularUniversalOptimality.universal_optimum_not_unique` | Classical.choice, Quot.sound, propext |
| `TriangularUniversalOptimality.vacancy_energy` | Classical.choice, Quot.sound, propext |
| `TriangularUniversalOptimality.vacancy_not_isometric_image` | Classical.choice, Quot.sound, propext |
| `TriangularUniversalOptimality.vacancy_universally_optimal` | Classical.choice, Quot.sound, propext |
| `ctl_axiom` | Classical.choice, Quot.sound, ctl_cheat, propext |
| `ctl_axiom_d4` | Classical.choice, Quot.sound, ctl_cheat_d4, propext |
| `ctl_sorry` | Classical.choice, Quot.sound, propext, sorryAx |
| `d4_nonvacuous` | Classical.choice, Quot.sound, propext |

**GATE: PASS**
