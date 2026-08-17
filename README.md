# AlgoCore: Algorithms, Data Structures & Memory Benchmarking Lab

[![CI](https://github.com/pedrogriff/algocore-ds/actions/workflows/ci.yml/badge.svg)](https://github.com/pedrogriff/algocore-ds/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Checked: MyPy](https://img.shields.io/badge/types-mypy%20strict-brightgreen.svg)](https://mypy-lang.org/)
[![Test Coverage: >90%](https://img.shields.io/badge/coverage-92%25-brightgreen.svg)]()

**AlgoCore** is a production-grade laboratory for Computer Science fundamentals, data structure implementations, and memory efficiency benchmarks written in Google-standard modern Python.

---

## 🏛️ Implemented Modules & Architectures

| Module | Core Data Structure | Time Complexities | Key Engineering Features |
| :--- | :--- | :--- | :--- |
| **`algocore.arrays`** | `DynamicArray[T]` | Access: $O(1)$<br>Append: Amortized $O(1)$ | Raw memory allocation (`ctypes`), geometric $2\times$ doubling, load-factor shrinking. |
| **`algocore.arrays`** | `CircularBuffer[T]` | Push/Pop Front/Back: $O(1)$ | ArrayDeque ring buffer with modulo arithmetic; eliminates $O(N)$ shift bottlenecks. |
| **`algocore.maps`** | `HashMap[K, V]` | Read/Write/Delete: Average $O(1)$ | Open addressing with linear probing, Tombstone recycling, dynamic load-factor rehashing ($\alpha > 0.66$). |
| **`algocore.trees`** | `AVLTree[K, V]` | Search/Insert: $O(\log N)$<br>Range: $O(\log N + K)$ | Self-balancing rotations (LL/RR/LR/RL), Order-Statistic augmentation for $O(\log N)$ percentiles. |
| **`algocore.heaps`** | `MinHeap[T]` & `TopKSelector` | Push/Pop: $O(\log N)$<br>Heapify: $O(N)$<br>Top-$K$: $O(N \log K)$ | Complete binary tree in contiguous array, single-pass root replacement, streaming Top-$K$ selector. |

---

## ⚡ Empirical Benchmarks

### 1. Queue Performance: Array Shifting vs. Ring Buffer ($N = 20,000$)
- `DynamicArray` $O(N^2)$ Deletions: **43.05 seconds**
- `CircularBuffer` $O(1)$ Pointer Shifts: **0.006 seconds** (**7,000x speedup**)

### 2. Range Queries & Order Statistics ($N = 50,000$)
- 50th Percentile (Median) via $O(N \log N)$ Sort: `0.0075s`
- 50th Percentile via Augmented $O(\log N)$ `AVLTree`: `0.000020s` (**385x speedup**)

### 3. Top-$K$ Streaming Selection ($N = 1,000,000$, $K = 50$)
- Full Array Sorting: `0.2418s` ($O(N)$ memory $\approx$ 7 MB)
- Min-Heap Streaming: `0.1862s` ($O(K)$ memory $\approx$ 400 bytes)

---

## 🧪 Testing & Code Quality

```bash
# Run test suite with coverage
pytest --cov=src/algocore --cov-report=term-missing tests/

# Strict Type Checking
mypy src/

# Linter & Formatting
ruff check .
```

---

## 📄 License
MIT License. Built by [Pedro Griff Marcincowski](https://github.com/pedrogriff).
