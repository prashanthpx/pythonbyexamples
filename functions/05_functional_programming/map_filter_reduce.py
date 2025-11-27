"""
Example: map(), filter(), and reduce()
Demonstrates built-in functional programming tools.

These functions enable functional-style data processing:
- map(): Transform each element
- filter(): Select elements based on condition
- reduce(): Combine elements into single value

Key Concepts:
- Lazy evaluation (map and filter return iterators)
- Functional data pipelines
- Avoiding explicit loops
- Declarative vs imperative style
"""

from functools import reduce
from typing import List, Callable, Any, Iterable, TypeVar


T = TypeVar('T')
U = TypeVar('U')


# ============================================================================
# MAP - TRANSFORM EACH ELEMENT
# ============================================================================

def demonstrate_map_basics() -> None:
    """
    Demonstrate basic map() usage.
    
    map(function, iterable) applies function to each element.
    Returns an iterator (lazy evaluation).
    """
    numbers = [1, 2, 3, 4, 5]
    
    # Square each number
    squared = map(lambda x: x ** 2, numbers)
    print(f"map object: {squared}")  # <map object>
    print(f"Squared: {list(squared)}")  # [1, 4, 9, 16, 25]
    
    # Convert to strings
    strings = map(str, numbers)
    print(f"Strings: {list(strings)}")  # ['1', '2', '3', '4', '5']
    
    # Multiple iterables
    a = [1, 2, 3]
    b = [10, 20, 30]
    sums = map(lambda x, y: x + y, a, b)
    print(f"Sums: {list(sums)}")  # [11, 22, 33]


def demonstrate_map_advanced() -> None:
    """Demonstrate advanced map() usage."""
    # Map with named function
    def celsius_to_fahrenheit(celsius: float) -> float:
        return (celsius * 9/5) + 32
    
    temperatures_c = [0, 10, 20, 30, 40]
    temperatures_f = map(celsius_to_fahrenheit, temperatures_c)
    print(f"Fahrenheit: {list(temperatures_f)}")
    
    # Map on strings
    words = ["hello", "world", "python"]
    uppercase = map(str.upper, words)
    print(f"Uppercase: {list(uppercase)}")
    
    # Map with complex transformation
    people = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]
    names = map(lambda p: p["name"], people)
    print(f"Names: {list(names)}")


def demonstrate_map_vs_comprehension() -> None:
    """Compare map() with list comprehension."""
    numbers = [1, 2, 3, 4, 5]
    
    # Using map
    squared_map = list(map(lambda x: x ** 2, numbers))
    
    # Using list comprehension
    squared_comp = [x ** 2 for x in numbers]
    
    print(f"map():        {squared_map}")
    print(f"comprehension: {squared_comp}")
    print(f"Same result: {squared_map == squared_comp}")


# ============================================================================
# FILTER - SELECT ELEMENTS
# ============================================================================

def demonstrate_filter_basics() -> None:
    """
    Demonstrate basic filter() usage.
    
    filter(predicate, iterable) selects elements where predicate is True.
    Returns an iterator (lazy evaluation).
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Filter even numbers
    evens = filter(lambda x: x % 2 == 0, numbers)
    print(f"filter object: {evens}")  # <filter object>
    print(f"Evens: {list(evens)}")  # [2, 4, 6, 8, 10]
    
    # Filter numbers > 5
    greater_than_5 = filter(lambda x: x > 5, numbers)
    print(f"Greater than 5: {list(greater_than_5)}")  # [6, 7, 8, 9, 10]
    
    # Filter with None (removes falsy values)
    mixed = [0, 1, False, True, "", "hello", None, [], [1, 2]]
    truthy = filter(None, mixed)
    print(f"Truthy values: {list(truthy)}")  # [1, True, 'hello', [1, 2]]


def demonstrate_filter_advanced() -> None:
    """Demonstrate advanced filter() usage."""
    # Filter with named function
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    numbers = range(1, 21)
    primes = filter(is_prime, numbers)
    print(f"Primes: {list(primes)}")
    
    # Filter strings by length
    words = ["apple", "pie", "banana", "cherry", "kiwi"]
    long_words = filter(lambda w: len(w) > 5, words)
    print(f"Long words: {list(long_words)}")
    
    # Filter dictionaries
    people = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 17},
        {"name": "Charlie", "age": 25}
    ]
    adults = filter(lambda p: p["age"] >= 18, people)
    print(f"Adults: {list(adults)}")


def demonstrate_filter_vs_comprehension() -> None:
    """Compare filter() with list comprehension."""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Using filter
    evens_filter = list(filter(lambda x: x % 2 == 0, numbers))
    
    # Using list comprehension
    evens_comp = [x for x in numbers if x % 2 == 0]
    
    print(f"filter():      {evens_filter}")
    print(f"comprehension: {evens_comp}")
    print(f"Same result: {evens_filter == evens_comp}")


# ============================================================================
# REDUCE - COMBINE ELEMENTS
# ============================================================================

def demonstrate_reduce_basics() -> None:
    """
    Demonstrate basic reduce() usage.

    reduce(function, iterable[, initializer]) applies function cumulatively.
    Combines all elements into single value.
    """
    numbers = [1, 2, 3, 4, 5]

    # Sum all numbers
    total = reduce(lambda x, y: x + y, numbers)
    print(f"Sum: {total}")  # 15

    # Product of all numbers
    product = reduce(lambda x, y: x * y, numbers)
    print(f"Product: {product}")  # 120

    # Maximum value
    maximum = reduce(lambda x, y: x if x > y else y, numbers)
    print(f"Maximum: {maximum}")  # 5

    # With initial value
    total_with_init = reduce(lambda x, y: x + y, numbers, 10)
    print(f"Sum with initial 10: {total_with_init}")  # 25


def demonstrate_reduce_advanced() -> None:
    """Demonstrate advanced reduce() usage."""
    # Flatten list of lists
    nested = [[1, 2], [3, 4], [5, 6]]
    flattened = reduce(lambda x, y: x + y, nested)
    print(f"Flattened: {flattened}")  # [1, 2, 3, 4, 5, 6]

    # Count occurrences
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    counts = reduce(
        lambda acc, word: {**acc, word: acc.get(word, 0) + 1},
        words,
        {}
    )
    print(f"Counts: {counts}")

    # Build string
    words_list = ["Hello", "functional", "programming"]
    sentence = reduce(lambda x, y: f"{x} {y}", words_list)
    print(f"Sentence: {sentence}")

    # Find minimum and maximum
    numbers = [5, 2, 8, 1, 9, 3]
    min_max = reduce(
        lambda acc, x: (min(acc[0], x), max(acc[1], x)),
        numbers,
        (float('inf'), float('-inf'))
    )
    print(f"Min and Max: {min_max}")


def demonstrate_reduce_vs_loop() -> None:
    """Compare reduce() with explicit loop."""
    numbers = [1, 2, 3, 4, 5]

    # Using reduce
    sum_reduce = reduce(lambda x, y: x + y, numbers)

    # Using loop
    sum_loop = 0
    for num in numbers:
        sum_loop += num

    # Using built-in
    sum_builtin = sum(numbers)

    print(f"reduce(): {sum_reduce}")
    print(f"loop:     {sum_loop}")
    print(f"sum():    {sum_builtin}")
    print(f"All same: {sum_reduce == sum_loop == sum_builtin}")


# ============================================================================
# COMBINING MAP, FILTER, AND REDUCE
# ============================================================================

def demonstrate_pipeline() -> None:
    """Demonstrate combining map, filter, and reduce."""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Pipeline: filter evens -> square -> sum
    result = reduce(
        lambda x, y: x + y,
        map(
            lambda x: x ** 2,
            filter(lambda x: x % 2 == 0, numbers)
        )
    )
    print(f"Sum of squared evens: {result}")
    # Steps: [2,4,6,8,10] -> [4,16,36,64,100] -> 220

    # Same with comprehension
    result_comp = sum(x ** 2 for x in numbers if x % 2 == 0)
    print(f"Comprehension: {result_comp}")


def demonstrate_complex_pipeline() -> None:
    """Demonstrate complex data pipeline."""
    # Process student data
    students = [
        {"name": "Alice", "scores": [85, 90, 88]},
        {"name": "Bob", "scores": [70, 75, 72]},
        {"name": "Charlie", "scores": [95, 92, 98]},
        {"name": "David", "scores": [60, 65, 62]}
    ]

    # Pipeline: calculate averages -> filter >= 80 -> get names
    passing_students = list(map(
        lambda s: s["name"],
        filter(
            lambda s: sum(s["scores"]) / len(s["scores"]) >= 80,
            students
        )
    ))
    print(f"Passing students: {passing_students}")

    # Calculate class average
    all_scores = reduce(
        lambda acc, student: acc + student["scores"],
        students,
        []
    )
    class_average = sum(all_scores) / len(all_scores)
    print(f"Class average: {class_average:.2f}")


# ============================================================================
# PRACTICAL EXAMPLES
# ============================================================================

def demonstrate_practical_map() -> None:
    """Practical map() examples."""
    # Parse strings to integers
    string_numbers = ["1", "2", "3", "4", "5"]
    integers = list(map(int, string_numbers))
    print(f"Parsed integers: {integers}")

    # Extract values from dictionaries
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ]
    emails = list(map(lambda u: u["email"], users))
    print(f"Emails: {emails}")

    # Apply function to nested data
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    doubled_matrix = list(map(lambda row: list(map(lambda x: x * 2, row)), matrix))
    print(f"Doubled matrix: {doubled_matrix}")


def demonstrate_practical_filter() -> None:
    """Practical filter() examples."""
    # Remove empty strings
    strings = ["hello", "", "world", "", "python"]
    non_empty = list(filter(None, strings))
    print(f"Non-empty: {non_empty}")

    # Filter valid emails (simple check)
    emails = ["alice@example.com", "invalid", "bob@test.com", "bad@"]
    valid_emails = list(filter(lambda e: "@" in e and "." in e, emails))
    print(f"Valid emails: {valid_emails}")

    # Filter by multiple conditions
    numbers = range(1, 101)
    filtered = list(filter(
        lambda x: x % 3 == 0 and x % 5 == 0,
        numbers
    ))
    print(f"Divisible by 3 and 5: {filtered}")


def demonstrate_practical_reduce() -> None:
    """Practical reduce() examples."""
    # Deep merge dictionaries
    dicts = [
        {"a": 1, "b": 2},
        {"b": 3, "c": 4},
        {"c": 5, "d": 6}
    ]
    merged = reduce(lambda x, y: {**x, **y}, dicts)
    print(f"Merged: {merged}")

    # Calculate factorial
    n = 5
    factorial = reduce(lambda x, y: x * y, range(1, n + 1))
    print(f"{n}! = {factorial}")

    # Group by key
    items = [
        {"category": "fruit", "name": "apple"},
        {"category": "vegetable", "name": "carrot"},
        {"category": "fruit", "name": "banana"}
    ]
    grouped = reduce(
        lambda acc, item: {
            **acc,
            item["category"]: acc.get(item["category"], []) + [item["name"]]
        },
        items,
        {}
    )
    print(f"Grouped: {grouped}")


# ============================================================================
# LAZY EVALUATION
# ============================================================================

def demonstrate_lazy_evaluation() -> None:
    """Demonstrate lazy evaluation of map and filter."""
    print("Creating map object...")
    numbers = [1, 2, 3, 4, 5]
    squared = map(lambda x: x ** 2, numbers)
    print(f"map object created: {squared}")
    print("No computation yet!")

    print("\nConverting to list...")
    result = list(squared)
    print(f"Now computed: {result}")

    print("\nTrying to iterate again...")
    result2 = list(squared)
    print(f"Empty! {result2}")
    print("← Iterator exhausted after first use")


def demonstrate_generator_expression() -> None:
    """Compare with generator expressions."""
    numbers = [1, 2, 3, 4, 5]

    # map
    squared_map = map(lambda x: x ** 2, numbers)

    # Generator expression
    squared_gen = (x ** 2 for x in numbers)

    # List comprehension
    squared_list = [x ** 2 for x in numbers]

    print(f"map:        {squared_map}")
    print(f"generator:  {squared_gen}")
    print(f"list:       {squared_list}")
    print("\nmap and generator are lazy, list is eager")


# ============================================================================
# DEMONSTRATION: map(), filter(), reduce()
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MAP, FILTER, AND REDUCE")
    print("=" * 60)

    print("\nFunctional programming tools:")
    print("  - map(): Transform each element")
    print("  - filter(): Select elements")
    print("  - reduce(): Combine elements")

    # ========================================================================
    # 1. MAP BASICS
    # ========================================================================
    print("\n" + "=" * 60)
    print("1. MAP - BASICS:")
    print("=" * 60)
    demonstrate_map_basics()
    print("   ← map() transforms each element")

    # ========================================================================
    # 2. MAP ADVANCED
    # ========================================================================
    print("\n" + "=" * 60)
    print("2. MAP - ADVANCED:")
    print("=" * 60)
    demonstrate_map_advanced()
    print("   ← map() with complex transformations")

    # ========================================================================
    # 3. MAP VS COMPREHENSION
    # ========================================================================
    print("\n" + "=" * 60)
    print("3. MAP VS LIST COMPREHENSION:")
    print("=" * 60)
    demonstrate_map_vs_comprehension()
    print("   ← Both produce same result")

    # ========================================================================
    # 4. FILTER BASICS
    # ========================================================================
    print("\n" + "=" * 60)
    print("4. FILTER - BASICS:")
    print("=" * 60)
    demonstrate_filter_basics()
    print("   ← filter() selects elements")

    # ========================================================================
    # 5. FILTER ADVANCED
    # ========================================================================
    print("\n" + "=" * 60)
    print("5. FILTER - ADVANCED:")
    print("=" * 60)
    demonstrate_filter_advanced()
    print("   ← filter() with complex predicates")

    # ========================================================================
    # 6. FILTER VS COMPREHENSION
    # ========================================================================
    print("\n" + "=" * 60)
    print("6. FILTER VS LIST COMPREHENSION:")
    print("=" * 60)
    demonstrate_filter_vs_comprehension()
    print("   ← Both produce same result")

    # ========================================================================
    # 7. REDUCE BASICS
    # ========================================================================
    print("\n" + "=" * 60)
    print("7. REDUCE - BASICS:")
    print("=" * 60)
    demonstrate_reduce_basics()
    print("   ← reduce() combines elements")

    # ========================================================================
    # 8. REDUCE ADVANCED
    # ========================================================================
    print("\n" + "=" * 60)
    print("8. REDUCE - ADVANCED:")
    print("=" * 60)
    demonstrate_reduce_advanced()
    print("   ← reduce() for complex aggregations")

    # ========================================================================
    # 9. REDUCE VS LOOP
    # ========================================================================
    print("\n" + "=" * 60)
    print("9. REDUCE VS LOOP:")
    print("=" * 60)
    demonstrate_reduce_vs_loop()
    print("   ← reduce() vs explicit loop")

    # ========================================================================
    # 10. COMBINING MAP, FILTER, REDUCE
    # ========================================================================
    print("\n" + "=" * 60)
    print("10. PIPELINE - COMBINING ALL THREE:")
    print("=" * 60)
    demonstrate_pipeline()
    print("   ← Chain operations together")

    # ========================================================================
    # 11. COMPLEX PIPELINE
    # ========================================================================
    print("\n" + "=" * 60)
    print("11. COMPLEX PIPELINE:")
    print("=" * 60)
    demonstrate_complex_pipeline()
    print("   ← Real-world data processing")

    # ========================================================================
    # 12. PRACTICAL MAP
    # ========================================================================
    print("\n" + "=" * 60)
    print("12. PRACTICAL MAP EXAMPLES:")
    print("=" * 60)
    demonstrate_practical_map()
    print("   ← Common map() use cases")

    # ========================================================================
    # 13. PRACTICAL FILTER
    # ========================================================================
    print("\n" + "=" * 60)
    print("13. PRACTICAL FILTER EXAMPLES:")
    print("=" * 60)
    demonstrate_practical_filter()
    print("   ← Common filter() use cases")

    # ========================================================================
    # 14. PRACTICAL REDUCE
    # ========================================================================
    print("\n" + "=" * 60)
    print("14. PRACTICAL REDUCE EXAMPLES:")
    print("=" * 60)
    demonstrate_practical_reduce()
    print("   ← Common reduce() use cases")

    # ========================================================================
    # 15. LAZY EVALUATION
    # ========================================================================
    print("\n" + "=" * 60)
    print("15. LAZY EVALUATION:")
    print("=" * 60)
    demonstrate_lazy_evaluation()
    print("   ← map/filter are lazy (computed on demand)")

    # ========================================================================
    # 16. GENERATOR EXPRESSIONS
    # ========================================================================
    print("\n" + "=" * 60)
    print("16. GENERATOR EXPRESSIONS:")
    print("=" * 60)
    demonstrate_generator_expression()
    print("   ← Generators vs lists")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. map(func, iterable) - Transform each element")
    print("2. filter(predicate, iterable) - Select elements")
    print("3. reduce(func, iterable[, init]) - Combine elements")
    print("4. map and filter return iterators (lazy)")
    print("5. reduce returns single value (eager)")
    print("6. Use list() to convert iterator to list")
    print("7. Iterators can only be consumed once")
    print("8. List comprehensions often more readable")
    print("9. Combine for powerful data pipelines")
    print("10. reduce needs: from functools import reduce")
    print("11. filter(None, iterable) removes falsy values")
    print("12. map can take multiple iterables")
    print("13. reduce initial value is optional")
    print("14. Prefer built-ins (sum, max, min) over reduce")
    print("=" * 60)


