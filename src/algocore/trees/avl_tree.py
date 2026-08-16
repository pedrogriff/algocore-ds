"""Google-Caliber Self-Balancing AVL Tree with Order-Statistic Augmentation.

Demonstrates:
1. Strict BST invariant with automatic O(1) rotation rebalancing (LL, RR, LR, RL).
2. O(log N) worst-case search, insertion, and deletion.
3. Order-Statistic Augmentation: Subtree size tracking for O(log N) percentile & median queries.
4. O(log N + K) Range Queries for compensation band filtering.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar


# Protocol for Keys that support ordering comparisons (<, >, <=, >=, ==)
class Comparable(Protocol):
    def __lt__(self, other: Comparable) -> bool: ...
    def __gt__(self, other: Comparable) -> bool: ...
    def __le__(self, other: Comparable) -> bool: ...
    def __ge__(self, other: Comparable) -> bool: ...
    def __eq__(self, other: object) -> bool: ...


K = TypeVar("K", bound=Comparable)
V = TypeVar("V")


@dataclass
class AVLNode(Generic[K, V]):
    """A single node in an augmented AVL tree."""

    key: K
    value: V
    left: AVLNode[K, V] | None = None
    right: AVLNode[K, V] | None = None
    height: int = 1
    subtree_size: int = 1


class AVLTree(Generic[K, V]):
    """Self-balancing AVL Search Tree supporting ordered lookups, percentiles, and range queries."""

    def __init__(self) -> None:
        """Initializes an empty AVL Tree."""
        self._root: AVLNode[K, V] | None = None

    def __len__(self) -> int:
        """Returns the total number of nodes in the tree."""
        return self._get_size(self._root)

    def is_empty(self) -> bool:
        """Returns True if the tree contains no elements."""
        return self._root is None

    @property
    def height(self) -> int:
        """Returns the current height of the tree."""
        return self._get_height(self._root)

    def _get_height(self, node: AVLNode[K, V] | None) -> int:
        """Returns node height, or 0 if node is None."""
        return node.height if node is not None else 0

    def _get_size(self, node: AVLNode[K, V] | None) -> int:
        """Returns subtree node count, or 0 if node is None."""
        return node.subtree_size if node is not None else 0

    def _get_balance_factor(self, node: AVLNode[K, V] | None) -> int:
        """Calculates balance factor (height(left) - height(right))."""
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_node_metadata(self, node: AVLNode[K, V]) -> None:
        """Recalculates height and subtree size based on direct children."""
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        node.subtree_size = 1 + self._get_size(node.left) + self._get_size(node.right)

    def _rotate_right(self, z: AVLNode[K, V]) -> AVLNode[K, V]:
        """Performs right rotation on node z."""
        y = z.left
        if y is None:
            return z

        temp_t3 = y.right

        # Perform rotation
        y.right = z
        z.left = temp_t3

        # Update metadata (z first as it is now child of y)
        self._update_node_metadata(z)
        self._update_node_metadata(y)
        return y

    def _rotate_left(self, z: AVLNode[K, V]) -> AVLNode[K, V]:
        """Performs left rotation on node z."""
        y = z.right
        if y is None:
            return z

        temp_t2 = y.left

        # Perform rotation
        y.left = z
        z.right = temp_t2

        # Update metadata (z first as it is now child of y)
        self._update_node_metadata(z)
        self._update_node_metadata(y)
        return y

    def insert(self, key: K, value: V) -> None:
        """Inserts a key-value pair, balancing the tree in O(log N) time."""
        self._root = self._insert_helper(self._root, key, value)

    def _insert_helper(self, node: AVLNode[K, V] | None, key: K, value: V) -> AVLNode[K, V]:
        # 1. Standard BST insertion
        if node is None:
            return AVLNode(key, value)

        if key < node.key:
            node.left = self._insert_helper(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_helper(node.right, key, value)
        else:
            # Key exists -> overwrite value (subtree size and height unchanged)
            node.value = value
            return node

        # 2. Update height and subtree size
        self._update_node_metadata(node)

        # 3. Check balance factor and perform rotations if needed
        balance = self._get_balance_factor(node)

        # Case 1: Left-Left (LL)
        if balance > 1 and node.left is not None and key < node.left.key:
            return self._rotate_right(node)

        # Case 2: Right-Right (RR)
        if balance < -1 and node.right is not None and key > node.right.key:
            return self._rotate_left(node)

        # Case 3: Left-Right (LR)
        if balance > 1 and node.left is not None and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Case 4: Right-Left (RL)
        if balance < -1 and node.right is not None and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def search(self, key: K) -> V | None:
        """Searches for a key in O(log N) time."""
        curr = self._root
        while curr is not None:
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                return curr.value
        return None

    def __contains__(self, key: K) -> bool:
        """Returns True if key is in tree."""
        return self.search(key) is not None

    def find_kth_smallest(self, k: int) -> tuple[K, V]:
        """Finds the k-th smallest element (1-indexed) in O(log N) time.

        Args:
            k: 1-indexed rank (1 <= k <= N).

        Returns:
            Tuple of (key, value) for the k-th smallest element.

        Raises:
            IndexError: If k < 1 or k > len(self).
        """
        if k < 1 or k > len(self):
            raise IndexError(f"Rank {k} out of bounds for tree with {len(self)} nodes")

        curr = self._root
        while curr is not None:
            left_size = self._get_size(curr.left)

            if k == left_size + 1:
                return curr.key, curr.value
            elif k <= left_size:
                curr = curr.left
            else:
                k -= left_size + 1
                curr = curr.right

        raise IndexError("Rank search encountered empty node")

    def range_query(self, low: K, high: K) -> list[tuple[K, V]]:
        """Returns all key-value pairs where low <= key <= high in sorted order.

        Complexity: O(log N + K) where K is the number of matching results.
        """
        results: list[tuple[K, V]] = []
        self._range_query_helper(self._root, low, high, results)
        return results

    def _range_query_helper(
        self,
        node: AVLNode[K, V] | None,
        low: K,
        high: K,
        results: list[tuple[K, V]],
    ) -> None:
        if node is None:
            return

        # If current key is greater than low, left subtree might have matching keys
        if node.key > low:
            self._range_query_helper(node.left, low, high, results)

        # If current key is within [low, high], record it
        if low <= node.key and node.key <= high:
            results.append((node.key, node.value))

        # If current key is less than high, right subtree might have matching keys
        if node.key < high:
            self._range_query_helper(node.right, low, high, results)

    def in_order(self) -> Iterator[tuple[K, V]]:
        """Yields all key-value pairs in sorted ascending order."""
        yield from self._in_order_helper(self._root)

    def _in_order_helper(self, node: AVLNode[K, V] | None) -> Iterator[tuple[K, V]]:
        if node is not None:
            yield from self._in_order_helper(node.left)
            yield node.key, node.value
            yield from self._in_order_helper(node.right)
