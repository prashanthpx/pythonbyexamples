"""
Example: Enclosing Scope
Demonstrates enclosing (nonlocal) scope in nested functions.

Key Concepts:
- Enclosing scope is the scope of outer functions
- Nested functions can access enclosing scope
- Multiple levels of enclosing scopes possible
- Closures capture enclosing scope
"""


def simple_enclosing() -> str:
    """
    Basic example of enclosing scope.
    
    Returns:
        Message from nested function
    """
    outer_var = "I'm in enclosing scope"  # ← Enclosing scope
    
    def inner() -> str:
        # ← Can access enclosing scope
        return outer_var
    
    return inner()


def multiple_nested_levels() -> str:
    """
    Multiple levels of enclosing scopes.
    
    Returns:
        Message showing all scope levels
    """
    level1 = "Level 1"  # ← Enclosing for level2 and level3
    
    def level2() -> str:
        level2_var = "Level 2"  # ← Enclosing for level3
        
        def level3() -> str:
            level3_var = "Level 3"  # ← Local to level3
            
            # ← Can access all enclosing scopes
            return f"{level1}, {level2_var}, {level3_var}"
        
        return level3()
    
    return level2()


def closure_example() -> tuple[int, int, int]:
    """
    Closure captures enclosing scope.
    
    Returns:
        Tuple of three values from closure
        
    Note:
        The inner function 'remembers' the enclosing scope
        even after the outer function returns.
    """
    x = 0  # ← Enclosing scope variable
    
    def increment() -> int:
        nonlocal x
        x += 1
        return x
    
    # Call the inner function multiple times
    first = increment()
    second = increment()
    third = increment()
    
    return first, second, third


def closure_factory(multiplier: int):
    """
    Factory that creates closures with different enclosing scopes.
    
    Args:
        multiplier: The multiplier to use
        
    Returns:
        A function that multiplies by the given multiplier
        
    Note:
        Each returned function has its own enclosing scope.
    """
    # ← 'multiplier' is in enclosing scope for the inner function
    
    def multiply(x: int) -> int:
        # ← Accesses 'multiplier' from enclosing scope
        return x * multiplier
    
    return multiply  # ← Return the function (closure)


def make_adder(n: int):
    """
    Creates a function that adds n to its argument.
    
    Args:
        n: The number to add
        
    Returns:
        A function that adds n
    """
    def adder(x: int) -> int:
        return x + n  # ← 'n' from enclosing scope
    
    return adder


def make_counter_with_step(start: int = 0, step: int = 1):
    """
    Creates a counter with custom start and step.
    
    Args:
        start: Starting value
        step: Increment step
        
    Returns:
        A counter function
    """
    count = start  # ← Enclosing scope
    
    def counter() -> int:
        nonlocal count
        current = count
        count += step  # ← 'step' from enclosing scope
        return current
    
    return counter


def enclosing_with_multiple_functions():
    """
    Multiple inner functions sharing the same enclosing scope.
    
    Returns:
        Tuple of (get, increment, decrement, reset) functions
    """
    value = 0  # ← Shared enclosing scope
    
    def get() -> int:
        return value
    
    def increment() -> int:
        nonlocal value
        value += 1
        return value
    
    def decrement() -> int:
        nonlocal value
        value -= 1
        return value
    
    def reset() -> int:
        nonlocal value
        value = 0
        return value
    
    # ← All four functions share the same 'value' variable
    return get, increment, decrement, reset


def enclosing_scope_lifetime():
    """
    Demonstrates that enclosing scope persists as long as closure exists.
    
    Returns:
        A function that demonstrates scope lifetime
    """
    data = []  # ← Enclosing scope (persists with closure)
    
    def add_item(item: str) -> list[str]:
        nonlocal data
        data.append(item)
        return data.copy()
    
    return add_item


def nested_closures():
    """
    Closures within closures.
    
    Returns:
        A nested closure function
    """
    outer_val = "outer"  # ← Enclosing for middle and inner
    
    def middle():
        middle_val = "middle"  # ← Enclosing for inner
        
        def inner() -> str:
            inner_val = "inner"  # ← Local
            return f"{outer_val}, {middle_val}, {inner_val}"
        
        return inner  # ← Return closure
    
    return middle  # ← Return closure that returns closure


# ============================================================================
# DEMONSTRATION: Enclosing scope
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ENCLOSING SCOPE - EXAMPLES")
    print("=" * 60)

    # ========================================================================
    # 1. SIMPLE ENCLOSING SCOPE
    # ========================================================================
    print("\n1. SIMPLE ENCLOSING SCOPE:")

    result = simple_enclosing()
    print(f"   simple_enclosing() = '{result}'")
    print("   ← Inner function accesses enclosing scope")

    # ========================================================================
    # 2. MULTIPLE NESTED LEVELS
    # ========================================================================
    print("\n2. MULTIPLE NESTED LEVELS:")

    result = multiple_nested_levels()
    print(f"   multiple_nested_levels() = '{result}'")
    print("   ← Can access multiple enclosing scope levels")

    # ========================================================================
    # 3. CLOSURE EXAMPLE
    # ========================================================================
    print("\n3. CLOSURE EXAMPLE:")

    first, second, third = closure_example()
    print(f"   First: {first}, Second: {second}, Third: {third}")
    print("   ← Closure captures and modifies enclosing scope")

    # ========================================================================
    # 4. CLOSURE FACTORY
    # ========================================================================
    print("\n4. CLOSURE FACTORY:")

    times2 = closure_factory(2)
    times5 = closure_factory(5)
    times10 = closure_factory(10)

    print(f"   times2(7) = {times2(7)}")
    print(f"   times5(7) = {times5(7)}")
    print(f"   times10(7) = {times10(7)}")
    print("   ← Each closure has its own enclosing scope")

    # ========================================================================
    # 5. ADDER FACTORY
    # ========================================================================
    print("\n5. ADDER FACTORY:")

    add5 = make_adder(5)
    add10 = make_adder(10)

    print(f"   add5(3) = {add5(3)}")
    print(f"   add10(3) = {add10(3)}")
    print("   ← Closures remember their enclosing scope")

    # ========================================================================
    # 6. COUNTER WITH STEP
    # ========================================================================
    print("\n6. COUNTER WITH STEP:")

    count_by_1 = make_counter_with_step(0, 1)
    count_by_5 = make_counter_with_step(100, 5)

    print(f"   count_by_1: {count_by_1()}, {count_by_1()}, {count_by_1()}")
    print(f"   count_by_5: {count_by_5()}, {count_by_5()}, {count_by_5()}")
    print("   ← Each counter has independent enclosing scope")

    # ========================================================================
    # 7. SHARED ENCLOSING SCOPE
    # ========================================================================
    print("\n7. SHARED ENCLOSING SCOPE:")

    get, increment, decrement, reset = enclosing_with_multiple_functions()

    print(f"   Initial: {get()}")
    print(f"   After increment: {increment()}")
    print(f"   After increment: {increment()}")
    print(f"   After decrement: {decrement()}")
    print(f"   After reset: {reset()}")
    print("   ← All functions share the same enclosing scope")

    # ========================================================================
    # 8. ENCLOSING SCOPE LIFETIME
    # ========================================================================
    print("\n8. ENCLOSING SCOPE LIFETIME:")

    add_item = enclosing_scope_lifetime()

    print(f"   add_item('apple'): {add_item('apple')}")
    print(f"   add_item('banana'): {add_item('banana')}")
    print(f"   add_item('cherry'): {add_item('cherry')}")
    print("   ← Enclosing scope persists as long as closure exists")

    # ========================================================================
    # 9. NESTED CLOSURES
    # ========================================================================
    print("\n9. NESTED CLOSURES:")

    middle_func = nested_closures()
    inner_func = middle_func()
    result = inner_func()

    print(f"   nested_closures()()() = '{result}'")
    print("   ← Closures can be nested multiple levels")

    # ========================================================================
    # 10. PRACTICAL: PRIVATE STATE
    # ========================================================================
    print("\n10. PRACTICAL: PRIVATE STATE:")

    def create_person(name: str):
        """Create a person with private state."""
        # ← Private state in enclosing scope
        _name = name
        _age = 0

        def get_name() -> str:
            return _name

        def get_age() -> int:
            return _age

        def set_age(age: int) -> None:
            nonlocal _age
            if age >= 0:
                _age = age

        def birthday() -> int:
            nonlocal _age
            _age += 1
            return _age

        return get_name, get_age, set_age, birthday

    get_name, get_age, set_age, birthday = create_person("Alice")

    print(f"   Name: {get_name()}")
    print(f"   Age: {get_age()}")

    set_age(25)
    print(f"   After set_age(25): {get_age()}")

    birthday()
    birthday()
    print(f"   After 2 birthdays: {get_age()}")

    print("   ← Enclosing scope provides encapsulation")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Enclosing scope = scope of outer/enclosing functions")
    print("2. Nested functions can access enclosing scope")
    print("3. Multiple levels of enclosing scopes possible")
    print("4. Closures 'capture' enclosing scope")
    print("5. Enclosing scope persists with closure")
    print("6. Each closure has its own enclosing scope")
    print("7. Multiple functions can share enclosing scope")
    print("8. Useful for creating private state")
    print("9. Common pattern in factory functions")
    print("=" * 60)

