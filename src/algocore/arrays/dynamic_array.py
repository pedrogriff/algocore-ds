"""Generic dynamic array implementation.

This module provides a custom DynamicArray implementation that operates on top of
raw, fixed-size contiguous memory blocks allocated via `ctypes.py_object`.

Key Computer Science Principles Demonstrated:
1. Contiguous Memory Allocation: Fast O(1) random access via memory address arithmetic.
2. Geometric Resizing: Capacity doubling (2x) to guarantee Amortized O(1) append operations.
3. Strict Bounds Checking: Defends against buffer over-reads and index out of bounds.
4. Generics & Strict Typing: Type safety with PEP 695 / TypeVar generics.
"""

from __future__ import annotations

import ctypes
from collections.abc import Iterator
from typing import Any, Generic, TypeVar, cast

T = TypeVar("T")


class DynamicArray(Generic[T]):
    """A generic, cache-friendly dynamic array with amortized O(1) insertions.

    Attributes:
        _size: The number of active elements currently stored.
        _capacity: The total number of elements the current underlying raw buffer can hold.
        _raw_buffer: The underlying contiguous array of C pointers allocated via ctypes.
    """

    DEFAULT_CAPACITY: int = 4
    GROWTH_FACTOR: int = 2

    def __init__(self, initial_capacity: int = DEFAULT_CAPACITY) -> None:
        """Initializes a DynamicArray with a given initial capacity.

        Args:
            initial_capacity: The initial memory capacity. Must be > 0.

        Raises:
            ValueError: If initial_capacity <= 0.
        """
        if initial_capacity <= 0:
            raise ValueError(f"Initial capacity must be positive, got {initial_capacity}")

        self._size: int = 0
        self._capacity: int = initial_capacity
        self._raw_buffer: Any = self._make_raw_buffer(self._capacity)

    @property
    def capacity(self) -> int:
        """Returns the total capacity of the underlying allocated buffer."""
        return self._capacity

    def __len__(self) -> int:
        """Returns the number of elements stored in the array."""
        return self._size

    def is_empty(self) -> bool:
        """Returns True if the array contains zero elements."""
        return self._size == 0

    def _make_raw_buffer(self, capacity: int) -> Any:
        """Allocates a contiguous raw block of memory of size `capacity`.

        Uses ctypes.py_object to allocate an array of PyObject pointers.
        """
        return (capacity * ctypes.py_object)()

    def _normalize_index(self, index: int) -> int:
        """Converts potential negative indices to positive indices and validates bounds.

        Args:
            index: The zero-based or negative index to access.

        Returns:
            Normalized zero-based positive index.

        Raises:
            IndexError: If index is out of valid range [-size, size - 1].
        """
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of bounds for array of size {self._size}")
        return index

    def __getitem__(self, index: int) -> T:
        """Retrieves element at index in O(1) time.

        Args:
            index: Zero-based or negative index.

        Returns:
            The element stored at the specified index.
        """
        normalized_idx = self._normalize_index(index)
        return cast(T, self._raw_buffer[normalized_idx])

    def __setitem__(self, index: int, value: T) -> None:
        """Overwrites the element at index in O(1) time.

        Args:
            index: Zero-based or negative index.
            value: The new element value.
        """
        normalized_idx = self._normalize_index(index)
        self._raw_buffer[normalized_idx] = value

    def append(self, value: T) -> None:
        """Appends an element to the end of the array in Amortized O(1) time.

        If the buffer is full, triggers geometric capacity doubling.
        """
        if self._size == self._capacity:
            self._resize(self._capacity * self.GROWTH_FACTOR)

        self._raw_buffer[self._size] = value
        self._size += 1

    def pop(self) -> T:
        """Removes and returns the last element in O(1) time.

        Also shrinks capacity by half if utilization drops below 25% (load factor < 0.25).

        Returns:
            The last element.

        Raises:
            IndexError: If attempting to pop from an empty array.
        """
        if self.is_empty():
            raise IndexError("Cannot pop from an empty DynamicArray")

        last_index = self._size - 1
        value = cast(T, self._raw_buffer[last_index])
        self._raw_buffer[last_index] = None  # Clear reference to assist Garbage Collection
        self._size -= 1

        # Optional memory reclamation: shrink if load factor < 25%
        quarter_capacity = self._capacity // 4
        is_underutilized = 0 < self._size <= quarter_capacity
        if is_underutilized and self._capacity > self.DEFAULT_CAPACITY:
            new_capacity = max(self.DEFAULT_CAPACITY, self._capacity // 2)
            self._resize(new_capacity)

        return value

    def insert(self, index: int, value: T) -> None:
        """Inserts an element at a specified index in O(N) time.

        Shifts all subsequent elements to the right.
        """
        if index < 0:
            index += self._size
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of bounds for insertion into size {self._size}")

        if self._size == self._capacity:
            self._resize(self._capacity * self.GROWTH_FACTOR)

        # Shift elements to the right from end down to index
        for i in range(self._size, index, -1):
            self._raw_buffer[i] = self._raw_buffer[i - 1]

        self._raw_buffer[index] = value
        self._size += 1

    def delete_at(self, index: int) -> T:
        """Deletes and returns element at index in O(N) time.

        Shifts all subsequent elements to the left.
        """
        normalized_idx = self._normalize_index(index)
        removed_value = cast(T, self._raw_buffer[normalized_idx])

        # Shift elements to the left
        for i in range(normalized_idx, self._size - 1):
            self._raw_buffer[i] = self._raw_buffer[i + 1]

        self._raw_buffer[self._size - 1] = None  # Help GC
        self._size -= 1
        return removed_value

    def _resize(self, new_capacity: int) -> None:
        """Allocates a new contiguous raw buffer and copies existing elements.

        This is an O(N) operation that runs only occasionally during geometric resizing.
        """
        new_buffer = self._make_raw_buffer(new_capacity)
        for i in range(self._size):
            new_buffer[i] = self._raw_buffer[i]

        self._raw_buffer = new_buffer
        self._capacity = new_capacity

    def __iter__(self) -> Iterator[T]:
        """Provides an iterator over the array elements."""
        for i in range(self._size):
            yield cast(T, self._raw_buffer[i])

    def __repr__(self) -> str:
        """Returns string representation of the array."""
        elements = [repr(self[i]) for i in range(self._size)]
        joined = ", ".join(elements)
        return f"DynamicArray([{joined}], size={self._size}, capacity={self._capacity})"
