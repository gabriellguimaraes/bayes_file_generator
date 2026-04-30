from __future__ import annotations

import textwrap

import pytest

from bayes_file_generator.config import ConfigError, load_config


def write_config(tmp_path, content: str):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    return config_path


def test_load_config_accepts_valid_yaml(tmp_path):
    config_path = write_config(
        tmp_path,
        """
        output_dir: ./run_output
        random_seed: 5

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
        """,
    )

    config = load_config(config_path)

    assert config.output_dir == (tmp_path / "run_output").resolve()
    assert config.random_seed == 5
    assert config.sampling.method == "latin_hypercube"
    assert config.sampling.n_design_points == 3
    assert [parameter.name for parameter in config.parameters] == ["eta_over_s", "tau0"]
    assert config.parameters[0].prior.lower == 0.08
    assert config.parameters[0].prior.upper == 0.24


def test_load_config_rejects_unsupported_sampling_method(tmp_path):
    config_path = write_config(
        tmp_path,
        """
        sampling:
          method: sobol
          n_design_points: 3

        parameters:
          - name: eta_over_s
            prior: uniform
            bounds: [0.08, 0.24]
        """,
    )

    with pytest.raises(ConfigError, match="Unsupported sampling method"):
        load_config(config_path)


def test_load_config_rejects_duplicate_parameter_names(tmp_path):
    config_path = write_config(
        tmp_path,
        """
        sampling:
          method: latin_hypercube
          n_design_points: 3

        parameters:
          - name: eta_over_s
            prior: uniform
            bounds: [0.08, 0.24]
          - name: eta_over_s
            prior: uniform
            bounds: [0.1, 0.3]
        """,
    )

    with pytest.raises(ConfigError, match="Duplicate parameter name"):
        load_config(config_path)