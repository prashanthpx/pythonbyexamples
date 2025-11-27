"""
Example: Local Scope
Demonstrates local variable scope in Python functions.

Key Concepts:
- Variables created inside a function are local
- Local variables only exist during function execution
- Local variables are destroyed when function returns
- Each function call creates a new local scope
"""


def simple_function() -> str:
    """
    Basic example of local scope.
    
    Returns:
        A message string
    """
    # ← This variable is LOCAL to this function
    message = "Hello from local scope!"
    return message


def multiple_locals() -> int:
    """
    Multiple local variables in one function.
    
    Returns:
        The calculated result
    """
    # ← All these variables are LOCAL
    x = 10
    y = 20
    z = 30
    result = x + y + z  # ← Also local
    
    return result


def nested_blocks() -> str:
    """
    Local variables in nested blocks (if, for, while).
    
    Returns:
        A message string
        
    Note:
        Unlike some languages, Python doesn't have block scope.
        Variables created in if/for/while are still function-local.
    """
    result = "Start"  # ← Local to function
    
    if True:
        # ← This variable is still function-local, not block-local
        inside_if = "Created in if block"
        result = inside_if  # Can access and modify
    
    # ← Can still access 'inside_if' here (no block scope in Python)
    for i in range(3):
        inside_loop = f"Loop iteration {i}"  # ← Also function-local
    
    # ← Can still access 'inside_loop' and 'i' here
    final = f"{result}, {inside_loop}, i={i}"
    
    return final


def parameter_scope(name: str, age: int) -> str:
    """
    Parameters are also local variables.
    
    Args:
        name: Person's name
        age: Person's age
        
    Returns:
        Formatted string
        
    Note:
        Parameters are local variables initialized with argument values.
    """
    # ← 'name' and 'age' are LOCAL variables
    # They exist only during this function call
    
    greeting = f"Hello, {name}! You are {age} years old."
    
    # Modifying parameters doesn't affect the caller
    name = name.upper()  # ← Only changes local copy
    age = age + 1        # ← Only changes local copy
    
    return greeting


def separate_scopes() -> tuple[int, int]:
    """
    Demonstrates that each function has its own scope.
    
    Returns:
        Tuple of (result1, result2)
    """
    def helper1() -> int:
        # ← This 'x' is local to helper1
        x = 100
        return x
    
    def helper2() -> int:
        # ← This 'x' is local to helper2 (different from helper1's x)
        x = 200
        return x
    
    result1 = helper1()  # Returns 100
    result2 = helper2()  # Returns 200
    
    # ← Each function has its own 'x' variable
    
    return result1, result2


def scope_lifetime() -> list[int]:
    """
    Demonstrates that local variables are created and destroyed each call.
    
    Returns:
        List of results from multiple calls
    """
    def counter() -> int:
        # ← This variable is created fresh each time counter() is called
        count = 0
        count += 1
        return count
    
    # Each call creates a new 'count' variable
    results = []
    results.append(counter())  # Returns 1
    results.append(counter())  # Returns 1 (not 2!)
    results.append(counter())  # Returns 1 (not 3!)
    
    # ← Local variables don't persist between calls
    
    return results


def cannot_access_from_outside() -> str:
    """
    Local variables cannot be accessed from outside the function.
    
    Returns:
        A message string
    """
    secret = "This is local"  # ← Only accessible inside this function
    return secret


# ============================================================================
# DEMONSTRATION: Local scope
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LOCAL SCOPE - EXAMPLES")
    print("=" * 60)
    
    # ========================================================================
    # 1. SIMPLE LOCAL SCOPE
    # ========================================================================
    print("\n1. SIMPLE LOCAL SCOPE:")
    
    result = simple_function()
    print(f"   simple_function() = '{result}'")
    
    # ❌ Cannot access 'message' here - it's local to the function
    # print(message)  # NameError: name 'message' is not defined
    print("   ⚠️  Cannot access 'message' variable outside the function")

    # ========================================================================
    # 2. MULTIPLE LOCAL VARIABLES
    # ========================================================================
    print("\n2. MULTIPLE LOCAL VARIABLES:")

    result = multiple_locals()
    print(f"   multiple_locals() = {result}")
    print("   (x, y, z, result are all local to the function)")

    # ========================================================================
    # 3. NO BLOCK SCOPE IN PYTHON
    # ========================================================================
    print("\n3. NO BLOCK SCOPE IN PYTHON:")

    result = nested_blocks()
    print(f"   nested_blocks() = '{result}'")
    print("   Note: Variables created in if/for blocks are still function-local")
    print("   (Unlike C/Java, Python has no block scope)")

    # ========================================================================
    # 4. PARAMETERS ARE LOCAL
    # ========================================================================
    print("\n4. PARAMETERS ARE LOCAL:")

    original_name = "Alice"
    original_age = 30

    result = parameter_scope(original_name, original_age)
    print(f"   parameter_scope('{original_name}', {original_age}):")
    print(f"   '{result}'")
    print(f"\n   After function call:")
    print(f"   original_name = '{original_name}' (unchanged)")
    print(f"   original_age = {original_age} (unchanged)")
    print("   ← Modifying parameters inside function doesn't affect caller")

    # ========================================================================
    # 5. SEPARATE SCOPES
    # ========================================================================
    print("\n5. SEPARATE SCOPES:")

    result1, result2 = separate_scopes()
    print(f"   separate_scopes():")
    print(f"   helper1() returned: {result1}")
    print(f"   helper2() returned: {result2}")
    print("   ← Each function has its own 'x' variable")

    # ========================================================================
    # 6. SCOPE LIFETIME
    # ========================================================================
    print("\n6. SCOPE LIFETIME:")

    results = scope_lifetime()
    print(f"   scope_lifetime() = {results}")
    print("   ← Local variables are created fresh each call")
    print("   ← They don't persist between calls")

    # ========================================================================
    # 7. CANNOT ACCESS FROM OUTSIDE
    # ========================================================================
    print("\n7. CANNOT ACCESS FROM OUTSIDE:")

    result = cannot_access_from_outside()
    print(f"   cannot_access_from_outside() = '{result}'")

    # ❌ Cannot access 'secret' here
    # print(secret)  # NameError: name 'secret' is not defined
    print("   ⚠️  Cannot access 'secret' variable from outside")

    # ========================================================================
    # 8. PRACTICAL EXAMPLE
    # ========================================================================
    print("\n8. PRACTICAL EXAMPLE:")

    def calculate_total(prices: list[float], tax_rate: float = 0.1) -> float:
        """Calculate total with tax."""
        # ← All these variables are local
        subtotal = sum(prices)
        tax = subtotal * tax_rate
        total = subtotal + tax
        return total

    prices = [10.0, 20.0, 30.0]
    total = calculate_total(prices)
    print(f"   Prices: {prices}")
    print(f"   Total with tax: ${total:.2f}")
    print("   (subtotal, tax, total are local to calculate_total)")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Variables created inside a function are LOCAL")
    print("2. Local variables only exist during function execution")
    print("3. Local variables are destroyed when function returns")
    print("4. Each function call creates a NEW local scope")
    print("5. Parameters are local variables")
    print("6. Python has NO block scope (if/for/while)")
    print("7. Variables in if/for/while are still function-local")
    print("8. Cannot access local variables from outside the function")
    print("=" * 60)

