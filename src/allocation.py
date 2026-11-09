
from decimal import Decimal


class BenchAllocator:

    def __init__(self, bench_manager):
        self.bench_manager = bench_manager
        self.round_robin_index = {}

    def allocate_case(
        self,
        case_id,
        subject,
        claim_value,
        party_ids
    ):

        subject = subject.upper()
        claim_value = Decimal(str(claim_value))

        if not claim_value.is_finite() or claim_value <= 0:
            raise ValueError("Invalid claim value")

        # Commercial claims above Rs 3 lakh
        # must go to a commercial bench.
        if subject == "COMMERCIAL" and claim_value > Decimal("300000"):
            required_subject = "COMMERCIAL"
        else:
            required_subject = subject

        # Find eligible benches
        eligible_benches = []

        for bench in self.bench_manager.get_all_benches():

            if required_subject not in [
                item.upper() for item in bench.subjects
            ]:
                continue

            # Skip benches with party conflicts
            if bench.has_conflict(party_ids):
                continue

            eligible_benches.append(bench)

        if not eligible_benches:
            return None

        # Sort to ensure deterministic round-robin order
        eligible_benches.sort(key=lambda b: b.bench_id)

        # Round-robin allocation
        index = self.round_robin_index.get(required_subject, 0)

        selected_bench = eligible_benches[
            index % len(eligible_benches)
        ]

        self.round_robin_index[required_subject] = (
            index + 1
        )

        return selected_bench.bench_id
