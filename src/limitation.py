
from dataclasses import dataclass
from datetime import date, timedelta


# Limitation periods for different case types
LIMITATION_PERIODS = {
    "CIVIL_SUIT": ("YEARS", 3),
    "MONEY_RECOVERY": ("YEARS", 3),
    "APPEAL": ("DAYS", 30),
    "REVISION": ("DAYS", 90)
}


@dataclass
class LimitationResult:
    original_deadline: date
    final_deadline: date
    status: str
    message: str


def add_years(start_date: date, years: int) -> date:
    """Add years while safely handling leap-year dates."""
    try:
        return start_date.replace(year=start_date.year + years)
    except ValueError:
        # February 29 becomes February 28 in a non-leap year
        return start_date.replace(
            year=start_date.year + years,
            day=28
        )


def calculate_limitation(
    case_type: str,
    relevant_date: date,
    filing_date: date,
    wrong_forum_days: int = 0,
    condonation_applied: bool = False,
    holidays: set[date] | None = None
) -> LimitationResult:

    case_type = case_type.upper()

    if case_type not in LIMITATION_PERIODS:
        raise ValueError("Invalid case type")

    if wrong_forum_days < 0:
        raise ValueError("Wrong forum days cannot be negative")

    if filing_date < relevant_date:
        raise ValueError("Filing date cannot precede the relevant date")

    holidays = holidays or set()

    period_type, period_value = LIMITATION_PERIODS[case_type]

    # Step 1: Calculate original deadline
    if period_type == "YEARS":
        deadline = add_years(relevant_date, period_value)
    else:
        deadline = relevant_date + timedelta(days=period_value)

    original_deadline = deadline

    # Step 2: Exclude time spent in the wrong forum
    deadline += timedelta(days=wrong_forum_days)

    # Step 3: Extend if the final day is a court holiday
    while deadline in holidays:
        deadline += timedelta(days=1)

    # Step 4: Determine admission status
    if filing_date <= deadline:
        status = "ACCEPTED"
        message = "Filing is within the limitation period."

    elif condonation_applied:
        status = "DELAY_CONDONATION_PENDING"
        message = "Late filing with condonation application."

    else:
        status = "REJECTED"
        message = "Filing is beyond the limitation period."

    return LimitationResult(
        original_deadline=original_deadline,
        final_deadline=deadline,
        status=status,
        message=message
    )
