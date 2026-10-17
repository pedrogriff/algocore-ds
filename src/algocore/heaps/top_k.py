"""Streaming top-K selection.

Finds top-K highest or bottom-K lowest elements from high-volume streams
in O(N log K) time and O(K) memory using Min-Heap and Max-Heap invariants.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any, Generic, TypeVar

from algocore.heaps.min_heap import MinHeap

T = TypeVar("T")


class TopKSelector(Generic[T]):
    """Streaming Top-K Selector for large-scale data streams."""

    @staticmethod
    def find_top_k(
        stream: Iterable[T],
        k: int,
        key: Callable[[T], Any] | None = None,
    ) -> list[T]:
        """Extracts the top K largest elements from an iterable in O(N log K) time.

        Uses a Min-Heap of size K as a gatekeeper.

        Args:
            stream: Data stream / collection to inspect.
            k: Number of top elements to retrieve (k > 0).
            key: Optional comparator key extraction function.

        Returns:
            List of top K elements in descending order (highest first).
        """
        if k <= 0:
            return []

        key_func: Callable[[T], Any] = key if key is not None else lambda x: x
        heap: MinHeap[T] = MinHeap(key=key_func)

        for item in stream:
            if len(heap) < k:
                heap.push(item)
            else:
                # If incoming item is greater than the smallest of the top-k (the root), replace it
                if key_func(item) > key_func(heap.peek()):
                    heap.replace(item)

        # Pop all elements and sort descending
        results: list[T] = []
        while not heap.is_empty():
            results.append(heap.pop())

        # Heap pop gives ascending order (smallest of top-k first), reverse for descending
        results.reverse()
        return results
