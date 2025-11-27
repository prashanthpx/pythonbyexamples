"""
Example: List and Optional Type Hints - Beginner's Guide
Answers common questions about List and Optional type hints.

Common Questions:
1. Do I need to use List keyword or can I just use []?
2. What's the difference between List[str] and list[str]?
3. What does Optional[List[str]] mean?
4. When and why should I use these?

Key Concepts:
- Type hints are optional annotations (not enforced at runtime)
- List (from typing) vs list (built-in)
- Optional[T] means "T or None"
- Type hints help IDEs, linters, and documentation
"""

from typing import List, Optional


# ============================================================================
# QUESTION 1: Do I need List keyword or can I just use []?
# ============================================================================

# ❌ WRONG: Cannot use [] in type hints
# def process_items(items: []) -> None:  # SyntaxError!
#     pass

# ✅ CORRECT: Use list or List
def process_items_v1(items: list) -> None:
    """
    Accept a list (any list, no element type specified).
    
    Args:
        items: A list of any type
    """
    for item in items:
        print(item)


def process_items_v2(items: List[str]) -> None:
    """
    Accept a list of strings.
    
    Args:
        items: A list of strings
    """
    for item in items:
        print(item.upper())  # ← IDE knows item is str


# ============================================================================
# QUESTION 2: List (from typing) vs list (built-in)
# ============================================================================

# Python 3.9+ : Use built-in list with []
def modern_way(items: list[str]) -> list[int]:
    """
    Modern way (Python 3.9+): Use built-in list.
    
    Args:
        items: List of strings
        
    Returns:
        List of integers (lengths)
    """
    return [len(item) for item in items]


# Python 3.8 and earlier: Use List from typing
def old_way(items: List[str]) -> List[int]:
    """
    Old way (Python 3.8 and earlier): Use List from typing.
    
    Args:
        items: List of strings
        
    Returns:
        List of integers (lengths)
    """
    return [len(item) for item in items]


# ============================================================================
# QUESTION 3: What does Optional[List[str]] mean?
# ============================================================================

def process_names(names: Optional[List[str]]) -> int:
    """
    Optional[List[str]] means: "a list of strings OR None"
    
    Args:
        names: Either a list of strings, or None
        
    Returns:
        Number of names (0 if None)
    """
    if names is None:  # ← Must check for None!
        return 0
    
    return len(names)  # ← Now we know it's a list


# Without Optional (names cannot be None)
def process_names_required(names: List[str]) -> int:
    """
    List[str] means: "a list of strings" (cannot be None)
    
    Args:
        names: A list of strings (required, not None)
        
    Returns:
        Number of names
    """
    # No need to check for None
    return len(names)


# ============================================================================
# QUESTION 4: When and why to use these?
# ============================================================================

def example_no_type_hints(items):
    """
    Without type hints: IDE doesn't know what 'items' is.
    """
    # IDE cannot help with autocomplete
    # No warning if you pass wrong type
    for item in items:
        print(item)


def example_with_type_hints(items: List[str]) -> None:
    """
    With type hints: IDE knows 'items' is a list of strings.
    
    Args:
        items: List of strings
    """
    # IDE provides autocomplete for string methods
    # IDE warns if you pass wrong type
    for item in items:
        print(item.upper())  # ← IDE knows .upper() exists


# ============================================================================
# REAL-WORLD EXAMPLES
# ============================================================================

def get_user_emails(user_ids: List[int]) -> List[str]:
    """
    Get emails for given user IDs.
    
    Args:
        user_ids: List of user IDs
        
    Returns:
        List of email addresses
    """
    # Simulate database lookup
    emails = []
    for user_id in user_ids:
        emails.append(f"user{user_id}@example.com")
    return emails


def find_user_by_email(email: str, users: List[dict]) -> Optional[dict]:
    """
    Find user by email.
    
    Args:
        email: Email to search for
        users: List of user dictionaries
        
    Returns:
        User dict if found, None otherwise
    """
    for user in users:
        if user.get("email") == email:
            return user  # ← Found
    return None  # ← Not found


def process_optional_list(items: Optional[List[str]] = None) -> List[str]:
    """
    Process optional list parameter.
    
    Args:
        items: Optional list of strings (defaults to None)
        
    Returns:
        Processed list (empty if None was passed)
    """
    if items is None:
        items = []  # ← Use empty list if None
    
    # Now process the list
    return [item.upper() for item in items]


# ============================================================================
# COMMON PATTERNS
# ============================================================================

def pattern_1_optional_with_default(
    items: Optional[List[str]] = None
) -> None:
    """
    Pattern 1: Optional parameter with None default.

    This is the most common pattern for optional list parameters.
    """
    if items is None:
        items = []

    for item in items:
        print(item)


def pattern_2_required_list(items: List[str]) -> None:
    """
    Pattern 2: Required list parameter.

    Caller MUST provide a list (cannot pass None).
    """
    # No None check needed
    for item in items:
        print(item)


def pattern_3_optional_return(
    search_term: str,
    items: List[str]
) -> Optional[str]:
    """
    Pattern 3: Optional return value.

    Returns:
        First matching item, or None if not found
    """
    for item in items:
        if search_term in item:
            return item
    return None


def pattern_4_nested_optional(
    data: Optional[List[Optional[str]]] = None
) -> List[str]:
    """
    Pattern 4: Nested optional (list of optional strings).

    Args:
        data: Optional list that may contain None values

    Returns:
        List with None values filtered out
    """
    if data is None:
        return []

    # Filter out None values
    return [item for item in data if item is not None]


# ============================================================================
# COMPARISON: With vs Without Type Hints
# ============================================================================

def without_hints(items, callback):
    """Without type hints - unclear what types are expected."""
    result = []
    for item in items:
        result.append(callback(item))
    return result


def with_hints(
    items: List[str],
    callback: callable
) -> List[int]:
    """
    With type hints - clear what types are expected.

    Args:
        items: List of strings to process
        callback: Function to apply to each item

    Returns:
        List of integers
    """
    result = []
    for item in items:
        result.append(callback(item))
    return result


# ============================================================================
# DEMONSTRATION: List and Optional Basics
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("LIST AND OPTIONAL TYPE HINTS - BEGINNER'S GUIDE")
    print("=" * 70)

    # ========================================================================
    # QUESTION 1: List keyword vs []
    # ========================================================================
    print("\n" + "=" * 70)
    print("QUESTION 1: Do I need List keyword or can I use []?")
    print("=" * 70)

    print("\n❌ WRONG: Cannot use [] in type hints")
    print("   def process(items: []) -> None:  # SyntaxError!")

    print("\n✅ CORRECT: Use 'list' or 'List'")
    print("   def process(items: list) -> None:")
    print("   def process(items: List[str]) -> None:")

    items = ["apple", "banana", "cherry"]
    print(f"\nExample: {items}")
    process_items_v1(items)

    # ========================================================================
    # QUESTION 2: List vs list
    # ========================================================================
    print("\n" + "=" * 70)
    print("QUESTION 2: List (typing) vs list (built-in)?")
    print("=" * 70)

    print("\nPython 3.9+:")
    print("   ✅ Use: list[str]  (built-in)")
    print("   ⚠️  Old: List[str]  (from typing)")

    print("\nPython 3.8 and earlier:")
    print("   ❌ Error: list[str]  (not supported)")
    print("   ✅ Use: List[str]  (from typing)")

    words = ["hello", "world", "python"]
    print(f"\nExample: {words}")
    print(f"Lengths: {modern_way(words)}")

    # ========================================================================
    # QUESTION 3: Optional[List[str]]
    # ========================================================================
    print("\n" + "=" * 70)
    print("QUESTION 3: What does Optional[List[str]] mean?")
    print("=" * 70)

    print("\nOptional[List[str]] means:")
    print("   - Either a list of strings")
    print("   - OR None")

    print("\nExample 1: Pass a list")
    names1 = ["Alice", "Bob", "Charlie"]
    print(f"   Names: {names1}")
    print(f"   Count: {process_names(names1)}")

    print("\nExample 2: Pass None")
    names2 = None
    print(f"   Names: {names2}")
    print(f"   Count: {process_names(names2)}")

    print("\nWithout Optional (cannot pass None):")
    print("   def process(names: List[str]) -> int:")
    print("   process(None)  # ← Type error!")

    # ========================================================================
    # QUESTION 4: When and why?
    # ========================================================================
    print("\n" + "=" * 70)
    print("QUESTION 4: When and why use type hints?")
    print("=" * 70)

    print("\nBenefits:")
    print("   1. IDE autocomplete and suggestions")
    print("   2. Catch errors before running code")
    print("   3. Better documentation")
    print("   4. Easier to understand code")

    print("\nExample: IDE knows item is str")
    print("   def process(items: List[str]):")
    print("       for item in items:")
    print("           item.upper()  ← IDE suggests .upper()")

    # ========================================================================
    # REAL-WORLD EXAMPLES
    # ========================================================================
    print("\n" + "=" * 70)
    print("REAL-WORLD EXAMPLES:")
    print("=" * 70)

    print("\nExample 1: Get user emails")
    user_ids = [1, 2, 3]
    emails = get_user_emails(user_ids)
    print(f"   User IDs: {user_ids}")
    print(f"   Emails: {emails}")

    print("\nExample 2: Find user by email")
    users = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"}
    ]
    found = find_user_by_email("alice@example.com", users)
    print(f"   Found: {found}")

    not_found = find_user_by_email("charlie@example.com", users)
    print(f"   Not found: {not_found}")

    print("\nExample 3: Process optional list")
    result1 = process_optional_list(["hello", "world"])
    print(f"   With list: {result1}")

    result2 = process_optional_list(None)
    print(f"   With None: {result2}")

    result3 = process_optional_list()  # Uses default None
    print(f"   With default: {result3}")

    # ========================================================================
    # COMMON PATTERNS
    # ========================================================================
    print("\n" + "=" * 70)
    print("COMMON PATTERNS:")
    print("=" * 70)

    print("\nPattern 1: Optional with default")
    print("   def func(items: Optional[List[str]] = None):")
    print("       if items is None:")
    print("           items = []")

    print("\nPattern 2: Required list")
    print("   def func(items: List[str]):")
    print("       # No None check needed")

    print("\nPattern 3: Optional return")
    print("   def find(term: str) -> Optional[str]:")
    print("       return item if found else None")

    print("\nPattern 4: Nested optional")
    data = ["hello", None, "world", None, "python"]
    filtered = pattern_4_nested_optional(data)
    print(f"   Input: {data}")
    print(f"   Filtered: {filtered}")

    print("\n" + "=" * 70)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Cannot use [] in type hints - use list or List")
    print("2. Python 3.9+: Use list[str] (built-in)")
    print("3. Python 3.8-: Use List[str] (from typing)")
    print("4. Optional[T] means 'T or None'")
    print("5. Optional[List[str]] means 'list of strings or None'")
    print("6. Type hints are optional but very helpful")
    print("7. IDEs use type hints for autocomplete")
    print("8. Always check for None with Optional parameters")
    print("9. Use Optional for parameters that can be None")
    print("10. Type hints don't affect runtime behavior")
    print("=" * 70)

