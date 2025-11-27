"""
Example: Basic Decorators
Demonstrates function decorators, @syntax, and wrapping functions.

Key Concepts:
- Decorators are functions that modify other functions
- @decorator syntax is syntactic sugar
- Decorators wrap functions to add functionality
- Common use cases: logging, timing, validation

Important:
- Decorator is a callable that takes a function and returns a function
- @decorator is equivalent to: func = decorator(func)
- Decorators execute at function definition time
"""

from typing import Callable, Any
import time
from functools import wraps


# ============================================================================
# BASIC DECORATOR PATTERN
# ============================================================================

def simple_decorator(func: Callable) -> Callable:
    """
    Simplest decorator - wraps a function.
    
    Pattern:
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Before function call
                result = func(*args, **kwargs)
                # After function call
                return result
            return wrapper
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Before calling {func.__name__}")
        result = func(*args, **kwargs)  # ← Call original function
        print(f"After calling {func.__name__}")
        return result
    return wrapper  # ← Return wrapper function


# Using the decorator with @ syntax
@simple_decorator
def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"


# Equivalent to: greet = simple_decorator(greet)


# ============================================================================
# DECORATOR WITHOUT @ SYNTAX
# ============================================================================

def say_goodbye(name: str) -> str:
    """Say goodbye."""
    return f"Goodbye, {name}!"


# Manual decoration (without @)
say_goodbye = simple_decorator(say_goodbye)  # ← Same as @simple_decorator


# ============================================================================
# LOGGING DECORATOR
# ============================================================================

def log_calls(func: Callable) -> Callable:
    """
    Log function calls with arguments and return value.
    
    Useful for debugging and monitoring.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Log function call
        args_str = ", ".join(repr(arg) for arg in args)
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        
        print(f"Calling {func.__name__}({all_args})")
        
        # Call function
        result = func(*args, **kwargs)
        
        # Log return value
        print(f"{func.__name__} returned {result!r}")
        
        return result
    return wrapper


@log_calls
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@log_calls
def multiply(x: int, y: int, z: int = 1) -> int:
    """Multiply numbers."""
    return x * y * z


# ============================================================================
# TIMING DECORATOR
# ============================================================================

def timer(func: Callable) -> Callable:
    """
    Measure function execution time.
    
    Useful for performance monitoring.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()  # ← Start timer
        
        result = func(*args, **kwargs)
        
        end_time = time.time()  # ← End timer
        elapsed = end_time - start_time
        
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        
        return result
    return wrapper


@timer
def slow_function(n: int) -> int:
    """Simulate slow function."""
    time.sleep(0.1)  # Sleep for 100ms
    return n * 2


@timer
def fast_function(n: int) -> int:
    """Fast function."""
    return n * 2


# ============================================================================
# VALIDATION DECORATOR
# ============================================================================

def validate_positive(func: Callable) -> Callable:
    """
    Validate that all arguments are positive numbers.
    
    Raises ValueError if any argument is not positive.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Check all positional arguments
        for arg in args:
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(f"All arguments must be positive, got {arg}")
        
        # Check all keyword arguments
        for value in kwargs.values():
            if isinstance(value, (int, float)) and value <= 0:
                raise ValueError(f"All arguments must be positive, got {value}")
        
        return func(*args, **kwargs)
    return wrapper


@validate_positive
def calculate_area(width: float, height: float) -> float:
    """Calculate rectangle area (width and height must be positive)."""
    return width * height


@validate_positive
def calculate_volume(length: float, width: float, height: float) -> float:
    """Calculate box volume (all dimensions must be positive)."""
    return length * width * height


# ============================================================================
# CACHING DECORATOR (Memoization)
# ============================================================================

def cache(func: Callable) -> Callable:
    """
    Cache function results to avoid recomputation.

    Useful for expensive computations with repeated inputs.
    """
    cached_results = {}  # ← Store results

    def wrapper(*args: Any) -> Any:
        # Check if result is cached
        if args in cached_results:
            print(f"Cache hit for {func.__name__}{args}")
            return cached_results[args]

        # Compute and cache result
        print(f"Cache miss for {func.__name__}{args}")
        result = func(*args)
        cached_results[args] = result

        return result

    # Expose cache for inspection
    wrapper.cache = cached_results  # type: ignore

    return wrapper


@cache
def fibonacci(n: int) -> int:
    """Calculate Fibonacci number (with caching)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@cache
def expensive_computation(x: int, y: int) -> int:
    """Simulate expensive computation."""
    print(f"  Computing {x} + {y}...")
    time.sleep(0.1)  # Simulate work
    return x + y


# ============================================================================
# DECORATOR WITH METADATA PRESERVATION
# ============================================================================

def better_decorator(func: Callable) -> Callable:
    """
    Decorator that preserves function metadata using @wraps.

    Without @wraps:
        - func.__name__ becomes 'wrapper'
        - func.__doc__ is lost
        - func.__module__ is wrong

    With @wraps:
        - Original metadata is preserved
    """
    @wraps(func)  # ← Preserves metadata
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@better_decorator
def documented_function(x: int) -> int:
    """
    This is a well-documented function.

    Args:
        x: An integer

    Returns:
        The input multiplied by 2
    """
    return x * 2


# ============================================================================
# COMPARISON: With vs Without @wraps
# ============================================================================

def without_wraps(func: Callable) -> Callable:
    """Decorator without @wraps."""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return wrapper


def with_wraps(func: Callable) -> Callable:
    """Decorator with @wraps."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return wrapper


@without_wraps
def func_without_wraps() -> None:
    """Original docstring."""
    pass


@with_wraps
def func_with_wraps() -> None:
    """Original docstring."""
    pass


# ============================================================================
# MULTIPLE DECORATORS (STACKING)
# ============================================================================

@timer
@log_calls
def complex_operation(a: int, b: int) -> int:
    """
    Function with multiple decorators.

    Decorators are applied bottom-to-top:
    1. log_calls is applied first
    2. timer is applied second

    Equivalent to:
        complex_operation = timer(log_calls(complex_operation))
    """
    return a ** b


# ============================================================================
# DEMONSTRATION: Basic Decorators
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("BASIC DECORATORS")
    print("=" * 70)

    # ========================================================================
    # Simple Decorator
    # ========================================================================
    print("\n" + "=" * 70)
    print("1. SIMPLE DECORATOR")
    print("=" * 70)

    print("\nCalling greet('Alice'):")
    result = greet("Alice")
    print(f"Result: {result}")

    print("\nCalling say_goodbye('Bob'):")
    result = say_goodbye("Bob")
    print(f"Result: {result}")

    # ========================================================================
    # Logging Decorator
    # ========================================================================
    print("\n" + "=" * 70)
    print("2. LOGGING DECORATOR")
    print("=" * 70)

    print("\nCalling add(5, 3):")
    result = add(5, 3)

    print("\nCalling multiply(2, 3, z=4):")
    result = multiply(2, 3, z=4)

    # ========================================================================
    # Timing Decorator
    # ========================================================================
    print("\n" + "=" * 70)
    print("3. TIMING DECORATOR")
    print("=" * 70)

    print("\nCalling slow_function(10):")
    result = slow_function(10)
    print(f"Result: {result}")

    print("\nCalling fast_function(10):")
    result = fast_function(10)
    print(f"Result: {result}")

    # ========================================================================
    # Validation Decorator
    # ========================================================================
    print("\n" + "=" * 70)
    print("4. VALIDATION DECORATOR")
    print("=" * 70)

    print("\nCalling calculate_area(5.0, 3.0):")
    result = calculate_area(5.0, 3.0)
    print(f"Result: {result}")

    print("\nCalling calculate_area(-5.0, 3.0):")
    try:
        result = calculate_area(-5.0, 3.0)
    except ValueError as e:
        print(f"Error: {e}")

    # ========================================================================
    # Caching Decorator
    # ========================================================================
    print("\n" + "=" * 70)
    print("5. CACHING DECORATOR")
    print("=" * 70)

    print("\nCalculating fibonacci(5) twice:")
    print(f"First call: {fibonacci(5)}")
    print(f"Second call: {fibonacci(5)}")  # Uses cache

    print("\nCalculating expensive_computation(10, 20) twice:")
    print(f"First call: {expensive_computation(10, 20)}")
    print(f"Second call: {expensive_computation(10, 20)}")  # Uses cache

    # ========================================================================
    # Metadata Preservation
    # ========================================================================
    print("\n" + "=" * 70)
    print("6. METADATA PRESERVATION (@wraps)")
    print("=" * 70)

    print("\nWithout @wraps:")
    print(f"  Name: {func_without_wraps.__name__}")
    print(f"  Doc: {func_without_wraps.__doc__}")

    print("\nWith @wraps:")
    print(f"  Name: {func_with_wraps.__name__}")
    print(f"  Doc: {func_with_wraps.__doc__}")

    print("\nDocumented function:")
    print(f"  Name: {documented_function.__name__}")
    print(f"  Doc: {documented_function.__doc__}")

    # ========================================================================
    # Multiple Decorators
    # ========================================================================
    print("\n" + "=" * 70)
    print("7. MULTIPLE DECORATORS (STACKING)")
    print("=" * 70)

    print("\nCalling complex_operation(2, 10):")
    result = complex_operation(2, 10)
    print(f"Result: {result}")

    print("\n" + "=" * 70)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Decorators are functions that modify other functions")
    print("2. @decorator is syntactic sugar for: func = decorator(func)")
    print("3. Decorators execute at function definition time")
    print("4. Use *args, **kwargs to accept any arguments")
    print("5. Always use @wraps to preserve function metadata")
    print("6. Decorators can be stacked (applied bottom-to-top)")
    print("7. Common uses: logging, timing, validation, caching")
    print("8. Decorator pattern: wrapper function inside decorator")
    print("9. Return wrapper function from decorator")
    print("10. Call original function inside wrapper")
    print("=" * 70)

