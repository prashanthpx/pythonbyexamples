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

## 4. Default Values and Mutable Arguments

**Files**: [`default_values.py`](default_values.py), [`mutable_argument_aliasing.py`](mutable_argument_aliasing.py)

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

**Files**: [`default_values.py`](default_values.py) - mutable list examples,
[`fn_list_mutable_default_demo.py`](fn_list_mutable_default_demo.py) - `fn_list` comparison

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

#### Example: `fn_list(lt: list)` vs `fn_list(lt: list = [])`

This is one of the **most important Python concepts** to understand.

**Question:**

> Should we write `def fn_list(lt: list) -> list:` or
> `def fn_list(lt: list = []) -> list:`? What is the difference?

Treat these as **two different definitions** (you would not define both at the
same time in real code):

**Version 1  no default value (safe)**

```python
def fn_list(lt: list) -> list:
    lt.append(100)
    return lt


fn_list([1, 2, 3])  # caller MUST pass a list
```

- The caller **must** pass a list.
- No default list is created.
- No hidden shared state.

If you try:

```python
fn_list()  # ❌ Error
```

you get:

```text
TypeError: fn_list() missing 1 required positional argument: 'lt'
```

**Version 2  mutable default list (dangerous)**

```python
def fn_list(lt: list = []) -> list:
    lt.append(100)
    return lt


print(fn_list())  # [100]
print(fn_list())  # [100, 100]
print(fn_list())  # [100, 100, 100]
```

Here `lt` uses the **same list object** on every call where you omit the
argument. Python evaluates `lt = []` **once at function definition time**, so
each call reuses that list.

You can imagine:

```text
fn_list()
  lt ───► SAME LIST
fn_list()
  lt ───► SAME LIST
fn_list()
  lt ───► SAME LIST
```

This is why professional Python programmers **avoid** mutable defaults.

**Safe alternative  use `None` and create the list inside**

```python
def fn_list(lt: list | None = None) -> list:
    if lt is None:
        lt = []   # new list created EACH CALL
    lt.append(100)
    return lt


print(fn_list())  # [100]
print(fn_list())  # [100]
print(fn_list())  # [100]
```

Now each call that omits `lt` gets a **fresh**, independent list.

**Summary:**

- `def fn_list(lt: list)`  caller must provide a list → **safe**.
- `def fn_list(lt: list = [])`  shared mutable default list → **dangerous**.
- `def fn_list(lt: list | None = None)`  recommended pattern → **safe and flexible**.

---

### 4.3. "non-default argument follows default argument" SyntaxError

**File**: [`parameter_order.py`](parameter_order.py) – functions
`log_number_required_first` and `log_number_keyword_only`

Another rule Python enforces for defaults is:

> **You cannot put a required parameter after one with a default value (in the same parameter group).**

If you try this:

```python
from typing import Optional


def log_number(sl: Optional[int] = 10, nu: int) -> None:
    print(f"{sl} {nu}")
```

Python raises a **SyntaxError** at *definition time*:

```text
SyntaxError: non-default argument follows default argument
```

Why? Because `sl` has a **default value** (optional), while `nu` is **required**.
If this were allowed, a simple call like:

```python
log_number(100)
```

would be **ambiguous**:

- Should `100` be used for `sl` (and `nu` is missing)?
- Or should `100` be used for `nu` (and `sl` uses its default `10`)?

Python avoids this confusion by enforcing the rule: **all required parameters must come before optional ones within the same group.**

#### Option 1 – Put the required parameter first

The usual fix is simply to put `nu` (required) before `sl` (optional):

```python
from typing import Optional


def log_number(nu: int, sl: Optional[int] = 10) -> None:
    print(f"{sl} {nu}")


log_number(100)       # nu = 100, sl = 10 (default)
log_number(5, 20)     # nu = 5,   sl = 20
```

Now there is no ambiguity:

- The **first positional argument** always goes to `nu`.
- `sl` is clearly optional and can use its default if omitted.

#### Option 2 – Keep `sl` first using a keyword-only parameter

Sometimes, for readability, you might want to keep `sl` first but still have
`nu` as a required parameter. You can do this by making `nu` **keyword-only**:

```python
from typing import Optional


def log_number(sl: Optional[int] = 10, *, nu: int) -> None:
    print(f"{sl} {nu}")


log_number(nu=20)        # sl = 10 (default), nu = 20
log_number(5, nu=20)     # sl = 5,           nu = 20
```

Here:

- `sl` is a standard parameter with a default (optional, can be positional or keyword).
- `*` introduces the **keyword-only** section.
- `nu` is a **required keyword-only** parameter: it **must** be passed as `nu=...`.

Because `sl` and `nu` are now in **different parameter groups** (standard vs
keyword-only), Python can unambiguously bind calls and the definition is valid.

This example ties together three ideas:

- *Default values* (optional vs required)
- The `SyntaxError: non-default argument follows default argument`
- Using `*` to introduce **keyword-only** parameters to control how callers pass
  arguments

---

### 4.4. Mutable List Arguments and Aliasing (Why the Caller’s List Changes)

**File**: [`mutable_argument_aliasing.py`](mutable_argument_aliasing.py)

> For a direct comparison of `def fn_list(lt: list)` vs
> `def fn_list(lt: list = [])` and the `None`-default pattern, see section
> **4.2 – The Mutable Default Argument Pitfall** (fn_list comparison).

Consider this function and call:

```python
def fn_list(lt: list = []) -> list:
    lt[0] = 100
    lt[1] = 200
    lt[2] = 300

    for i in lt:
        print(f" i {i}")

    return lt


l = [1, 2, 3]
m = fn_list(l)
for i in l:
    print(f" i {i}")
```

Output:

```text
 i 100
 i 200
 i 300
 i 100
 i 200
 i 300
```

#### Why does modifying `lt` also modify `l`?

In Python, **variables hold references to objects**, not the objects themselves.

When you call:

```python
l = [1, 2, 3]
m = fn_list(l)
```

inside `fn_list`, the parameter `lt` becomes a **reference to the exact same
list object** as `l`. There is **no copy** made automatically:

```text
l  ───►  [1, 2, 3]  ◄───  lt
```

So when you do:

```python
lt[0] = 100
lt[1] = 200
lt[2] = 300
```

you are modifying the **same underlying list** that `l` refers to. That’s why
the caller sees `l == [100, 200, 300]` after the function call.

You can verify they are the same object using `id`:

```python
print(id(l))
print(id(lt))
```

This prints the same memory address → same object.

**Tiny demo – running `mutable_argument_aliasing.py`:**

```text
id(l) before: 4335860864
Inside fn_list (lt):
 i 100
 i 200
 i 300
id(m) after:  4335860864

Outside fn_list (l):
 i 100
 i 200
 i 300

Same object? True
```

Think of:

```python
lt = l
```

not as “make a copy”, but as **“give me another name for the same object.”**

#### How to prevent modifying the original list

If you want `fn_list` to **work on its own copy** and not change the caller’s
list, you must create a new list explicitly.

**Option 1 – Copy inside the function**

```python
def fn_list(lt: list) -> list:
    lt = lt.copy()  # or list(lt)

    lt[0] = 100
    lt[1] = 200
    lt[2] = 300

    return lt
```

Now:

```python
l = [1, 2, 3]
m = fn_list(l)

print(l)  # [1, 2, 3]
print(m)  # [100, 200, 300]
```

**Option 2 – Caller passes a copy explicitly**

```python
m = fn_list(l.copy())

# or using slices
m = fn_list(l[:])
```

In both cases, the function receives a **separate list object**, so changes
inside the function do not affect `l`.

#### Bonus: mutable default in `fn_list(lt: list = [])`

The original function also had a **mutable default**:

```python
def fn_list(lt: list = []) -> list:
    ...
```

This is dangerous for the same reason as in section **4.2**: Python creates the
default list **once** when the function is defined, so it would be **shared
across calls** if you ever rely on the default.

The safer pattern is:

```python
from typing import Optional


def fn_list(lt: Optional[list] = None) -> list:
    if lt is None:
        lt = []
    # modify lt here
    return lt
```

This way:

- Passing a list gives the function permission to modify that list.
- Omitting the argument creates a **fresh list** for each call.

**Key idea**: *Python uses references + mutable lists + call-by-object-reference*,
so passing a list into a function does **not** make a copy. If you want
independence, you must copy the list yourself.

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

| File | Description |
|------|-------------|
| [`positional_args.py`](positional_args.py) | Positional arguments and positional-only |
| [`keyword_args.py`](keyword_args.py) | Keyword arguments and keyword-only |
| [`default_values.py`](default_values.py) | Default values and mutable default pitfall |
| [`args_kwargs.py`](args_kwargs.py) | *args, **kwargs, and unpacking |
| [`parameter_order.py`](parameter_order.py) | Complete parameter order rules |

**Total**: 5 files

---

[← Back to Functions](../functions.md) | [Previous: Basics](../01_basics/) | [Next: Scope →](../03_scope/)


