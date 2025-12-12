# Python Functions - Complete Learning Guide

> **Master Python functions from beginner to advanced level**

---

## 📖 About This Guide

This comprehensive guide covers everything you need to know about Python functions, from basic definitions to advanced topics like decorators, generators, and async functions. Each topic is in its own folder with:

- **Detailed documentation** (README.md)
- **Runnable Python examples** (one file per concept)
- **Type annotations** throughout
- **Best practices** and common pitfalls
- **Real-world examples**

---

## 🗺️ Learning Path

Follow these topics in order for a structured learning experience:

### 🟢 Beginner Level

#### [01. Basics](01_basics/)
**Estimated Time**: 2 hours  
**Status**: ✅ Complete

Learn the fundamentals of Python functions:
- Defining and calling functions
- Parameters and return values
- Type annotations
- Docstrings and documentation
- Function structure and naming conventions

**Files**: 5 Python examples, 1,106 lines of code

---

### 🟡 Intermediate Level

#### [02. Parameters](02_parameters/)
**Estimated Time**: 2.5 hours
**Status**: ✅ Complete

Master different parameter types:
- Positional and keyword arguments
- Default parameter values
- Variable arguments (*args)
- Keyword arguments (**kwargs)
- Keyword-only parameters
- Parameter order rules

**Quick beginner summary: `*args` and `**kwargs`**

When you see `*args` and `**kwargs` in a function definition:

- `*args` means: "accept **any number of extra positional arguments**" → inside
  the function, `args` is a **tuple**.
- `**kwargs` means: "accept **any number of extra keyword arguments**" → inside
  the function, `kwargs` is a **dict**.

Simple `*args` example (sum any number of numbers):

<augment_code_snippet path="functions/02_parameters/args_kwargs.py" mode="EXCERPT">
````python
def sum_numbers(*args: int) -> int:
    total = 0
    for num in args:
        total += num
    return total

sum_numbers(1, 2, 3, 4)  # 10
````
</augment_code_snippet>

Simple `**kwargs` example (collect options into a dict):

<augment_code_snippet path="functions/02_parameters/args_kwargs.py" mode="EXCERPT">
````python
from typing import Any


def print_info(**kwargs: Any) -> None:
    for key, value in kwargs.items():
        print(f"{key} = {value}")

print_info(name="Alice", age=25)
````
</augment_code_snippet>

Common real-world uses:

- Writing **flexible functions** like `print()` that take any number of
  arguments.
- **Forwarding arguments** in wrappers/decorators:
  `inner(*args, **kwargs)` calls the wrapped function with whatever it
  received.
- Building APIs that accept many optional settings via `**kwargs` while still
  having a small fixed set of required parameters.
- Allowing base class `__init__` methods to stay generic while subclasses add
  extra parameters using `*args` / `**kwargs`.

**What does `*` mean in a function parameter list? (keyword-only marker)**

When you write a bare `*` in the parameter list:

- **All parameters after `*` must be passed as keyword arguments only.**
- This is called the **keyword-only argument marker**.

Tiny example:

<augment_code_snippet mode="EXCERPT">
````python
def test(a, *, x, y=10):
    print(a, x, y)


test(1, x=5, y=20)  # OK
test(1, 5, 20)      # ❌ ERROR — x and y must be keyword arguments
````
</augment_code_snippet>

The `*` prevents calls like `test(1, 5, 20)` from accidentally treating `x`
and `y` as positional arguments. Callers must spell them out as keywords.

**Files**: 5 Python examples, 1,424 lines of code

---

#### [03. Scope and Namespaces](03_scope/)
**Estimated Time**: 2 hours
**Status**: ✅ Complete

Understand variable scope:
- Local scope
- Global scope
- Nonlocal scope
- Enclosing scope
- LEGB rule
- Global and nonlocal keywords

**Files**: 5 Python examples, 1,722 lines of code

---

#### [04. Advanced Features](04_advanced_features/)
**Estimated Time**: 3 hours
**Status**: ✅ Complete

Explore advanced function features:
- Lambda functions (anonymous functions)
- Closures and nested functions
- Advanced type hints (Union, Optional, Callable)
- Function annotations
- Partial functions
- List and Optional basics (beginner guide)

**Quick beginner summary: `Callable` (function type hints)**

Python already lets you **pass functions to other functions**. `Callable` is
just the **type hint** that says “this parameter is a function with this
signature”.

- Go: `f func(int) int`
- Python: `f: Callable[[int], int]`

Basic example – pass a function as a parameter:

<augment_code_snippet mode="EXCERPT">
````python
from typing import Callable


def apply(f: Callable[[int], int], x: int) -> int:
    return f(x)


def double(n: int) -> int:
    return n * 2


print(apply(double, 5))  # 10
````
</augment_code_snippet>

Here `f: Callable[[int], int]` means: *a function that takes one `int` and
returns an `int`* – exactly like `func(int) int` in Go.

`Callable[[A, B], R]` in general means: **a function taking `(A, B)` and
returning `R`**, e.g. `Callable[[int, str], bool]` ≈ `func(int, string) bool`.

For more advanced cases, you can keep the parameter list flexible using
`ParamSpec` and still forward arguments safely:

<augment_code_snippet mode="EXCERPT">
````python
from typing import Callable, ParamSpec


P = ParamSpec("P")


def wait_until_true(
    condition: Callable[P, bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> None:
    if condition(*args, **kwargs):
        print("Condition is True!")
    else:
        print("Condition is False!")
````
</augment_code_snippet>

Key ideas:

- `Callable[P, bool]` – **a function that takes some parameters `P` and
  returns `bool`.**
- `P = ParamSpec("P")` – a *type-level* “parameter list” that can be reused.
- `*args: P.args, **kwargs: P.kwargs` – this helper accepts **whatever
  positional and keyword arguments** the `condition` function needs and
  forwards them with `condition(*args, **kwargs)`.

This is the Python equivalent of a Go helper like:

- Go: `func waitUntil(cond func(args...) bool, args ...T) { ... }`
- Python: `def wait_until_true(condition: Callable[P, bool], *args, **kwargs): ...`

Another generic helper: **`call_twice`**

Sometimes you want a helper that calls any function **twice** with the same
arguments and returns both results. `Callable[P, R]` plus `ParamSpec` and
`TypeVar` let you type this precisely:

<augment_code_snippet mode="EXCERPT">
````python
from typing import Callable, ParamSpec, TypeVar


P = ParamSpec("P")
R = TypeVar("R")


def call_twice(
    f: Callable[P, R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> tuple[R, R]:
    return f(*args, **kwargs), f(*args, **kwargs)


def greet(name: str, punctuation: str = "!") -> str:
    return f"Hello, {name}{punctuation}"


print(call_twice(greet, "Prashanth", punctuation="!"))
````
</augment_code_snippet>

Here:

- `f` is just like the earlier `double` or the `condition` function in
  `wait_until_true`.
- `*args` / `**kwargs` are **forwarded** directly to `f` twice.
- `ParamSpec P` keeps the **parameter types** consistent between
  `Callable[P, R]` and `*args: P.args, **kwargs: P.kwargs`.
- `TypeVar R` captures the **return type** so the result is a
  `tuple[R, R]`.

Key takeaways for `Callable[P, R]` and `ParamSpec P`:

- `Callable[P, bool]` means: **"a function that takes some parameters `P` and
  returns `bool`"**.
- A helper like `_wait_until` or `wait_until_true` **does pass arguments to
  `condition`** via `*args` and `**kwargs` → `condition(*args, **kwargs)`.
- Your `math(double, 10)` example is equivalent in shape to calling a
  `_wait_until(condition, *args)` helper with
  `condition = double`, `args = (10,)`.
- The use of `ParamSpec P` is **for type checking**; at runtime these behave
  like normal `*args` / `**kwargs`.

Timeout-based `wait_until` example (more realistic):

<augment_code_snippet mode="EXCERPT">
````python
from typing import Callable, ParamSpec
import time


P = ParamSpec("P")


def wait_until(
    condition: Callable[P, bool],
    timeout_sec: float,
    *args: P.args,
    **kwargs: P.kwargs,
) -> None:
    print(f"Waiting up to {timeout_sec} seconds...")
    end = time.time() + timeout_sec
    while time.time() < end:
        if condition(*args, **kwargs):
            print("Condition became True")
            return
        print("Condition still False, sleeping...")
        time.sleep(1)
    raise TimeoutError("Condition did not become True in time")


def is_even_after_increment(n: int, increments: int) -> bool:
    return (n + increments) % 2 == 0


wait_until(is_even_after_increment, 5, 3, increments=1)
````
</augment_code_snippet>

Here again, `condition` is any function returning `bool`, and `*args` / `**kwargs`
are forwarded. The call

- `wait_until(is_even_after_increment, 5, 3, increments=1)`

follows the same idea as `math(double, 10)`: pass a function plus its
arguments into a generic helper.

Step-by-step argument binding for this call:

- `condition = is_even_after_increment`
- `timeout_sec = 5`
- `args = (3,)`
- `kwargs = {"increments": 1}`

Then the helper does `condition(*args, **kwargs)`, which becomes:

- `condition(*(3,), **{"increments": 1})`
- → `is_even_after_increment(3, increments=1)`

So even though you see **three** values after the function (`5, 3, increments=1`),
only **two** of them (`3` and `increments=1`) are forwarded into the condition;
`5` is consumed by the wrapper's own `timeout_sec` parameter.

This is why helpers like `_wait_until` / `wait_until` are written very
carefully to only call:

- `condition(*args, **kwargs)`

and **not** something like:

- `condition(timeout_sec, *args, **kwargs)` (which would force the condition
  to accept a spurious extra parameter).

What does `P` really represent here?

- `P = ParamSpec("P")` is a **type-level description of the parameter list**
  of the `condition` function.
- `Callable[P, bool]` says "a function taking parameters `P` and returning
  `bool`".
- `*args: P.args, **kwargs: P.kwargs` says "this helper also accepts those
  same parameters and forwards them to `condition`".

At runtime, `P` does **nothing** – it exists purely for static type checkers
(`mypy`, `pyright`, IDEs). The caller of `wait_until` never "sees" or passes
`P`; it is only there so tools can verify that the arguments you pass match
what `condition` expects.

### Wrapper using `Any` vs using `ParamSpec P`

A common pattern in real code is to use a strongly-typed core helper and a
thinner, more flexible wrapper. For example (simplified):

<augment_code_snippet mode="EXCERPT">
````python
from typing import Any, Callable, ParamSpec


P = ParamSpec("P")


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
        condition: Callable[P, bool],
        action: str,
        timeout_sec: float | None = None,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        ...
````
</augment_code_snippet>

- `_wait_until` uses `Callable[P, bool]` and `*args: P.args, **kwargs: P.kwargs`
  to keep the **relationship** between `condition` and its arguments precise.
- `wait_until_running` is just a **public wrapper** that forwards whatever
  arguments the caller gives; using `Any` here keeps the method signature
  simpler and avoids some edge-cases with generic methods on classes.
- You *could* make `wait_until_running` generic over the same `P`, but many
  codebases choose the pragmatic approach: **strict typing in the core helper,
  simpler `Any` in the thin wrapper**.

When calling such helpers, Python always processes arguments in this order:

1. Positional arguments (`f(1, 2)`)
2. Expanded `*args` (`f(1, *args)`)
3. Keyword arguments (`f(a=1)`)
4. Expanded `**kwargs` (`f(a=1, **kwargs)`)

Example of how `*args` and `**kwargs` expand:

<augment_code_snippet mode="EXCERPT">
````python
def test(a, b, c, x=None, y=None, z=None):
    print(a, b, c, x, y, z)


args = (2, 3)
kwargs = {"y": 20, "z": 30}


test(1, *args, x=10, **kwargs)
# Python sees: test(1, 2, 3, x=10, y=20, z=30)
````
</augment_code_snippet>

Putting it together:

- **Callable** = “this argument is a function (with this parameter/return
  type)”.
- It’s the Python type-hint equivalent of Go’s **function types**.

**Files**: 4 Python examples, 2,400 lines of code

---

### 🔴 Advanced Level

#### [05. Functional Programming](05_functional_programming/)
**Estimated Time**: 3 hours
**Status**: ✅ Complete

Learn functional programming concepts:
- Functions as first-class objects
- Higher-order functions
- map(), filter(), reduce()
- List comprehensions vs functions
- Pure functions and side effects

**Files**: 3 Python examples, 1,929 lines of code

---

#### [06. Decorators](06_decorators/)
**Estimated Time**: 3.5 hours
**Status**: ✅ Complete

Master function decorators:
- What are decorators?
- Creating simple decorators
- Decorators with arguments
- Class decorators
- Built-in decorators (@property, @staticmethod, @classmethod)
- Decorator chaining

**Files**: 3 Python examples, 1,592 lines of code
- functools.wraps

---

#### [07. Generators and Iterators](07_generators/)
**Estimated Time**: 3 hours
**Status**: ✅ Complete

Understand generators:
- Generator functions (yield)
- Generator expressions
- Iterators and iterables
- yield from
- Infinite generators
- Generator pipelines

**Files**: 3 Python examples, 1,398 lines of code

---

#### [08. Advanced Topics](08_advanced_topics/)
**Estimated Time**: 4 hours
**Status**: ✅ Complete

Dive into advanced concepts:
- Recursion and tail recursion
- Binary search and tree traversal
- Async functions (async/await)
- Concurrent execution with asyncio
- Partial application (functools.partial)
- Memoization and caching (@lru_cache, @cache)

**Files**: 3 Python examples, 1,437 lines of code

---

## 📊 Progress Tracker

| Topic | Level | Status | Files | Estimated Time |
|-------|-------|--------|-------|----------------|
| [01. Basics](01_basics/) | 🟢 Beginner | ✅ Complete | 5 | 2 hours |
| [02. Parameters](02_parameters/) | 🟡 Intermediate | ✅ Complete | 5 | 2.5 hours |
| [03. Scope](03_scope/) | 🟡 Intermediate | ✅ Complete | 5 | 2 hours |
| [04. Advanced Features](04_advanced_features/) | 🔴 Advanced | ✅ Complete | 4 | 3 hours |
| [05. Functional Programming](05_functional_programming/) | 🔴 Advanced | ✅ Complete | 3 | 3 hours |
| [06. Decorators](06_decorators/) | 🔴 Advanced | ✅ Complete | 3 | 3.5 hours |
| [07. Generators](07_generators/) | 🔴 Advanced | ✅ Complete | 3 | 3 hours |
| [08. Advanced Topics](08_advanced_topics/) | 🔴 Advanced | ✅ Complete | 3 | 4 hours |

**Total Estimated Time**: ~23 hours
**Completion**: 🎉 **100% Complete!**

---

## 🚀 Quick Start

### Option 1: Sequential Learning (Recommended)

Start from the beginning and work through each topic:

```bash
cd functions/01_basics
python3 defining_functions.py
python3 calling_functions.py
# ... continue with other examples
```

### Option 2: Jump to Specific Topic

If you're already familiar with basics:

```bash
cd functions/03_scope
# Read README.md first, then run examples
```

---

## 📝 How to Use This Guide

1. **Read the README.md** in each folder first
2. **Run the Python examples** to see concepts in action
3. **Experiment** - modify the code and see what happens
4. **Complete the checklist** at the end of each section

---

## 💡 Learning Tips

### For Beginners
- Don't skip the basics - they're the foundation
- Run every example and observe the output
- Try modifying examples before moving on
- Write your own functions to practice

### For Intermediate Learners
- Focus on understanding *why*, not just *how*
- Pay attention to nuances and edge cases
- Compare different approaches
- Think about when to use each pattern

### For Advanced Learners
- Study the implementation details
- Consider performance implications
- Explore the Python documentation
- Look at real-world code examples

---

## 🎯 What You'll Learn

By completing this guide, you will be able to:

✅ Write clean, well-documented functions
✅ Use type annotations effectively
✅ Handle different parameter types (*args, **kwargs)
✅ Understand and apply scope rules
✅ Create and use decorators
✅ Work with generators and iterators
✅ Write functional-style Python code
✅ Use async functions for concurrent programming
✅ Apply best practices and design patterns

---

## 📚 Additional Resources

### Official Documentation
- [Python Functions Tutorial](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)

### Recommended Reading
- "Fluent Python" by Luciano Ramalho
- "Effective Python" by Brett Slatkin
- "Python Cookbook" by David Beazley

---

## 🗂️ Repository Structure

```
functions/
├── README.md                          # This file
│
├── 01_basics/                         # ✅ Complete
│   ├── README.md
│   ├── defining_functions.py
│   ├── calling_functions.py
│   ├── return_values.py
│   ├── docstrings.py
│   └── function_structure.py
│
├── 02_parameters/                     # ✅ Complete
│   ├── README.md
│   ├── positional_args.py
│   ├── keyword_args.py
│   ├── default_values.py
│   ├── args_kwargs.py
│   └── parameter_order.py
│
├── 03_scope/                          # ✅ Complete
│   ├── README.md
│   ├── local_scope.py
│   ├── global_scope.py
│   ├── nonlocal_scope.py
│   ├── enclosing_scope.py
│   └── legb_rule.py
│
├── 04_advanced_features/              # ✅ Complete
│   ├── README.md
│   ├── lambda_functions.py
│   ├── closures.py
│   ├── type_hints.py
│   └── list_optional_basics.py
│
├── 05_functional_programming/         # ✅ Complete
│   ├── README.md
│   ├── higher_order_functions.py
│   ├── map_filter_reduce.py
│   └── function_composition.py
│
├── 06_decorators/                     # ✅ Complete
│   ├── README.md
│   ├── basic_decorators.py
│   ├── decorator_arguments.py
│   └── class_decorators.py
│
├── 07_generators/                     # ✅ Complete
│   ├── README.md
│   ├── basic_generators.py
│   ├── generator_expressions.py
│   └── advanced_patterns.py
│
└── 08_advanced_topics/                # ✅ Complete
    ├── README.md
    ├── recursion.py
    ├── async_and_partial.py
    └── memoization.py
```

---

## 🤝 Contributing

Found an error or have a suggestion? Feel free to:
- Report issues
- Suggest improvements
- Add more examples
- Fix typos

---

## 📄 License

This learning guide is provided as-is for educational purposes.

---

## 🎓 Prerequisites

Before starting this guide, you should be familiar with:
- Basic Python syntax (variables, data types, operators)
- Control flow (if/else, loops)
- Basic data structures (lists, dictionaries)

If you're new to Python, consider starting with a Python basics tutorial first.

---

## ✨ Features of This Guide

- ✅ **Every example is runnable** - No pseudocode, all real Python
- ✅ **Type annotations throughout** - Modern Python best practices
- ✅ **Detailed explanations** - Line-by-line breakdowns
- ✅ **Key takeaways** - Important concepts highlighted
- ✅ **Nuances explained** - Subtle details that matter
- ✅ **Best practices** - Professional coding standards
- ✅ **Common pitfalls** - Mistakes to avoid
- ✅ **Real-world examples** - Practical use cases

---

**Ready to start?** → [Begin with 01. Basics](01_basics/)

---

## 🎉 Completion Summary

### 📊 Final Statistics

| Metric | Count |
|--------|-------|
| **Total Topics** | 8 |
| **Total Python Files** | 31 |
| **Total Lines of Code** | ~12,500+ |
| **Total Documentation** | ~5,500+ lines |
| **Completion Status** | 100% ✅ |

### 📁 Files by Topic

| Topic | Python Files | Lines of Code |
|-------|--------------|---------------|
| 01. Basics | 5 | 1,106 |
| 02. Parameters | 5 | 1,204 |
| 03. Scope | 5 | 1,608 |
| 04. Advanced Features | 4 | 2,400 |
| 05. Functional Programming | 3 | 1,925 |
| 06. Decorators | 3 | 1,592 |
| 07. Generators | 3 | 1,398 |
| 08. Advanced Topics | 3 | 1,437 |
| **Total** | **31** | **~12,670** |

### 🎯 What You've Mastered

After completing this guide, you now understand:

✅ **Fundamentals**: Function definition, parameters, return values
✅ **Parameters**: Positional, keyword, *args, **kwargs, defaults
✅ **Scope**: LEGB rule, global, nonlocal, closures
✅ **Advanced Features**: Lambda, type hints, List, Optional
✅ **Functional Programming**: map, filter, reduce, composition
✅ **Decorators**: Basic, with arguments, class decorators
✅ **Generators**: yield, generator expressions, pipelines
✅ **Advanced Topics**: Recursion, async/await, partial, memoization

### 🚀 Next Steps

Now that you've mastered Python functions, consider exploring:

1. **Object-Oriented Programming** - Classes, inheritance, polymorphism
2. **Design Patterns** - Common software design patterns in Python
3. **Testing** - pytest, unit testing, test-driven development
4. **Performance** - Profiling, optimization techniques
5. **Concurrency** - Threading, multiprocessing, asyncio deep dive

---

**Last Updated**: 2025-11-24
**Python Version**: 3.8+
**Status**: 🎉 **Complete!**

