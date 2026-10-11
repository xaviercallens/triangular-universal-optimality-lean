#!/usr/bin/env python3
"""Figures for the physicist guide, generated from the committed result files (no hand-entered numbers).

Usage (from the repository root): python3 docs/physicist_guide/make_figures.py
Writes docs/physicist_guide/fig_{calibration,theory,data}.pdf and numbers.tex (macros used by guide.tex).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
RES = ROOT / "physics" / "results"
BLUE, ORANGE = "#2a78d6", "#eb6834"  # categorical slots 1-2 (validated: CVD dE 24.7, normal dE 33.6, >= 3:1)
INK, MUTED, GRID = "#1f1f1e", "#6b6a63", "#e4e3de"
SNAP = {"330K_40uT": ("330 K, 40 µT", BLUE, "o"), "338K_20uT": ("338 K, 20 µT", ORANGE, "s")}
LABEL = {"gauss_a0.5": "Gaussian α=0.5", "gauss_a1": "Gaussian α=1", "gauss_a2": "Gaussian α=2",
         "gauss_a4": "Gaussian α=4", "riesz_s3": "Riesz s=3", "riesz_s4": "Riesz s=4", "riesz_s6": "Riesz s=6"}

plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False,
                     "font.family": "DejaVu Sans"})


WORD = {"0.5": "Half", "1": "One", "2": "Two", "3": "Three", "4": "Four", "6": "Six"}


def mname(p: str) -> str:
    """LaTeX-safe (letters only) name for a potential key, e.g. riesz_s3 -> RieszThree."""
    kind, val = p.split("_")
    return ("Gauss" if kind == "gauss" else "Riesz") + WORD[val[1:]]


def square_gap_theory(name: str) -> float:
    """Exact relative energy excess of the density-1 square lattice over the triangular lattice."""
    if name.startswith("riesz"):
        s = int(name.split("_s")[1])
        sig = mpmath.mpf(s) / 2
        beta = mpmath.power(4, -sig) * (mpmath.zeta(sig, 0.25) - mpmath.zeta(sig, 0.75))  # Dirichlet beta
        sq = 4 * mpmath.zeta(sig) * beta
        l_chi = mpmath.power(3, -sig) * (mpmath.zeta(sig, mpmath.mpf(1) / 3) - mpmath.zeta(sig, mpmath.mpf(2) / 3))
        tri = mpmath.power(2 / mpmath.sqrt(3), -sig) * 6 * mpmath.zeta(sig) * l_chi
        return float(sq / tri - 1)
    a = float(name.split("_a")[1])
    q = mpmath.exp(-mpmath.pi * a)
    sq = mpmath.jtheta(3, 0, q) ** 2 - 1
    # triangular: sum over A of exp(-pi a |x|^2), |x|^2 = (2/sqrt3)(j^2+jk+k^2)
    c = 2 / mpmath.sqrt(3)
    tri = mpmath.nsum(lambda j, k: mpmath.exp(-mpmath.pi * a * c * (j * j + j * k + k * k)), [-40, 40], [-40, 40]) - 1
    return float(sq / tri - 1)


def main() -> None:
    p1b = json.loads((RES / "P1b_skyrmion.json").read_text())
    p2 = json.loads((RES / "P2_skyrmion.json").read_text())
    pots = list(p2["snapshots"]["338K_20uT"]["data_gap"].keys())
    macros: list[str] = []

    # ---- Figure 1: calibration error, box (P1b) vs Voronoi (P2), 338 K snapshot
    fig, ax = plt.subplots(figsize=(5.6, 2.6))
    y = list(range(len(pots)))[::-1]
    box = [p1b["snapshots"]["338K_20uT"]["C1_max_abs_gap"][p] for p in pots]
    vor = [p2["snapshots"]["338K_20uT"]["C1_max_abs_gap"][p] for p in pots]
    ax.hlines(y, vor, box, color=GRID, lw=2, zorder=1)
    ax.scatter(box, y, s=36, color=BLUE, marker="o", zorder=3, edgecolor="white", linewidth=1.5,
               label="box count (P1b)")
    ax.scatter(vor, y, s=36, color=ORANGE, marker="s", zorder=3, edgecolor="white", linewidth=1.5,
               label="Voronoi cells (P2)")
    ax.set_xscale("log")
    ax.set_yticks(y, [LABEL[p] for p in pots])
    ax.set_xlabel("largest |relative energy error| on a perfect lattice (20 seeds)")
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 1.18), ncol=2)
    fig.tight_layout()
    fig.savefig(OUT / "fig_calibration.pdf")
    plt.close(fig)

    # ---- Figure 2: measured square-vs-triangle excess vs exact theory (P2 control C3, both snapshots)
    fig, ax = plt.subplots(figsize=(3.4, 3.2))
    rows = []
    for p in pots:
        th = square_gap_theory(p)
        for snap, (lab, col, mk) in SNAP.items():
            meas = p2["snapshots"][snap]["C3_square_gap"][p]
            rows.append((p, snap, th, meas))
            if mk == "o":  # hollow, larger: stays visible where both snapshots coincide
                ax.scatter(th, meas, s=70, facecolor="none", edgecolor=col, linewidth=1.6, zorder=2,
                           label=lab if p == pots[0] else None)
            else:
                ax.scatter(th, meas, s=22, color=col, marker=mk, edgecolor="white", linewidth=0.8, zorder=3,
                           label=lab if p == pots[0] else None)
    lo, hi = 3e-3, 6
    ax.plot([lo, hi], [lo, hi], color=MUTED, lw=1, zorder=1)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_xlabel("exact (closed form / theta series)"); ax.set_ylabel("measured by the estimator")
    ax.grid(color=GRID, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "fig_theory.pdf")
    plt.close(fig)
    worst = max(abs(m - t) / t for _, _, t, m in rows)
    macros.append(f"\\newcommand{{\\SquareWorstRelDev}}{{{100 * worst:.1f}}}")
    for p in pots:
        macros.append(f"\\newcommand{{\\SqTh{mname(p)}}}{{{100 * square_gap_theory(p):.3f}}}")

    # ---- Figure 3: data gaps with tolerance, P2 (exclude the nearest-neighbour-dominated Gaussian a2/a4)
    show = [p for p in pots if p not in ("gauss_a2", "gauss_a4")]
    fig, ax = plt.subplots(figsize=(5.6, 2.5))
    y = list(range(len(show)))[::-1]
    for k, (snap, (lab, col, mk)) in enumerate(SNAP.items()):
        s = p2["snapshots"][snap]
        off = 0.14 if k == 0 else -0.14
        gx = [100 * s["data_gap"][p] for p in show]
        tx = [100 * s["tol"][p] for p in show]
        for yy, t in zip(y, tx):
            ax.add_patch(plt.Rectangle((0, yy + off - 0.09), t, 0.18, color=GRID, zorder=1, lw=0))
        ax.scatter(gx, [yy + off for yy in y], s=34, color=col, marker=mk, edgecolor="white", linewidth=1.2,
                   zorder=3, label=lab)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_yticks(y, [LABEL[p] for p in show])
    ax.set_xlabel("energy above the triangular-lattice bound (%); grey = tolerance")
    ax.set_xscale("symlog", linthresh=1)
    ax.set_xlim(-0.5, 60)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(0.0, 1.0))
    fig.tight_layout()
    fig.savefig(OUT / "fig_data.pdf")
    plt.close(fig)

    # ---- numbers for the text
    for p, v in p2["lattice_energy_density1"].items():
        macros.append(f"\\newcommand{{\\Lat{mname(p)}}}{{{v['value']:.10g}}}")
    yk = json.loads((RES / "ubound_FIG_snap_absPsi6_338K_20uT.json").read_text())["potentials"]
    for k, word in (("yukawa:1", "One"), ("yukawa:2", "Two")):
        macros.append(f"\\newcommand{{\\LatYukawa{word}}}{{{yk[k]['lattice_energy_density1']:.10g}}}")
    for snapfile, tag in (("FIG_snap_absPsi6_330K_40uT", "A"), ("FIG_snap_absPsi6_338K_20uT", "B")):
        u = json.loads((RES / f"ubound_{snapfile}.json").read_text())["potentials"]
        for k, word in (("yukawa:1", "One"), ("yukawa:2", "Two")):
            macros.append(f"\\newcommand{{\\Gap{tag}Yukawa{word}}}{{{100 * u[k]['gap']:.1f}}}")
    for snap in SNAP:
        s = p2["snapshots"][snap]
        tag = "A" if snap.startswith("330") else "B"
        macros.append(f"\\newcommand{{\\N{tag}}}{{{s['n_points']}}}")
        macros.append(f"\\newcommand{{\\Spacing{tag}}}{{{s['mean_spacing_um']:.2f}}}")
        for p in show:
            macros.append(f"\\newcommand{{\\Gap{tag}{mname(p)}}}{{{100 * s['data_gap'][p]:.1f}}}")
    (OUT / "numbers.tex").write_text("% generated by make_figures.py; do not edit\n" + "\n".join(macros) + "\n")
    print("\n".join(macros))


if __name__ == "__main__":
    main()
