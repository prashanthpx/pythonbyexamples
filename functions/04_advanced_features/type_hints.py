"""
Example: Type Hints and Annotations
Demonstrates advanced type hints for functions.

Type hints (PEP 484, 526, 544, 585, 604) provide:
- Better code documentation
- IDE autocomplete and error detection
- Runtime type checking (with tools like mypy)
- Improved code maintainability

Key Concepts:
- Basic types: int, str, float, bool
- Container types: list, dict, tuple, set
- Optional and Union types
- Callable types for functions
- TypeVar for generic types
- Protocol for structural typing
"""

from typing import (
    List, Dict, Tuple, Set, Optional, Union, Any,
    Callable, TypeVar, Generic, Protocol, Literal,
    overload, Final
)
from collections.abc import Iterable, Sequence


# ============================================================================
# BASIC TYPE HINTS
# ============================================================================

def basic_types(
    name: str,
    age: int,
    height: float,
    is_student: bool
) -> str:
    """
    Basic type hints for parameters and return.
    
    Args:
        name: Person's name
        age: Person's age
        height: Person's height in meters
        is_student: Whether person is a student
        
    Returns:
        Formatted string
    """
    return f"{name}, {age} years, {height}m, student={is_student}"


def none_return(message: str) -> None:
    """
    Function that returns None.
    
    Args:
        message: Message to print
    """
    print(message)
    # ← Implicitly returns None


# ============================================================================
# CONTAINER TYPE HINTS
# ============================================================================

def list_types(numbers: list[int]) -> list[int]:
    """
    List with element type.
    
    Args:
        numbers: List of integers
        
    Returns:
        Squared numbers
    """
    return [n ** 2 for n in numbers]


def dict_types(data: dict[str, int]) -> dict[str, int]:
    """
    Dictionary with key and value types.
    
    Args:
        data: Dictionary mapping strings to integers
        
    Returns:
        Filtered dictionary
    """
    return {k: v for k, v in data.items() if v > 0}


def tuple_types(point: tuple[float, float, float]) -> float:
    """
    Tuple with fixed element types.
    
    Args:
        point: 3D point (x, y, z)
        
    Returns:
        Distance from origin
    """
    x, y, z = point
    return (x**2 + y**2 + z**2) ** 0.5


def set_types(items: set[str]) -> set[str]:
    """
    Set with element type.
    
    Args:
        items: Set of strings
        
    Returns:
        Uppercase strings
    """
    return {item.upper() for item in items}


# ============================================================================
# OPTIONAL AND UNION TYPES
# ============================================================================

def optional_parameter(name: str, age: Optional[int] = None) -> str:
    """
    Optional parameter (can be None).
    
    Args:
        name: Person's name
        age: Person's age (optional)
        
    Returns:
        Formatted string
    """
    if age is None:
        return f"{name} (age unknown)"
    return f"{name}, {age} years"


def union_types(value: Union[int, str]) -> str:
    """
    Union type (can be int OR str).
    
    Args:
        value: Either an integer or string
        
    Returns:
        String representation
    """
    if isinstance(value, int):
        return f"Number: {value}"
    return f"String: {value}"


def optional_return(value: int) -> Optional[str]:
    """
    Function that may return None.
    
    Args:
        value: Input value
        
    Returns:
        String if positive, None otherwise
    """
    if value > 0:
        return str(value)
    return None  # ← Explicitly return None


# ============================================================================
# CALLABLE TYPE HINTS
# ============================================================================

def apply_function(func: Callable[[int], int], value: int) -> int:
    """
    Function that takes a function as parameter.
    
    Args:
        func: Function that takes int and returns int
        value: Value to pass to function
        
    Returns:
        Result of applying function
    """
    return func(value)


def make_adder(n: int) -> Callable[[int], int]:
    """
    Function that returns a function.
    
    Args:
        n: Number to add
        
    Returns:
        Function that adds n to its argument
    """
    def add(x: int) -> int:
        return x + n
    
    return add  # ← Return type is Callable[[int], int]


def callback_example(
    data: list[int],
    callback: Callable[[int], None]
) -> None:
    """
    Function with callback parameter.

    Args:
        data: List of integers
        callback: Function to call for each item
    """
    for item in data:
        callback(item)


# ============================================================================
# GENERIC TYPES (TypeVar)
# ============================================================================

T = TypeVar('T')  # ← Generic type variable


def first_element(items: list[T]) -> Optional[T]:
    """
    Get first element of list (generic type).

    Args:
        items: List of any type

    Returns:
        First element or None
    """
    return items[0] if items else None


def reverse_list(items: list[T]) -> list[T]:
    """
    Reverse a list (preserves type).

    Args:
        items: List of any type

    Returns:
        Reversed list of same type
    """
    return items[::-1]


K = TypeVar('K')
V = TypeVar('V')


def swap_dict(d: dict[K, V]) -> dict[V, K]:
    """
    Swap keys and values in dictionary.

    Args:
        d: Dictionary to swap

    Returns:
        Dictionary with swapped keys/values
    """
    return {v: k for k, v in d.items()}


# ============================================================================
# GENERIC CLASSES
# ============================================================================

class Stack(Generic[T]):
    """Generic stack data structure."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """Push item onto stack."""
        self._items.append(item)

    def pop(self) -> Optional[T]:
        """Pop item from stack."""
        return self._items.pop() if self._items else None

    def peek(self) -> Optional[T]:
        """Peek at top item."""
        return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self._items) == 0


# ============================================================================
# PROTOCOL (STRUCTURAL TYPING)
# ============================================================================

class Drawable(Protocol):
    """Protocol for drawable objects."""

    def draw(self) -> str:
        """Draw the object."""
        ...


class Circle:
    """Circle class (implements Drawable protocol)."""

    def __init__(self, radius: float) -> None:
        self.radius = radius

    def draw(self) -> str:
        return f"Circle(radius={self.radius})"


class Square:
    """Square class (implements Drawable protocol)."""

    def __init__(self, side: float) -> None:
        self.side = side

    def draw(self) -> str:
        return f"Square(side={self.side})"


def render(obj: Drawable) -> str:
    """
    Render any drawable object.

    Args:
        obj: Object with draw() method

    Returns:
        Rendered string
    """
    return obj.draw()  # ← Works with any object that has draw()


# ============================================================================
# LITERAL TYPES
# ============================================================================

def set_mode(mode: Literal["read", "write", "append"]) -> str:
    """
    Function with literal type (only specific values allowed).

    Args:
        mode: File mode (must be "read", "write", or "append")

    Returns:
        Mode description
    """
    return f"Mode: {mode}"


# ============================================================================
# FINAL TYPES
# ============================================================================

MAX_SIZE: Final[int] = 100  # ← Cannot be reassigned


def get_max_size() -> int:
    """Get maximum size constant."""
    return MAX_SIZE


# ============================================================================
# OVERLOAD (FUNCTION OVERLOADING)
# ============================================================================

@overload
def process(value: int) -> int:
    ...


@overload
def process(value: str) -> str:
    ...


def process(value: Union[int, str]) -> Union[int, str]:
    """
    Process value (overloaded for int and str).

    Args:
        value: Integer or string

    Returns:
        Processed value
    """
    if isinstance(value, int):
        return value * 2
    return value.upper()


# ============================================================================
# COMPLEX TYPE HINTS
# ============================================================================

def complex_function(
    data: dict[str, list[tuple[int, str]]],
    callback: Optional[Callable[[str], None]] = None
) -> list[int]:
    """
    Function with complex type hints.

    Args:
        data: Dictionary mapping strings to lists of (int, str) tuples
        callback: Optional callback function

    Returns:
        List of integers
    """
    result = []
    for key, values in data.items():
        if callback:
            callback(key)
        result.extend(num for num, _ in values)
    return result


def nested_containers() -> dict[str, dict[str, list[int]]]:
    """
    Nested container types.

    Returns:
        Nested dictionary structure
    """
    return {
        "group1": {"subgroup1": [1, 2, 3]},
        "group2": {"subgroup2": [4, 5, 6]}
    }


# ============================================================================
# TYPE ALIASES
# ============================================================================

# ← Type aliases for complex types
Point3D = tuple[float, float, float]
Matrix = list[list[float]]
JSONDict = dict[str, Union[str, int, float, bool, None]]


def distance_3d(p1: Point3D, p2: Point3D) -> float:
    """
    Calculate distance between 3D points.

    Args:
        p1: First point
        p2: Second point

    Returns:
        Distance
    """
    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5


def create_matrix(rows: int, cols: int) -> Matrix:
    """
    Create a matrix.

    Args:
        rows: Number of rows
        cols: Number of columns

    Returns:
        Matrix filled with zeros
    """
    return [[0.0 for _ in range(cols)] for _ in range(rows)]


def parse_json(data: str) -> JSONDict:
    """
    Parse JSON string.

    Args:
        data: JSON string

    Returns:
        Parsed dictionary
    """
    import json
    return json.loads(data)


# ============================================================================
# ANY TYPE (ESCAPE HATCH)
# ============================================================================

def process_any(value: Any) -> Any:
    """
    Function that accepts any type.

    Args:
        value: Any value

    Returns:
        Processed value
    """
    # ⚠️ Use Any sparingly - defeats purpose of type hints
    return value


# ============================================================================
# ITERABLE AND SEQUENCE
# ============================================================================

def sum_iterable(items: Iterable[int]) -> int:
    """
    Sum any iterable of integers.

    Args:
        items: Iterable of integers (list, tuple, set, etc.)

    Returns:
        Sum
    """
    return sum(items)


def first_n(items: Sequence[T], n: int) -> Sequence[T]:
    """
    Get first n items from sequence.

    Args:
        items: Sequence (list, tuple, str, etc.)
        n: Number of items

    Returns:
        First n items
    """
    return items[:n]


# ============================================================================
# DEMONSTRATION: Type Hints
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TYPE HINTS - ADVANCED TYPE ANNOTATIONS")
    print("=" * 60)

    print("\nType hints provide:")
    print("  - Better documentation")
    print("  - IDE autocomplete")
    print("  - Static type checking (mypy)")
    print("  - Improved maintainability")

    # ========================================================================
    # 1. BASIC TYPES
    # ========================================================================
    print("\n" + "=" * 60)
    print("1. BASIC TYPES:")
    print("=" * 60)

    result = basic_types("Alice", 25, 1.65, True)
    print(f"   {result}")
    print("   ← Basic type hints: str, int, float, bool")

    none_return("Hello")
    print("   ← Return type: None")

    # ========================================================================
    # 2. CONTAINER TYPES
    # ========================================================================
    print("\n" + "=" * 60)
    print("2. CONTAINER TYPES:")
    print("=" * 60)

    print(f"   list[int]: {list_types([1, 2, 3])}")
    print(f"   dict[str, int]: {dict_types({'a': 1, 'b': -2, 'c': 3})}")
    print(f"   tuple[float, float, float]: {tuple_types((3.0, 4.0, 0.0)):.2f}")
    print(f"   set[str]: {set_types({'a', 'b', 'c'})}")
    print("   ← Container types with element types")

    # ========================================================================
    # 3. OPTIONAL AND UNION
    # ========================================================================
    print("\n" + "=" * 60)
    print("3. OPTIONAL AND UNION:")
    print("=" * 60)

    print(f"   With age: {optional_parameter('Bob', 30)}")
    print(f"   Without age: {optional_parameter('Alice')}")
    print("   ← Optional[int] = int or None")

    print(f"   Union int: {union_types(42)}")
    print(f"   Union str: {union_types('hello')}")
    print("   ← Union[int, str] = int or str")

    result = optional_return(5)
    print(f"   Optional return: {result}")
    print("   ← Optional[str] = str or None")

    # ========================================================================
    # 4. CALLABLE TYPES
    # ========================================================================
    print("\n" + "=" * 60)
    print("4. CALLABLE TYPES:")
    print("=" * 60)

    result = apply_function(lambda x: x * 2, 10)
    print(f"   apply_function: {result}")
    print("   ← Callable[[int], int] = function(int) -> int")

    add5 = make_adder(5)
    print(f"   make_adder(5)(10) = {add5(10)}")
    print("   ← Return type: Callable[[int], int]")

    print("\n   Callback example:")
    callback_example([1, 2, 3], lambda x: print(f"      Item: {x}"))
    print("   ← Callable[[int], None] = function(int) -> None")

    # ========================================================================
    # 5. GENERIC TYPES
    # ========================================================================
    print("\n" + "=" * 60)
    print("5. GENERIC TYPES (TypeVar):")
    print("=" * 60)

    print(f"   first_element([1, 2, 3]) = {first_element([1, 2, 3])}")
    print(f"   first_element(['a', 'b']) = {first_element(['a', 'b'])}")
    print("   ← TypeVar preserves type")

    print(f"   reverse_list([1, 2, 3]) = {reverse_list([1, 2, 3])}")
    print(f"   swap_dict({{'a': 1, 'b': 2}}) = {swap_dict({'a': 1, 'b': 2})}")

    # ========================================================================
    # 6. GENERIC CLASSES
    # ========================================================================
    print("\n" + "=" * 60)
    print("6. GENERIC CLASSES:")
    print("=" * 60)

    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    print(f"   int_stack.pop() = {int_stack.pop()}")

    str_stack: Stack[str] = Stack()
    str_stack.push("hello")
    str_stack.push("world")
    print(f"   str_stack.pop() = {str_stack.pop()}")
    print("   ← Generic[T] for type-safe containers")

    # ========================================================================
    # 7. PROTOCOL (STRUCTURAL TYPING)
    # ========================================================================
    print("\n" + "=" * 60)
    print("7. PROTOCOL (STRUCTURAL TYPING):")
    print("=" * 60)

    circle = Circle(5.0)
    square = Square(10.0)

    print(f"   render(circle) = {render(circle)}")
    print(f"   render(square) = {render(square)}")
    print("   ← Protocol: structural typing (duck typing)")

    # ========================================================================
    # 8. LITERAL TYPES
    # ========================================================================
    print("\n" + "=" * 60)
    print("8. LITERAL TYPES:")
    print("=" * 60)

    print(f"   set_mode('read') = {set_mode('read')}")
    print(f"   set_mode('write') = {set_mode('write')}")
    print("   ← Literal: only specific values allowed")

    # ========================================================================
    # 9. FINAL TYPES
    # ========================================================================
    print("\n" + "=" * 60)
    print("9. FINAL TYPES:")
    print("=" * 60)

    print(f"   MAX_SIZE = {get_max_size()}")
    print("   ← Final: constant that cannot be reassigned")

    # ========================================================================
    # 10. OVERLOAD
    # ========================================================================
    print("\n" + "=" * 60)
    print("10. OVERLOAD:")
    print("=" * 60)

    print(f"   process(5) = {process(5)}")
    print(f"   process('hello') = {process('hello')}")
    print("   ← @overload: multiple type signatures")

    # ========================================================================
    # 11. COMPLEX TYPES
    # ========================================================================
    print("\n" + "=" * 60)
    print("11. COMPLEX TYPES:")
    print("=" * 60)

    data = {
        "group1": [(1, "a"), (2, "b")],
        "group2": [(3, "c")]
    }
    result = complex_function(data)
    print(f"   complex_function: {result}")
    print("   ← dict[str, list[tuple[int, str]]]")

    result = nested_containers()
    print(f"   nested_containers: {result}")
    print("   ← dict[str, dict[str, list[int]]]")

    # ========================================================================
    # 12. TYPE ALIASES
    # ========================================================================
    print("\n" + "=" * 60)
    print("12. TYPE ALIASES:")
    print("=" * 60)

    p1: Point3D = (0.0, 0.0, 0.0)
    p2: Point3D = (3.0, 4.0, 0.0)
    print(f"   distance_3d: {distance_3d(p1, p2):.2f}")
    print("   ← Point3D = tuple[float, float, float]")

    matrix = create_matrix(2, 3)
    print(f"   create_matrix: {matrix}")
    print("   ← Matrix = list[list[float]]")

    # ========================================================================
    # 13. ITERABLE AND SEQUENCE
    # ========================================================================
    print("\n" + "=" * 60)
    print("13. ITERABLE AND SEQUENCE:")
    print("=" * 60)

    print(f"   sum_iterable([1, 2, 3]) = {sum_iterable([1, 2, 3])}")
    print(f"   sum_iterable({{1, 2, 3}}) = {sum_iterable({1, 2, 3})}")
    print("   ← Iterable[int]: any iterable")

    print(f"   first_n([1, 2, 3, 4, 5], 3) = {first_n([1, 2, 3, 4, 5], 3)}")
    print(f"   first_n('hello', 3) = {first_n('hello', 3)}")
    print("   ← Sequence[T]: list, tuple, str, etc.")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Type hints improve code documentation and IDE support")
    print("2. Basic types: int, str, float, bool, None")
    print("3. Container types: list[T], dict[K, V], tuple, set[T]")
    print("4. Optional[T] = T or None")
    print("5. Union[A, B] = A or B")
    print("6. Callable[[Args], Return] for function types")
    print("7. TypeVar for generic types")
    print("8. Generic[T] for generic classes")
    print("9. Protocol for structural typing")
    print("10. Literal for specific values only")
    print("11. Final for constants")
    print("12. @overload for multiple signatures")
    print("13. Type aliases for complex types")
    print("14. Use mypy for static type checking")
    print("=" * 60)


