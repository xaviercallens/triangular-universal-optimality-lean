#!/usr/bin/env python3
"""Check measured or simulated 2D point configurations against the triangular-lattice energy bound.

The bound: for every completely monotone potential g of squared distance (energy sum g(|x - y|^2)) and every locally
finite planar configuration of density rho, the energy per point is at least that of the triangular lattice at density
rho (D2 in this repository; kernel-checked in Lean, conditional on the upstream openai/math theorem). This tool applies
it to YOUR point data, with the estimator validated in P2 (Voronoi-cell density, inner points only) and the same
controls, so that you know whether the result is resolved.

Input: a text/CSV file with x and y columns (any length unit; only ratios matter).
Potentials (density-1 units, t = r^2):
  gauss:A    exp(-pi A t)                  Tier A (kernel-checked admissible via upstream)  -- any A > 0
  riesz:S    t^(-S/2) = r^(-S)             Tier A (D1); informative for S > 2
  yukawa:K   exp(-K r) / r                 Tier C: complete monotonicity in t is a written argument, not kernel-checked

Usage:
  python3 physics/ubound.py positions.csv [--cols 0,1] [--potentials gauss:1,riesz:3,yukawa:1] [--json out.json]
  python3 physics/ubound.py --self-test
Exit code: 0 if no potential is BELOW the bound, 1 otherwise, 2 on self-test failure.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skyrmion_check as sc  # noqa: E402  (shares the P2-validated estimator and controls)

DEFAULT = "gauss:0.5,gauss:1,gauss:2,riesz:3,riesz:4,riesz:6,yukawa:1"


def parse_potential(spec: str) -> sc.Potential:
    kind, val = spec.split(":")
    v = float(val)
    if v <= 0:
        raise ValueError(f"parameter must be > 0: {spec}")
    if kind == "gauss":
        return sc.Potential(spec, lambda t, a=v: np.exp(-math.pi * a * t), 0.0, None)
    if kind == "riesz":
        if v <= 2:
            raise ValueError("riesz:S needs S > 2 (for S <= 2 the lattice energy is infinite, so the bound is vacuous)")
        return sc.Potential(spec, lambda t, s=v: t ** (-s / 2), 2 * math.pi * sc.RC ** (2 - v) / (v - 2), v)
    if kind == "yukawa":
        tail = 2 * math.pi * math.exp(-v * sc.RC) / v  # integral of exp(-K r)/r * 2 pi r dr beyond R_c
        return sc.Potential(spec, lambda t, k=v: np.exp(-k * np.sqrt(t)) / np.sqrt(t), tail, None)
    raise ValueError(f"unknown potential kind: {kind}")


def tier(spec: str) -> str:
    return "C" if spec.startswith("yukawa") else "A"


def lattice_energy(p: sc.Potential, density: float = 1.0) -> float:
    if p.s is not None:
        return sc.lattice_energy(p, density)[0]
    pts = sc.lattice_points(60.0)
    t = np.sum(pts ** 2, axis=1)
    t = t[t > 1e-12] / density
    total = float(np.sum(p.g(t)))
    if p.name.startswith("yukawa"):  # continuum tail beyond radius 60: 2 pi d exp(-60 k / sqrt d) / k
        k = float(p.name.split(":")[1])
        total += 2 * math.pi * density * math.exp(-k * 60.0 / math.sqrt(density)) / k
    return total


def gaps(raw: np.ndarray, pots: list[sc.Potential], density_factor: float = 1.0) -> dict[str, float]:
    pts, _ = sc.to_density_one(raw)
    _, e = sc.per_point_energies(pts, pots)
    return {p.name: (float(e[p.name].mean()) - lattice_energy(p, density_factor)) / lattice_energy(p, density_factor)
            for p in pots}


def analyse(raw: np.ndarray, pots: list[sc.Potential], seed: int = 20261013, seeds: int = 20) -> dict:
    sc.DENSITY_MODE = "voronoi"
    rng = np.random.default_rng(seed)
    n = len(raw)
    aspect = float(np.ptp(raw[:, 0]) / np.ptp(raw[:, 1]))
    c1 = [gaps(sc.patch("tri", n, aspect, rng), pots) for _ in range(seeds)]
    tol = {p.name: 3 * max(abs(r[p.name]) for r in c1) for p in pots}
    c2 = {s: gaps(sc.patch("tri", n, aspect, rng, jitter=s), pots) for s in sc.JITTERS}
    c3 = gaps(sc.patch("sq", n, aspect, rng), pots)
    data = gaps(raw, pots)
    c4 = gaps(raw, pots, density_factor=sc.MISMATCH)
    _, rho = sc.to_density_one(raw)
    rows = {}
    for p in pots:
        seq = [c2[s][p.name] for s in sc.JITTERS]
        resolved = seq[0] > tol[p.name] and all(b > a for a, b in zip(seq, seq[1:])) and c3[p.name] > tol[p.name]
        g = data[p.name]
        if g < -tol[p.name]:
            verdict = "BELOW the bound - investigate"
        elif not resolved:
            verdict = "unresolved (controls fail: estimator too coarse for this potential)"
        elif g > tol[p.name]:
            verdict = "above the bound (resolved)"
        else:
            verdict = "at the bound within tolerance (lattice-like)"
        rows[p.name] = {"tier": tier(p.name), "gap": g, "tol": tol[p.name], "resolved": resolved, "verdict": verdict,
                        "C2_jitter": seq, "C3_square": c3[p.name], "C4_density_x1.3": c4[p.name],
                        "lattice_energy_density1": lattice_energy(p)}
    return {"n_points": n, "density_per_unit_area": rho, "seed": seed, "potentials": rows,
            "test_can_fail": any(c4[p.name] < -tol[p.name] for p in pots)}


def render(res: dict) -> str:
    L = [f"{res['n_points']} points, estimated density {res['density_per_unit_area']:.6g} per unit area "
         f"(Voronoi), seed {res['seed']}", "",
         f"{'potential':<12} {'tier':<4} {'gap':>11} {'tol':>9}  verdict", "-" * 78]
    for k, r in res["potentials"].items():
        L.append(f"{k:<12} {r['tier']:<4} {r['gap']:>+11.3e} {r['tol']:>9.1e}  {r['verdict']}")
    L += ["", f"density-mismatch control can fail the test: {res['test_can_fail']}"]
    return "\n".join(L)


def self_test() -> int:
    """Positive control: perfect lattice sits at the bound. Negative controls: square lattice above, wrong density below."""
    pots = [parse_potential(s) for s in DEFAULT.split(",")]
    rng = np.random.default_rng(1)
    sc.DENSITY_MODE = "voronoi"
    tri = sc.patch("tri", 2000, 1.3, rng) * 3.7 + 11.0  # arbitrary units and offset
    sq = sc.patch("sq", 2000, 1.3, rng) * 3.7
    g_tri, g_sq = gaps(tri, pots), gaps(sq, pots)
    g_bad = gaps(tri, pots, density_factor=1.3)
    ok = True
    for p in pots:
        a, b, c = g_tri[p.name], g_sq[p.name], g_bad[p.name]
        cond = abs(a) < 2e-2 and b > 3 * abs(a) and c < 0
        ok &= cond
        print(f"{p.name:<12} perfect {a:+.2e}  square {b:+.2e}  wrong-density {c:+.2e}  {'ok' if cond else 'FAIL'}")
    # known closed-form check: square vs triangle for Riesz s = 4 is 6.02681203969/5.78335929968 - 1
    want = 6.02681203969 / 5.78335929968 - 1
    got = g_sq["riesz:4"]
    print(f"riesz:4 square-vs-triangle {got:.4f} vs closed form {want:.4f}")
    ok &= abs(got - want) < 0.01
    print("SELF-TEST", "PASS" if ok else "FAIL")
    return 0 if ok else 2


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", type=Path)
    ap.add_argument("--cols", default="0,1", help="zero-based x,y column indices")
    ap.add_argument("--potentials", default=DEFAULT)
    ap.add_argument("--seed", type=int, default=20261013)
    ap.add_argument("--json", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.file is None:
        ap.error("a point file is required (or --self-test)")
    cx, cy = (int(c) for c in args.cols.split(","))
    delim = "," if args.file.suffix.lower() == ".csv" else None
    raw = np.loadtxt(args.file, delimiter=delim, usecols=(cx, cy), comments="#")
    pots = [parse_potential(s) for s in args.potentials.split(",")]
    res = analyse(raw, pots, args.seed)
    print(render(res))
    if args.json:
        args.json.write_text(json.dumps(res, indent=2) + "\n")
    return 1 if any(r["gap"] < -r["tol"] for r in res["potentials"].values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
