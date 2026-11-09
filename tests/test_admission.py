
from datetime import date
from decimal import Decimal

from src.admission import CaseFiling, admit_case


def create_filing(**changes):
    data = {
        "case_id": "C001",
        "case_type": "CIVIL_SUIT",
        "relevant_date": date(2023, 1, 1),
        "filing_date": date(2025, 1, 1),
        "claim_value": Decimal("500000"),
        "paid_fee": Decimal("21000"),
        "party_ids": ["P101", "P102"]
    }

    data.update(changes)
    return CaseFiling(**data)


def test_successful_admission():
    result = admit_case(create_filing())

    assert result.admission_status == "ACCEPTED"
    assert result.required_fee == Decimal("21000.00")


def test_rejected_limitation():
    filing = create_filing(
        filing_date=date(2027, 1, 1)
    )

    result = admit_case(filing)

    assert result.admission_status == "REJECTED"
    assert result.fee_status == "NOT_CHECKED"


def test_condonation_pending():
    filing = create_filing(
        filing_date=date(2027, 1, 1),
        condonation_applied=True
    )

    result = admit_case(filing)

    assert result.admission_status == "DELAY_CONDONATION_PENDING"


def test_defective_fee():
    filing = create_filing(
        paid_fee=Decimal("10000")
    )

    result = admit_case(filing)

    assert result.admission_status == "DEFECTIVE"
    assert result.shortfall == Decimal("11000.00")


def test_returned_after_seven_days():
    filing = create_filing(
        paid_fee=Decimal("10000")
    )

    result = admit_case(
        filing,
        current_date=date(2025, 1, 9)
    )

    assert result.admission_status == "RETURNED"


def test_cure_on_seventh_day():
    filing = create_filing(
        paid_fee=Decimal("10000")
    )

    result = admit_case(
        filing,
        current_date=date(2025, 1, 8)
    )

    assert result.admission_status == "DEFECTIVE"
