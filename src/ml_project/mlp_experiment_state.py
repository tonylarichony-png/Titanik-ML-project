"""Synchronize MLP decisions from Obsidian cards without retraining."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Keep direct execution reliable on machines with many logical CPUs or little
# free memory. The sync itself does not benefit from threaded BLAS.
for variable in (
    "OPENBLAS_NUM_THREADS",
    "OMP_NUM_THREADS",
    "OMP_THREAD_LIMIT",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ.setdefault(variable, "1")

try:
    from .mlp_experiment import sync_mlp_state
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from ml_project.mlp_experiment import sync_mlp_state


def main(argv: list[str] | None = None) -> int:
    """Запустить команду модуля из командной строки."""
    parser = argparse.ArgumentParser(description="Synchronize MLP experiment decisions.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    result = sync_mlp_state(args.project_root)
    print("MLP state synchronized:", result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
