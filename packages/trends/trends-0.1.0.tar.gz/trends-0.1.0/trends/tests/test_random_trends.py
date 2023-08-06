"""Unit tests for trends."""
# Prevent complaints about fixtures.
#   pylint: disable=redefined-outer-name

import random
from operator import gt as falling_trend
from operator import lt as rising_trend
from typing import Tuple

import pytest

from trends.trends import Trend, Trendlist, _average_merge, random_trends

FIXED_SEED = 1.0


@pytest.fixture(scope="function")
def random_trend_singleton() -> Trendlist:
    """Return up- and down-Trendlist from single Trend with fixed seed."""
    random.seed(FIXED_SEED)
    trendlist = Trendlist([Trend(random.random())])
    return trendlist


@pytest.fixture(scope="function")
def random_trend_pair() -> Tuple[Trend, Trend]:
    """Return up- and down-Trendlist from Trend pair with fixed seed."""
    random.seed(FIXED_SEED)
    trend_1 = Trend(random.random())
    trend_2 = Trend(random.random())
    return trend_1, trend_2


def test_trivial_random_trends(random_trend_singleton) -> None:
    """Unit-test random_trends."""
    trendlist = random_trend_singleton
    assert random_trends(seq_length=0) == ([], [])
    assert random_trends(seq_length=0, seed=FIXED_SEED) == ([], [])
    assert random_trends(seq_length=1, seed=FIXED_SEED) == (trendlist, trendlist)


def test_random_trends(random_trend_pair) -> None:
    """Make a random_trends_pair."""
    trend_1, trend_2 = random_trend_pair
    up_exp = _average_merge([trend_1], trend_2, are_one_trend=rising_trend)
    down_exp = _average_merge([trend_1], trend_2, are_one_trend=falling_trend)
    up_trs, down_trs = random_trends(seq_length=2, seed=FIXED_SEED)
    assert isinstance(up_trs, Trendlist)
    assert isinstance(down_trs, Trendlist)
    assert up_trs == up_exp
    assert down_trs == down_exp


def test_random_trends_direction(random_trend_pair) -> None:
    """Specify up- or down- trend."""
    trend_1, trend_2 = random_trend_pair
    up_exp = _average_merge([trend_1], trend_2, are_one_trend=rising_trend)
    down_exp = _average_merge([trend_1], trend_2, are_one_trend=falling_trend)
    assert random_trends(
        seq_length=2, seed=FIXED_SEED, direction="both"
    ) == random_trends(seq_length=2, seed=FIXED_SEED)
    up_trs, down_trs = random_trends(seq_length=2, seed=FIXED_SEED, direction="up")
    assert up_trs == up_exp
    assert not down_trs
    up_trs, down_trs = random_trends(seq_length=2, seed=FIXED_SEED, direction="down")
    assert not up_trs
    assert down_trs == down_exp


def test_random_trends_direction_err() -> None:
    """A bogus direction raises ValueError."""
    with pytest.raises(ValueError) as excerr:
        random_trends(seq_length=1, seed=FIXED_SEED, direction="foo")
    assert str(excerr.value) == "direction must be in {'up', 'down', 'both'}"
