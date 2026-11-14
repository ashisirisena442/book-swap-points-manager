"""Tests for the Member class."""
import pytest
from member import Member


def test_new_member_starts_with_zero_points():
    member = Member("Akarsha", "M001")
    assert member.points == 0


def test_earning_points_adds_to_balance():
    member = Member("Akarsha", "M001")
    member.earn(30)
    member.earn(20)
    assert member.points == 50


def test_spending_points_reduces_balance():
    member = Member("Akarsha", "M001")
    member.earn(30)
    member.spend(20)
    assert member.points == 10


def test_spending_more_than_the_balance_is_rejected():
    member = Member("Akarsha", "M001")
    member.earn(10)
    with pytest.raises(ValueError):
        member.spend(30)


def test_spending_exact_balance_is_allowed():
    member = Member("Akarsha", "M001")
    member.earn(20)
    member.spend(20)
    assert member.points == 0


def test_earning_zero_or_negative_points_is_rejected():
    member = Member("Akarsha", "M001")
    with pytest.raises(ValueError):
        member.earn(0)


def test_empty_name_is_rejected():
    with pytest.raises(ValueError):
        Member(" ", "M001")