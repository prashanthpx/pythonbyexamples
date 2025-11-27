"""
Example: Basic Function Definition
Demonstrates the fundamental structure of Python functions with type annotations.

Key Concepts:
- Function definition syntax
- Type annotations for parameters and return values
- Docstrings for documentation
- Return statements
"""


def greet(name: str) -> str:
    """
    Greet a person by name.
    
    Args:
        name: The person's name to greet
        
    Returns:
        A greeting message as a string
        
    Key Takeaway:
        This shows the basic structure: def keyword, function name, 
        parameters with type hints, return type annotation, and docstring.
    """
    message = f"Hello, {name}!"  # ← Important: f-strings for string formatting
    return message  # ← Important: Explicit return statement


def calculate_area(length: float, width: float) -> float:
    """
    Calculate the area of a rectangle.
    
    Args:
        length: Length of the rectangle
        width: Width of the rectangle
        
    Returns:
        Area as a float
        
    Nuance:
        Using float annotations allows both int and float inputs.
        Python's type hints are not enforced at runtime.
    """
    return length * width  # ← Can return expression directly without storing in variable


def print_info(name: str, age: int) -> None:
    """
    Print user information to console.
    
    Args:
        name: User's name
        age: User's age
        
    Returns:
        None (this function has side effects, not a return value)
        
    Important:
        -> None annotation indicates no return value.
        Functions that perform actions (print, write files) often return None.
    """
    print(f"{name} is {age} years old")
    # ← No return statement = implicit return None


def add_numbers(a: int, b: int) -> int:
    """
    Add two integers.
    
    Args:
        a: First integer
        b: Second integer
        
    Returns:
        Sum of a and b
        
    Note:
        Simple, focused function that does one thing well.
    """
    result = a + b
    return result


def no_parameters() -> str:
    """
    Function with no parameters.
    
    Returns:
        A fixed string message
        
    Nuance:
        Empty parentheses () indicate no parameters.
        Still need the parentheses even with no parameters.
    """
    return "I don't need any input!"


def no_return_value(message: str) -> None:
    """
    Function that performs an action but returns nothing.
    
    Args:
        message: Message to print
        
    Returns:
        None
        
    Important:
        Functions without explicit return automatically return None.
        Use -> None to make this explicit in the signature.
    """
    print(f"Message: {message}")
    # Implicit return None


# ============================================================================
# DEMONSTRATION: Running the examples
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("BASIC FUNCTION DEFINITIONS - EXAMPLES")
    print("=" * 60)
    
    # Example 1: Function with return value
    print("\n1. Function with return value:")
    greeting = greet("Alice")
    print(f"   Result: {greeting}")
    print(f"   Type: {type(greeting)}")
    
    # Example 2: Function with multiple parameters
    print("\n2. Function with multiple parameters:")
    area = calculate_area(5.0, 3.0)
    print(f"   Area of 5.0 x 3.0 = {area}")
    
    # Example 3: Function with no return (side effects)
    print("\n3. Function with side effects (no return):")
    result = print_info("Bob", 30)
    print(f"   Return value: {result}")  # Will be None
    
    # Example 4: Simple addition
    print("\n4. Simple addition function:")
    sum_result = add_numbers(10, 20)
    print(f"   10 + 20 = {sum_result}")
    
    # Example 5: No parameters
    print("\n5. Function with no parameters:")
    msg = no_parameters()
    print(f"   Result: {msg}")
    
    # Example 6: No return value
    print("\n6. Function with no return value:")
    ret = no_return_value("Hello World")
    print(f"   Return value: {ret}")  # None
    
    print("\n" + "=" * 60)

