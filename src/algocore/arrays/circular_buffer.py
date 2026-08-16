"""Google-Caliber Generic Circular Ring Buffer (ArrayDeque) Implementation.

Demonstrates O(1) double-ended queue operations (push/pop front & back) using
pointer wrap-around modulo arithmetic over contiguous memory.
"""

from __future__ import annotations

import ctypes
from typing import Any, Generic, Iterator, TypeVar, cast

T = TypeVar("T")


class CircularBuffer(Generic[T]):
    """A high-performance circular ring buffer / double-ended queue.

    Provides O(1) amortized push_back, push_front, pop_back, and pop_front without
    element shifting by leveraging head and tail pointers with modulo arithmetic.
    """

    DEFAULT_CAPACITY: int = 8
    GROWTH_FACTOR: int = 2

    def __init__(self, initial_capacity: int = DEFAULT_CAPACITY) -> None:
        """Initializes circular buffer with a given initial capacity."""
        if initial_capacity <= 0:
            raise ValueError(f"Capacity must be positive, got {initial_capacity}")

        self._capacity: int = initial_capacity
        self._size: int = 0
        self._head: int = 0  # Points to the first valid element
        self._tail: int = 0  # Points to the next empty insertion slot at back
        self._raw_buffer: Any = self._make_raw_buffer(self._capacity)

    @property
    def capacity(self) -> int:
        """Returns current allocated buffer capacity."""
        return self._capacity

    def __len__(self) -> int:
        """Returns the number of elements in the buffer."""
        return self._size

    def is_empty(self) -> bool:
        """Returns True if the buffer contains no elements."""
        return self._size == 0

    def _make_raw_buffer(self, capacity: int) -> Any:
        """Allocates a contiguous raw block of memory."""
        return (capacity * ctypes.py_object)()

    def push_back(self, value: T) -> None:
        """Pushes an element to the back of the queue in Amortized O(1) time."""
        if self._size == self._capacity:
            self._resize(self._capacity * self.GROWTH_FACTOR)

        self._raw_buffer[self._tail] = value
        self._tail = (self._tail + 1) % self._capacity
        self._size += 1

    def push_front(self, value: T) -> None:
        """Pushes an element to the front of the queue in Amortized O(1) time."""
        if self._size == self._capacity:
            self._resize(self._capacity * self.GROWTH_FACTOR)

        # Move head one step counter-clockwise with modulo wrap-around
        self._head = (self._head - 1 + self._capacity) % self._capacity
        self._raw_buffer[self._head] = value
        self._size += 1

    def pop_front(self) -> T:
        """Removes and returns the front element in O(1) time without shifting.

        Raises:
            IndexError: If buffer is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot pop from an empty CircularBuffer")

        value = cast(T, self._raw_buffer[self._head])
        self._raw_buffer[self._head] = None  # Assist Garbage Collection
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return value

    def pop_back(self) -> T:
        """Removes and returns the back element in O(1) time.

        Raises:
            IndexError: If buffer is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot pop from an empty CircularBuffer")

        # Move tail one step counter-clockwise
        self._tail = (self._tail - 1 + self._capacity) % self._capacity
        value = cast(T, self._raw_buffer[self._tail])
        self._raw_buffer[self._tail] = None  # Assist GC
        self._size -= 1
        return value

    def peek_front(self) -> T:
        """Returns front element without removing it in O(1) time."""
        if self.is_empty():
            raise IndexError("Cannot peek into an empty CircularBuffer")
        return cast(T, self._raw_buffer[self._head])

    def peek_back(self) -> T:
        """Returns back element without removing it in O(1) time."""
        if self.is_empty():
            raise IndexError("Cannot peek into an empty CircularBuffer")
        last_idx = (self._tail - 1 + self._capacity) % self._capacity
        return cast(T, self._raw_buffer[last_idx])

    def __getitem__(self, index: int) -> T:
        """Accesses element by logical 0-indexed position relative to head."""
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")

        physical_idx = (self._head + index) % self._capacity
        return cast(T, self._raw_buffer[physical_idx])

    def _resize(self, new_capacity: int) -> None:
        """Unrolls circular buffer into a linear layout with new capacity."""
        new_buffer = self._make_raw_buffer(new_capacity)
        for i in range(self._size):
            physical_idx = (self._head + i) % self._capacity
            new_buffer[i] = self._raw_buffer[physical_idx]

        self._raw_buffer = new_buffer
        self._head = 0
        self._tail = self._size
        self._capacity = new_capacity

    def __iter__(self) -> Iterator[T]:
        """Iterates from head to tail in logical FIFO order."""
        for i in range(self._size):
            yield self[i]

    def __repr__(self) -> str:
        elements = [repr(self[i]) for i in range(self._size)]
        joined = ", ".join(elements)
        return f"CircularBuffer([{joined}], size={self._size}, capacity={self._capacity})"
