#!/usr/bin/env python3
"""P1: real-data consistency check of the D2 energy bound on measured skyrmion lattices (Zenodo 4450305).

D2 (with upstream `universal_energy_minimum`) says: for every completely monotone g of squared distance and every
locally finite configuration C of density rho, the per-point g-energy of C is at least that of the triangular lattice
at density rho. This script feeds two experimentally measured 2D configurations into that inequality, with the
estimator, tolerance, controls and kill criterion fixed in prereg/P1_skyrmion.json before it was run on the data.

Usage: python3 physics/skyrmion_check.py [--out physics/results] [--cache physics/data]
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import mpmath
import numpy as np
from scipy.spatial import Voronoi, cKDTree
from scipy.stats import spearmanr

RECORD = "4450305"
ZIP_KEY = "Skyrmion Lattice Phases Ascii Data.zip"
SNAPSHOTS = {"330K_40uT": "fig3/FIG_snap_absPsi6_330K_40uT.dat", "338K_20uT": "fig3/FIG_snap_absPsi6_338K_20uT.dat"}
RC = 6.0  # cutoff radius in density-1 units (prereg)
N_CONTROL_SEEDS = 20
JITTERS = (0.05, 0.1, 0.2)
MISMATCH = 1.3


@dataclass(frozen=True)
class Potential:
    name: str
    g: Callable[[np.ndarray], np.ndarray]  # function of squared distance t, density-1 units
    tail: float  # uniform-density contribution beyond RC
    s: float | None  # Riesz exponent, None for Gaussians


def potentials() -> list[Potential]:
    out = [Potential(f"gauss_a{a:g}", (lambda t, a=a: np.exp(-math.pi * a * t)), 0.0, None) for a in (0.5, 1, 2, 4)]
    out += [Potential(f"riesz_s{s}", (lambda t, s=s: t ** (-s / 2)), 2 * math.pi * RC ** (2 - s) / (s - 2), float(s))
            for s in (3, 4, 6)]
    return out


# ---------------------------------------------------------------- triangular lattice, density 1
C_TRI = math.sqrt(2 / math.sqrt(3))
B1 = np.array([C_TRI, 0.0])
B2 = np.array([C_TRI / 2, C_TRI * math.sqrt(3) / 2])


def lattice_points(radius: float) -> np.ndarray:
    k = int(radius / (C_TRI * math.sqrt(3) / 2)) + 2
    j, i = np.meshgrid(np.arange(-k, k + 1), np.arange(-k, k + 1))
    pts = i.reshape(-1, 1) * B1 + j.reshape(-1, 1) * B2
    return pts[np.linalg.norm(pts, axis=1) <= radius]


def riesz_lattice_closed_form(s: float) -> float:
    """Sum over A minus 0 of |a|^{-s} at density 1: (2/sqrt3)^{-s/2} * 6 zeta(s/2) L(s/2, chi_{-3})."""
    sig = mpmath.mpf(s) / 2
    l_chi = mpmath.power(3, -sig) * (mpmath.zeta(sig, mpmath.mpf(1) / 3) - mpmath.zeta(sig, mpmath.mpf(2) / 3))
    return float(mpmath.power(2 / mpmath.sqrt(3), -sig) * 6 * mpmath.zeta(sig) * l_chi)


def lattice_energy(p: Potential, density: float = 1.0) -> tuple[float, float]:
    """(value, cross-check). Lattice at `density` evaluated in density-1 units: sum g(|a|^2 / density)."""
    pts = lattice_points(60.0)
    t = np.sum(pts ** 2, axis=1)
    t = t[t > 1e-12] / density
    direct = float(np.sum(p.g(t)))
    if p.s is None:
        return direct, direct
    # Riesz: closed form is exact; direct sum + continuum tail beyond radius 60 is the cross-check
    scale = density ** (p.s / 2)  # sum (|a|^2/density)^{-s/2} = density^{s/2} sum |a|^{-s}
    closed = riesz_lattice_closed_form(p.s) * scale
    return closed, direct + scale * 2 * math.pi * 60.0 ** (2 - p.s) / (p.s - 2)


# ---------------------------------------------------------------- estimator (prereg)
def inner_mask(pts: np.ndarray, lo: np.ndarray, hi: np.ndarray, margin: float) -> np.ndarray:
    return np.all((pts >= lo + margin) & (pts <= hi - margin), axis=1)


DENSITY_MODE = "box"  # "box" = P1/P1b estimator; "voronoi" = P2 (set from the command line)


def polygon_area(v: np.ndarray) -> float:
    x, y = v[:, 0], v[:, 1]
    return 0.5 * abs(float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))))


def voronoi_density(raw: np.ndarray, inner: np.ndarray) -> float:
    """Number of inner points / total Voronoi area of their cells (cells of inner points are bounded)."""
    vor = Voronoi(raw)
    total = 0.0
    for i in np.flatnonzero(inner):
        reg = vor.regions[vor.point_region[i]]
        if not reg or -1 in reg:
            raise ValueError("unbounded Voronoi cell for an inner point")
        total += polygon_area(vor.vertices[reg])
    return inner.sum() / total


def to_density_one(raw: np.ndarray) -> tuple[np.ndarray, float]:
    """Rescale so the estimated density is 1. Returns (points in density-1 units, rho_hat in raw units)."""
    lo, hi = raw.min(0), raw.max(0)
    rho = len(raw) / float(np.prod(hi - lo))
    for _ in range(2):  # initial estimate, then iterated once (prereg)
        m = RC / math.sqrt(rho)
        inner = inner_mask(raw, lo, hi, m)
        if DENSITY_MODE == "voronoi":
            rho = voronoi_density(raw, inner)
        else:
            rho = inner.sum() / float(np.prod(hi - lo - 2 * m))
    return raw * math.sqrt(rho), rho


def per_point_energies(pts: np.ndarray, pots: list[Potential]) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    lo, hi = pts.min(0), pts.max(0)
    inner = np.flatnonzero(inner_mask(pts, lo, hi, RC))
    tree = cKDTree(pts)
    nbrs = tree.query_ball_point(pts[inner], RC)
    out = {p.name: np.empty(len(inner)) for p in pots}
    for row, (i, nb) in enumerate(zip(inner, nbrs)):
        nb = np.asarray([j for j in nb if j != i])
        t = np.sum((pts[nb] - pts[i]) ** 2, axis=1)
        for p in pots:
            out[p.name][row] = float(np.sum(p.g(t))) + p.tail
    return inner, out


def gaps(pts_raw: np.ndarray, pots: list[Potential], density_factor: float = 1.0) -> dict[str, float]:
    pts, _ = to_density_one(pts_raw)
    _, e = per_point_energies(pts, pots)
    res = {}
    for p in pots:
        lat, _ = lattice_energy(p, density_factor)
        res[p.name] = (float(e[p.name].mean()) - lat) / lat
    return res


# ---------------------------------------------------------------- synthetic controls
def patch(kind: str, n: int, aspect: float, rng: np.random.Generator, jitter: float = 0.0) -> np.ndarray:
    """~n points of a density-1 triangular (or square) lattice, random rotation/offset, in a box of area n."""
    w, h = math.sqrt(n * aspect), math.sqrt(n / aspect)
    r = math.hypot(w, h) / 2 + 3
    if kind == "tri":
        base = lattice_points(r)
    else:
        k = int(r) + 2
        g = np.arange(-k, k + 1, dtype=float)
        base = np.stack(np.meshgrid(g, g), -1).reshape(-1, 2)
    th = rng.uniform(0, 2 * math.pi)
    rot = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    pts = base @ rot.T + rng.uniform(-1, 1, 2)
    pts = pts[(np.abs(pts[:, 0]) <= w / 2) & (np.abs(pts[:, 1]) <= h / 2)]
    if jitter:
        pts = pts + rng.normal(0, jitter, pts.shape)
    return pts


# ---------------------------------------------------------------- data
def fetch(cache: Path) -> tuple[dict[str, np.ndarray], dict[str, str]]:
    meta = json.load(urllib.request.urlopen(f"https://zenodo.org/api/records/{RECORD}"))
    fmeta = next(f for f in meta["files"] if f["key"] == ZIP_KEY)
    cache.mkdir(parents=True, exist_ok=True)
    zpath = cache / f"zenodo_{RECORD}.zip"
    if not zpath.exists():
        urllib.request.urlretrieve(fmeta["links"]["self"], zpath)
    algo, want = fmeta["checksum"].split(":")
    got = hashlib.new(algo, zpath.read_bytes()).hexdigest()
    if got != want:
        raise SystemExit(f"checksum mismatch for {zpath}: {got} != {want}")
    z = zipfile.ZipFile(zpath)
    data = {k: np.loadtxt(io.BytesIO(z.read(v))) for k, v in SNAPSHOTS.items()}
    prov = {"record": RECORD, "doi": meta.get("doi", ""), "license": meta["metadata"].get("license", {}).get("id", ""),
            "file": ZIP_KEY, "checksum": fmeta["checksum"], "checksum_verified": "yes"}
    return data, prov


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("physics/results"))
    ap.add_argument("--cache", type=Path, default=Path("physics/data"))
    ap.add_argument("--tol-mode", choices=["global", "per-potential"], default="global",
                    help="global = P1 as preregistered; per-potential = amendment P1b")
    ap.add_argument("--seed", type=int, default=20261011, help="P1: 20261011; P1b: 20261012")
    ap.add_argument("--tag", default="P1")
    ap.add_argument("--density", choices=["box", "voronoi"], default="box", help="box = P1/P1b; voronoi = P2")
    args = ap.parse_args()
    global DENSITY_MODE
    DENSITY_MODE = args.density
    pots = potentials()
    rng = np.random.default_rng(args.seed)

    lattice = {}
    for p in pots:
        v, x = lattice_energy(p)
        lattice[p.name] = {"value": v, "cross_check": x, "rel_diff": abs(v - x) / v}

    data, prov = fetch(args.cache)
    report: dict[str, object] = {"provenance": prov, "lattice_energy_density1": lattice, "snapshots": {}}
    problems: list[str] = []

    for name, arr in data.items():
        xy, psi6 = arr[:, :2], arr[:, 2]
        aspect = float(np.ptp(xy[:, 0]) / np.ptp(xy[:, 1]))
        n = len(xy)
        # C1 calibrates tol before the data are evaluated
        c1 = [gaps(patch("tri", n, aspect, rng), pots) for _ in range(N_CONTROL_SEEDS)]
        c1_max_p = {p.name: max(abs(run[p.name]) for run in c1) for p in pots}
        c1_mean_p = {p.name: float(np.mean([run[p.name] for run in c1])) for p in pots}
        c1_max = max(c1_max_p.values())
        if args.tol_mode == "global":
            tol_p = {p.name: 3 * c1_max for p in pots}
        else:
            tol_p = {k: 3 * v for k, v in c1_max_p.items()}
        c2 = {sig: gaps(patch("tri", n, aspect, rng, jitter=sig), pots) for sig in JITTERS}
        c3 = gaps(patch("sq", n, aspect, rng), pots)
        real = gaps(xy, pots)
        c4 = gaps(xy, pots, density_factor=MISMATCH)

        unresolved = []
        for p in pots:
            tol = tol_p[p.name]
            bad = []
            if real[p.name] < -tol:
                problems.append(f"{name} {p.name}: data gap {real[p.name]:.3e} < -tol {-tol:.3e}  (KILL)")
            seq = [c2[s][p.name] for s in JITTERS]
            if not (seq[0] > tol and all(b > a for a, b in zip(seq, seq[1:]))):
                bad.append(f"C2 jitter gaps {['%.2e' % v for v in seq]} not all > tol {tol:.2e} and increasing")
            if c3[p.name] <= tol:
                bad.append(f"C3 square gap {c3[p.name]:.3e} <= tol {tol:.2e}")
            if bad:
                unresolved.append(p.name)
                problems += [f"{name} {p.name}: {b}" for b in bad]
        if not any(c4[p.name] < -tol_p[p.name] for p in pots):
            problems.append(f"{name}: C4 density mismatch never violated the bound (test cannot fail)")

        # exploratory (not gated): local excess vs measured |psi6|
        pts, rho = to_density_one(xy)
        inner, e = per_point_energies(pts, pots)
        lat1 = lattice["gauss_a1"]["value"]
        rs = spearmanr(e["gauss_a1"] - lat1, psi6[inner])
        report["snapshots"][name] = {
            "n_points": n, "n_inner": int(len(inner)), "rho_hat_per_um2": rho,
            "mean_spacing_um": math.sqrt(2 / (math.sqrt(3) * rho)), "tol_mode": args.tol_mode, "seed": args.seed,
            "density_estimator": args.density,
            "tol": tol_p, "C1_max_abs_gap": c1_max_p, "C1_mean_gap": c1_mean_p,
            "data_gap": real, "data_gap_bias_corrected": {k: real[k] - c1_mean_p[k] for k in real},
            "beyond_resolution": unresolved,
            "C2_jitter_gap": {str(k): v for k, v in c2.items()}, "C3_square_gap": c3,
            "C4_mismatch_gap": c4,
            "exploratory_spearman_gauss1_excess_vs_psi6": {"rho": float(rs.statistic), "p": float(rs.pvalue)},
        }

    report["gate"] = "PASS" if not problems else "FAIL"
    report["problems"] = problems
    args.out.mkdir(parents=True, exist_ok=True)
    report["tag"] = args.tag
    (args.out / f"{args.tag}_skyrmion.json").write_text(json.dumps(report, indent=2) + "\n")
    (args.out / f"{args.tag}_skyrmion.md").write_text(render(report, pots))
    print(render(report, pots))
    return 0 if not problems else 1


def render(r: dict, pots: list[Potential]) -> str:
    L = [f"# {r.get('tag', 'P1')}: D2 energy bound vs measured skyrmion lattices (Zenodo 4450305)", "",
         "Generated by `physics/skyrmion_check.py`; preregistration `prereg/P1_skyrmion.json`"
         + (" with amendment `prereg/P1b_skyrmion_amendment.json` (post-hoc, not blind)" if r.get("tag") == "P1b" else "")
         + (" superseded by `prereg/P2_skyrmion_voronoi.json` (Voronoi density estimator)" if r.get("tag") == "P2" else "")
         + ". Relative gap = "
         "(E_data - E_lattice) / E_lattice at the same density; the theorem's reading predicts gap >= -tol.", "",
         f"Data: doi:{r['provenance']['doi']} ({r['provenance']['license']}), `{r['provenance']['file']}`, "
         f"{r['provenance']['checksum']} (verified).", "",
         "## Lattice energies at density 1", "", "| Potential | value | cross-check rel. diff |", "|---|---|---|"]
    for k, v in r["lattice_energy_density1"].items():
        L.append(f"| {k} | {v['value']:.10g} | {v['rel_diff']:.1e} |")
    for name, s in r["snapshots"].items():
        L += ["", f"## Snapshot {name}: {s['n_points']} skyrmions ({s['n_inner']} inner), mean spacing "
              f"{s['mean_spacing_um']:.2f} um, tolerance mode {s['tol_mode']}, seed {s['seed']}", "",
              "| Potential | tol | data gap | bias-corrected | C2 jitter 0.05 / 0.1 / 0.2 | C3 square | C4 density x1.3 | resolved |",
              "|---|---|---|---|---|---|---|---|"]
        for p in pots:
            c2 = " / ".join(f"{s['C2_jitter_gap'][str(j)][p.name]:+.2e}" for j in JITTERS)
            ok = "no" if p.name in s["beyond_resolution"] else "yes"
            L.append(f"| {p.name} | {s['tol'][p.name]:.1e} | **{s['data_gap'][p.name]:+.3e}** | "
                     f"{s['data_gap_bias_corrected'][p.name]:+.3e} | {c2} | {s['C3_square_gap'][p.name]:+.2e} | "
                     f"{s['C4_mismatch_gap'][p.name]:+.2e} | {ok} |")
        sp = s["exploratory_spearman_gauss1_excess_vs_psi6"]
        L += ["", f"Exploratory (not gated): Spearman(local Gaussian-1 excess, |psi6|) = {sp['rho']:+.3f} (p = {sp['p']:.1e})."]
    L += ["", f"## GATE: {r['gate']}"] + [f"- {p}" for p in r["problems"]]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
