"""
Example: Lambda Functions
Demonstrates anonymous functions (lambda expressions).

Lambda functions are small, anonymous functions defined with the lambda keyword.
Syntax: lambda arguments: expression

Key Concepts:
- Single expression only (no statements)
- Implicit return (no return keyword)
- Can have multiple arguments
- Often used with map(), filter(), sorted()
- Limited compared to regular functions
"""

from typing import Callable, List, Tuple


# ============================================================================
# BASIC LAMBDA FUNCTIONS
# ============================================================================

def basic_lambda_examples() -> dict[str, int]:
    """
    Basic lambda function examples.
    
    Returns:
        Dictionary with lambda results
    """
    # ← Simple lambda: takes x, returns x + 10
    add_10 = lambda x: x + 10
    
    # ← Lambda with multiple arguments
    multiply = lambda x, y: x * y
    
    # ← Lambda with no arguments
    get_constant = lambda: 42
    
    return {
        "add_10(5)": add_10(5),           # 15
        "multiply(3, 4)": multiply(3, 4),  # 12
        "get_constant()": get_constant()   # 42
    }


def lambda_vs_function() -> dict[str, int]:
    """
    Comparison: lambda vs regular function.
    
    Returns:
        Dictionary showing equivalence
    """
    # Regular function
    def square_func(x: int) -> int:
        return x ** 2
    
    # ← Equivalent lambda
    square_lambda = lambda x: x ** 2
    
    return {
        "function": square_func(5),  # 25
        "lambda": square_lambda(5)   # 25
    }


# ============================================================================
# LAMBDA WITH BUILT-IN FUNCTIONS
# ============================================================================

def lambda_with_map() -> list[int]:
    """
    Using lambda with map().
    
    Returns:
        List of squared numbers
    """
    numbers = [1, 2, 3, 4, 5]
    
    # ← map() applies lambda to each element
    squared = list(map(lambda x: x ** 2, numbers))
    
    return squared  # [1, 4, 9, 16, 25]


def lambda_with_filter() -> list[int]:
    """
    Using lambda with filter().
    
    Returns:
        List of even numbers
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # ← filter() keeps elements where lambda returns True
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    
    return evens  # [2, 4, 6, 8, 10]


def lambda_with_sorted() -> list[Tuple[str, int]]:
    """
    Using lambda with sorted() for custom sorting.
    
    Returns:
        Sorted list of tuples
    """
    people = [
        ("Alice", 30),
        ("Bob", 25),
        ("Charlie", 35),
        ("David", 20)
    ]
    
    # ← Sort by age (second element of tuple)
    by_age = sorted(people, key=lambda person: person[1])
    
    # ← Sort by name length
    by_name_length = sorted(people, key=lambda person: len(person[0]))
    
    return by_age


def lambda_with_reduce() -> int:
    """
    Using lambda with reduce().
    
    Returns:
        Product of all numbers
    """
    from functools import reduce
    
    numbers = [1, 2, 3, 4, 5]
    
    # ← reduce() applies lambda cumulatively
    product = reduce(lambda x, y: x * y, numbers)
    
    return product  # 1 * 2 * 3 * 4 * 5 = 120


# ============================================================================
# LAMBDA LIMITATIONS
# ============================================================================

def lambda_limitations() -> dict[str, str]:
    """
    Demonstrates lambda limitations.
    
    Returns:
        Dictionary explaining limitations
    """
    # ✅ Lambda: Single expression only
    simple = lambda x: x * 2
    
    # ❌ Cannot use statements (if/for/while as statements)
    # This won't work:
    # bad_lambda = lambda x: if x > 0: return x else: return -x
    
    # ✅ But can use conditional expression (ternary)
    absolute = lambda x: x if x > 0 else -x
    
    # ❌ Cannot have multiple statements
    # This won't work:
    # bad_lambda = lambda x: y = x * 2; return y
    
    # ✅ Regular function for complex logic
    def complex_function(x: int) -> int:
        if x > 0:
            result = x * 2
        else:
            result = x * -2
        return result
    
    return {
        "simple": str(simple(5)),
        "absolute": str(absolute(-5)),
        "complex": str(complex_function(-5))
    }


# ============================================================================
# LAMBDA IN DATA STRUCTURES
# ============================================================================

def lambda_in_dict() -> dict[str, int]:
    """
    Storing lambdas in data structures.

    Returns:
        Dictionary with operation results
    """
    # ← Dictionary of operations
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else 0
    }

    return {
        "add": operations["add"](10, 5),
        "subtract": operations["subtract"](10, 5),
        "multiply": operations["multiply"](10, 5),
        "divide": int(operations["divide"](10, 5))
    }


def lambda_in_list() -> list[int]:
    """
    List of lambda functions.

    Returns:
        List of results
    """
    # ← List of functions
    functions = [
        lambda x: x + 1,
        lambda x: x * 2,
        lambda x: x ** 2
    ]

    # Apply each function to 5
    results = [func(5) for func in functions]

    return results  # [6, 10, 25]


# ============================================================================
# LAMBDA WITH DEFAULT ARGUMENTS
# ============================================================================

def lambda_with_defaults() -> dict[str, int]:
    """
    Lambda functions with default arguments.

    Returns:
        Dictionary with results
    """
    # ← Lambda with default argument
    power = lambda x, n=2: x ** n

    return {
        "power(3)": power(3),      # 3^2 = 9 (default)
        "power(3, 3)": power(3, 3)  # 3^3 = 27
    }


# ============================================================================
# LAMBDA CLOSURES
# ============================================================================

def lambda_closure() -> list[int]:
    """
    Lambda functions as closures.

    Returns:
        List of results
    """
    # ← Lambda captures 'multiplier' from enclosing scope
    def make_multiplier(multiplier: int) -> Callable[[int], int]:
        return lambda x: x * multiplier

    times2 = make_multiplier(2)
    times5 = make_multiplier(5)

    return [times2(10), times5(10)]  # [20, 50]


def lambda_closure_pitfall() -> list[int]:
    """
    Common pitfall with lambda closures in loops.

    Returns:
        List showing the pitfall
    """
    # ❌ WRONG: All lambdas capture the same 'i'
    functions_wrong = []
    for i in range(5):
        functions_wrong.append(lambda x: x + i)  # ← Captures 'i' by reference!

    # All functions use i=4 (final value)
    wrong_results = [func(10) for func in functions_wrong]  # All return 14!

    # ✅ CORRECT: Use default argument to capture current value
    functions_correct = []
    for i in range(5):
        functions_correct.append(lambda x, i=i: x + i)  # ← Captures value

    correct_results = [func(10) for func in functions_correct]  # [10, 11, 12, 13, 14]

    return correct_results


# ============================================================================
# PRACTICAL LAMBDA EXAMPLES
# ============================================================================

def practical_sorting() -> list[dict[str, str]]:
    """
    Practical example: sorting complex data.

    Returns:
        Sorted list of dictionaries
    """
    students = [
        {"name": "Alice", "grade": 85, "age": 20},
        {"name": "Bob", "grade": 92, "age": 19},
        {"name": "Charlie", "grade": 78, "age": 21},
        {"name": "David", "grade": 92, "age": 18}
    ]

    # ← Sort by grade (descending), then by age (ascending)
    sorted_students = sorted(
        students,
        key=lambda s: (-s["grade"], s["age"])
    )

    return sorted_students


def practical_filtering() -> list[str]:
    """
    Practical example: filtering and transforming data.

    Returns:
        List of processed strings
    """
    words = ["apple", "banana", "cherry", "date", "elderberry", "fig"]

    # ← Filter words with length > 5, convert to uppercase
    long_words = list(
        map(
            lambda w: w.upper(),
            filter(lambda w: len(w) > 5, words)
        )
    )

    return long_words  # ['BANANA', 'CHERRY', 'ELDERBERRY']


def practical_grouping() -> dict[str, list[int]]:
    """
    Practical example: grouping data.

    Returns:
        Dictionary with grouped data
    """
    from itertools import groupby

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # ← Group by even/odd
    grouped = {
        key: list(group)
        for key, group in groupby(
            sorted(numbers, key=lambda x: x % 2),
            key=lambda x: "even" if x % 2 == 0 else "odd"
        )
    }

    return grouped


# ============================================================================
# DEMONSTRATION: Lambda Functions
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LAMBDA FUNCTIONS - ANONYMOUS FUNCTIONS")
    print("=" * 60)

    print("\nSyntax: lambda arguments: expression")
    print("- Single expression only")
    print("- Implicit return")
    print("- Often used with map/filter/sorted")

    # ========================================================================
    # 1. BASIC LAMBDA EXAMPLES
    # ========================================================================
    print("\n" + "=" * 60)
    print("1. BASIC LAMBDA EXAMPLES:")
    print("=" * 60)

    results = basic_lambda_examples()
    for key, value in results.items():
        print(f"   {key} = {value}")
    print("   ← Lambda: anonymous function")

    # ========================================================================
    # 2. LAMBDA VS FUNCTION
    # ========================================================================
    print("\n" + "=" * 60)
    print("2. LAMBDA VS FUNCTION:")
    print("=" * 60)

    results = lambda_vs_function()
    for key, value in results.items():
        print(f"   {key}: {value}")
    print("   ← Both produce same result")

    # ========================================================================
    # 3. LAMBDA WITH MAP
    # ========================================================================
    print("\n" + "=" * 60)
    print("3. LAMBDA WITH MAP:")
    print("=" * 60)

    result = lambda_with_map()
    print(f"   Squared: {result}")
    print("   ← map() applies lambda to each element")

    # ========================================================================
    # 4. LAMBDA WITH FILTER
    # ========================================================================
    print("\n" + "=" * 60)
    print("4. LAMBDA WITH FILTER:")
    print("=" * 60)

    result = lambda_with_filter()
    print(f"   Even numbers: {result}")
    print("   ← filter() keeps elements where lambda returns True")

    # ========================================================================
    # 5. LAMBDA WITH SORTED
    # ========================================================================
    print("\n" + "=" * 60)
    print("5. LAMBDA WITH SORTED:")
    print("=" * 60)

    result = lambda_with_sorted()
    for person in result:
        print(f"   {person}")
    print("   ← sorted() uses lambda as key function")

    # ========================================================================
    # 6. LAMBDA WITH REDUCE
    # ========================================================================
    print("\n" + "=" * 60)
    print("6. LAMBDA WITH REDUCE:")
    print("=" * 60)

    result = lambda_with_reduce()
    print(f"   Product: {result}")
    print("   ← reduce() applies lambda cumulatively")

    # ========================================================================
    # 7. LAMBDA LIMITATIONS
    # ========================================================================
    print("\n" + "=" * 60)
    print("7. LAMBDA LIMITATIONS:")
    print("=" * 60)

    results = lambda_limitations()
    for key, value in results.items():
        print(f"   {key}: {value}")
    print("   ⚠️  Lambda limited to single expression")

    # ========================================================================
    # 8. LAMBDA IN DATA STRUCTURES
    # ========================================================================
    print("\n" + "=" * 60)
    print("8. LAMBDA IN DICT:")
    print("=" * 60)

    results = lambda_in_dict()
    for key, value in results.items():
        print(f"   {key}: {value}")
    print("   ← Store lambdas in dictionaries")

    print("\n   LAMBDA IN LIST:")
    result = lambda_in_list()
    print(f"   Results: {result}")
    print("   ← Store lambdas in lists")

    # ========================================================================
    # 9. LAMBDA WITH DEFAULTS
    # ========================================================================
    print("\n" + "=" * 60)
    print("9. LAMBDA WITH DEFAULTS:")
    print("=" * 60)

    results = lambda_with_defaults()
    for key, value in results.items():
        print(f"   {key} = {value}")
    print("   ← Lambda can have default arguments")

    # ========================================================================
    # 10. LAMBDA CLOSURES
    # ========================================================================
    print("\n" + "=" * 60)
    print("10. LAMBDA CLOSURES:")
    print("=" * 60)

    result = lambda_closure()
    print(f"   Results: {result}")
    print("   ← Lambda can be a closure")

    print("\n   CLOSURE PITFALL:")
    result = lambda_closure_pitfall()
    print(f"   Correct results: {result}")
    print("   ⚠️  Use default args to capture loop variable")

    # ========================================================================
    # 11. PRACTICAL EXAMPLES
    # ========================================================================
    print("\n" + "=" * 60)
    print("11. PRACTICAL: SORTING:")
    print("=" * 60)

    result = practical_sorting()
    for student in result:
        print(f"   {student}")
    print("   ← Sort by multiple criteria")

    print("\n   PRACTICAL: FILTERING:")
    result = practical_filtering()
    print(f"   Long words: {result}")
    print("   ← Chain filter and map")

    print("\n   PRACTICAL: GROUPING:")
    result = practical_grouping()
    for key, values in result.items():
        print(f"   {key}: {values}")
    print("   ← Group with lambda key")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Lambda = anonymous function (lambda args: expression)")
    print("2. Single expression only (no statements)")
    print("3. Implicit return (no return keyword)")
    print("4. Often used with map/filter/sorted/reduce")
    print("5. Can have multiple arguments and defaults")
    print("6. Can be stored in data structures")
    print("7. Can be closures (capture enclosing scope)")
    print("8. Pitfall: loop variables captured by reference")
    print("9. Use default args to capture loop variable value")
    print("10. For complex logic, use regular functions")
    print("=" * 60)

