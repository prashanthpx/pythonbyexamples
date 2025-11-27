"""
Example: Global Scope
Demonstrates global variable scope in Python.

Key Concepts:
- Variables defined at module level are global
- Global variables can be read from anywhere
- Use 'global' keyword to modify global variables
- Global variables persist for the program's lifetime
"""

from typing import Optional

# ============================================================================
# GLOBAL VARIABLES (defined at module level)
# ============================================================================

# ← These variables are GLOBAL (module-level)
GLOBAL_CONSTANT = 100  # Convention: UPPERCASE for constants
global_counter = 0     # Global variable (can be modified)
global_list = []       # Global mutable object


def read_global() -> int:
    """
    Functions can READ global variables without any special syntax.
    
    Returns:
        The value of GLOBAL_CONSTANT
    """
    # ← Can read global variables directly
    return GLOBAL_CONSTANT


def try_modify_global_wrong() -> None:
    """
    Attempting to modify global without 'global' keyword creates a local variable.
    
    This is a common mistake!
    """
    # ❌ This creates a NEW LOCAL variable, doesn't modify global
    global_counter = 10  # ← Creates local 'global_counter'
    print(f"   Inside function: global_counter = {global_counter}")


def modify_global_correct() -> None:
    """
    Use 'global' keyword to modify global variables.
    
    Note:
        This is the correct way to modify global variables.
    """
    global global_counter  # ← Declare we're using the global variable
    
    # ✅ Now this modifies the global variable
    global_counter += 1
    print(f"   Inside function: global_counter = {global_counter}")


def modify_global_mutable() -> None:
    """
    Mutable global objects can be modified without 'global' keyword.
    
    Note:
        You can modify the CONTENTS of mutable objects (list, dict)
        without 'global' keyword, but you need 'global' to reassign.
    """
    # ✅ Can modify contents without 'global'
    global_list.append("item")
    
    # ❌ But reassignment needs 'global'
    # global_list = []  # This would create a local variable!


def reassign_global_mutable() -> None:
    """
    Reassigning a global variable requires 'global' keyword.
    """
    global global_list  # ← Need 'global' to reassign
    
    # ✅ Now can reassign
    global_list = ["new", "list"]


def multiple_globals() -> str:
    """
    Can declare multiple global variables.
    
    Returns:
        A formatted string
    """
    global global_counter, global_list  # ← Multiple globals
    
    global_counter += 1
    global_list.append(f"count_{global_counter}")
    
    return f"Counter: {global_counter}, List: {global_list}"


def global_vs_local() -> tuple[int, int]:
    """
    Demonstrates the difference between global and local variables.
    
    Returns:
        Tuple of (local_value, global_value)
    """
    # Local variable with same name as global
    global_counter = 999  # ← This is LOCAL (shadows global)
    
    # Read the actual global
    global GLOBAL_CONSTANT
    actual_global = GLOBAL_CONSTANT
    
    return global_counter, actual_global


# ============================================================================
# PRACTICAL EXAMPLES
# ============================================================================

# Configuration (global)
config = {
    "debug": False,
    "max_retries": 3,
    "timeout": 30
}


def get_config(key: str) -> Optional[int]:
    """
    Read from global configuration.

    Args:
        key: Configuration key

    Returns:
        Configuration value or None
    """
    # ← Can read global dict without 'global' keyword
    return config.get(key)


def update_config(key: str, value: int) -> None:
    """
    Update global configuration.

    Args:
        key: Configuration key
        value: New value
    """
    # ← Can modify dict contents without 'global'
    config[key] = value


# Application state (global)
app_state = {
    "requests_count": 0,
    "errors_count": 0
}


def increment_requests() -> None:
    """Increment request counter."""
    # ← Modifying dict contents (no 'global' needed)
    app_state["requests_count"] += 1


def increment_errors() -> None:
    """Increment error counter."""
    app_state["errors_count"] += 1


def get_stats() -> dict[str, int]:
    """Get application statistics."""
    return app_state.copy()


# ============================================================================
# DEMONSTRATION: Global scope
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("GLOBAL SCOPE - EXAMPLES")
    print("=" * 60)

    # ========================================================================
    # 1. READING GLOBAL VARIABLES
    # ========================================================================
    print("\n1. READING GLOBAL VARIABLES:")

    print(f"   GLOBAL_CONSTANT = {GLOBAL_CONSTANT}")
    result = read_global()
    print(f"   read_global() = {result}")
    print("   ← Functions can read globals without special syntax")

    # ========================================================================
    # 2. WRONG WAY TO MODIFY GLOBAL
    # ========================================================================
    print("\n2. WRONG WAY TO MODIFY GLOBAL:")

    print(f"   Before: global_counter = {global_counter}")
    try_modify_global_wrong()
    print(f"   After: global_counter = {global_counter}")
    print("   ← Global not modified! Function created a local variable instead")

    # ========================================================================
    # 3. CORRECT WAY TO MODIFY GLOBAL
    # ========================================================================
    print("\n3. CORRECT WAY TO MODIFY GLOBAL:")

    print(f"   Before: global_counter = {global_counter}")
    modify_global_correct()
    print(f"   After: global_counter = {global_counter}")
    print("   ← Global modified correctly using 'global' keyword")

    # ========================================================================
    # 4. MODIFYING MUTABLE GLOBALS
    # ========================================================================
    print("\n4. MODIFYING MUTABLE GLOBALS:")

    print(f"   Before: global_list = {global_list}")
    modify_global_mutable()
    print(f"   After: global_list = {global_list}")
    print("   ← Can modify list contents without 'global' keyword")

    # ========================================================================
    # 5. REASSIGNING MUTABLE GLOBALS
    # ========================================================================
    print("\n5. REASSIGNING MUTABLE GLOBALS:")

    print(f"   Before: global_list = {global_list}")
    reassign_global_mutable()
    print(f"   After: global_list = {global_list}")
    print("   ← Reassignment requires 'global' keyword")

    # ========================================================================
    # 6. MULTIPLE GLOBALS
    # ========================================================================
    print("\n6. MULTIPLE GLOBALS:")

    result = multiple_globals()
    print(f"   multiple_globals() = '{result}'")

    # ========================================================================
    # 7. GLOBAL VS LOCAL (SHADOWING)
    # ========================================================================
    print("\n7. GLOBAL VS LOCAL (SHADOWING):")

    print(f"   Before: global_counter = {global_counter}")
    local_val, global_val = global_vs_local()
    print(f"   Inside function: local global_counter = {local_val}")
    print(f"   Inside function: GLOBAL_CONSTANT = {global_val}")
    print(f"   After: global_counter = {global_counter} (unchanged)")
    print("   ← Local variable 'shadows' global (doesn't modify it)")

    # ========================================================================
    # 8. PRACTICAL: CONFIGURATION
    # ========================================================================
    print("\n8. PRACTICAL: CONFIGURATION:")

    debug = get_config("debug")
    max_retries = get_config("max_retries")
    print(f"   debug = {debug}")
    print(f"   max_retries = {max_retries}")

    update_config("max_retries", 5)
    print(f"   After update: max_retries = {get_config('max_retries')}")

    # ========================================================================
    # 9. PRACTICAL: APPLICATION STATE
    # ========================================================================
    print("\n9. PRACTICAL: APPLICATION STATE:")

    increment_requests()
    increment_requests()
    increment_requests()
    increment_errors()

    stats = get_stats()
    print(f"   Application stats: {stats}")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Global variables are defined at module level")
    print("2. Can READ globals from anywhere (no special syntax)")
    print("3. Need 'global' keyword to MODIFY/REASSIGN globals")
    print("4. Can modify CONTENTS of mutable globals without 'global'")
    print("5. But REASSIGNING mutable globals needs 'global'")
    print("6. Local variables can 'shadow' globals (same name)")
    print("7. Use UPPERCASE for global constants (convention)")
    print("8. Minimize use of global variables (prefer parameters)")
    print("=" * 60)

