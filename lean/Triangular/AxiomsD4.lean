import Triangular.OpenDisk

/-! Supplementary axiom audit of D4 (open versus closed disks), written for the 2026-10-11 clean rebuild: a
non-vacuity theorem at the lattice `A` and a planted-axiom control. `Axioms.lean` also audits D4. -/

#print axioms TriangularOpenDisk.energy_eq_openEnergy
#print axioms TriangularOpenDisk.densityOne_iff_open
#print axioms TriangularOpenDisk.universal_energy_minimum_open

/-- Non-vacuity: the open-disk theorem applies to the lattice itself. -/
theorem d4_nonvacuous (g : ℝ → ℝ) (hg : OAI.AtomicTriangular.AdmissiblePotential g) :
    OAI.AtomicTriangular.latticeEnergy g ≤ TriangularOpenDisk.openEnergy g OAI.AtomicTriangular.A :=
  (TriangularOpenDisk.universal_energy_minimum_open g OAI.AtomicTriangular.A hg TriangularDensity.A_lf
    ((TriangularOpenDisk.densityOne_iff_open TriangularDensity.A_lf).1 TriangularDensity.A_d1)).1

#print axioms d4_nonvacuous

axiom ctl_cheat_d4 : False
theorem ctl_axiom_d4 : TriangularOpenDisk.openEnergy (fun _ => 0) OAI.AtomicTriangular.A = 1 := ctl_cheat_d4.elim
#print axioms ctl_axiom_d4
