from __future__ import annotations

from pathlib import Path

from bayes_file_generator.models import AppConfig, ParameterSpec, PriorSpec, SamplingConfig
from bayes_file_generator.sampler import sample_design_points


def build_config(seed: int | None = 11) -> AppConfig:
    return AppConfig(
        config_path=Path("config.yaml"),
        output_dir=Path("output"),
        random_seed=seed,
        sampling=SamplingConfig(method="latin_hypercube", n_design_points=4),
        parameters=(
            ParameterSpec(name="eta_over_s", prior=PriorSpec(kind="uniform", lower=0.08, upper=0.24)),
            ParameterSpec(name="tau0", prior=PriorSpec(kind="uniform", lower=0.2, upper=1.0)),
        ),
    )


def test_sample_design_points_respects_bounds_and_indices():
    design_points = sample_design_points(build_config())

    assert len(design_points) == 4
    assert [design_point.index for design_point in design_points] == [0, 1, 2, 3]

    for design_point in design_points:
        values = dict(design_point.parameter_values)
        assert 0.08 <= values["eta_over_s"] <= 0.24
        assert 0.2 <= values["tau0"] <= 1.0


def test_sample_design_points_is_deterministic_with_fixed_seed():
    first_run = sample_design_points(build_config(seed=23))
    second_run = sample_design_points(build_config(seed=23))

    assert first_run == second_run