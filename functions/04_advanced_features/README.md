# Python Functions - Advanced Features

[← Back to Functions](../functions.md) | [Previous: Scope](../03_scope/) | [Next: Functional Programming →](../05_functional_programming/)

> **Level**: 🔴 Advanced  
> **Estimated Time**: 3 hours  
> **Prerequisites**: [01. Basics](../01_basics/), [02. Parameters](../02_parameters/), [03. Scope](../03_scope/)

---

## 📚 Table of Contents

1. [Introduction](#1-introduction)
2. [Lambda Functions](#2-lambda-functions)
3. [Closures](#3-closures)
4. [Type Hints](#4-type-hints)
5. [List and Optional Basics](#5-list-and-optional-basics)
6. [Summary](#6-summary)

---

## 1. Introduction

This section covers advanced function features in Python:

| Feature | Description | Use Cases |
|---------|-------------|-----------|
| **Lambda** | Anonymous functions | map/filter/sorted, callbacks |
| **Closures** | Functions with memory | Data hiding, factories, decorators |
| **Type Hints** | Static type annotations | Documentation, IDE support, mypy |

These features enable more expressive, maintainable, and type-safe code.

---

## 2. Lambda Functions

**File**: [`lambda_functions.py`](lambda_functions.py)

### 2.1. What Are Lambda Functions?

**Lambda functions** are small, anonymous functions defined with the `lambda` keyword:

```python
# Regular function
def square(x):
    return x ** 2

# ← Equivalent lambda
square = lambda x: x ** 2
```

**Syntax**: `lambda arguments: expression`

### 🔑 Key Characteristics

1. **Single expression only** (no statements)
2. **Implicit return** (no `return` keyword)
3. **Can have multiple arguments**
4. **Anonymous** (no name required)
5. **Limited** compared to regular functions

### 2.2. Basic Lambda Examples

**File**: [`lambda_functions.py`](lambda_functions.py) - Line 24

```python
# Simple lambda
add_10 = lambda x: x + 10

# Multiple arguments
multiply = lambda x, y: x * y

# No arguments
get_constant = lambda: 42

# Results
add_10(5)        # 15
multiply(3, 4)   # 12
get_constant()   # 42
```

### 2.3. Lambda with Built-in Functions

**File**: [`lambda_functions.py`](lambda_functions.py) - Line 67

#### map()

```python
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
# [1, 4, 9, 16, 25]
```

#### filter()

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
# [2, 4, 6, 8, 10]
```

#### sorted()

```python
people = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]

# Sort by age (second element)
by_age = sorted(people, key=lambda person: person[1])
# [('Bob', 25), ('Alice', 30), ('Charlie', 35)]
```

#### reduce()

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)
# 1 * 2 * 3 * 4 * 5 = 120
```

### 2.4. Lambda Limitations

**File**: [`lambda_functions.py`](lambda_functions.py) - Line 139

```python
# ✅ Single expression
simple = lambda x: x * 2

# ✅ Conditional expression (ternary)
absolute = lambda x: x if x > 0 else -x

# ❌ Cannot use statements
# bad = lambda x: if x > 0: return x  # SyntaxError

# ❌ Cannot have multiple statements
# bad = lambda x: y = x * 2; return y  # SyntaxError

# ✅ Use regular function for complex logic
def complex_function(x):
    if x > 0:
        result = x * 2
    else:
        result = x * -2
    return result
```

### ⚠️ When NOT to Use Lambda

- Complex logic requiring multiple statements
- Need for documentation (docstrings)
- Debugging (lambdas have no name)
- Readability concerns

### 2.5. Lambda in Data Structures

**File**: [`lambda_functions.py`](lambda_functions.py) - Line 177

```python
# Dictionary of operations
operations = {
    "add": lambda x, y: x + y,
    "subtract": lambda x, y: x - y,
    "multiply": lambda x, y: x * y,
    "divide": lambda x, y: x / y if y != 0 else 0
}

operations["add"](10, 5)       # 15
operations["multiply"](10, 5)  # 50
```

### 2.6. Lambda Closure Pitfall

**File**: [`lambda_functions.py`](lambda_functions.py) - Line 241

```python
# ❌ WRONG: All lambdas capture same 'i'
functions_wrong = []
for i in range(5):
    functions_wrong.append(lambda x: x + i)

# All use i=4 (final value)
[func(10) for func in functions_wrong]  # [14, 14, 14, 14, 14]

# ✅ CORRECT: Use default argument
functions_correct = []
for i in range(5):
    functions_correct.append(lambda x, i=i: x + i)

[func(10) for func in functions_correct]  # [10, 11, 12, 13, 14]
```

### 💡 Lambda Best Practices

1. **Use for simple operations** (one-liners)
2. **Prefer with map/filter/sorted**
3. **Use regular functions for complex logic**
4. **Capture loop variables with default args**
5. **Consider readability** (named functions are clearer)

---

## 3. Closures

**File**: [`closures.py`](closures.py)

### 3.1. What Are Closures?

A **closure** is a function that:
1. Is defined inside another function (nested)
2. References variables from the enclosing scope
3. Is returned or passed around
4. "Remembers" the enclosing scope

```python
def make_multiplier(n):
    # ← 'n' is in enclosing scope
    
    def multiply(x):
        return x * n  # ← Captures 'n'
    
    return multiply  # ← Returns closure

times3 = make_multiplier(3)
times3(10)  # 30 (remembers n=3)
```

### 3.2. Basic Closure Examples

**File**: [`closures.py`](closures.py) - Line 24

```python
def simple_closure():
    message = "Hello from closure"  # ← Enclosing scope
    
    def inner():
        return message  # ← Captures 'message'
    
    return inner

closure = simple_closure()
closure()  # "Hello from closure"
```

### 3.3. Closures with State

**File**: [`closures.py`](closures.py) - Line 56

```python
def closure_with_state():
    count = 0  # ← Private state
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter

counter = closure_with_state()
counter()  # 1
counter()  # 2
counter()  # 3 (maintains state!)
```

### 🔑 Key Point

Each closure has its **own independent state**:

```python
counter1 = closure_with_state()
counter2 = closure_with_state()

counter1()  # 1
counter1()  # 2
counter2()  # 1 (independent!)
```

### 3.4. Closure Factories

**File**: [`closures.py`](closures.py) - Line 75

Factory functions create closures with different configurations:

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor  # ← Captures 'factor'
    return multiply

times2 = make_multiplier(2)
times5 = make_multiplier(5)

times2(10)  # 20
times5(10)  # 50
```

### 3.5. Closures for Encapsulation

**File**: [`closures.py`](closures.py) - Line 133

Closures provide **data hiding** (private state):

```python
def create_bank_account(initial_balance=0.0):
    # ← Private state (cannot access directly)
    balance = initial_balance
    transaction_history = []

    def deposit(amount):
        nonlocal balance
        if amount > 0:
            balance += amount
            transaction_history.append(f"Deposit: +${amount:.2f}")
        return balance

    def withdraw(amount):
        nonlocal balance
        if 0 < amount <= balance:
            balance -= amount
            transaction_history.append(f"Withdraw: -${amount:.2f}")
        return balance

    def get_balance():
        return balance

    def get_history():
        return transaction_history.copy()

    # ← Return interface to private state
    return deposit, withdraw, get_balance, get_history

# Usage
deposit, withdraw, balance, history = create_bank_account(100.0)
deposit(50.0)   # 150.0
withdraw(30.0)  # 120.0
balance()       # 120.0
# Cannot access 'balance' variable directly!
```

### 💡 Benefits

- **Encapsulation**: Hide implementation details
- **Data privacy**: No direct access to internal state
- **Clean interface**: Only expose necessary functions

### 3.6. Shared Enclosing Scope

**File**: [`closures.py`](closures.py) - Line 113

Multiple closures can share the same enclosing scope:

```python
def make_counter(start=0, step=1):
    count = start  # ← Shared state

    def increment():
        nonlocal count
        count += step
        return count

    def decrement():
        nonlocal count
        count -= step
        return count

    def reset():
        nonlocal count
        count = start

    # ← All three share same 'count'
    return increment, decrement, reset

inc, dec, reset = make_counter(0, 5)
inc()    # 5
inc()    # 10
dec()    # 5
reset()  # Back to 0
```

### 3.7. Closure Loop Pitfall

**File**: [`closures.py`](closures.py) - Line 261

**Common mistake** when creating closures in loops:

```python
# ❌ WRONG: All closures capture same 'i'
functions = []
for i in range(5):
    def func():
        return i  # ← Captures 'i' by reference!
    functions.append(func)

# All return 4 (final value)
[f() for f in functions]  # [4, 4, 4, 4, 4]

# ✅ CORRECT: Use default argument
functions = []
for i in range(5):
    def func(i=i):  # ← Captures current value
        return i
    functions.append(func)

[f() for f in functions]  # [0, 1, 2, 3, 4]
```

### ⚠️ Why This Happens

- Closures capture variables **by reference**, not by value
- Loop variable `i` is shared across all iterations
- All closures see the **final value** of `i`

### ✅ Solution

Use **default argument** to capture the current value:
- `def func(i=i):` captures the value at definition time
- Each closure gets its own copy of the value

### 3.8. Practical Closure Patterns

**File**: [`closures.py`](closures.py) - Line 305

#### Pattern 1: Logger with Prefix

```python
def make_logger(prefix):
    def log(message):
        print(f"[{prefix}] {message}")
    return log

error_log = make_logger("ERROR")
info_log = make_logger("INFO")

error_log("Something went wrong")  # [ERROR] Something went wrong
info_log("Application started")    # [INFO] Application started
```

#### Pattern 2: Memoization

```python
def make_memoizer():
    cache = {}  # ← Private cache

    def fibonacci(n):
        if n in cache:
            return cache[n]

        if n <= 1:
            result = n
        else:
            result = fibonacci(n - 1) + fibonacci(n - 2)

        cache[n] = result
        return result

    def get_cache():
        return cache.copy()

    return fibonacci, get_cache

fib, cache = make_memoizer()
fib(10)  # 55
len(cache())  # 11 (cached values)
```

#### Pattern 3: Accumulator

```python
def make_accumulator(initial=0):
    total = initial

    def accumulate(value):
        nonlocal total
        total += value
        return total

    return accumulate

acc = make_accumulator(0)
acc(5)   # 5
acc(10)  # 15
acc(3)   # 18
```

### 3.9. Closure Inspection

**File**: [`closures.py`](closures.py) - Line 383

Python provides attributes to inspect closures:

```python
def outer():
    x = 10
    y = 20

    def closure():
        return x + y

    return closure

func = outer()

# Closure attributes
func.__name__              # 'closure'
func.__closure__           # Tuple of cells
func.__code__.co_freevars  # ('x', 'y')

# Get captured values
[cell.cell_contents for cell in func.__closure__]  # [10, 20]
```

### 💡 Closure Best Practices

1. **Use for data hiding** and encapsulation
2. **Factory functions** for creating configured closures
3. **Avoid complex nested structures** (hard to debug)
4. **Be aware of loop variable pitfall**
5. **Use default args** to capture loop variables
6. **Document closure behavior** clearly

---

## 4. Type Hints

**File**: [`type_hints.py`](type_hints.py)

### 4.1. What Are Type Hints?

**Type hints** (PEP 484) provide static type annotations:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

### 🎯 Benefits

1. **Better documentation** - Self-documenting code
2. **IDE support** - Autocomplete and error detection
3. **Static type checking** - Catch errors before runtime (mypy)
4. **Improved maintainability** - Easier to understand code

### ⚠️ Important

Type hints are **optional** and **not enforced at runtime**. Use tools like `mypy` for static type checking.

### 4.2. Basic Type Hints

**File**: [`type_hints.py`](type_hints.py) - Line 35

```python
def basic_types(
    name: str,
    age: int,
    height: float,
    is_student: bool
) -> str:
    return f"{name}, {age} years, {height}m, student={is_student}"

def none_return(message: str) -> None:
    print(message)
    # ← Returns None
```

### 4.3. Container Type Hints

**File**: [`type_hints.py`](type_hints.py) - Line 65

```python
def list_types(numbers: list[int]) -> list[int]:
    return [n ** 2 for n in numbers]

def dict_types(data: dict[str, int]) -> dict[str, int]:
    return {k: v for k, v in data.items() if v > 0}

def tuple_types(point: tuple[float, float, float]) -> float:
    x, y, z = point
    return (x**2 + y**2 + z**2) ** 0.5

def set_types(items: set[str]) -> set[str]:
    return {item.upper() for item in items}
```

### 4.4. Optional and Union Types

**File**: [`type_hints.py`](type_hints.py) - Line 115

```python
from typing import Optional, Union

# Optional[T] = T or None
def optional_parameter(name: str, age: Optional[int] = None) -> str:
    if age is None:
        return f"{name} (age unknown)"
    return f"{name}, {age} years"

# Union[A, B] = A or B
def union_types(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return f"Number: {value}"
    return f"String: {value}"

# Optional return
def optional_return(value: int) -> Optional[str]:
    if value > 0:
        return str(value)
    return None
```

### 📋 Type Hint Summary

| Type Hint | Meaning | Example |
|-----------|---------|---------|
| `int`, `str`, `float`, `bool` | Basic types | `age: int` |
| `list[T]` | List of T | `numbers: list[int]` |
| `dict[K, V]` | Dict with keys K, values V | `data: dict[str, int]` |
| `tuple[T, ...]` | Tuple of types | `point: tuple[float, float]` |
| `set[T]` | Set of T | `items: set[str]` |
| `Optional[T]` | T or None | `age: Optional[int]` |
| `Union[A, B]` | A or B | `value: Union[int, str]` |
| `None` | No return value | `-> None` |

### 4.5. Callable Type Hints

**File**: [`type_hints.py`](type_hints.py) - Line 149

```python
from typing import Callable

# Function that takes a function
def apply_function(func: Callable[[int], int], value: int) -> int:
    return func(value)

# Function that returns a function
def make_adder(n: int) -> Callable[[int], int]:
    def add(x: int) -> int:
        return x + n
    return add

# Callback
def callback_example(
    data: list[int],
    callback: Callable[[int], None]
) -> None:
    for item in data:
        callback(item)
```

**Syntax**: `Callable[[ArgTypes], ReturnType]`

- `Callable[[int], int]` - Function taking int, returning int
- `Callable[[int, str], bool]` - Function taking int and str, returning bool
- `Callable[[], None]` - Function with no args, returning None

If you come from Go, the mapping is:

- Go: `f func(int) int`
- Python: `f: Callable[[int], int]`

and in general:

- `Callable[[A, B], R]`  Gos `func(A, B) R`

#### 4.5.1 Callable + ParamSpec for flexible helpers

Sometimes you want helpers that accept *any* function and forward whatever
arguments it expects. For this we use `ParamSpec`.

**File**: [`param_spec_examples.py`](param_spec_examples.py)  `call_twice`

```python
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def call_twice(
    f: Callable[P, R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> tuple[R, R]:
    return f(*args, **kwargs), f(*args, **kwargs)
```

Key ideas:

- `Callable[P, R]`  a function that takes some parameters `P` and returns `R`.
- `P = ParamSpec("P")`  a *type-level* parameter list that can be reused.
- `*args: P.args, **kwargs: P.kwargs`  this helper accepts **whatever
  positional and keyword arguments** `f` needs and forwards them with
  `f(*args, **kwargs)`.
- `R = TypeVar("R")`  captures the return type so the result is a `tuple[R, R]`.

Usage:

```python
from param_spec_examples import call_twice, greet

print(call_twice(greet, "Prashanth", punctuation="!"))  # two greetings
```

#### 4.5.2 Timeout-based wait_until and argument binding

**File**: [`param_spec_examples.py`](param_spec_examples.py)  `wait_until`

```python
from typing import Callable, ParamSpec

P2 = ParamSpec("P2")

def wait_until(
    condition: Callable[P2, bool],
    timeout_sec: float,
    *args: P2.args,
    **kwargs: P2.kwargs,
) -> None:
    ...
```

Call:

```python
from param_spec_examples import wait_until, is_even_after_increment

wait_until(is_even_after_increment, 5, 3, increments=1)
```

Argument binding step-by-step for this call:

- `condition = is_even_after_increment`
- `timeout_sec = 5`
- `args = (3,)`
- `kwargs = {"increments": 1}`

Inside the helper we only call `condition(*args, **kwargs)`, which becomes:

- `is_even_after_increment(3, increments=1)`

Even though the outer call has three values after the function (`5, 3, increments=1`),
only two of them (`3` and `increments=1`) are forwarded into the condition; `5`
is consumed by the wrappers own `timeout_sec` parameter.

This is why helpers like `wait_until` are written very carefully to call:

```python
condition(*args, **kwargs)
```

and **not** something like:

```python
condition(timeout_sec, *args, **kwargs)
```

which would force the condition to accept a spurious extra parameter.

Your mental model `math(double, 10)` (pass a function plus its arguments into a
generic helper) is exactly what is happening here.

#### 4.5.3 Wrapper using Any vs using ParamSpec P

A common pattern in real code is to use a strongly-typed core helper and a
thinner, more flexible wrapper.

**File**: [`param_spec_examples.py`](param_spec_examples.py)  `Service`

```python
from typing import Any, Callable, ParamSpec

P3 = ParamSpec("P3")

class Service:
    def wait_until_running(
        self,
        *args: Any,
        timeout_sec: float | None = None,
        **kwargs: Any,
    ) -> None:
        return self._wait_until(
            self.is_running,
            "start",
            timeout_sec,
            *args,
            **kwargs,
        )

    def _wait_until(
        self,
        condition: Callable[P3, bool],
        action: str,
        timeout_sec: float | None = None,
        *args: P3.args,
        **kwargs: P3.kwargs,
    ) -> None:
        ...
```

- `_wait_until` uses `Callable[P3, bool]` and `*args: P3.args, **kwargs: P3.kwargs`
  to keep the **relationship** between `condition` and its arguments precise.
- `wait_until_running` is just a **public wrapper** that forwards whatever
  arguments the caller gives; using `Any` here keeps the method signature
  simpler and avoids some edge-cases with generic methods on classes.
- You *could* make `wait_until_running` generic over the same `P3`, but many
  codebases choose the pragmatic approach: **strict typing in the core helper,
  simpler `Any` in the thin wrapper**.

#### 4.5.4 What ParamSpec P really represents

- `P = ParamSpec("P")` is a **type-level description of the parameter list**
  of the target function (e.g. `condition`, `f`).
- `Callable[P, bool]` says a function taking parameters `P` and returning
  `bool`.
- `*args: P.args, **kwargs: P.kwargs` says this helper also accepts those
  same parameters and forwards them to that function.

At runtime, `P` does **nothing**  it exists purely for static type checkers
(`mypy`, `pyright`, IDEs). The caller of `call_twice` or `wait_until` never
“sees” or passes `P`; it is only there so tools can verify that the arguments
you pass match what the target function expects.

### 4.6. Generic Types (TypeVar)

**File**: [`type_hints.py`](type_hints.py) - Line 215

```python
from typing import TypeVar

T = TypeVar('T')  # ← Generic type variable

def first_element(items: list[T]) -> Optional[T]:
    return items[0] if items else None

def reverse_list(items: list[T]) -> list[T]:
    return items[::-1]

# Usage
first_element([1, 2, 3])      # Returns int
first_element(['a', 'b'])     # Returns str
reverse_list([1, 2, 3])       # Returns list[int]
reverse_list(['a', 'b', 'c']) # Returns list[str]
```

**TypeVar** preserves the type through the function:
- Input `list[int]` → Output `int` or `list[int]`
- Input `list[str]` → Output `str` or `list[str]`

### 4.7. Generic Classes

**File**: [`type_hints.py`](type_hints.py) - Line 253

```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> Optional[T]:
        return self._items.pop() if self._items else None

# Usage
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)

str_stack: Stack[str] = Stack()
str_stack.push("hello")
str_stack.push("world")
```

### 4.8. Protocol (Structural Typing)

**File**: [`type_hints.py`](type_hints.py) - Line 283

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str:
        ...

class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def draw(self) -> str:
        return f"Circle(radius={self.radius})"

class Square:
    def __init__(self, side: float) -> None:
        self.side = side

    def draw(self) -> str:
        return f"Square(side={self.side})"

def render(obj: Drawable) -> str:
    return obj.draw()  # ← Works with any object with draw()

# Usage
render(Circle(5.0))  # ✅ Works
render(Square(10.0)) # ✅ Works
```

**Protocol** enables **structural typing** (duck typing with type hints):
- No inheritance required
- Any class with matching methods works
- More flexible than nominal typing

### 4.9. Literal Types

**File**: [`type_hints.py`](type_hints.py) - Line 329

```python
from typing import Literal

def set_mode(mode: Literal["read", "write", "append"]) -> str:
    return f"Mode: {mode}"

# Usage
set_mode("read")    # ✅ OK
set_mode("write")   # ✅ OK
set_mode("delete")  # ❌ Type error (mypy)
```

**Literal** restricts to specific values only.

### 4.10. Final Types

**File**: [`type_hints.py`](type_hints.py) - Line 343

```python
from typing import Final

MAX_SIZE: Final[int] = 100  # ← Cannot be reassigned

# MAX_SIZE = 200  # ❌ Type error (mypy)
```

### 4.11. Function Overloading

**File**: [`type_hints.py`](type_hints.py) - Line 353

```python
from typing import overload, Union

@overload
def process(value: int) -> int:
    ...

@overload
def process(value: str) -> str:
    ...

def process(value: Union[int, str]) -> Union[int, str]:
    if isinstance(value, int):
        return value * 2
    return value.upper()

# Type checker knows:
process(5)       # Returns int
process("hello") # Returns str
```

### 4.12. Type Aliases

**File**: [`type_hints.py`](type_hints.py) - Line 489

```python
# Type aliases for complex types
Point3D = tuple[float, float, float]
Matrix = list[list[float]]
JSONDict = dict[str, Union[str, int, float, bool, None]]

def distance_3d(p1: Point3D, p2: Point3D) -> float:
    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5

def create_matrix(rows: int, cols: int) -> Matrix:
    return [[0.0 for _ in range(cols)] for _ in range(rows)]
```

### 4.13. Advanced Type Hints

**File**: [`type_hints.py`](type_hints.py) - Line 373

```python
from collections.abc import Iterable, Sequence

# Iterable: any iterable (list, tuple, set, generator, etc.)
def sum_iterable(items: Iterable[int]) -> int:
    return sum(items)

# Sequence: list, tuple, str (supports indexing)
def first_n(items: Sequence[T], n: int) -> Sequence[T]:
    return items[:n]

# Complex nested types
def complex_function(
    data: dict[str, list[tuple[int, str]]],
    callback: Optional[Callable[[str], None]] = None
) -> list[int]:
    ...
```

### 💡 Type Hint Best Practices

1. **Use type hints for public APIs** (functions, classes)
2. **Start with basic types**, add complexity as needed
3. **Use mypy** for static type checking
4. **Type aliases** for complex types
5. **Optional** for values that can be None
6. **Callable** for function parameters
7. **TypeVar** for generic functions
8. **Protocol** for structural typing
9. **Avoid Any** (defeats purpose of type hints)
10. **Document with docstrings** in addition to type hints

---

## 5. List and Optional Basics

**File**: [`list_optional_basics.py`](list_optional_basics.py)

### 5.1. Common Questions Answered

This section answers the most common beginner questions about `List` and `Optional` type hints.

#### Question 1: Do I need List keyword or can I use []?

**File**: [`list_optional_basics.py`](list_optional_basics.py) - Line 21

```python
# ❌ WRONG: Cannot use [] in type hints
# def process(items: []) -> None:  # SyntaxError!

# ✅ CORRECT: Use list or List
def process(items: list) -> None:
    for item in items:
        print(item)

def process_strings(items: List[str]) -> None:
    for item in items:
        print(item.upper())
```

**Answer**: You **cannot** use `[]` in type hints. Use `list` or `List[T]`.

#### Question 2: List (from typing) vs list (built-in)?

**File**: [`list_optional_basics.py`](list_optional_basics.py) - Line 54

```python
# Python 3.9+: Use built-in list
def modern_way(items: list[str]) -> list[int]:
    return [len(item) for item in items]

# Python 3.8 and earlier: Use List from typing
from typing import List

def old_way(items: List[str]) -> List[int]:
    return [len(item) for item in items]
```

**Answer**:
- **Python 3.9+**: Use `list[str]` (built-in, lowercase)
- **Python 3.8 and earlier**: Use `List[str]` (from typing, uppercase)

#### Question 3: What does Optional[List[str]] mean?

**File**: [`list_optional_basics.py`](list_optional_basics.py) - Line 79

```python
from typing import Optional, List

def process_names(names: Optional[List[str]]) -> int:
    """
    Optional[List[str]] means: "a list of strings OR None"
    """
    if names is None:  # ← Must check for None!
        return 0
    return len(names)

# Usage
process_names(["Alice", "Bob"])  # ✅ OK - list of strings
process_names(None)              # ✅ OK - None
process_names([])                # ✅ OK - empty list
```

**Answer**: `Optional[List[str]]` means the parameter can be:
- A list of strings: `["a", "b", "c"]`
- OR `None`

**Equivalent to**: `Union[List[str], None]` or `List[str] | None` (Python 3.10+)

#### Question 4: When and why use type hints?

**File**: [`list_optional_basics.py`](list_optional_basics.py) - Line 125

**Benefits**:

1. **IDE Autocomplete**: IDE knows what methods are available
   ```python
   def process(items: List[str]) -> None:
       for item in items:
           item.upper()  # ← IDE suggests .upper(), .lower(), etc.
   ```

2. **Catch Errors Early**: Type checkers (mypy) find bugs before runtime
   ```python
   def get_length(items: List[str]) -> int:
       return len(items)

   get_length([1, 2, 3])  # ← mypy error: Expected List[str], got List[int]
   ```

3. **Better Documentation**: Clear what types are expected
   ```python
   def find_user(email: str, users: List[dict]) -> Optional[dict]:
       # Clear: takes string and list of dicts, returns dict or None
       ...
   ```

4. **Easier to Understand**: Code is self-documenting

### 5.2. Real-World Examples

**File**: [`list_optional_basics.py`](list_optional_basics.py) - Line 149

#### Example 1: Get User Emails

```python
def get_user_emails(user_ids: List[int]) -> List[str]:
    """Get emails for given user IDs."""
    emails = []
    for user_id in user_ids:
        emails.append(f"user{user_id}@example.com")
    return emails

# Usage
emails = get_user_emails([1, 2, 3])
# ['user1@example.com', 'user2@example.com', 'user3@example.com']
```

#### Example 2: Find User by Email

```python
def find_user_by_email(
    email: str,
    users: List[dict]
) -> Optional[dict]:
    """Find user by email. Returns None if not found."""
    for user in users:
        if user.get("email") == email:
            return user
    return None

# Usage
users = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"}
]
found = find_user_by_email("alice@example.com", users)
# {'name': 'Alice', 'email': 'alice@example.com'}
```

#### Example 3: Process Optional List

```python
def process_optional_list(
    items: Optional[List[str]] = None
) -> List[str]:
    """Process optional list parameter."""
    if items is None:
        items = []
    return [item.upper() for item in items]

# Usage
process_optional_list(["hello", "world"])  # ['HELLO', 'WORLD']
process_optional_list(None)                # []
process_optional_list()                    # []
```

### 5.3. Common Patterns

**File**: [`list_optional_basics.py`](list_optional_basics.py) - Line 186

#### Pattern 1: Optional with Default
```python
def func(items: Optional[List[str]] = None) -> None:
    if items is None:
        items = []
    # Process items...
```
**Use when**: Parameter is optional, defaults to None

#### Pattern 2: Required List
```python
def func(items: List[str]) -> None:
    # No None check needed
    for item in items:
        print(item)
```
**Use when**: Parameter is required, cannot be None

#### Pattern 3: Optional Return
```python
def find(term: str, items: List[str]) -> Optional[str]:
    for item in items:
        if term in item:
            return item
    return None
```
**Use when**: Function may or may not return a value

#### Pattern 4: Nested Optional
```python
def filter_none(
    data: Optional[List[Optional[str]]] = None
) -> List[str]:
    if data is None:
        return []
    return [item for item in data if item is not None]
```
**Use when**: List may contain None values

### 💡 List and Optional Best Practices

1. **Python 3.9+**: Use `list[str]` instead of `List[str]`
2. **Python 3.8-**: Import and use `List` from typing
3. **Always check for None** with Optional parameters
4. **Use Optional** for parameters that can be None
5. **Use Optional** for return values that may be None
6. **Avoid mutable defaults**: Use `None` and create list inside function
7. **Be explicit**: `Optional[List[str]]` is clearer than just `list`
8. **Type checkers**: Run mypy to catch type errors

### 📊 Quick Reference

| Type Hint | Meaning | Example |
|-----------|---------|---------|
| `list` | Any list | `items: list` |
| `list[str]` | List of strings (3.9+) | `names: list[str]` |
| `List[str]` | List of strings (3.8-) | `names: List[str]` |
| `Optional[list]` | List or None | `items: Optional[list]` |
| `Optional[List[str]]` | List of strings or None | `names: Optional[List[str]]` |
| `List[Optional[str]]` | List that may contain None | `data: List[Optional[str]]` |

---

## 6. Summary

### 🎯 What You Learned

1. **Lambda Functions**
   - Anonymous functions with `lambda` keyword
   - Single expression only
   - Common with map/filter/sorted
   - Closure pitfall in loops
   - Use default args to capture values

2. **Closures**
   - Functions that capture enclosing scope
   - Maintain state between calls
   - Data hiding and encapsulation
   - Factory pattern for creating closures
   - Shared vs independent state
   - Loop variable pitfall

3. **Type Hints**
   - Static type annotations
   - Basic types and containers
   - Optional and Union types
   - Callable for functions
   - TypeVar for generics
   - Protocol for structural typing
   - Literal and Final types
   - Function overloading
   - Type aliases

4. **List and Optional Basics**
   - Cannot use `[]` in type hints
   - `list[str]` (Python 3.9+) vs `List[str]` (Python 3.8-)
   - `Optional[T]` means "T or None"
   - `Optional[List[str]]` means "list of strings or None"
   - Type hints for IDE autocomplete
   - Common patterns (optional with default, required list, optional return)
   - Real-world examples

### 📝 Quick Reference

#### Lambda Syntax
```python
lambda arguments: expression

# Examples
lambda x: x * 2
lambda x, y: x + y
lambda: 42
```

#### Closure Pattern
```python
def factory(config):
    state = initial_value

    def closure(arg):
        nonlocal state
        # Use config and state
        return result

    return closure
```

#### Type Hint Patterns
```python
# Basic
def func(x: int) -> str: ...

# Optional
def func(x: Optional[int] = None) -> str: ...

# Callable
def func(callback: Callable[[int], str]) -> None: ...

# Generic
T = TypeVar('T')
def func(items: list[T]) -> T: ...
```

### ✅ Checklist

Before moving to the next topic, make sure you can:

- [ ] Write and use lambda functions
- [ ] Understand lambda limitations
- [ ] Use lambda with map/filter/sorted/reduce
- [ ] Avoid closure pitfall in loops
- [ ] Create closures that maintain state
- [ ] Use closures for data hiding
- [ ] Understand factory pattern with closures
- [ ] Add type hints to functions
- [ ] Use Optional and Union types
- [ ] Type hint functions (Callable)
- [ ] Create generic functions (TypeVar)
- [ ] Use Protocol for structural typing
- [ ] Create type aliases for complex types
- [ ] Run mypy for type checking

### 🚀 Next Steps

Ready to learn more? Continue to:

- **[05. Functional Programming](../05_functional_programming/)** - Higher-order functions, map/filter/reduce
- **[06. Decorators](../06_decorators/)** - Decorator patterns and applications
- **[07. Generators](../07_generators/)** - Generators and yield

### 💡 Common Patterns

**Pattern 1: Lambda for Sorting**
```python
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
sorted(students, key=lambda s: s[1], reverse=True)
```

**Pattern 2: Closure for Configuration**
```python
def make_validator(min_val, max_val):
    def validate(value):
        return min_val <= value <= max_val
    return validate

is_valid_age = make_validator(0, 120)
```

**Pattern 3: Type-Safe Factory**
```python
T = TypeVar('T')

def create_list(item: T, count: int) -> list[T]:
    return [item] * count
```

---

### 📁 Files in This Section

| File | Description |
|------|-------------|
| [`lambda_functions.py`](lambda_functions.py) | Lambda functions and patterns |
| [`closures.py`](closures.py) | Closures and encapsulation |
| [`type_hints.py`](type_hints.py) | Advanced type hints |
| [`param_spec_examples.py`](param_spec_examples.py) | Callable + ParamSpec helper examples (`call_twice`, `wait_until`) |
| [`list_optional_basics.py`](list_optional_basics.py) | List and Optional type hints (beginner guide) |

**Total**: 5 files

---

[← Back to Functions](../functions.md) | [Previous: Scope](../03_scope/) | [Next: Functional Programming →](../05_functional_programming/)




