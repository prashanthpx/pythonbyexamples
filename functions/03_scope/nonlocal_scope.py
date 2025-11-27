"""
Example: Nonlocal Scope
Demonstrates nonlocal variable scope in nested functions.

Key Concepts:
- Nonlocal variables are in enclosing function scope
- Use 'nonlocal' keyword to modify enclosing scope variables
- Common in closures and nested functions
- Different from both local and global scope
"""


def outer_function() -> str:
    """
    Demonstrates basic nonlocal scope.
    
    Returns:
        Message from inner function
    """
    # ← This variable is in the ENCLOSING scope for inner_function
    message = "Hello from outer"
    
    def inner_function() -> str:
        # ← Can read enclosing scope variables
        return f"Inner says: {message}"
    
    return inner_function()


def nonlocal_modification() -> tuple[str, str]:
    """
    Demonstrates modifying nonlocal variables.
    
    Returns:
        Tuple of (before, after) messages
    """
    message = "Original"  # ← Enclosing scope variable
    
    def try_modify_wrong() -> str:
        # ❌ This creates a LOCAL variable, doesn't modify enclosing
        message = "Modified"  # ← Creates new local variable
        return message
    
    def modify_correct() -> str:
        nonlocal message  # ← Declare we're using enclosing scope variable
        # ✅ Now this modifies the enclosing scope variable
        message = "Modified"
        return message
    
    before = try_modify_wrong()
    # message is still "Original" here
    
    after = modify_correct()
    # message is now "Modified"
    
    return before, message


def counter_closure() -> tuple[int, int, int]:
    """
    Classic closure example using nonlocal.
    
    Returns:
        Tuple of three counter values
        
    Note:
        This is a common pattern for creating stateful functions.
    """
    count = 0  # ← Enclosing scope variable
    
    def increment() -> int:
        nonlocal count  # ← Access enclosing scope
        count += 1
        return count
    
    # Each call increments the same 'count' variable
    first = increment()   # 1
    second = increment()  # 2
    third = increment()   # 3
    
    return first, second, third


def multiple_nonlocals() -> str:
    """
    Using multiple nonlocal variables.
    
    Returns:
        Formatted string with all values
    """
    x = 10  # ← Enclosing scope
    y = 20  # ← Enclosing scope
    z = 30  # ← Enclosing scope
    
    def modify_all() -> None:
        nonlocal x, y, z  # ← Multiple nonlocals
        x += 1
        y += 2
        z += 3
    
    modify_all()
    
    return f"x={x}, y={y}, z={z}"


def nested_levels() -> tuple[int, int, int]:
    """
    Nonlocal with multiple nesting levels.
    
    Returns:
        Tuple of (outer_val, middle_val, inner_val)
    """
    outer_var = 100  # ← Outermost enclosing scope
    
    def middle() -> tuple[int, int, int]:
        middle_var = 200  # ← Middle enclosing scope
        
        def inner() -> tuple[int, int, int]:
            inner_var = 300  # ← Local to inner
            
            # Can access both enclosing scopes
            nonlocal middle_var  # ← From middle()
            nonlocal outer_var   # ← From nested_levels()
            
            middle_var += 1
            outer_var += 1
            
            return outer_var, middle_var, inner_var
        
        return inner()
    
    return middle()


def nonlocal_vs_global() -> tuple[int, int]:
    """
    Demonstrates difference between nonlocal and global.
    
    Returns:
        Tuple of (nonlocal_val, global_val)
    """
    enclosing_var = 100  # ← Enclosing scope
    
    def inner() -> tuple[int, int]:
        nonlocal enclosing_var  # ← Refers to enclosing function's variable
        # global would refer to module-level variable
        
        enclosing_var += 1
        
        return enclosing_var, GLOBAL_VAR
    
    return inner()


# Global variable for comparison
GLOBAL_VAR = 999


def create_counter(start: int = 0):
    """
    Factory function that creates counter functions.
    
    Args:
        start: Starting value for counter
        
    Returns:
        A counter function
        
    Note:
        This is a practical use of nonlocal - creating closures.
    """
    count = start  # ← Enclosing scope
    
    def counter() -> int:
        nonlocal count  # ← Modify enclosing scope
        count += 1
        return count
    
    return counter  # ← Return the inner function


def create_account(initial_balance: float = 0.0):
    """
    Factory function that creates account management functions.
    
    Args:
        initial_balance: Starting balance
        
    Returns:
        Tuple of (deposit, withdraw, get_balance) functions
    """
    balance = initial_balance  # ← Enclosing scope (private state)
    
    def deposit(amount: float) -> float:
        nonlocal balance
        balance += amount
        return balance
    
    def withdraw(amount: float) -> float:
        nonlocal balance
        if amount <= balance:
            balance -= amount
        return balance
    
    def get_balance() -> float:
        return balance  # ← Can read without nonlocal
    
    return deposit, withdraw, get_balance


# ============================================================================
# DEMONSTRATION: Nonlocal scope
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NONLOCAL SCOPE - EXAMPLES")
    print("=" * 60)

    # ========================================================================
    # 1. READING ENCLOSING SCOPE
    # ========================================================================
    print("\n1. READING ENCLOSING SCOPE:")

    result = outer_function()
    print(f"   outer_function() = '{result}'")
    print("   ← Inner function can read enclosing scope variables")

    # ========================================================================
    # 2. MODIFYING NONLOCAL VARIABLES
    # ========================================================================
    print("\n2. MODIFYING NONLOCAL VARIABLES:")

    before, after = nonlocal_modification()
    print(f"   Without 'nonlocal': '{before}'")
    print(f"   With 'nonlocal': '{after}'")
    print("   ← Need 'nonlocal' keyword to modify enclosing scope")

    # ========================================================================
    # 3. COUNTER CLOSURE
    # ========================================================================
    print("\n3. COUNTER CLOSURE:")

    first, second, third = counter_closure()
    print(f"   First call: {first}")
    print(f"   Second call: {second}")
    print(f"   Third call: {third}")
    print("   ← Nonlocal variable persists across inner function calls")

    # ========================================================================
    # 4. MULTIPLE NONLOCALS
    # ========================================================================
    print("\n4. MULTIPLE NONLOCALS:")

    result = multiple_nonlocals()
    print(f"   multiple_nonlocals() = '{result}'")
    print("   ← Can declare multiple nonlocal variables")

    # ========================================================================
    # 5. NESTED LEVELS
    # ========================================================================
    print("\n5. NESTED LEVELS:")

    outer_val, middle_val, inner_val = nested_levels()
    print(f"   outer_var = {outer_val}")
    print(f"   middle_var = {middle_val}")
    print(f"   inner_var = {inner_val}")
    print("   ← Can access multiple enclosing scope levels")

    # ========================================================================
    # 6. NONLOCAL VS GLOBAL
    # ========================================================================
    print("\n6. NONLOCAL VS GLOBAL:")

    nonlocal_val, global_val = nonlocal_vs_global()
    print(f"   nonlocal variable = {nonlocal_val}")
    print(f"   global variable = {global_val}")
    print("   ← 'nonlocal' refers to enclosing function scope")
    print("   ← 'global' refers to module-level scope")

    # ========================================================================
    # 7. COUNTER FACTORY
    # ========================================================================
    print("\n7. COUNTER FACTORY:")

    counter1 = create_counter(0)
    counter2 = create_counter(100)

    print(f"   counter1(): {counter1()}")  # 1
    print(f"   counter1(): {counter1()}")  # 2
    print(f"   counter1(): {counter1()}")  # 3

    print(f"   counter2(): {counter2()}")  # 101
    print(f"   counter2(): {counter2()}")  # 102

    print("   ← Each counter has its own enclosing scope")

    # ========================================================================
    # 8. ACCOUNT FACTORY (PRACTICAL EXAMPLE)
    # ========================================================================
    print("\n8. ACCOUNT FACTORY (PRACTICAL EXAMPLE):")

    deposit, withdraw, get_balance = create_account(100.0)

    print(f"   Initial balance: ${get_balance():.2f}")

    deposit(50.0)
    print(f"   After deposit $50: ${get_balance():.2f}")

    withdraw(30.0)
    print(f"   After withdraw $30: ${get_balance():.2f}")

    withdraw(200.0)  # Insufficient funds
    print(f"   After trying to withdraw $200: ${get_balance():.2f}")

    print("   ← Nonlocal creates private state (encapsulation)")

    # ========================================================================
    # 9. MULTIPLE ACCOUNTS
    # ========================================================================
    print("\n9. MULTIPLE ACCOUNTS:")

    # Create two separate accounts
    deposit1, withdraw1, balance1 = create_account(1000.0)
    deposit2, withdraw2, balance2 = create_account(500.0)

    deposit1(100.0)
    deposit2(50.0)

    print(f"   Account 1 balance: ${balance1():.2f}")
    print(f"   Account 2 balance: ${balance2():.2f}")
    print("   ← Each account has its own independent state")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. 'nonlocal' refers to enclosing function scope")
    print("2. Use 'nonlocal' to modify enclosing scope variables")
    print("3. Without 'nonlocal', assignment creates local variable")
    print("4. Can read enclosing scope without 'nonlocal'")
    print("5. Common in closures and factory functions")
    print("6. Each closure has its own enclosing scope")
    print("7. 'nonlocal' != 'global' (different scopes)")
    print("8. Useful for creating private state (encapsulation)")
    print("=" * 60)

