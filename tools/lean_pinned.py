#!/usr/bin/env python3
"""Compile the Lean files in lean/ under upstream's pinned Lean 4.34.1 + Mathlib d13f23b7 (openai/math adc7f124).

Machine-specific paths of the original wrapper are replaced by two environment variables:
    OPENAI_MATH_PINNED   path to openai/math's lean/ directory, already built (see BUILD.md)
    LEAN_TOOLCHAIN_BIN   bin/ directory of the leanprover/lean4:v4.34.1 toolchain
Our own modules are compiled to oleans in .olean_out/, which is appended to LEAN_PATH so later files can import them.

Usage:
    python3 tools/lean_pinned.py compile <file.lean> [--olean <Module.Name>] [--timeout S] [--json-out F]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def _env_path(name: str) -> Path:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"environment variable {name} is not set (see BUILD.md)")
    return Path(value)


PINNED = _env_path("OPENAI_MATH_PINNED")
TOOLCHAIN_BIN = _env_path("LEAN_TOOLCHAIN_BIN")
REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "lean"
OUT = REPO / ".olean_out"


def lean_path() -> str:
    env = dict(os.environ, PATH=f"{TOOLCHAIN_BIN}:{os.environ.get('PATH', '')}")
    res = subprocess.run(["lake", "env", "printenv", "LEAN_PATH"], cwd=PINNED, env=env, capture_output=True, text=True, check=True)
    return res.stdout.strip() + ":" + str(OUT)


def compile_file(src: Path, module: str | None, timeout: int) -> dict[str, object]:
    OUT.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, LEAN_PATH=lean_path(), PATH=f"{TOOLCHAIN_BIN}:{os.environ.get('PATH', '')}")
    cmd = [str(TOOLCHAIN_BIN / "lean"), "-DautoImplicit=false", f"--root={ROOT}"]
    if module:
        olean = OUT / (module.replace(".", "/") + ".olean")
        olean.parent.mkdir(parents=True, exist_ok=True)
        cmd += ["-o", str(olean), "-i", str(olean.with_suffix(".ilean"))]
    cmd.append(str(src))
    t0 = time.time()
    try:
        res = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=timeout)
        rc, out = res.returncode, res.stdout + res.stderr
    except subprocess.TimeoutExpired:
        rc, out = -9, "TIMEOUT"
    return {"file": str(src.relative_to(REPO)) if src.is_relative_to(REPO) else str(src), "module": module, "rc": rc,
            "seconds": round(time.time() - t0, 1), "output": out}


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compile")
    c.add_argument("file", type=Path)
    c.add_argument("--olean")
    c.add_argument("--timeout", type=int, default=3000)
    c.add_argument("--json-out", type=Path)
    args = ap.parse_args()
    res = compile_file(args.file.resolve(), args.olean, args.timeout)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(res, indent=2) + "\n")
    print(json.dumps({k: res[k] for k in ("module", "rc", "seconds")}))
    print(str(res["output"])[-6000:])
    return 0 if res["rc"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
