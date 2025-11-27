"""
Example: Keyword Arguments
Demonstrates how keyword arguments work in Python functions.

Key Concepts:
- Arguments matched by name (order doesn't matter)
- Improved code readability
- Mixing positional and keyword arguments
- Keyword-only parameters
"""

from typing import Union


def create_profile(name: str, age: int, city: str, country: str) -> dict[str, Union[str, int]]:
    """
    Create a user profile.
    
    Args:
        name: User's name
        age: User's age
        city: User's city
        country: User's country
        
    Returns:
        Profile dictionary
        
    Note:
        Can be called with positional or keyword arguments.
    """
    return {
        "name": name,
        "age": age,
        "city": city,
        "country": country
    }


def send_email(to: str, subject: str, body: str, cc: str = "", bcc: str = "") -> str:
    """
    Send an email message.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body
        cc: CC recipients (optional)
        bcc: BCC recipients (optional)
        
    Returns:
        Status message
        
    Important:
        Using keyword arguments makes it clear what each value represents.
    """
    message = f"To: {to}\nSubject: {subject}\n"
    if cc:
        message += f"CC: {cc}\n"
    if bcc:
        message += f"BCC: {bcc}\n"
    message += f"\n{body}"
    
    return f"Email sent!\n{message}"


def configure_server(
    host: str,
    port: int,
    ssl: bool = True,
    timeout: int = 30,
    retries: int = 3
) -> dict[str, Union[str, int, bool]]:
    """
    Configure server connection.
    
    Args:
        host: Server hostname
        port: Server port
        ssl: Use SSL connection (default: True)
        timeout: Connection timeout in seconds (default: 30)
        retries: Number of retry attempts (default: 3)
        
    Returns:
        Configuration dictionary
        
    Note:
        Keyword arguments make it easy to override specific defaults.
    """
    return {
        "host": host,
        "port": port,
        "ssl": ssl,
        "timeout": timeout,
        "retries": retries
    }


def keyword_only_params(*, name: str, age: int, email: str) -> str:
    """
    Function with keyword-only parameters.
    
    Args:
        *: Marker indicating all following parameters are keyword-only
        name: Person's name (keyword-only)
        age: Person's age (keyword-only)
        email: Person's email (keyword-only)
        
    Returns:
        Formatted string
        
    Important:
        The '*' marker means ALL parameters after it MUST be passed as keywords.
        Cannot use positional arguments at all.
    """
    return f"{name} ({age}) - {email}"


def mixed_keyword_only(required: str, optional: str = "default", *, kw_only: str) -> str:
    """
    Mix of regular and keyword-only parameters.
    
    Args:
        required: Required parameter (can be positional or keyword)
        optional: Optional parameter with default (can be positional or keyword)
        *: Keyword-only marker
        kw_only: Keyword-only parameter (must be keyword)
        
    Returns:
        Formatted string
        
    Note:
        Parameters before '*' can be positional or keyword.
        Parameters after '*' must be keyword.
    """
    return f"required={required}, optional={optional}, kw_only={kw_only}"


# ============================================================================
# DEMONSTRATION: Keyword arguments
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("KEYWORD ARGUMENTS - EXAMPLES")
    print("=" * 60)
    
    # ========================================================================
    # 1. BASIC KEYWORD ARGUMENTS
    # ========================================================================
    print("\n1. BASIC KEYWORD ARGUMENTS:")
    
    # Order doesn't matter with keyword arguments
    profile1 = create_profile(name="Alice", age=30, city="Seattle", country="USA")
    print(f"   create_profile(name='Alice', age=30, city='Seattle', country='USA'):")
    print(f"   {profile1}")
    
    # Different order, same result
    profile2 = create_profile(country="USA", city="Seattle", age=30, name="Alice")
    print(f"\n   create_profile(country='USA', city='Seattle', age=30, name='Alice'):")
    print(f"   {profile2}")
    
    print("\n   ✓ Both calls produce the same result - order doesn't matter!")

    # ← Important: Keyword arguments are matched by NAME, not position

    # ========================================================================
    # 2. KEYWORD ARGUMENTS FOR CLARITY
    # ========================================================================
    print("\n2. KEYWORD ARGUMENTS FOR CLARITY:")

    # Without keywords - hard to understand
    email1 = send_email("bob@example.com", "Meeting", "See you at 3pm")
    print("   Without keywords (less clear):")
    print("   send_email('bob@example.com', 'Meeting', 'See you at 3pm')")

    # With keywords - much clearer
    email2 = send_email(
        to="bob@example.com",
        subject="Meeting",
        body="See you at 3pm"
    )
    print("\n   With keywords (very clear):")
    print("   send_email(to='bob@example.com', subject='Meeting', body='See you at 3pm')")

    # ← Keyword arguments make code self-documenting

    # ========================================================================
    # 3. SELECTIVE OVERRIDE OF DEFAULTS
    # ========================================================================
    print("\n3. SELECTIVE OVERRIDE OF DEFAULTS:")

    # Use all defaults
    config1 = configure_server(host="api.example.com", port=443)
    print(f"   configure_server(host='api.example.com', port=443):")
    print(f"   {config1}")

    # Override specific defaults
    config2 = configure_server(
        host="api.example.com",
        port=443,
        timeout=60,  # Override only timeout
        ssl=False    # Override only ssl
    )
    print(f"\n   configure_server(host='...', port=443, timeout=60, ssl=False):")
    print(f"   {config2}")

    # ← Can override any combination of defaults

    # ========================================================================
    # 4. KEYWORD-ONLY PARAMETERS (*)
    # ========================================================================
    print("\n4. KEYWORD-ONLY PARAMETERS (*):")

    # Correct: all keyword arguments
    result = keyword_only_params(name="Charlie", age=35, email="charlie@example.com")
    print(f"   keyword_only_params(name='Charlie', age=35, email='charlie@example.com'):")
    print(f"   Result: '{result}'")

    # ❌ Error: cannot use positional arguments
    # keyword_only_params("Charlie", 35, "charlie@example.com")  # TypeError
    print("\n   ⚠️  Cannot use positional: keyword_only_params('Charlie', 35, '...')")

    # ← The '*' marker enforces keyword-only

    # ========================================================================
    # 5. MIXING POSITIONAL AND KEYWORD
    # ========================================================================
    print("\n5. MIXING POSITIONAL AND KEYWORD:")

    # Positional for required, keyword for kw_only
    result1 = mixed_keyword_only("value1", kw_only="kw_value")
    print(f"   mixed_keyword_only('value1', kw_only='kw_value'):")
    print(f"   Result: '{result1}'")

    # All keyword arguments
    result2 = mixed_keyword_only(required="value1", optional="value2", kw_only="kw_value")
    print(f"\n   mixed_keyword_only(required='value1', optional='value2', kw_only='kw_value'):")
    print(f"   Result: '{result2}'")

    # Positional for both regular params, keyword for kw_only
    result3 = mixed_keyword_only("value1", "value2", kw_only="kw_value")
    print(f"\n   mixed_keyword_only('value1', 'value2', kw_only='kw_value'):")
    print(f"   Result: '{result3}'")

    # ← Parameters before '*' can be positional or keyword
    # ← Parameters after '*' MUST be keyword

    # ========================================================================
    # 6. BENEFITS OF KEYWORD ARGUMENTS
    # ========================================================================
    print("\n6. BENEFITS OF KEYWORD ARGUMENTS:")
    print("   ✓ Order doesn't matter - more flexible")
    print("   ✓ Self-documenting - clear what each value means")
    print("   ✓ Easy to skip optional parameters")
    print("   ✓ Easy to override specific defaults")
    print("   ✓ Reduces errors from wrong argument order")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Keyword arguments are matched by NAME, not position")
    print("2. Order doesn't matter with keyword arguments")
    print("3. Makes code more readable and self-documenting")
    print("4. Easy to override specific defaults")
    print("5. '*' marker makes parameters keyword-only")
    print("6. Keyword-only params MUST be passed as keywords")
    print("7. Mix positional and keyword (positional first)")
    print("=" * 60)

