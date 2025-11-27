"""
Example: Positional Arguments
Demonstrates how positional arguments work in Python functions.

Key Concepts:
- Arguments matched by position (order matters)
- Required vs optional positional arguments
- Positional-only parameters (Python 3.8+)
"""

from typing import Union


def greet(first_name: str, last_name: str) -> str:
    """
    Greet a person using their full name.
    
    Args:
        first_name: Person's first name
        last_name: Person's last name
        
    Returns:
        Greeting message
        
    Note:
        Arguments are matched by position - order matters!
    """
    return f"Hello, {first_name} {last_name}!"


def calculate_rectangle(length: float, width: float, height: float = 1.0) -> dict[str, float]:
    """
    Calculate properties of a rectangle or rectangular prism.
    
    Args:
        length: Length of the rectangle (required)
        width: Width of the rectangle (required)
        height: Height for 3D calculations (optional, default: 1.0)
        
    Returns:
        Dictionary with area and volume
        
    Important:
        First two parameters are required positional.
        Third parameter is optional with default value.
    """
    area = length * width
    volume = length * width * height
    
    return {
        "area": area,
        "volume": volume
    }


def create_user(username: str, email: str, age: int) -> dict[str, Union[str, int]]:
    """
    Create a user profile.
    
    Args:
        username: User's username
        email: User's email address
        age: User's age
        
    Returns:
        User profile dictionary
        
    Note:
        All three parameters are required positional arguments.
        Must be provided in the correct order.
    """
    return {
        "username": username,
        "email": email,
        "age": age
    }


def positional_only_example(name: str, age: int, /) -> str:
    """
    Function with positional-only parameters (Python 3.8+).
    
    Args:
        name: Person's name (positional-only)
        age: Person's age (positional-only)
        /: Marker indicating parameters before it are positional-only
        
    Returns:
        Formatted string
        
    Important:
        The '/' marker means parameters before it MUST be positional.
        They CANNOT be passed as keyword arguments.
    """
    return f"{name} is {age} years old"


def mixed_parameters(pos_only: str, /, standard: str, *, kw_only: str) -> str:
    """
    Function demonstrating all parameter types.
    
    Args:
        pos_only: Positional-only parameter (before /)
        /: Positional-only marker
        standard: Can be positional or keyword
        *: Keyword-only marker
        kw_only: Keyword-only parameter (after *)
        
    Returns:
        Formatted string
        
    Note:
        This shows the full spectrum of parameter types in one function.
    """
    return f"pos_only={pos_only}, standard={standard}, kw_only={kw_only}"


# ============================================================================
# DEMONSTRATION: Positional arguments
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("POSITIONAL ARGUMENTS - EXAMPLES")
    print("=" * 60)
    
    # ========================================================================
    # 1. BASIC POSITIONAL ARGUMENTS
    # ========================================================================
    print("\n1. BASIC POSITIONAL ARGUMENTS:")
    
    # Correct order
    greeting1 = greet("John", "Doe")
    print(f"   greet('John', 'Doe') = '{greeting1}'")
    
    # Wrong order gives wrong result
    greeting2 = greet("Doe", "John")
    print(f"   greet('Doe', 'John') = '{greeting2}'")
    print("   ⚠️  Order matters! Second call has reversed names")
    
    # ← Important: Position determines which parameter gets which value
    
    # ========================================================================
    # 2. REQUIRED VS OPTIONAL POSITIONAL
    # ========================================================================
    print("\n2. REQUIRED VS OPTIONAL POSITIONAL:")
    
    # Only required arguments (2D rectangle)
    result1 = calculate_rectangle(5.0, 3.0)
    print(f"   calculate_rectangle(5.0, 3.0):")
    print(f"   - Area: {result1['area']}")
    print(f"   - Volume: {result1['volume']} (height defaulted to 1.0)")

    # All arguments including optional (3D rectangular prism)
    result2 = calculate_rectangle(5.0, 3.0, 2.0)
    print(f"\n   calculate_rectangle(5.0, 3.0, 2.0):")
    print(f"   - Area: {result2['area']}")
    print(f"   - Volume: {result2['volume']}")

    # ← Optional parameters can be omitted or provided

    # ========================================================================
    # 3. MULTIPLE REQUIRED POSITIONAL ARGUMENTS
    # ========================================================================
    print("\n3. MULTIPLE REQUIRED POSITIONAL ARGUMENTS:")

    user = create_user("alice123", "alice@example.com", 25)
    print(f"   create_user('alice123', 'alice@example.com', 25):")
    print(f"   - Username: {user['username']}")
    print(f"   - Email: {user['email']}")
    print(f"   - Age: {user['age']}")

    # ⚠️ All three arguments are required - omitting any causes an error
    # create_user("alice123", "alice@example.com")  # ❌ TypeError: missing 1 required positional argument

    # ========================================================================
    # 4. POSITIONAL-ONLY PARAMETERS (Python 3.8+)
    # ========================================================================
    print("\n4. POSITIONAL-ONLY PARAMETERS (/):")

    # Correct: positional arguments
    result = positional_only_example("Bob", 30)
    print(f"   positional_only_example('Bob', 30) = '{result}'")

    # ❌ Error: cannot use keyword arguments
    # positional_only_example(name="Bob", age=30)  # TypeError
    print("   ⚠️  Cannot call with keywords: positional_only_example(name='Bob', age=30)")

    # ← The '/' marker enforces positional-only

    # ========================================================================
    # 5. MIXED PARAMETER TYPES
    # ========================================================================
    print("\n5. MIXED PARAMETER TYPES (/, standard, *):")

    # Correct usage
    result = mixed_parameters("pos", "std", kw_only="kw")
    print(f"   mixed_parameters('pos', 'std', kw_only='kw'):")
    print(f"   Result: '{result}'")

    # Standard parameter can be positional or keyword
    result2 = mixed_parameters("pos", standard="std", kw_only="kw")
    print(f"\n   mixed_parameters('pos', standard='std', kw_only='kw'):")
    print(f"   Result: '{result2}'")

    # ❌ Errors:
    # mixed_parameters(pos_only="pos", standard="std", kw_only="kw")  # pos_only must be positional
    # mixed_parameters("pos", "std", "kw")  # kw_only must be keyword

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Positional arguments are matched by ORDER")
    print("2. Order matters - wrong order = wrong result")
    print("3. Required positional args must be provided")
    print("4. Optional positional args have default values")
    print("5. '/' marker makes parameters positional-only (Python 3.8+)")
    print("6. Positional-only params CANNOT be passed as keywords")
    print("=" * 60)

