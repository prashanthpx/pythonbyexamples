"""
Example: *args and **kwargs
Demonstrates variable-length arguments in Python functions.

Key Concepts:
- *args: Variable positional arguments (tuple)
- **kwargs: Variable keyword arguments (dict)
- Combining regular params with *args and **kwargs
- Unpacking arguments when calling functions
"""

from typing import Any


def sum_numbers(*args: int) -> int:
    """
    Sum any number of integers.
    
    Args:
        *args: Variable number of integers
        
    Returns:
        Sum of all arguments
        
    Note:
        *args collects all positional arguments into a tuple.
        The name 'args' is convention, but you can use any name.
    """
    total = 0
    for num in args:
        total += num
    return total


def print_info(**kwargs: Any) -> None:
    """
    Print key-value pairs.
    
    Args:
        **kwargs: Variable number of keyword arguments
        
    Note:
        **kwargs collects all keyword arguments into a dictionary.
        The name 'kwargs' is convention, but you can use any name.
    """
    for key, value in kwargs.items():
        print(f"  {key}: {value}")


def create_person(name: str, age: int, **kwargs: Any) -> dict[str, Any]:
    """
    Create a person with required and optional attributes.
    
    Args:
        name: Person's name (required)
        age: Person's age (required)
        **kwargs: Additional optional attributes
        
    Returns:
        Person dictionary
        
    Important:
        Combines required parameters with variable keyword arguments.
    """
    person = {
        "name": name,
        "age": age
    }
    # Add all additional keyword arguments
    person.update(kwargs)
    return person


def calculate(*args: float, operation: str = "sum") -> float:
    """
    Perform calculation on variable number of values.
    
    Args:
        *args: Variable number of values
        operation: Operation to perform (default: "sum")
        
    Returns:
        Result of calculation
        
    Important:
        Parameters after *args must be keyword-only.
    """
    if operation == "sum":
        return sum(args)
    elif operation == "product":
        result = 1
        for num in args:
            result *= num
        return result
    elif operation == "average":
        return sum(args) / len(args) if args else 0
    else:
        raise ValueError(f"Unknown operation: {operation}")


def full_signature(
    pos_only: str,
    /,
    standard: str,
    *args: int,
    kw_only: str,
    **kwargs: Any
) -> dict[str, Any]:
    """
    Function demonstrating all parameter types together.
    
    Args:
        pos_only: Positional-only parameter
        /: Positional-only marker
        standard: Can be positional or keyword
        *args: Variable positional arguments
        kw_only: Keyword-only parameter
        **kwargs: Variable keyword arguments
        
    Returns:
        Dictionary with all received arguments
        
    Note:
        This shows the complete parameter syntax in order.
    """
    return {
        "pos_only": pos_only,
        "standard": standard,
        "args": args,
        "kw_only": kw_only,
        "kwargs": kwargs
    }


def wrapper_function(*args: Any, **kwargs: Any) -> Any:
    """
    Wrapper that forwards all arguments to another function.
    
    Args:
        *args: All positional arguments
        **kwargs: All keyword arguments
        
    Returns:
        Result from wrapped function
        
    Note:
        Common pattern for decorators and wrappers.
    """
    print(f"Wrapper called with args={args}, kwargs={kwargs}")
    # In real code, would call another function here
    return f"Processed {len(args)} args and {len(kwargs)} kwargs"


# ============================================================================
# DEMONSTRATION: *args and **kwargs
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("*ARGS AND **KWARGS - EXAMPLES")
    print("=" * 60)
    
    # ========================================================================
    # 1. *ARGS - VARIABLE POSITIONAL ARGUMENTS
    # ========================================================================
    print("\n1. *ARGS - VARIABLE POSITIONAL ARGUMENTS:")
    
    # Different number of arguments
    result1 = sum_numbers(1, 2, 3)
    print(f"   sum_numbers(1, 2, 3) = {result1}")
    
    result2 = sum_numbers(10, 20, 30, 40, 50)
    print(f"   sum_numbers(10, 20, 30, 40, 50) = {result2}")
    
    result3 = sum_numbers(5)
    print(f"   sum_numbers(5) = {result3}")
    
    result4 = sum_numbers()
    print(f"   sum_numbers() = {result4}")
    
    # ← *args accepts any number of positional arguments (including zero)

    # ========================================================================
    # 2. **KWARGS - VARIABLE KEYWORD ARGUMENTS
    # ========================================================================
    print("\n2. **KWARGS - VARIABLE KEYWORD ARGUMENTS:")

    print("   print_info(name='Alice', age=30, city='Seattle'):")
    print_info(name="Alice", age=30, city="Seattle")

    print("\n   print_info(color='blue', size='large', quantity=5, available=True):")
    print_info(color="blue", size="large", quantity=5, available=True)

    # ← **kwargs accepts any number of keyword arguments

    # ========================================================================
    # 3. COMBINING REQUIRED PARAMS WITH **KWARGS
    # ========================================================================
    print("\n3. COMBINING REQUIRED PARAMS WITH **KWARGS:")

    person1 = create_person("Bob", 25)
    print(f"   create_person('Bob', 25):")
    print(f"   {person1}")

    person2 = create_person("Alice", 30, city="Seattle", job="Engineer", hobby="Reading")
    print(f"\n   create_person('Alice', 30, city='Seattle', job='Engineer', hobby='Reading'):")
    print(f"   {person2}")

    # ← Required params first, then any additional keyword arguments

    # ========================================================================
    # 4. PARAMETERS AFTER *ARGS ARE KEYWORD-ONLY
    # ========================================================================
    print("\n4. PARAMETERS AFTER *ARGS ARE KEYWORD-ONLY:")

    result1 = calculate(1, 2, 3, 4, 5)
    print(f"   calculate(1, 2, 3, 4, 5) = {result1}")
    print("   (default operation='sum')")

    result2 = calculate(2, 3, 4, operation="product")
    print(f"\n   calculate(2, 3, 4, operation='product') = {result2}")

    result3 = calculate(10, 20, 30, 40, operation="average")
    print(f"   calculate(10, 20, 30, 40, operation='average') = {result3}")

    # ← 'operation' must be passed as keyword argument

    # ========================================================================
    # 5. FULL PARAMETER SIGNATURE
    # ========================================================================
    print("\n5. FULL PARAMETER SIGNATURE:")

    result = full_signature(
        "pos_value",           # positional-only
        "std_value",           # standard (positional here)
        1, 2, 3,              # *args
        kw_only="kw_value",   # keyword-only
        extra1="value1",      # **kwargs
        extra2="value2"       # **kwargs
    )

    print("   full_signature('pos_value', 'std_value', 1, 2, 3,")
    print("                  kw_only='kw_value', extra1='value1', extra2='value2'):")
    print(f"   {result}")

    # ← Order: pos_only, /, standard, *args, kw_only, **kwargs

    # ========================================================================
    # 6. UNPACKING ARGUMENTS
    # ========================================================================
    print("\n6. UNPACKING ARGUMENTS:")

    # Unpack list/tuple with *
    numbers = [1, 2, 3, 4, 5]
    result = sum_numbers(*numbers)  # ← Unpacks list into separate arguments
    print(f"   numbers = {numbers}")
    print(f"   sum_numbers(*numbers) = {result}")
    print("   (equivalent to sum_numbers(1, 2, 3, 4, 5))")

    # Unpack dictionary with **
    person_data = {"name": "Charlie", "age": 35, "city": "Boston", "job": "Developer"}
    person = create_person(**person_data)  # ← Unpacks dict into keyword arguments
    print(f"\n   person_data = {person_data}")
    print(f"   create_person(**person_data):")
    print(f"   {person}")

    # ← * unpacks sequences, ** unpacks dictionaries

    # ========================================================================
    # 7. WRAPPER PATTERN
    # ========================================================================
    print("\n7. WRAPPER PATTERN:")

    result = wrapper_function(1, 2, 3, name="test", value=42)
    print(f"   Result: {result}")

    # ← Common pattern for decorators and function wrappers

    # ========================================================================
    # 8. COMBINING EVERYTHING
    # ========================================================================
    print("\n8. COMBINING EVERYTHING:")

    def flexible_function(required: str, *args: int, optional: str = "default", **kwargs: Any) -> None:
        print(f"     required: {required}")
        print(f"     args: {args}")
        print(f"     optional: {optional}")
        print(f"     kwargs: {kwargs}")

    print("   flexible_function('req', 1, 2, 3, optional='opt', extra='value'):")
    flexible_function("req", 1, 2, 3, optional="opt", extra="value")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. *args collects positional arguments into a TUPLE")
    print("2. **kwargs collects keyword arguments into a DICT")
    print("3. Names 'args' and 'kwargs' are convention (can use any name)")
    print("4. Parameters after *args are keyword-only")
    print("5. Order: pos_only, /, standard, *args, kw_only, **kwargs")
    print("6. * unpacks sequences, ** unpacks dictionaries")
    print("7. Common in wrappers, decorators, and flexible APIs")
    print("=" * 60)

