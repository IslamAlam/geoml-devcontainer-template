import numpy as np
import pytest

from mypackage import linear_to_db, normalize


def test_linear_to_db_known_values() -> None:
    np.testing.assert_allclose(linear_to_db([1.0, 10.0, 0.01]), [0.0, 10.0, -20.0])


def test_linear_to_db_clips_zero() -> None:
    assert np.isfinite(linear_to_db([0.0])).all()


def test_normalize_zero_mean_unit_std() -> None:
    rng = np.random.default_rng(0)
    out = normalize(rng.normal(5.0, 3.0, size=(64, 64)))
    assert out.mean() == pytest.approx(0.0, abs=1e-9)
    assert out.std() == pytest.approx(1.0, rel=1e-9)


def test_normalize_keeps_nans() -> None:
    out = normalize([1.0, np.nan, 3.0])
    assert np.isnan(out[1])
    np.testing.assert_allclose(out[[0, 2]], [-1.0, 1.0])
