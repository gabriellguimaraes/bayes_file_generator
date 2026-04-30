"""Bayes file generator package."""

from importlib.metadata import PackageNotFoundError, version

from .cli import run_generation

try:
    __version__ = version("bayes-file-generator")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

__all__ = ["run_generation", "__version__"]