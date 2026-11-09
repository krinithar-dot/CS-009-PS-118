
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from src.limitation import calculate_limitation
from src.fee_calculator import (
    calculate_court_fee,
    check_fee_payment
)


@dataclass
class CaseFiling:
    case_id: str
    case_type: str
    relevant_date: date
    filing_date: date
    claim_value: Decimal
    paid_fee: Decimal
    party_ids: list[str]
    urgent: bool = False
    wrong_forum_days: int = 0
    condonation_applied: bool = False


@dataclass
class AdmissionDecision:
    case_id: str
    limitation_status: str
    fee_status: str
    admission_status: str
    required_fee: Decimal
    paid_fee: Decimal
    shortfall: Decimal
    cure_deadline: date | None
    message: str


def admit_case(
    filing: CaseFiling,
    holidays: set[date] | None = None,
    current_date: date | None = None
) -> AdmissionDecision:

    # STEP 1: Check limitation
    limitation = calculate_limitation(
        case_type=filing.case_type,
        relevant_date=filing.relevant_date,
        filing_date=filing.filing_date,
        wrong_forum_days=filing.wrong_forum_days,
        condonation_applied=filing.condonation_applied,
        holidays=holidays
    )

    # A filing rejected for limitation cannot proceed
    if limitation.status == "REJECTED":
        return AdmissionDecision(
            filing.case_id,
            limitation.status,
            "NOT_CHECKED",
            "REJECTED",
            Decimal("0.00"),
            filing.paid_fee,
            Decimal("0.00"),
            None,
            limitation.message
        )

    # STEP 2: Calculate required court fee
    required_fee = calculate_court_fee(
        claim_value=filing.claim_value,
        case_type=filing.case_type
    )

    # STEP 3: Check fee payment
    fee_result = check_fee_payment(
        required_fee=required_fee,
        paid_fee=filing.paid_fee,
        filing_date=filing.filing_date,
        current_date=current_date
    )

    # STEP 4: Determine final admission status
    if fee_result.status == "RETURNED":
        admission_status = "RETURNED"
        message = "Court fee deficiency was not corrected within 7 days."

    elif fee_result.status == "DEFECTIVE":
        admission_status = "DEFECTIVE"
        message = "Insufficient court fee. Correct within 7 days."

    elif limitation.status == "DELAY_CONDONATION_PENDING":
        admission_status = "DELAY_CONDONATION_PENDING"
        message = "Fee is sufficient. Condonation decision is pending."

    else:
        admission_status = "ACCEPTED"
        message = "Filing passed limitation and court fee checks."

    return AdmissionDecision(
        case_id=filing.case_id,
        limitation_status=limitation.status,
        fee_status=fee_result.status,
        admission_status=admission_status,
        required_fee=required_fee,
        paid_fee=filing.paid_fee,
        shortfall=fee_result.shortfall,
        cure_deadline=fee_result.cure_deadline,
        message=message
    )
