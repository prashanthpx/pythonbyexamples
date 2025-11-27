"""
Example: Calling Functions
Demonstrates different ways to call functions in Python.

Key Concepts:
- Positional arguments
- Keyword arguments
- Mixing positional and keyword arguments
- Storing function results
- Chaining function calls
"""


def create_full_name(first: str, last: str, middle: str = "") -> str:
    """
    Create a full name from components.
    
    Args:
        first: First name
        last: Last name
        middle: Middle name (optional)
        
    Returns:
        Full name as a string
    """
    if middle:
        return f"{first} {middle} {last}"
    return f"{first} {last}"


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


def power(base: float, exponent: float = 2.0) -> float:
    """
    Raise base to the power of exponent.
    
    Args:
        base: The base number
        exponent: The exponent (default: 2.0 for square)
        
    Returns:
        Result of base ** exponent
    """
    return base ** exponent


def describe_person(name: str, age: int, city: str) -> str:
    """
    Create a description of a person.
    
    Args:
        name: Person's name
        age: Person's age
        city: Person's city
        
    Returns:
        Description string
    """
    return f"{name} is {age} years old and lives in {city}"


# ============================================================================
# DEMONSTRATION: Different ways to call functions
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CALLING FUNCTIONS - EXAMPLES")
    print("=" * 60)
    
    # ========================================================================
    # 1. POSITIONAL ARGUMENTS
    # ========================================================================
    print("\n1. POSITIONAL ARGUMENTS:")
    print("   Arguments are matched by position (order matters)")
    
    name1 = create_full_name("John", "Doe")
    print(f"   create_full_name('John', 'Doe') = '{name1}'")
    
    name2 = create_full_name("Jane", "Smith", "Marie")
    print(f"   create_full_name('Jane', 'Smith', 'Marie') = '{name2}'")
    
    # ← Important: Order matters! First arg goes to 'first', second to 'last'
    
    # ========================================================================
    # 2. KEYWORD ARGUMENTS
    # ========================================================================
    print("\n2. KEYWORD ARGUMENTS:")
    print("   Arguments are matched by name (order doesn't matter)")
    
    name3 = create_full_name(first="Alice", last="Johnson")
    print(f"   create_full_name(first='Alice', last='Johnson') = '{name3}'")
    
    # ← Important: Order doesn't matter with keyword arguments
    name4 = create_full_name(last="Brown", first="Bob", middle="Lee")
    print(f"   create_full_name(last='Brown', first='Bob', middle='Lee') = '{name4}'")
    
    # ========================================================================
    # 3. MIXING POSITIONAL AND KEYWORD ARGUMENTS
    # ========================================================================
    print("\n3. MIXING POSITIONAL AND KEYWORD:")
    print("   Positional args must come before keyword args")
    
    name5 = create_full_name("Charlie", "Davis", middle="Ray")
    print(f"   create_full_name('Charlie', 'Davis', middle='Ray') = '{name5}'")
    
    # ← Important: Positional args first, then keyword args
    # This would be an error: create_full_name(first="X", "Y", "Z")
    
    # ========================================================================
    # 4. USING DEFAULT VALUES
    # ========================================================================
    print("\n4. USING DEFAULT VALUES:")
    print("   Parameters with defaults can be omitted")
    
    square = power(5)  # Uses default exponent=2.0
    print(f"   power(5) = {square} (using default exponent=2.0)")
    
    cube = power(5, 3)  # Override default
    print(f"   power(5, 3) = {cube}")
    
    # Using keyword argument for clarity
    fourth = power(base=5, exponent=4)
    print(f"   power(base=5, exponent=4) = {fourth}")
    
    # ========================================================================
    # 5. STORING FUNCTION RESULTS
    # ========================================================================
    print("\n5. STORING FUNCTION RESULTS:")
    
    result = multiply(6, 7)
    print(f"   result = multiply(6, 7)")
    print(f"   result = {result}")
    
    # ← Important: Store result in variable for later use
    
    # ========================================================================
    # 6. USING RESULTS DIRECTLY
    # ========================================================================
    print("\n6. USING RESULTS DIRECTLY:")
    
    # Use function result directly in expression
    total = multiply(3, 4) + multiply(5, 6)
    print(f"   total = multiply(3, 4) + multiply(5, 6)")
    print(f"   total = {total}")
    
    # Use in print statement
    print(f"   Direct: {multiply(8, 9)}")
    
    # ========================================================================
    # 7. CHAINING FUNCTION CALLS
    # ========================================================================
    print("\n7. CHAINING FUNCTION CALLS:")
    
    # Pass result of one function to another
    description = describe_person(
        name=create_full_name("Emma", "Wilson"),
        age=28,
        city="Seattle"
    )
    print(f"   {description}")
    
    # ← Important: Inner function executes first, result passed to outer
    
    # ========================================================================
    # 8. MULTIPLE CALLS TO SAME FUNCTION
    # ========================================================================
    print("\n8. MULTIPLE CALLS:")
    
    print(f"   multiply(2, 3) = {multiply(2, 3)}")
    print(f"   multiply(4, 5) = {multiply(4, 5)}")
    print(f"   multiply(6, 7) = {multiply(6, 7)}")
    
    # ← Each call is independent and returns a new result
    
    print("\n" + "=" * 60)

