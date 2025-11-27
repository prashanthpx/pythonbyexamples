"""
Example: Higher-Order Functions
Demonstrates functions as first-class objects.

Higher-order functions are functions that:
1. Take one or more functions as arguments, OR
2. Return a function as result

Key Concepts:
- Functions are first-class objects in Python
- Can be assigned to variables
- Can be passed as arguments
- Can be returned from functions
- Can be stored in data structures
"""

from typing import Callable, List, Any, Optional


# ============================================================================
# FUNCTIONS AS FIRST-CLASS OBJECTS
# ============================================================================

def greet(name: str) -> str:
    """Simple function to demonstrate first-class nature."""
    return f"Hello, {name}!"


def demonstrate_first_class() -> None:
    """
    Demonstrate that functions are first-class objects.
    
    First-class objects can be:
    - Assigned to variables
    - Passed as arguments
    - Returned from functions
    - Stored in data structures
    """
    # Assign function to variable
    say_hello = greet  # ← No parentheses! Reference, not call
    print(say_hello("Alice"))  # "Hello, Alice!"
    
    # Store in data structure
    functions = [greet, str.upper, str.lower]
    print(functions[0]("Bob"))  # "Hello, Bob!"
    
    # Function attributes
    print(greet.__name__)  # "greet"
    print(callable(greet))  # True


# ============================================================================
# FUNCTIONS AS ARGUMENTS
# ============================================================================

def apply_operation(
    x: int,
    y: int,
    operation: Callable[[int, int], int]
) -> int:
    """
    Apply an operation to two numbers.
    
    Args:
        x: First number
        y: Second number
        operation: Function that takes two ints and returns int
        
    Returns:
        Result of operation
    """
    return operation(x, y)  # ← Call the passed function


def add(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y


def multiply(x: int, y: int) -> int:
    """Multiply two numbers."""
    return x * y


def subtract(x: int, y: int) -> int:
    """Subtract two numbers."""
    return x - y


def demonstrate_function_arguments() -> None:
    """Demonstrate passing functions as arguments."""
    print(apply_operation(10, 5, add))       # 15
    print(apply_operation(10, 5, multiply))  # 50
    print(apply_operation(10, 5, subtract))  # 5
    print(apply_operation(10, 5, lambda x, y: x ** y))  # 100000


# ============================================================================
# FUNCTIONS AS RETURN VALUES
# ============================================================================

def make_multiplier(factor: int) -> Callable[[int], int]:
    """
    Create a function that multiplies by a factor.
    
    Args:
        factor: Multiplication factor
        
    Returns:
        Function that multiplies its argument by factor
    """
    def multiplier(x: int) -> int:
        return x * factor  # ← Closure captures 'factor'
    
    return multiplier  # ← Return function


def make_power(exponent: int) -> Callable[[int], int]:
    """
    Create a function that raises to a power.
    
    Args:
        exponent: Power to raise to
        
    Returns:
        Function that raises its argument to exponent
    """
    def power(base: int) -> int:
        return base ** exponent
    
    return power


def demonstrate_function_return() -> None:
    """Demonstrate returning functions."""
    times3 = make_multiplier(3)
    times5 = make_multiplier(5)
    
    print(times3(10))  # 30
    print(times5(10))  # 50
    
    square = make_power(2)
    cube = make_power(3)
    
    print(square(5))  # 25
    print(cube(5))    # 125


# ============================================================================
# CALLBACK FUNCTIONS
# ============================================================================

def process_list(
    items: List[int],
    callback: Callable[[int], None]
) -> None:
    """
    Process each item in list with callback.
    
    Args:
        items: List of integers
        callback: Function to call for each item
    """
    for item in items:
        callback(item)  # ← Call callback for each item


def process_with_result(
    items: List[int],
    processor: Callable[[int], int]
) -> List[int]:
    """
    Process each item and return results.

    Args:
        items: List of integers
        processor: Function to process each item

    Returns:
        List of processed items
    """
    return [processor(item) for item in items]


def demonstrate_callbacks() -> None:
    """Demonstrate callback functions."""
    numbers = [1, 2, 3, 4, 5]

    # Callback that prints
    print("Processing with print callback:")
    process_list(numbers, lambda x: print(f"  Item: {x}"))

    # Callback that processes and returns
    doubled = process_with_result(numbers, lambda x: x * 2)
    print(f"Doubled: {doubled}")


# ============================================================================
# FUNCTION COMPOSITION
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


def demonstrate_composition() -> None:
    """Demonstrate function composition."""
    # Simple functions
    add_10 = lambda x: x + 10
    multiply_2 = lambda x: x * 2

    # Compose: first multiply by 2, then add 10
    composed = compose(add_10, multiply_2)
    print(composed(5))  # (5 * 2) + 10 = 20

    # Reverse order: first add 10, then multiply by 2
    composed_reverse = compose(multiply_2, add_10)
    print(composed_reverse(5))  # (5 + 10) * 2 = 30


# ============================================================================
# FUNCTION FACTORIES
# ============================================================================

def make_validator(
    min_value: int,
    max_value: int
) -> Callable[[int], bool]:
    """
    Create a validator function.

    Args:
        min_value: Minimum valid value
        max_value: Maximum valid value

    Returns:
        Validator function
    """
    def validate(value: int) -> bool:
        return min_value <= value <= max_value

    return validate


def make_formatter(
    prefix: str,
    suffix: str
) -> Callable[[str], str]:
    """
    Create a formatter function.

    Args:
        prefix: String to prepend
        suffix: String to append

    Returns:
        Formatter function
    """
    def format_string(text: str) -> str:
        return f"{prefix}{text}{suffix}"

    return format_string


def demonstrate_factories() -> None:
    """Demonstrate function factories."""
    # Validators
    is_valid_age = make_validator(0, 120)
    is_valid_percentage = make_validator(0, 100)

    print(is_valid_age(25))    # True
    print(is_valid_age(150))   # False
    print(is_valid_percentage(50))   # True
    print(is_valid_percentage(150))  # False

    # Formatters
    html_bold = make_formatter("<b>", "</b>")
    html_italic = make_formatter("<i>", "</i>")

    print(html_bold("Hello"))    # <b>Hello</b>
    print(html_italic("World"))  # <i>World</i>


# ============================================================================
# SORTING WITH CUSTOM KEY FUNCTIONS
# ============================================================================

def sort_by_key(
    items: List[Any],
    key_func: Callable[[Any], Any],
    reverse: bool = False
) -> List[Any]:
    """
    Sort items using custom key function.

    Args:
        items: List to sort
        key_func: Function to extract sort key
        reverse: Sort in reverse order

    Returns:
        Sorted list
    """
    return sorted(items, key=key_func, reverse=reverse)


def demonstrate_sorting() -> None:
    """Demonstrate sorting with key functions."""
    # Sort strings by length
    words = ["apple", "pie", "banana", "cherry"]
    by_length = sort_by_key(words, len)
    print(f"By length: {by_length}")

    # Sort tuples by second element
    people = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]
    by_age = sort_by_key(people, lambda p: p[1])
    print(f"By age: {by_age}")

    # Sort by multiple criteria
    students = [
        {"name": "Alice", "grade": 85, "age": 20},
        {"name": "Bob", "grade": 92, "age": 19},
        {"name": "Charlie", "grade": 85, "age": 21}
    ]

    # Sort by grade (descending), then by age (ascending)
    by_grade_age = sorted(
        students,
        key=lambda s: (-s["grade"], s["age"])
    )
    print(f"By grade and age: {by_grade_age}")


# ============================================================================
# FILTERING WITH PREDICATES
# ============================================================================

def filter_by_predicate(
    items: List[Any],
    predicate: Callable[[Any], bool]
) -> List[Any]:
    """
    Filter items using predicate function.

    Args:
        items: List to filter
        predicate: Function that returns True for items to keep

    Returns:
        Filtered list
    """
    return [item for item in items if predicate(item)]


def demonstrate_filtering() -> None:
    """Demonstrate filtering with predicates."""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Filter even numbers
    evens = filter_by_predicate(numbers, lambda x: x % 2 == 0)
    print(f"Evens: {evens}")

    # Filter numbers > 5
    greater_than_5 = filter_by_predicate(numbers, lambda x: x > 5)
    print(f"Greater than 5: {greater_than_5}")

    # Filter strings by length
    words = ["apple", "pie", "banana", "cherry", "kiwi"]
    long_words = filter_by_predicate(words, lambda w: len(w) > 5)
    print(f"Long words: {long_words}")


# ============================================================================
# TRANSFORMING WITH MAPPERS
# ============================================================================

def transform_list(
    items: List[Any],
    transformer: Callable[[Any], Any]
) -> List[Any]:
    """
    Transform each item in list.

    Args:
        items: List to transform
        transformer: Function to transform each item

    Returns:
        Transformed list
    """
    return [transformer(item) for item in items]


def demonstrate_transforming() -> None:
    """Demonstrate transforming with mapper functions."""
    numbers = [1, 2, 3, 4, 5]

    # Square each number
    squared = transform_list(numbers, lambda x: x ** 2)
    print(f"Squared: {squared}")

    # Convert to strings
    strings = transform_list(numbers, str)
    print(f"Strings: {strings}")

    # Complex transformation
    people = [("Alice", 30), ("Bob", 25)]
    formatted = transform_list(
        people,
        lambda p: f"{p[0]} is {p[1]} years old"
    )
    print(f"Formatted: {formatted}")


# ============================================================================
# CHAINING OPERATIONS
# ============================================================================

def chain_operations(
    items: List[int],
    *operations: Callable[[List[int]], List[int]]
) -> List[int]:
    """
    Chain multiple operations on a list.

    Args:
        items: Initial list
        *operations: Variable number of operations to apply

    Returns:
        Result after all operations
    """
    result = items
    for operation in operations:
        result = operation(result)  # ← Apply each operation
    return result


def demonstrate_chaining() -> None:
    """Demonstrate chaining operations."""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Define operations
    filter_evens = lambda lst: [x for x in lst if x % 2 == 0]
    double = lambda lst: [x * 2 for x in lst]
    take_first_3 = lambda lst: lst[:3]

    # Chain operations
    result = chain_operations(
        numbers,
        filter_evens,   # [2, 4, 6, 8, 10]
        double,         # [4, 8, 12, 16, 20]
        take_first_3    # [4, 8, 12]
    )
    print(f"Chained result: {result}")


# ============================================================================
# CONDITIONAL EXECUTION
# ============================================================================

def execute_if(
    condition: bool,
    true_func: Callable[[], Any],
    false_func: Optional[Callable[[], Any]] = None
) -> Any:
    """
    Execute function based on condition.

    Args:
        condition: Condition to check
        true_func: Function to execute if True
        false_func: Function to execute if False (optional)

    Returns:
        Result of executed function
    """
    if condition:
        return true_func()
    elif false_func:
        return false_func()
    return None


def demonstrate_conditional() -> None:
    """Demonstrate conditional execution."""
    age = 25

    result = execute_if(
        age >= 18,
        lambda: "Adult",
        lambda: "Minor"
    )
    print(f"Status: {result}")


# ============================================================================
# MEMOIZATION WITH HIGHER-ORDER FUNCTION
# ============================================================================

def memoize(func: Callable) -> Callable:
    """
    Create memoized version of function.

    Args:
        func: Function to memoize

    Returns:
        Memoized function
    """
    cache = {}  # ← Cache for results

    def memoized(*args):
        if args not in cache:
            cache[args] = func(*args)  # ← Compute and cache
        return cache[args]  # ← Return cached result

    memoized.cache = cache  # ← Expose cache
    return memoized


def demonstrate_memoization() -> None:
    """Demonstrate memoization."""
    # Expensive function
    def fibonacci(n: int) -> int:
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    # Memoized version
    fib_memo = memoize(fibonacci)

    print(f"fib(10) = {fib_memo(10)}")
    print(f"Cache size: {len(fib_memo.cache)}")


# ============================================================================
# RETRY DECORATOR (HIGHER-ORDER FUNCTION)
# ============================================================================

def retry(max_attempts: int) -> Callable:
    """
    Create retry wrapper for functions.

    Args:
        max_attempts: Maximum number of attempts

    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator


def demonstrate_retry() -> None:
    """Demonstrate retry pattern."""
    attempts = 0

    @retry(3)
    def unreliable_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError(f"Attempt {attempts} failed")
        return "Success!"

    result = unreliable_function()
    print(f"Result: {result}")


# ============================================================================
# DEMONSTRATION: Higher-Order Functions
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("HIGHER-ORDER FUNCTIONS")
    print("=" * 60)

    print("\nHigher-order functions:")
    print("  - Take functions as arguments")
    print("  - Return functions as results")
    print("  - Enable powerful abstractions")

    # ========================================================================
    # 1. FIRST-CLASS OBJECTS
    # ========================================================================
    print("\n" + "=" * 60)
    print("1. FUNCTIONS AS FIRST-CLASS OBJECTS:")
    print("=" * 60)
    demonstrate_first_class()
    print("   ← Functions can be assigned, passed, returned, stored")

    # ========================================================================
    # 2. FUNCTIONS AS ARGUMENTS
    # ========================================================================
    print("\n" + "=" * 60)
    print("2. FUNCTIONS AS ARGUMENTS:")
    print("=" * 60)
    demonstrate_function_arguments()
    print("   ← Pass different operations to same function")

    # ========================================================================
    # 3. FUNCTIONS AS RETURN VALUES
    # ========================================================================
    print("\n" + "=" * 60)
    print("3. FUNCTIONS AS RETURN VALUES:")
    print("=" * 60)
    demonstrate_function_return()
    print("   ← Create specialized functions dynamically")

    # ========================================================================
    # 4. CALLBACKS
    # ========================================================================
    print("\n" + "=" * 60)
    print("4. CALLBACK FUNCTIONS:")
    print("=" * 60)
    demonstrate_callbacks()
    print("   ← Execute custom logic for each item")

    # ========================================================================
    # 5. FUNCTION COMPOSITION
    # ========================================================================
    print("\n" + "=" * 60)
    print("5. FUNCTION COMPOSITION:")
    print("=" * 60)
    demonstrate_composition()
    print("   ← Combine functions to create new functions")

    # ========================================================================
    # 6. FUNCTION FACTORIES
    # ========================================================================
    print("\n" + "=" * 60)
    print("6. FUNCTION FACTORIES:")
    print("=" * 60)
    demonstrate_factories()
    print("   ← Create configured functions")

    # ========================================================================
    # 7. SORTING WITH KEY FUNCTIONS
    # ========================================================================
    print("\n" + "=" * 60)
    print("7. SORTING WITH KEY FUNCTIONS:")
    print("=" * 60)
    demonstrate_sorting()
    print("   ← Custom sorting logic")

    # ========================================================================
    # 8. FILTERING WITH PREDICATES
    # ========================================================================
    print("\n" + "=" * 60)
    print("8. FILTERING WITH PREDICATES:")
    print("=" * 60)
    demonstrate_filtering()
    print("   ← Select items based on condition")

    # ========================================================================
    # 9. TRANSFORMING WITH MAPPERS
    # ========================================================================
    print("\n" + "=" * 60)
    print("9. TRANSFORMING WITH MAPPERS:")
    print("=" * 60)
    demonstrate_transforming()
    print("   ← Transform each item")

    # ========================================================================
    # 10. CHAINING OPERATIONS
    # ========================================================================
    print("\n" + "=" * 60)
    print("10. CHAINING OPERATIONS:")
    print("=" * 60)
    demonstrate_chaining()
    print("   ← Apply multiple operations in sequence")

    # ========================================================================
    # 11. CONDITIONAL EXECUTION
    # ========================================================================
    print("\n" + "=" * 60)
    print("11. CONDITIONAL EXECUTION:")
    print("=" * 60)
    demonstrate_conditional()
    print("   ← Execute different functions based on condition")

    # ========================================================================
    # 12. MEMOIZATION
    # ========================================================================
    print("\n" + "=" * 60)
    print("12. MEMOIZATION:")
    print("=" * 60)
    demonstrate_memoization()
    print("   ← Cache function results")

    # ========================================================================
    # 13. RETRY PATTERN
    # ========================================================================
    print("\n" + "=" * 60)
    print("13. RETRY PATTERN:")
    print("=" * 60)
    demonstrate_retry()
    print("   ← Retry failed operations")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Functions are first-class objects in Python")
    print("2. Higher-order functions take/return functions")
    print("3. Callbacks enable custom behavior")
    print("4. Function composition creates new functions")
    print("5. Factories create configured functions")
    print("6. Key functions enable custom sorting")
    print("7. Predicates enable custom filtering")
    print("8. Mappers enable custom transformations")
    print("9. Chaining enables pipeline processing")
    print("10. Memoization caches expensive computations")
    print("11. Higher-order functions enable abstraction")
    print("12. Use type hints for function parameters")
    print("=" * 60)


