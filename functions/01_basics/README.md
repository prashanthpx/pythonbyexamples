# Python Functions - Basics

[← Back to Functions](../functions.md) | [Next: Parameters →](../02_parameters/)

> **Level**: 🟢 Beginner  
> **Estimated Time**: 2 hours  
> **Prerequisites**: Basic Python syntax

---

## 📚 Table of Contents

1. [What is a Function?](#1-what-is-a-function)
2. [Defining Functions](#2-defining-functions)
3. [Calling Functions](#3-calling-functions)
4. [Return Values](#4-return-values)
5. [Docstrings](#5-docstrings)
6. [Function Structure](#6-function-structure)
7. [Summary](#7-summary)

---

## 1. What is a Function?

A **function** is a reusable block of code that performs a specific task. Functions help you:

- **Organize code**: Break complex problems into smaller pieces
- **Reuse code**: Write once, use many times
- **Maintain code**: Changes in one place affect all uses
- **Test code**: Easier to test small, focused functions

### Why Use Functions?

**Without functions** (repetitive code):
```python
# Calculate area of rectangle 1
area1 = 5 * 3
print(f"Area 1: {area1}")

# Calculate area of rectangle 2
area2 = 10 * 7
print(f"Area 2: {area2}")

# Calculate area of rectangle 3
area3 = 8 * 4
print(f"Area 3: {area3}")
```

**With functions** (clean, reusable):
```python
def calculate_area(length, width):
    return length * width

print(f"Area 1: {calculate_area(5, 3)}")
print(f"Area 2: {calculate_area(10, 7)}")
print(f"Area 3: {calculate_area(8, 4)}")
```

---

## 2. Defining Functions

**File**: [`defining_functions.py`](defining_functions.py)

### 2.1. Basic Function Definition

```python
def greet(name: str) -> str:
    """Greet a person by name."""
    message = f"Hello, {name}!"
    return message
```

### 🔑 Key Components

| Component | Example | Description |
|-----------|---------|-------------|
| **`def` keyword** | `def` | Starts function definition |
| **Function name** | `greet` | Descriptive name (snake_case) |
| **Parameters** | `name: str` | Input with type hint |
| **Return type** | `-> str` | What function returns |
| **Docstring** | `"""..."""` | Documentation |
| **Function body** | `message = ...` | Indented code block |
| **Return statement** | `return message` | Value to return |

### 2.2. Function with Multiple Parameters

**File**: [`defining_functions.py`](defining_functions.py) - Line 32

```python
def calculate_area(length: float, width: float) -> float:
    """
    Calculate the area of a rectangle.
    
    Args:
        length: Length of the rectangle
        width: Width of the rectangle
        
    Returns:
        Area as a float
    """
    return length * width
```

### ⚠️ Important Lines

**Line 32**: `def calculate_area(length: float, width: float) -> float:`
- Multiple parameters separated by commas
- `float` type hint accepts both `int` and `float` values
- Type hints are **not enforced** at runtime (they're for documentation and tools)

**Line 44**: `return length * width`
- Can return an expression directly
- No need to store in a variable first

### 💡 Nuances

1. **Type hints are optional but recommended**
   - Help IDEs provide better autocomplete
   - Make code self-documenting
   - Can be checked with tools like `mypy`

2. **Float annotations accept integers**
   ```python
   calculate_area(5, 3)      # Works! Ints are accepted
   calculate_area(5.0, 3.0)  # Also works
   ```

3. **Return can be implicit or explicit**
   ```python
   # Explicit (clear)
   result = length * width
   return result
   
   # Implicit (concise)
   return length * width
   ```

### 2.3. Function with No Return Value

**File**: [`defining_functions.py`](defining_functions.py) - Line 47

```python
def print_info(name: str, age: int) -> None:
    """Print user information to console."""
    print(f"{name} is {age} years old")
    # No return statement = implicit return None
```

### 🔑 Key Takeaways

- `-> None` indicates function doesn't return a value
- Functions without `return` automatically return `None`
- Use for functions with **side effects** (print, write files, modify data)

### 2.4. Function with No Parameters

**File**: [`defining_functions.py`](defining_functions.py) - Line 87

```python
def no_parameters() -> str:
    """Function with no parameters."""
    return "I don't need any input!"
```

### ⚠️ Important

- Empty parentheses `()` are **required** even with no parameters
- This is different from some languages where parentheses are optional

---

## 3. Calling Functions

**File**: [`calling_functions.py`](calling_functions.py)

### 3.1. Positional Arguments

Arguments are matched by **position** (order matters).

```python
def create_full_name(first: str, last: str, middle: str = "") -> str:
    if middle:
        return f"{first} {middle} {last}"
    return f"{first} {last}"

# Positional arguments
name = create_full_name("John", "Doe")  # first="John", last="Doe"
```

### ⚠️ Important

- **Order matters!** First argument goes to first parameter
- Must provide all required parameters
- Optional parameters (with defaults) can be omitted

### 3.2. Keyword Arguments

Arguments are matched by **name** (order doesn't matter).

```python
# Keyword arguments - order doesn't matter
name = create_full_name(last="Brown", first="Bob", middle="Lee")
# Result: "Bob Lee Brown"
```

### 🔑 Key Takeaway

Keyword arguments make code **more readable** and **less error-prone**.

### 3.3. Mixing Positional and Keyword Arguments

**File**: [`calling_functions.py`](calling_functions.py) - Line 91

```python
# Positional first, then keyword
name = create_full_name("Charlie", "Davis", middle="Ray")
# Result: "Charlie Ray Davis"
```

### ⚠️ Critical Rule

**Positional arguments MUST come before keyword arguments!**

```python
# ✅ Correct
create_full_name("Charlie", "Davis", middle="Ray")

# ❌ Error: positional argument follows keyword argument
create_full_name(first="Charlie", "Davis", "Ray")
```

### 3.4. Using Default Values

**File**: [`calling_functions.py`](calling_functions.py) - Line 99

```python
def power(base: float, exponent: float = 2.0) -> float:
    """Raise base to the power of exponent."""
    return base ** exponent

# Use default
square = power(5)  # exponent defaults to 2.0

# Override default
cube = power(5, 3)  # exponent = 3
```

### 💡 Nuance

Parameters with defaults can be omitted, but you can still override them when needed.

### 3.5. Storing vs Using Results Directly

**File**: [`calling_functions.py`](calling_functions.py) - Lines 111-125

```python
# Store result for later use
result = multiply(6, 7)
print(f"Result: {result}")

# Use result directly in expression
total = multiply(3, 4) + multiply(5, 6)

# Use in print statement
print(f"Direct: {multiply(8, 9)}")
```

### 3.6. Chaining Function Calls

**File**: [`calling_functions.py`](calling_functions.py) - Line 131

```python
# Pass result of one function to another
description = describe_person(
    name=create_full_name("Emma", "Wilson"),  # Inner function executes first
    age=28,
    city="Seattle"
)
```

### 🔑 Key Takeaway

Inner functions execute **first**, their results are passed to outer functions.

---

## 4. Return Values

**File**: [`return_values.py`](return_values.py)

### 4.1. Single Return Value

Most common pattern - return one value.

```python
def get_square(number: int) -> int:
    """Return the square of a number."""
    return number * number

result = get_square(5)  # result = 25
```

### 4.2. Multiple Return Values (Tuples)

**File**: [`return_values.py`](return_values.py) - Line 35

```python
def get_rectangle_properties(length: float, width: float) -> tuple[float, float, float]:
    """Calculate area, perimeter, and diagonal."""
    area = length * width
    perimeter = 2 * (length + width)
    diagonal = (length**2 + width**2) ** 0.5

    # Return multiple values (automatically creates a tuple)
    return area, perimeter, diagonal

# Unpack all values
area, perimeter, diagonal = get_rectangle_properties(5.0, 3.0)

# Or get as tuple
result = get_rectangle_properties(5.0, 3.0)  # result is a tuple
```

### 🔑 Key Takeaways

1. **Automatic tuple packing**: `return a, b, c` creates a tuple
2. **Tuple unpacking**: `x, y, z = function()` assigns each value
3. **Can get as tuple**: `result = function()` keeps it as tuple

### ⚠️ Important Line

**Line 50**: `return area, perimeter, diagonal`
- Python automatically packs multiple values into a tuple
- No need to write `return (area, perimeter, diagonal)`

### 4.3. Optional Return (None for Errors)

**File**: [`return_values.py`](return_values.py) - Line 56

```python
from typing import Optional

def divide_safely(a: float, b: float) -> Optional[float]:
    """Divide two numbers, return None if division by zero."""
    if b == 0:
        return None  # Early return for error case
    return a / b

# Use the function
result = divide_safely(10, 2)  # result = 5.0
error = divide_safely(10, 0)   # error = None

# Always check for None
if error is None:
    print("Division by zero!")
```

### 💡 Nuances

1. **Optional[float]** means "float or None"
   - Same as `float | None` in Python 3.10+
   - Indicates function might not return a value

2. **Early returns** exit function immediately
   - Rest of function doesn't execute
   - Useful for error handling

3. **Always check for None** before using result
   ```python
   result = divide_safely(10, 0)
   if result is not None:
       print(f"Result: {result}")
   ```

### 4.4. Conditional Returns

**File**: [`return_values.py`](return_values.py) - Line 78

```python
def get_grade(score: int) -> str:
    """Convert numeric score to letter grade."""
    if score >= 90:
        return "A"  # Exits immediately
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
```

### 🔑 Key Takeaway

**Only one return statement executes per function call**. Once a return is hit, the function exits immediately.

### 4.5. No Return Value (None)

**File**: [`return_values.py`](return_values.py) - Line 125

```python
def log_message(message: str) -> None:
    """Log a message (no return value)."""
    print(f"[LOG] {message}")
    # No return statement = implicit return None

result = log_message("Hello")  # result = None
```

### ⚠️ Important

- Functions without `return` automatically return `None`
- `-> None` annotation makes this explicit
- Use for functions with **side effects** (print, write, modify)

---

## 5. Docstrings

**File**: [`docstrings.py`](docstrings.py)

### 5.1. What are Docstrings?

**Docstrings** are documentation strings that describe what a function does. They:

- Are the **first statement** in a function
- Use **triple quotes**: `"""..."""`
- Can be accessed with `function.__doc__`
- Are displayed by the `help()` function

### 5.2. Simple Docstring (One-liner)

**File**: [`docstrings.py`](docstrings.py) - Line 14

```python
def simple_docstring(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"
```

### 🔑 Key Points

- Use for simple, obvious functions
- Still use triple quotes (even for one line)
- Should be a complete sentence

### 5.3. Detailed Docstring (Google Style)

**File**: [`docstrings.py`](docstrings.py) - Line 19

```python
def detailed_docstring(name: str, age: int, city: str = "Unknown") -> str:
    """
    Create a detailed person description.

    This function takes personal information and creates a formatted
    description string. It demonstrates a multi-line docstring with
    detailed parameter and return value documentation.

    Args:
        name: The person's full name
        age: The person's age in years (must be positive)
        city: The city where the person lives (default: "Unknown")

    Returns:
        A formatted string describing the person

    Raises:
        ValueError: If age is negative

    Example:
        >>> detailed_docstring("Alice", 30, "Seattle")
        'Alice (30) lives in Seattle'

    Note:
        This is the Google-style docstring format, which is widely used
        and supported by many documentation tools.
    """
    if age < 0:
        raise ValueError("Age cannot be negative")

    return f"{name} ({age}) lives in {city}"
```

### 📋 Google Style Sections

| Section | Purpose | Required? |
|---------|---------|-----------|
| **Summary** | Brief description | ✅ Yes |
| **Args** | Parameter descriptions | If has params |
| **Returns** | Return value description | If returns value |
| **Raises** | Exceptions that can be raised | If raises exceptions |
| **Example** | Usage examples | Recommended |
| **Note** | Additional information | Optional |

### 5.4. NumPy Style Docstring

**File**: [`docstrings.py`](docstrings.py) - Line 52

```python
def numpy_style_docstring(x: float, y: float) -> float:
    """
    Calculate the Euclidean distance between two points.

    This demonstrates NumPy-style docstring format.

    Parameters
    ----------
    x : float
        The x-coordinate
    y : float
        The y-coordinate

    Returns
    -------
    float
        The Euclidean distance from origin

    Examples
    --------
    >>> numpy_style_docstring(3.0, 4.0)
    5.0

    Notes
    -----
    Uses the formula: sqrt(x² + y²)
    """
    return (x**2 + y**2) ** 0.5
```

### 💡 When to Use Each Style

| Style | Best For | Used By |
|-------|----------|---------|
| **Google** | General Python projects | Google, many open-source projects |
| **NumPy** | Scientific/data projects | NumPy, SciPy, pandas |
| **reStructuredText** | Sphinx documentation | Django, Flask |

### 5.5. Accessing Docstrings

**File**: [`docstrings.py`](docstrings.py) - Lines 120-150

```python
# Access with __doc__ attribute
print(simple_docstring.__doc__)
# Output: "Return a greeting message."

# Use help() function
help(detailed_docstring)
# Shows formatted documentation

# Check if function has docstring
has_doc = simple_docstring.__doc__ is not None
```

### 🔑 Key Takeaways

1. **Always write docstrings** for public functions
2. **Choose a style** and be consistent
3. **Document parameters** and return values
4. **Include examples** when helpful
5. **Mention exceptions** that can be raised

### ⚠️ Best Practices

```python
# ✅ Good
def calculate_total(items: list[float]) -> float:
    """
    Calculate the total price of items.

    Args:
        items: List of item prices

    Returns:
        Total price as float
    """
    return sum(items)

# ❌ Bad (no docstring)
def calculate_total(items: list[float]) -> float:
    return sum(items)

# ❌ Bad (not descriptive)
def calculate_total(items: list[float]) -> float:
    """Calculate."""
    return sum(items)
```

---

## 6. Function Structure

**File**: [`function_structure.py`](function_structure.py)

### 6.1. Complete Anatomy of a Function

```python
def function_name(parameters) -> return_type:
    │      │           │              │
    │      │           │              └─ Return type annotation
    │      │           └──────────────── Parameters with type hints
    │      └──────────────────────────── Function name (snake_case)
    └─────────────────────────────────── 'def' keyword

    """Docstring describing the function."""

    # Function body (indented)
    result = some_computation()

    return result  # Return statement
```

### 6.2. Naming Conventions (PEP 8)

**File**: [`function_structure.py`](function_structure.py) - Lines 62-82

| Pattern | Example | Use For |
|---------|---------|---------|
| **snake_case** | `calculate_total_price()` | ✅ Functions |
| **Verb prefix** | `get_user_name()` | ✅ Action functions |
| **Boolean prefix** | `is_valid_email()` | ✅ Boolean functions |
| **PascalCase** | `MyFunction()` | ❌ Use for classes |
| **ALL_CAPS** | `CALCULATE()` | ❌ Use for constants |
| **Single letter** | `f()` | ❌ Not descriptive |

### 🔑 Naming Best Practices

```python
# ✅ Good: Descriptive, starts with verb
def calculate_total_price(items: list[float]) -> float:
    return sum(items)

# ✅ Good: Boolean function starts with 'is'
def is_valid_email(email: str) -> bool:
    return "@" in email

# ✅ Good: Action verb
def get_user_name() -> str:
    return "John Doe"

# ❌ Bad: Not descriptive
def calc(items):
    return sum(items)

# ❌ Bad: No verb
def total_price(items):
    return sum(items)
```

### 6.3. The `pass` Statement

**File**: [`function_structure.py`](function_structure.py) - Line 95

```python
def placeholder_function() -> None:
    """
    Function with pass statement.

    The 'pass' statement is a null operation - it does nothing.
    Used as a placeholder when you need a function body but
    haven't implemented it yet.
    """
    pass  # Placeholder for future implementation
```

### 💡 When to Use `pass`

- **During development**: Define API before implementation
- **Abstract methods**: Placeholder for subclasses to override
- **Empty blocks**: When syntax requires a statement but you have nothing to do

### 6.4. Function Attributes (Introspection)

**File**: [`function_structure.py`](function_structure.py) - Lines 125-135

Every function is an object with special attributes:

```python
def example_function(x: int, y: int = 5) -> int:
    """Example function."""
    return x + y

# Access function attributes
print(example_function.__name__)        # "example_function"
print(example_function.__doc__)         # "Example function."
print(example_function.__annotations__) # {'x': int, 'y': int, 'return': int}
print(example_function.__defaults__)    # (5,)
```

### 📋 Common Function Attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| `__name__` | Function name | `"example_function"` |
| `__doc__` | Docstring | `"Example function."` |
| `__annotations__` | Type hints | `{'x': int, 'return': int}` |
| `__defaults__` | Default values | `(5,)` |
| `__code__` | Code object | `<code object>` |

---

## 7. Summary

### 🎯 What You Learned

1. **Defining Functions**
   - Use `def` keyword
   - Add type annotations
   - Write docstrings
   - Return values

2. **Calling Functions**
   - Positional arguments (order matters)
   - Keyword arguments (order doesn't matter)
   - Mix both (positional first)
   - Use default values

3. **Return Values**
   - Single values
   - Multiple values (tuples)
   - Optional returns (None)
   - Conditional returns

4. **Documentation**
   - Write docstrings
   - Choose a style (Google, NumPy, reST)
   - Document parameters and returns
   - Include examples

5. **Best Practices**
   - Use snake_case names
   - Start with verbs
   - Add type hints
   - Write docstrings
   - Keep functions focused

### 📝 Quick Reference

```python
def function_name(param1: type1, param2: type2 = default) -> return_type:
    """
    Brief description.

    Args:
        param1: Description
        param2: Description (default: value)

    Returns:
        Description of return value
    """
    # Function body
    result = param1 + param2
    return result

# Call the function
value = function_name(10, 20)           # Positional
value = function_name(param1=10, param2=20)  # Keyword
value = function_name(10, param2=20)    # Mixed
```

### ✅ Checklist

Before moving to the next topic, make sure you can:

- [ ] Define a function with parameters and return type
- [ ] Call functions with positional and keyword arguments
- [ ] Return single and multiple values
- [ ] Write clear docstrings
- [ ] Use proper naming conventions
- [ ] Understand when to use `-> None`
- [ ] Access function attributes

### 🚀 Next Steps

Ready to learn more? Continue to:

- **[02. Parameters](../02_parameters/)** - Default values, *args, **kwargs
- **[03. Scope](../03_scope/)** - Variable scope and namespaces
- **[04. Advanced Features](../04_advanced_features/)** - Lambda, closures, type hints

---

### 📁 Files in This Section

| File | Description | Lines |
|------|-------------|-------|
| [`defining_functions.py`](defining_functions.py) | Basic function definitions | 161 |
| [`calling_functions.py`](calling_functions.py) | Different ways to call functions | 158 |
| [`return_values.py`](return_values.py) | Return value patterns | 273 |
| [`docstrings.py`](docstrings.py) | Documentation styles | 225 |
| [`function_structure.py`](function_structure.py) | Function anatomy and conventions | 289 |

**Total**: 5 files, 1,106 lines of code and documentation

---

[← Back to Functions](../functions.md) | [Next: Parameters →](../02_parameters/)


