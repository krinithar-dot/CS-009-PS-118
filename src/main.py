
from datetime import date
from src.models import Bench
from src.bench_manager import BenchManager


manager = BenchManager()

bench = Bench(
    bench_id="B01",
    subjects=["CIVIL"],
    sitting_days=[0, 2, 4],
    capacity=40,
    conflict_parties={"P101", "P105"}
)

manager.register_bench(bench)

print("Registered Benches:")

for b in manager.get_all_benches():
    print("Bench ID:", b.bench_id)
    print("Subjects:", b.subjects)
    print("Capacity:", b.capacity)

print("\nAvailability:", bench.is_available(date(2026, 11, 9)))
print("Conflict:", bench.has_conflict(["P101"]))
