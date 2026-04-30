from __future__ import annotations

import csv
from pathlib import Path
from typing import Sequence

from .generator import bayes_file_name, build_design_points_rows, render_bayes_file
from .models import AppConfig, DesignPoint


def write_output_files(
    config: AppConfig,
    design_points: Sequence[DesignPoint],
) -> tuple[Path, tuple[Path, ...]]:
    output_dir = config.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    bayes_dir = output_dir / "bayes_files"
    bayes_dir.mkdir(parents=True, exist_ok=True)

    for stale_file in bayes_dir.glob("bayes_file_*.dat"):
        if stale_file.is_file():
            stale_file.unlink()

    design_points_path = output_dir / "design_points.csv"
    parameter_names = [parameter.name for parameter in config.parameters]
    rows = build_design_points_rows(parameter_names, design_points)

    with design_points_path.open("w", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerows(rows)

    bayes_paths: list[Path] = []
    for design_point in design_points:
        bayes_path = bayes_dir / bayes_file_name(design_point.index)
        bayes_path.write_text(render_bayes_file(design_point), encoding="utf-8")
        bayes_paths.append(bayes_path)

    return design_points_path, tuple(bayes_paths)