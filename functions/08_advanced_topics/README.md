# 08. Advanced Topics

[← Back to Functions](../functions.md) | [Previous: Generators](../07_generators/)

## 📚 Table of Contents

1. [Introduction](#1-introduction)
2. [Recursion](#2-recursion)
3. [Async Functions](#3-async-functions)
4. [Partial Application](#4-partial-application)
5. [Memoization](#5-memoization)
6. [Summary](#6-summary)

---

## 1. Introduction

This section covers advanced Python function topics that enable powerful programming patterns and optimizations.

### Topics Covered

| Topic | Description | Use Cases |
|-------|-------------|-----------|
| **Recursion** | Functions calling themselves | Trees, graphs, divide-and-conquer |
| **Async Functions** | Non-blocking concurrent execution | I/O-bound operations, network requests |
| **Partial Application** | Pre-fill function arguments | Callbacks, configuration |
| **Memoization** | Cache function results | Expensive computations, recursion |

---

## 2. Recursion

**File**: [`recursion.py`](recursion.py)

### 2.1. Basic Recursion Pattern

**File**: [`recursion.py`](recursion.py) - Line 24

```python
def factorial(n):
    # Base case: stop recursion
    if n <= 1:
        return 1
    
    # Recursive case: call itself
    return n * factorial(n - 1)

# How it works:
# factorial(5)
# = 5 * factorial(4)
# = 5 * 4 * factorial(3)
# = 5 * 4 * 3 * factorial(2)
# = 5 * 4 * 3 * 2 * factorial(1)
# = 5 * 4 * 3 * 2 * 1
# = 120
```

### 🔑 Recursion Requirements

1. **Base case**: Condition to stop recursion (critical!)
2. **Recursive case**: Function calls itself with modified input
3. **Progress**: Each call must move toward base case

### 2.2. Fibonacci (Inefficient)

**File**: [`recursion.py`](recursion.py) - Line 42

```python
def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

# Problem: Exponential time complexity O(2^n)
# fibonacci(5) calls fibonacci(4) and fibonacci(3)
# fibonacci(4) calls fibonacci(3) and fibonacci(2)
# fibonacci(3) is computed TWICE!
```

### 2.3. List Recursion

**File**: [`recursion.py`](recursion.py) - Line 78

```python
def reverse_list(items):
    if len(items) <= 1:
        return items
    
    # Last element + reverse of rest
    return [items[-1]] + reverse_list(items[:-1])

def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))  # ← Recursive
        else:
            result.append(item)
    return result

nested = [1, [2, 3, [4, 5]], 6]
print(flatten(nested))  # [1, 2, 3, 4, 5, 6]
```

### 2.4. Tree Recursion

**File**: [`recursion.py`](recursion.py) - Line 185

```python
class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

def tree_sum(node):
    if node is None:
        return 0
    
    total = node.value
    for child in node.children:
        total += tree_sum(child)  # ← Recursive
    
    return total

def tree_height(node):
    if node is None:
        return 0
    if not node.children:
        return 1
    
    return 1 + max(tree_height(child) for child in node.children)
```

### 2.5. Binary Search (Recursive)

**File**: [`recursion.py`](recursion.py) - Line 259

```python
def binary_search(arr, target, left=0, right=-1):
    if right == -1:
        right = len(arr) - 1
    
    if left > right:
        return -1  # Not found
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    
    if arr[mid] > target:
        return binary_search(arr, target, left, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, right)
```

### 2.6. Recursion Depth Limit

**File**: [`recursion.py`](recursion.py) - Line 395

```python
import sys

print(sys.getrecursionlimit())  # Default: ~1000

# Increase limit (use with caution!)
# sys.setrecursionlimit(10000)

# Deep recursion will raise RecursionError
def deep(n):
    if n <= 0:
        return 0
    return 1 + deep(n - 1)

deep(10000)  # RecursionError!
```

### 💡 Recursion Best Practices

1. **Always have a base case** (or infinite recursion!)
2. **Make progress toward base case** in each call
3. **Consider iteration** for simple loops (more efficient)
4. **Use memoization** for overlapping subproblems
5. **Watch recursion depth** (Python limit ~1000)
6. **Tail recursion not optimized** in Python
7. **Best for**: trees, graphs, divide-and-conquer

---

## 3. Async Functions

**File**: [`async_and_partial.py`](async_and_partial.py)

### 3.1. Basic Async Function

**File**: [`async_and_partial.py`](async_and_partial.py) - Line 24

```python
import asyncio

async def simple_async():
    print("Starting")
    await asyncio.sleep(1)  # ← Non-blocking sleep
    print("Finished")
    return "Done!"

# Run async function
result = asyncio.run(simple_async())
```

### 🔑 Async Concepts

1. **`async def`**: Define async function (coroutine)
2. **`await`**: Pause until coroutine completes
3. **Coroutine**: Async function returns coroutine object
4. **Event loop**: Manages async execution
5. **Concurrent**: Multiple tasks, single thread
6. **Not parallel**: Still single-threaded

### 3.2. Concurrent Execution

**File**: [`async_and_partial.py`](async_and_partial.py) - Line 51

```python
async def fetch_data(url, delay=1.0):
    print(f"Fetching {url}...")
    await asyncio.sleep(delay)
    print(f"Fetched {url}")
    return {"url": url, "data": f"Data from {url}"}

async def fetch_multiple():
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/posts",
        "https://api.example.com/comments"
    ]
    
    # Create tasks
    tasks = [fetch_data(url) for url in urls]
    
    # Run concurrently
    results = await asyncio.gather(*tasks)
    
    return results

# Sequential: 3 seconds
# Concurrent: 1 second (3x faster!)
```

### 3.3. Async with Timeout

**File**: [`async_and_partial.py`](async_and_partial.py) - Line 73

```python
async def fetch_with_timeout(url, timeout=2.0):
    try:
        result = await asyncio.wait_for(
            fetch_data(url),
            timeout=timeout
        )
        return result
    except asyncio.TimeoutError:
        print(f"Timeout fetching {url}")
        raise
```

### 3.4. Async Generators

**File**: [`async_and_partial.py`](async_and_partial.py) - Line 95

```python
async def async_range(start, stop, delay=0.1):
    for i in range(start, stop):
        await asyncio.sleep(delay)
        yield i

async def process():
    async for value in async_range(1, 6):
        print(f"Received: {value}")
```

### 💡 Async Best Practices

1. **Use for I/O-bound operations** (network, file, database)
2. **Don't use for CPU-bound** (use multiprocessing instead)
3. **Always await coroutines** (or they won't run!)
4. **Use asyncio.gather()** for concurrent execution
5. **Add timeouts** to prevent hanging
6. **Handle exceptions** in async code
7. **Async is concurrent, not parallel**

---

## 4. Partial Application

**File**: [`async_and_partial.py`](async_and_partial.py)

### 4.1. Basic Partial

**File**: [`async_and_partial.py`](async_and_partial.py) - Line 119

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

# Create specialized functions
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125
```

### 🔑 Partial Concepts

1. **Pre-fill arguments**: Fix some arguments, leave others open
2. **Create specialized functions**: From general functions
3. **Works with positional and keyword args**
4. **Useful for callbacks and configuration**

### 4.2. Partial with Multiple Arguments

**File**: [`async_and_partial.py`](async_and_partial.py) - Line 135

```python
def greet(greeting, name, punctuation="!"):
    return f"{greeting}, {name}{punctuation}"

# Fix greeting
say_hello = partial(greet, "Hello")
say_goodbye = partial(greet, "Goodbye")

# Fix multiple arguments
formal_hello = partial(greet, "Hello", punctuation=".")

print(say_hello("Alice"))        # Hello, Alice!
print(say_goodbye("Bob"))        # Goodbye, Bob!
print(formal_hello("Dr. Smith")) # Hello, Dr. Smith.
```

### 4.3. Partial for Callbacks

**File**: [`async_and_partial.py`](async_and_partial.py) - Line 153

```python
def process_data(data, operation):
    return [operation(x) for x in data]

def multiply(x, factor):
    return x * factor

# Create specialized operations
double = partial(multiply, factor=2)
triple = partial(multiply, factor=3)

data = [1, 2, 3, 4, 5]
print(process_data(data, double))  # [2, 4, 6, 8, 10]
print(process_data(data, triple))  # [3, 6, 9, 12, 15]
```

### 💡 Partial Best Practices

1. **Use for configuration** (specialized versions)
2. **Use for callbacks** (pre-fill parameters)
3. **Improves readability** (clear intent)
4. **Works with methods** too
5. **Can fix positional or keyword args**
6. **Alternative to lambda** (more readable)

---

## 5. Memoization

**File**: [`memoization.py`](memoization.py)

### 5.1. The Problem: Slow Fibonacci

**File**: [`memoization.py`](memoization.py) - Line 24

```python
def fibonacci_slow(n):
    if n <= 1:
        return n
    return fibonacci_slow(n - 1) + fibonacci_slow(n - 2)

# Problem: Exponential time O(2^n)
# fibonacci_slow(30) takes ~0.3 seconds
# fibonacci_slow(40) takes ~30 seconds!
```

### 5.2. Solution 1: Manual Memoization

**File**: [`memoization.py`](memoization.py) - Line 40

```python
def fibonacci_manual_memo(n, memo=None):
    if memo is None:
        memo = {}

    # Check cache
    if n in memo:
        return memo[n]  # ← Cache hit!

    # Base cases
    if n <= 1:
        return n

    # Compute and cache
    result = fibonacci_manual_memo(n - 1, memo) + fibonacci_manual_memo(n - 2, memo)
    memo[n] = result  # ← Store in cache

    return result

# fibonacci_manual_memo(30) takes ~0.0001 seconds
# 3000x faster!
```

### 5.3. Solution 2: Decorator Memoization

**File**: [`memoization.py`](memoization.py) - Line 68

```python
def memoize(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]

        result = func(*args)
        cache[args] = result
        return result

    wrapper.cache = cache
    return wrapper

@memoize
def fibonacci_decorator(n):
    if n <= 1:
        return n
    return fibonacci_decorator(n - 1) + fibonacci_decorator(n - 2)
```

### 5.4. Solution 3: functools.lru_cache

**File**: [`memoization.py`](memoization.py) - Line 98

```python
from functools import lru_cache

@lru_cache(maxsize=128)  # ← LRU cache with max 128 entries
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# Check cache statistics
stats = fibonacci_lru.cache_info()
print(f"Hits: {stats.hits}, Misses: {stats.misses}")

# Clear cache
fibonacci_lru.cache_clear()
```

### 🔑 LRU Cache Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `maxsize=128` | Max cache entries (default) | `@lru_cache(maxsize=128)` |
| `maxsize=None` | Unlimited cache | `@lru_cache(maxsize=None)` |
| `maxsize=0` | No caching (for stats only) | `@lru_cache(maxsize=0)` |

### 5.5. Solution 4: functools.cache (Python 3.9+)

**File**: [`memoization.py`](memoization.py) - Line 125

```python
from functools import cache

@cache  # ← Simpler syntax, unlimited cache
def fibonacci_cache(n):
    if n <= 1:
        return n
    return fibonacci_cache(n - 1) + fibonacci_cache(n - 2)

# Equivalent to @lru_cache(maxsize=None)
```

### 5.6. Memoization with Multiple Arguments

**File**: [`memoization.py`](memoization.py) - Line 143

```python
@lru_cache(maxsize=256)
def binomial_coefficient(n, k):
    """Calculate C(n, k) = n! / (k! * (n-k)!)"""
    if k == 0 or k == n:
        return 1
    return binomial_coefficient(n - 1, k - 1) + binomial_coefficient(n - 1, k)

# Works with multiple arguments
print(binomial_coefficient(10, 5))  # 252
```

### 5.7. Cache Management

**File**: [`memoization.py`](memoization.py) - Line 165

```python
@lru_cache(maxsize=128)
def expensive_computation(x, y):
    time.sleep(0.01)
    return x ** y

# Get cache statistics
stats = expensive_computation.cache_info()
print(f"Hits: {stats.hits}")
print(f"Misses: {stats.misses}")
print(f"Size: {stats.currsize}")
print(f"Max size: {stats.maxsize}")

# Clear cache
expensive_computation.cache_clear()
```

### 5.8. Class-Based Memoization

**File**: [`memoization.py`](memoization.py) - Line 313

```python
class Memoized:
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]

        result = self.func(*args)
        self.cache[args] = result
        return result

    def clear_cache(self):
        self.cache.clear()

@Memoized
def fibonacci_class(n):
    if n <= 1:
        return n
    return fibonacci_class(n - 1) + fibonacci_class(n - 2)
```

### 💡 Memoization Best Practices

1. **Use for expensive computations** (slow functions)
2. **Use for pure functions** (same input → same output)
3. **Perfect for recursion** with overlapping subproblems
4. **Choose appropriate maxsize** (memory vs speed tradeoff)
5. **Only works with hashable arguments** (no lists/dicts)
6. **Monitor cache statistics** (cache_info())
7. **Clear cache when needed** (cache_clear())
8. **Massive speedup**: O(2^n) → O(n) for Fibonacci

### 📊 Performance Comparison

| Function | Time for fib(30) | Speedup |
|----------|------------------|---------|
| `fibonacci_slow` | ~0.3s | 1x |
| `fibonacci_manual_memo` | ~0.0001s | 3000x |
| `fibonacci_lru` | ~0.0001s | 3000x |
| `fibonacci_cache` | ~0.0001s | 3000x |

---

## 6. Summary

### 📋 Quick Reference

#### Recursion

```python
def factorial(n):
    if n <= 1:        # ← Base case
        return 1
    return n * factorial(n - 1)  # ← Recursive case
```

#### Async Functions

```python
import asyncio

async def fetch(url):
    await asyncio.sleep(1)  # ← Non-blocking
    return f"Data from {url}"

# Run concurrently
results = await asyncio.gather(
    fetch("url1"),
    fetch("url2"),
    fetch("url3")
)
```

#### Partial Application

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)
```

#### Memoization

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### 🎯 When to Use Each Technique

| Technique | Use When | Avoid When |
|-----------|----------|------------|
| **Recursion** | Trees, graphs, divide-and-conquer | Simple loops, deep recursion |
| **Async** | I/O-bound operations | CPU-bound operations |
| **Partial** | Callbacks, configuration | Simple cases (use lambda) |
| **Memoization** | Expensive pure functions | Impure functions, unhashable args |

### ✅ Self-Assessment Checklist

- [ ] Can write recursive functions with base and recursive cases
- [ ] Understand recursion depth limits and tail recursion
- [ ] Can use async/await for concurrent execution
- [ ] Understand difference between concurrent and parallel
- [ ] Can use asyncio.gather() for multiple tasks
- [ ] Can create partial functions with functools.partial
- [ ] Understand when to use partial vs lambda
- [ ] Can use @lru_cache for memoization
- [ ] Understand cache statistics and management
- [ ] Know when memoization provides benefits

### 🔗 Common Patterns

#### Pattern 1: Recursive Tree Traversal

```python
def tree_sum(node):
    if node is None:
        return 0
    total = node.value
    for child in node.children:
        total += tree_sum(child)
    return total
```

#### Pattern 2: Async API Calls

```python
async def fetch_all(urls):
    tasks = [fetch(url) for url in urls]
    return await asyncio.gather(*tasks)
```

#### Pattern 3: Partial for Configuration

```python
log_info = partial(log, level="INFO")
log_error = partial(log, level="ERROR")
```

#### Pattern 4: Memoized Recursion

```python
@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### 📁 Files in This Section

| File | Lines | Description |
|------|-------|-------------|
| [`recursion.py`](recursion.py) | 577 | Recursive functions, tree traversal, permutations |
| [`async_and_partial.py`](async_and_partial.py) | 415 | Async/await, concurrent execution, partial application |
| [`memoization.py`](memoization.py) | 445 | Caching, @lru_cache, @cache, performance optimization |
| **Total** | **1,437** | **3 Python examples** |

---

### 🎓 Key Takeaways

1. **Recursion**: Elegant for trees/graphs, but watch depth limit
2. **Base case is critical**: Missing base case = infinite recursion
3. **Async is concurrent, not parallel**: Single-threaded concurrency
4. **Use async for I/O-bound**: Network, file, database operations
5. **Partial creates specialized functions**: Pre-fill arguments
6. **Memoization = massive speedup**: O(2^n) → O(n) for recursion
7. **@lru_cache is built-in**: No need to write custom memoization
8. **Cache only pure functions**: Same input → same output
9. **Monitor cache statistics**: Use cache_info() to optimize
10. **Choose right tool for job**: Each technique has specific use cases

---

[← Back to Functions](../functions.md) | [Previous: Generators](../07_generators/)

**🎉 Congratulations!** You've completed all 8 topics in the Python Functions learning path!
