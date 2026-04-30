from __future__ import annotations

from typing import Sequence

from .models import DesignPoint

VALUE_FORMAT = ".12g"


def format_numeric_value(value: float) -> str:
    return format(value, VALUE_FORMAT)


def bayes_file_name(index: int) -> str:
    return f"bayes_file_{index}.dat"


def render_bayes_file(design_point: DesignPoint) -> str:
    lines = [
        f"{parameter_name} {format_numeric_value(parameter_value)}"
        for parameter_name, parameter_value in design_point.parameter_values
    ]
    return "\n".join(lines) + "\n"


def build_design_points_rows(
    parameter_names: Sequence[str],
    design_points: Sequence[DesignPoint],
) -> list[list[str]]:
    rows: list[list[str]] = [["index", *parameter_names]]

    for design_point in design_points:
        rows.append(
            [
                str(design_point.index),
                *[
                    format_numeric_value(parameter_value)
                    for _, parameter_value in design_point.parameter_values
                ],
            ]
        )

    return rows