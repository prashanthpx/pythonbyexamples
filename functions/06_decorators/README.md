# 06. Decorators

[← Back to Functions](../functions.md) | [Previous: Functional Programming](../05_functional_programming/) | [Next: Generators →](../07_generators/)

## 📚 Table of Contents

1. [Introduction](#1-introduction)
2. [Basic Decorators](#2-basic-decorators)
3. [Decorators with Arguments](#3-decorators-with-arguments)
4. [Class Decorators](#4-class-decorators)
5. [Summary](#5-summary)

---

## 1. Introduction

**Decorators** are a powerful Python feature that allows you to modify or enhance functions and classes without changing their source code.

### What Are Decorators?

A decorator is a **callable** (function or class) that:
1. Takes a function (or class) as input
2. Returns a modified version of that function (or class)

### The @ Syntax

The `@decorator` syntax is **syntactic sugar**:

```python
@decorator
def func():
    pass

# Equivalent to:
func = decorator(func)
```

### Why Use Decorators?

| Use Case | Example |
|----------|---------|
| **Logging** | Log function calls and returns |
| **Timing** | Measure execution time |
| **Caching** | Store results to avoid recomputation |
| **Validation** | Check arguments before execution |
| **Authentication** | Verify user permissions |
| **Rate Limiting** | Control call frequency |
| **Retry Logic** | Retry failed operations |

### Core Concepts

1. **Decorators execute at definition time** (when function is defined)
2. **Decorators wrap functions** (add behavior before/after)
3. **Use `@wraps`** to preserve function metadata
4. **Decorators can be stacked** (applied bottom-to-top)
5. **Decorators can take arguments** (decorator factories)

---

## 2. Basic Decorators

**File**: [`basic_decorators.py`](basic_decorators.py)

### 2.1. Simple Decorator Pattern

**File**: [`basic_decorators.py`](basic_decorators.py) - Line 24

```python
def simple_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Before calling {func.__name__}")
        result = func(*args, **kwargs)  # ← Call original
        print(f"After calling {func.__name__}")
        return result
    return wrapper  # ← Return wrapper

@simple_decorator
def greet(name):
    return f"Hello, {name}!"

# Equivalent to:
# greet = simple_decorator(greet)
```

#### Deep dive: what actually happens to `greet`

The key moment is this line:

```python
greet = simple_decorator(greet)
```

This is what Python does **under the hood** for:

```python
@simple_decorator
def greet(name):
    ...
```

At the start you have **one name, one function object**:

```text
greet  ───►  function greet(name)
```

**Step 1 – Call `simple_decorator(greet)`**

You pass the **original** `greet` function into `simple_decorator`:

- Inside `simple_decorator`, the parameter `func` refers to the original
  `greet` function.

**Step 2 – `simple_decorator` returns `wrapper`**

Inside the decorator:

```python
def simple_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Before calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After calling {func.__name__}")
        return result
    return wrapper
```

The `return wrapper` line means that the call:

```python
simple_decorator(greet)
```

evaluates to **the new `wrapper` function object**.

**Step 3 – Assignment replaces the name `greet`**

Now Python assigns that returned `wrapper` back to the name `greet`:

```python
greet = wrapper
```

So after decoration:

```text
greet  ───►  wrapper(*args, **kwargs)
```

The **original** `greet` function still exists, but it is now only reachable as
`func` **inside the closure** of `wrapper`.

Full picture:

```text
Before decoration:
    greet   ───────►  [function greet(name)]

After calling simple_decorator(greet):
    wrapper ──────►  [function wrapper(...):
                          calls func(...)
                      ]
    func    ───────►  original greet(name)

After assignment greet = wrapper:
    greet   ───────►  wrapper
                       │
                       └── inside wrapper: func = original greet
```

#### Call flow when you run `greet("Bob")`

When you call:

```python
greet("Bob")
```

you are **actually calling the wrapper**, because `greet` now points to it:

1. User calls `greet("Bob")`.
2. Python calls `wrapper("Bob")`.
3. `wrapper` prints `Before calling greet`.
4. `wrapper` calls `func("Bob")` – this is the **original** `greet`.
5. The original `greet` returns `"Hello, Bob!"`.
6. `wrapper` prints `After calling greet`.
7. `wrapper` returns `"Hello, Bob!"` to the caller.

#### Final mental model

- Decorators **do not modify** the original function object.
- They **replace the function name** (like `greet`) with a **new wrapper
  function**.
- The wrapper **calls the original** via the closed-over `func` variable.

So your mental model should be:

```text
greet  ==  wrapper   (after decoration)
```

and:

```text
inside wrapper: func == original greet
```

### 🔑 Key Pattern

```
decorator(function) -> wrapper function
wrapper(*args, **kwargs) -> calls original function
```

#### 2.1.1 Same mechanic without `@` syntax

In the same file we also have a version **without** the `@` syntax:

```python
def say_goodbye(name: str) -> str:
    """Say goodbye."""
    return f"Goodbye, {name}!"


# Manual decoration (without @)
say_goodbye = simple_decorator(say_goodbye)  #  Same as @simple_decorator
```

This line:

```python
say_goodbye = simple_decorator(say_goodbye)
```

does **exactly the same thing** as writing:

```python
@simple_decorator
def say_goodbye(name: str) -> str:
    ...
```

So the same mental model applies:

- Before decoration:

  ```text
  say_goodbye  ───►  function say_goodbye(name)
  ```

- After decoration:

  ```text
  say_goodbye  ───►  wrapper(...)
                      │
                      └── inside wrapper: func == original say_goodbye
  ```

The `@simple_decorator` form is just a **shorter spelling** for
`name = simple_decorator(name)` at definition time.

### 2.2. Logging Decorator

**File**: [`basic_decorators.py`](basic_decorators.py) - Line 73

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        # Log arguments
        print(f"Calling {func.__name__}({args}, {kwargs})")
        
        # Call function
        result = func(*args, **kwargs)
        
        # Log return value
        print(f"{func.__name__} returned {result!r}")
        
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(5, 3)
# Output:
# Calling add((5, 3), {})
# add returned 8
```

### 2.3. Timing Decorator

**File**: [`basic_decorators.py`](basic_decorators.py) - Line 109

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function(n):
    time.sleep(0.1)
    return n * 2
```

### 2.4. Validation Decorator

**File**: [`basic_decorators.py`](basic_decorators.py) - Line 145

```python
def validate_positive(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(f"All arguments must be positive")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def calculate_area(width, height):
    return width * height

calculate_area(5, 3)   # ✅ OK
calculate_area(-5, 3)  # ❌ ValueError
```

### 2.5. Caching Decorator (Memoization)

**File**: [`basic_decorators.py`](basic_decorators.py) - Line 191

```python
def cache(func):
    cached_results = {}
    
    def wrapper(*args):
        if args in cached_results:
            return cached_results[args]  # ← Cache hit
        
        result = func(*args)
        cached_results[args] = result  # ← Store result
        return result
    
    return wrapper

@cache
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### 2.6. Preserving Metadata with @wraps

**File**: [`basic_decorators.py`](basic_decorators.py) - Line 225

**Problem**: Decorators hide function metadata

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def my_func():
    """My docstring"""
    pass

print(my_func.__name__)  # 'wrapper' ❌
print(my_func.__doc__)   # None ❌
```

**Solution**: Use `@wraps`

```python
from functools import wraps

def decorator(func):
    @wraps(func)  # ← Preserves metadata
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def my_func():
    """My docstring"""
    pass

print(my_func.__name__)  # 'my_func' ✅
print(my_func.__doc__)   # 'My docstring' ✅
```

### 2.7. Stacking Decorators

**File**: [`basic_decorators.py`](basic_decorators.py) - Line 283

```python
@timer
@log_calls
def complex_operation(a, b):
    return a ** b

# Equivalent to:
# complex_operation = timer(log_calls(complex_operation))
```

**Order**: Decorators are applied **bottom-to-top**:
1. `log_calls` is applied first (innermost)
2. `timer` is applied second (outermost)

### 2.8 Visual summary – what decorators do to names

You can think of decorators like this for both `greet` and `say_goodbye`.

**Before decoration**

```text
greet       ───►  function greet(name)
say_goodbye ───►  function say_goodbye(name)
```

**Decoration step**

```python
greet       = simple_decorator(greet)
say_goodbye = simple_decorator(say_goodbye)
```

**After decoration**

```text
greet       ───►  wrapper(...)
                    │
                    └── inside wrapper: func == original greet

say_goodbye ───►  wrapper(...)
                    │
                    └── inside wrapper: func == original say_goodbye
```

Same pattern, different original function:

- The **name** (like `greet` or `say_goodbye`) now refers to `wrapper`.
- The **original function** is captured in the closure as `func`.

This is true whether you write it with `@simple_decorator` or with an
explicit assignment.

### 💡 Basic Decorators Best Practices

1. **Always use `@wraps`** to preserve metadata
2. **Use `*args, **kwargs`** to accept any arguments
3. **Return the result** from the original function
4. **Keep decorators simple** (single responsibility)
5. **Document what the decorator does**
6. **Consider side effects** (logging, timing are OK; modifying args is risky)

---

## 3. Decorators with Arguments

**File**: [`decorator_arguments.py`](decorator_arguments.py)

### 3.1. Decorator Factory Pattern

To create a decorator that accepts arguments, you need **three levels of nesting**:

```python
def decorator_factory(param):      # ← Level 1: Factory (takes params)
    def decorator(func):            # ← Level 2: Decorator (takes function)
        def wrapper(*args, **kwargs):  # ← Level 3: Wrapper (takes args)
            # Use param, func, args, kwargs
            return func(*args, **kwargs)
        return wrapper
    return decorator

@decorator_factory(value)
def my_func():
    pass

# Equivalent to:
# my_func = decorator_factory(value)(my_func)
```

### 3.2. Repeat Decorator

**File**: [`decorator_arguments.py`](decorator_arguments.py) - Line 35

```python
def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for i in range(times):  # ← Use 'times' from factory
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Output:
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

### 3.3. Logging with Custom Prefix

**File**: [`decorator_arguments.py`](decorator_arguments.py) - Line 76

```python
def log_with_prefix(prefix="LOG"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{prefix}] Calling {func.__name__}")
            result = func(*args, **kwargs)
            print(f"[{prefix}] Returned {result!r}")
            return result
        return wrapper
    return decorator

@log_with_prefix("INFO")
def add(a, b):
    return a + b

@log_with_prefix()  # ← Use default
def subtract(a, b):
    return a - b
```

### 3.4. Retry Decorator

**File**: [`decorator_arguments.py`](decorator_arguments.py) - Line 117

```python
def retry(max_attempts=3, delay=1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_attempts:
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_function():
    # May fail, will retry up to 3 times
    ...
```

### 3.5. Rate Limiting

**File**: [`decorator_arguments.py`](decorator_arguments.py) - Line 170

```python
def rate_limit(calls_per_second):
    min_interval = 1.0 / calls_per_second

    def decorator(func):
        last_called = [0.0]

        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)

            last_called[0] = time.time()
            return func(*args, **kwargs)

        return wrapper
    return decorator

@rate_limit(calls_per_second=2.0)  # Max 2 calls/second
def api_call(endpoint):
    ...
```

### 3.6. Validation with Custom Rules

**File**: [`decorator_arguments.py`](decorator_arguments.py) - Line 209

```python
def validate(min_value=None, max_value=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in args:
                if isinstance(arg, (int, float)):
                    if min_value is not None and arg < min_value:
                        raise ValueError(f"Argument {arg} < {min_value}")
                    if max_value is not None and arg > max_value:
                        raise ValueError(f"Argument {arg} > {max_value}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate(min_value=0, max_value=100)
def set_percentage(value):
    return f"Percentage: {value}%"

set_percentage(75)   # ✅ OK
set_percentage(150)  # ❌ ValueError
```

### 3.7. Decorator with or without Arguments

**File**: [`decorator_arguments.py`](decorator_arguments.py) - Line 365

```python
def smart_log(func=None, *, prefix="LOG"):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(f"[{prefix}] {f.__name__} called")
            return f(*args, **kwargs)
        return wrapper

    # Called without arguments: @smart_log
    if func is not None:
        return decorator(func)

    # Called with arguments: @smart_log(prefix="INFO")
    return decorator

@smart_log
def func1():
    pass

@smart_log(prefix="DEBUG")
def func2():
    pass
```

### 💡 Decorator Arguments Best Practices

1. **Three levels**: factory -> decorator -> wrapper
2. **Use default arguments** for optional parameters
3. **Document parameters** clearly
4. **Validate parameters** in factory
5. **Use keyword-only args** (`*,` syntax) for clarity
6. **Consider making decorator work with or without args**

---

## 4. Class Decorators

**File**: [`class_decorators.py`](class_decorators.py)

### 4.1. Two Patterns

**Pattern 1**: Function decorator for classes
```python
def decorator(cls):
    # Modify class
    return cls

@decorator
class MyClass:
    pass
```

**Pattern 2**: Class as decorator
```python
class Decorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

@Decorator
def my_func():
    pass
```

### 4.2. Adding Methods to Classes

**File**: [`class_decorators.py`](class_decorators.py) - Line 20

```python
def add_str_method(cls):
    def __str__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"

    cls.__str__ = __str__
    return cls

@add_str_method
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Alice", 30)
print(person)  # Person(name='Alice', age=30)
```

### 4.3. Singleton Pattern

**File**: [`class_decorators.py`](class_decorators.py) - Line 54

```python
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Database:
    def __init__(self, host="localhost"):
        self.host = host

db1 = Database("localhost")
db2 = Database("remote")
print(db1 is db2)  # True (same instance!)
```

### 4.4. Class as Decorator (CountCalls)

**File**: [`class_decorators.py`](class_decorators.py) - Line 99

```python
class CountCalls:
    def __init__(self, func):
        wraps(func)(self)
        self.func = func
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        print(f"Call #{self.call_count}")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    return f"Hello, {name}!"

greet("Alice")  # Call #1
greet("Bob")    # Call #2
print(greet.call_count)  # 2
```

### 4.5. Class Decorator with Parameters

**File**: [`class_decorators.py`](class_decorators.py) - Line 143

```python
class Timer:
    def __init__(self, message="Execution time"):
        self.message = message

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"{self.message}: {elapsed:.4f}s")
            return result
        return wrapper

@Timer()  # ← Note: parentheses required
def slow_function():
    time.sleep(0.1)

@Timer(message="Custom timer")
def another_function():
    time.sleep(0.05)
```

### 💡 Class Decorators Best Practices

1. **Use `__call__`** to make class instances callable
2. **Preserve metadata** with `wraps(func)(self)`
3. **Store state** in instance variables
4. **Document clearly** which pattern you're using
5. **Class decorators with params**: `__init__` for params, `__call__` for function

---

## 5. Summary

### 🎯 What You Learned

1. **Basic Decorators**
   - Decorator pattern: function that wraps another function
   - `@decorator` syntax is syntactic sugar
   - Use `*args, **kwargs` to accept any arguments
   - Always use `@wraps` to preserve metadata
   - Common patterns: logging, timing, validation, caching
   - Decorators can be stacked (bottom-to-top)

2. **Decorators with Arguments**
   - Decorator factories create parameterized decorators
   - Three levels: factory -> decorator -> wrapper
   - Factory takes parameters, returns decorator
   - Decorator takes function, returns wrapper
   - Wrapper takes arguments, calls function
   - Common patterns: retry, rate limit, validation

3. **Class Decorators**
   - Two patterns: function decorator for classes, class as decorator
   - Function decorators modify class definition
   - Class decorators use `__call__` to be callable
   - Can maintain state in instance variables
   - Singleton pattern with class decorators
   - Class decorators with params: `__init__` for params, `__call__` for function

### 📝 Quick Reference

#### Basic Decorator
```python
from functools import wraps

def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Before
        result = func(*args, **kwargs)
        # After
        return result
    return wrapper

@decorator
def my_func():
    pass
```

#### Decorator with Arguments
```python
def decorator_factory(param):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use param
            return func(*args, **kwargs)
        return wrapper
    return decorator

@decorator_factory(value)
def my_func():
    pass
```

#### Class as Decorator
```python
class Decorator:
    def __init__(self, func):
        wraps(func)(self)
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

@Decorator
def my_func():
    pass
```

#### Class Decorator with Parameters
```python
class Decorator:
    def __init__(self, param):
        self.param = param

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use self.param
            return func(*args, **kwargs)
        return wrapper

@Decorator(value)
def my_func():
    pass
```

### ✅ Checklist

Before moving to the next topic, make sure you can:

- [ ] Write a basic decorator
- [ ] Use `@decorator` syntax
- [ ] Preserve metadata with `@wraps`
- [ ] Stack multiple decorators
- [ ] Create decorator factories (decorators with arguments)
- [ ] Understand the three-level nesting pattern
- [ ] Apply decorators to classes
- [ ] Create class-based decorators
- [ ] Use `__call__` to make classes callable
- [ ] Implement common patterns (logging, timing, caching, validation)
- [ ] Understand decorator execution order
- [ ] Debug decorated functions

### 🚀 Next Steps

Ready to learn more? Continue to:

- **[07. Generators](../07_generators/)** - Generators and yield
- **[08. Advanced Topics](../08_advanced_topics/)** - Recursion, async, memoization

### 💡 Common Patterns

**Pattern 1: Logging**
```python
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Returned {result!r}")
        return result
    return wrapper
```

**Pattern 2: Timing**
```python
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Took {time.time() - start:.4f}s")
        return result
    return wrapper
```

**Pattern 3: Caching**
```python
def cache(func):
    cached = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cached:
            cached[args] = func(*args)
        return cached[args]
    return wrapper
```

**Pattern 4: Retry**
```python
def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
        return wrapper
    return decorator
```

**Pattern 5: Validation**
```python
def validate_positive(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError("Must be positive")
        return func(*args, **kwargs)
    return wrapper
```

---

### 📁 Files in This Section

| File | Description | Lines |
|------|-------------|-------|
| [`basic_decorators.py`](basic_decorators.py) | Basic decorator patterns | 450 |
| [`decorator_arguments.py`](decorator_arguments.py) | Decorators with arguments | 557 |
| [`class_decorators.py`](class_decorators.py) | Class decorators and decorators for classes | 585 |

**Total**: 3 files, 1,592 lines of code and documentation

---

[← Back to Functions](../functions.md) | [Previous: Functional Programming](../05_functional_programming/) | [Next: Generators →](../07_generators/)

