"""Benchmark: HashMap vs. AVLTree on Exact Lookup, Range Filtering & Percentiles.

Empirically proves:
1. HashMaps win on exact O(1) point lookups.
2. AVLTrees win dramatically on O(log N + K) range queries and O(log N) percentiles.
"""

from __future__ import annotations

import random
import time

from algocore.maps.hash_map import HashMap
from algocore.trees.avl_tree import AVLTree


def run_benchmarks() -> None:
    n = 50_000
    print("=" * 75)
    print(f"AlgoCore: Performance Benchmark — HashMap vs. AVLTree (N = {n:,d} Employees)")
    print("=" * 75)

    # Generate synthetic compensation dataset: (salary, employee_id)
    salaries = [random.randint(80_000, 350_000) for _ in range(n)]

    hmap: HashMap[int, str] = HashMap()
    tree: AVLTree[int, str] = AVLTree()

    for idx, sal in enumerate(salaries):
        hmap[sal] = f"emp_{idx}"
        tree.insert(sal, f"emp_{idx}")

    # 1. Exact Point Lookups (1,000 random queries)
    query_keys = random.sample(salaries, 1_000)

    t0 = time.perf_counter()
    for k in query_keys:
        _ = hmap.get(k)
    hmap_point_time = time.perf_counter() - t0

    t1 = time.perf_counter()
    for k in query_keys:
        _ = tree.search(k)
    tree_point_time = time.perf_counter() - t1

    header_1 = f"{'1. Exact Point Lookups (1,000 queries)':<45} | HashMap: {hmap_point_time:.6f}s | AVLTree: {tree_point_time:.6f}s"
    print(header_1)

    # 2. Range Query: Find all salaries between $180,000 and $220,000
    low_band, high_band = 180_000, 220_000

    # Scan-based approach (Simulating HashMap / Unsorted full scan)
    t2 = time.perf_counter()
    _ = [v for k, v in hmap.items() if low_band <= k <= high_band]
    scan_time = time.perf_counter() - t2

    # AVL Tree Range Query
    t3 = time.perf_counter()
    _ = tree.range_query(low_band, high_band)
    tree_range_time = time.perf_counter() - t3

    speedup_range = scan_time / tree_range_time if tree_range_time > 0 else 0
    header_2 = f"{'2. Range Query ($180k - $220k)':<45} | Scan:    {scan_time:.6f}s | AVLTree: {tree_range_time:.6f}s ({speedup_range:.1f}x faster)"
    print(header_2)

    # 3. Median / Percentile Calculation (50th percentile)
    t4 = time.perf_counter()
    # Traditional sort: O(N log N)
    sorted_salaries = sorted(salaries)
    _ = sorted_salaries[len(sorted_salaries) // 2]
    sort_time = time.perf_counter() - t4

    # AVL Tree Order Statistic: O(log N)
    t5 = time.perf_counter()
    _ = tree.find_kth_smallest(len(tree) // 2)
    tree_stat_time = time.perf_counter() - t5

    speedup_stat = sort_time / tree_stat_time if tree_stat_time > 0 else 0
    header_3 = f"{'3. Median Calculation (50th percentile)':<45} | Sort:    {sort_time:.6f}s | AVLTree: {tree_stat_time:.6f}s ({speedup_stat:.1f}x faster)"
    print(header_3)
    print("=" * 75)


if __name__ == "__main__":
    run_benchmarks()
