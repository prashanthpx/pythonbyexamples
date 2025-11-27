"""
Example: Function Composition
Demonstrates composing functions to create new functions.

Function composition combines simple functions to build complex operations:
- f ∘ g (x) = f(g(x))
- Build complex logic from simple pieces
- Reusable, testable components

Key Concepts:
- Composition operator
- Chaining functions
- Pipeline pattern
- Point-free style
"""

from typing import Callable, Any, TypeVar
from functools import reduce


T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')


# ============================================================================
# BASIC COMPOSITION
# ============================================================================

def compose(
    f: Callable[[Any], Any],
    g: Callable[[Any], Any]
) -> Callable[[Any], Any]:
    """
    Compose two functions: (f ∘ g)(x) = f(g(x))
    
    Args:
        f: Outer function
        g: Inner function
        
    Returns:
        Composed function
    """
    def composed(x: Any) -> Any:
        return f(g(x))  # ← Apply g first, then f
    
    return composed


def demonstrate_basic_composition() -> None:
    """Demonstrate basic function composition."""
    # Simple functions
    add_10 = lambda x: x + 10
    multiply_2 = lambda x: x * 2
    square = lambda x: x ** 2
    
    # Compose: (x * 2) + 10
    f1 = compose(add_10, multiply_2)
    print(f"f1(5) = {f1(5)}")  # (5 * 2) + 10 = 20
    
    # Compose: (x + 10) * 2
    f2 = compose(multiply_2, add_10)
    print(f"f2(5) = {f2(5)}")  # (5 + 10) * 2 = 30
    
    # Compose: ((x * 2) + 10)²
    f3 = compose(square, compose(add_10, multiply_2))
    print(f"f3(5) = {f3(5)}")  # ((5 * 2) + 10)² = 400


# ============================================================================
# MULTIPLE FUNCTION COMPOSITION
# ============================================================================

def compose_many(*functions: Callable) -> Callable:
    """
    Compose multiple functions.
    
    Args:
        *functions: Functions to compose (right to left)
        
    Returns:
        Composed function
    """
    def composed(x: Any) -> Any:
        # Apply functions right to left
        return reduce(lambda acc, f: f(acc), reversed(functions), x)
    
    return composed


def pipe(*functions: Callable) -> Callable:
    """
    Pipe functions (left to right composition).
    
    Args:
        *functions: Functions to pipe (left to right)
        
    Returns:
        Piped function
    """
    def piped(x: Any) -> Any:
        # Apply functions left to right
        return reduce(lambda acc, f: f(acc), functions, x)
    
    return piped


def demonstrate_multiple_composition() -> None:
    """Demonstrate composing multiple functions."""
    # Define operations
    add_5 = lambda x: x + 5
    multiply_3 = lambda x: x * 3
    subtract_2 = lambda x: x - 2
    
    # Compose (right to left): subtract_2(multiply_3(add_5(x)))
    composed = compose_many(subtract_2, multiply_3, add_5)
    print(f"compose_many(10) = {composed(10)}")
    # (10 + 5) * 3 - 2 = 43
    
    # Pipe (left to right): add_5 -> multiply_3 -> subtract_2
    piped = pipe(add_5, multiply_3, subtract_2)
    print(f"pipe(10) = {piped(10)}")
    # (10 + 5) * 3 - 2 = 43


# ============================================================================
# STRING PROCESSING PIPELINE
# ============================================================================

def demonstrate_string_pipeline() -> None:
    """Demonstrate string processing pipeline."""
    # Define string operations
    strip_whitespace = lambda s: s.strip()
    to_lowercase = lambda s: s.lower()
    remove_punctuation = lambda s: ''.join(c for c in s if c.isalnum() or c.isspace())
    collapse_spaces = lambda s: ' '.join(s.split())
    
    # Create pipeline
    normalize = pipe(
        strip_whitespace,
        to_lowercase,
        remove_punctuation,
        collapse_spaces
    )
    
    # Test
    text = "  Hello,  WORLD!!!  How are   you?  "
    result = normalize(text)
    print(f"Original: '{text}'")
    print(f"Normalized: '{result}'")


# ============================================================================
# DATA TRANSFORMATION PIPELINE
# ============================================================================

def demonstrate_data_pipeline() -> None:
    """Demonstrate data transformation pipeline."""
    # Sample data
    data = [
        {"name": "Alice", "age": 30, "score": 85},
        {"name": "Bob", "age": 25, "score": 92},
        {"name": "Charlie", "age": 35, "score": 78},
        {"name": "David", "age": 28, "score": 88}
    ]
    
    # Define transformations
    filter_passing = lambda items: [i for i in items if i["score"] >= 80]
    sort_by_score = lambda items: sorted(items, key=lambda x: x["score"], reverse=True)
    extract_names = lambda items: [i["name"] for i in items]
    
    # Create pipeline
    process = pipe(
        filter_passing,
        sort_by_score,
        extract_names
    )
    
    result = process(data)
    print(f"Top passing students: {result}")


# ============================================================================
# MATHEMATICAL COMPOSITION
# ============================================================================

def demonstrate_math_composition() -> None:
    """Demonstrate mathematical function composition."""
    import math
    
    # Mathematical functions
    sqrt = lambda x: math.sqrt(x)
    square = lambda x: x ** 2
    add_1 = lambda x: x + 1
    
    # Compose: √(x² + 1)
    f = compose(sqrt, compose(add_1, square))
    print(f"√(3² + 1) = {f(3):.2f}")  # √10 ≈ 3.16
    
    # Using pipe for clarity
    g = pipe(square, add_1, sqrt)
    print(f"3² + 1 then √ = {g(3):.2f}")  # Same result


# ============================================================================
# PARTIAL APPLICATION WITH COMPOSITION
# ============================================================================

def partial_left(func: Callable, *args) -> Callable:
    """
    Partial application from left.
    
    Args:
        func: Function to partially apply
        *args: Arguments to fix
        
    Returns:
        Partially applied function
    """
    def partial(*remaining_args):
        return func(*args, *remaining_args)
    
    return partial


def demonstrate_partial_composition() -> None:
    """Demonstrate composition with partial application."""
    # Define base functions
    add = lambda x, y: x + y
    multiply = lambda x, y: x * y
    
    # Create specialized functions
    add_10 = partial_left(add, 10)
    multiply_5 = partial_left(multiply, 5)
    
    # Compose
    f = compose(multiply_5, add_10)
    print(f"(5 + 10) * 5 = {f(5)}")  # 75


# ============================================================================
# POINT-FREE STYLE
# ============================================================================

def demonstrate_point_free() -> None:
    """
    Demonstrate point-free style (tacit programming).

    Point-free style defines functions without mentioning arguments.
    """
    # Point-ful (explicit arguments)
    def double_then_add_10_pointful(x):
        return x * 2 + 10

    # Point-free (no explicit arguments)
    double = lambda x: x * 2
    add_10 = lambda x: x + 10
    double_then_add_10_pointfree = compose(add_10, double)

    print(f"Point-ful: {double_then_add_10_pointful(5)}")
    print(f"Point-free: {double_then_add_10_pointfree(5)}")


# ============================================================================
# VALIDATION PIPELINE
# ============================================================================

def demonstrate_validation_pipeline() -> None:
    """Demonstrate validation pipeline."""
    # Validators
    def is_not_empty(s: str) -> bool:
        return len(s) > 0

    def is_email(s: str) -> bool:
        return "@" in s and "." in s

    def is_long_enough(s: str) -> bool:
        return len(s) >= 5

    # Combine validators
    def all_validators(*validators):
        def validate(value):
            return all(v(value) for v in validators)
        return validate

    # Create combined validator
    validate_email = all_validators(is_not_empty, is_email, is_long_enough)

    print(f"'alice@example.com': {validate_email('alice@example.com')}")
    print(f"'a@b.c': {validate_email('a@b.c')}")
    print(f"'': {validate_email('')}")


# ============================================================================
# DECORATOR-STYLE COMPOSITION
# ============================================================================

def trace(func: Callable) -> Callable:
    """Decorator that traces function calls."""
    def wrapper(*args, **kwargs):
        print(f"  Calling {func.__name__}({args})")
        result = func(*args, **kwargs)
        print(f"  {func.__name__} returned {result}")
        return result
    return wrapper


def demonstrate_decorator_composition() -> None:
    """Demonstrate composing decorators."""
    # Define functions
    def add_5(x):
        return x + 5

    def multiply_2(x):
        return x * 2

    # Apply tracing
    add_5_traced = trace(add_5)
    multiply_2_traced = trace(multiply_2)

    # Compose traced functions
    composed = compose(multiply_2_traced, add_5_traced)

    print("Executing composed function:")
    result = composed(10)
    print(f"Final result: {result}")


# ============================================================================
# CURRYING AND COMPOSITION
# ============================================================================

def curry2(func: Callable) -> Callable:
    """
    Curry a 2-argument function.

    Args:
        func: Function with 2 arguments

    Returns:
        Curried function
    """
    def curried(x):
        def inner(y):
            return func(x, y)
        return inner
    return curried


def demonstrate_curry_composition() -> None:
    """Demonstrate currying with composition."""
    # Define binary operations
    add = lambda x, y: x + y
    multiply = lambda x, y: x * y

    # Curry them
    add_curried = curry2(add)
    multiply_curried = curry2(multiply)

    # Create specialized functions
    add_10 = add_curried(10)
    multiply_5 = multiply_curried(5)

    # Compose
    f = compose(multiply_5, add_10)
    print(f"(5 + 10) * 5 = {f(5)}")  # 75


# ============================================================================
# PRACTICAL EXAMPLE: DATA PROCESSING
# ============================================================================

def demonstrate_practical_example() -> None:
    """Demonstrate practical data processing pipeline."""
    # Sample log data
    logs = [
        "2024-01-01 ERROR: Database connection failed",
        "2024-01-01 INFO: Application started",
        "2024-01-02 ERROR: File not found",
        "2024-01-02 WARNING: Low memory",
        "2024-01-03 ERROR: Timeout occurred"
    ]

    # Define processing steps
    filter_errors = lambda lines: [l for l in lines if "ERROR" in l]
    extract_message = lambda lines: [l.split(": ", 1)[1] for l in lines]
    to_uppercase = lambda lines: [l.upper() for l in lines]

    # Create pipeline
    process_errors = pipe(
        filter_errors,
        extract_message,
        to_uppercase
    )

    result = process_errors(logs)
    print("Error messages:")
    for msg in result:
        print(f"  - {msg}")


# ============================================================================
# FUNCTION COMPOSITION WITH TYPE SAFETY
# ============================================================================

def compose_typed(
    f: Callable[[U], V],
    g: Callable[[T], U]
) -> Callable[[T], V]:
    """
    Type-safe function composition.

    Args:
        f: Function from U to V
        g: Function from T to U

    Returns:
        Function from T to V
    """
    def composed(x: T) -> V:
        return f(g(x))

    return composed


def demonstrate_typed_composition() -> None:
    """Demonstrate type-safe composition."""
    # int -> str
    int_to_str: Callable[[int], str] = lambda x: str(x)

    # str -> int (length)
    str_to_int: Callable[[str], int] = lambda s: len(s)

    # Compose: int -> str -> int
    f = compose_typed(str_to_int, int_to_str)

    print(f"Length of str(12345): {f(12345)}")  # 5


# ============================================================================
# DEMONSTRATION: Function Composition
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("FUNCTION COMPOSITION")
    print("=" * 60)

    print("\nFunction composition:")
    print("  - Combine simple functions")
    print("  - Build complex operations")
    print("  - Reusable components")

    # ========================================================================
    # 1. BASIC COMPOSITION
    # ========================================================================
    print("\n" + "=" * 60)
    print("1. BASIC COMPOSITION:")
    print("=" * 60)
    demonstrate_basic_composition()
    print("   ← compose(f, g)(x) = f(g(x))")

    # ========================================================================
    # 2. MULTIPLE COMPOSITION
    # ========================================================================
    print("\n" + "=" * 60)
    print("2. MULTIPLE COMPOSITION:")
    print("=" * 60)
    demonstrate_multiple_composition()
    print("   ← Compose many functions")

    # ========================================================================
    # 3. STRING PIPELINE
    # ========================================================================
    print("\n" + "=" * 60)
    print("3. STRING PROCESSING PIPELINE:")
    print("=" * 60)
    demonstrate_string_pipeline()
    print("   ← Chain string transformations")

    # ========================================================================
    # 4. DATA PIPELINE
    # ========================================================================
    print("\n" + "=" * 60)
    print("4. DATA TRANSFORMATION PIPELINE:")
    print("=" * 60)
    demonstrate_data_pipeline()
    print("   ← Process data through stages")

    # ========================================================================
    # 5. MATHEMATICAL COMPOSITION
    # ========================================================================
    print("\n" + "=" * 60)
    print("5. MATHEMATICAL COMPOSITION:")
    print("=" * 60)
    demonstrate_math_composition()
    print("   ← Compose mathematical functions")

    # ========================================================================
    # 6. PARTIAL APPLICATION
    # ========================================================================
    print("\n" + "=" * 60)
    print("6. PARTIAL APPLICATION WITH COMPOSITION:")
    print("=" * 60)
    demonstrate_partial_composition()
    print("   ← Combine partial application and composition")

    # ========================================================================
    # 7. POINT-FREE STYLE
    # ========================================================================
    print("\n" + "=" * 60)
    print("7. POINT-FREE STYLE:")
    print("=" * 60)
    demonstrate_point_free()
    print("   ← Define functions without explicit arguments")

    # ========================================================================
    # 8. VALIDATION PIPELINE
    # ========================================================================
    print("\n" + "=" * 60)
    print("8. VALIDATION PIPELINE:")
    print("=" * 60)
    demonstrate_validation_pipeline()
    print("   ← Combine validators")

    # ========================================================================
    # 9. DECORATOR COMPOSITION
    # ========================================================================
    print("\n" + "=" * 60)
    print("9. DECORATOR-STYLE COMPOSITION:")
    print("=" * 60)
    demonstrate_decorator_composition()
    print("   ← Compose decorated functions")

    # ========================================================================
    # 10. CURRYING AND COMPOSITION
    # ========================================================================
    print("\n" + "=" * 60)
    print("10. CURRYING WITH COMPOSITION:")
    print("=" * 60)
    demonstrate_curry_composition()
    print("   ← Curry then compose")

    # ========================================================================
    # 11. PRACTICAL EXAMPLE
    # ========================================================================
    print("\n" + "=" * 60)
    print("11. PRACTICAL EXAMPLE - LOG PROCESSING:")
    print("=" * 60)
    demonstrate_practical_example()
    print("   ← Real-world data processing")

    # ========================================================================
    # 12. TYPED COMPOSITION
    # ========================================================================
    print("\n" + "=" * 60)
    print("12. TYPE-SAFE COMPOSITION:")
    print("=" * 60)
    demonstrate_typed_composition()
    print("   ← Composition with type safety")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Composition: (f ∘ g)(x) = f(g(x))")
    print("2. compose() applies right to left")
    print("3. pipe() applies left to right")
    print("4. Build complex from simple functions")
    print("5. Reusable, testable components")
    print("6. Point-free style omits arguments")
    print("7. Combine with partial application")
    print("8. Combine with currying")
    print("9. Use for data pipelines")
    print("10. Type hints ensure safety")
    print("11. Prefer pipe() for readability")
    print("12. Each function should do one thing")
    print("=" * 60)

