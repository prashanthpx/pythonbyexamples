"""
Example: LEGB Rule
Demonstrates Python's LEGB scope resolution rule.

LEGB stands for:
- L: Local (function scope)
- E: Enclosing (outer function scope)
- G: Global (module scope)
- B: Built-in (Python built-ins)

Key Concepts:
- Python searches scopes in LEGB order
- First match wins
- Understanding scope resolution is crucial
"""

# ============================================================================
# BUILT-IN SCOPE (B)
# ============================================================================
# Python built-in functions like len(), print(), str(), etc.
# These are always available without import

# ============================================================================
# GLOBAL SCOPE (G)
# ============================================================================

# ← Global variable (module level)
x = "GLOBAL"
name = "Global Name"


def demonstrate_legb() -> str:
    """
    Demonstrates LEGB scope resolution order.
    
    Returns:
        String showing scope resolution
    """
    # ← Local variable (L)
    x = "LOCAL"
    
    # When we reference 'x', Python finds it in Local scope first
    return f"x = {x}"  # Returns "LOCAL"


def demonstrate_enclosing() -> str:
    """
    Demonstrates Enclosing scope (E).
    
    Returns:
        String from nested function
    """
    # ← Enclosing scope variable (E)
    x = "ENCLOSING"
    
    def inner() -> str:
        # No local 'x', so Python looks in Enclosing scope
        return f"x = {x}"  # Returns "ENCLOSING"
    
    return inner()


def demonstrate_global_access() -> str:
    """
    Demonstrates Global scope (G) access.
    
    Returns:
        String from global scope
    """
    # No local 'name', no enclosing scope
    # Python looks in Global scope
    return f"name = {name}"  # Returns "Global Name"


def demonstrate_builtin() -> int:
    """
    Demonstrates Built-in scope (B).
    
    Returns:
        Length of a list
    """
    # 'len' is not local, not enclosing, not global
    # Python finds it in Built-in scope
    my_list = [1, 2, 3, 4, 5]
    return len(my_list)  # ← 'len' from built-in scope


def complete_legb_example() -> dict[str, str]:
    """
    Complete example showing all LEGB scopes.
    
    Returns:
        Dictionary with values from each scope
    """
    # ← Local variable (L)
    local_var = "LOCAL"
    
    def inner() -> dict[str, str]:
        # ← Local to inner (L for inner function)
        inner_local = "INNER LOCAL"
        
        return {
            "local": local_var,      # ← From Enclosing (E)
            "global": name,          # ← From Global (G)
            "builtin": str(42),      # ← 'str' from Built-in (B)
            "inner_local": inner_local  # ← From Local (L)
        }
    
    return inner()


def shadowing_example() -> dict[str, str]:
    """
    Demonstrates variable shadowing (same name in different scopes).
    
    Returns:
        Dictionary showing shadowing behavior
    """
    # ← Local 'x' shadows global 'x'
    x = "LOCAL x"
    
    def inner() -> dict[str, str]:
        # ← Local 'x' in inner shadows enclosing 'x'
        x = "INNER x"
        
        return {
            "inner_x": x,           # "INNER x" (Local)
            "global_x": globals()['x']  # "GLOBAL" (explicit global access)
        }
    
    result = inner()
    result["outer_x"] = x  # "LOCAL x" (Local to outer)
    
    return result


def scope_search_order() -> list[str]:
    """
    Demonstrates the order Python searches scopes.
    
    Returns:
        List showing search order
    """
    results = []
    
    # 1. Local scope (L)
    local_only = "local"
    results.append(f"1. Local: {local_only}")
    
    # 2. Enclosing scope (E)
    def outer():
        enclosing_var = "enclosing"
        
        def inner():
            # Searches: Local (not found) → Enclosing (found!)
            results.append(f"2. Enclosing: {enclosing_var}")
        
        inner()
    
    outer()
    
    # 3. Global scope (G)
    # Searches: Local (not found) → Enclosing (N/A) → Global (found!)
    results.append(f"3. Global: {name}")
    
    # 4. Built-in scope (B)
    # Searches: Local (not found) → Enclosing (N/A) → Global (not found) → Built-in (found!)
    results.append(f"4. Built-in: {len([1, 2, 3])}")
    
    return results


def modifying_scopes() -> dict[str, str]:
    """
    Demonstrates modifying different scopes.
    
    Returns:
        Dictionary with results
    """
    # Local variable
    local_var = "original local"
    
    # Modify local (no keyword needed)
    local_var = "modified local"
    
    def inner() -> dict[str, str]:
        # Modify enclosing (need 'nonlocal')
        nonlocal local_var
        local_var = "modified by inner"
        
        # Modify global (need 'global')
        global name
        original_global = name
        name = "Modified Global"
        
        return {
            "local_var": local_var,
            "original_global": original_global,
            "new_global": name
        }
    
    result = inner()
    result["after_inner"] = local_var

    return result


def builtin_shadowing() -> dict[str, str]:
    """
    Demonstrates shadowing built-in names (usually a bad idea!).

    Returns:
        Dictionary showing builtin shadowing
    """
    # ❌ BAD PRACTICE: Shadowing built-in 'len'
    len = "I'm not the built-in len!"  # ← Local 'len' shadows built-in

    # Now 'len' refers to the local variable, not the built-in function
    # len([1, 2, 3])  # TypeError: 'str' object is not callable

    # Can still access built-in via __builtins__
    import builtins
    actual_len = builtins.len([1, 2, 3])

    return {
        "local_len": len,
        "actual_len": str(actual_len)
    }


def practical_legb() -> dict[str, int]:
    """
    Practical example using LEGB.

    Returns:
        Dictionary with calculation results
    """
    # Global configuration
    global_multiplier = 2

    def calculate(values: list[int]) -> dict[str, int]:
        # Enclosing scope
        local_multiplier = 3

        def process(value: int) -> int:
            # Local scope
            result = value * local_multiplier * global_multiplier
            # Uses: value (L), local_multiplier (E), global_multiplier (E)
            return result

        # Use built-in 'sum' (B)
        total = sum(process(v) for v in values)

        return {
            "total": total,
            "count": len(values)  # ← 'len' from Built-in (B)
        }

    return calculate([1, 2, 3, 4, 5])


# ============================================================================
# DEMONSTRATION: LEGB Rule
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LEGB RULE - SCOPE RESOLUTION ORDER")
    print("=" * 60)

    print("\nLEGB stands for:")
    print("  L - Local (function scope)")
    print("  E - Enclosing (outer function scope)")
    print("  G - Global (module scope)")
    print("  B - Built-in (Python built-ins)")
    print("\nPython searches in this order: L → E → G → B")
    print("First match wins!")

    # ========================================================================
    # 1. LOCAL SCOPE (L)
    # ========================================================================
    print("\n" + "=" * 60)
    print("1. LOCAL SCOPE (L):")
    print("=" * 60)

    print(f"   Global x = '{x}'")
    result = demonstrate_legb()
    print(f"   demonstrate_legb() = '{result}'")
    print("   ← Local 'x' shadows global 'x'")

    # ========================================================================
    # 2. ENCLOSING SCOPE (E)
    # ========================================================================
    print("\n" + "=" * 60)
    print("2. ENCLOSING SCOPE (E):")
    print("=" * 60)

    result = demonstrate_enclosing()
    print(f"   demonstrate_enclosing() = '{result}'")
    print("   ← Inner function finds 'x' in enclosing scope")

    # ========================================================================
    # 3. GLOBAL SCOPE (G)
    # ========================================================================
    print("\n" + "=" * 60)
    print("3. GLOBAL SCOPE (G):")
    print("=" * 60)

    result = demonstrate_global_access()
    print(f"   demonstrate_global_access() = '{result}'")
    print("   ← Function finds 'name' in global scope")

    # ========================================================================
    # 4. BUILT-IN SCOPE (B)
    # ========================================================================
    print("\n" + "=" * 60)
    print("4. BUILT-IN SCOPE (B):")
    print("=" * 60)

    result = demonstrate_builtin()
    print(f"   demonstrate_builtin() = {result}")
    print("   ← 'len' found in built-in scope")

    # ========================================================================
    # 5. COMPLETE LEGB EXAMPLE
    # ========================================================================
    print("\n" + "=" * 60)
    print("5. COMPLETE LEGB EXAMPLE:")
    print("=" * 60)

    result = complete_legb_example()
    for key, value in result.items():
        print(f"   {key}: '{value}'")
    print("   ← Demonstrates all four scopes")

    # ========================================================================
    # 6. VARIABLE SHADOWING
    # ========================================================================
    print("\n" + "=" * 60)
    print("6. VARIABLE SHADOWING:")
    print("=" * 60)

    result = shadowing_example()
    for key, value in result.items():
        print(f"   {key}: '{value}'")
    print("   ← Same name in different scopes")

    # ========================================================================
    # 7. SCOPE SEARCH ORDER
    # ========================================================================
    print("\n" + "=" * 60)
    print("7. SCOPE SEARCH ORDER:")
    print("=" * 60)

    results = scope_search_order()
    for result in results:
        print(f"   {result}")
    print("   ← Python searches L → E → G → B")

    # ========================================================================
    # 8. MODIFYING SCOPES
    # ========================================================================
    print("\n" + "=" * 60)
    print("8. MODIFYING SCOPES:")
    print("=" * 60)

    # Reset global
    name = "Global Name"

    result = modifying_scopes()
    for key, value in result.items():
        print(f"   {key}: '{value}'")
    print("   ← Use 'nonlocal' for enclosing, 'global' for global")

    # Reset global again
    name = "Global Name"

    # ========================================================================
    # 9. BUILT-IN SHADOWING (BAD PRACTICE)
    # ========================================================================
    print("\n" + "=" * 60)
    print("9. BUILT-IN SHADOWING (BAD PRACTICE):")
    print("=" * 60)

    result = builtin_shadowing()
    for key, value in result.items():
        print(f"   {key}: {value}")
    print("   ⚠️  Avoid shadowing built-ins!")

    # ========================================================================
    # 10. PRACTICAL LEGB
    # ========================================================================
    print("\n" + "=" * 60)
    print("10. PRACTICAL LEGB:")
    print("=" * 60)

    result = practical_legb()
    print(f"   Calculation result: {result}")
    print("   ← Uses all LEGB scopes together")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. LEGB = Local → Enclosing → Global → Built-in")
    print("2. Python searches scopes in LEGB order")
    print("3. First match wins (stops searching)")
    print("4. Local scope: variables in current function")
    print("5. Enclosing scope: variables in outer functions")
    print("6. Global scope: module-level variables")
    print("7. Built-in scope: Python's built-in names")
    print("8. Variables in inner scopes 'shadow' outer scopes")
    print("9. Use 'nonlocal' to modify enclosing scope")
    print("10. Use 'global' to modify global scope")
    print("11. Avoid shadowing built-ins (bad practice)")
    print("=" * 60)

