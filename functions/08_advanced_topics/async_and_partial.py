"""
Example: Async Functions and Partial Application
Demonstrates async/await and functools.partial.

Key Concepts:
- Async functions: defined with 'async def'
- await: pause execution until coroutine completes
- Coroutines: async functions return coroutine objects
- Event loop: manages async execution
- partial: create new function with pre-filled arguments

Async vs Sync:
- Sync: blocking, one at a time
- Async: non-blocking, concurrent execution
"""

import asyncio
from functools import partial
from typing import Callable, Any
import time


# ============================================================================
# BASIC ASYNC FUNCTIONS
# ============================================================================

async def simple_async() -> str:
    """
    Simple async function.
    
    Returns:
        String result
    """
    print("Starting async function")
    await asyncio.sleep(1)  # ← Non-blocking sleep
    print("Finished async function")
    return "Done!"


async def fetch_data(url: str, delay: float = 1.0) -> dict:
    """
    Simulate fetching data asynchronously.
    
    Args:
        url: URL to fetch
        delay: Simulated delay
        
    Returns:
        Simulated data
    """
    print(f"Fetching {url}...")
    await asyncio.sleep(delay)  # ← Simulate network delay
    print(f"Fetched {url}")
    return {"url": url, "data": f"Data from {url}"}


# ============================================================================
# RUNNING ASYNC FUNCTIONS CONCURRENTLY
# ============================================================================

async def fetch_multiple() -> list[dict]:
    """
    Fetch multiple URLs concurrently.
    
    Returns:
        List of results
    """
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/posts",
        "https://api.example.com/comments"
    ]
    
    # Create tasks
    tasks = [fetch_data(url, delay=1.0) for url in urls]
    
    # Run concurrently
    results = await asyncio.gather(*tasks)  # ← Wait for all
    
    return results


async def fetch_with_timeout(url: str, timeout: float = 2.0) -> dict:
    """
    Fetch with timeout.
    
    Args:
        url: URL to fetch
        timeout: Timeout in seconds
        
    Returns:
        Fetched data
        
    Raises:
        asyncio.TimeoutError: If timeout exceeded
    """
    try:
        result = await asyncio.wait_for(
            fetch_data(url, delay=1.0),
            timeout=timeout
        )
        return result
    except asyncio.TimeoutError:
        print(f"Timeout fetching {url}")
        raise


# ============================================================================
# ASYNC GENERATORS
# ============================================================================

async def async_range(start: int, stop: int, delay: float = 0.1) -> int:
    """
    Async generator that yields numbers with delay.
    
    Args:
        start: Starting number
        stop: Stopping number
        delay: Delay between yields
        
    Yields:
        Numbers from start to stop
    """
    for i in range(start, stop):
        await asyncio.sleep(delay)  # ← Async delay
        yield i  # ← Yield value


async def process_async_stream() -> None:
    """Process async generator."""
    print("Processing async stream:")
    async for value in async_range(1, 6, delay=0.2):
        print(f"  Received: {value}")


# ============================================================================
# PARTIAL APPLICATION
# ============================================================================

def power(base: int, exponent: int) -> int:
    """
    Calculate base^exponent.
    
    Args:
        base: Base number
        exponent: Exponent
        
    Returns:
        base^exponent
    """
    return base ** exponent


# Create specialized functions using partial
square = partial(power, exponent=2)  # ← Fix exponent=2
cube = partial(power, exponent=3)    # ← Fix exponent=3


def greet(greeting: str, name: str, punctuation: str = "!") -> str:
    """
    Greet someone.
    
    Args:
        greeting: Greeting word
        name: Person's name
        punctuation: Ending punctuation
        
    Returns:
        Greeting message
    """
    return f"{greeting}, {name}{punctuation}"


# Create specialized greeting functions
say_hello = partial(greet, "Hello")  # ← Fix greeting
say_goodbye = partial(greet, "Goodbye")  # ← Fix greeting
formal_hello = partial(greet, "Hello", punctuation=".")  # ← Fix both


# ============================================================================
# PARTIAL WITH CALLBACKS
# ============================================================================

def process_data(data: list[int], operation: Callable[[int], int]) -> list[int]:
    """
    Process data with operation.
    
    Args:
        data: List of integers
        operation: Function to apply
        
    Returns:
        Processed data
    """
    return [operation(x) for x in data]


def multiply(x: int, factor: int) -> int:
    """Multiply x by factor."""
    return x * factor


# Create specialized operations
double = partial(multiply, factor=2)
triple = partial(multiply, factor=3)


# ============================================================================
# PARTIAL FOR CONFIGURATION
# ============================================================================

def log_message(
    message: str,
    level: str = "INFO",
    prefix: str = "",
    suffix: str = ""
) -> str:
    """
    Log message with configuration.

    Args:
        message: Message to log
        level: Log level
        prefix: Prefix string
        suffix: Suffix string

    Returns:
        Formatted log message
    """
    return f"{prefix}[{level}] {message}{suffix}"


# Create specialized loggers
info_log = partial(log_message, level="INFO")
error_log = partial(log_message, level="ERROR", prefix=">>> ")
debug_log = partial(log_message, level="DEBUG", suffix=" <<<")


# ============================================================================
# PARTIAL WITH METHODS
# ============================================================================

class Calculator:
    """Calculator with configurable operations."""

    def __init__(self, initial: float = 0.0):
        """Initialize calculator."""
        self.value = initial

    def add(self, x: float, y: float) -> float:
        """Add two numbers."""
        return x + y

    def multiply(self, x: float, y: float) -> float:
        """Multiply two numbers."""
        return x * y


# Create partial methods
calc = Calculator()
add_10 = partial(calc.add, 10)  # ← Fix first argument
multiply_by_5 = partial(calc.multiply, y=5)  # ← Fix second argument


# ============================================================================
# DEMONSTRATION: Async and Partial
# ============================================================================

async def main_async():
    """Main async demonstration."""

    print("=" * 70)
    print("ASYNC FUNCTIONS")
    print("=" * 70)

    # ========================================================================
    # Basic Async Function
    # ========================================================================
    print("\n" + "=" * 70)
    print("1. BASIC ASYNC FUNCTION")
    print("=" * 70)

    result = await simple_async()
    print(f"Result: {result}")

    # ========================================================================
    # Concurrent Execution
    # ========================================================================
    print("\n" + "=" * 70)
    print("2. CONCURRENT EXECUTION")
    print("=" * 70)

    print("\nFetching multiple URLs concurrently:")
    start_time = time.time()
    results = await fetch_multiple()
    elapsed = time.time() - start_time

    print(f"\nFetched {len(results)} URLs in {elapsed:.2f}s")
    print("(Sequential would take ~3s, concurrent takes ~1s)")

    # ========================================================================
    # Async with Timeout
    # ========================================================================
    print("\n" + "=" * 70)
    print("3. ASYNC WITH TIMEOUT")
    print("=" * 70)

    print("\nFetching with timeout:")
    try:
        result = await fetch_with_timeout("https://api.example.com/data", timeout=2.0)
        print(f"Success: {result}")
    except asyncio.TimeoutError:
        print("Request timed out")

    # ========================================================================
    # Async Generators
    # ========================================================================
    print("\n" + "=" * 70)
    print("4. ASYNC GENERATORS")
    print("=" * 70)

    await process_async_stream()


def main_partial():
    """Main partial application demonstration."""

    print("\n" + "=" * 70)
    print("PARTIAL APPLICATION")
    print("=" * 70)

    # ========================================================================
    # Basic Partial
    # ========================================================================
    print("\n" + "=" * 70)
    print("5. BASIC PARTIAL APPLICATION")
    print("=" * 70)

    print("\nPower functions:")
    print(f"  square(5) = {square(5)}")
    print(f"  cube(5) = {cube(5)}")
    print(f"  power(5, 4) = {power(5, 4)}")

    print("\nGreeting functions:")
    print(f"  say_hello('Alice') = {say_hello('Alice')}")
    print(f"  say_goodbye('Bob') = {say_goodbye('Bob')}")
    print(f"  formal_hello('Dr. Smith') = {formal_hello('Dr. Smith')}")

    # ========================================================================
    # Partial with Callbacks
    # ========================================================================
    print("\n" + "=" * 70)
    print("6. PARTIAL WITH CALLBACKS")
    print("=" * 70)

    data = [1, 2, 3, 4, 5]

    print(f"\nOriginal data: {data}")
    print(f"  Doubled: {process_data(data, double)}")
    print(f"  Tripled: {process_data(data, triple)}")

    # ========================================================================
    # Partial for Configuration
    # ========================================================================
    print("\n" + "=" * 70)
    print("7. PARTIAL FOR CONFIGURATION")
    print("=" * 70)

    print("\nSpecialized loggers:")
    print(f"  {info_log('Application started')}")
    print(f"  {error_log('Connection failed')}")
    print(f"  {debug_log('Variable x = 42')}")

    # ========================================================================
    # Partial with Methods
    # ========================================================================
    print("\n" + "=" * 70)
    print("8. PARTIAL WITH METHODS")
    print("=" * 70)

    print("\nPartial methods:")
    print(f"  add_10(5) = {add_10(5)}")
    print(f"  multiply_by_5(7) = {multiply_by_5(7)}")


if __name__ == "__main__":
    # Run async demonstrations
    asyncio.run(main_async())

    # Run partial demonstrations
    main_partial()

    print("\n" + "=" * 70)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("ASYNC:")
    print("1. async def: define async function (coroutine)")
    print("2. await: pause until coroutine completes")
    print("3. asyncio.gather(): run multiple coroutines concurrently")
    print("4. asyncio.wait_for(): add timeout to coroutine")
    print("5. async for: iterate over async generator")
    print("6. Async is concurrent, not parallel (single-threaded)")
    print("7. Use for I/O-bound operations (network, file)")
    print()
    print("PARTIAL:")
    print("8. partial(): create new function with pre-filled arguments")
    print("9. Useful for callbacks and configuration")
    print("10. Can fix positional or keyword arguments")
    print("11. Works with functions, methods, and lambdas")
    print("12. Creates more readable, reusable code")
    print("=" * 70)

