"""Example: Parameter Order Rules

Demonstrates the correct order of different parameter types in Python.

Key Concepts:
- Parameter order rules
- Positional-only (/)
- Standard parameters
- *args
- Keyword-only (*)
- **kwargs
- What happens when you break the rules
"""

from typing import Any, Optional


def correct_order(
    pos_only1: str,
    pos_only2: str,
    /,
    standard1: str,
    standard2: str = "default",
    *args: int,
    kw_only1: str,
    kw_only2: str = "default",
    **kwargs: Any
) -> dict[str, Any]:
    """
    Function demonstrating correct parameter order.
    
    Parameter Order (MUST follow this order):
    1. Positional-only parameters (before /)
    2. / marker (optional)
    3. Standard parameters (can be positional or keyword)
    4. *args (optional)
    5. Keyword-only parameters (after * or *args)
    6. **kwargs (optional)
    
    Args:
        pos_only1: Positional-only (required)
        pos_only2: Positional-only (required)
        /: Positional-only marker
        standard1: Standard (required)
        standard2: Standard with default
        *args: Variable positional arguments
        kw_only1: Keyword-only (required)
        kw_only2: Keyword-only with default
        **kwargs: Variable keyword arguments
        
    Returns:
        Dictionary with all parameters
    """
    return {
        "pos_only1": pos_only1,
        "pos_only2": pos_only2,
        "standard1": standard1,
        "standard2": standard2,
        "args": args,
        "kw_only1": kw_only1,
        "kw_only2": kw_only2,
        "kwargs": kwargs
    }


def minimal_example(a: str, b: str = "default") -> str:
    """
    Minimal: Just standard parameters.
    
    Args:
        a: Required standard parameter
        b: Optional standard parameter
        
    Returns:
        Formatted string
    """
    return f"a={a}, b={b}"


def with_pos_only(a: str, /, b: str) -> str:
    """
    With positional-only parameter.
    
    Args:
        a: Positional-only (before /)
        /: Positional-only marker
        b: Standard parameter
        
    Returns:
        Formatted string
    """
    return f"a={a}, b={b}"


def with_args(a: str, *args: int) -> tuple[str, tuple[int, ...]]:
    """
    With *args.
    
    Args:
        a: Required standard parameter
        *args: Variable positional arguments
        
    Returns:
        Tuple of (a, args)
        
    Note:
        No parameters can come after *args except keyword-only.
    """
    return (a, args)


def with_kw_only(a: str, *, b: str) -> str:
    """
    With keyword-only parameter.
    
    Args:
        a: Standard parameter
        *: Keyword-only marker
        b: Keyword-only parameter
        
    Returns:
        Formatted string
    """
    return f"a={a}, b={b}"


def with_kwargs(a: str, **kwargs: Any) -> dict[str, Any]:
    """
    With **kwargs.
    
    Args:
        a: Required standard parameter
        **kwargs: Variable keyword arguments
        
    Returns:
        Dictionary with all parameters
    """
    return {"a": a, **kwargs}


def args_and_kw_only(a: str, *args: int, b: str, c: str = "default") -> dict[str, Any]:
    """
    Combining *args with keyword-only parameters.
    
    Args:
        a: Standard parameter
        *args: Variable positional arguments
        b: Keyword-only (required)
        c: Keyword-only with default
        
    Returns:
        Dictionary with all parameters
        
    Important:
        Parameters after *args MUST be keyword-only.
    """
    return {"a": a, "args": args, "b": b, "c": c}


def log_number_required_first(nu: int, sl: Optional[int] = 10) -> None:
    """Required parameter before optional with default.

    This follows the rule "required parameters come before optional" within
    the same parameter group, so it is valid and unambiguous.

    Examples:
        log_number_required_first(100)      # nu=100, sl=10 (default)
        log_number_required_first(5, 20)    # nu=5,   sl=20
    """

    print(f"sl={sl}, nu={nu}")


def log_number_keyword_only(sl: Optional[int] = 10, *, nu: int) -> None:
    """Keep ``sl`` first by making ``nu`` keyword-only.

    Here ``sl`` is a standard parameter with a default value, and ``nu`` is a
    required keyword-only parameter. Callers must pass ``nu`` by name.

    Examples:
        log_number_keyword_only(nu=20)      # sl=10 (default), nu=20
        log_number_keyword_only(5, nu=20)   # sl=5,           nu=20
    """

    print(f"sl={sl}, nu={nu}")


# ============================================================================
# DEMONSTRATION: Parameter order rules
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PARAMETER ORDER RULES - EXAMPLES")
    print("=" * 60)
    
    # ========================================================================
    # 1. CORRECT PARAMETER ORDER
    # ========================================================================
    print("\n1. CORRECT PARAMETER ORDER:")
    print("   Order: pos_only, /, standard, *args, kw_only, **kwargs")
    
    result = correct_order(
        "p1", "p2",              # positional-only
        "s1",                    # standard (positional)
        1, 2, 3,                # *args
        kw_only1="k1",          # keyword-only
        extra="value"           # **kwargs
    )
    
    print("\n   correct_order('p1', 'p2', 's1', 1, 2, 3,")
    print("                 kw_only1='k1', extra='value'):")
    for key, value in result.items():
        print(f"     {key}: {value}")

    # ========================================================================
    # 2. MINIMAL EXAMPLE
    # ========================================================================
    print("\n2. MINIMAL EXAMPLE (just standard params):")

    result1 = minimal_example("value1")
    print(f"   minimal_example('value1') = '{result1}'")

    result2 = minimal_example("value1", "value2")
    print(f"   minimal_example('value1', 'value2') = '{result2}'")

    # ========================================================================
    # 3. WITH POSITIONAL-ONLY
    # ========================================================================
    print("\n3. WITH POSITIONAL-ONLY (/):")

    result = with_pos_only("pos_value", "std_value")
    print(f"   with_pos_only('pos_value', 'std_value') = '{result}'")

    # Can use keyword for standard param
    result2 = with_pos_only("pos_value", b="std_value")
    print(f"   with_pos_only('pos_value', b='std_value') = '{result2}'")

    # ❌ Cannot use keyword for positional-only
    # with_pos_only(a="pos_value", b="std_value")  # TypeError
    print("   ⚠️  Cannot use: with_pos_only(a='pos_value', b='std_value')")

    # ========================================================================
    # 4. WITH *ARGS
    # ========================================================================
    print("\n4. WITH *ARGS:")

    result1 = with_args("value")
    print(f"   with_args('value') = {result1}")

    result2 = with_args("value", 1, 2, 3)
    print(f"   with_args('value', 1, 2, 3) = {result2}")

    # ========================================================================
    # 5. WITH KEYWORD-ONLY (*)
    # ========================================================================
    print("\n5. WITH KEYWORD-ONLY (*):")

    result = with_kw_only("value1", b="value2")
    print(f"   with_kw_only('value1', b='value2') = '{result}'")

    # ❌ Cannot use positional for keyword-only
    # with_kw_only("value1", "value2")  # TypeError
    print("   ⚠️  Cannot use: with_kw_only('value1', 'value2')")

    # ========================================================================
    # 6. WITH **KWARGS
    # ========================================================================
    print("\n6. WITH **KWARGS:")

    result = with_kwargs("value", x=1, y=2, z=3)
    print(f"   with_kwargs('value', x=1, y=2, z=3) = {result}")

    # ========================================================================
    # 7. *ARGS WITH KEYWORD-ONLY
    # ========================================================================
    print("\n7. *ARGS WITH KEYWORD-ONLY:")

    result1 = args_and_kw_only("a_value", b="b_value")
    print(f"   args_and_kw_only('a_value', b='b_value'):")
    print(f"   {result1}")

    result2 = args_and_kw_only("a_value", 1, 2, 3, b="b_value", c="c_value")
    print(f"\n   args_and_kw_only('a_value', 1, 2, 3, b='b_value', c='c_value'):")
    print(f"   {result2}")

    # ← Parameters after *args MUST be keyword-only

    # ========================================================================
    # 8. PARAMETER ORDER SUMMARY
    # ========================================================================
    print("\n8. PARAMETER ORDER SUMMARY:")
    print("""
   def function(
       pos_only1, pos_only2, /,        # 1. Positional-only (optional)
       standard1, standard2=default,   # 2. Standard parameters
       *args,                          # 3. Variable positional (optional)
       kw_only1, kw_only2=default,    # 4. Keyword-only
       **kwargs                        # 5. Variable keyword (optional)
   ):
       pass

   Rules:
   - Positional-only must come first (before /)
   - Standard parameters come next
   - *args comes after standard parameters
   - Keyword-only parameters come after * or *args
   - **kwargs must come last
   - Required parameters before optional (within each group)
    """)

    # ========================================================================
    # 9. COMMON PATTERNS
    # ========================================================================
    print("\n9. COMMON PATTERNS:")

    print("   Pattern 1: Standard only")
    print("   def func(a, b, c=default):")

    print("\n   Pattern 2: With *args")
    print("   def func(a, *args):")

    print("\n   Pattern 3: With **kwargs")
    print("   def func(a, b=default, **kwargs):")

    print("\n   Pattern 4: With keyword-only")
    print("   def func(a, *, b, c=default):")

    print("\n   Pattern 5: Everything")
    print("   def func(pos, /, std, *args, kw, **kwargs):")

    # ========================================================================
    # 10. DEFAULT VS REQUIRED ORDER (log_number example)
    # ========================================================================
    print("\n10. DEFAULT VS REQUIRED ORDER (log_number example):")

    print("   log_number_required_first(100):")
    log_number_required_first(100)

    print("   log_number_keyword_only(5, nu=20):")
    log_number_keyword_only(5, nu=20)

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Parameter order is STRICT and enforced by Python")
    print("2. Order: pos_only, /, standard, *args, kw_only, **kwargs")
    print("3. Required params before optional (within each group)")
    print("4. '/' makes preceding params positional-only")
    print("5. '*' or *args makes following params keyword-only")
    print("6. **kwargs must always come last")
    print("7. Breaking order rules causes SyntaxError")
    print("=" * 60)

