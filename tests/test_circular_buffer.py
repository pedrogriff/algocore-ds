"""Unit tests for CircularBuffer (ArrayDeque) with strict invariant checking."""

import unittest

from algocore.arrays.circular_buffer import CircularBuffer


class TestCircularBuffer(unittest.TestCase):
    """Test suite for CircularBuffer operations, wrap-around semantics, and resizing."""

    def test_initialization(self) -> None:
        """Verifies initial state and defaults."""
        buf: CircularBuffer[int] = CircularBuffer()
        self.assertEqual(len(buf), 0)
        self.assertTrue(buf.is_empty())
        self.assertEqual(buf.capacity, CircularBuffer.DEFAULT_CAPACITY)

    def test_invalid_capacity(self) -> None:
        """Verifies capacity validation."""
        with self.assertRaises(ValueError):
            CircularBuffer(initial_capacity=0)

    def test_fifo_queue_operations(self) -> None:
        """Verifies FIFO queue pattern: push_back and pop_front."""
        buf: CircularBuffer[str] = CircularBuffer(initial_capacity=4)
        buf.push_back("Job-1")
        buf.push_back("Job-2")
        buf.push_back("Job-3")

        self.assertEqual(buf.peek_front(), "Job-1")
        self.assertEqual(buf.peek_back(), "Job-3")
        self.assertEqual(len(buf), 3)

        self.assertEqual(buf.pop_front(), "Job-1")
        self.assertEqual(buf.pop_front(), "Job-2")
        self.assertEqual(buf.pop_front(), "Job-3")
        self.assertTrue(buf.is_empty())

    def test_modulo_wrap_around_without_resizing(self) -> None:
        """Verifies pointers wrap around buffer boundaries correctly."""
        buf: CircularBuffer[int] = CircularBuffer(initial_capacity=4)

        # Push 3 items, pop 2 items -> head advances
        buf.push_back(10)
        buf.push_back(20)
        buf.push_back(30)
        self.assertEqual(buf.pop_front(), 10)
        self.assertEqual(buf.pop_front(), 20)

        # Push 3 more items -> tail wraps around to index 0 and 1
        buf.push_back(40)
        buf.push_back(50)
        buf.push_back(60)

        self.assertEqual(len(buf), 4)
        self.assertEqual(buf.capacity, 4)  # No resize needed yet!
        self.assertEqual(list(buf), [30, 40, 50, 60])

        self.assertEqual(buf.pop_front(), 30)
        self.assertEqual(buf.pop_front(), 40)
        self.assertEqual(buf.pop_front(), 50)
        self.assertEqual(buf.pop_front(), 60)
        self.assertTrue(buf.is_empty())

    def test_push_front_and_pop_back(self) -> None:
        """Verifies double-ended deque capabilities."""
        buf: CircularBuffer[int] = CircularBuffer(initial_capacity=4)
        buf.push_front(10)
        buf.push_front(20)
        buf.push_back(30)

        # Logical order: [20, 10, 30]
        self.assertEqual(list(buf), [20, 10, 30])
        self.assertEqual(buf.pop_back(), 30)
        self.assertEqual(buf.pop_front(), 20)
        self.assertEqual(buf.pop_front(), 10)

    def test_resizing_unrolls_correctly(self) -> None:
        """Verifies unrolling of wrap-around state during capacity doubling."""
        buf: CircularBuffer[int] = CircularBuffer(initial_capacity=3)
        buf.push_back(1)
        buf.push_back(2)
        buf.pop_front()  # head is at 1

        buf.push_back(3)
        buf.push_back(4)  # Buffer is full, wrap-around in place

        # Trigger resize on next push: 3 -> 6
        buf.push_back(5)
        self.assertEqual(buf.capacity, 6)
        self.assertEqual(list(buf), [2, 3, 4, 5])

    def test_indexing(self) -> None:
        """Verifies random access relative to logical head."""
        buf: CircularBuffer[str] = CircularBuffer(initial_capacity=4)
        buf.push_back("A")
        buf.push_back("B")
        buf.push_back("C")
        buf.pop_front()  # Removes 'A'
        buf.push_back("D")

        # Elements are ['B', 'C', 'D']
        self.assertEqual(buf[0], "B")
        self.assertEqual(buf[1], "C")
        self.assertEqual(buf[2], "D")
        self.assertEqual(buf[-1], "D")

    def test_empty_exceptions(self) -> None:
        """Verifies exceptions on empty operations."""
        buf: CircularBuffer[int] = CircularBuffer()
        with self.assertRaises(IndexError):
            buf.pop_front()
        with self.assertRaises(IndexError):
            buf.pop_back()
        with self.assertRaises(IndexError):
            buf.peek_front()
        with self.assertRaises(IndexError):
            buf.peek_back()


if __name__ == "__main__":
    unittest.main()
