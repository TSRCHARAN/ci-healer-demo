import pytest

from shop.stats import mean, median


def test_mean():
    assert mean([1, 2, 3, 4]) == 2.5


def test_median_odd():
    assert median([3, 1, 2]) == 2


def test_median_even():
    assert median([4, 1, 3, 2]) == 2.5


def test_empty_inputs_raise():
    with pytest.raises(ValueError):
        mean([])
    with pytest.raises(ValueError):
        median([])
