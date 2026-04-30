from __future__ import annotations

from pathlib import Path

from bayes_file_generator.io import write_output_files
from bayes_file_generator.models import AppConfig, DesignPoint, ParameterSpec, PriorSpec, SamplingConfig


def build_config(output_dir: Path) -> AppConfig:
    return AppConfig(
        config_path=Path("config.yaml"),
        output_dir=output_dir,
        random_seed=7,
        sampling=SamplingConfig(method="latin_hypercube", n_design_points=2),
        parameters=(
            ParameterSpec(name="eta_over_s", prior=PriorSpec(kind="uniform", lower=0.08, upper=0.24)),
            ParameterSpec(name="tau0", prior=PriorSpec(kind="uniform", lower=0.2, upper=1.0)),
        ),
    )


def test_write_output_files_creates_expected_csv_and_bayes_files(tmp_path):
    output_dir = tmp_path / "generated"
    config = build_config(output_dir)
    design_points = (
        DesignPoint(index=0, parameter_values=(("eta_over_s", 0.125), ("tau0", 0.45))),
        DesignPoint(index=1, parameter_values=(("eta_over_s", 0.2), ("tau0", 0.8))),
    )

    stale_file = output_dir / "bayes_files" / "bayes_file_99.dat"
    stale_file.parent.mkdir(parents=True, exist_ok=True)
    stale_file.write_text("stale\n", encoding="utf-8")

    design_points_path, bayes_paths = write_output_files(config, design_points)

    assert not stale_file.exists()
    assert design_points_path.exists()
    assert [path.name for path in bayes_paths] == ["bayes_file_0.dat", "bayes_file_1.dat"]
    assert design_points_path.read_text(encoding="utf-8").splitlines() == [
        "index,eta_over_s,tau0",
        "0,0.125,0.45",
        "1,0.2,0.8",
    ]
    assert bayes_paths[0].read_text(encoding="utf-8") == "eta_over_s 0.125\ntau0 0.45\n"
