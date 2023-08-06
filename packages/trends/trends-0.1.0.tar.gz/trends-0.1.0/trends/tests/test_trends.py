"""Unit tests for trend."""
# Prevent complaints about fixtures.
#   pylint: disable=redefined-outer-name
# TODO: Don't hardwire averages.

from copy import copy
from math import e, pi
from typing import List

import pytest

from trends.trends import Trend


@pytest.fixture(scope="module")
def list_of_trends() -> List:
    """Defind a standard list of test Trendlist.

    Used throughout test suite.
    """
    return [
        Trend(length=5, average=e),
        Trend(average=e),
        Trend(length=10, average=pi),
        Trend(length=3, average=3.0),
        Trend(length=6, average=6.0),
        Trend(length=9, average=5.0),
        Trend(length=1, average=1),
        Trend(length=1, average=2),
        Trend(length=2, average=1.5),
    ]


def test_init(list_of_trends: List) -> None:
    """Test __init__()."""
    trend = list_of_trends[0]
    assert isinstance(trend, Trend)
    assert trend.length == 5
    assert trend.average == e


def test_trend_default(list_of_trends: List) -> None:
    """Test default length of 1."""
    trend = list_of_trends[1]
    assert trend.length == 1


def test_str(list_of_trends: List) -> None:
    """Test __str__()."""
    assert f"{list_of_trends[0]}" == "(5, 2.7)"
    assert str(list_of_trends[0]) == "(5, 2.7)"


def test_eq(list_of_trends: List) -> None:
    """Test __eq__()."""
    assert list_of_trends[0] == list_of_trends[1]
    assert list_of_trends[1] != list_of_trends[2]


def test_lt(list_of_trends: List) -> None:
    """Test dunder inequality functions."""
    assert list_of_trends[0] < list_of_trends[2]
    assert list_of_trends[2] > list_of_trends[0]
    assert not list_of_trends[0] < list_of_trends[0]
    assert not list_of_trends[0] > list_of_trends[0]
    assert list_of_trends[0] <= list_of_trends[1]  # ==
    assert list_of_trends[1] <= list_of_trends[2]  # <
    assert list_of_trends[0] >= list_of_trends[1]  # ==
    assert list_of_trends[2] >= list_of_trends[1]  # >


def test_repr(list_of_trends: List) -> None:
    """Test __repr__()."""
    assert repr(list_of_trends[0]) == "Trend(average=2.718281828459045, length=5)"
    assert repr(list_of_trends[0]) == f"Trend(average={e}, length=5)"


def test_add(list_of_trends: List) -> None:
    """Test addition."""
    ntrend = list_of_trends[3] + list_of_trends[4]
    assert ntrend.length == list_of_trends[5].length
    assert ntrend.average == list_of_trends[5].average
    ntrend = list_of_trends[6] + list_of_trends[7]
    assert ntrend.length == list_of_trends[8].length
    assert ntrend.average == list_of_trends[8].average


def test_iadd(list_of_trends: List) -> None:
    """Test in-place addition."""
    sample = copy(list_of_trends[3])
    sample += list_of_trends[4]
    assert sample == list_of_trends[5]
    assert sample.length == list_of_trends[5].length
    assert sample != list_of_trends[3]  # because it's a copy.


@pytest.mark.parametrize(
    "exception_type, length, average, message",
    [
        (TypeError, None, None, "average must be number"),
        (TypeError, 1, None, "average must be number"),
        (TypeError, None, [1, 2, 3], "average must be number"),
        (TypeError, pi, 1, "length must be integer"),
        (TypeError, "a", 1, "length must be integer"),
        (ValueError, 0, 1, "length must be positive"),
        (ValueError, -1, 1, "length must be positive"),
    ],
)
def test_trend_error(exception_type, length, average, message) -> None:
    """Test error handling."""
    with pytest.raises(exception_type) as excerr:
        Trend(length=length, average=average)
    assert str(excerr.value) == message
