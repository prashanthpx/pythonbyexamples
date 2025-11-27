"""
Example: Return Values
Demonstrates different types of return values in Python functions.

Key Concepts:
- Single return values
- Multiple return values (tuples)
- Early returns
- Conditional returns
- Returning different types
- No return (None)
"""

from typing import Optional


def get_square(number: int) -> int:
    """
    Return the square of a number.
    
    Args:
        number: Number to square
        
    Returns:
        Square of the number
        
    Note:
        Simple single value return
    """
    return number * number


def get_rectangle_properties(length: float, width: float) -> tuple[float, float, float]:
    """
    Calculate area and perimeter of a rectangle.
    
    Args:
        length: Rectangle length
        width: Rectangle width
        
    Returns:
        Tuple of (area, perimeter, diagonal)
        
    Key Takeaway:
        Functions can return multiple values as a tuple.
        Python automatically packs multiple values into a tuple.
    """
    area = length * width
    perimeter = 2 * (length + width)
    diagonal = (length**2 + width**2) ** 0.5
    
    # ← Important: Returning multiple values (automatically creates a tuple)
    return area, perimeter, diagonal


def divide_safely(a: float, b: float) -> Optional[float]:
    """
    Divide two numbers, return None if division by zero.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        Result of division, or None if b is zero
        
    Important:
        Using | None (Union type) indicates function might return None.
        This is called an Optional return type.
    """
    if b == 0:
        # ← Early return: Exit function immediately if condition met
        return None
    return a / b


def get_grade(score: int) -> str:
    """
    Convert numeric score to letter grade.
    
    Args:
        score: Numeric score (0-100)
        
    Returns:
        Letter grade (A, B, C, D, F)
        
    Nuance:
        Multiple return statements based on conditions.
        Only one return executes per function call.
    """
    if score >= 90:
        return "A"  # ← Exits immediately, rest of function doesn't run
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def find_max_min(numbers: list[int]) -> Optional[tuple[int, int]]:
    """
    Find maximum and minimum in a list.
    
    Args:
        numbers: List of integers
        
    Returns:
        Tuple of (max, min) or None if list is empty
        
    Important:
        Demonstrates returning None for invalid input.
        Also shows tuple unpacking in return.
    """
    if not numbers:  # Empty list check
        return None
    
    return max(numbers), min(numbers)


def process_data(data: str) -> str:
    """
    Process data and return result.
    
    Args:
        data: Input data string
        
    Returns:
        Processed data
        
    Note:
        Shows explicit return at end of function.
    """
    result = data.upper().strip()
    return result  # ← Explicit return statement


def log_message(message: str) -> None:
    """
    Log a message (no return value).
    
    Args:
        message: Message to log
        
    Returns:
        None
        
    Important:
        Functions that don't return a value implicitly return None.
        -> None annotation makes this explicit.
    """
    print(f"[LOG] {message}")
    # ← No return statement = implicit return None


# ============================================================================
# DEMONSTRATION: Different return value patterns
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("RETURN VALUES - EXAMPLES")
    print("=" * 60)
    
    # ========================================================================
    # 1. SINGLE RETURN VALUE
    # ========================================================================
    print("\n1. SINGLE RETURN VALUE:")
    
    square = get_square(5)
    print(f"   Square of 5 = {square}")
    print(f"   Type: {type(square)}")
    
    # ========================================================================
    # 2. MULTIPLE RETURN VALUES (TUPLE)
    # ========================================================================
    print("\n2. MULTIPLE RETURN VALUES:")
    
    # Unpack all values
    area, perimeter, diagonal = get_rectangle_properties(5.0, 3.0)
    print(f"   Rectangle 5.0 x 3.0:")
    print(f"   - Area: {area}")
    print(f"   - Perimeter: {perimeter}")
    print(f"   - Diagonal: {diagonal:.2f}")
    
    # ← Important: Tuple unpacking - assign multiple values at once
    
    # Get as tuple without unpacking
    result = get_rectangle_properties(4.0, 6.0)
    print(f"\n   As tuple: {result}")
    print(f"   Type: {type(result)}")

    # ========================================================================
    # 3. OPTIONAL RETURN (None for errors)
    # ========================================================================
    print("\n3. OPTIONAL RETURN (None for errors):")

    valid_result = divide_safely(10, 2)
    print(f"   10 / 2 = {valid_result}")

    invalid_result = divide_safely(10, 0)
    print(f"   10 / 0 = {invalid_result}")

    # ← Important: Check for None before using result
    if invalid_result is None:
        print("   Division by zero detected!")

    # ========================================================================
    # 4. CONDITIONAL RETURNS
    # ========================================================================
    print("\n4. CONDITIONAL RETURNS:")

    print(f"   Score 95 -> Grade: {get_grade(95)}")
    print(f"   Score 85 -> Grade: {get_grade(85)}")
    print(f"   Score 75 -> Grade: {get_grade(75)}")
    print(f"   Score 65 -> Grade: {get_grade(65)}")
    print(f"   Score 55 -> Grade: {get_grade(55)}")

    # ← Only one return statement executes per call

    # ========================================================================
    # 5. RETURNING NONE FOR INVALID INPUT
    # ========================================================================
    print("\n5. RETURNING None FOR INVALID INPUT:")

    numbers = [3, 7, 1, 9, 4]
    max_min = find_max_min(numbers)
    if max_min:
        maximum, minimum = max_min
        print(f"   List: {numbers}")
        print(f"   Max: {maximum}, Min: {minimum}")

    empty_result = find_max_min([])
    print(f"   Empty list result: {empty_result}")

    # ========================================================================
    # 6. EXPLICIT RETURN
    # ========================================================================
    print("\n6. EXPLICIT RETURN:")

    processed = process_data("  hello world  ")
    print(f"   Original: '  hello world  '")
    print(f"   Processed: '{processed}'")

    # ========================================================================
    # 7. NO RETURN VALUE (None)
    # ========================================================================
    print("\n7. NO RETURN VALUE (None):")

    return_value = log_message("System started")
    print(f"   Return value: {return_value}")
    print(f"   Type: {type(return_value)}")

    # ← Functions without return automatically return None

    # ========================================================================
    # 8. USING RETURN VALUES IN EXPRESSIONS
    # ========================================================================
    print("\n8. USING RETURN VALUES IN EXPRESSIONS:")

    # Use return value directly in calculation
    total = get_square(3) + get_square(4)
    print(f"   3² + 4² = {total}")

    # Use in conditional
    if get_square(5) > 20:
        print(f"   5² is greater than 20")

    # Chain function calls
    result = get_square(get_square(2))
    print(f"   Square of square of 2 = {result}")

    print("\n" + "=" * 60)

