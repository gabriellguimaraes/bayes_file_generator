from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PriorSpec:
    kind: str
    lower: float
    upper: float


@dataclass(frozen=True)
class ParameterSpec:
    name: str
    prior: PriorSpec


@dataclass(frozen=True)
class SamplingConfig:
    method: str
    n_design_points: int


@dataclass(frozen=True)
class AppConfig:
    config_path: Path
    output_dir: Path
    random_seed: int | None
    sampling: SamplingConfig
    parameters: tuple[ParameterSpec, ...]


@dataclass(frozen=True)
class DesignPoint:
    index: int
    parameter_values: tuple[tuple[str, float], ...]