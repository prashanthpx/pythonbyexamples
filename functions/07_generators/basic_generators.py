"""
Example: Basic Generators and yield
Demonstrates generator functions and the yield keyword.

Key Concepts:
- Generators are functions that use 'yield' instead of 'return'
- Generators produce values lazily (on-demand)
- Generators maintain state between calls
- Generators are memory-efficient for large sequences
- Generators are iterators (can be used in for loops)

Generator vs Regular Function:
- Regular function: returns once, loses state
- Generator: yields multiple times, maintains state
"""

from typing import Generator, Iterator
import sys


# ============================================================================
# BASIC GENERATOR FUNCTION
# ============================================================================

def simple_generator() -> Generator[int, None, None]:
    """
    Simple generator that yields three values.
    
    Yields:
        int: Values 1, 2, 3
    """
    print("Starting generator")
    yield 1  # ← Pause here, return 1
    print("Resuming after first yield")
    yield 2  # ← Pause here, return 2
    print("Resuming after second yield")
    yield 3  # ← Pause here, return 3
    print("Generator finished")


# ============================================================================
# GENERATOR FOR RANGE (LIKE range())
# ============================================================================

def my_range(start: int, stop: int, step: int = 1) -> Generator[int, None, None]:
    """
    Generator that mimics range().
    
    Args:
        start: Starting value
        stop: Stopping value (exclusive)
        step: Step size
        
    Yields:
        int: Values from start to stop
    """
    current = start
    while current < stop:
        yield current  # ← Yield current value
        current += step  # ← Update state


# ============================================================================
# INFINITE GENERATOR
# ============================================================================

def infinite_sequence() -> Generator[int, None, None]:
    """
    Generator that produces infinite sequence.
    
    Yields:
        int: 0, 1, 2, 3, ...
    """
    num = 0
    while True:  # ← Infinite loop
        yield num
        num += 1


def fibonacci() -> Generator[int, None, None]:
    """
    Generator for Fibonacci sequence.
    
    Yields:
        int: Fibonacci numbers (0, 1, 1, 2, 3, 5, 8, ...)
    """
    a, b = 0, 1
    while True:
        yield a  # ← Yield current Fibonacci number
        a, b = b, a + b  # ← Update state


# ============================================================================
# GENERATOR WITH PARAMETERS
# ============================================================================

def countdown(n: int) -> Generator[int, None, None]:
    """
    Generator that counts down from n to 1.
    
    Args:
        n: Starting number
        
    Yields:
        int: n, n-1, ..., 1
    """
    print(f"Countdown from {n}")
    while n > 0:
        yield n
        n -= 1
    print("Blastoff!")


# ============================================================================
# GENERATOR THAT PROCESSES DATA
# ============================================================================

def read_lines(filename: str) -> Generator[str, None, None]:
    """
    Generator that reads file line by line.
    
    Memory-efficient: doesn't load entire file into memory.
    
    Args:
        filename: File to read
        
    Yields:
        str: Each line from file
    """
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()  # ← Yield one line at a time


def filter_lines(lines: Iterator[str], keyword: str) -> Generator[str, None, None]:
    """
    Generator that filters lines containing keyword.
    
    Args:
        lines: Iterator of lines
        keyword: Keyword to search for
        
    Yields:
        str: Lines containing keyword
    """
    for line in lines:
        if keyword in line:
            yield line  # ← Yield only matching lines


# ============================================================================
# GENERATOR THAT TRANSFORMS DATA
# ============================================================================

def square_numbers(numbers: Iterator[int]) -> Generator[int, None, None]:
    """
    Generator that squares numbers.
    
    Args:
        numbers: Iterator of numbers
        
    Yields:
        int: Squared numbers
    """
    for num in numbers:
        yield num ** 2  # ← Transform and yield


def take(n: int, iterable: Iterator) -> Generator:
    """
    Generator that takes first n items from iterable.
    
    Args:
        n: Number of items to take
        iterable: Source iterable
        
    Yields:
        Items from iterable (up to n)
    """
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item


# ============================================================================
# MEMORY EFFICIENCY COMPARISON
# ============================================================================

def list_squares(n: int) -> list:
    """
    Regular function: returns list of squares.

    Memory: O(n) - stores all values in memory
    """
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result


def generator_squares(n: int) -> Generator[int, None, None]:
    """
    Generator: yields squares one at a time.

    Memory: O(1) - stores only current value
    """
    for i in range(n):
        yield i ** 2


# ============================================================================
# GENERATOR STATE EXAMPLE
# ============================================================================

def stateful_generator() -> Generator[str, None, None]:
    """
    Generator that demonstrates state preservation.

    State is maintained between yields.
    """
    state = "initialized"
    yield f"State: {state}"

    state = "processing"
    yield f"State: {state}"

    state = "completed"
    yield f"State: {state}"


# ============================================================================
# GENERATOR WITH CLEANUP
# ============================================================================

def generator_with_cleanup() -> Generator[int, None, None]:
    """
    Generator with setup and cleanup.

    Demonstrates try/finally for cleanup.
    """
    print("Setup: acquiring resource")
    try:
        for i in range(3):
            yield i
    finally:
        print("Cleanup: releasing resource")


# ============================================================================
# CHAINING GENERATORS
# ============================================================================

def chain_generators() -> Generator[int, None, None]:
    """
    Generator that chains multiple generators.

    Yields:
        int: Values from multiple sources
    """
    # Yield from first generator
    for value in my_range(1, 4):
        yield value

    # Yield from second generator
    for value in my_range(10, 13):
        yield value


# ============================================================================
# DEMONSTRATION: Basic Generators
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("BASIC GENERATORS AND YIELD")
    print("=" * 70)

    # ========================================================================
    # Simple Generator
    # ========================================================================
    print("\n" + "=" * 70)
    print("1. SIMPLE GENERATOR")
    print("=" * 70)

    print("\nCreating generator:")
    gen = simple_generator()
    print(f"Generator object: {gen}")
    print(f"Type: {type(gen)}")

    print("\nCalling next() three times:")
    print(f"First: {next(gen)}")
    print(f"Second: {next(gen)}")
    print(f"Third: {next(gen)}")

    print("\nTrying to call next() again:")
    try:
        next(gen)
    except StopIteration:
        print("StopIteration raised (generator exhausted)")

    # ========================================================================
    # Using Generator in For Loop
    # ========================================================================
    print("\n" + "=" * 70)
    print("2. GENERATOR IN FOR LOOP")
    print("=" * 70)

    print("\nIterating with for loop:")
    for value in simple_generator():
        print(f"  Value: {value}")

    # ========================================================================
    # Custom Range Generator
    # ========================================================================
    print("\n" + "=" * 70)
    print("3. CUSTOM RANGE GENERATOR")
    print("=" * 70)

    print("\nmy_range(0, 10, 2):")
    for num in my_range(0, 10, 2):
        print(f"  {num}", end=" ")
    print()

    # ========================================================================
    # Infinite Generator
    # ========================================================================
    print("\n" + "=" * 70)
    print("4. INFINITE GENERATOR")
    print("=" * 70)

    print("\nFirst 10 numbers from infinite_sequence():")
    for num in take(10, infinite_sequence()):
        print(f"  {num}", end=" ")
    print()

    print("\nFirst 10 Fibonacci numbers:")
    for num in take(10, fibonacci()):
        print(f"  {num}", end=" ")
    print()

    # ========================================================================
    # Countdown Generator
    # ========================================================================
    print("\n" + "=" * 70)
    print("5. COUNTDOWN GENERATOR")
    print("=" * 70)

    print("\nCountdown from 5:")
    for num in countdown(5):
        print(f"  {num}")

    # ========================================================================
    # Generator Pipeline
    # ========================================================================
    print("\n" + "=" * 70)
    print("6. GENERATOR PIPELINE")
    print("=" * 70)

    print("\nSquaring numbers 1-5:")
    numbers = my_range(1, 6)
    squares = square_numbers(numbers)
    for sq in squares:
        print(f"  {sq}", end=" ")
    print()

    print("\nChaining: range -> square -> take first 3:")
    result = take(3, square_numbers(my_range(1, 10)))
    for value in result:
        print(f"  {value}", end=" ")
    print()

    # ========================================================================
    # Memory Efficiency
    # ========================================================================
    print("\n" + "=" * 70)
    print("7. MEMORY EFFICIENCY")
    print("=" * 70)

    n = 1000

    print(f"\nCreating list of {n} squares:")
    list_result = list_squares(n)
    list_size = sys.getsizeof(list_result)
    print(f"  Memory used: {list_size:,} bytes")

    print(f"\nCreating generator of {n} squares:")
    gen_result = generator_squares(n)
    gen_size = sys.getsizeof(gen_result)
    print(f"  Memory used: {gen_size:,} bytes")

    print(f"\nMemory savings: {list_size / gen_size:.1f}x")

    # ========================================================================
    # Stateful Generator
    # ========================================================================
    print("\n" + "=" * 70)
    print("8. STATEFUL GENERATOR")
    print("=" * 70)

    print("\nGenerator maintains state between yields:")
    for state in stateful_generator():
        print(f"  {state}")

    # ========================================================================
    # Generator with Cleanup
    # ========================================================================
    print("\n" + "=" * 70)
    print("9. GENERATOR WITH CLEANUP")
    print("=" * 70)

    print("\nGenerator with try/finally:")
    for value in generator_with_cleanup():
        print(f"  Value: {value}")

    # ========================================================================
    # Chaining Generators
    # ========================================================================
    print("\n" + "=" * 70)
    print("10. CHAINING GENERATORS")
    print("=" * 70)

    print("\nChaining multiple generators:")
    for value in chain_generators():
        print(f"  {value}", end=" ")
    print()

    print("\n" + "=" * 70)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Generators use 'yield' instead of 'return'")
    print("2. Generators are lazy: values computed on-demand")
    print("3. Generators maintain state between yields")
    print("4. Generators are memory-efficient (O(1) vs O(n))")
    print("5. Generators are iterators (can use in for loops)")
    print("6. Use next() to get next value manually")
    print("7. StopIteration raised when generator exhausted")
    print("8. Generators can be infinite (while True)")
    print("9. Generators can be chained for pipelines")
    print("10. Use try/finally for cleanup in generators")
    print("=" * 70)

