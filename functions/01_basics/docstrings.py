"""
Example: Docstrings and Documentation
Demonstrates how to write effective docstrings for Python functions.

Key Concepts:
- What are docstrings
- Different docstring styles (Google, NumPy, reStructuredText)
- Accessing docstrings with __doc__
- Best practices for documentation
"""


def simple_docstring(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"


def detailed_docstring(name: str, age: int, city: str = "Unknown") -> str:
    """
    Create a detailed person description.
    
    This function takes personal information and creates a formatted
    description string. It demonstrates a multi-line docstring with
    detailed parameter and return value documentation.
    
    Args:
        name: The person's full name
        age: The person's age in years (must be positive)
        city: The city where the person lives (default: "Unknown")
        
    Returns:
        A formatted string describing the person
        
    Raises:
        ValueError: If age is negative
        
    Example:
        >>> detailed_docstring("Alice", 30, "Seattle")
        'Alice (30) lives in Seattle'
        
    Note:
        This is the Google-style docstring format, which is widely used
        and supported by many documentation tools.
    """
    if age < 0:
        raise ValueError("Age cannot be negative")
    
    return f"{name} ({age}) lives in {city}"


def numpy_style_docstring(x: float, y: float) -> float:
    """
    Calculate the Euclidean distance between two points.
    
    This demonstrates NumPy-style docstring format.
    
    Parameters
    ----------
    x : float
        The x-coordinate
    y : float
        The y-coordinate
        
    Returns
    -------
    float
        The Euclidean distance from origin
        
    Examples
    --------
    >>> numpy_style_docstring(3.0, 4.0)
    5.0
    
    Notes
    -----
    Uses the formula: sqrt(x² + y²)
    """
    return (x**2 + y**2) ** 0.5


def rest_style_docstring(items: list[int]) -> int:
    """
    Calculate the sum of a list of integers.
    
    This demonstrates reStructuredText (reST) style docstring.
    
    :param items: List of integers to sum
    :type items: list[int]
    :return: Sum of all integers in the list
    :rtype: int
    :raises TypeError: If items is not a list
    
    .. note::
        This style is used by Sphinx documentation generator.
        
    .. warning::
        Empty list returns 0.
    """
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    
    return sum(items)


def minimal_but_good(data: str) -> str:
    """
    Clean and normalize input data.
    
    Removes whitespace and converts to lowercase.
    
    Args:
        data: Input string to clean
        
    Returns:
        Cleaned string
    """
    return data.strip().lower()


def one_liner(x: int) -> int:
    """Double the input value."""
    return x * 2


# ============================================================================
# DEMONSTRATION: Accessing and using docstrings
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DOCSTRINGS - EXAMPLES")
    print("=" * 60)
    
    # ========================================================================
    # 1. SIMPLE DOCSTRING
    # ========================================================================
    print("\n1. SIMPLE DOCSTRING (one-liner):")
    print(f"   Function: simple_docstring")
    print(f"   Docstring: {simple_docstring.__doc__}")
    
    # ← Important: Access docstring with __doc__ attribute
    
    # ========================================================================
    # 2. DETAILED DOCSTRING (Google Style)
    # ========================================================================
    print("\n2. DETAILED DOCSTRING (Google Style):")
    print(f"   Function: detailed_docstring")
    print(f"   Docstring:\n{detailed_docstring.__doc__}")
    
    # ========================================================================
    # 3. NUMPY STYLE DOCSTRING
    # ========================================================================
    print("\n3. NUMPY STYLE DOCSTRING:")
    print(f"   Function: numpy_style_docstring")
    print(f"   Docstring:\n{numpy_style_docstring.__doc__}")
    
    # ========================================================================
    # 4. USING help() FUNCTION
    # ========================================================================
    print("\n4. USING help() FUNCTION:")
    print("   help(detailed_docstring) shows:")
    print("   " + "-" * 56)
    help(detailed_docstring)

    # ========================================================================
    # 5. PRACTICAL USAGE
    # ========================================================================
    print("\n5. PRACTICAL USAGE:")

    # Call functions and show they work
    result1 = simple_docstring("Bob")
    print(f"   simple_docstring('Bob') = '{result1}'")

    result2 = detailed_docstring("Alice", 30, "Seattle")
    print(f"   detailed_docstring('Alice', 30, 'Seattle') = '{result2}'")

    result3 = numpy_style_docstring(3.0, 4.0)
    print(f"   numpy_style_docstring(3.0, 4.0) = {result3}")

    result4 = rest_style_docstring([1, 2, 3, 4, 5])
    print(f"   rest_style_docstring([1,2,3,4,5]) = {result4}")

    # ========================================================================
    # 6. DOCSTRING BEST PRACTICES
    # ========================================================================
    print("\n6. DOCSTRING BEST PRACTICES:")
    print("   ✓ Always write docstrings for public functions")
    print("   ✓ Use triple quotes (even for one-liners)")
    print("   ✓ First line should be a brief summary")
    print("   ✓ Document all parameters and return values")
    print("   ✓ Include examples when helpful")
    print("   ✓ Mention exceptions that can be raised")
    print("   ✓ Be consistent with your chosen style")

    # ========================================================================
    # 7. CHECKING IF FUNCTION HAS DOCSTRING
    # ========================================================================
    print("\n7. CHECKING FOR DOCSTRINGS:")

    functions = [
        simple_docstring,
        detailed_docstring,
        numpy_style_docstring,
        one_liner
    ]

    for func in functions:
        has_doc = func.__doc__ is not None and func.__doc__.strip() != ""
        status = "✓" if has_doc else "✗"
        print(f"   {status} {func.__name__}: {has_doc}")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Docstrings are the first string in a function")
    print("2. Use triple quotes: \"\"\" ... \"\"\"")
    print("3. Access with function.__doc__")
    print("4. help() function displays docstrings")
    print("5. Choose a style (Google, NumPy, reST) and be consistent")
    print("6. Good documentation makes code maintainable")
    print("=" * 60)

