"""
Example: Memoization and Caching
Demonstrates memoization techniques for optimization.

Key Concepts:
- Memoization: cache function results
- Cache: store computed values to avoid recomputation
- functools.lru_cache: built-in LRU cache decorator
- functools.cache: unlimited cache (Python 3.9+)
- Manual caching: custom cache implementation

When to Use:
- Expensive computations
- Pure functions (same input -> same output)
- Recursive functions with overlapping subproblems
"""

from functools import lru_cache, cache
from typing import Callable, Any
import time


# ============================================================================
# PROBLEM: SLOW RECURSIVE FIBONACCI
# ============================================================================

def fibonacci_slow(n: int) -> int:
    """
    Slow Fibonacci (exponential time complexity).
    
    Args:
        n: Position in sequence
        
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    return fibonacci_slow(n - 1) + fibonacci_slow(n - 2)  # ← Recomputes values


# ============================================================================
# SOLUTION 1: MANUAL MEMOIZATION
# ============================================================================

def fibonacci_manual_memo(n: int, memo: dict = None) -> int:
    """
    Fibonacci with manual memoization.
    
    Args:
        n: Position in sequence
        memo: Cache dictionary
        
    Returns:
        nth Fibonacci number
    """
    if memo is None:
        memo = {}
    
    # Check cache
    if n in memo:
        return memo[n]  # ← Return cached value
    
    # Base cases
    if n <= 1:
        return n
    
    # Compute and cache
    result = fibonacci_manual_memo(n - 1, memo) + fibonacci_manual_memo(n - 2, memo)
    memo[n] = result  # ← Store in cache
    
    return result


# ============================================================================
# SOLUTION 2: DECORATOR-BASED MEMOIZATION
# ============================================================================

def memoize(func: Callable) -> Callable:
    """
    Memoization decorator.
    
    Args:
        func: Function to memoize
        
    Returns:
        Memoized function
    """
    cache = {}  # ← Cache storage
    
    def wrapper(*args):
        if args in cache:
            return cache[args]  # ← Cache hit
        
        result = func(*args)
        cache[args] = result  # ← Cache miss, store result
        return result
    
    wrapper.cache = cache  # ← Expose cache for inspection
    return wrapper


@memoize
def fibonacci_decorator(n: int) -> int:
    """Fibonacci with decorator memoization."""
    if n <= 1:
        return n
    return fibonacci_decorator(n - 1) + fibonacci_decorator(n - 2)


# ============================================================================
# SOLUTION 3: functools.lru_cache
# ============================================================================

@lru_cache(maxsize=128)  # ← LRU cache with max 128 entries
def fibonacci_lru(n: int) -> int:
    """
    Fibonacci with LRU cache.
    
    Args:
        n: Position in sequence
        
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


@lru_cache(maxsize=None)  # ← Unlimited cache
def factorial_lru(n: int) -> int:
    """Factorial with unlimited LRU cache."""
    if n <= 1:
        return 1
    return n * factorial_lru(n - 1)


# ============================================================================
# SOLUTION 4: functools.cache (Python 3.9+)
# ============================================================================

try:
    @cache  # ← Simpler syntax, unlimited cache
    def fibonacci_cache(n: int) -> int:
        """Fibonacci with @cache decorator."""
        if n <= 1:
            return n
        return fibonacci_cache(n - 1) + fibonacci_cache(n - 2)
except NameError:
    # Fallback for Python < 3.9
    fibonacci_cache = lru_cache(maxsize=None)(fibonacci_lru)


# ============================================================================
# MEMOIZATION WITH MULTIPLE ARGUMENTS
# ============================================================================

@lru_cache(maxsize=256)
def binomial_coefficient(n: int, k: int) -> int:
    """
    Calculate binomial coefficient C(n, k).
    
    Args:
        n: Total items
        k: Items to choose
        
    Returns:
        C(n, k) = n! / (k! * (n-k)!)
    """
    if k == 0 or k == n:
        return 1
    return binomial_coefficient(n - 1, k - 1) + binomial_coefficient(n - 1, k)


# ============================================================================
# CACHE STATISTICS AND MANAGEMENT
# ============================================================================

@lru_cache(maxsize=128)
def expensive_computation(x: int, y: int) -> int:
    """Simulate expensive computation."""
    time.sleep(0.01)  # Simulate work
    return x ** y


def demonstrate_cache_stats() -> None:
    """Demonstrate cache statistics."""

    # Clear cache
    expensive_computation.cache_clear()

    print("Computing values:")
    for i in range(5):
        result = expensive_computation(2, i)
        print(f"  2^{i} = {result}")

    # Check cache stats
    stats = expensive_computation.cache_info()
    print(f"\nCache statistics:")
    print(f"  Hits: {stats.hits}")
    print(f"  Misses: {stats.misses}")
    print(f"  Size: {stats.currsize}")
    print(f"  Max size: {stats.maxsize}")

    # Recompute (should hit cache)
    print("\nRecomputing (should hit cache):")
    for i in range(5):
        result = expensive_computation(2, i)

    stats = expensive_computation.cache_info()
    print(f"\nUpdated statistics:")
    print(f"  Hits: {stats.hits}")
    print(f"  Misses: {stats.misses}")


# ============================================================================
# MEMOIZATION FOR EXPENSIVE OPERATIONS
# ============================================================================

@lru_cache(maxsize=1000)
def is_prime(n: int) -> bool:
    """
    Check if number is prime (memoized).

    Args:
        n: Number to check

    Returns:
        True if prime
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False

    return True


@lru_cache(maxsize=100)
def nth_prime(n: int) -> int:
    """
    Find nth prime number (memoized).

    Args:
        n: Position (1-indexed)

    Returns:
        nth prime number
    """
    count = 0
    num = 2

    while count < n:
        if is_prime(num):
            count += 1
            if count == n:
                return num
        num += 1

    return -1


# ============================================================================
# CLASS-BASED MEMOIZATION
# ============================================================================

class Memoized:
    """Class-based memoization."""

    def __init__(self, func: Callable):
        """Initialize with function."""
        self.func = func
        self.cache = {}

    def __call__(self, *args: Any) -> Any:
        """Call with memoization."""
        if args in self.cache:
            return self.cache[args]

        result = self.func(*args)
        self.cache[args] = result
        return result

    def clear_cache(self) -> None:
        """Clear the cache."""
        self.cache.clear()


@Memoized
def fibonacci_class(n: int) -> int:
    """Fibonacci with class-based memoization."""
    if n <= 1:
        return n
    return fibonacci_class(n - 1) + fibonacci_class(n - 2)


# ============================================================================
# DEMONSTRATION: Memoization
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("MEMOIZATION AND CACHING")
    print("=" * 70)

    # ========================================================================
    # Problem: Slow Fibonacci
    # ========================================================================
    print("\n" + "=" * 70)
    print("1. PROBLEM: SLOW RECURSIVE FIBONACCI")
    print("=" * 70)

    print("\nComputing fibonacci_slow(30):")
    start = time.time()
    result = fibonacci_slow(30)
    elapsed = time.time() - start
    print(f"  Result: {result}")
    print(f"  Time: {elapsed:.4f}s")

    # ========================================================================
    # Solution 1: Manual Memoization
    # ========================================================================
    print("\n" + "=" * 70)
    print("2. SOLUTION 1: MANUAL MEMOIZATION")
    print("=" * 70)

    print("\nComputing fibonacci_manual_memo(30):")
    start = time.time()
    result = fibonacci_manual_memo(30)
    elapsed = time.time() - start
    print(f"  Result: {result}")
    print(f"  Time: {elapsed:.4f}s")
    print(f"  Speedup: {(time.time() - start) / elapsed:.0f}x faster")

    # ========================================================================
    # Solution 2: Decorator Memoization
    # ========================================================================
    print("\n" + "=" * 70)
    print("3. SOLUTION 2: DECORATOR MEMOIZATION")
    print("=" * 70)

    print("\nComputing fibonacci_decorator(30):")
    start = time.time()
    result = fibonacci_decorator(30)
    elapsed = time.time() - start
    print(f"  Result: {result}")
    print(f"  Time: {elapsed:.4f}s")
    print(f"  Cache size: {len(fibonacci_decorator.cache)}")

    # ========================================================================
    # Solution 3: LRU Cache
    # ========================================================================
    print("\n" + "=" * 70)
    print("4. SOLUTION 3: functools.lru_cache")
    print("=" * 70)

    print("\nComputing fibonacci_lru(30):")
    start = time.time()
    result = fibonacci_lru(30)
    elapsed = time.time() - start
    print(f"  Result: {result}")
    print(f"  Time: {elapsed:.4f}s")

    stats = fibonacci_lru.cache_info()
    print(f"  Cache hits: {stats.hits}")
    print(f"  Cache misses: {stats.misses}")

    # ========================================================================
    # Multiple Arguments
    # ========================================================================
    print("\n" + "=" * 70)
    print("5. MEMOIZATION WITH MULTIPLE ARGUMENTS")
    print("=" * 70)

    print("\nBinomial coefficients:")
    for n in [10, 20, 30]:
        k = n // 2
        result = binomial_coefficient(n, k)
        print(f"  C({n}, {k}) = {result}")

    stats = binomial_coefficient.cache_info()
    print(f"\nCache statistics:")
    print(f"  Hits: {stats.hits}, Misses: {stats.misses}")

    # ========================================================================
    # Cache Statistics
    # ========================================================================
    print("\n" + "=" * 70)
    print("6. CACHE STATISTICS AND MANAGEMENT")
    print("=" * 70)

    demonstrate_cache_stats()

    # ========================================================================
    # Expensive Operations
    # ========================================================================
    print("\n" + "=" * 70)
    print("7. MEMOIZATION FOR EXPENSIVE OPERATIONS")
    print("=" * 70)

    print("\nFinding primes:")
    for i in [1, 10, 100, 1000]:
        prime = nth_prime(i)
        print(f"  Prime #{i}: {prime}")

    # ========================================================================
    # Class-Based Memoization
    # ========================================================================
    print("\n" + "=" * 70)
    print("8. CLASS-BASED MEMOIZATION")
    print("=" * 70)

    print("\nComputing fibonacci_class(35):")
    start = time.time()
    result = fibonacci_class(35)
    elapsed = time.time() - start
    print(f"  Result: {result}")
    print(f"  Time: {elapsed:.4f}s")
    print(f"  Cache size: {len(fibonacci_class.cache)}")

    print("\n" + "=" * 70)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Memoization: cache function results to avoid recomputation")
    print("2. Use for: expensive computations, recursive functions")
    print("3. @lru_cache: built-in LRU cache decorator")
    print("4. @cache: unlimited cache (Python 3.9+)")
    print("5. maxsize=None: unlimited cache")
    print("6. maxsize=128: default LRU cache size")
    print("7. cache_info(): get cache statistics")
    print("8. cache_clear(): clear the cache")
    print("9. Only works with hashable arguments")
    print("10. Massive speedup for recursive functions (exponential -> linear)")
    print("=" * 70)

