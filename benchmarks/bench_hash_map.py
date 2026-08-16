"""Benchmark: HashMap O(1) Lookup Latency across Scale.

Verifies constant-time read/write performance in open-addressing hash tables.
"""

import time
from algocore.maps.hash_map import HashMap


def benchmark_hash_map_operations(n: int) -> tuple[float, float]:
    """Measures insertion time and random lookup time for N elements."""
    hmap: HashMap[str, int] = HashMap()

    # Benchmark Insertions
    t0 = time.perf_counter()
    for i in range(n):
        hmap[f"emp_{i:07d}"] = 100_000 + i
    insert_time = time.perf_counter() - t0

    # Benchmark Lookups
    t1 = time.perf_counter()
    for i in range(n):
        _ = hmap[f"emp_{i:07d}"]
    lookup_time = time.perf_counter() - t1

    return insert_time, lookup_time


def run_benchmark() -> None:
    sizes = [1_000, 10_000, 50_000, 100_000]
    print("=" * 70)
    print("AlgoCore: HashMap O(1) Scale Benchmark (Employee Key-Value Lookups)")
    print("=" * 70)
    header = f"{'Entries (N)':<15} | {'Insert Total (s)':<18} | {'Lookup Total (s)':<18} | {'Avg Lookup (μs)':<15}"
    print(header)
    print("-" * 70)

    for n in sizes:
        t_ins, t_get = benchmark_hash_map_operations(n)
        avg_lookup_us = (t_get / n) * 1_000_000
        print(f"{n:<15,d} | {t_ins:<18.4f} | {t_get:<18.4f} | {avg_lookup_us:<15.2f}")

    print("=" * 70)


if __name__ == "__main__":
    run_benchmark()
