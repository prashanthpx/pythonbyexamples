# 07. Generators

[← Back to Functions](../functions.md) | [Previous: Decorators](../06_decorators/) | [Next: Advanced Topics →](../08_advanced_topics/)

## 📚 Table of Contents

1. [Introduction](#1-introduction)
2. [Basic Generators](#2-basic-generators)
3. [Generator Expressions](#3-generator-expressions)
4. [Advanced Patterns](#4-advanced-patterns)
5. [Summary](#5-summary)

---

## 1. Introduction

**Generators** are a powerful Python feature for creating iterators in a simple and memory-efficient way.

### What Are Generators?

A generator is a function that:
1. Uses `yield` instead of `return`
2. Produces values **lazily** (on-demand)
3. Maintains **state** between calls
4. Is **memory-efficient** for large sequences

### Generator vs Regular Function

| Feature | Regular Function | Generator |
|---------|-----------------|-----------|
| **Keyword** | `return` | `yield` |
| **Returns** | Once | Multiple times |
| **State** | Lost after return | Maintained between yields |
| **Memory** | O(n) for sequences | O(1) |
| **Evaluation** | Eager | Lazy |

### Why Use Generators?

| Benefit | Description |
|---------|-------------|
| **Memory Efficiency** | Don't store entire sequence in memory |
| **Lazy Evaluation** | Compute values only when needed |
| **Infinite Sequences** | Can represent infinite data |
| **Pipeline Processing** | Chain generators for data transformation |
| **Cleaner Code** | Simpler than implementing iterator protocol |

---

## 2. Basic Generators

**File**: [`basic_generators.py`](basic_generators.py)

### 2.1. Simple Generator Function

**File**: [`basic_generators.py`](basic_generators.py) - Line 24

```python
def simple_generator():
    print("Starting generator")
    yield 1  # ← Pause here, return 1
    print("Resuming after first yield")
    yield 2  # ← Pause here, return 2
    print("Resuming after second yield")
    yield 3  # ← Pause here, return 3
    print("Generator finished")

# Using the generator
gen = simple_generator()
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
# next(gen)  # StopIteration
```

### 🔑 Key Concepts

1. **`yield` pauses execution** and returns a value
2. **`next()` resumes execution** from where it paused
3. **`StopIteration` raised** when generator exhausted
4. **State is maintained** between yields

### 2.2. Generator for Range

**File**: [`basic_generators.py`](basic_generators.py) - Line 48

```python
def my_range(start, stop, step=1):
    current = start
    while current < stop:
        yield current  # ← Yield current value
        current += step  # ← Update state

for num in my_range(0, 10, 2):
    print(num)  # 0, 2, 4, 6, 8
```

### 2.3. Infinite Generators

**File**: [`basic_generators.py`](basic_generators.py) - Line 66

```python
def infinite_sequence():
    num = 0
    while True:  # ← Infinite loop
        yield num
        num += 1

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Use with take() to limit
def take(n, iterable):
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item

# First 10 Fibonacci numbers
for num in take(10, fibonacci()):
    print(num)
```

### 2.4. Memory Efficiency

**File**: [`basic_generators.py`](basic_generators.py) - Line 177

```python
# List: O(n) memory
def list_squares(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result  # Stores all values

# Generator: O(1) memory
def generator_squares(n):
    for i in range(n):
        yield i ** 2  # Yields one at a time

# Memory comparison
list_result = list_squares(1000)    # ~9KB
gen_result = generator_squares(1000)  # ~200 bytes
# 45x memory savings!
```

### 2.5. Generator Pipelines

**File**: [`basic_generators.py`](basic_generators.py) - Line 127

```python
def filter_even(numbers):
    for num in numbers:
        if num % 2 == 0:
            yield num

def square_numbers(numbers):
    for num in numbers:
        yield num ** 2

# Chain generators
numbers = my_range(1, 11)
evens = filter_even(numbers)
squares = square_numbers(evens)

for value in squares:
    print(value)  # 4, 16, 36, 64, 100
```

### 💡 Basic Generators Best Practices

1. **Use generators for large sequences** (memory efficiency)
2. **Use generators for infinite sequences** (can't use lists)
3. **Chain generators** for data pipelines
4. **Use `try/finally`** for cleanup
5. **Document what generator yields**
6. **Use type hints**: `Generator[YieldType, SendType, ReturnType]`

---

## 3. Generator Expressions

**File**: [`generator_expressions.py`](generator_expressions.py)

### 3.1. Generator Expression Syntax

**File**: [`generator_expressions.py`](generator_expressions.py) - Line 22

```python
# List comprehension (eager)
list_comp = [x ** 2 for x in range(10)]  # ← Creates list immediately

# Generator expression (lazy)
gen_expr = (x ** 2 for x in range(10))   # ← Creates generator

# Memory comparison
import sys
print(sys.getsizeof(list_comp))  # ~200 bytes
print(sys.getsizeof(gen_expr))   # ~200 bytes (for small n)

# For large n=10000:
# List: ~87KB
# Generator: ~200 bytes
# 435x memory savings!
```

### 🔑 Syntax Difference

```python
# List comprehension: [ ]
[expr for item in iterable if condition]

# Generator expression: ( )
(expr for item in iterable if condition)
```

### 3.2. Using in Functions

**File**: [`generator_expressions.py`](generator_expressions.py) - Line 45

```python
def sum_of_squares(n):
    # No extra parentheses needed
    return sum(x ** 2 for x in range(n))

def max_of_transformed(numbers):
    return max(x * 2 + 1 for x in numbers)

# Works with any function that accepts iterables
result = sum(x ** 2 for x in range(10))
result = max(x for x in range(10) if x % 2 == 0)
result = list(x * 2 for x in range(5))
```

### 3.3. Filtering

**File**: [`generator_expressions.py`](generator_expressions.py) - Line 63

```python
# Filter even squares
even_squares = (x ** 2 for x in range(10) if x % 2 == 0)

# Filter and transform strings
uppercase = (s.upper() for s in strings if s)

# Multiple conditions
filtered = (x for x in range(100) if x % 2 == 0 if x % 3 == 0)
```

### 3.4. Nested Generator Expressions

**File**: [`generator_expressions.py`](generator_expressions.py) - Line 83

```python
# Flatten 2D matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = (item for row in matrix for item in row)
# Result: 1, 2, 3, 4, 5, 6, 7, 8, 9

# Cartesian product
pairs = ((a, b) for a in [1, 2, 3] for b in ['x', 'y'])
# Result: (1,'x'), (1,'y'), (2,'x'), (2,'y'), (3,'x'), (3,'y')
```

### 3.5. Iterator Protocol

**File**: [`generator_expressions.py`](generator_expressions.py) - Line 107

```python
class CountDown:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self  # ← Return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration  # ← Signal end
        value = self.current
        self.current -= 1
        return value

# Use like any iterator
for num in CountDown(5):
    print(num)  # 5, 4, 3, 2, 1
```

### 💡 Generator Expressions Best Practices

1. **Use for simple transformations** (complex logic → generator function)
2. **Pass directly to functions** (sum, max, min, etc.)
3. **Prefer over list comprehensions** for large data
4. **Use for one-time iteration** (can't reuse)
5. **Chain for pipelines** (readable data transformations)

---

## 4. Advanced Patterns

**File**: [`advanced_patterns.py`](advanced_patterns.py)

### 4.1. yield from

**File**: [`advanced_patterns.py`](advanced_patterns.py) - Line 22

```python
def chain(*iterables):
    for iterable in iterables:
        yield from iterable  # ← Delegate to sub-generator

# Usage
for value in chain([1, 2], [3, 4], [5, 6]):
    print(value)  # 1, 2, 3, 4, 5, 6

# Recursive flattening
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)  # ← Recursive
        else:
            yield item

nested = [1, [2, 3, [4, 5]], 6]
print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6]
```

### 🔑 yield from Benefits

1. **Cleaner code**: No manual loop
2. **Delegation**: Sub-generator handles iteration
3. **Recursion**: Natural for recursive structures
4. **Performance**: Slightly faster than manual loop

### 4.2. Generator with send()

**File**: [`advanced_patterns.py`](advanced_patterns.py) - Line 73

```python
def running_average():
    total = 0.0
    count = 0

    while True:
        value = yield (total / count if count > 0 else 0.0)
        if value is not None:
            total += value
            count += 1

# Usage
avg = running_average()
next(avg)  # Prime the generator

print(avg.send(10))  # 10.0
print(avg.send(20))  # 15.0
print(avg.send(30))  # 20.0
```

### 🔑 send() Pattern

```python
value = yield result
# 1. Yield 'result' to caller
# 2. Pause and wait
# 3. Resume when send(value) called
# 4. Receive 'value' from caller
```

### 4.3. Generator with throw() and close()

**File**: [`advanced_patterns.py`](advanced_patterns.py) - Line 103

```python
def resilient_generator():
    num = 0
    while True:
        try:
            yield num
            num += 1
        except ValueError as e:
            print(f"Caught: {e}")
            num = 0  # Reset
        except GeneratorExit:
            print("Closing...")
            raise  # Re-raise for cleanup

gen = resilient_generator()
next(gen)  # 0
next(gen)  # 1

gen.throw(ValueError, "Reset!")  # Caught: Reset!
next(gen)  # 0

gen.close()  # Closing...
```

### 4.4. Generator Pipelines

**File**: [`advanced_patterns.py`](advanced_patterns.py) - Line 127

```python
def numbers(start, stop):
    for num in range(start, stop):
        yield num

def filter_even(numbers):
    for num in numbers:
        if num % 2 == 0:
            yield num

def square(numbers):
    for num in numbers:
        yield num ** 2

# Build pipeline
pipeline = square(filter_even(numbers(1, 11)))

for value in pipeline:
    print(value)  # 4, 16, 36, 64, 100
```

### 4.5. Recursive Generators

**File**: [`advanced_patterns.py`](advanced_patterns.py) - Line 172

```python
def tree_traverse(node):
    yield node['value']

    if 'children' in node:
        for child in node['children']:
            yield from tree_traverse(child)

tree = {
    'value': 1,
    'children': [
        {'value': 2, 'children': [{'value': 4}, {'value': 5}]},
        {'value': 3}
    ]
}

print(list(tree_traverse(tree)))  # [1, 2, 4, 5, 3]
```

### 4.6. itertools Utilities

**File**: [`advanced_patterns.py`](advanced_patterns.py) - Line 237

```python
import itertools

# tee: Split generator into multiple iterators
gen = (x ** 2 for x in range(10))
gen1, gen2 = itertools.tee(gen, 2)

# islice: Slice infinite generators
def infinite():
    num = 0
    while True:
        yield num
        num += 1

# Get items 10-20
for value in itertools.islice(infinite(), 10, 20):
    print(value)

# chain: Chain iterables
for value in itertools.chain([1, 2], [3, 4], [5, 6]):
    print(value)
```

### 💡 Advanced Patterns Best Practices

1. **Use `yield from`** for delegation and recursion
2. **Use `send()`** for coroutines (two-way communication)
3. **Use `throw()`** for error handling
4. **Use `close()`** for cleanup
5. **Build pipelines** for data processing
6. **Use `itertools`** for common patterns
7. **Document generator behavior** clearly

---

## 5. Summary

### 🎯 What You Learned

1. **Basic Generators**
   - Generators use `yield` instead of `return`
   - Lazy evaluation: values computed on-demand
   - Memory-efficient: O(1) vs O(n)
   - State maintained between yields
   - Can be infinite (while True)
   - Use `next()` to get next value
   - `StopIteration` raised when exhausted

2. **Generator Expressions**
   - Syntax: `(expr for item in iterable if condition)`
   - Similar to list comprehensions but lazy
   - Much more memory-efficient
   - Can be used directly in functions
   - Iterator protocol: `__iter__()` and `__next__()`
   - Iterable vs Iterator distinction

3. **Advanced Patterns**
   - `yield from`: delegate to sub-generator
   - `send()`: send values into generator
   - `throw()`: raise exception in generator
   - `close()`: stop generator and cleanup
   - Generator pipelines for data processing
   - Recursive generators with `yield from`
   - `itertools` utilities (tee, islice, chain)

### 📝 Quick Reference

#### Basic Generator
```python
def my_generator():
    yield 1
    yield 2
    yield 3

for value in my_generator():
    print(value)
```

#### Generator Expression
```python
# List comprehension
squares = [x ** 2 for x in range(10)]

# Generator expression
squares = (x ** 2 for x in range(10))
```

#### yield from
```python
def chain(*iterables):
    for iterable in iterables:
        yield from iterable
```

#### Generator with send()
```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value

acc = accumulator()
next(acc)  # Prime
acc.send(10)  # 10
acc.send(20)  # 30
```

#### Generator Pipeline
```python
pipeline = transform(filter_func(source()))
for value in pipeline:
    process(value)
```

### ✅ Checklist

Before moving to the next topic, make sure you can:

- [ ] Write basic generator functions with `yield`
- [ ] Understand lazy evaluation
- [ ] Use `next()` to manually iterate
- [ ] Handle `StopIteration` exception
- [ ] Create infinite generators
- [ ] Write generator expressions
- [ ] Understand memory benefits
- [ ] Implement iterator protocol (`__iter__`, `__next__`)
- [ ] Use `yield from` for delegation
- [ ] Use `send()` for two-way communication
- [ ] Use `throw()` and `close()` for control
- [ ] Build generator pipelines
- [ ] Use `itertools` utilities
- [ ] Write recursive generators

### 🚀 Next Steps

Ready to learn more? Continue to:

- **[08. Advanced Topics](../08_advanced_topics/)** - Recursion, async functions, memoization

### 💡 Common Patterns

**Pattern 1: Infinite Sequence**
```python
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1
```

**Pattern 2: File Processing**
```python
def read_large_file(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()
```

**Pattern 3: Pipeline**
```python
def pipeline(data):
    filtered = (x for x in data if x > 0)
    squared = (x ** 2 for x in filtered)
    return squared
```

**Pattern 4: Recursive Traversal**
```python
def traverse(node):
    yield node.value
    for child in node.children:
        yield from traverse(child)
```

**Pattern 5: Stateful Generator**
```python
def running_sum():
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value
```

---

### 📁 Files in This Section

| File | Description | Lines |
|------|-------------|-------|
| [`basic_generators.py`](basic_generators.py) | Basic generators, yield, infinite sequences | 445 |
| [`generator_expressions.py`](generator_expressions.py) | Generator expressions, iterator protocol | 487 |
| [`advanced_patterns.py`](advanced_patterns.py) | yield from, send(), pipelines, recursion | 466 |

**Total**: 3 files, 1,398 lines of code and documentation

---

[← Back to Functions](../functions.md) | [Previous: Decorators](../06_decorators/) | [Next: Advanced Topics →](../08_advanced_topics/)
