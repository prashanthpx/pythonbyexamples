"""
Example: Function Structure and Anatomy
Demonstrates the complete structure of a Python function with all components.

Key Concepts:
- Function components (def, name, parameters, body, return)
- Naming conventions (PEP 8)
- Function annotations and type hints
- The pass statement
- Function attributes
"""


# ============================================================================
# ANATOMY OF A FUNCTION
# ============================================================================

def complete_function_example(
    required_param: str,
    optional_param: int = 10,
    *args: int,
    keyword_only: bool = False,
    **kwargs: str
) -> dict[str, any]:
    """
    A complete function showing all possible components.
    
    This function demonstrates:
    - Required parameters
    - Optional parameters (with defaults)
    - Variable positional arguments (*args)
    - Keyword-only parameters
    - Variable keyword arguments (**kwargs)
    - Type annotations
    - Return type annotation
    - Docstring
    
    Args:
        required_param: A required string parameter
        optional_param: An optional integer (default: 10)
        *args: Variable positional arguments
        keyword_only: Must be passed as keyword argument
        **kwargs: Variable keyword arguments
        
    Returns:
        Dictionary containing all received arguments
        
    Example:
        >>> complete_function_example("test", 20, 1, 2, 3, keyword_only=True, extra="value")
    """
    # Function body starts here
    result = {
        "required": required_param,
        "optional": optional_param,
        "args": args,
        "keyword_only": keyword_only,
        "kwargs": kwargs
    }
    
    # Return statement
    return result


# ============================================================================
# NAMING CONVENTIONS (PEP 8)
# ============================================================================

def good_function_name() -> None:
    """
    Good: lowercase with underscores (snake_case).
    
    PEP 8 Guidelines:
    - Use lowercase letters
    - Separate words with underscores
    - Use descriptive names
    - Start with a verb for actions
    """
    pass


def calculate_total_price(items: list[float]) -> float:
    """Good: Descriptive name that explains what it does."""
    return sum(items)


def get_user_name() -> str:
    """Good: Starts with verb (get), describes action."""
    return "John Doe"


def is_valid_email(email: str) -> bool:
    """Good: Boolean function starts with 'is', 'has', 'can', etc."""
    return "@" in email


# Bad examples (for demonstration only - don't use these patterns):
# def MyFunction():  # Bad: PascalCase (use for classes, not functions)
# def CALCULATE():   # Bad: ALL_CAPS (use for constants, not functions)
# def f():           # Bad: Single letter (not descriptive)
# def calc():        # Bad: Abbreviated (use full words)


# ============================================================================
# THE PASS STATEMENT
# ============================================================================

def placeholder_function() -> None:
    """
    Function with pass statement.
    
    The 'pass' statement is a null operation - it does nothing.
    Used as a placeholder when you need a function body but
    haven't implemented it yet.
    """
    pass  # ← Important: Placeholder for future implementation


def another_placeholder(x: int) -> int:
    """
    Another placeholder example.
    
    Useful during development when you're defining the API
    but haven't implemented the logic yet.
    """
    pass  # TODO: Implement this function


# ============================================================================
# MINIMAL FUNCTION
# ============================================================================

def minimal() -> None:
    """Minimal valid function."""
    pass


# ============================================================================
# FUNCTION WITH ONLY RETURN
# ============================================================================

def return_constant() -> int:
    """Function that just returns a constant."""
    return 42


# ============================================================================
# FUNCTION ATTRIBUTES
# ============================================================================

def function_with_attributes(x: int, y: int = 5) -> int:
    """
    Function demonstrating introspection attributes.
    
    Every function has special attributes that can be accessed:
    - __name__: Function name
    - __doc__: Docstring
    - __annotations__: Type hints
    - __defaults__: Default parameter values
    - __code__: Code object
    """
    return x + y


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("FUNCTION STRUCTURE - EXAMPLES")
    print("=" * 60)
    
    # ========================================================================
    # 1. COMPLETE FUNCTION EXAMPLE
    # ========================================================================
    print("\n1. COMPLETE FUNCTION WITH ALL COMPONENTS:")
    
    result = complete_function_example(
        "hello",           # required_param
        20,                # optional_param
        1, 2, 3,          # *args
        keyword_only=True, # keyword_only parameter
        extra="value",     # **kwargs
        another="data"
    )
    
    print(f"   Result: {result}")

    # ========================================================================
    # 2. NAMING CONVENTIONS
    # ========================================================================
    print("\n2. NAMING CONVENTIONS (PEP 8):")
    print("   ✓ good_function_name() - snake_case")
    print("   ✓ calculate_total_price() - descriptive, starts with verb")
    print("   ✓ get_user_name() - action verb")
    print("   ✓ is_valid_email() - boolean function")
    print("\n   ✗ MyFunction() - PascalCase (use for classes)")
    print("   ✗ CALCULATE() - ALL_CAPS (use for constants)")
    print("   ✗ f() - too short, not descriptive")
    print("   ✗ calc() - abbreviated")

    # ========================================================================
    # 3. THE PASS STATEMENT
    # ========================================================================
    print("\n3. THE PASS STATEMENT:")
    print("   Used as placeholder for future implementation")

    placeholder_function()  # Does nothing, but valid
    print("   ✓ placeholder_function() executed (does nothing)")

    # ========================================================================
    # 4. FUNCTION ATTRIBUTES (INTROSPECTION)
    # ========================================================================
    print("\n4. FUNCTION ATTRIBUTES:")

    func = function_with_attributes

    print(f"   __name__: {func.__name__}")
    print(f"   __doc__: {func.__doc__[:50]}...")
    print(f"   __annotations__: {func.__annotations__}")
    print(f"   __defaults__: {func.__defaults__}")

    # ← Important: Functions are objects with attributes

    # ========================================================================
    # 5. FUNCTION COMPONENTS BREAKDOWN
    # ========================================================================
    print("\n5. FUNCTION COMPONENTS BREAKDOWN:")
    print("""
   def function_name(parameters) -> return_type:
       │      │           │              │
       │      │           │              └─ Return type annotation
       │      │           └──────────────── Parameters with type hints
       │      └──────────────────────────── Function name (snake_case)
       └─────────────────────────────────── 'def' keyword

       \"\"\"Docstring describing the function.\"\"\"

       # Function body (indented)
       result = some_computation()

       return result  # Return statement
    """)

    # ========================================================================
    # 6. MINIMAL VALID FUNCTION
    # ========================================================================
    print("\n6. MINIMAL VALID FUNCTION:")
    print("   def minimal() -> None:")
    print("       pass")
    print("\n   This is the smallest valid function in Python")

    # ========================================================================
    # 7. TESTING FUNCTIONS
    # ========================================================================
    print("\n7. TESTING FUNCTIONS:")

    # Test naming convention functions
    total = calculate_total_price([10.0, 20.0, 30.0])
    print(f"   calculate_total_price([10, 20, 30]) = {total}")

    name = get_user_name()
    print(f"   get_user_name() = '{name}'")

    valid = is_valid_email("test@example.com")
    print(f"   is_valid_email('test@example.com') = {valid}")

    invalid = is_valid_email("invalid-email")
    print(f"   is_valid_email('invalid-email') = {invalid}")

    # Test constant return
    constant = return_constant()
    print(f"   return_constant() = {constant}")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Function structure: def name(params) -> return_type:")
    print("2. Use snake_case for function names (PEP 8)")
    print("3. Start function names with verbs (get, calculate, is, etc.)")
    print("4. Add type annotations for parameters and return values")
    print("5. Write docstrings for all public functions")
    print("6. Use 'pass' as placeholder during development")
    print("7. Functions are objects with introspectable attributes")
    print("=" * 60)

