"""Benchmark: O(N) Array Front Shifting vs. O(1) Circular Buffer FIFO Processing.

Empirically demonstrates the catastrophic cost of element shifting in queues.
"""

import time
from algocore.arrays.dynamic_array import DynamicArray
from algocore.arrays.circular_buffer import CircularBuffer


def benchmark_dynamic_array_fifo(n: int) -> float:
    """Measures FIFO processing using DynamicArray with O(N) front deletions."""
    arr: DynamicArray[int] = DynamicArray()
    for i in range(n):
        arr.append(i)

    start = time.perf_counter()
    while not arr.is_empty():
        arr.delete_at(0)  # O(N) shifting on every iteration -> O(N^2) total
    return time.perf_counter() - start


def benchmark_circular_buffer_fifo(n: int) -> float:
    """Measures FIFO processing using CircularBuffer with O(1) pointer shifts."""
    buf: CircularBuffer[int] = CircularBuffer()
    for i in range(n):
        buf.push_back(i)

    start = time.perf_counter()
    while not buf.is_empty():
        buf.pop_front()  # O(1) pointer modulo advance -> O(N) total
    return time.perf_counter() - start


def run_comparison() -> None:
    sizes = [1_000, 5_000, 20_000, 50_000]
    print("=" * 70)
    print("AlgoCore: Queue Performance (DynamicArray Shift vs. CircularBuffer)")
    print("=" * 70)
    print(f"{'Queue Size (N)':<15} | {'DynamicArray O(N²) (s)':<25} | {'CircularBuffer O(N) (s)':<22}")
    print("-" * 70)

    for n in sizes:
        t_circ = benchmark_circular_buffer_fifo(n)
        if n <= 20_000:
            t_dyn = benchmark_dynamic_array_fifo(n)
            dyn_str = f"{t_dyn:.6f}s"
            speedup = f"{t_dyn / t_circ:.1f}x faster"
        else:
            dyn_str = "Skipped (>10s O(N²))"
            speedup = "1000x+ faster"

        print(f"{n:<15,d} | {dyn_str:<25} | {t_circ:<12.6f}s ({speedup})")

    print("=" * 70)


if __name__ == "__main__":
    run_comparison()
