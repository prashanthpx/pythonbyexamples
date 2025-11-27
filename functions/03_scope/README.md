# Python Functions - Scope and Namespaces

[← Back to Functions](../functions.md) | [Previous: Parameters](../02_parameters/) | [Next: Advanced Features →](../04_advanced_features/)

> **Level**: 🟡 Intermediate  
> **Estimated Time**: 2 hours  
> **Prerequisites**: [01. Basics](../01_basics/), [02. Parameters](../02_parameters/)

---

## 📚 Table of Contents

1. [Introduction to Scope](#1-introduction-to-scope)
2. [Local Scope](#2-local-scope)
3. [Global Scope](#3-global-scope)
4. [Nonlocal Scope](#4-nonlocal-scope)
5. [Enclosing Scope](#5-enclosing-scope)
6. [LEGB Rule](#6-legb-rule)
7. [Summary](#7-summary)

---

## 1. Introduction to Scope

**Scope** determines where a variable can be accessed in your code. Python has four types of scope:

| Scope | Description | Keyword | Lifetime |
|-------|-------------|---------|----------|
| **Local (L)** | Inside current function | None | During function call |
| **Enclosing (E)** | In outer function(s) | `nonlocal` | While closure exists |
| **Global (G)** | Module level | `global` | Program lifetime |
| **Built-in (B)** | Python built-ins | None | Always available |

### Why Scope Matters

```python
x = "global"

def my_function():
    x = "local"
    print(x)  # Which 'x'? Local!

my_function()  # Prints "local"
print(x)       # Prints "global"
```

Understanding scope prevents bugs and helps you write cleaner code.

---

## 2. Local Scope

**File**: [`local_scope.py`](local_scope.py)

### 2.1. Basic Local Scope

Variables created inside a function are **local** to that function:

```python
def my_function() -> str:
    message = "Hello"  # ← Local variable
    return message

result = my_function()
# print(message)  # ❌ NameError: 'message' not defined
```

### 🔑 Key Points

1. **Local variables** exist only during function execution
2. **Created fresh** each time the function is called
3. **Destroyed** when the function returns
4. **Cannot be accessed** from outside the function

### 2.2. No Block Scope in Python

**File**: [`local_scope.py`](local_scope.py) - Line 48

Unlike C/Java, Python has **no block scope**:

```python
def nested_blocks() -> str:
    if True:
        inside_if = "Created in if block"  # ← Still function-local!
    
    # ✅ Can still access 'inside_if' here
    for i in range(3):
        inside_loop = f"Loop {i}"  # ← Also function-local
    
    # ✅ Can still access 'inside_loop' and 'i' here
    return f"{inside_if}, {inside_loop}, i={i}"
```

### ⚠️ Important

Variables created in `if`, `for`, `while` blocks are **function-local**, not block-local. They remain accessible after the block ends.

### 2.3. Parameters Are Local

**File**: [`local_scope.py`](local_scope.py) - Line 72

Function parameters are local variables:

```python
def greet(name: str) -> str:  # 'name' is local
    name = name.upper()  # ← Only modifies local copy
    return f"Hello, {name}!"

original = "alice"
greet(original)
print(original)  # Still "alice" (unchanged)
```

### 2.4. Scope Lifetime

**File**: [`local_scope.py`](local_scope.py) - Line 119

Local variables don't persist between calls:

```python
def counter() -> int:
    count = 0  # ← Created fresh each call
    count += 1
    return count

counter()  # Returns 1
counter()  # Returns 1 (not 2!)
counter()  # Returns 1 (not 3!)
```

---

## 3. Global Scope

**File**: [`global_scope.py`](global_scope.py)

### 3.1. Reading Global Variables

Variables defined at module level are **global**:

```python
GLOBAL_CONSTANT = 100  # ← Global variable

def read_global() -> int:
    # ✅ Can read globals without special syntax
    return GLOBAL_CONSTANT
```

### 3.2. Modifying Global Variables

**File**: [`global_scope.py`](global_scope.py) - Line 35

Use the `global` keyword to modify globals:

```python
counter = 0  # ← Global

def increment_wrong():
    # ❌ This creates a LOCAL variable!
    counter = counter + 1  # UnboundLocalError

def increment_correct():
    global counter  # ← Declare we're using the global
    counter += 1    # ✅ Now modifies global
```

### ⚠️ Common Mistake

Without `global`, assignment creates a **new local variable** instead of modifying the global one!

### 3.3. Mutable Globals

**File**: [`global_scope.py`](global_scope.py) - Line 63

You can modify **contents** of mutable globals without `global`:

```python
global_list = []  # ← Global mutable object

def modify_contents():
    # ✅ Can modify contents without 'global'
    global_list.append("item")

def reassign():
    global global_list  # ← Need 'global' to reassign
    global_list = ["new", "list"]
```

### 🔑 Key Rule

- **Modifying contents**: No `global` needed (for lists, dicts, etc.)
- **Reassigning variable**: Need `global` keyword

### 3.4. Best Practices

**File**: [`global_scope.py`](global_scope.py) - Line 125

```python
# ✅ Good: Global constants (UPPERCASE)
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# ⚠️ Minimize: Mutable globals
app_state = {}  # Use sparingly

# ✅ Better: Pass as parameters
def process(data, config):  # Better than global config
    pass
```

---

## 4. Nonlocal Scope

**File**: [`nonlocal_scope.py`](nonlocal_scope.py)

### 4.1. What is Nonlocal?

`nonlocal` refers to variables in **enclosing function scope** (not global, not local):

```python
def outer():
    count = 0  # ← Enclosing scope for inner()
    
    def inner():
        nonlocal count  # ← Access enclosing scope
        count += 1
        return count
    
    return inner

counter = outer()
counter()  # 1
counter()  # 2
counter()  # 3
```

### 4.2. Nonlocal vs Global

**File**: [`nonlocal_scope.py`](nonlocal_scope.py) - Line 125

```python
global_var = 100  # ← Module level

def outer():
    enclosing_var = 200  # ← Enclosing scope
    
    def inner():
        nonlocal enclosing_var  # ← Refers to outer()'s variable
        global global_var       # ← Refers to module-level variable
        
        enclosing_var += 1
        global_var += 1
```

### 🔑 Key Difference

- `nonlocal`: Refers to **enclosing function** scope
- `global`: Refers to **module-level** scope

### 4.3. Closures and Nonlocal

**File**: [`nonlocal_scope.py`](nonlocal_scope.py) - Line 152

Common pattern for creating stateful functions:

```python
def create_counter(start: int = 0):
    count = start  # ← Enclosing scope (private state)
    
    def counter() -> int:
        nonlocal count
        count += 1
        return count
    
    return counter  # ← Return closure

counter1 = create_counter(0)
counter2 = create_counter(100)

counter1()  # 1
counter1()  # 2
counter2()  # 101 (independent state!)
```

### 💡 Use Cases

- Creating closures with state
- Factory functions
- Encapsulation (private variables)
- Decorators with state

---

## 5. Enclosing Scope

**File**: [`enclosing_scope.py`](enclosing_scope.py)

### 5.1. What is Enclosing Scope?

Enclosing scope is the scope of **outer functions** in nested function definitions:

```python
def outer():
    x = "enclosing"  # ← Enclosing scope for inner()
    
    def inner():
        print(x)  # ← Accesses enclosing scope
    
    inner()
```

### 5.2. Multiple Nesting Levels

**File**: [`enclosing_scope.py`](enclosing_scope.py) - Line 28

```python
def level1():
    var1 = "Level 1"  # ← Enclosing for level2 and level3
    
    def level2():
        var2 = "Level 2"  # ← Enclosing for level3
        
        def level3():
            # ← Can access both enclosing scopes
            print(f"{var1}, {var2}")
        
        level3()
    
    level2()
```

### 5.3. Closures Capture Enclosing Scope

**File**: [`enclosing_scope.py`](enclosing_scope.py) - Line 78

```python
def make_multiplier(n: int):
    # ← 'n' is in enclosing scope
    
    def multiply(x: int) -> int:
        return x * n  # ← Captures 'n'
    
    return multiply  # ← Returns closure

times3 = make_multiplier(3)
times5 = make_multiplier(5)

times3(10)  # 30
times5(10)  # 50
```

### 🔑 Key Point

Each closure has its **own independent** enclosing scope!

### 5.4. Shared Enclosing Scope

**File**: [`enclosing_scope.py`](enclosing_scope.py) - Line 119

Multiple functions can share the same enclosing scope:

```python
def create_account(balance: float = 0.0):
    # ← Shared enclosing scope (private state)

    def deposit(amount: float) -> float:
        nonlocal balance
        balance += amount
        return balance

    def withdraw(amount: float) -> float:
        nonlocal balance
        balance -= amount
        return balance

    def get_balance() -> float:
        return balance

    # ← All three functions share the same 'balance'
    return deposit, withdraw, get_balance

deposit, withdraw, balance = create_account(100.0)
deposit(50.0)   # 150.0
withdraw(30.0)  # 120.0
balance()       # 120.0
```

---

## 6. LEGB Rule

**File**: [`legb_rule.py`](legb_rule.py)

### 6.1. The LEGB Search Order

Python searches for variables in this order:

```
L → E → G → B
```

1. **L**ocal: Current function
2. **E**nclosing: Outer function(s)
3. **G**lobal: Module level
4. **B**uilt-in: Python built-ins

**First match wins!** Python stops searching once it finds the variable.

### 6.2. Visual Example

**File**: [`legb_rule.py`](legb_rule.py) - Line 27

```python
x = "GLOBAL"  # ← Global (G)

def outer():
    x = "ENCLOSING"  # ← Enclosing (E)

    def inner():
        x = "LOCAL"  # ← Local (L)
        print(x)  # Prints "LOCAL" (L wins)

    inner()

outer()
```

### 6.3. Scope Resolution Examples

**File**: [`legb_rule.py`](legb_rule.py) - Line 85

```python
name = "Global"  # ← Global scope

def demonstrate():
    # No local 'name'
    # No enclosing scope
    # Found in Global scope!
    return name  # Returns "Global"

def demonstrate_builtin():
    # 'len' not local, not enclosing, not global
    # Found in Built-in scope!
    return len([1, 2, 3])  # Returns 3
```

### 6.4. Variable Shadowing

**File**: [`legb_rule.py`](legb_rule.py) - Line 107

Variables in inner scopes **shadow** (hide) outer scopes:

```python
x = "GLOBAL"

def outer():
    x = "ENCLOSING"  # ← Shadows global

    def inner():
        x = "LOCAL"  # ← Shadows enclosing
        print(x)  # "LOCAL"

    inner()
    print(x)  # "ENCLOSING"

outer()
print(x)  # "GLOBAL"
```

### ⚠️ Avoid Shadowing Built-ins

**File**: [`legb_rule.py`](legb_rule.py) - Line 208

```python
# ❌ BAD: Shadowing built-in 'len'
def bad_example():
    len = "not a function"  # ← Shadows built-in!
    # len([1, 2, 3])  # TypeError!

# ✅ GOOD: Use different name
def good_example():
    length = "a string"
    result = len([1, 2, 3])  # ✅ Works fine
```

### 6.5. Complete LEGB Example

**File**: [`legb_rule.py`](legb_rule.py) - Line 100

```python
name = "Global"  # ← Global (G)

def outer():
    local_var = "Enclosing"  # ← Enclosing (E)

    def inner():
        inner_var = "Local"  # ← Local (L)

        return {
            "local": inner_var,      # L
            "enclosing": local_var,  # E
            "global": name,          # G
            "builtin": str(42)       # B (str is built-in)
        }

    return inner()
```

### 6.6. Modifying Different Scopes

**File**: [`legb_rule.py`](legb_rule.py) - Line 175

```python
global_var = "global"

def outer():
    enclosing_var = "enclosing"

    def inner():
        # Modify local (no keyword needed)
        local_var = "local"

        # Modify enclosing (need 'nonlocal')
        nonlocal enclosing_var
        enclosing_var = "modified"

        # Modify global (need 'global')
        global global_var
        global_var = "modified"
```

### 📋 Modification Summary

| Scope | Keyword | Example |
|-------|---------|---------|
| Local | None | `x = 10` |
| Enclosing | `nonlocal` | `nonlocal x; x = 10` |
| Global | `global` | `global x; x = 10` |
| Built-in | N/A | Cannot modify |

---

## 7. Summary

### 🎯 What You Learned

1. **Local Scope**
   - Variables in current function
   - Created fresh each call
   - No block scope in Python
   - Parameters are local

2. **Global Scope**
   - Module-level variables
   - Can read without keyword
   - Need `global` to modify
   - Minimize mutable globals

3. **Nonlocal Scope**
   - Variables in enclosing functions
   - Use `nonlocal` to modify
   - Common in closures
   - Different from global

4. **Enclosing Scope**
   - Scope of outer functions
   - Multiple nesting levels
   - Closures capture it
   - Can be shared

5. **LEGB Rule**
   - Search order: L → E → G → B
   - First match wins
   - Inner scopes shadow outer
   - Avoid shadowing built-ins

### 📝 Quick Reference

```python
# LEGB Example
x = "GLOBAL"  # G

def outer():
    x = "ENCLOSING"  # E

    def inner():
        x = "LOCAL"  # L

        # Access different scopes:
        local_x = x                    # L
        enclosing_x = outer.__code__.co_freevars  # E (advanced)
        global_x = globals()['x']      # G (explicit)
        builtin_len = len              # B

        # Modify different scopes:
        x = "new local"                # L (no keyword)

        nonlocal x                     # E (need nonlocal)
        x = "new enclosing"

        global x                       # G (need global)
        x = "new global"
```

### ✅ Checklist

Before moving to the next topic, make sure you can:

- [ ] Explain the four types of scope (L, E, G, B)
- [ ] Understand local scope and lifetime
- [ ] Know that Python has no block scope
- [ ] Use `global` keyword to modify global variables
- [ ] Use `nonlocal` keyword to modify enclosing variables
- [ ] Explain the difference between `global` and `nonlocal`
- [ ] Understand the LEGB search order
- [ ] Recognize variable shadowing
- [ ] Create closures that capture enclosing scope
- [ ] Avoid shadowing built-in names

### 🚀 Next Steps

Ready to learn more? Continue to:

- **[04. Advanced Features](../04_advanced_features/)** - Lambda, closures, type hints
- **[05. Functional Programming](../05_functional_programming/)** - Higher-order functions
- **[06. Decorators](../06_decorators/)** - Decorator patterns

### 💡 Common Patterns

**Pattern 1: Counter with Closure**
```python
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter
```

**Pattern 2: Private State**
```python
def create_object(initial_value):
    _private = initial_value

    def get():
        return _private

    def set(value):
        nonlocal _private
        _private = value

    return get, set
```

**Pattern 3: Configuration**
```python
# Global configuration
CONFIG = {"debug": False, "timeout": 30}

def get_config(key):
    return CONFIG.get(key)

def set_config(key, value):
    global CONFIG
    CONFIG[key] = value
```

---

### 📁 Files in This Section

| File | Description | Lines |
|------|-------------|-------|
| [`local_scope.py`](local_scope.py) | Local scope and lifetime | 278 |
| [`global_scope.py`](global_scope.py) | Global variables and modification | 298 |
| [`nonlocal_scope.py`](nonlocal_scope.py) | Nonlocal scope and closures | 349 |
| [`enclosing_scope.py`](enclosing_scope.py) | Enclosing scope in nested functions | 378 |
| [`legb_rule.py`](legb_rule.py) | LEGB scope resolution order | 419 |

**Total**: 5 files, 1,722 lines of code and documentation

---

[← Back to Functions](../functions.md) | [Previous: Parameters](../02_parameters/) | [Next: Advanced Features →](../04_advanced_features/)


