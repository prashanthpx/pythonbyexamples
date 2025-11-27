"""
Example: Decorators with Arguments
Demonstrates decorator factories and parameterized decorators.

Key Concepts:
- Decorator factories create decorators with custom parameters
- Three levels of nesting: factory -> decorator -> wrapper
- Allows customization of decorator behavior
- Common pattern for configurable decorators

Pattern:
    def decorator_factory(param):
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Use param, func, args, kwargs
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    @decorator_factory(value)
    def my_func():
        pass
"""

from typing import Callable, Any, Optional
import time
from functools import wraps


# ============================================================================
# BASIC DECORATOR FACTORY
# ============================================================================

def repeat(times: int) -> Callable:
    """
    Decorator factory that repeats function execution.
    
    Args:
        times: Number of times to repeat
        
    Returns:
        Decorator function
        
    Usage:
        @repeat(3)
        def greet():
            print("Hello!")
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = None
            for i in range(times):  # ← Use 'times' from outer scope
                print(f"Execution {i + 1}/{times}")
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator  # ← Return decorator


@repeat(3)
def greet(name: str) -> str:
    """Greet someone (repeated 3 times)."""
    message = f"Hello, {name}!"
    print(message)
    return message


@repeat(5)
def count(n: int) -> None:
    """Count (repeated 5 times)."""
    print(f"Count: {n}")


# ============================================================================
# LOGGING WITH CUSTOM PREFIX
# ============================================================================

def log_with_prefix(prefix: str = "LOG") -> Callable:
    """
    Decorator factory for logging with custom prefix.
    
    Args:
        prefix: Prefix for log messages
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"[{prefix}] Calling {func.__name__}")  # ← Use prefix
            result = func(*args, **kwargs)
            print(f"[{prefix}] {func.__name__} returned {result!r}")
            return result
        return wrapper
    return decorator


@log_with_prefix("INFO")
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@log_with_prefix("DEBUG")
def multiply(x: int, y: int) -> int:
    """Multiply two numbers."""
    return x * y


@log_with_prefix()  # ← Use default prefix
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b


# ============================================================================
# RETRY DECORATOR WITH CONFIGURABLE ATTEMPTS
# ============================================================================

def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """
    Decorator factory for retrying failed function calls.
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Delay between attempts (seconds)
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"Attempt {attempt}/{max_attempts}")
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"  Failed: {e}")
                    
                    if attempt < max_attempts:
                        print(f"  Retrying in {delay} seconds...")
                        time.sleep(delay)
            
            # All attempts failed
            print(f"All {max_attempts} attempts failed")
            raise last_exception  # type: ignore
        
        return wrapper
    return decorator


# Simulated unreliable function
_call_count = 0

@retry(max_attempts=3, delay=0.5)
def unreliable_function() -> str:
    """Function that fails first 2 times."""
    global _call_count
    _call_count += 1
    
    if _call_count < 3:
        raise ValueError(f"Simulated failure #{_call_count}")
    
    return "Success!"


# ============================================================================
# RATE LIMITING DECORATOR
# ============================================================================

def rate_limit(calls_per_second: float) -> Callable:
    """
    Decorator factory for rate limiting function calls.

    Args:
        calls_per_second: Maximum calls per second

    Returns:
        Decorator function
    """
    min_interval = 1.0 / calls_per_second  # ← Calculate minimum interval

    def decorator(func: Callable) -> Callable:
        last_called = [0.0]  # ← Mutable to modify in wrapper

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Calculate time since last call
            elapsed = time.time() - last_called[0]

            # Wait if necessary
            if elapsed < min_interval:
                sleep_time = min_interval - elapsed
                print(f"Rate limiting: sleeping {sleep_time:.3f}s")
                time.sleep(sleep_time)

            # Update last called time
            last_called[0] = time.time()

            return func(*args, **kwargs)

        return wrapper
    return decorator


@rate_limit(calls_per_second=2.0)  # ← Max 2 calls per second
def api_call(endpoint: str) -> str:
    """Simulate API call."""
    print(f"  Calling API: {endpoint}")
    return f"Response from {endpoint}"


# ============================================================================
# VALIDATION WITH CUSTOM RULES
# ============================================================================

def validate(
    min_value: Optional[float] = None,
    max_value: Optional[float] = None
) -> Callable:
    """
    Decorator factory for validating numeric arguments.

    Args:
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Validate all numeric arguments
            for arg in args:
                if isinstance(arg, (int, float)):
                    if min_value is not None and arg < min_value:
                        raise ValueError(
                            f"Argument {arg} is less than minimum {min_value}"
                        )
                    if max_value is not None and arg > max_value:
                        raise ValueError(
                            f"Argument {arg} is greater than maximum {max_value}"
                        )

            return func(*args, **kwargs)

        return wrapper
    return decorator


@validate(min_value=0, max_value=100)
def set_percentage(value: float) -> str:
    """Set percentage (must be 0-100)."""
    return f"Percentage set to {value}%"


@validate(min_value=0)
def set_age(age: int) -> str:
    """Set age (must be non-negative)."""
    return f"Age set to {age}"


# ============================================================================
# TIMEOUT DECORATOR
# ============================================================================

def timeout(seconds: float) -> Callable:
    """
    Decorator factory for function timeout.

    Note: This is a simplified version for demonstration.
    Real implementation would use threading or signals.

    Args:
        seconds: Timeout in seconds

    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"Timeout set to {seconds} seconds")
            start_time = time.time()

            result = func(*args, **kwargs)

            elapsed = time.time() - start_time
            if elapsed > seconds:
                print(f"Warning: Function took {elapsed:.2f}s (timeout: {seconds}s)")

            return result

        return wrapper
    return decorator


@timeout(seconds=0.5)
def quick_task() -> str:
    """Quick task."""
    time.sleep(0.1)
    return "Done quickly"


@timeout(seconds=0.5)
def slow_task() -> str:
    """Slow task."""
    time.sleep(1.0)
    return "Done slowly"


# ============================================================================
# CACHING WITH CONFIGURABLE SIZE
# ============================================================================

def cache_with_size(max_size: int = 128) -> Callable:
    """
    Decorator factory for caching with size limit.

    Args:
        max_size: Maximum cache size

    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        cache: dict = {}

        @wraps(func)
        def wrapper(*args: Any) -> Any:
            # Check cache
            if args in cache:
                print(f"Cache hit: {func.__name__}{args}")
                return cache[args]

            # Compute result
            print(f"Cache miss: {func.__name__}{args}")
            result = func(*args)

            # Add to cache (with size limit)
            if len(cache) >= max_size:
                # Remove oldest entry (simplified LRU)
                oldest_key = next(iter(cache))
                del cache[oldest_key]
                print(f"Cache full, removed {oldest_key}")

            cache[args] = result
            return result

        # Expose cache for inspection
        wrapper.cache = cache  # type: ignore

        return wrapper
    return decorator


@cache_with_size(max_size=3)
def compute(x: int, y: int) -> int:
    """Compute x + y (with limited cache)."""
    return x + y


# ============================================================================
# DECORATOR THAT CAN BE USED WITH OR WITHOUT ARGUMENTS
# ============================================================================

def smart_log(func: Optional[Callable] = None, *, prefix: str = "LOG") -> Callable:
    """
    Decorator that works with or without arguments.

    Usage:
        @smart_log
        def func1(): pass

        @smart_log(prefix="INFO")
        def func2(): pass
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"[{prefix}] {f.__name__} called")
            return f(*args, **kwargs)
        return wrapper

    # Called without arguments: @smart_log
    if func is not None:
        return decorator(func)

    # Called with arguments: @smart_log(prefix="INFO")
    return decorator


@smart_log
def function1() -> str:
    """Function with default prefix."""
    return "Result 1"


@smart_log(prefix="DEBUG")
def function2() -> str:
    """Function with custom prefix."""
    return "Result 2"


# ============================================================================
# DEMONSTRATION: Decorators with Arguments
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DECORATORS WITH ARGUMENTS")
    print("=" * 70)

    # ========================================================================
    # Repeat Decorator
    # ========================================================================
    print("\n" + "=" * 70)
    print("1. REPEAT DECORATOR")
    print("=" * 70)

    print("\nCalling greet('Alice'):")
    greet("Alice")

    print("\nCalling count(42):")
    count(42)

    # ========================================================================
    # Logging with Prefix
    # ========================================================================
    print("\n" + "=" * 70)
    print("2. LOGGING WITH CUSTOM PREFIX")
    print("=" * 70)

    print("\nCalling add(5, 3):")
    add(5, 3)

    print("\nCalling multiply(4, 7):")
    multiply(4, 7)

    print("\nCalling subtract(10, 3):")
    subtract(10, 3)

    # ========================================================================
    # Retry Decorator
    # ========================================================================
    print("\n" + "=" * 70)
    print("3. RETRY DECORATOR")
    print("=" * 70)

    print("\nCalling unreliable_function():")
    _call_count = 0  # Reset counter
    result = unreliable_function()
    print(f"Final result: {result}")

    # ========================================================================
    # Rate Limiting
    # ========================================================================
    print("\n" + "=" * 70)
    print("4. RATE LIMITING")
    print("=" * 70)

    print("\nCalling api_call() 3 times (max 2 calls/second):")
    for i in range(3):
        api_call(f"/endpoint{i + 1}")

    # ========================================================================
    # Validation
    # ========================================================================
    print("\n" + "=" * 70)
    print("5. VALIDATION WITH CUSTOM RULES")
    print("=" * 70)

    print("\nCalling set_percentage(75):")
    print(set_percentage(75))

    print("\nCalling set_percentage(150):")
    try:
        set_percentage(150)
    except ValueError as e:
        print(f"Error: {e}")

    print("\nCalling set_age(25):")
    print(set_age(25))

    print("\nCalling set_age(-5):")
    try:
        set_age(-5)
    except ValueError as e:
        print(f"Error: {e}")

    # ========================================================================
    # Timeout
    # ========================================================================
    print("\n" + "=" * 70)
    print("6. TIMEOUT DECORATOR")
    print("=" * 70)

    print("\nCalling quick_task():")
    quick_task()

    print("\nCalling slow_task():")
    slow_task()

    # ========================================================================
    # Caching with Size Limit
    # ========================================================================
    print("\n" + "=" * 70)
    print("7. CACHING WITH SIZE LIMIT")
    print("=" * 70)

    print("\nAdding 4 items to cache (max size: 3):")
    compute(1, 2)
    compute(3, 4)
    compute(5, 6)
    compute(7, 8)  # This will evict oldest entry

    print("\nAccessing cached item:")
    compute(3, 4)  # Cache hit

    # ========================================================================
    # Smart Decorator (with or without arguments)
    # ========================================================================
    print("\n" + "=" * 70)
    print("8. DECORATOR WITH OR WITHOUT ARGUMENTS")
    print("=" * 70)

    print("\nCalling function1() (default prefix):")
    function1()

    print("\nCalling function2() (custom prefix):")
    function2()

    print("\n" + "=" * 70)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Decorator factories create decorators with parameters")
    print("2. Three levels: factory -> decorator -> wrapper")
    print("3. Factory returns decorator, decorator returns wrapper")
    print("4. Parameters are captured in closure")
    print("5. @decorator(args) calls factory, then applies decorator")
    print("6. Use default arguments for optional parameters")
    print("7. Common patterns: retry, rate limit, validation, caching")
    print("8. Can create decorators that work with or without arguments")
    print("9. Always use @wraps to preserve metadata")
    print("10. Decorator factories enable highly configurable decorators")
    print("=" * 70)

