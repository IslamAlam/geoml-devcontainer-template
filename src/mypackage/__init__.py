"""mypackage: a Python package for geospatial / SAR machine learning."""

from importlib.metadata import PackageNotFoundError, version

from mypackage.core import linear_to_db, normalize

try:
    __version__ = version("mypackage")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"

__all__ = ["__version__", "linear_to_db", "normalize"]
