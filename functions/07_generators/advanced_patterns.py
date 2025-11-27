"""
Example: Advanced Generator Patterns
Demonstrates advanced generator techniques and patterns.

Key Concepts:
- yield from: delegate to sub-generator
- Generator methods: send(), throw(), close()
- Coroutines (generator-based)
- Generator pipelines
- Recursive generators

Advanced Features:
- send(): Send values into generator
- throw(): Raise exception in generator
- close(): Stop generator
- yield from: Yield all values from another generator
"""

from typing import Generator, Iterator, Any
import itertools


# ============================================================================
# YIELD FROM
# ============================================================================

def chain(*iterables: Iterator) -> Generator:
    """
    Chain multiple iterables using yield from.
    
    Args:
        *iterables: Iterables to chain
        
    Yields:
        Values from all iterables
    """
    for iterable in iterables:
        yield from iterable  # ← Delegate to sub-generator


def flatten(nested: list) -> Generator:
    """
    Recursively flatten nested list using yield from.
    
    Args:
        nested: Nested list
        
    Yields:
        Flattened values
    """
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)  # ← Recursive yield from
        else:
            yield item


def read_files(*filenames: str) -> Generator[str, None, None]:
    """
    Read multiple files using yield from.
    
    Args:
        *filenames: Files to read
        
    Yields:
        Lines from all files
    """
    for filename in filenames:
        try:
            with open(filename, 'r') as f:
                yield from f  # ← Yield all lines from file
        except FileNotFoundError:
            print(f"Warning: {filename} not found")


# ============================================================================
# GENERATOR WITH send()
# ============================================================================

def running_average() -> Generator[float, float, None]:
    """
    Generator that calculates running average.
    
    Uses send() to receive values.
    
    Yields:
        Current running average
    """
    total = 0.0
    count = 0
    
    while True:
        value = yield (total / count if count > 0 else 0.0)  # ← Yield and receive
        if value is not None:
            total += value
            count += 1


def accumulator(initial: float = 0.0) -> Generator[float, float, None]:
    """
    Generator that accumulates values.
    
    Args:
        initial: Initial value
        
    Yields:
        Current accumulated value
    """
    total = initial
    
    while True:
        value = yield total  # ← Yield current, receive next
        if value is not None:
            total += value


# ============================================================================
# GENERATOR WITH throw() AND close()
# ============================================================================

def resilient_generator() -> Generator[int, None, None]:
    """
    Generator that handles exceptions.
    
    Demonstrates throw() method.
    
    Yields:
        int: Sequential numbers
    """
    num = 0
    while True:
        try:
            yield num
            num += 1
        except ValueError as e:
            print(f"Caught ValueError: {e}")
            num = 0  # Reset on error
        except GeneratorExit:
            print("Generator closing...")
            raise  # Re-raise to allow cleanup


# ============================================================================
# GENERATOR PIPELINES
# ============================================================================

def numbers(start: int, stop: int) -> Generator[int, None, None]:
    """Generate numbers from start to stop."""
    for num in range(start, stop):
        yield num


def filter_even(numbers: Iterator[int]) -> Generator[int, None, None]:
    """Filter even numbers."""
    for num in numbers:
        if num % 2 == 0:
            yield num


def square(numbers: Iterator[int]) -> Generator[int, None, None]:
    """Square numbers."""
    for num in numbers:
        yield num ** 2


def take_while(predicate, iterable: Iterator) -> Generator:
    """
    Take items while predicate is true.
    
    Args:
        predicate: Function that returns bool
        iterable: Source iterable
        
    Yields:
        Items while predicate is true
    """
    for item in iterable:
        if not predicate(item):
            break
        yield item


# ============================================================================
# RECURSIVE GENERATORS
# ============================================================================

def tree_traverse(node: dict) -> Generator[Any, None, None]:
    """
    Recursively traverse tree structure.

    Args:
        node: Tree node (dict with 'value' and optional 'children')

    Yields:
        Values from tree in depth-first order
    """
    yield node['value']

    if 'children' in node:
        for child in node['children']:
            yield from tree_traverse(child)  # ← Recursive traversal


def permutations(items: list) -> Generator[list, None, None]:
    """
    Generate all permutations recursively.

    Args:
        items: List of items

    Yields:
        All permutations
    """
    if len(items) <= 1:
        yield items
    else:
        for i, item in enumerate(items):
            rest = items[:i] + items[i+1:]
            for perm in permutations(rest):
                yield [item] + perm


# ============================================================================
# GENERATOR CONTEXT MANAGER
# ============================================================================

def file_reader(filename: str) -> Generator[str, None, None]:
    """
    Generator with cleanup (context manager pattern).

    Args:
        filename: File to read

    Yields:
        Lines from file
    """
    print(f"Opening {filename}")
    try:
        with open(filename, 'r') as f:
            for line in f:
                yield line.strip()
    finally:
        print(f"Closing {filename}")


# ============================================================================
# TEE: SPLIT GENERATOR INTO MULTIPLE
# ============================================================================

def demonstrate_tee() -> None:
    """Demonstrate itertools.tee() to split generator."""

    # Create generator
    gen = (x ** 2 for x in range(10))

    # Split into two independent iterators
    gen1, gen2 = itertools.tee(gen, 2)

    print("First iterator:")
    for value in gen1:
        print(f"  {value}", end=" ")
    print()

    print("\nSecond iterator (independent):")
    for value in gen2:
        print(f"  {value}", end=" ")
    print()


# ============================================================================
# ISLICE: SLICE GENERATOR
# ============================================================================

def demonstrate_islice() -> None:
    """Demonstrate itertools.islice() for slicing generators."""

    # Infinite generator
    def infinite():
        num = 0
        while True:
            yield num
            num += 1

    # Take items 10-20
    print("Items 10-20 from infinite generator:")
    for value in itertools.islice(infinite(), 10, 20):
        print(f"  {value}", end=" ")
    print()


# ============================================================================
# DEMONSTRATION: Advanced Generator Patterns
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ADVANCED GENERATOR PATTERNS")
    print("=" * 70)

    # ========================================================================
    # yield from
    # ========================================================================
    print("\n" + "=" * 70)
    print("1. YIELD FROM")
    print("=" * 70)

    print("\nChaining iterables:")
    for value in chain([1, 2, 3], [4, 5, 6], [7, 8, 9]):
        print(f"  {value}", end=" ")
    print()

    print("\nFlattening nested list:")
    nested = [1, [2, 3, [4, 5]], 6, [7, [8, 9]]]
    print(f"  Nested: {nested}")
    print(f"  Flattened: {list(flatten(nested))}")

    # ========================================================================
    # Generator with send()
    # ========================================================================
    print("\n" + "=" * 70)
    print("2. GENERATOR WITH send()")
    print("=" * 70)

    print("\nRunning average:")
    avg = running_average()
    next(avg)  # Prime the generator

    print(f"  Send 10: {avg.send(10)}")
    print(f"  Send 20: {avg.send(20)}")
    print(f"  Send 30: {avg.send(30)}")
    print(f"  Current average: {avg.send(None)}")

    print("\nAccumulator:")
    acc = accumulator(100)
    next(acc)  # Prime the generator

    print(f"  Initial: {acc.send(None)}")
    print(f"  Add 10: {acc.send(10)}")
    print(f"  Add 20: {acc.send(20)}")
    print(f"  Add 30: {acc.send(30)}")

    # ========================================================================
    # Generator with throw() and close()
    # ========================================================================
    print("\n" + "=" * 70)
    print("3. GENERATOR WITH throw() AND close()")
    print("=" * 70)

    print("\nResilient generator:")
    gen = resilient_generator()

    print(f"  Next: {next(gen)}")
    print(f"  Next: {next(gen)}")
    print(f"  Next: {next(gen)}")

    print("\n  Throwing ValueError:")
    gen.throw(ValueError, "Reset!")

    print(f"  Next: {next(gen)}")
    print(f"  Next: {next(gen)}")

    print("\n  Closing generator:")
    gen.close()

    # ========================================================================
    # Generator Pipelines
    # ========================================================================
    print("\n" + "=" * 70)
    print("4. GENERATOR PIPELINES")
    print("=" * 70)

    print("\nPipeline: numbers -> filter_even -> square")
    pipeline = square(filter_even(numbers(1, 11)))
    for value in pipeline:
        print(f"  {value}", end=" ")
    print()

    print("\nPipeline with take_while:")
    pipeline = take_while(lambda x: x < 100, square(filter_even(numbers(1, 20))))
    for value in pipeline:
        print(f"  {value}", end=" ")
    print()

    # ========================================================================
    # Recursive Generators
    # ========================================================================
    print("\n" + "=" * 70)
    print("5. RECURSIVE GENERATORS")
    print("=" * 70)

    print("\nTree traversal:")
    tree = {
        'value': 1,
        'children': [
            {'value': 2, 'children': [{'value': 4}, {'value': 5}]},
            {'value': 3, 'children': [{'value': 6}]}
        ]
    }
    print(f"  Tree values: {list(tree_traverse(tree))}")

    print("\nPermutations of [1, 2, 3]:")
    for perm in permutations([1, 2, 3]):
        print(f"  {perm}")

    # ========================================================================
    # itertools.tee()
    # ========================================================================
    print("\n" + "=" * 70)
    print("6. SPLITTING GENERATOR WITH tee()")
    print("=" * 70)

    demonstrate_tee()

    # ========================================================================
    # itertools.islice()
    # ========================================================================
    print("\n" + "=" * 70)
    print("7. SLICING GENERATOR WITH islice()")
    print("=" * 70)

    demonstrate_islice()

    # ========================================================================
    # Practical Example: Data Processing Pipeline
    # ========================================================================
    print("\n" + "=" * 70)
    print("8. PRACTICAL EXAMPLE: DATA PROCESSING PIPELINE")
    print("=" * 70)

    print("\nProcessing pipeline:")
    print("  1. Generate numbers 1-100")
    print("  2. Filter multiples of 3")
    print("  3. Square them")
    print("  4. Take first 5")

    def multiples_of_3(nums):
        for num in nums:
            if num % 3 == 0:
                yield num

    pipeline = itertools.islice(
        square(multiples_of_3(numbers(1, 101))),
        5
    )

    result = list(pipeline)
    print(f"  Result: {result}")

    print("\n" + "=" * 70)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. yield from: delegate to sub-generator")
    print("2. send(): send values into generator")
    print("3. throw(): raise exception in generator")
    print("4. close(): stop generator and run cleanup")
    print("5. Generator pipelines: chain generators for data processing")
    print("6. Recursive generators: use yield from for recursion")
    print("7. itertools.tee(): split generator into multiple iterators")
    print("8. itertools.islice(): slice infinite generators")
    print("9. Generators maintain state between yields")
    print("10. Use try/finally for cleanup in generators")
    print("=" * 70)

