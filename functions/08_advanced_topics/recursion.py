"""
Example: Recursion
Demonstrates recursive functions and patterns.

Key Concepts:
- Recursion: function calling itself
- Base case: condition to stop recursion
- Recursive case: function calls itself with modified input
- Call stack: each recursive call adds to stack
- Tail recursion: recursive call is last operation

Recursion vs Iteration:
- Recursion: elegant for tree/graph structures
- Iteration: more efficient (no stack overhead)
- Python: no tail call optimization
"""

from typing import List, Any, Optional
import sys


# ============================================================================
# BASIC RECURSION
# ============================================================================

def factorial(n: int) -> int:
    """
    Calculate factorial using recursion.
    
    Args:
        n: Non-negative integer
        
    Returns:
        n! = n * (n-1) * ... * 1
    """
    # Base case
    if n <= 1:
        return 1  # ← Stop recursion
    
    # Recursive case
    return n * factorial(n - 1)  # ← Call itself


def fibonacci(n: int) -> int:
    """
    Calculate nth Fibonacci number using recursion.
    
    Args:
        n: Position in sequence (0-indexed)
        
    Returns:
        nth Fibonacci number
    """
    # Base cases
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    # Recursive case
    return fibonacci(n - 1) + fibonacci(n - 2)  # ← Two recursive calls


def sum_list(numbers: List[int]) -> int:
    """
    Sum list using recursion.
    
    Args:
        numbers: List of integers
        
    Returns:
        Sum of all numbers
    """
    # Base case: empty list
    if not numbers:
        return 0
    
    # Recursive case: first + sum of rest
    return numbers[0] + sum_list(numbers[1:])  # ← Process head, recurse on tail


# ============================================================================
# RECURSION WITH LISTS
# ============================================================================

def reverse_list(items: List[Any]) -> List[Any]:
    """
    Reverse list using recursion.
    
    Args:
        items: List to reverse
        
    Returns:
        Reversed list
    """
    # Base case
    if len(items) <= 1:
        return items
    
    # Recursive case: last + reverse of rest
    return [items[-1]] + reverse_list(items[:-1])


def flatten(nested: List[Any]) -> List[Any]:
    """
    Flatten nested list using recursion.
    
    Args:
        nested: Nested list
        
    Returns:
        Flattened list
    """
    result = []
    
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))  # ← Recursive call
        else:
            result.append(item)
    
    return result


def max_in_list(numbers: List[int]) -> int:
    """
    Find maximum in list using recursion.
    
    Args:
        numbers: Non-empty list of integers
        
    Returns:
        Maximum value
    """
    # Base case: single element
    if len(numbers) == 1:
        return numbers[0]
    
    # Recursive case: max of first and max of rest
    rest_max = max_in_list(numbers[1:])
    return numbers[0] if numbers[0] > rest_max else rest_max


# ============================================================================
# RECURSION WITH STRINGS
# ============================================================================

def reverse_string(s: str) -> str:
    """
    Reverse string using recursion.
    
    Args:
        s: String to reverse
        
    Returns:
        Reversed string
    """
    # Base case
    if len(s) <= 1:
        return s
    
    # Recursive case: last + reverse of rest
    return s[-1] + reverse_string(s[:-1])


def is_palindrome(s: str) -> bool:
    """
    Check if string is palindrome using recursion.
    
    Args:
        s: String to check
        
    Returns:
        True if palindrome
    """
    # Base cases
    if len(s) <= 1:
        return True
    
    # Check first and last characters
    if s[0] != s[-1]:
        return False
    
    # Recursive case: check middle
    return is_palindrome(s[1:-1])


# ============================================================================
# TREE RECURSION
# ============================================================================

class TreeNode:
    """Simple tree node."""

    def __init__(self, value: Any, children: Optional[List['TreeNode']] = None):
        self.value = value
        self.children = children or []


def tree_sum(node: Optional[TreeNode]) -> int:
    """
    Sum all values in tree using recursion.

    Args:
        node: Root node

    Returns:
        Sum of all values
    """
    if node is None:
        return 0

    # Sum current node + all children
    total = node.value
    for child in node.children:
        total += tree_sum(child)  # ← Recursive call for each child

    return total


def tree_height(node: Optional[TreeNode]) -> int:
    """
    Calculate tree height using recursion.

    Args:
        node: Root node

    Returns:
        Height of tree
    """
    if node is None:
        return 0

    if not node.children:
        return 1

    # Height = 1 + max height of children
    return 1 + max(tree_height(child) for child in node.children)


def tree_contains(node: Optional[TreeNode], value: Any) -> bool:
    """
    Check if tree contains value using recursion.

    Args:
        node: Root node
        value: Value to search for

    Returns:
        True if value found
    """
    if node is None:
        return False

    if node.value == value:
        return True

    # Search in children
    return any(tree_contains(child, value) for child in node.children)


# ============================================================================
# BINARY SEARCH (RECURSIVE)
# ============================================================================

def binary_search(arr: List[int], target: int, left: int = 0, right: int = -1) -> int:
    """
    Binary search using recursion.

    Args:
        arr: Sorted list
        target: Value to find
        left: Left boundary
        right: Right boundary

    Returns:
        Index of target, or -1 if not found
    """
    if right == -1:
        right = len(arr) - 1

    # Base case: not found
    if left > right:
        return -1

    # Find middle
    mid = (left + right) // 2

    # Base case: found
    if arr[mid] == target:
        return mid

    # Recursive cases
    if arr[mid] > target:
        return binary_search(arr, target, left, mid - 1)  # ← Search left
    else:
        return binary_search(arr, target, mid + 1, right)  # ← Search right


# ============================================================================
# PERMUTATIONS AND COMBINATIONS
# ============================================================================

def permutations(items: List[Any]) -> List[List[Any]]:
    """
    Generate all permutations using recursion.

    Args:
        items: List of items

    Returns:
        List of all permutations
    """
    # Base case
    if len(items) <= 1:
        return [items]

    result = []

    # For each item, make it first and permute rest
    for i in range(len(items)):
        current = items[i]
        rest = items[:i] + items[i+1:]

        # Get permutations of rest
        for perm in permutations(rest):
            result.append([current] + perm)

    return result


def combinations(items: List[Any], k: int) -> List[List[Any]]:
    """
    Generate all k-combinations using recursion.

    Args:
        items: List of items
        k: Size of combinations

    Returns:
        List of all k-combinations
    """
    # Base cases
    if k == 0:
        return [[]]
    if len(items) < k:
        return []

    result = []

    # Include first item
    first = items[0]
    rest = items[1:]

    # Combinations with first item
    for combo in combinations(rest, k - 1):
        result.append([first] + combo)

    # Combinations without first item
    result.extend(combinations(rest, k))

    return result


# ============================================================================
# TAIL RECURSION (NOT OPTIMIZED IN PYTHON)
# ============================================================================

def factorial_tail(n: int, accumulator: int = 1) -> int:
    """
    Tail-recursive factorial.

    Note: Python doesn't optimize tail recursion.

    Args:
        n: Number
        accumulator: Accumulated result

    Returns:
        Factorial
    """
    if n <= 1:
        return accumulator

    return factorial_tail(n - 1, n * accumulator)  # ← Tail call


# ============================================================================
# RECURSION DEPTH LIMIT
# ============================================================================

def demonstrate_recursion_limit() -> None:
    """Demonstrate Python's recursion depth limit."""

    print(f"Default recursion limit: {sys.getrecursionlimit()}")

    def deep_recursion(n: int) -> int:
        if n <= 0:
            return 0
        return 1 + deep_recursion(n - 1)

    try:
        result = deep_recursion(10000)
        print(f"Result: {result}")
    except RecursionError as e:
        print(f"RecursionError: {e}")

    # Can increase limit (use with caution)
    # sys.setrecursionlimit(20000)


# ============================================================================
# DEMONSTRATION: Recursion
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("RECURSION")
    print("=" * 70)

    # ========================================================================
    # Basic Recursion
    # ========================================================================
    print("\n" + "=" * 70)
    print("1. BASIC RECURSION")
    print("=" * 70)

    print("\nFactorial:")
    for n in [0, 1, 5, 10]:
        print(f"  {n}! = {factorial(n)}")

    print("\nFibonacci:")
    for n in range(10):
        print(f"  fib({n}) = {fibonacci(n)}", end=" ")
    print()

    print("\nSum list:")
    numbers = [1, 2, 3, 4, 5]
    print(f"  {numbers} -> {sum_list(numbers)}")

    # ========================================================================
    # Recursion with Lists
    # ========================================================================
    print("\n" + "=" * 70)
    print("2. RECURSION WITH LISTS")
    print("=" * 70)

    print("\nReverse list:")
    items = [1, 2, 3, 4, 5]
    print(f"  {items} -> {reverse_list(items)}")

    print("\nFlatten nested list:")
    nested = [1, [2, 3, [4, 5]], 6, [7, [8, 9]]]
    print(f"  {nested}")
    print(f"  -> {flatten(nested)}")

    print("\nMax in list:")
    numbers = [3, 7, 2, 9, 1, 5]
    print(f"  {numbers} -> {max_in_list(numbers)}")

    # ========================================================================
    # Recursion with Strings
    # ========================================================================
    print("\n" + "=" * 70)
    print("3. RECURSION WITH STRINGS")
    print("=" * 70)

    print("\nReverse string:")
    s = "hello"
    print(f"  '{s}' -> '{reverse_string(s)}'")

    print("\nPalindrome check:")
    test_strings = ["racecar", "hello", "madam", "python"]
    for s in test_strings:
        result = is_palindrome(s)
        print(f"  '{s}': {result}")

    # ========================================================================
    # Tree Recursion
    # ========================================================================
    print("\n" + "=" * 70)
    print("4. TREE RECURSION")
    print("=" * 70)

    # Build tree
    tree = TreeNode(1, [
        TreeNode(2, [TreeNode(4), TreeNode(5)]),
        TreeNode(3, [TreeNode(6)])
    ])

    print("\nTree sum:")
    print(f"  Sum: {tree_sum(tree)}")

    print("\nTree height:")
    print(f"  Height: {tree_height(tree)}")

    print("\nTree contains:")
    for value in [1, 5, 7]:
        result = tree_contains(tree, value)
        print(f"  Contains {value}: {result}")

    # ========================================================================
    # Binary Search
    # ========================================================================
    print("\n" + "=" * 70)
    print("5. BINARY SEARCH (RECURSIVE)")
    print("=" * 70)

    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    print(f"\nArray: {arr}")

    for target in [7, 15, 20]:
        index = binary_search(arr, target)
        if index != -1:
            print(f"  Found {target} at index {index}")
        else:
            print(f"  {target} not found")

    # ========================================================================
    # Permutations and Combinations
    # ========================================================================
    print("\n" + "=" * 70)
    print("6. PERMUTATIONS AND COMBINATIONS")
    print("=" * 70)

    print("\nPermutations of [1, 2, 3]:")
    perms = permutations([1, 2, 3])
    for perm in perms:
        print(f"  {perm}")
    print(f"  Total: {len(perms)} permutations")

    print("\n2-combinations of [1, 2, 3, 4]:")
    combos = combinations([1, 2, 3, 4], 2)
    for combo in combos:
        print(f"  {combo}")
    print(f"  Total: {len(combos)} combinations")

    # ========================================================================
    # Tail Recursion
    # ========================================================================
    print("\n" + "=" * 70)
    print("7. TAIL RECURSION")
    print("=" * 70)

    print("\nTail-recursive factorial:")
    for n in [5, 10, 15]:
        print(f"  {n}! = {factorial_tail(n)}")

    print("\nNote: Python doesn't optimize tail recursion")

    # ========================================================================
    # Recursion Depth Limit
    # ========================================================================
    print("\n" + "=" * 70)
    print("8. RECURSION DEPTH LIMIT")
    print("=" * 70)

    demonstrate_recursion_limit()

    print("\n" + "=" * 70)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Recursion: function calling itself")
    print("2. Base case: condition to stop recursion (critical!)")
    print("3. Recursive case: function calls itself with modified input")
    print("4. Call stack: each call adds to stack (memory overhead)")
    print("5. Python recursion limit: ~1000 calls (sys.getrecursionlimit())")
    print("6. Tail recursion: not optimized in Python")
    print("7. Use for: trees, graphs, divide-and-conquer")
    print("8. Avoid for: simple loops (use iteration instead)")
    print("9. Watch for: infinite recursion (missing base case)")
    print("10. Consider: memoization for overlapping subproblems")
    print("=" * 70)

