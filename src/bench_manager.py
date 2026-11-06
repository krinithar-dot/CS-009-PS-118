
from models import Bench


class BenchManager:

    def __init__(self):
        self.benches = {}

    def register_bench(self, bench: Bench):
        if bench.bench_id in self.benches:
            raise ValueError("Bench already exists")

        if not 1 <= bench.capacity <= 40:
            raise ValueError("Bench capacity must be between 1 and 40")

        self.benches[bench.bench_id] = bench

    def get_bench(self, bench_id: str):
        return self.benches.get(bench_id)

    def get_all_benches(self):
        return list(self.benches.values())
