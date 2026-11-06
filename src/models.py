
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Bench:
    bench_id: str
    subjects: list[str]
    sitting_days: list[int]
    capacity: int = 40
    leave_dates: set[date] = field(default_factory=set)
    conflict_parties: set[str] = field(default_factory=set)

    def is_available(self, hearing_date: date) -> bool:
        """Check whether the bench is sitting on the given date."""
        return (
            hearing_date.weekday() in self.sitting_days
            and hearing_date not in self.leave_dates
        )

    def has_conflict(self, party_ids: list[str]) -> bool:
        """Check whether any party has a conflict with this bench."""
        return bool(set(party_ids) & self.conflict_parties)
