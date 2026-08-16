"""Unit tests for DynamicArray demonstrating Google-caliber testing rigor.

Uses standard library unittest with pytest compatibility.
"""

import unittest

from algocore.arrays.dynamic_array import DynamicArray


class TestDynamicArray(unittest.TestCase):
    """Test suite for DynamicArray functionality, boundary conditions, and memory invariants."""

    def test_initialization_defaults(self) -> None:
        """Verifies default capacity and initial empty state."""
        arr: DynamicArray[int] = DynamicArray()
        self.assertEqual(len(arr), 0)
        self.assertTrue(arr.is_empty())
        self.assertEqual(arr.capacity, DynamicArray.DEFAULT_CAPACITY)

    def test_custom_capacity_initialization(self) -> None:
        """Verifies initializing with a custom valid capacity."""
        arr: DynamicArray[str] = DynamicArray(initial_capacity=10)
        self.assertEqual(arr.capacity, 10)
        self.assertEqual(len(arr), 0)

    def test_invalid_capacity_raises_error(self) -> None:
        """Verifies that non-positive initial capacity raises ValueError."""
        with self.assertRaises(ValueError):
            DynamicArray(initial_capacity=0)

        with self.assertRaises(ValueError):
            DynamicArray(initial_capacity=-5)

    def test_append_and_geometric_resizing(self) -> None:
        """Tests that appending doubles capacity when full."""
        arr: DynamicArray[int] = DynamicArray(initial_capacity=2)
        self.assertEqual(arr.capacity, 2)

        arr.append(10)
        arr.append(20)
        self.assertEqual(len(arr), 2)
        self.assertEqual(arr.capacity, 2)

        # 3rd append should trigger resize: 2 -> 4
        arr.append(30)
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr.capacity, 4)
        self.assertEqual(list(arr), [10, 20, 30])

        # 5th append should trigger resize: 4 -> 8
        arr.append(40)
        arr.append(50)
        self.assertEqual(len(arr), 5)
        self.assertEqual(arr.capacity, 8)
        self.assertEqual(list(arr), [10, 20, 30, 40, 50])

    def test_getitem_and_setitem(self) -> None:
        """Verifies O(1) random access reads and writes."""
        arr: DynamicArray[str] = DynamicArray()
        arr.append("alpha")
        arr.append("bravo")
        arr.append("charlie")

        self.assertEqual(arr[0], "alpha")
        self.assertEqual(arr[1], "bravo")
        self.assertEqual(arr[2], "charlie")

        # Negative indexing
        self.assertEqual(arr[-1], "charlie")
        self.assertEqual(arr[-2], "bravo")
        self.assertEqual(arr[-3], "alpha")

        # Update
        arr[1] = "beta"
        self.assertEqual(arr[1], "beta")
        self.assertEqual(list(arr), ["alpha", "beta", "charlie"])

    def test_out_of_bounds_access_raises_index_error(self) -> None:
        """Verifies bounds checking prevents buffer over-reads."""
        arr: DynamicArray[int] = DynamicArray()
        arr.append(1)

        with self.assertRaises(IndexError):
            _ = arr[1]

        with self.assertRaises(IndexError):
            _ = arr[-2]

        with self.assertRaises(IndexError):
            arr[5] = 99

    def test_pop_and_shrinking(self) -> None:
        """Verifies popping elements and memory reclamation."""
        arr: DynamicArray[int] = DynamicArray(initial_capacity=4)
        for i in range(16):
            arr.append(i)

        self.assertEqual(arr.capacity, 16)
        self.assertEqual(len(arr), 16)

        popped = arr.pop()
        self.assertEqual(popped, 15)
        self.assertEqual(len(arr), 15)

        # Pop down until load factor < 25% to trigger shrinking
        while len(arr) > 4:
            arr.pop()

        # At size 4 out of 16 (25%), next pop shrinks capacity: 16 -> 8
        arr.pop()
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr.capacity, 8)

    def test_pop_empty_raises_error(self) -> None:
        """Verifies pop on empty array raises IndexError."""
        arr: DynamicArray[int] = DynamicArray()
        with self.assertRaises(IndexError):
            arr.pop()

    def test_insert_at_indices(self) -> None:
        """Verifies inserting at beginning, middle, and end."""
        arr: DynamicArray[str] = DynamicArray(initial_capacity=2)
        arr.append("B")
        arr.append("D")

        # Insert at beginning
        arr.insert(0, "A")
        self.assertEqual(list(arr), ["A", "B", "D"])

        # Insert in middle
        arr.insert(2, "C")
        self.assertEqual(list(arr), ["A", "B", "C", "D"])

        # Insert at end (equivalent to append)
        arr.insert(4, "E")
        self.assertEqual(list(arr), ["A", "B", "C", "D", "E"])

    def test_delete_at_indices(self) -> None:
        """Verifies deleting from start, middle, and end."""
        arr: DynamicArray[int] = DynamicArray()
        for i in [10, 20, 30, 40, 50]:
            arr.append(i)

        # Delete middle
        removed = arr.delete_at(2)
        self.assertEqual(removed, 30)
        self.assertEqual(list(arr), [10, 20, 40, 50])

        # Delete head
        removed = arr.delete_at(0)
        self.assertEqual(removed, 10)
        self.assertEqual(list(arr), [20, 40, 50])

        # Delete tail
        removed = arr.delete_at(2)
        self.assertEqual(removed, 50)
        self.assertEqual(list(arr), [20, 40])

    def test_large_scale_integrity(self) -> None:
        """Stress test verifying 10,000 continuous insertions and lookups."""
        arr: DynamicArray[int] = DynamicArray()
        n = 10_000

        for i in range(n):
            arr.append(i * 2)

        self.assertEqual(len(arr), n)
        for i in range(n):
            self.assertEqual(arr[i], i * 2)


if __name__ == "__main__":
    unittest.main()
