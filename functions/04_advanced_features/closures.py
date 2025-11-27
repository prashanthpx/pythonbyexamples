"""
Example: Closures
Demonstrates closures and their advanced patterns.

A closure is a function that:
1. Is defined inside another function (nested)
2. References variables from the enclosing scope
3. Is returned or passed around
4. "Remembers" the enclosing scope even after outer function returns

Key Concepts:
- Closures capture enclosing scope
- Each closure has independent state
- Useful for data hiding and encapsulation
- Common in decorators and factory functions
"""

from typing import Callable, List, Tuple


# ============================================================================
# BASIC CLOSURES
# ============================================================================

def simple_closure() -> Callable[[], str]:
    """
    Simplest closure example.
    
    Returns:
        Closure function
    """
    message = "Hello from closure"  # ← Enclosing scope
    
    def inner() -> str:
        # ← References 'message' from enclosing scope
        return message
    
    return inner  # ← Returns closure


def closure_with_parameter(name: str) -> Callable[[], str]:
    """
    Closure that captures parameter.
    
    Args:
        name: Name to capture
        
    Returns:
        Closure function
    """
    # ← 'name' is captured by closure
    
    def greet() -> str:
        return f"Hello, {name}!"
    
    return greet  # ← Closure remembers 'name'


def closure_with_state() -> Callable[[], int]:
    """
    Closure with mutable state.
    
    Returns:
        Counter closure
    """
    count = 0  # ← Private state
    
    def counter() -> int:
        nonlocal count  # ← Modify enclosing scope
        count += 1
        return count
    
    return counter  # ← Closure maintains state


# ============================================================================
# CLOSURE FACTORIES
# ============================================================================

def make_multiplier(factor: int) -> Callable[[int], int]:
    """
    Factory function creating multiplier closures.
    
    Args:
        factor: Multiplication factor
        
    Returns:
        Multiplier function
    """
    # ← 'factor' captured by closure
    
    def multiply(x: int) -> int:
        return x * factor
    
    return multiply


def make_power(exponent: int) -> Callable[[int], int]:
    """
    Factory function creating power closures.
    
    Args:
        exponent: Power exponent
        
    Returns:
        Power function
    """
    def power(base: int) -> int:
        return base ** exponent  # ← Captures 'exponent'
    
    return power


def make_counter(start: int = 0, step: int = 1) -> Tuple[Callable[[], int], Callable[[], int], Callable[[], None]]:
    """
    Factory creating counter with increment, decrement, reset.
    
    Args:
        start: Starting value
        step: Step size
        
    Returns:
        Tuple of (increment, decrement, reset) functions
    """
    count = start  # ← Shared state
    
    def increment() -> int:
        nonlocal count
        count += step
        return count
    
    def decrement() -> int:
        nonlocal count
        count -= step
        return count
    
    def reset() -> None:
        nonlocal count
        count = start
    
    # ← All three closures share same 'count'
    return increment, decrement, reset


# ============================================================================
# CLOSURES FOR ENCAPSULATION
# ============================================================================

def create_bank_account(initial_balance: float = 0.0):
    """
    Bank account with private state using closures.
    
    Args:
        initial_balance: Starting balance
        
    Returns:
        Tuple of account operations
    """
    # ← Private state (cannot be accessed directly)
    balance = initial_balance
    transaction_history: List[str] = []
    
    def deposit(amount: float) -> float:
        nonlocal balance
        if amount > 0:
            balance += amount
            transaction_history.append(f"Deposit: +${amount:.2f}")
        return balance
    
    def withdraw(amount: float) -> float:
        nonlocal balance
        if 0 < amount <= balance:
            balance -= amount
            transaction_history.append(f"Withdraw: -${amount:.2f}")
        return balance
    
    def get_balance() -> float:
        return balance
    
    def get_history() -> List[str]:
        return transaction_history.copy()  # ← Return copy for safety
    
    # ← Return interface to private state
    return deposit, withdraw, get_balance, get_history


def create_validator(min_value: int, max_value: int) -> Callable[[int], bool]:
    """
    Create a validator closure.

    Args:
        min_value: Minimum valid value
        max_value: Maximum valid value

    Returns:
        Validator function
    """
    # ← Capture validation rules

    def validate(value: int) -> bool:
        return min_value <= value <= max_value

    return validate


# ============================================================================
# CLOSURES WITH MULTIPLE LEVELS
# ============================================================================

def outer_closure(x: int) -> Callable[[int], Callable[[int], int]]:
    """
    Nested closures (closure returning closure).

    Args:
        x: First value

    Returns:
        Closure that returns another closure
    """
    def middle(y: int) -> Callable[[int], int]:
        # ← Captures 'x' from outer

        def inner(z: int) -> int:
            # ← Captures both 'x' and 'y'
            return x + y + z

        return inner

    return middle


def make_adder_factory() -> Callable[[int], Callable[[int], int]]:
    """
    Factory that creates adder factories.

    Returns:
        Function that creates adder functions
    """
    def make_adder(n: int) -> Callable[[int], int]:
        def add(x: int) -> int:
            return x + n
        return add

    return make_adder


# ============================================================================
# CLOSURES IN LOOPS (COMMON PITFALL)
# ============================================================================

def closure_loop_pitfall() -> List[int]:
    """
    Common pitfall: closures in loops.

    Returns:
        List showing the pitfall
    """
    # ❌ WRONG: All closures capture same 'i'
    functions_wrong = []
    for i in range(5):
        def func():
            return i  # ← Captures 'i' by reference!
        functions_wrong.append(func)

    # All functions return 4 (final value of i)
    wrong_results = [f() for f in functions_wrong]  # [4, 4, 4, 4, 4]

    # ✅ CORRECT: Use default argument
    functions_correct = []
    for i in range(5):
        def func(i=i):  # ← Captures current value
            return i
        functions_correct.append(func)

    correct_results = [f() for f in functions_correct]  # [0, 1, 2, 3, 4]

    return correct_results


def closure_loop_lambda() -> List[int]:
    """
    Closure loop pitfall with lambda.

    Returns:
        Correct results
    """
    # ✅ Lambda with default argument
    functions = [lambda x, i=i: x + i for i in range(5)]

    results = [f(10) for f in functions]  # [10, 11, 12, 13, 14]

    return results


# ============================================================================
# PRACTICAL CLOSURE PATTERNS
# ============================================================================

def make_logger(prefix: str) -> Callable[[str], None]:
    """
    Create a logger with custom prefix.

    Args:
        prefix: Log message prefix

    Returns:
        Logger function
    """
    def log(message: str) -> None:
        print(f"[{prefix}] {message}")

    return log


def make_memoizer():
    """
    Create a memoization closure.

    Returns:
        Tuple of (memoized_function, get_cache)
    """
    cache = {}  # ← Private cache

    def fibonacci(n: int) -> int:
        if n in cache:
            return cache[n]

        if n <= 1:
            result = n
        else:
            result = fibonacci(n - 1) + fibonacci(n - 2)

        cache[n] = result
        return result

    def get_cache() -> dict:
        return cache.copy()

    return fibonacci, get_cache


def make_rate_limiter(max_calls: int, time_window: float):
    """
    Create a rate limiter closure.

    Args:
        max_calls: Maximum calls allowed
        time_window: Time window in seconds

    Returns:
        Rate limiter function
    """
    import time

    calls = []  # ← Track call times

    def is_allowed() -> bool:
        nonlocal calls

        current_time = time.time()

        # Remove old calls outside time window
        calls = [t for t in calls if current_time - t < time_window]

        if len(calls) < max_calls:
            calls.append(current_time)
            return True

        return False

    return is_allowed


def make_accumulator(initial: int = 0) -> Callable[[int], int]:
    """
    Create an accumulator closure.

    Args:
        initial: Initial value

    Returns:
        Accumulator function
    """
    total = initial

    def accumulate(value: int) -> int:
        nonlocal total
        total += value
        return total

    return accumulate


# ============================================================================
# CLOSURE INSPECTION
# ============================================================================

def inspect_closure() -> dict:
    """
    Inspect closure internals.

    Returns:
        Dictionary with closure information
    """
    x = 10
    y = 20

    def closure():
        return x + y

    # ← Closure attributes
    return {
        "name": closure.__name__,
        "closure": closure.__closure__ is not None,
        "free_vars": closure.__code__.co_freevars,  # ('x', 'y')
        "cell_contents": [cell.cell_contents for cell in closure.__closure__]  # [10, 20]
    }


# ============================================================================
# DEMONSTRATION: Closures
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CLOSURES - FUNCTIONS WITH MEMORY")
    print("=" * 60)

    print("\nClosure = nested function that:")
    print("  1. References enclosing scope")
    print("  2. Is returned/passed around")
    print("  3. 'Remembers' enclosing scope")

    # ========================================================================
    # 1. SIMPLE CLOSURE
    # ========================================================================
    print("\n" + "=" * 60)
    print("1. SIMPLE CLOSURE:")
    print("=" * 60)

    closure = simple_closure()
    print(f"   closure() = '{closure()}'")
    print("   ← Closure remembers enclosing scope")

    # ========================================================================
    # 2. CLOSURE WITH PARAMETER
    # ========================================================================
    print("\n" + "=" * 60)
    print("2. CLOSURE WITH PARAMETER:")
    print("=" * 60)

    greet_alice = closure_with_parameter("Alice")
    greet_bob = closure_with_parameter("Bob")

    print(f"   greet_alice() = '{greet_alice()}'")
    print(f"   greet_bob() = '{greet_bob()}'")
    print("   ← Each closure has independent state")

    # ========================================================================
    # 3. CLOSURE WITH STATE
    # ========================================================================
    print("\n" + "=" * 60)
    print("3. CLOSURE WITH STATE:")
    print("=" * 60)

    counter = closure_with_state()
    print(f"   counter() = {counter()}")
    print(f"   counter() = {counter()}")
    print(f"   counter() = {counter()}")
    print("   ← Closure maintains state between calls")

    # ========================================================================
    # 4. CLOSURE FACTORIES
    # ========================================================================
    print("\n" + "=" * 60)
    print("4. CLOSURE FACTORIES:")
    print("=" * 60)

    times3 = make_multiplier(3)
    times7 = make_multiplier(7)

    print(f"   times3(10) = {times3(10)}")
    print(f"   times7(10) = {times7(10)}")
    print("   ← Factory creates closures with different state")

    square = make_power(2)
    cube = make_power(3)

    print(f"   square(5) = {square(5)}")
    print(f"   cube(5) = {cube(5)}")

    # ========================================================================
    # 5. COUNTER WITH OPERATIONS
    # ========================================================================
    print("\n" + "=" * 60)
    print("5. COUNTER WITH OPERATIONS:")
    print("=" * 60)

    inc, dec, reset = make_counter(0, 5)

    print(f"   inc() = {inc()}")
    print(f"   inc() = {inc()}")
    print(f"   dec() = {dec()}")
    reset()
    print(f"   After reset, inc() = {inc()}")
    print("   ← Multiple closures share same state")

    # ========================================================================
    # 6. BANK ACCOUNT (ENCAPSULATION)
    # ========================================================================
    print("\n" + "=" * 60)
    print("6. BANK ACCOUNT (ENCAPSULATION):")
    print("=" * 60)

    deposit, withdraw, balance, history = create_bank_account(100.0)

    print(f"   Initial balance: ${balance():.2f}")
    deposit(50.0)
    print(f"   After deposit: ${balance():.2f}")
    withdraw(30.0)
    print(f"   After withdraw: ${balance():.2f}")
    print(f"   History: {history()}")
    print("   ← Closures provide data hiding")

    # ========================================================================
    # 7. VALIDATOR
    # ========================================================================
    print("\n" + "=" * 60)
    print("7. VALIDATOR:")
    print("=" * 60)

    is_valid_age = create_validator(0, 120)
    is_valid_percentage = create_validator(0, 100)

    print(f"   is_valid_age(25) = {is_valid_age(25)}")
    print(f"   is_valid_age(150) = {is_valid_age(150)}")
    print(f"   is_valid_percentage(50) = {is_valid_percentage(50)}")
    print("   ← Closure captures validation rules")

    # ========================================================================
    # 8. NESTED CLOSURES
    # ========================================================================
    print("\n" + "=" * 60)
    print("8. NESTED CLOSURES:")
    print("=" * 60)

    result = outer_closure(1)(2)(3)
    print(f"   outer_closure(1)(2)(3) = {result}")
    print("   ← Closures can be nested multiple levels")

    # ========================================================================
    # 9. CLOSURE LOOP PITFALL
    # ========================================================================
    print("\n" + "=" * 60)
    print("9. CLOSURE LOOP PITFALL:")
    print("=" * 60)

    result = closure_loop_pitfall()
    print(f"   Correct results: {result}")
    print("   ⚠️  Use default args to capture loop variable")

    result = closure_loop_lambda()
    print(f"   Lambda results: {result}")

    # ========================================================================
    # 10. PRACTICAL PATTERNS
    # ========================================================================
    print("\n" + "=" * 60)
    print("10. PRACTICAL: LOGGER:")
    print("=" * 60)

    error_log = make_logger("ERROR")
    info_log = make_logger("INFO")

    print("   ", end="")
    error_log("Something went wrong")
    print("   ", end="")
    info_log("Application started")
    print("   ← Custom loggers with closures")

    print("\n   PRACTICAL: MEMOIZATION:")
    fib, cache = make_memoizer()
    result = fib(10)
    print(f"   fib(10) = {result}")
    print(f"   Cache size: {len(cache())}")
    print("   ← Closure maintains cache")

    print("\n   PRACTICAL: ACCUMULATOR:")
    acc = make_accumulator(0)
    print(f"   acc(5) = {acc(5)}")
    print(f"   acc(10) = {acc(10)}")
    print(f"   acc(3) = {acc(3)}")
    print("   ← Accumulator with closure")

    # ========================================================================
    # 11. CLOSURE INSPECTION
    # ========================================================================
    print("\n" + "=" * 60)
    print("11. CLOSURE INSPECTION:")
    print("=" * 60)

    info = inspect_closure()
    for key, value in info.items():
        print(f"   {key}: {value}")
    print("   ← Inspect closure internals")

    print("\n" + "=" * 60)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 60)
    print("1. Closure = nested function that captures enclosing scope")
    print("2. Closures 'remember' enclosing scope after outer returns")
    print("3. Each closure has independent state")
    print("4. Useful for data hiding and encapsulation")
    print("5. Common in factory functions and decorators")
    print("6. Multiple closures can share same enclosing scope")
    print("7. Pitfall: loop variables captured by reference")
    print("8. Fix: use default arguments to capture value")
    print("9. Can inspect with __closure__ and __code__")
    print("10. Powerful pattern for stateful functions")
    print("=" * 60)

