# Limitations and scope

| # | Limitation | Consequence |
|---|---|---|
| L1 | Everything depends on upstream `universal_energy_minimum`. It is AI-generated and not peer reviewed. Its statement fidelity was audited only by an AI. | Wherever these files say "proved", read "proved, assuming upstream's definitions mean what we think". |
| L2 | `UniversallyOptimal` (D3) uses lower energy (liminf). CKMRV Def. 1.2–1.3 also require the energy to exist as a limit. | Our notion is weaker than CKMRV's. We do not claim it is *strictly* weaker, because we have no witness. |
| L3 | Upstream does not claim the per-potential form of Cohn–Kumar (a sharp auxiliary function for each potential). | Neither do we. |
| L4 | Uniqueness among periodic configurations in dimension 2 is not claimed by upstream and is not addressed here. | The non-uniqueness result (D3) is about *all* locally finite configurations under lower energy, as in CKMRV's remark after Thm 1.4. |
| L5 | For Riesz `s ≤ 2` the lattice energy is `∞`. | D1 and D2 say something only for `s > 2`. |
| L6 | Upstream counts points in closed disks centred at the origin. D4 shows open disks give the same density, lower energy and optimality conclusion. | This settles only upstream's own observables. It says nothing about other window shapes, non-centred windows, `limsup` energies, or physical boundary conditions such as jellium (D4 verification §5). |
| L7 | D1 is a case the upstream manuscript already states, and D2 is standard rescaling. | No novelty is claimed for the mathematics. The contribution is the formal statements, controls and audit trail. |
| L8 | Only a first-pass web search has been done (2026-10-11, [LITERATURE.md](LITERATURE.md)). The latest paper found (arXiv:2511.03353, November 2025) still calls the 2D conjecture open, and we found no assessment of the upstream proof by a mathematician. | A systematic review is still red-team target T6. |
| L9 | A clean rebuild of all modules was done on 2026-10-11, with stale oleans moved aside, but only on the original machine and its pinned stack. | A rebuild from a fresh clone on another machine is still red-team target T5. |
| L10 | Upstream withdrew three unrelated manuscripts on 2026-10-07 (commit `fd4aeeb2`). The triangular files are byte-identical at that commit. | Watch upstream for errata or a withdrawal affecting the triangular manuscripts. |
