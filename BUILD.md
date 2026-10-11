# Reproducing the build

**Status:** these steps were run on 2026-10-11 on the original machine, with stale oleans removed first; the results
are in `verification/rebuild_2026-10-11/`. No rebuild from a fresh clone on another machine has been done yet
(red-team target T5), so reports of what happens when you follow these steps are very welcome.

These files are **not** a standalone Lake package. They compile as loose modules against upstream's pinned build,
with the `lean` binary, in dependency order.

## 1. Pinned upstream stack

```bash
git clone https://github.com/openai/math openai-math
cd openai-math && git checkout adc7f124      # triangular files are identical at fd4aeeb2
cd lean                                       # lean-toolchain: leanprover/lean4:v4.34.1
lake build OAI.Analysis.Triangular.Energy.Universal OAI.NumberTheory.DirichletL.LatticeSummability
export OPENAI_MATH_PINNED=$PWD
```

The upstream build is large. On the original machine, compiling a single corollary file took between 5 minutes (idle)
and over 12 minutes (under load) once upstream was built.

## 2. Compile the corollaries in order

```bash
export LEAN_TOOLCHAIN_BIN=$HOME/.elan/toolchains/leanprover--lean4---v4.34.1/bin   # adjust
cd <this repo>
for m in Riesz RieszFinite AnyDensity Controls UniversalOptimality OpenDisk OpenDiskAny; do
  python3 tools/lean_pinned.py compile lean/Triangular/$m.lean --olean Triangular.$m || break
done
python3 tools/lean_pinned.py compile lean/Triangular/Axioms.lean --json-out my_axioms.json
python3 tools/lean_pinned.py compile lean/Triangular/AxiomsD4.lean --json-out my_axioms_d4.json
```

## 3. Check the axiom audit

Compare `my_axioms.json` with `verification/axiom_audit_Axioms.json`. You should see:

- every real theorem: `[propext, Classical.choice, Quot.sound]`;
- `ctl_sorry`: includes `sorryAx` (planted control);
- `ctl_axiom`: includes `ctl_cheat` (planted control).

`Axioms.lean` covers D1–D4, including `OpenDiskAny`. `AxiomsD4.lean` is a supplementary D4 audit with a non-vacuity
theorem at `A` and its own planted-axiom control.

Delete stale `.olean` files before rebuilding. Raw `lean` does not check that an olean matches its source.
