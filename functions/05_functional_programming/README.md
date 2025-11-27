# Python Functions - Functional Programming

[← Back to Functions](../functions.md) | [Previous: Advanced Features](../04_advanced_features/) | [Next: Decorators →](../06_decorators/)

> **Level**: 🔴 Advanced  
> **Estimated Time**: 3 hours  
> **Prerequisites**: [01. Basics](../01_basics/), [02. Parameters](../02_parameters/), [03. Scope](../03_scope/), [04. Advanced Features](../04_advanced_features/)

---

## 📚 Table of Contents

1. [Introduction](#1-introduction)
2. [Higher-Order Functions](#2-higher-order-functions)
3. [map(), filter(), and reduce()](#3-map-filter-and-reduce)
4. [Function Composition](#4-function-composition)
5. [Summary](#5-summary)

---

## 1. Introduction

**Functional programming** is a programming paradigm that treats computation as the evaluation of mathematical functions and avoids changing state and mutable data.

### 🎯 Core Principles

| Principle | Description | Benefit |
|-----------|-------------|---------|
| **Pure Functions** | No side effects, same input → same output | Predictable, testable |
| **Immutability** | Data doesn't change | Easier to reason about |
| **First-Class Functions** | Functions as values | Higher abstraction |
| **Function Composition** | Combine simple functions | Reusable components |

### 📦 What You'll Learn

- Higher-order functions (functions that take/return functions)
- Built-in functional tools (map, filter, reduce)
- Function composition and pipelines
- Functional programming patterns

---

## 2. Higher-Order Functions

**File**: [`higher_order_functions.py`](higher_order_functions.py)

### 2.1. What Are Higher-Order Functions?

A **higher-order function** is a function that:
1. Takes one or more functions as arguments, OR
2. Returns a function as result

### 🔑 Functions as First-Class Objects

In Python, functions are **first-class objects**:

```python
def greet(name):
    return f"Hello, {name}!"

# Assign to variable
say_hello = greet  # ← No parentheses!

# Store in data structure
functions = [greet, str.upper, str.lower]

# Pass as argument
def apply(func, value):
    return func(value)

apply(greet, "Alice")  # "Hello, Alice!"
```

### 2.2. Functions as Arguments

**File**: [`higher_order_functions.py`](higher_order_functions.py) - Line 56

```python
def apply_operation(
    x: int,
    y: int,
    operation: Callable[[int, int], int]
) -> int:
    return operation(x, y)  # ← Call the passed function

# Usage
apply_operation(10, 5, lambda x, y: x + y)      # 15
apply_operation(10, 5, lambda x, y: x * y)      # 50
apply_operation(10, 5, lambda x, y: x ** y)     # 100000
```

### 💡 Benefits

- **Flexibility**: Different behavior with same function
- **Abstraction**: Separate "what" from "how"
- **Reusability**: Generic functions work with many operations

### 2.3. Functions as Return Values

**File**: [`higher_order_functions.py`](higher_order_functions.py) - Line 91

```python
def make_multiplier(factor: int) -> Callable[[int], int]:
    def multiplier(x: int) -> int:
        return x * factor  # ← Closure captures 'factor'
    return multiplier  # ← Return function

times3 = make_multiplier(3)
times5 = make_multiplier(5)

times3(10)  # 30
times5(10)  # 50
```

### 🔑 Key Point

Each returned function is a **closure** that remembers its configuration.

### 2.4. Callback Functions

**File**: [`higher_order_functions.py`](higher_order_functions.py) - Line 141

```python
def process_list(
    items: List[int],
    callback: Callable[[int], None]
) -> None:
    for item in items:
        callback(item)  # ← Call callback for each item

# Usage
numbers = [1, 2, 3, 4, 5]
process_list(numbers, lambda x: print(f"Item: {x}"))
```

### 2.5. Common Higher-Order Patterns

**File**: [`higher_order_functions.py`](higher_order_functions.py) - Line 235

#### Pattern 1: Sorting with Key Functions

```python
people = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]

# Sort by age (second element)
by_age = sorted(people, key=lambda p: p[1])
# [('Bob', 25), ('Alice', 30), ('Charlie', 35)]
```

#### Pattern 2: Filtering with Predicates

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Filter even numbers
evens = [x for x in numbers if lambda x: x % 2 == 0]
# Or using filter()
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

#### Pattern 3: Transforming with Mappers

```python
numbers = [1, 2, 3, 4, 5]

# Square each number
squared = [x ** 2 for x in numbers]
# Or using map()
squared = list(map(lambda x: x ** 2, numbers))
```

### 2.6. Function Factories

**File**: [`higher_order_functions.py`](higher_order_functions.py) - Line 275

```python
def make_validator(min_value: int, max_value: int) -> Callable[[int], bool]:
    def validate(value: int) -> bool:
        return min_value <= value <= max_value
    return validate

is_valid_age = make_validator(0, 120)
is_valid_percentage = make_validator(0, 100)

is_valid_age(25)    # True
is_valid_age(150)   # False
```

### 💡 Higher-Order Function Best Practices

1. **Use type hints** for function parameters (`Callable[[Args], Return]`)
2. **Keep functions pure** when possible
3. **Name functions clearly** (describe what they do)
4. **Prefer built-ins** (sorted, filter, map) over custom implementations
5. **Document expected behavior** of function parameters

---

## 3. map(), filter(), and reduce()

**File**: [`map_filter_reduce.py`](map_filter_reduce.py)

Python provides three powerful built-in functional tools:

| Function | Purpose | Returns | Example |
|----------|---------|---------|---------|
| `map()` | Transform each element | Iterator | `map(lambda x: x*2, [1,2,3])` |
| `filter()` | Select elements | Iterator | `filter(lambda x: x>0, [-1,0,1])` |
| `reduce()` | Combine to single value | Single value | `reduce(lambda x,y: x+y, [1,2,3])` |

### 3.1. map() - Transform Each Element

**File**: [`map_filter_reduce.py`](map_filter_reduce.py) - Line 26

**Syntax**: `map(function, iterable, ...)`

```python
numbers = [1, 2, 3, 4, 5]

# Square each number
squared = map(lambda x: x ** 2, numbers)
list(squared)  # [1, 4, 9, 16, 25]

# Convert to strings
strings = map(str, numbers)
list(strings)  # ['1', '2', '3', '4', '5']

# Multiple iterables
a = [1, 2, 3]
b = [10, 20, 30]
sums = map(lambda x, y: x + y, a, b)
list(sums)  # [11, 22, 33]
```

### ⚠️ Important: Lazy Evaluation

`map()` returns an **iterator**, not a list:

```python
squared = map(lambda x: x ** 2, [1, 2, 3])
print(squared)  # <map object at 0x...>

# Convert to list to see results
print(list(squared))  # [1, 4, 9]

# Iterator is exhausted after first use!
print(list(squared))  # []
```

### 3.2. filter() - Select Elements

**File**: [`map_filter_reduce.py`](map_filter_reduce.py) - Line 89

**Syntax**: `filter(predicate, iterable)`

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Filter even numbers
evens = filter(lambda x: x % 2 == 0, numbers)
list(evens)  # [2, 4, 6, 8, 10]

# Filter numbers > 5
greater_than_5 = filter(lambda x: x > 5, numbers)
list(greater_than_5)  # [6, 7, 8, 9, 10]

# Filter with None (removes falsy values)
mixed = [0, 1, False, True, "", "hello", None, [], [1, 2]]
truthy = filter(None, mixed)
list(truthy)  # [1, True, 'hello', [1, 2]]
```

### 🔑 Special Case: filter(None, iterable)

Using `None` as the predicate removes all **falsy values**:
- `False`, `0`, `0.0`, `""`, `[]`, `{}`, `None`

### 3.3. reduce() - Combine Elements

**File**: [`map_filter_reduce.py`](map_filter_reduce.py) - Line 153

**Syntax**: `reduce(function, iterable[, initializer])`

**Note**: Must import from `functools`:

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum all numbers
total = reduce(lambda x, y: x + y, numbers)
# 15 (1+2=3, 3+3=6, 6+4=10, 10+5=15)

# Product of all numbers
product = reduce(lambda x, y: x * y, numbers)
# 120 (1*2=2, 2*3=6, 6*4=24, 24*5=120)

# With initial value
total_with_init = reduce(lambda x, y: x + y, numbers, 10)
# 25 (10+1=11, 11+2=13, 13+3=16, 16+4=20, 20+5=25)
```

### 🔑 How reduce() Works

```
reduce(f, [a, b, c, d])
= f(f(f(a, b), c), d)

With initial value:
reduce(f, [a, b, c], init)
= f(f(f(init, a), b), c)
```

### 3.4. map() vs List Comprehension

**File**: [`map_filter_reduce.py`](map_filter_reduce.py) - Line 73

```python
numbers = [1, 2, 3, 4, 5]

# Using map
squared_map = list(map(lambda x: x ** 2, numbers))

# Using list comprehension
squared_comp = [x ** 2 for x in numbers]

# Both produce same result
squared_map == squared_comp  # True
```

### 💡 When to Use Which?

| Use Case | Prefer |
|----------|--------|
| Simple transformation | List comprehension (more readable) |
| Existing function | `map(str, numbers)` |
| Multiple iterables | `map(add, list1, list2)` |
| Lazy evaluation needed | `map()` (returns iterator) |

### 3.5. filter() vs List Comprehension

**File**: [`map_filter_reduce.py`](map_filter_reduce.py) - Line 143

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Using filter
evens_filter = list(filter(lambda x: x % 2 == 0, numbers))

# Using list comprehension
evens_comp = [x for x in numbers if x % 2 == 0]

# Both produce same result
evens_filter == evens_comp  # True
```

### 💡 When to Use Which?

| Use Case | Prefer |
|----------|--------|
| Simple condition | List comprehension (more readable) |
| Existing predicate function | `filter(is_valid, items)` |
| Remove falsy values | `filter(None, items)` |
| Lazy evaluation needed | `filter()` (returns iterator) |

### 3.6. Combining map, filter, and reduce

**File**: [`map_filter_reduce.py`](map_filter_reduce.py) - Line 243

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Pipeline: filter evens -> square -> sum
result = reduce(
    lambda x, y: x + y,
    map(
        lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, numbers)
    )
)
# Steps: [2,4,6,8,10] -> [4,16,36,64,100] -> 220

# Same with comprehension (more readable)
result_comp = sum(x ** 2 for x in numbers if x % 2 == 0)
```

### 3.7. Practical Examples

**File**: [`map_filter_reduce.py`](map_filter_reduce.py) - Line 289

#### Example 1: Parse Strings to Integers

```python
string_numbers = ["1", "2", "3", "4", "5"]
integers = list(map(int, string_numbers))
# [1, 2, 3, 4, 5]
```

#### Example 2: Extract Dictionary Values

```python
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]
emails = list(map(lambda u: u["email"], users))
# ['alice@example.com', 'bob@example.com']
```

#### Example 3: Remove Empty Strings

```python
strings = ["hello", "", "world", "", "python"]
non_empty = list(filter(None, strings))
# ['hello', 'world', 'python']
```

#### Example 4: Merge Dictionaries

```python
dicts = [
    {"a": 1, "b": 2},
    {"b": 3, "c": 4},
    {"c": 5, "d": 6}
]
merged = reduce(lambda x, y: {**x, **y}, dicts)
# {'a': 1, 'b': 3, 'c': 5, 'd': 6}
```

### 💡 map/filter/reduce Best Practices

1. **Prefer list comprehensions** for simple cases (more Pythonic)
2. **Use map() with existing functions** (`map(str, numbers)`)
3. **Use filter(None, ...)** to remove falsy values
4. **Prefer built-ins over reduce()** (`sum()`, `max()`, `min()`)
5. **Remember lazy evaluation** (convert to list if needed)
6. **Don't forget to import reduce** (`from functools import reduce`)
7. **Consider readability** (comprehensions often clearer)

---

## 4. Function Composition

**File**: [`function_composition.py`](function_composition.py)

### 4.1. What Is Function Composition?

**Function composition** combines simple functions to create complex operations:

**Mathematical notation**: `(f ∘ g)(x) = f(g(x))`

```python
def compose(f, g):
    def composed(x):
        return f(g(x))  # ← Apply g first, then f
    return composed

# Example
add_10 = lambda x: x + 10
multiply_2 = lambda x: x * 2

# Compose: (x * 2) + 10
f = compose(add_10, multiply_2)
f(5)  # (5 * 2) + 10 = 20
```

### 🔑 Key Point

Composition applies functions **right to left**: `compose(f, g)` means "g first, then f"

### 4.2. Multiple Function Composition

**File**: [`function_composition.py`](function_composition.py) - Line 75

```python
def compose_many(*functions):
    def composed(x):
        return reduce(lambda acc, f: f(acc), reversed(functions), x)
    return composed

# Example
add_5 = lambda x: x + 5
multiply_3 = lambda x: x * 3
subtract_2 = lambda x: x - 2

# Compose: subtract_2(multiply_3(add_5(x)))
f = compose_many(subtract_2, multiply_3, add_5)
f(10)  # (10 + 5) * 3 - 2 = 43
```

### 4.3. Pipe (Left-to-Right Composition)

**File**: [`function_composition.py`](function_composition.py) - Line 89

```python
def pipe(*functions):
    def piped(x):
        return reduce(lambda acc, f: f(acc), functions, x)
    return piped

# Same functions, but left-to-right
piped = pipe(add_5, multiply_3, subtract_2)
piped(10)  # (10 + 5) * 3 - 2 = 43
```

### 💡 compose() vs pipe()

| Function | Order | Reads Like |
|----------|-------|------------|
| `compose(f, g, h)` | Right to left | Mathematical notation |
| `pipe(f, g, h)` | Left to right | Unix pipes, more intuitive |

**Recommendation**: Use `pipe()` for better readability in most cases.

### 4.4. Practical Composition Examples

**File**: [`function_composition.py`](function_composition.py) - Line 113

#### Example 1: String Processing Pipeline

```python
# Define operations
strip_whitespace = lambda s: s.strip()
to_lowercase = lambda s: s.lower()
remove_punctuation = lambda s: ''.join(c for c in s if c.isalnum() or c.isspace())
collapse_spaces = lambda s: ' '.join(s.split())

# Create pipeline
normalize = pipe(
    strip_whitespace,
    to_lowercase,
    remove_punctuation,
    collapse_spaces
)

text = "  Hello,  WORLD!!!  How are   you?  "
normalize(text)  # "hello world how are you"
```

#### Example 2: Data Transformation Pipeline

```python
data = [
    {"name": "Alice", "age": 30, "score": 85},
    {"name": "Bob", "age": 25, "score": 92},
    {"name": "Charlie", "age": 35, "score": 78},
    {"name": "David", "age": 28, "score": 88}
]

# Define transformations
filter_passing = lambda items: [i for i in items if i["score"] >= 80]
sort_by_score = lambda items: sorted(items, key=lambda x: x["score"], reverse=True)
extract_names = lambda items: [i["name"] for i in items]

# Create pipeline
process = pipe(
    filter_passing,
    sort_by_score,
    extract_names
)

process(data)  # ['Bob', 'David', 'Alice']
```

### 4.5. Point-Free Style

**File**: [`function_composition.py`](function_composition.py) - Line 192

**Point-free style** (tacit programming) defines functions without mentioning arguments:

```python
# Point-ful (explicit arguments)
def double_then_add_10_pointful(x):
    return x * 2 + 10

# Point-free (no explicit arguments)
double = lambda x: x * 2
add_10 = lambda x: x + 10
double_then_add_10_pointfree = compose(add_10, double)

# Both work the same
double_then_add_10_pointful(5)    # 20
double_then_add_10_pointfree(5)   # 20
```

### 💡 Benefits of Point-Free Style

- **Concise**: Less boilerplate
- **Composable**: Easy to combine
- **Declarative**: Focus on "what", not "how"

### ⚠️ Drawbacks

- **Less readable** for complex operations
- **Harder to debug** (no intermediate variables)
- **Can be cryptic** for beginners

### 4.6. Composition with Currying

**File**: [`function_composition.py`](function_composition.py) - Line 267

**Currying** transforms a multi-argument function into a chain of single-argument functions:

```python
def curry2(func):
    def curried(x):
        def inner(y):
            return func(x, y)
        return inner
    return curried

# Define binary operations
add = lambda x, y: x + y
multiply = lambda x, y: x * y

# Curry them
add_curried = curry2(add)
multiply_curried = curry2(multiply)

# Create specialized functions
add_10 = add_curried(10)
multiply_5 = multiply_curried(5)

# Compose
f = compose(multiply_5, add_10)
f(5)  # (5 + 10) * 5 = 75
```

### 💡 Function Composition Best Practices

1. **Use pipe() for readability** (left-to-right is more intuitive)
2. **Keep functions small** (single responsibility)
3. **Make functions pure** (no side effects)
4. **Name intermediate steps** for clarity
5. **Test components separately** before composing
6. **Document the pipeline** (what each step does)
7. **Consider comprehensions** for simple cases
8. **Use type hints** for safety

---

## 5. Summary

### 🎯 What You Learned

1. **Higher-Order Functions**
   - Functions as first-class objects
   - Functions as arguments (callbacks, predicates, key functions)
   - Functions as return values (factories, closures)
   - Common patterns (sorting, filtering, transforming)
   - Memoization and retry patterns

2. **map(), filter(), and reduce()**
   - `map()` transforms each element
   - `filter()` selects elements based on predicate
   - `reduce()` combines elements into single value
   - All support lazy evaluation (except reduce)
   - Comparison with list comprehensions
   - Practical use cases

3. **Function Composition**
   - Combining simple functions to build complex operations
   - `compose()` (right-to-left) vs `pipe()` (left-to-right)
   - Data processing pipelines
   - Point-free style
   - Composition with currying

### 📝 Quick Reference

#### Higher-Order Function Pattern
```python
def higher_order(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        # Do something before
        result = func(*args, **kwargs)
        # Do something after
        return result
    return wrapper
```

#### map/filter/reduce Pattern
```python
from functools import reduce

# Transform
mapped = map(lambda x: x * 2, items)

# Select
filtered = filter(lambda x: x > 0, items)

# Combine
reduced = reduce(lambda x, y: x + y, items)

# Pipeline
result = reduce(
    lambda x, y: x + y,
    map(lambda x: x * 2, filter(lambda x: x > 0, items))
)
```

#### Composition Pattern
```python
def pipe(*functions):
    def piped(x):
        return reduce(lambda acc, f: f(acc), functions, x)
    return piped

# Usage
process = pipe(
    step1,
    step2,
    step3
)
result = process(data)
```

### ✅ Checklist

Before moving to the next topic, make sure you can:

- [ ] Understand functions as first-class objects
- [ ] Write higher-order functions
- [ ] Pass functions as arguments
- [ ] Return functions from functions
- [ ] Use map() to transform data
- [ ] Use filter() to select data
- [ ] Use reduce() to combine data
- [ ] Understand lazy evaluation
- [ ] Compare map/filter with comprehensions
- [ ] Compose functions with compose()
- [ ] Create pipelines with pipe()
- [ ] Apply functional patterns to real problems
- [ ] Write point-free style code
- [ ] Combine composition with currying

### 🚀 Next Steps

Ready to learn more? Continue to:

- **[06. Decorators](../06_decorators/)** - Decorator patterns and applications
- **[07. Generators](../07_generators/)** - Generators and yield
- **[08. Advanced Topics](../08_advanced_topics/)** - Recursion, async, memoization

### 💡 Common Patterns

**Pattern 1: Data Processing Pipeline**
```python
result = pipe(
    lambda data: [x for x in data if x["active"]],
    lambda data: sorted(data, key=lambda x: x["score"], reverse=True),
    lambda data: [x["name"] for x in data[:10]]
)(users)
```

**Pattern 2: Function Factory**
```python
def make_validator(min_val, max_val):
    return lambda x: min_val <= x <= max_val

is_valid_age = make_validator(0, 120)
is_valid_percentage = make_validator(0, 100)
```

**Pattern 3: Memoization**
```python
def memoize(func):
    cache = {}
    def memoized(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return memoized

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

---

### 📁 Files in This Section

| File | Description | Lines |
|------|-------------|-------|
| [`higher_order_functions.py`](higher_order_functions.py) | Higher-order functions and patterns | 747 |
| [`map_filter_reduce.py`](map_filter_reduce.py) | Built-in functional tools | 601 |
| [`function_composition.py`](function_composition.py) | Function composition and pipelines | 581 |

**Total**: 3 files, 1,929 lines of code and documentation

---

[← Back to Functions](../functions.md) | [Previous: Advanced Features](../04_advanced_features/) | [Next: Decorators →](../06_decorators/)


