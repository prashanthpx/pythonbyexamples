"""
Example: Generator Expressions and Iterators
Demonstrates generator expressions and iterator protocol.

Key Concepts:
- Generator expressions: (expr for item in iterable)
- Similar to list comprehensions but lazy
- Iterator protocol: __iter__() and __next__()
- iter() and next() built-in functions
- Iterables vs Iterators

Comparison:
- List comprehension: [x**2 for x in range(10)] - eager, returns list
- Generator expression: (x**2 for x in range(10)) - lazy, returns generator
"""

from typing import Iterator, Iterable, Any
import sys


# ============================================================================
# GENERATOR EXPRESSIONS
# ============================================================================

def demonstrate_generator_expressions() -> None:
    """Demonstrate generator expressions vs list comprehensions."""
    
    # List comprehension (eager)
    list_comp = [x ** 2 for x in range(10)]
    print(f"List comprehension: {list_comp}")
    print(f"Type: {type(list_comp)}")
    print(f"Memory: {sys.getsizeof(list_comp)} bytes")
    
    # Generator expression (lazy)
    gen_expr = (x ** 2 for x in range(10))
    print(f"\nGenerator expression: {gen_expr}")
    print(f"Type: {type(gen_expr)}")
    print(f"Memory: {sys.getsizeof(gen_expr)} bytes")
    
    # Consuming generator
    print(f"Values: {list(gen_expr)}")


# ============================================================================
# GENERATOR EXPRESSIONS IN FUNCTIONS
# ============================================================================

def sum_of_squares(n: int) -> int:
    """
    Calculate sum of squares using generator expression.
    
    Args:
        n: Upper limit
        
    Returns:
        Sum of squares from 0 to n-1
    """
    # Generator expression passed directly to sum()
    return sum(x ** 2 for x in range(n))  # ← No parentheses needed


def max_of_transformed(numbers: list[int]) -> int:
    """
    Find maximum of transformed values.
    
    Args:
        numbers: List of numbers
        
    Returns:
        Maximum transformed value
    """
    # Generator expression in max()
    return max(x * 2 + 1 for x in numbers)


# ============================================================================
# FILTERING WITH GENERATOR EXPRESSIONS
# ============================================================================

def even_squares(n: int) -> Iterator[int]:
    """
    Generator expression for even squares.
    
    Args:
        n: Upper limit
        
    Returns:
        Generator of even squares
    """
    return (x ** 2 for x in range(n) if x % 2 == 0)  # ← With filter


def filtered_and_transformed(data: list[str]) -> Iterator[str]:
    """
    Filter and transform strings.
    
    Args:
        data: List of strings
        
    Returns:
        Generator of uppercase non-empty strings
    """
    return (s.upper() for s in data if s)  # ← Filter and transform


# ============================================================================
# NESTED GENERATOR EXPRESSIONS
# ============================================================================

def flatten(matrix: list[list[int]]) -> Iterator[int]:
    """
    Flatten 2D matrix using generator expression.
    
    Args:
        matrix: 2D list
        
    Returns:
        Generator of flattened values
    """
    return (item for row in matrix for item in row)  # ← Nested iteration


def cartesian_product(list1: list, list2: list) -> Iterator[tuple]:
    """
    Cartesian product using generator expression.
    
    Args:
        list1: First list
        list2: Second list
        
    Returns:
        Generator of tuples (a, b)
    """
    return ((a, b) for a in list1 for b in list2)  # ← Nested loops


# ============================================================================
# ITERATOR PROTOCOL
# ============================================================================

class CountDown:
    """
    Custom iterator that counts down.
    
    Implements iterator protocol: __iter__() and __next__()
    """
    
    def __init__(self, start: int):
        """
        Initialize countdown.
        
        Args:
            start: Starting number
        """
        self.current = start
    
    def __iter__(self) -> Iterator[int]:
        """
        Return iterator object (self).
        
        Returns:
            Iterator
        """
        return self  # ← Return self
    
    def __next__(self) -> int:
        """
        Get next value.
        
        Returns:
            Next countdown value
            
        Raises:
            StopIteration: When countdown reaches 0
        """
        if self.current <= 0:
            raise StopIteration  # ← Signal end of iteration
        
        value = self.current
        self.current -= 1
        return value


class Range:
    """
    Custom range iterator.
    
    Mimics built-in range() using iterator protocol.
    """
    
    def __init__(self, start: int, stop: int, step: int = 1):
        """
        Initialize range.
        
        Args:
            start: Starting value
            stop: Stopping value (exclusive)
            step: Step size
        """
        self.current = start
        self.stop = stop
        self.step = step
    
    def __iter__(self) -> Iterator[int]:
        """Return iterator."""
        return self
    
    def __next__(self) -> int:
        """Get next value."""
        if self.current >= self.stop:
            raise StopIteration
        
        value = self.current
        self.current += self.step
        return value


# ============================================================================
# ITERABLE VS ITERATOR
# ============================================================================

class Fibonacci:
    """
    Iterable that produces Fibonacci sequence.

    Iterable: has __iter__() that returns iterator
    Iterator: has __iter__() and __next__()
    """

    def __init__(self, max_count: int):
        """
        Initialize Fibonacci iterable.

        Args:
            max_count: Maximum number of values to generate
        """
        self.max_count = max_count

    def __iter__(self) -> Iterator[int]:
        """
        Return new iterator.

        Returns:
            FibonacciIterator instance
        """
        return FibonacciIterator(self.max_count)  # ← Return new iterator


class FibonacciIterator:
    """Iterator for Fibonacci sequence."""

    def __init__(self, max_count: int):
        """Initialize iterator."""
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1

    def __iter__(self) -> Iterator[int]:
        """Return self."""
        return self

    def __next__(self) -> int:
        """Get next Fibonacci number."""
        if self.count >= self.max_count:
            raise StopIteration

        value = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return value


# ============================================================================
# USING iter() AND next()
# ============================================================================

def demonstrate_iter_next() -> None:
    """Demonstrate iter() and next() built-in functions."""

    # Create iterator from list
    numbers = [1, 2, 3, 4, 5]
    iterator = iter(numbers)  # ← Get iterator

    print("Using next():")
    print(f"  {next(iterator)}")  # 1
    print(f"  {next(iterator)}")  # 2
    print(f"  {next(iterator)}")  # 3

    print("\nRemaining values:")
    for value in iterator:  # Continue from where we left off
        print(f"  {value}")


# ============================================================================
# GENERATOR EXPRESSION PIPELINES
# ============================================================================

def pipeline_example(data: list[int]) -> Iterator[int]:
    """
    Create pipeline of generator expressions.

    Args:
        data: Input data

    Returns:
        Generator of processed values
    """
    # Step 1: Filter even numbers
    evens = (x for x in data if x % 2 == 0)

    # Step 2: Square them
    squares = (x ** 2 for x in evens)

    # Step 3: Filter values > 10
    filtered = (x for x in squares if x > 10)

    return filtered


# ============================================================================
# DEMONSTRATION: Generator Expressions and Iterators
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("GENERATOR EXPRESSIONS AND ITERATORS")
    print("=" * 70)

    # ========================================================================
    # Generator Expressions vs List Comprehensions
    # ========================================================================
    print("\n" + "=" * 70)
    print("1. GENERATOR EXPRESSIONS VS LIST COMPREHENSIONS")
    print("=" * 70)

    demonstrate_generator_expressions()

    # ========================================================================
    # Generator Expressions in Functions
    # ========================================================================
    print("\n" + "=" * 70)
    print("2. GENERATOR EXPRESSIONS IN FUNCTIONS")
    print("=" * 70)

    print("\nsum_of_squares(10):")
    result = sum_of_squares(10)
    print(f"  Result: {result}")

    print("\nmax_of_transformed([1, 2, 3, 4, 5]):")
    result = max_of_transformed([1, 2, 3, 4, 5])
    print(f"  Result: {result}")

    # ========================================================================
    # Filtering with Generator Expressions
    # ========================================================================
    print("\n" + "=" * 70)
    print("3. FILTERING WITH GENERATOR EXPRESSIONS")
    print("=" * 70)

    print("\nEven squares up to 10:")
    for value in even_squares(10):
        print(f"  {value}", end=" ")
    print()

    print("\nFiltered and transformed strings:")
    data = ["hello", "", "world", "python", ""]
    for value in filtered_and_transformed(data):
        print(f"  {value}", end=" ")
    print()

    # ========================================================================
    # Nested Generator Expressions
    # ========================================================================
    print("\n" + "=" * 70)
    print("4. NESTED GENERATOR EXPRESSIONS")
    print("=" * 70)

    print("\nFlattening matrix:")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(f"  Matrix: {matrix}")
    print(f"  Flattened: {list(flatten(matrix))}")

    print("\nCartesian product:")
    list1 = [1, 2, 3]
    list2 = ['a', 'b']
    print(f"  {list1} × {list2}")
    for pair in cartesian_product(list1, list2):
        print(f"    {pair}")

    # ========================================================================
    # Iterator Protocol
    # ========================================================================
    print("\n" + "=" * 70)
    print("5. ITERATOR PROTOCOL")
    print("=" * 70)

    print("\nCountDown iterator:")
    countdown = CountDown(5)
    for value in countdown:
        print(f"  {value}", end=" ")
    print()

    print("\nCustom Range iterator:")
    custom_range = Range(0, 10, 2)
    for value in custom_range:
        print(f"  {value}", end=" ")
    print()

    # ========================================================================
    # Iterable vs Iterator
    # ========================================================================
    print("\n" + "=" * 70)
    print("6. ITERABLE VS ITERATOR")
    print("=" * 70)

    print("\nFibonacci iterable (can iterate multiple times):")
    fib = Fibonacci(10)

    print("First iteration:")
    for value in fib:
        print(f"  {value}", end=" ")
    print()

    print("Second iteration (works because iterable returns new iterator):")
    for value in fib:
        print(f"  {value}", end=" ")
    print()

    # ========================================================================
    # Using iter() and next()
    # ========================================================================
    print("\n" + "=" * 70)
    print("7. USING iter() AND next()")
    print("=" * 70)

    demonstrate_iter_next()

    # ========================================================================
    # Generator Expression Pipelines
    # ========================================================================
    print("\n" + "=" * 70)
    print("8. GENERATOR EXPRESSION PIPELINES")
    print("=" * 70)

    print("\nPipeline: filter evens -> square -> filter > 10")
    data = list(range(1, 11))
    print(f"  Input: {data}")
    result = list(pipeline_example(data))
    print(f"  Output: {result}")

    # ========================================================================
    # Memory Comparison
    # ========================================================================
    print("\n" + "=" * 70)
    print("9. MEMORY COMPARISON")
    print("=" * 70)

    n = 10000

    print(f"\nList comprehension for {n} items:")
    list_comp = [x ** 2 for x in range(n)]
    print(f"  Memory: {sys.getsizeof(list_comp):,} bytes")

    print(f"\nGenerator expression for {n} items:")
    gen_expr = (x ** 2 for x in range(n))
    print(f"  Memory: {sys.getsizeof(gen_expr):,} bytes")

    print(f"\nMemory savings: {sys.getsizeof(list_comp) / sys.getsizeof(gen_expr):.1f}x")

    print("\n" + "=" * 70)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Generator expressions: (expr for item in iterable)")
    print("2. Similar to list comprehensions but lazy (on-demand)")
    print("3. Much more memory-efficient than list comprehensions")
    print("4. Can be used directly in functions like sum(), max(), etc.")
    print("5. Iterator protocol: __iter__() and __next__()")
    print("6. Iterable: has __iter__() that returns iterator")
    print("7. Iterator: has __iter__() and __next__()")
    print("8. Use iter() to get iterator, next() to get next value")
    print("9. Generator expressions can be chained for pipelines")
    print("10. StopIteration signals end of iteration")
    print("=" * 70)
