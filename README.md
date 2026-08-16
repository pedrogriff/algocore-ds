# AlgoCore: Algorithms, Data Structures & Memory Benchmarking Lab

[![CI](https://github.com/pedrogriff/algocore-ds/actions/workflows/ci.yml/badge.svg)](https://github.com/pedrogriff/algocore-ds/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Checked: MyPy](https://img.shields.io/badge/types-mypy%20strict-brightgreen.svg)](https://mypy-lang.org/)

**AlgoCore** is an educational, production-grade laboratory for Computer Science fundamentals, data structure implementations, and memory efficiency benchmarks written in Google-standard modern Python.

---

## 🏛️ Repository Architecture

```
algocore-ds/
├── .github/workflows/      # Automated CI pipeline (lint, typing, tests)
├── docs/                   # CS Architecture & Memory analysis papers
├── src/algocore/           # Core library implementations
│   ├── arrays/             # Dynamic arrays & ring buffers
│   ├── trees/              # Self-balancing trees & Tries (in progress)
│   └── heaps/              # Priority queues & min-max heaps
├── tests/                  # Unit and property-based test suites
└── benchmarks/             # CPU & memory allocation benchmarks
```

---

## 📦 Implemented Modules

### 1. `DynamicArray[T]` (`algocore.arrays.dynamic_array`)
A generic, cache-aware dynamic array operating directly on top of contiguous memory blocks allocated via `ctypes.py_object`.

* **Memory Model**: Direct pointer arithmetic over contiguous RAM blocks.
* **Amortized $O(1)$ Append**: Geometric capacity doubling ($2\times$) with mathematical invariance proofs.
* **Memory Reclamation**: Shrinks capacity by half when utilization drops below 25% to prevent memory leakage.
* **Type Safety**: Strictly typed with generics and boundary validation.

```python
from algocore.arrays import DynamicArray

arr: DynamicArray[int] = DynamicArray(initial_capacity=4)
for val in [10, 20, 30, 40, 50]:
    arr.append(val)

print(arr)  # DynamicArray([10, 20, 30, 40, 50], size=5, capacity=8)
```

---

## 🧪 Testing & Code Health

AlgoCore enforces strict Google-standard code quality:

```bash
# Run test suite
pytest

# Static Type Checking
mypy src/

# Linter & Formatting Check
ruff check .
```

---

## ⚡ Performance & Benchmarks

Run the benchmark suite to observe scaling performance across input sizes up to $N = 1,000,000$:

```bash
python -m benchmarks.bench_arrays
```

---

## 📄 License
MIT License. Built by [Pedro Griff Marcincowski](https://github.com/pedrogriff).
