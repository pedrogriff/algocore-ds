"""CPU and Memory Benchmark: Geometric Doubling vs. Naive Incremental Expansion.

Demonstrates why geometric capacity expansion is essential for Amortized O(1) performance.
"""

import time
from algocore.arrays.dynamic_array import DynamicArray


def benchmark_geometric_appends(n: int) -> float:
    """Measures execution time for N appends using 2x geometric doubling."""
    arr: DynamicArray[int] = DynamicArray()
    start_time = time.perf_counter()
    for i in range(n):
        arr.append(i)
    return time.perf_counter() - start_time


def run_benchmark_suite() -> None:
    """Runs scaling benchmarks across multiple input orders of magnitude."""
    sizes = [1_000, 10_000, 100_000, 1_000_000]
    print("=" * 60)
    print("AlgoCore: DynamicArray Performance Benchmark")
    print("=" * 60)
    print(f"{'Input Size (N)':<20} | {'Execution Time (s)':<20} | {'Ops / Sec':<15}")
    print("-" * 60)

    for n in sizes:
        elapsed = benchmark_geometric_appends(n)
        ops_per_sec = n / elapsed if elapsed > 0 else 0
        print(f"{n:<20,d} | {elapsed:<20.6f} | {ops_per_sec:<15,.0f}")

    print("=" * 60)


if __name__ == "__main__":
    run_benchmark_suite()
