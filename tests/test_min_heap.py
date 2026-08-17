"""Unit tests for MinHeap and TopKSelector with complex key extraction."""

import random
import unittest
from dataclasses import dataclass

from algocore.heaps.min_heap import MinHeap
from algocore.heaps.top_k import TopKSelector


@dataclass
class Employee:
    eid: str
    salary: int


class TestMinHeap(unittest.TestCase):
    """Test suite for MinHeap priority queue semantics and algorithms."""

    def test_basic_push_and_pop(self) -> None:
        """Verifies smallest elements are always popped first."""
        heap: MinHeap[int] = MinHeap()
        for num in [50, 20, 80, 10, 30]:
            heap.push(num)

        self.assertEqual(len(heap), 5)
        self.assertEqual(heap.peek(), 10)

        popped = [heap.pop() for _ in range(5)]
        self.assertEqual(popped, [10, 20, 30, 50, 80])
        self.assertTrue(heap.is_empty())

    def test_floyds_linear_heapify(self) -> None:
        """Verifies O(N) heapify on arbitrary unorganized lists."""
        data = [90, 40, 70, 10, 30, 80, 20, 60, 50]
        heap: MinHeap[int] = MinHeap(items=data)

        self.assertEqual(len(heap), len(data))
        popped = [heap.pop() for _ in range(len(data))]
        self.assertEqual(popped, sorted(data))

    def test_custom_key_function(self) -> None:
        """Verifies heapifying custom objects by attribute (Employee salary)."""
        employees = [
            Employee("emp_3", 190_000),
            Employee("emp_1", 140_000),
            Employee("emp_4", 250_000),
            Employee("emp_2", 170_000),
        ]
        heap: MinHeap[Employee] = MinHeap(items=employees, key=lambda e: e.salary)

        self.assertEqual(heap.peek().eid, "emp_1")
        lowest_paid = heap.pop()
        self.assertEqual(lowest_paid.eid, "emp_1")
        self.assertEqual(lowest_paid.salary, 140_000)

    def test_replace_and_pushpop(self) -> None:
        """Verifies atomic O(log N) root replacement."""
        heap: MinHeap[int] = MinHeap(items=[20, 40, 60])
        old_root = heap.replace(50)
        self.assertEqual(old_root, 20)
        self.assertEqual(heap.peek(), 40)

        # pushpop with smaller item (should return item immediately)
        res = heap.pushpop(10)
        self.assertEqual(res, 10)
        self.assertEqual(heap.peek(), 40)

    def test_empty_exceptions(self) -> None:
        """Verifies IndexError on empty operations."""
        heap: MinHeap[int] = MinHeap()
        with self.assertRaises(IndexError):
            heap.pop()
        with self.assertRaises(IndexError):
            heap.peek()
        with self.assertRaises(IndexError):
            heap.replace(10)


class TestTopKSelector(unittest.TestCase):
    """Test suite for streaming Top-K selection."""

    def test_top_k_basic(self) -> None:
        """Verifies top-K selection matches sorted order."""
        numbers = [15, 3, 99, 42, 8, 77, 23, 61, 105, 12]
        k = 4
        top_4 = TopKSelector.find_top_k(numbers, k=k)
        expected = sorted(numbers, reverse=True)[:k]
        self.assertEqual(top_4, expected)

    def test_top_k_large_random_stream(self) -> None:
        """Verifies top-K selection on 10,000 streaming elements."""
        stream = [random.randint(1, 1_000_000) for _ in range(10_000)]
        k = 25
        top_k = TopKSelector.find_top_k(stream, k=k)
        expected = sorted(stream, reverse=True)[:k]
        self.assertEqual(top_k, expected)

    def test_top_k_compensation_records(self) -> None:
        """Verifies finding top 3 highest earning employees."""
        records = [
            Employee("alice", 180_000),
            Employee("bob", 240_000),
            Employee("charlie", 150_000),
            Employee("david", 310_000),
            Employee("eva", 290_000),
        ]
        top_3 = TopKSelector.find_top_k(records, k=3, key=lambda e: e.salary)
        self.assertEqual([e.eid for e in top_3], ["david", "eva", "bob"])

    def test_edge_cases(self) -> None:
        """Verifies k=0 and k > len(stream)."""
        self.assertEqual(TopKSelector.find_top_k([1, 2, 3], k=0), [])
        self.assertEqual(TopKSelector.find_top_k([1, 2, 3], k=5), [3, 2, 1])


if __name__ == "__main__":
    unittest.main()
