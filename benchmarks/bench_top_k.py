"""Benchmark: Top-K Streaming Min-Heap vs. Full Array Sorting at Scale.

Results to look for:
1. Min-Heap of size K processes 1,000,000 streaming elements in O(N log K) time.
2. Full Sort takes O(N log N) time and wastes O(N) memory.
"""

from __future__ import annotations

import random
import time

from algocore.heaps.top_k import TopKSelector


def run_benchmark() -> None:
    n = 1_000_000
    k = 50
    print("=" * 75)
    print(f"AlgoCore: Top-K Benchmark — Min-Heap vs. Full Sort (N = {n:,d}, K = {k})")
    print("=" * 75)

    # Generate streaming salaries dataset
    salaries = [random.randint(60_000, 500_000) for _ in range(n)]

    # 1. Full Sort Approach: O(N log N) time, O(N) memory
    t0 = time.perf_counter()
    full_sorted = sorted(salaries, reverse=True)[:k]
    sort_time = time.perf_counter() - t0

    # 2. Min-Heap Streaming Approach: O(N log K) time, O(K) memory
    t1 = time.perf_counter()
    heap_top_k = TopKSelector.find_top_k(salaries, k=k)
    heap_time = time.perf_counter() - t1

    assert full_sorted == heap_top_k, "Top-K results mismatch!"

    speedup = sort_time / heap_time if heap_time > 0 else 0
    print(f"{'Method':<30} | {'Execution Time (s)':<20} | {'Memory Complexity':<18}")
    print("-" * 75)
    print(f"{'1. Full Sort O(N log N)':<30} | {sort_time:<20.6f} | {'O(N) (~' + str(n * 8 // 1024 // 1024) + ' MB)':<18}")
    print(f"{'2. Min-Heap Top-K O(N log K)':<30} | {heap_time:<20.6f} | {'O(K) (~' + str(k * 8) + ' bytes)':<18}")
    print("-" * 75)
    print(f"Speedup: Min-Heap is {speedup:.2f}x faster while using virtually ZERO extra RAM!")
    print("=" * 75)


if __name__ == "__main__":
    run_benchmark()
