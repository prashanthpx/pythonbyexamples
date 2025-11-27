# Python Functions - Parameters

[← Back to Functions](../functions.md) | [Previous: Basics](../01_basics/) | [Next: Scope →](../03_scope/)

> **Level**: 🟡 Intermediate  
> **Estimated Time**: 2.5 hours  
> **Prerequisites**: [01. Basics](../01_basics/)

---

## 📚 Table of Contents

1. [Introduction to Parameters](#1-introduction-to-parameters)
2. [Positional Arguments](#2-positional-arguments)
3. [Keyword Arguments](#3-keyword-arguments)
4. [Default Values](#4-default-values)
5. [*args and **kwargs](#5-args-and-kwargs)
6. [Parameter Order Rules](#6-parameter-order-rules)
7. [Summary](#7-summary)

---

## 1. Introduction to Parameters

**Parameters** are the variables listed in a function definition. **Arguments** are the actual values passed to the function when calling it.

```python
def greet(name):  # 'name' is a parameter
    return f"Hello, {name}!"

greet("Alice")    # "Alice" is an argument
```

### Types of Parameters in Python

| Type | Syntax | Description |
|------|--------|-------------|
| **Positional-only** | `param, /` | Must be passed by position |
| **Standard** | `param` | Can be positional or keyword |
| **Positional with default** | `param=value` | Optional, can be positional or keyword |
| **Variable positional** | `*args` | Collects extra positional arguments |
| **Keyword-only** | `*, param` | Must be passed by keyword |
| **Variable keyword** | `**kwargs` | Collects extra keyword arguments |

---

## 2. Positional Arguments

**File**: [`positional_args.py`](positional_args.py)

### 2.1. Basic Positional Arguments

Arguments are matched by **position** - order matters!

```python
def greet(first_name: str, last_name: str) -> str:
    return f"Hello, {first_name} {last_name}!"

# Correct order
greet("John", "Doe")  # "Hello, John Doe!"

# Wrong order - wrong result!
greet("Doe", "John")  # "Hello, Doe John!"
```

### 🔑 Key Takeaway

**Order matters!** The first argument goes to the first parameter, second to second, etc.

### 2.2. Positional-Only Parameters (Python 3.8+)

**File**: [`positional_args.py`](positional_args.py) - Line 90

Use `/` to mark parameters as positional-only:

```python
def positional_only_example(name: str, age: int, /) -> str:
    """
    Parameters before '/' MUST be positional.
    """
    return f"{name} is {age} years old"

# ✅ Correct: positional arguments
positional_only_example("Bob", 30)

# ❌ Error: cannot use keywords
positional_only_example(name="Bob", age=30)  # TypeError!
```

### ⚠️ Important

The `/` marker enforces positional-only. Parameters before `/` **cannot** be passed as keyword arguments.

### 💡 When to Use Positional-Only

- When parameter names are not meaningful (`x, y` coordinates)
- To prevent breaking changes if you rename parameters
- For performance-critical code (slight speed improvement)
- When you want to reserve parameter names for **kwargs

---

## 3. Keyword Arguments

**File**: [`keyword_args.py`](keyword_args.py)

### 3.1. Basic Keyword Arguments

Arguments are matched by **name** - order doesn't matter!

```python
def create_profile(name: str, age: int, city: str, country: str) -> dict:
    return {"name": name, "age": age, "city": city, "country": country}

# Order doesn't matter with keyword arguments
profile1 = create_profile(name="Alice", age=30, city="Seattle", country="USA")
profile2 = create_profile(country="USA", city="Seattle", age=30, name="Alice")

# Both produce the same result!
```

### 🔑 Key Takeaway

Keyword arguments are matched by **name**, not position. This makes code more readable and less error-prone.

### 3.2. Benefits of Keyword Arguments

**File**: [`keyword_args.py`](keyword_args.py) - Line 50

```python
# Without keywords - hard to understand
send_email("bob@example.com", "Meeting", "See you at 3pm")

# With keywords - crystal clear!
send_email(
    to="bob@example.com",
    subject="Meeting",
    body="See you at 3pm"
)
```

### ✅ Benefits

1. **Self-documenting** - clear what each value means
2. **Order-independent** - more flexible
3. **Easy to skip optional parameters**
4. **Reduces errors** from wrong argument order

### 3.3. Keyword-Only Parameters

**File**: [`keyword_args.py`](keyword_args.py) - Line 98

Use `*` to make parameters keyword-only:

```python
def keyword_only_params(*, name: str, age: int, email: str) -> str:
    """
    All parameters after '*' MUST be passed as keywords.
    """
    return f"{name} ({age}) - {email}"

# ✅ Correct: keyword arguments
keyword_only_params(name="Charlie", age=35, email="charlie@example.com")

# ❌ Error: cannot use positional
keyword_only_params("Charlie", 35, "charlie@example.com")  # TypeError!
```

### 💡 When to Use Keyword-Only

- For boolean flags (`enabled=True`, `verbose=False`)
- When you have many optional parameters
- To make function calls more explicit and readable
- To prevent positional argument mistakes

---

## 4. Default Values

**File**: [`default_values.py`](default_values.py)

### 4.1. Basic Default Values

Parameters can have default values, making them optional:

```python
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# Use default
greet("Alice")  # "Hello, Alice!"

# Override default
greet("Bob", "Hi")  # "Hi, Bob!"
```

### 🔑 Key Rules

1. **Required parameters come first**, then optional
2. Parameters with defaults can be **omitted or overridden**
3. Default values are evaluated **once** at function definition

### 4.2. The Mutable Default Argument Pitfall

**File**: [`default_values.py`](default_values.py) - Line 88

**⚠️ DANGER: Never use mutable objects as defaults!**

```python
# ❌ WRONG - Mutable default
def append_to_list_wrong(item: str, items: list = []) -> list:
    items.append(item)
    return items

list1 = append_to_list_wrong("apple")   # ['apple']
list2 = append_to_list_wrong("banana")  # ['apple', 'banana'] - WRONG!
# The default list is shared across all calls!
```

### ✅ Correct Way - Use None

```python
# ✅ CORRECT - Use None as default
def append_to_list_correct(item: str, items: Optional[list] = None) -> list:
    if items is None:
        items = []  # Create new list each time
    items.append(item)
    return items

list1 = append_to_list_correct("apple")   # ['apple']
list2 = append_to_list_correct("banana")  # ['banana'] - CORRECT!
```

### 🔑 Key Takeaway

**Never use mutable objects (list, dict, set) as default values!** Use `None` and create the mutable object inside the function.

### 💡 Why This Happens

Default values are created **once** when the function is defined, not each time it's called. Mutable objects get modified and retain their state across calls.

---

## 5. *args and **kwargs

**File**: [`args_kwargs.py`](args_kwargs.py)

### 5.1. *args - Variable Positional Arguments

`*args` collects any number of positional arguments into a **tuple**:

```python
def sum_numbers(*args: int) -> int:
    """Sum any number of integers."""
    total = 0
    for num in args:
        total += num
    return total

sum_numbers(1, 2, 3)           # 6
sum_numbers(10, 20, 30, 40)    # 100
sum_numbers()                  # 0 (empty tuple)
```

### 🔑 Key Points

- `*args` collects arguments into a **tuple**
- The name `args` is **convention** (can use any name)
- Can accept **zero or more** arguments
- Inside function, `args` is a regular tuple

### 5.2. **kwargs - Variable Keyword Arguments

**File**: [`args_kwargs.py`](args_kwargs.py) - Line 35

`**kwargs` collects any number of keyword arguments into a **dictionary**:

```python
def print_info(**kwargs: Any) -> None:
    """Print key-value pairs."""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="Seattle")
# Output:
# name: Alice
# age: 30
# city: Seattle
```

### 🔑 Key Points

- `**kwargs` collects arguments into a **dictionary**
- The name `kwargs` is **convention** (can use any name)
- Can accept **zero or more** keyword arguments
- Inside function, `kwargs` is a regular dict

### 5.3. Combining Regular Parameters with *args and **kwargs

**File**: [`args_kwargs.py`](args_kwargs.py) - Line 52

```python
def create_person(name: str, age: int, **kwargs: Any) -> dict:
    """
    Required parameters first, then **kwargs for optional attributes.
    """
    person = {"name": name, "age": age}
    person.update(kwargs)  # Add all additional keyword arguments
    return person

# Required params + optional extras
create_person("Alice", 30, city="Seattle", job="Engineer", hobby="Reading")
# {'name': 'Alice', 'age': 30, 'city': 'Seattle', 'job': 'Engineer', 'hobby': 'Reading'}
```

### 5.4. Parameters After *args Are Keyword-Only

**File**: [`args_kwargs.py`](args_kwargs.py) - Line 72

```python
def calculate(*args: float, operation: str = "sum") -> float:
    """
    Parameters after *args MUST be keyword-only.
    """
    if operation == "sum":
        return sum(args)
    elif operation == "product":
        result = 1
        for num in args:
            result *= num
        return result

# 'operation' must be passed as keyword
calculate(1, 2, 3, 4, 5)                    # sum (default)
calculate(2, 3, 4, operation="product")     # product
```

### ⚠️ Important

Any parameter after `*args` **must** be passed as a keyword argument. This is automatic - you don't need the `*` marker.

### 5.5. Unpacking Arguments

**File**: [`args_kwargs.py`](args_kwargs.py) - Line 230

Use `*` to unpack sequences and `**` to unpack dictionaries:

```python
# Unpack list with *
numbers = [1, 2, 3, 4, 5]
sum_numbers(*numbers)  # Equivalent to sum_numbers(1, 2, 3, 4, 5)

# Unpack dictionary with **
person_data = {"name": "Charlie", "age": 35, "city": "Boston"}
create_person(**person_data)  # Unpacks dict into keyword arguments
```

### 🔑 Key Takeaway

- `*` unpacks **sequences** (list, tuple) into positional arguments
- `**` unpacks **dictionaries** into keyword arguments
- Very useful for forwarding arguments to other functions

### 5.6. Full Parameter Signature

**File**: [`args_kwargs.py`](args_kwargs.py) - Line 95

```python
def full_signature(
    pos_only: str,
    /,
    standard: str,
    *args: int,
    kw_only: str,
    **kwargs: Any
) -> dict:
    """Demonstrates all parameter types together."""
    return {
        "pos_only": pos_only,
        "standard": standard,
        "args": args,
        "kw_only": kw_only,
        "kwargs": kwargs
    }

# Call with all parameter types
full_signature(
    "pos_value",           # positional-only
    "std_value",           # standard (positional)
    1, 2, 3,              # *args
    kw_only="kw_value",   # keyword-only
    extra1="value1",      # **kwargs
    extra2="value2"       # **kwargs
)
```

---

## 6. Parameter Order Rules

**File**: [`parameter_order.py`](parameter_order.py)

### 6.1. The Strict Order

Python enforces a **strict order** for parameter types:

```python
def function(
    pos_only1, pos_only2, /,        # 1. Positional-only (optional)
    standard1, standard2=default,   # 2. Standard parameters
    *args,                          # 3. Variable positional (optional)
    kw_only1, kw_only2=default,    # 4. Keyword-only
    **kwargs                        # 5. Variable keyword (optional)
):
    pass
```

### 📋 Order Rules

| Position | Type | Marker | Required? | Can Have Defaults? |
|----------|------|--------|-----------|-------------------|
| 1 | Positional-only | Before `/` | No | Yes |
| 2 | Standard | Between `/` and `*` | No | Yes |
| 3 | *args | `*args` | No | N/A |
| 4 | Keyword-only | After `*` or `*args` | No | Yes |
| 5 | **kwargs | `**kwargs` | No | N/A |

### ⚠️ Critical Rules

1. **Required before optional** (within each group)
2. **Positional-only** must come first
3. **Standard** parameters come next
4. **`*args`** comes after standard
5. **Keyword-only** comes after `*` or `*args`
6. **`**kwargs`** must come last
7. Breaking these rules causes **SyntaxError**

### 6.2. Common Patterns

**File**: [`parameter_order.py`](parameter_order.py) - Line 280

```python
# Pattern 1: Standard only
def func(a, b, c=default):
    pass

# Pattern 2: With *args
def func(a, *args):
    pass

# Pattern 3: With **kwargs
def func(a, b=default, **kwargs):
    pass

# Pattern 4: With keyword-only
def func(a, *, b, c=default):
    pass

# Pattern 5: Everything
def func(pos, /, std, *args, kw, **kwargs):
    pass
```

### 6.3. Why Order Matters

**File**: [`parameter_order.py`](parameter_order.py) - Line 15

The order ensures Python can unambiguously determine:
- Which arguments are positional
- Which are keyword
- Where variable arguments go
- What's required vs optional

Breaking the order would create ambiguity in how to match arguments to parameters.

---

## 7. Summary

### 🎯 What You Learned

1. **Positional Arguments**
   - Matched by position (order matters)
   - Use `/` for positional-only parameters
   - Good for simple, obvious parameters

2. **Keyword Arguments**
   - Matched by name (order doesn't matter)
   - Use `*` for keyword-only parameters
   - Makes code self-documenting

3. **Default Values**
   - Make parameters optional
   - Required before optional
   - ⚠️ Never use mutable defaults!

4. ***args and **kwargs**
   - `*args` collects positional arguments (tuple)
   - `**kwargs` collects keyword arguments (dict)
   - Use `*` and `**` to unpack arguments

5. **Parameter Order**
   - Strict order: `pos_only, /, standard, *args, kw_only, **kwargs`
   - Breaking order causes SyntaxError
   - Required before optional within each group

### 📝 Quick Reference

```python
def complete_function(
    # 1. Positional-only (before /)
    pos_only_required: str,
    pos_only_optional: str = "default",
    /,

    # 2. Standard (can be positional or keyword)
    standard_required: str,
    standard_optional: str = "default",

    # 3. Variable positional
    *args: int,

    # 4. Keyword-only (after * or *args)
    kw_only_required: str,
    kw_only_optional: str = "default",

    # 5. Variable keyword
    **kwargs: Any
) -> dict:
    return {
        "pos_only_required": pos_only_required,
        "pos_only_optional": pos_only_optional,
        "standard_required": standard_required,
        "standard_optional": standard_optional,
        "args": args,
        "kw_only_required": kw_only_required,
        "kw_only_optional": kw_only_optional,
        "kwargs": kwargs
    }
```

### ✅ Checklist

Before moving to the next topic, make sure you can:

- [ ] Explain the difference between positional and keyword arguments
- [ ] Use `/` to create positional-only parameters
- [ ] Use `*` to create keyword-only parameters
- [ ] Set default values for parameters
- [ ] Avoid the mutable default argument pitfall
- [ ] Use `*args` to accept variable positional arguments
- [ ] Use `**kwargs` to accept variable keyword arguments
- [ ] Unpack arguments with `*` and `**`
- [ ] Understand and follow parameter order rules

### 🚀 Next Steps

Ready to learn more? Continue to:

- **[03. Scope](../03_scope/)** - Variable scope and namespaces
- **[04. Advanced Features](../04_advanced_features/)** - Lambda, closures, type hints
- **[05. Functional Programming](../05_functional_programming/)** - Higher-order functions

---

### 📁 Files in This Section

| File | Description | Lines |
|------|-------------|-------|
| [`positional_args.py`](positional_args.py) | Positional arguments and positional-only | 221 |
| [`keyword_args.py`](keyword_args.py) | Keyword arguments and keyword-only | 270 |
| [`default_values.py`](default_values.py) | Default values and mutable default pitfall | 308 |
| [`args_kwargs.py`](args_kwargs.py) | *args, **kwargs, and unpacking | 307 |
| [`parameter_order.py`](parameter_order.py) | Complete parameter order rules | 318 |

**Total**: 5 files, 1,424 lines of code and documentation

---

[← Back to Functions](../functions.md) | [Previous: Basics](../01_basics/) | [Next: Scope →](../03_scope/)


