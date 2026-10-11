# Red-team log

One row per report. Outcomes: ACCEPTED-fixed, ACCEPTED-scope, DECLINED (with reason), OPEN.
"Source commit" refers to the AutoevolveAI repository where the work was produced (see PROVENANCE.md).

## Internal reviews before publication (AI verifier and auditor agents)

| Date | Target | Reporter | Summary | Outcome | Source commit |
|---|---|---|---|---|---|
| 2026-10-10 | T3 | D1 verifier agent | "Settles Cohn–Kumar" framing too strong; D1 informative only for s > 2 | ACCEPTED-fixed in docstring and paper | after 57c8a9c / 4d5a6b3 |
| 2026-10-10 | T1 | D2 verifier agent | D2 proved only a lower bound; added `scaled_density`, `attained`, `unscaled_false` | ACCEPTED-fixed | 63b24aa |
| 2026-10-10 | T2 | D3 verifier agent | `UniversallyOptimal` drops the energy-limit requirement of CKMRV Def. 1.2 | ACCEPTED-scope (L2) | d50dfc43 |
| 2026-10-10 | T3 | D3 verifier agent | "Previously solved only in dimensions 8 and 24" is wrong: d = 1 was solved earlier | ACCEPTED-fixed in paper | d50dfc43 |
| 2026-10-11 | T3 | manuscript auditor agent | "Strictly weaker" unproven; "periodic uniqueness is open" unsourced ("not claimed by upstream"); "only the minimum value is determined" overreaches | **Fixed in the preprint and this repo's docs; still OPEN in the Lean docstrings** (see below) | — |

| 2026-10-11 | T7 | D4 verifier agent | D4 identities need no `LocallyFinite` hypothesis; "settles guideline 4" holds only for upstream's centred-disk liminf observables | ACCEPTED-fixed (`OpenDiskAny.lean`, docstring scope note) | AutoevolveAI `f81a2209` |
| 2026-10-11 | T5 | own clean rebuild (`verification/rebuild_2026-10-11/`) | Public commit `064cfa9` shipped `Axioms.lean` importing `Triangular.OpenDiskAny` without the file, so `Axioms.lean` did not compile from the repo | ACCEPTED-fixed in v0.1.0 (file added, rebuild gate re-run) | v0.1.0 |

| 2026-10-11 | T6 | producer (web search) | First-pass literature check: arXiv:2511.03353 (November 2025) still calls the 2D conjecture open; no assessment of the upstream proof by a mathematician was found | ACCEPTED-scope (LITERATURE.md, L8); a systematic review stays open | v0.1.0 |

| 2026-10-11 | T3 | producer (P1 run) | Real-data check P1 failed its own control-sensitivity gate as preregistered: the single tolerance across potentials was too loose. The post-hoc P1b (per-potential tolerance, fresh seed) also failed for 8 of 14 potential–snapshot pairs. No data gap was below the bound. | ACCEPTED-scope: reported as FAIL with the resolved subset named; no "validated" wording | physics/ |

## Open at publication

| Target | Where | Summary | Outcome |
|---|---|---|---|
| T3 | `lean/Triangular/UniversalOptimality.lean` lines 10, 20–21, 237–238 (docstrings only) | The docstrings still say "strictly weaker", "is open in dimension 2" and "only the minimum value". The correct wording is "weaker (strictness not claimed)", "not claimed by upstream and not addressed", and "the minimiser is not unique up to isometry among all configurations (lower energy)". The Lean statements and proofs are unaffected. The file is kept byte-identical to the audited and Zenodo-published version, and will be corrected in the next release. | OPEN |
