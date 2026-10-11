# Limitations and scope

| # | Limitation | Consequence |
|---|---|---|
| L1 | Everything depends on upstream `universal_energy_minimum`. It is AI-generated and not peer reviewed. Its statement fidelity was audited only by an AI. | Wherever these files say "proved", read "proved, assuming upstream's definitions mean what we think". |
| L2 | `UniversallyOptimal` (D3) uses lower energy (liminf). CKMRV Def. 1.2–1.3 also require the energy to exist as a limit. | Our notion is weaker than CKMRV's. We do not claim it is *strictly* weaker, because we have no witness. |
| L3 | Upstream does not claim the per-potential form of Cohn–Kumar (a sharp auxiliary function for each potential). | Neither do we. |
| L4 | Uniqueness among periodic configurations in dimension 2 is not claimed by upstream and is not addressed here. | The non-uniqueness result (D3) is about *all* locally finite configurations under lower energy, as in CKMRV's remark after Thm 1.4. |
| L5 | For Riesz `s ≤ 2` the lattice energy is `∞`. | D1 and D2 say something only for `s > 2`. |
| L6 | Upstream counts points in closed disks centred at the origin. D4 claims that open disks give the same results. | D4 is unaudited: there is no compile log or axiom audit on record (red-team target T7). |
| L7 | D1 is a case the upstream manuscript already states, and D2 is standard rescaling. | No novelty is claimed for the mathematics. The contribution is the formal statements, controls and audit trail. |
| L8 | No literature search after 2025 has been done for the current status of the 2D Cohn–Kumar conjecture, or for public reactions to the upstream claim. | Red-team target T6. |
| L9 | No rebuild from a fresh clone has been done outside the original machine. | Red-team target T5. |
| L10 | Upstream withdrew three unrelated manuscripts on 2026-10-07 (commit `fd4aeeb2`). The triangular files are byte-identical at that commit. | Watch upstream for errata or a withdrawal affecting the triangular manuscripts. |
