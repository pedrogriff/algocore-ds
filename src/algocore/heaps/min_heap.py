"""Binary min-heap and priority queue.

Demonstrates:
1. Array-backed complete binary tree arithmetic (parent=(i-1)//2, left=2i+1, right=2i+2).
2. O(log N) push and pop via sift_up and sift_down.
3. O(N) Floyd's linear-time heapify algorithm.
4. Single-pass O(log N) root replacement for streaming top-k pipelines.
5. Generic custom key extraction (e.g. heapifying Employee objects by salary).
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class MinHeap(Generic[T]):
    """A generic, cache-friendly binary min-heap / priority queue."""

    def __init__(
        self,
        items: list[T] | None = None,
        key: Callable[[T], Any] | None = None,
    ) -> None:
        """Initializes MinHeap, optionally building it from an existing list in O(N) time.

        Args:
            items: Optional initial list of items to heapify.
            key: Optional function to extract comparison key from elements.
        """
        self._key_func: Callable[[T], Any] = key if key is not None else lambda x: x
        self._data: list[T] = []

        if items:
            self._data = list(items)
            self._heapify()

    def __len__(self) -> int:
        """Returns the number of elements in the heap."""
        return len(self._data)

    def is_empty(self) -> bool:
        """Returns True if the heap contains no elements."""
        return len(self._data) == 0

    def _val(self, item: T) -> Any:
        """Extracts comparable value using key function."""
        return self._key_func(item)

    def peek(self) -> T:
        """Returns the smallest element (root) in O(1) time without removing it.

        Raises:
            IndexError: If the heap is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot peek into an empty MinHeap")
        return self._data[0]

    def push(self, item: T) -> None:
        """Inserts an element into the heap in O(log N) time."""
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> T:
        """Removes and returns the smallest element (root) in O(log N) time.

        Raises:
            IndexError: If the heap is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot pop from an empty MinHeap")

        root = self._data[0]
        last_item = self._data.pop()

        if self._data:
            self._data[0] = last_item
            self._sift_down(0)

        return root

    def replace(self, item: T) -> T:
        """Pops the root and pushes a new item in a single O(log N) sift-down pass.

        More efficient than a separate pop() followed by push().

        Raises:
            IndexError: If the heap is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot replace root in an empty MinHeap")

        root = self._data[0]
        self._data[0] = item
        self._sift_down(0)
        return root

    def pushpop(self, item: T) -> T:
        """Fast push then pop.

        If item <= root, returns item immediately without altering the heap.
        Otherwise replaces root with item and returns old root.
        """
        if self._data and self._val(item) > self._val(self._data[0]):
            root = self._data[0]
            self._data[0] = item
            self._sift_down(0)
            return root
        return item

    def _sift_up(self, idx: int) -> None:
        """Sifts element at idx upward until heap invariant is satisfied."""
        current_item = self._data[idx]
        current_val = self._val(current_item)

        while idx > 0:
            parent_idx = (idx - 1) // 2
            parent_item = self._data[parent_idx]

            if current_val < self._val(parent_item):
                self._data[idx] = parent_item
                idx = parent_idx
            else:
                break

        self._data[idx] = current_item

    def _sift_down(self, idx: int) -> None:
        """Sifts element at idx downward until heap invariant is satisfied."""
        n = len(self._data)
        current_item = self._data[idx]
        current_val = self._val(current_item)

        while True:
            left_idx = 2 * idx + 1
            right_idx = 2 * idx + 2
            smallest_idx = idx
            smallest_val = current_val

            if left_idx < n and self._val(self._data[left_idx]) < smallest_val:
                smallest_idx = left_idx
                smallest_val = self._val(self._data[left_idx])

            if right_idx < n and self._val(self._data[right_idx]) < smallest_val:
                smallest_idx = right_idx

            if smallest_idx != idx:
                self._data[idx] = self._data[smallest_idx]
                idx = smallest_idx
            else:
                break

        self._data[idx] = current_item

    def _heapify(self) -> None:
        """Transforms an arbitrary array into a valid Min-Heap in O(N) linear time.

        Uses Floyd's algorithm starting from the lowest non-leaf node down to root.
        """
        start_idx = (len(self._data) // 2) - 1
        for i in range(start_idx, -1, -1):
            self._sift_down(i)

    def __iter__(self) -> Iterator[T]:
        """Iterates over elements in internal array layout."""
        return iter(self._data)
