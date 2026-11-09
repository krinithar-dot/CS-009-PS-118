
from datetime import date

from src.limitation import calculate_limitation


def test_civil_suit_within_limitation():
    result = calculate_limitation(
        "CIVIL_SUIT",
        date(2023, 1, 1),
        date(2025, 1, 1)
    )

    assert result.status == "ACCEPTED"


def test_filing_beyond_limitation():
    result = calculate_limitation(
        "CIVIL_SUIT",
        date(2023, 1, 1),
        date(2027, 1, 1)
    )

    assert result.status == "REJECTED"


def test_condonation_application():
    result = calculate_limitation(
        "CIVIL_SUIT",
        date(2023, 1, 1),
        date(2027, 1, 1),
        condonation_applied=True
    )

    assert result.status == "DELAY_CONDONATION_PENDING"


def test_wrong_forum_exclusion():
    result = calculate_limitation(
        "CIVIL_SUIT",
        date(2023, 1, 1),
        date(2026, 1, 20),
        wrong_forum_days=30
    )

    assert result.status == "ACCEPTED"


def test_holiday_extension():
    result = calculate_limitation(
        "CIVIL_SUIT",
        date(2023, 1, 1),
        date(2026, 1, 2),
        holidays={date(2026, 1, 1)}
    )

    assert result.final_deadline == date(2026, 1, 2)
    assert result.status == "ACCEPTED"


def test_appeal_limitation():
    result = calculate_limitation(
        "APPEAL",
        date(2026, 1, 1),
        date(2026, 1, 20)
    )

    assert result.status == "ACCEPTED"

import pytest


def test_filing_on_exact_deadline():
    result = calculate_limitation(
        "CIVIL_SUIT",
        date(2023, 1, 1),
        date(2026, 1, 1)
    )

    assert result.status == "ACCEPTED"


def test_consecutive_holidays():
    result = calculate_limitation(
        "CIVIL_SUIT",
        date(2023, 1, 1),
        date(2026, 1, 3),
        holidays={
            date(2026, 1, 1),
            date(2026, 1, 2)
        }
    )

    assert result.final_deadline == date(2026, 1, 3)
    assert result.status == "ACCEPTED"


def test_money_recovery_uses_due_date():
    result = calculate_limitation(
        "MONEY_RECOVERY",
        date(2023, 6, 15),
        date(2025, 6, 15)
    )

    assert result.original_deadline == date(2026, 6, 15)
    assert result.status == "ACCEPTED"


def test_revision_limitation():
    result = calculate_limitation(
        "REVISION",
        date(2026, 1, 1),
        date(2026, 3, 1)
    )

    assert result.status == "ACCEPTED"
    assert result.original_deadline == date(2026, 4, 1)


def test_negative_wrong_forum_days():
    with pytest.raises(ValueError):
        calculate_limitation(
            "CIVIL_SUIT",
            date(2023, 1, 1),
            date(2025, 1, 1),
            wrong_forum_days=-10
        )
