from __future__ import annotations

from random import Random

from .models import AppConfig, DesignPoint, ParameterSpec


def sample_design_points(config: AppConfig) -> list[DesignPoint]:
    rng = Random(config.random_seed)
    unit_samples = _latin_hypercube_samples(
        n_samples=config.sampling.n_design_points,
        n_dimensions=len(config.parameters),
        rng=rng,
    )

    design_points: list[DesignPoint] = []
    for index, unit_sample in enumerate(unit_samples):
        parameter_values = tuple(
            (parameter.name, _scale_unit_value(unit_value, parameter))
            for parameter, unit_value in zip(config.parameters, unit_sample, strict=True)
        )
        design_points.append(DesignPoint(index=index, parameter_values=parameter_values))

    return design_points


def _latin_hypercube_samples(n_samples: int, n_dimensions: int, rng: Random) -> list[list[float]]:
    columns: list[list[float]] = []

    for _ in range(n_dimensions):
        column = [((sample_index + rng.random()) / n_samples) for sample_index in range(n_samples)]
        rng.shuffle(column)
        columns.append(column)

    return [
        [columns[dimension_index][sample_index] for dimension_index in range(n_dimensions)]
        for sample_index in range(n_samples)
    ]


def _scale_unit_value(unit_value: float, parameter: ParameterSpec) -> float:
    lower = parameter.prior.lower
    upper = parameter.prior.upper
    return lower + (upper - lower) * unit_value