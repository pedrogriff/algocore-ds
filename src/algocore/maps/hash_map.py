"""Google-Caliber Open-Addressing Hash Map with Tombstone Recycling.

Demonstrates:
1. Hash compression and bucket index mapping.
2. Open addressing with linear probing.
3. Tombstone sentinel markers for safe O(1) deletions without broken probe chains.
4. Tombstone recycling during insertions.
5. Dynamic load-factor based rehashing (alpha > 0.66).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Iterator, TypeVar, cast

K = TypeVar("K")
V = TypeVar("V")


# Unique sentinel marker for deleted slots (Tombstones)
_TOMBSTONE: object = object()


@dataclass
class _Entry(Generic[K, V]):
    """Internal key-value pair stored in a bucket."""

    key: K
    value: V


class HashMap(Generic[K, V]):
    """An open-addressing hash table with linear probing and tombstone recycling."""

    DEFAULT_CAPACITY: int = 8
    MAX_LOAD_FACTOR: float = 0.66
    GROWTH_FACTOR: int = 2

    def __init__(self, initial_capacity: int = DEFAULT_CAPACITY) -> None:
        """Initializes HashMap with given initial capacity."""
        if initial_capacity <= 0:
            raise ValueError(f"Capacity must be positive, got {initial_capacity}")

        self._capacity: int = initial_capacity
        self._size: int = 0
        self._tombstones_count: int = 0
        self._buckets: list[Any] = [None] * self._capacity

    @property
    def capacity(self) -> int:
        """Returns total allocated bucket capacity."""
        return self._capacity

    @property
    def load_factor(self) -> float:
        """Returns current load factor (active elements + tombstones / capacity)."""
        return (self._size + self._tombstones_count) / self._capacity

    def __len__(self) -> int:
        """Returns number of active key-value pairs."""
        return self._size

    def is_empty(self) -> bool:
        """Returns True if map contains no elements."""
        return self._size == 0

    def _hash(self, key: K) -> int:
        """Computes positive bucket index for key."""
        return (hash(key) & 0x7FFFFFFF) % self._capacity

    def _find_slot(self, key: K) -> tuple[int, bool, int | None]:
        """Probes the bucket array for a matching key or an available insertion slot.

        Returns:
            A tuple of (slot_index, found, first_tombstone_index).
            - slot_index: index where key was found, or terminal empty slot if not found.
            - found: True if key is currently in the map.
            - first_tombstone_index: index of first encountered tombstone to recycle on insert.
        """
        start_idx = self._hash(key)
        first_tombstone: int | None = None

        for step in range(self._capacity):
            idx = (start_idx + step) % self._capacity
            slot = self._buckets[idx]

            if slot is None:
                # Reached terminal empty slot -> key does not exist
                return idx, False, first_tombstone

            if slot is _TOMBSTONE:
                # Record the first available tombstone for insertion recycling
                if first_tombstone is None:
                    first_tombstone = idx
                continue

            entry = cast(_Entry[K, V], slot)
            if entry.key == key:
                return idx, True, first_tombstone

        # Buffer is completely probed without hitting None
        return -1, False, first_tombstone

    def __setitem__(self, key: K, value: V) -> None:
        """Inserts or updates a key-value pair in Average O(1) time."""
        idx, found, first_tombstone = self._find_slot(key)

        if found:
            # Key exists -> overwrite value
            cast(_Entry[K, V], self._buckets[idx]).value = value
            return

        # Check if adding a new key exceeds load factor
        prospective_load = (self._size + 1 + self._tombstones_count) / self._capacity
        if prospective_load > self.MAX_LOAD_FACTOR:
            self._resize(self._capacity * self.GROWTH_FACTOR)
            # Recompute slot after resizing
            idx, found, first_tombstone = self._find_slot(key)

        # Key does not exist -> insert new entry
        # If we passed a tombstone, recycle it to keep the table compact
        target_idx = first_tombstone if first_tombstone is not None else idx
        if first_tombstone is not None:
            self._tombstones_count -= 1

        self._buckets[target_idx] = _Entry(key, value)
        self._size += 1

    def __getitem__(self, key: K) -> V:
        """Retrieves value for key in Average O(1) time.

        Raises:
            KeyError: If key does not exist.
        """
        idx, found, _ = self._find_slot(key)
        if not found or idx == -1:
            raise KeyError(f"Key {key!r} not found")

        return cast(_Entry[K, V], self._buckets[idx]).value

    def get(self, key: K, default: V | None = None) -> V | None:
        """Returns value if key exists, else default."""
        try:
            return self[key]
        except KeyError:
            return default

    def __delitem__(self, key: K) -> None:
        """Deletes key by placing a Tombstone sentinel in Average O(1) time.

        Raises:
            KeyError: If key does not exist.
        """
        idx, found, _ = self._find_slot(key)
        if not found or idx == -1:
            raise KeyError(f"Key {key!r} not found")

        # Place tombstone to preserve probe chains
        self._buckets[idx] = _TOMBSTONE
        self._size -= 1
        self._tombstones_count += 1

    def __contains__(self, key: object) -> bool:
        """Returns True if key exists in the map."""
        idx, found, _ = self._find_slot(cast(K, key))
        return found and idx != -1

    def _resize(self, new_capacity: int) -> None:
        """Rehashes all active entries into a larger bucket array, purging tombstones."""
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [None] * new_capacity
        self._size = 0
        self._tombstones_count = 0

        for slot in old_buckets:
            if slot is not None and slot is not _TOMBSTONE:
                entry = cast(_Entry[K, V], slot)
                self[entry.key] = entry.value

    def keys(self) -> Iterator[K]:
        """Iterates over all active keys."""
        for slot in self._buckets:
            if slot is not None and slot is not _TOMBSTONE:
                yield cast(_Entry[K, V], slot).key

    def values(self) -> Iterator[V]:
        """Iterates over all active values."""
        for slot in self._buckets:
            if slot is not None and slot is not _TOMBSTONE:
                yield cast(_Entry[K, V], slot).value

    def items(self) -> Iterator[tuple[K, V]]:
        """Iterates over all active (key, value) pairs."""
        for slot in self._buckets:
            if slot is not None and slot is not _TOMBSTONE:
                entry = cast(_Entry[K, V], slot)
                yield entry.key, entry.value

    def __iter__(self) -> Iterator[K]:
        """Iterates over keys."""
        return self.keys()

    def __repr__(self) -> str:
        pairs = [f"{k!r}: {v!r}" for k, v in self.items()]
        return f"HashMap({{{', '.join(pairs)}}}, size={self._size}, capacity={self._capacity})"
