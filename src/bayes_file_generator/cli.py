from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from pathlib import Path
from typing import Sequence

from .config import ConfigError, load_config, resolve_path
from .io import write_output_files
from .sampler import sample_design_points


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate Latin hypercube design points and per-point bayes files "
            "for iEBE-MUSIC-style workflows."
        )
    )
    parser.add_argument("config", type=Path, help="Path to the YAML configuration file")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Override the output directory defined in the config",
    )
    return parser


def run_generation(
    config_path: str | Path,
    output_dir_override: str | Path | None = None,
) -> tuple[Path, tuple[Path, ...]]:
    config = load_config(config_path)

    if output_dir_override is not None:
        config = replace(
            config,
            output_dir=resolve_path(
                output_dir_override,
                base_dir=Path.cwd(),
                field_name="output_dir",
            ),
        )

    design_points = sample_design_points(config)
    return write_output_files(config, design_points)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        design_points_path, bayes_paths = run_generation(args.config, args.output_dir)
    except (ConfigError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {design_points_path} and {len(bayes_paths)} bayes files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())