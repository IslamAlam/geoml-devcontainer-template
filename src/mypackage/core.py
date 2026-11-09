"""Small example functions. Replace them with your own code."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def linear_to_db(intensity: npt.ArrayLike, floor: float = 1e-10) -> npt.NDArray[np.float64]:
    """Convert linear SAR intensity (e.g. sigma0) to decibels.

    Values below ``floor`` are clipped to avoid ``log10(0)``.

    Args:
        intensity: Linear intensity values.
        floor: Smallest value used before taking the logarithm.

    Returns:
        The intensity in dB.

    Examples:
        >>> linear_to_db([1.0, 0.1]).tolist()
        [0.0, -10.0]
    """
    values = np.asarray(intensity, dtype=np.float64)
    result: npt.NDArray[np.float64] = 10.0 * np.log10(np.maximum(values, floor))
    return result


def normalize(image: npt.ArrayLike, eps: float = 1e-12) -> npt.NDArray[np.float64]:
    """Scale an array to zero mean and unit standard deviation, ignoring NaNs.

    Args:
        image: Input array, e.g. a SAR backscatter image in dB.
        eps: Small constant that prevents division by zero for constant images.

    Returns:
        The normalized array, with NaNs preserved.

    Examples:
        >>> normalize([1.0, 3.0]).round(6).tolist()
        [-1.0, 1.0]
    """
    values = np.asarray(image, dtype=np.float64)
    mean = np.nanmean(values)
    std = np.nanstd(values)
    result: npt.NDArray[np.float64] = (values - mean) / (std + eps)
    return result
