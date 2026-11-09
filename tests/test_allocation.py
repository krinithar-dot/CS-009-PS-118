
from src.models import Bench
from src.bench_manager import BenchManager
from src.allocation import BenchAllocator


def create_manager():
    manager = BenchManager()

    manager.register_bench(
        Bench("B01", ["CIVIL"], [0, 2, 4],
             conflict_parties={"P101"})
    )

    manager.register_bench(
        Bench("B05", ["CIVIL"], [0, 2, 4])
    )

    manager.register_bench(
        Bench("B04", ["COMMERCIAL"], [0, 2, 4])
    )

    manager.register_bench(
        Bench("B03", ["FAMILY"], [0, 2, 4])
    )

    return manager


def test_civil_allocation():
    allocator = BenchAllocator(create_manager())

    result = allocator.allocate_case(
        "C001", "CIVIL", 200000, ["P102"]
    )

    assert result == "B01"


def test_conflict_bench_skipped():
    allocator = BenchAllocator(create_manager())

    result = allocator.allocate_case(
        "C001", "CIVIL", 200000, ["P101"]
    )

    assert result == "B05"


def test_round_robin_allocation():
    allocator = BenchAllocator(create_manager())

    first = allocator.allocate_case(
        "C001", "CIVIL", 200000, ["P102"]
    )

    second = allocator.allocate_case(
        "C002", "CIVIL", 200000, ["P103"]
    )

    assert first == "B01"
    assert second == "B05"


def test_commercial_allocation():
    allocator = BenchAllocator(create_manager())

    result = allocator.allocate_case(
        "C003", "COMMERCIAL", 500000, ["P102"]
    )

    assert result == "B04"


def test_family_allocation():
    allocator = BenchAllocator(create_manager())

    result = allocator.allocate_case(
        "C004", "FAMILY", 100000, ["P102"]
    )

    assert result == "B03"


def test_no_eligible_bench():
    allocator = BenchAllocator(create_manager())

    result = allocator.allocate_case(
        "C005", "CRIMINAL", 100000, ["P102"]
    )

    assert result is None
