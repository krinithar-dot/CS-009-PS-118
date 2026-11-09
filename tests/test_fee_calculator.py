
from datetime import date
from decimal import Decimal
import pytest

from src.fee_calculator import (
    calculate_court_fee,
    check_fee_payment
)


def test_fee_exactly_one_lakh():
    assert calculate_court_fee(100000) == Decimal("5000.00")


def test_fee_exactly_ten_lakh():
    assert calculate_court_fee(1000000) == Decimal("41000.00")


def test_fee_five_lakh():
    assert calculate_court_fee(500000) == Decimal("21000.00")


def test_fee_above_ten_lakh():
    assert calculate_court_fee(1500000) == Decimal("51000.00")


def test_maximum_fee_cap():
    assert calculate_court_fee(20000000) == Decimal("300000.00")


def test_appeal_fee():
    assert calculate_court_fee(
        500000,
        case_type="APPEAL",
        original_fee=21000
    ) == Decimal("10500.00")


def test_insufficient_fee():
    result = check_fee_payment(
        5000,
        3000,
        date(2026, 11, 9)
    )

    assert result.status == "DEFECTIVE"
    assert result.shortfall == Decimal("2000.00")


def test_fee_cured_within_seven_days():
    result = check_fee_payment(
        5000,
        3000,
        date(2026, 11, 9),
        date(2026, 11, 16)
    )

    assert result.status == "DEFECTIVE"


def test_fee_not_cured_after_seven_days():
    result = check_fee_payment(
        5000,
        3000,
        date(2026, 11, 9),
        date(2026, 11, 17)
    )

    assert result.status == "RETURNED"


def test_invalid_claim_value():
    with pytest.raises(ValueError):
        calculate_court_fee(-1000)
