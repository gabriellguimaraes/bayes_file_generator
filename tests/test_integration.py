from __future__ import annotations

import textwrap

from bayes_file_generator.cli import main


def test_main_generates_outputs_from_yaml_config(tmp_path, capsys):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        textwrap.dedent(
            """
            output_dir: ./generated_output
            random_seed: 9

            sampling:
              method: latin_hypercube
              n_design_points: 3

            parameters:
              - name: eta_over_s
                prior: uniform
                bounds: [0.08, 0.24]
              - name: tau0
                prior: uniform
                bounds: [0.2, 1.0]
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )

    exit_code = main([str(config_path)])

    assert exit_code == 0

    output_dir = tmp_path / "generated_output"
    design_points_path = output_dir / "design_points.csv"
    bayes_dir = output_dir / "bayes_files"

    assert design_points_path.exists()
    assert design_points_path.read_text(encoding="utf-8").splitlines()[0] == "index,eta_over_s,tau0"
    assert sorted(path.name for path in bayes_dir.glob("bayes_file_*.dat")) == [
        "bayes_file_0.dat",
        "bayes_file_1.dat",
        "bayes_file_2.dat",
    ]
    assert "Wrote" in capsys.readouterr().out