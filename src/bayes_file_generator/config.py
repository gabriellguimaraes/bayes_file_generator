from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import AppConfig, ParameterSpec, PriorSpec, SamplingConfig

DEFAULT_OUTPUT_DIR = "output"
SUPPORTED_PRIOR = "uniform"
SUPPORTED_SAMPLING_METHOD = "latin_hypercube"


class ConfigError(ValueError):
    """Raised when the input config is missing required fields or values."""


def load_config(config_path: str | Path) -> AppConfig:
    config_file = Path(config_path).expanduser().resolve()

    try:
        with config_file.open("r", encoding="utf-8") as handle:
            raw_config = yaml.safe_load(handle)
    except FileNotFoundError as exc:
        raise ConfigError(f"Config file not found: {config_file}") from exc
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in config file: {config_file}") from exc
    except OSError as exc:
        raise ConfigError(f"Unable to read config file: {config_file}") from exc

    return parse_config(raw_config, config_file)


def parse_config(raw_config: Any, config_file: Path) -> AppConfig:
    config_data = _require_mapping(raw_config, "Top-level config")

    output_dir_value = config_data.get("output_dir", DEFAULT_OUTPUT_DIR)
    output_dir = resolve_path(output_dir_value, base_dir=config_file.parent, field_name="output_dir")

    random_seed = config_data.get("random_seed")
    if random_seed is not None and not _is_int(random_seed):
        raise ConfigError("random_seed must be an integer when provided")

    sampling_data = _require_mapping(config_data.get("sampling"), "sampling")
    sampling_method = _require_string(sampling_data.get("method"), "sampling.method")
    if sampling_method != SUPPORTED_SAMPLING_METHOD:
        raise ConfigError(
            f"Unsupported sampling method '{sampling_method}'. Expected '{SUPPORTED_SAMPLING_METHOD}'."
        )

    n_design_points = _require_positive_int(
        sampling_data.get("n_design_points"),
        "sampling.n_design_points",
    )

    raw_parameters = _require_list(config_data.get("parameters"), "parameters")
    if not raw_parameters:
        raise ConfigError("parameters must contain at least one entry")

    seen_names: set[str] = set()
    parameters: list[ParameterSpec] = []
    for index, raw_parameter in enumerate(raw_parameters):
        parameter = _parse_parameter(raw_parameter, index)
        if parameter.name in seen_names:
            raise ConfigError(f"Duplicate parameter name: {parameter.name}")
        seen_names.add(parameter.name)
        parameters.append(parameter)

    return AppConfig(
        config_path=config_file,
        output_dir=output_dir,
        random_seed=None if random_seed is None else int(random_seed),
        sampling=SamplingConfig(
            method=sampling_method,
            n_design_points=n_design_points,
        ),
        parameters=tuple(parameters),
    )


def resolve_path(path_value: str | Path, *, base_dir: Path, field_name: str) -> Path:
    if not isinstance(path_value, (str, Path)):
        raise ConfigError(f"{field_name} must be a path string")

    candidate = Path(path_value)
    if candidate == Path():
        raise ConfigError(f"{field_name} must not be empty")

    if candidate.is_absolute():
        return candidate.resolve()

    return (base_dir / candidate).resolve()


def _parse_parameter(raw_parameter: Any, index: int) -> ParameterSpec:
    parameter_data = _require_mapping(raw_parameter, f"parameters[{index}]")

    name = _require_string(parameter_data.get("name"), f"parameters[{index}].name")
    prior_kind = _require_string(parameter_data.get("prior"), f"parameters[{index}].prior")
    if prior_kind != SUPPORTED_PRIOR:
        raise ConfigError(
            f"Unsupported prior '{prior_kind}' for parameter '{name}'. Expected '{SUPPORTED_PRIOR}'."
        )

    lower, upper = _require_bounds(parameter_data.get("bounds"), f"parameters[{index}].bounds")
    if lower >= upper:
        raise ConfigError(
            f"parameters[{index}].bounds must contain an increasing [min, max] pair"
        )

    return ParameterSpec(name=name, prior=PriorSpec(kind=prior_kind, lower=lower, upper=upper))


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigError(f"{field_name} must be a mapping")
    return value


def _require_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ConfigError(f"{field_name} must be a list")
    return value


def _require_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_positive_int(value: Any, field_name: str) -> int:
    if not _is_int(value) or int(value) <= 0:
        raise ConfigError(f"{field_name} must be a positive integer")
    return int(value)


def _require_bounds(value: Any, field_name: str) -> tuple[float, float]:
    if not isinstance(value, list) or len(value) != 2:
        raise ConfigError(f"{field_name} must be a two-element list")

    lower, upper = value
    if not _is_number(lower) or not _is_number(upper):
        raise ConfigError(f"{field_name} must contain numeric values")

    return float(lower), float(upper)


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)