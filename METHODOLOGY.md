# Methodology

## Pipeline

Each result went through these steps, in this order:

1. **Preregistration** (`prereg/`). The hypothesis, the predicted proof route, a kill criterion (what would count as
   failure) and controls were written and committed *before* the Lean file. The probability estimates in them are
   subjective priors, not measurements.
2. **Lean proof**, compiled against upstream's pinned stack (Lean `v4.34.1`, Mathlib `d13f23b7`, openai/math
   `adc7f124`) with `-DautoImplicit=false` (see [BUILD.md](BUILD.md)).
3. **Axiom audit.** `#print axioms` on every named theorem (`lean/Triangular/Axioms.lean`, output in
   `verification/axiom_audit_Axioms.json`). Only `propext`, `Classical.choice` and `Quot.sound` are accepted.
   `sorry` and extra axioms both compile with exit code 0, so the exit code alone proves nothing. The audit is the
   check.
4. **Planted controls.** `Axioms.lean` contains a theorem proved by `sorry` and one proved from a fake axiom. Both are
   flagged in the audit output, which shows the audit catches cheating.
5. **Negative controls**, kernel-checked, showing the statements are not trivially true:
   - `riesz_neg_two_not_admissible`: the wrong-sign potential is not admissible.
   - `unscaled_false`: D2 without the `ρ⁻¹` rescaling is false.
   - `vacancy_not_isometric_image`: the vacancy configuration is genuinely different from the lattice.
   - D1b shows the Riesz bound is not `∞ ≤ ∞` for `s > 2`.
6. **Independent verification (producer ≠ verifier).** A separate AI-agent instance recompiled each result, re-ran
   the axiom audit, wrote its own controls and numerics, and checked the wording against the CKMRV text
   (`verification/D{1,2,3}/verification.md`). All three verdicts were CONFIRMED_WITH_CORRECTIONS. The corrections were
   applied to the Lean code and the papers. Three docstring phrases in `UniversalOptimality.lean` were not updated;
   they are listed as OPEN in [RED_TEAM_LOG.md](RED_TEAM_LOG.md).
7. **Manuscript audit.** A separate read-only instance audited the D3 preprint
   (`verification/manuscript_audit_2026-10-11.md`). Verdict: ACCEPT_WITH_CORRECTIONS, with no mathematical error found.

## Who checked what (read this before trusting anything)

| Check | Done by | Human? |
|---|---|---|
| Upstream proof correct | Lean kernel (Comparator run, 140 min, `COMPARATOR_ACCEPTS`) | no |
| Upstream definitions match CKMRV | the producing AI agent (`statement_fidelity.md`); the verifier agents re-read them | **no** |
| Our corollaries compile, axiom-clean | Lean kernel, run by producer and verifier agents | no |
| Wording and overclaim review | verifier and auditor agents | **no** |
| Clean rebuild of every module, stale oleans removed (`verification/rebuild_2026-10-11/`) | Lean kernel, original machine and pinned stack; source sha256 of upstream's challenge file matched the audited one | no |
| Fresh-clone rebuild on another machine | **not done yet** | — |

The "independent" verifiers were other instances of the same family of AI models. They are independent in process,
not in kind. No human mathematician has checked any step. This is the main reason for the red-team review.

## Known process incidents

- The D2 commit accidentally included verifier scratch files, one with a `sorry`. They were removed, and the
  scratch-file pattern is now ignored.
- The D3 verifier reused oleans built by the producer. Raw `lean` does not check that an olean matches its source.
  This was closed on 2026-10-11 by a clean rebuild of the whole chain (`verification/rebuild_2026-10-11/`).
- The first public commit (`064cfa9`) shipped an `Axioms.lean` that imports `Triangular.OpenDiskAny` but not the file
  itself. The source changed between our review and the copy. The file was added in v0.1.0 and caught by our own
  rebuild before release; see RED_TEAM_LOG.
- D4 was verified by a separate agent (`verification/D4/verification.md`, ACCEPT_WITH_CORRECTIONS). Its correction was
  that the identities need no local-finiteness hypothesis, and that is now proved in `OpenDiskAny.lean`.
