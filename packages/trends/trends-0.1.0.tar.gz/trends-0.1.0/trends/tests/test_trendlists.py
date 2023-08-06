"""Unit tests for trendlists."""
# Prevent complaints about fixtures.
#   pylint: disable=redefined-outer-name
# TODO: don't hardwire averages

from copy import deepcopy
from math import e, pi
from operator import gt as falling_trend
from typing import List

import pytest

from trends.trends import Trend, Trendlist, _average_merge

# N.B.,
#    Decomposing a sequence into a list of maximal upwards trends
#    will produce a list with monotonically decreasing averages!
#    (and vice-versa)


# TODO: make lengths more interesting
@pytest.fixture()
def downtrends_list() -> List["Trend"]:
    """Create a list of downwards trends."""
    downs = [Trend(average) for average in range(100)]
    return downs


# TODO: make lengths more interesting
@pytest.fixture()
def uptrends_list(downtrends_list: List["Trend"]) -> List["Trend"]:
    """Create a list of upwards trends."""
    ups = deepcopy(downtrends_list)
    ups.reverse()
    return ups


def test_average_merge_simple(
    downtrends_list: List["Trend"], uptrends_list: List["Trend"]
) -> None:
    """_average_merge() works in both directions."""
    assert _average_merge([], Trend(0)) == [Trend(0)]
    assert _average_merge(uptrends_list[:-1], uptrends_list[-1]) == uptrends_list
    assert (
        _average_merge(
            downtrends_list[:-1], downtrends_list[-1], are_one_trend=falling_trend
        )
        == downtrends_list
    )


def test_average_merge_fancy() -> None:
    """_average_merge() will do real merges."""
    trendlist = [Trend(1)]
    assert _average_merge(trendlist, Trend(3)) == [Trend(2)]
    trendlist = [Trend(3)]
    assert _average_merge(trendlist, Trend(1), are_one_trend=falling_trend) == [
        Trend(2)
    ]
    trendlist = [Trend(1), Trend(0)]
    assert _average_merge(trendlist, Trend(5)) == [Trend(2)]
    trendlist = [Trend(2), Trend(0)]
    assert _average_merge(trendlist, Trend(2)) == [Trend(2), Trend(1)]


def test_average_merge_error_1() -> None:
    """Append a non-trend object."""
    trendlist = [Trend(4)]
    with pytest.raises(TypeError) as excerr:
        _average_merge(trendlist, 0)  # type: ignore[arg-type]
    assert str(excerr.value) == "merging element must be Trend"


def test_average_merge_error_2() -> None:
    """Merge trends with equal averages."""
    list_of_trends = [Trend(2)]
    with pytest.raises(ValueError) as excerr:
        _average_merge(list_of_trends, Trend(2))
    assert str(excerr.value) == "trend averages must differ!"


def test_average_merge_error_3() -> None:
    """Merge into a non-Trend array."""
    trendlist = [2, Trend(0)]
    with pytest.raises(TypeError) as excerr:
        _average_merge(trendlist, Trend(2))  # type: ignore[arg-type]
    assert str(excerr.value) == "non-Trend in list"


def test_init(uptrends_list: List["Trend"], downtrends_list: List["Trend"]) -> None:
    """Create Trendlist objects."""
    trendlist = Trendlist()
    assert not trendlist
    assert isinstance(trendlist, Trendlist)
    assert Trendlist(uptrends_list[0:2]) == uptrends_list[0:2]
    assert (
        Trendlist(downtrends_list[0:2], are_one_trend=falling_trend)
        == downtrends_list[0:2]
    )


def test_str_short(uptrends_list) -> None:
    """Stringify short Trendlist object."""
    tr6 = Trendlist(uptrends_list[:6])
    exp6 = "[" + ", ".join([str(trend) for trend in tr6]) + "]"
    assert str(tr6) == exp6


def test_str_long(uptrends_list) -> None:
    """Stringify long Trendlist object."""
    tr7 = Trendlist(uptrends_list[:7])
    exp7 = (
        "["
        + ", ".join([str(trend) for trend in uptrends_list[:3]])
        + ", ..., "
        + ", ".join([str(trend) for trend in uptrends_list[4:7]])
        + "]"
    )
    assert str(tr7) == exp7


def test_empty() -> None:
    """An empty trend gathers no moss."""
    trendlist = Trendlist()
    assert not trendlist
    assert not trendlist.averages()
    assert not trendlist.lengths()


def test_lengths_and_averages() -> None:
    """lengths() and averages() return expected values."""
    tr_e = Trend(average=e, length=9)
    tr_pi = Trend(average=pi, length=6)
    trendlist = Trendlist([tr_pi, tr_e])
    assert trendlist.lengths() == [6, 9]
    assert trendlist.averages() == [pi, e]


def test_append_empty() -> None:
    """Append to empty Trendlist."""
    trendlist = Trendlist()
    trend = Trend(pi)
    trendlist.append(trend)
    assert trendlist == [trend]


def test_append_error_1() -> None:
    """Append a non-trend object."""
    trendlist = Trendlist([Trend(4)])
    with pytest.raises(TypeError) as excerr:
        trendlist.append(0)  # type: ignore[arg-type]
    assert str(excerr.value) == "merging element must be Trend"


def test_append_error_2() -> None:
    """Merge trends with equal averages."""
    trendlist = Trendlist([Trend(2)])
    with pytest.raises(ValueError) as excerr:
        trendlist.append(Trend(2))
    assert str(excerr.value) == "trend averages must differ!"


def test_append_no_merge(
    uptrends_list: List["Trend"], downtrends_list: List["Trend"]
) -> None:
    """Create Trendlist objects."""
    trendlist = Trendlist(uptrends_list[0:2])
    trendlist.append(uptrends_list[2])
    assert trendlist == uptrends_list[0:3]
    trendlist = Trendlist(downtrends_list[0:2], are_one_trend=falling_trend)
    trendlist.append(downtrends_list[2], are_one_trend=falling_trend)
    assert trendlist == downtrends_list[0:3]


def test_trend_append_merge(downtrends_list: List, uptrends_list: List) -> None:
    """Append simply merge-able objects."""
    trendlist = Trendlist()
    for trend in downtrends_list[:5]:
        trendlist.append(trend)
    assert trendlist == Trendlist([Trend(average=2, length=5)])
    trendlist = Trendlist()
    for trend in uptrends_list[:5]:
        trendlist.append(trend, are_one_trend=falling_trend)
    assert trendlist == Trendlist([Trend(average=97, length=5)])


def test_trend_append_multi_merge(downtrends_list: List) -> None:
    """Do a more complex merge."""
    indices = [4, 3, 0, 1, 2]
    expected = [
        Trend(average=4, length=1),
        Trend(average=3, length=1),
        Trend(average=1, length=3),
    ]
    trendlist = Trendlist()
    for average in indices:
        trendlist.append(downtrends_list[average])
    assert trendlist == expected


def test_rotate_noop() -> None:
    """Rotate, empty, singleton trendlist."""
    trendlist = Trendlist()
    assert trendlist.rotate() == trendlist  # no elements
    trendlist.append(Trend(pi))
    assert trendlist.rotate() == trendlist  # one element


def test_rotate_merge(downtrends_list: List) -> None:
    """Simple rotation to get a single trend."""
    trendlist = Trendlist()
    shortlist = downtrends_list[:5]  # 0..4
    largest = shortlist.pop()
    trendlist.append(largest)
    for trend in shortlist:
        trendlist.append(trend)
    assert trendlist.rotate() == Trendlist([Trend(average=2, length=5)])


def test_rotate_one_merge(downtrends_list: List) -> None:
    """Rotation does not produce a single trend."""
    first_five = downtrends_list[:5]
    first_five.reverse()
    trendlist = Trendlist(first_five)
    result = Trendlist(
        [
            Trend(average=3, length=1),
            Trend(average=2, length=1),
            Trend(average=1.6666666666666667, length=3),
        ]
    )
    assert trendlist.rotate() == result


def test_rotate_to_single_trend_trivial() -> None:
    """Rotations of a trivial Trendlist."""
    trendlist = Trendlist()
    assert trendlist.rotate_to_single_trend() == (0, 0)
    trendlist = Trendlist([Trend(0)])
    assert trendlist.rotate_to_single_trend() == (0, 0)


def test_rotate_to_a_single_trend(uptrends_list):
    """Rotate and merge."""
    trendlist = Trendlist(uptrends_list[:4])
    assert trendlist.rotate_to_single_trend() == (2, 2)
