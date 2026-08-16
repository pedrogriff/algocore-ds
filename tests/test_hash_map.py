"""Unit tests for HashMap verifying open addressing, tombstone recycling, and rehashing."""

import unittest

from algocore.maps.hash_map import HashMap


class TestHashMap(unittest.TestCase):
    """Test suite for HashMap operations and invariants."""

    def test_initialization(self) -> None:
        """Verifies initial empty state and default capacity."""
        hmap: HashMap[str, int] = HashMap()
        self.assertEqual(len(hmap), 0)
        self.assertTrue(hmap.is_empty())
        self.assertEqual(hmap.capacity, HashMap.DEFAULT_CAPACITY)

    def test_basic_put_and_get(self) -> None:
        """Verifies basic insert, lookup, and updates."""
        hmap: HashMap[str, int] = HashMap()
        hmap["alice"] = 180_000
        hmap["bob"] = 195_000
        hmap["charlie"] = 210_000

        self.assertEqual(len(hmap), 3)
        self.assertEqual(hmap["alice"], 180_000)
        self.assertEqual(hmap["bob"], 195_000)
        self.assertEqual(hmap["charlie"], 210_000)

        # Update existing key
        hmap["alice"] = 190_000
        self.assertEqual(hmap["alice"], 190_000)
        self.assertEqual(len(hmap), 3)

    def test_tombstone_probe_chain_preservation(self) -> None:
        """Verifies deleting an element does not break search for colliding elements."""
        # Force a small capacity of 4 to guarantee collisions
        hmap: HashMap[str, str] = HashMap(initial_capacity=4)

        hmap["key1"] = "val1"
        hmap["key2"] = "val2"

        # Delete key1 -> leaves a Tombstone
        del hmap["key1"]
        self.assertNotIn("key1", hmap)
        self.assertEqual(len(hmap), 1)

        # key2 must still be found even if it probed past key1
        self.assertIn("key2", hmap)
        self.assertEqual(hmap["key2"], "val2")

    def test_tombstone_recycling(self) -> None:
        """Verifies that new insertions reclaim tombstone slots."""
        hmap: HashMap[str, int] = HashMap(initial_capacity=4)
        hmap["A"] = 1
        hmap["B"] = 2
        del hmap["A"]

        # Insert new key 'C' -> should reuse tombstone slot without premature resize
        hmap["C"] = 3
        self.assertEqual(len(hmap), 2)
        self.assertEqual(hmap["C"], 3)
        self.assertEqual(hmap["B"], 2)

    def test_dynamic_rehashing_and_tombstone_purge(self) -> None:
        """Verifies that exceeding MAX_LOAD_FACTOR triggers capacity doubling."""
        hmap: HashMap[int, str] = HashMap(initial_capacity=4)
        hmap[1] = "one"
        hmap[2] = "two"
        self.assertEqual(hmap.capacity, 4)

        # 3rd insert triggers load factor (3/4 = 0.75 >= 0.66) -> capacity doubles to 8
        hmap[3] = "three"
        self.assertEqual(hmap.capacity, 8)
        self.assertEqual(len(hmap), 3)

        # Verify all elements survived rehashing
        self.assertEqual(hmap[1], "one")
        self.assertEqual(hmap[2], "two")
        self.assertEqual(hmap[3], "three")

    def test_missing_key_behavior(self) -> None:
        """Verifies KeyError on non-existent keys and get() default return."""
        hmap: HashMap[str, int] = HashMap()
        with self.assertRaises(KeyError):
            _ = hmap["non_existent"]

        with self.assertRaises(KeyError):
            del hmap["non_existent"]

        self.assertIsNone(hmap.get("non_existent"))
        self.assertEqual(hmap.get("non_existent", default=42), 42)

    def test_iteration(self) -> None:
        """Verifies iteration over keys, values, and items."""
        hmap: HashMap[str, int] = HashMap()
        data = {"A": 10, "B": 20, "C": 30}
        for k, v in data.items():
            hmap[k] = v

        self.assertEqual(set(hmap.keys()), {"A", "B", "C"})
        self.assertEqual(set(hmap.values()), {10, 20, 30})
        self.assertEqual(set(hmap.items()), {("A", 10), ("B", 20), ("C", 30)})

    def test_stress_integrity(self) -> None:
        """Stress test with 2,000 inserts, updates, and deletes."""
        hmap: HashMap[int, int] = HashMap()
        n = 2_000

        # Insert 2,000 elements
        for i in range(n):
            hmap[i] = i * 10

        self.assertEqual(len(hmap), n)
        for i in range(n):
            self.assertEqual(hmap[i], i * 10)

        # Delete odd numbers
        for i in range(1, n, 2):
            del hmap[i]

        self.assertEqual(len(hmap), n // 2)

        # Verify even numbers remain accessible
        for i in range(0, n, 2):
            self.assertEqual(hmap[i], i * 10)

        # Verify odd numbers are gone
        for i in range(1, n, 2):
            self.assertNotIn(i, hmap)


if __name__ == "__main__":
    unittest.main()
