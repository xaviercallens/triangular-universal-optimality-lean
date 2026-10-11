# Literature status (red-team target T6)

This is a first pass, done with web search on 2026-10-11. It is not a systematic review. Please add to it (T6).

## Status of the 2D conjecture, apart from the upstream claim

- **Still described as open.** *The hexagonal lattice is universally locally optimal*,
  [arXiv:2511.03353](https://arxiv.org/abs/2511.03353) (November 2025), calls global universal optimality of A₂ among
  density-1 configurations a major open problem (Cohn–Kumar 2007, Conjecture 9.4). It proves *local* optimality for
  all Gaussian potentials.
- **Among lattices, the result is classical.** Montgomery (1988) proved it for theta functions; Rankin, Cassels, Ennola
  and Diananda proved the Epstein-zeta case.
- **Among periodic configurations with small periods:** the same paper cites [HT25] for universal optimality of A₂ among
  configurations with a period of 4 or 6 points. We have not read HT25.
- **Other potentials:** Bétermin's computer-assisted work on Lennard-Jones type energies
  ([arXiv:2104.09795](https://arxiv.org/abs/2104.09795)) covers potentials that are *not* completely monotone, so they
  are outside this repository's scope.
- **Dimensions 8 and 24:** CKMRV, [arXiv:1902.05438](https://arxiv.org/abs/1902.05438) (Ann. of Math. 2022).

## Public discussion of the openai/math claim (family 090)

- We found no assessment of the upstream proof or its statement by a mathematician.
- **Secondary blog review** of OpenAI's math release
  ([kingy.ai, 2026-10-06](https://kingy.ai/blog/openai-math-722-manuscripts-results-proofs-compute-costs/)):
  - It lists "Universal optimality of the triangular lattice" as result family 090 (4 manuscripts, Lean scope).
  - It says it did *no independent Lean execution*.
  - It cautions that a checked proof only establishes the formal statement relative to its definitions.
- **AI-made explainer videos** ([dimenwarper/oai-math-vids](https://github.com/dimenwarper/oai-math-vids/releases/tag/v1.0)):
  they label the result as Lean-formalised, and say mathematicians have not checked the videos.

## What this repository adds to that picture

- It runs Lean independently: a clean rebuild against the pinned upstream stack, with an axiom audit.
- It audits the statement against CKMRV, though the auditor was an AI (T1 is still the main open question).
- It adds named corollaries and controls.

None of this replaces a mathematician's reading of the upstream definitions.
