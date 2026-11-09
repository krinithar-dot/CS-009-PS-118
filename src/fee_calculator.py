
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta
from dataclasses import dataclass


MAX_COURT_FEE = Decimal("300000.00")


def calculate_court_fee(
    claim_value,
    case_type="CIVIL_SUIT",
    original_fee=None
):
    claim = Decimal(str(claim_value))

    if not claim.is_finite() or claim <= 0:
        raise ValueError("Claim value must be positive")

    # Appeals pay 50% of the original case fee
    if case_type.upper() == "APPEAL":
        if original_fee is None:
            raise ValueError("Original case fee is required for appeals")

        original = Decimal(str(original_fee))

        if not original.is_finite() or original < 0:
            raise ValueError("Invalid original fee")

        fee = original * Decimal("0.50")

    else:
        # First slab: 5% up to Rs 1 lakh
        first_slab = min(claim, Decimal("100000"))
        fee1 = first_slab * Decimal("0.05")

        # Second slab: 4% from Rs 1 lakh to Rs 10 lakh
        second_slab = min(
            max(claim - Decimal("100000"), Decimal("0")),
            Decimal("900000")
        )
        fee2 = second_slab * Decimal("0.04")

        # Third slab: 2% above Rs 10 lakh
        third_slab = max(claim - Decimal("1000000"), Decimal("0"))
        fee3 = third_slab * Decimal("0.02")

        fee = fee1 + fee2 + fee3

        # Maximum fee is Rs 3 lakh
        fee = min(fee, MAX_COURT_FEE)

    return fee.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


@dataclass
class FeePaymentResult:
    status: str
    required_fee: Decimal
    paid_fee: Decimal
    shortfall: Decimal
    cure_deadline: date | None


def check_fee_payment(
    required_fee,
    paid_fee,
    filing_date,
    current_date=None
):
    required = Decimal(str(required_fee))
    paid = Decimal(str(paid_fee))

    if not required.is_finite() or required < 0:
        raise ValueError("Invalid required fee")

    if not paid.is_finite() or paid < 0:
        raise ValueError("Invalid paid fee")

    if current_date is None:
        current_date = filing_date

    if paid >= required:
        return FeePaymentResult(
            "FEE_SUFFICIENT",
            required,
            paid,
            Decimal("0.00"),
            None
        )

    deadline = filing_date + timedelta(days=7)
    shortfall = required - paid

    if current_date > deadline:
        status = "RETURNED"
    else:
        status = "DEFECTIVE"

    return FeePaymentResult(
        status,
        required,
        paid,
        shortfall,
        deadline
    )
