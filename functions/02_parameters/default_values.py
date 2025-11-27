"""
Example: Default Parameter Values
Demonstrates how to use default values for function parameters.

Key Concepts:
- Parameters with default values
- Optional parameters
- Mutable default arguments (DANGER!)
- Best practices for defaults
"""

from typing import Optional, Union


def greet(name: str, greeting: str = "Hello") -> str:
    """
    Greet a person with a customizable greeting.
    
    Args:
        name: Person's name (required)
        greeting: Greeting word (optional, default: "Hello")
        
    Returns:
        Greeting message
        
    Note:
        Parameters with defaults can be omitted when calling.
    """
    return f"{greeting}, {name}!"


def create_user(
    username: str,
    email: str,
    role: str = "user",
    active: bool = True,
    notifications: bool = True
) -> dict[str, Union[str, bool]]:
    """
    Create a user with default settings.
    
    Args:
        username: User's username (required)
        email: User's email (required)
        role: User role (default: "user")
        active: Account active status (default: True)
        notifications: Enable notifications (default: True)
        
    Returns:
        User configuration dictionary
        
    Important:
        Required parameters come first, then optional with defaults.
    """
    return {
        "username": username,
        "email": email,
        "role": role,
        "active": active,
        "notifications": notifications
    }


def connect_database(
    host: str,
    port: int = 5432,
    database: str = "mydb",
    username: str = "admin",
    password: Optional[str] = None,
    timeout: int = 30
) -> str:
    """
    Connect to a database with sensible defaults.
    
    Args:
        host: Database host (required)
        port: Database port (default: 5432 for PostgreSQL)
        database: Database name (default: "mydb")
        username: Username (default: "admin")
        password: Password (default: None)
        timeout: Connection timeout (default: 30)
        
    Returns:
        Connection string
        
    Note:
        Only host is required, everything else has defaults.
    """
    conn_str = f"postgresql://{username}"
    if password:
        conn_str += f":{password}"
    conn_str += f"@{host}:{port}/{database}?timeout={timeout}"
    
    return conn_str


def append_to_list_wrong(item: str, items: list[str] = []) -> list[str]:
    """
    WRONG: Mutable default argument (list).
    
    Args:
        item: Item to append
        items: List to append to (default: [])
        
    Returns:
        List with item appended
        
    WARNING:
        This is a common Python pitfall!
        The default list is created ONCE when function is defined,
        not each time function is called.
        This causes unexpected behavior!
    """
    items.append(item)
    return items


def append_to_list_correct(item: str, items: Optional[list[str]] = None) -> list[str]:
    """
    CORRECT: Proper handling of mutable default.
    
    Args:
        item: Item to append
        items: List to append to (default: None, creates new list)
        
    Returns:
        List with item appended
        
    Best Practice:
        Use None as default, then create new mutable object inside function.
    """
    if items is None:
        items = []  # ← Create new list each time
    
    items.append(item)
    return items


def configure_logger(
    name: str,
    level: str = "INFO",
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers: Optional[list[str]] = None
) -> dict[str, Union[str, list[str]]]:
    """
    Configure a logger with defaults.
    
    Args:
        name: Logger name (required)
        level: Log level (default: "INFO")
        format: Log format string (default: standard format)
        handlers: List of handlers (default: None, uses console)
        
    Returns:
        Logger configuration
        
    Note:
        Complex default values (like format strings) are fine for immutable types.
    """
    if handlers is None:
        handlers = ["console"]  # ← Create new list each time
    
    return {
        "name": name,
        "level": level,
        "format": format,
        "handlers": handlers
    }


# ============================================================================
# DEMONSTRATION: Default parameter values
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DEFAULT PARAMETER VALUES - EXAMPLES")
    print("=" * 60)
    
    # ========================================================================
    # 1. BASIC DEFAULT VALUES
    # ========================================================================
    print("\n1. BASIC DEFAULT VALUES:")
    
    # Use default greeting
    msg1 = greet("Alice")
    print(f"   greet('Alice') = '{msg1}'")
    print("   (used default greeting='Hello')")
    
    # Override default
    msg2 = greet("Bob", "Hi")
    print(f"\n   greet('Bob', 'Hi') = '{msg2}'")
    print("   (overrode default greeting)")
    
    # ← Parameters with defaults can be omitted or overridden

    # ========================================================================
    # 2. MULTIPLE DEFAULT VALUES
    # ========================================================================
    print("\n2. MULTIPLE DEFAULT VALUES:")

    # Use all defaults
    user1 = create_user("alice", "alice@example.com")
    print(f"   create_user('alice', 'alice@example.com'):")
    print(f"   {user1}")
    print("   (all optional params used defaults)")

    # Override some defaults
    user2 = create_user("bob", "bob@example.com", role="admin", notifications=False)
    print(f"\n   create_user('bob', 'bob@example.com', role='admin', notifications=False):")
    print(f"   {user2}")
    print("   (overrode role and notifications)")

    # ← Can override any combination of defaults

    # ========================================================================
    # 3. MANY DEFAULTS - ONLY REQUIRED PARAM
    # ========================================================================
    print("\n3. MANY DEFAULTS - ONLY REQUIRED PARAM:")

    # Minimal call - only required parameter
    conn1 = connect_database("localhost")
    print(f"   connect_database('localhost'):")
    print(f"   {conn1}")

    # Override specific defaults
    conn2 = connect_database("db.example.com", port=3306, database="production")
    print(f"\n   connect_database('db.example.com', port=3306, database='production'):")
    print(f"   {conn2}")

    # ========================================================================
    # 4. MUTABLE DEFAULT ARGUMENTS - THE PITFALL!
    # ========================================================================
    print("\n4. MUTABLE DEFAULT ARGUMENTS - THE PITFALL!")
    print("   ⚠️  WARNING: This demonstrates a common mistake!")

    # First call
    list1 = append_to_list_wrong("apple")
    print(f"\n   First call: append_to_list_wrong('apple') = {list1}")

    # Second call - UNEXPECTED BEHAVIOR!
    list2 = append_to_list_wrong("banana")
    print(f"   Second call: append_to_list_wrong('banana') = {list2}")
    print("   ❌ WRONG! Expected ['banana'], got ['apple', 'banana']")

    # Third call - gets worse!
    list3 = append_to_list_wrong("cherry")
    print(f"   Third call: append_to_list_wrong('cherry') = {list3}")
    print("   ❌ WRONG! Expected ['cherry'], got ['apple', 'banana', 'cherry']")

    print("\n   ⚠️  The default list is shared across all calls!")
    print("   ⚠️  It's created ONCE when function is defined, not per call")

    # ← NEVER use mutable objects (list, dict, set) as defaults!

    # ========================================================================
    # 5. CORRECT WAY - USE None AS DEFAULT
    # ========================================================================
    print("\n5. CORRECT WAY - USE None AS DEFAULT:")

    # First call
    list1 = append_to_list_correct("apple")
    print(f"\n   First call: append_to_list_correct('apple') = {list1}")

    # Second call - CORRECT BEHAVIOR
    list2 = append_to_list_correct("banana")
    print(f"   Second call: append_to_list_correct('banana') = {list2}")
    print("   ✓ CORRECT! Got ['banana'] as expected")

    # Third call
    list3 = append_to_list_correct("cherry")
    print(f"   Third call: append_to_list_correct('cherry') = {list3}")
    print("   ✓ CORRECT! Got ['cherry'] as expected")

    print("\n   ✓ Each call gets a fresh list")

    # ← Use None as default, create mutable object inside function

    # ========================================================================
    # 6. COMPLEX DEFAULT VALUES
    # ========================================================================
    print("\n6. COMPLEX DEFAULT VALUES:")

    logger1 = configure_logger("myapp")
    print(f"   configure_logger('myapp'):")
    print(f"   Level: {logger1['level']}")
    print(f"   Handlers: {logger1['handlers']}")

    logger2 = configure_logger("webapp", level="DEBUG", handlers=["console", "file"])
    print(f"\n   configure_logger('webapp', level='DEBUG', handlers=['console', 'file']):")
    print(f"   Level: {logger2['level']}")
    print(f"   Handlers: {logger2['handlers']}")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Parameters with defaults are OPTIONAL")
    print("2. Required parameters must come BEFORE optional ones")
    print("3. Can override any combination of defaults")
    print("4. ❌ NEVER use mutable objects (list, dict) as defaults")
    print("5. ✓ Use None as default, create mutable inside function")
    print("6. Default values are evaluated ONCE at function definition")
    print("7. Immutable defaults (str, int, bool, None) are safe")
    print("=" * 60)

