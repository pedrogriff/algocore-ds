"""Unit tests for AVLTree self-balancing, order statistics, and range queries."""

import math
import unittest

from algocore.trees.avl_tree import AVLTree


class TestAVLTree(unittest.TestCase):
    """Test suite for AVLTree operations and invariants."""

    def test_initialization(self) -> None:
        """Verifies initial empty state."""
        tree: AVLTree[int, str] = AVLTree()
        self.assertEqual(len(tree), 0)
        self.assertTrue(tree.is_empty())
        self.assertEqual(tree.height, 0)

    def test_search_and_insert(self) -> None:
        """Verifies inserting and searching elements."""
        tree: AVLTree[str, int] = AVLTree()
        tree.insert("alice", 180_000)
        tree.insert("bob", 195_000)
        tree.insert("charlie", 210_000)

        self.assertEqual(len(tree), 3)
        self.assertEqual(tree.search("alice"), 180_000)
        self.assertEqual(tree.search("bob"), 195_000)
        self.assertEqual(tree.search("charlie"), 210_000)
        self.assertIsNone(tree.search("david"))

    def test_strict_balance_on_sorted_inputs(self) -> None:
        """Verifies that inserting strictly sorted numbers maintains O(log N) height."""
        tree: AVLTree[int, int] = AVLTree()
        n = 1_000

        # Inserting sequential numbers would create a degenerate linked list (height 1,000) in naive BST
        for i in range(1, n + 1):
            tree.insert(i, i * 10)

        self.assertEqual(len(tree), n)

        # AVL Tree height is guaranteed to be <= 1.44 * log2(n + 2)
        max_allowed_height = math.ceil(1.44 * math.log2(n + 2))
        self.assertLessEqual(tree.height, max_allowed_height)

        # Check all values can be retrieved
        for i in range(1, n + 1):
            self.assertEqual(tree.search(i), i * 10)

    def test_in_order_traversal(self) -> None:
        """Verifies in-order traversal produces strictly sorted output."""
        tree: AVLTree[int, str] = AVLTree()
        values = [50, 20, 70, 10, 30, 60, 80]
        for val in values:
            tree.insert(val, f"val_{val}")

        sorted_keys = [k for k, _ in tree.in_order()]
        self.assertEqual(sorted_keys, [10, 20, 30, 50, 60, 70, 80])

    def test_range_queries(self) -> None:
        """Verifies O(log N + K) range filtering for compensation bands."""
        tree: AVLTree[int, str] = AVLTree()
        # Insert compensation data: salary -> employee name
        salaries = [
            (120_000, "Alice"),
            (150_000, "Bob"),
            (180_000, "Charlie"),
            (200_000, "David"),
            (220_000, "Eva"),
            (260_000, "Frank"),
            (300_000, "Grace"),
        ]
        for sal, name in salaries:
            tree.insert(sal, name)

        # Query all employees earning between $160,000 and $240,000
        results = tree.range_query(160_000, 240_000)
        expected = [(180_000, "Charlie"), (200_000, "David"), (220_000, "Eva")]
        self.assertEqual(results, expected)

    def test_order_statistics_percentiles(self) -> None:
        """Verifies O(log N) calculation of min, max, median, and percentiles."""
        tree: AVLTree[int, str] = AVLTree()
        n = 100

        for i in range(1, n + 1):
            tree.insert(i * 1_000, f"emp_{i}")

        # Minimum (1st smallest)
        min_key, min_val = tree.find_kth_smallest(1)
        self.assertEqual(min_key, 1_000)
        self.assertEqual(min_val, "emp_1")

        # Maximum (100th smallest)
        max_key, max_val = tree.find_kth_smallest(100)
        self.assertEqual(max_key, 100_000)
        self.assertEqual(max_val, "emp_100")

        # Median (50th smallest)
        median_key, median_val = tree.find_kth_smallest(50)
        self.assertEqual(median_key, 50_000)
        self.assertEqual(median_val, "emp_50")

        # 90th percentile (90th smallest)
        p90_key, p90_val = tree.find_kth_smallest(90)
        self.assertEqual(p90_key, 90_000)
        self.assertEqual(p90_val, "emp_90")

    def test_order_statistic_bounds_error(self) -> None:
        """Verifies rank out of bounds raises IndexError."""
        tree: AVLTree[int, str] = AVLTree()
        tree.insert(10, "ten")

        with self.assertRaises(IndexError):
            tree.find_kth_smallest(0)

        with self.assertRaises(IndexError):
            tree.find_kth_smallest(2)


if __name__ == "__main__":
    unittest.main()
