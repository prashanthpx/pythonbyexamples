"""
Example: Class Decorators
Demonstrates decorating classes and class-based decorators.

Key Concepts:
- Decorators can be applied to classes
- Classes can be used as decorators
- Class decorators modify class behavior
- __call__ method makes instances callable

Two main patterns:
1. Function decorator for classes (modifies class)
2. Class as decorator (uses __call__)
"""

from typing import Any, Callable
from functools import wraps
import time


# ============================================================================
# PATTERN 1: FUNCTION DECORATOR FOR CLASSES
# ============================================================================

def add_str_method(cls: type) -> type:
    """
    Decorator that adds a __str__ method to a class.
    
    Args:
        cls: Class to decorate
        
    Returns:
        Modified class
    """
    def __str__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    
    cls.__str__ = __str__  # ← Add method to class
    return cls


@add_str_method
class Person:
    """Person class with auto-generated __str__."""
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


@add_str_method
class Product:
    """Product class with auto-generated __str__."""
    
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


# ============================================================================
# SINGLETON PATTERN WITH CLASS DECORATOR
# ============================================================================

def singleton(cls: type) -> type:
    """
    Decorator that makes a class a singleton.
    
    Only one instance of the class can exist.
    """
    instances = {}  # ← Store instances
    
    @wraps(cls, updated=[])  # ← Preserve class metadata
    def get_instance(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class Database:
    """Database connection (singleton)."""
    
    def __init__(self, host: str = "localhost"):
        self.host = host
        print(f"Connecting to database at {host}")
    
    def query(self, sql: str) -> str:
        return f"Executing: {sql}"


@singleton
class Config:
    """Application configuration (singleton)."""
    
    def __init__(self):
        self.settings = {}
        print("Loading configuration...")
    
    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value
    
    def get(self, key: str) -> Any:
        return self.settings.get(key)


# ============================================================================
# PATTERN 2: CLASS AS DECORATOR
# ============================================================================

class CountCalls:
    """
    Class-based decorator that counts function calls.
    
    Uses __call__ to make instances callable.
    """
    
    def __init__(self, func: Callable):
        """
        Initialize decorator.
        
        Args:
            func: Function to decorate
        """
        wraps(func)(self)  # ← Preserve function metadata
        self.func = func
        self.call_count = 0
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Called when decorated function is invoked.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result
        """
        self.call_count += 1
        print(f"Call #{self.call_count} to {self.func.__name__}")
        return self.func(*args, **kwargs)


@CountCalls
def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"


@CountCalls
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


# ============================================================================
# CLASS DECORATOR WITH PARAMETERS
# ============================================================================

class Timer:
    """
    Class-based decorator that times function execution.
    
    Can be configured with custom message.
    """
    
    def __init__(self, message: str = "Execution time"):
        """
        Initialize timer decorator.
        
        Args:
            message: Message to display
        """
        self.message = message
    
    def __call__(self, func: Callable) -> Callable:
        """
        Decorate function.
        
        Args:
            func: Function to decorate
            
        Returns:
            Wrapped function
        """
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            print(f"{self.message} for {func.__name__}: {elapsed:.4f}s")
            return result
        return wrapper


@Timer()  # ← Note: parentheses required
def slow_function(n: int) -> int:
    """Slow function."""
    time.sleep(0.1)
    return n * 2


@Timer(message="Custom timer")
def another_function(x: int) -> int:
    """Another function."""
    time.sleep(0.05)
    return x ** 2


# ============================================================================
# MEMOIZATION WITH CLASS DECORATOR
# ============================================================================

class Memoize:
    """
    Class-based memoization decorator.

    Caches function results to avoid recomputation.
    """

    def __init__(self, func: Callable):
        """
        Initialize memoization decorator.

        Args:
            func: Function to memoize
        """
        wraps(func)(self)
        self.func = func
        self.cache: dict = {}

    def __call__(self, *args: Any) -> Any:
        """
        Call memoized function.

        Args:
            *args: Function arguments

        Returns:
            Cached or computed result
        """
        if args in self.cache:
            print(f"Cache hit for {self.func.__name__}{args}")
            return self.cache[args]

        print(f"Cache miss for {self.func.__name__}{args}")
        result = self.func(*args)
        self.cache[args] = result
        return result

    def clear_cache(self) -> None:
        """Clear the cache."""
        self.cache.clear()
        print(f"Cache cleared for {self.func.__name__}")


@Memoize
def fibonacci(n: int) -> int:
    """Calculate Fibonacci number (memoized)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@Memoize
def factorial(n: int) -> int:
    """Calculate factorial (memoized)."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


# ============================================================================
# VALIDATION WITH CLASS DECORATOR
# ============================================================================

class ValidateTypes:
    """
    Class-based decorator for type validation.

    Validates argument types match annotations.
    """

    def __init__(self, func: Callable):
        """
        Initialize validation decorator.

        Args:
            func: Function to validate
        """
        wraps(func)(self)
        self.func = func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Call function with type validation.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            TypeError: If argument types don't match annotations
        """
        # Get function annotations
        annotations = self.func.__annotations__

        # Validate positional arguments
        param_names = list(self.func.__code__.co_varnames[:self.func.__code__.co_argcount])

        for i, (arg, param_name) in enumerate(zip(args, param_names)):
            if param_name in annotations:
                expected_type = annotations[param_name]
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"Argument '{param_name}' must be {expected_type.__name__}, "
                        f"got {type(arg).__name__}"
                    )

        return self.func(*args, **kwargs)


@ValidateTypes
def process_user(name: str, age: int) -> str:
    """Process user data (with type validation)."""
    return f"User: {name}, Age: {age}"


@ValidateTypes
def calculate_price(base: float, tax: float) -> float:
    """Calculate price with tax (with type validation)."""
    return base * (1 + tax)


# ============================================================================
# ADDING METHODS TO CLASS
# ============================================================================

def add_methods(**methods: Callable) -> Callable:
    """
    Decorator that adds methods to a class.

    Args:
        **methods: Methods to add (name=function)

    Returns:
        Class decorator
    """
    def decorator(cls: type) -> type:
        for name, method in methods.items():
            setattr(cls, name, method)
        return cls
    return decorator


def to_dict(self) -> dict:
    """Convert instance to dictionary."""
    return self.__dict__.copy()


def from_dict(cls, data: dict) -> Any:
    """Create instance from dictionary."""
    return cls(**data)


@add_methods(to_dict=to_dict, from_dict=classmethod(from_dict))
class User:
    """User class with added methods."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


# ============================================================================
# FREEZING CLASS (IMMUTABLE)
# ============================================================================

def frozen(cls: type) -> type:
    """
    Decorator that makes a class immutable.

    Prevents attribute modification after initialization.
    """
    original_setattr = cls.__setattr__

    def __setattr__(self, name: str, value: Any) -> None:
        if hasattr(self, '_frozen') and self._frozen:
            raise AttributeError(f"Cannot modify frozen class {cls.__name__}")
        original_setattr(self, name, value)

    def __init_wrapper__(original_init: Callable) -> Callable:
        @wraps(original_init)
        def wrapper(self, *args: Any, **kwargs: Any) -> None:
            original_init(self, *args, **kwargs)
            original_setattr(self, '_frozen', True)
        return wrapper

    cls.__setattr__ = __setattr__
    cls.__init__ = __init_wrapper__(cls.__init__)

    return cls


@frozen
class Point:
    """Immutable point class."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# ============================================================================
# DEMONSTRATION: Class Decorators
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CLASS DECORATORS")
    print("=" * 70)

    # ========================================================================
    # Function Decorator for Classes
    # ========================================================================
    print("\n" + "=" * 70)
    print("1. FUNCTION DECORATOR FOR CLASSES")
    print("=" * 70)

    print("\nCreating Person and Product:")
    person = Person("Alice", 30)
    product = Product("Laptop", 999.99)

    print(f"Person: {person}")
    print(f"Product: {product}")

    # ========================================================================
    # Singleton Pattern
    # ========================================================================
    print("\n" + "=" * 70)
    print("2. SINGLETON PATTERN")
    print("=" * 70)

    print("\nCreating Database instances:")
    db1 = Database("localhost")
    db2 = Database("remote")  # Same instance!

    print(f"db1 is db2: {db1 is db2}")
    print(f"db1.host: {db1.host}")
    print(f"db2.host: {db2.host}")

    print("\nCreating Config instances:")
    config1 = Config()
    config2 = Config()  # Same instance!

    config1.set("debug", True)
    print(f"config1 is config2: {config1 is config2}")
    print(f"config2.get('debug'): {config2.get('debug')}")

    # ========================================================================
    # Class as Decorator
    # ========================================================================
    print("\n" + "=" * 70)
    print("3. CLASS AS DECORATOR (CountCalls)")
    print("=" * 70)

    print("\nCalling greet() multiple times:")
    greet("Alice")
    greet("Bob")
    greet("Charlie")
    print(f"Total calls to greet: {greet.call_count}")

    print("\nCalling add() multiple times:")
    add(1, 2)
    add(3, 4)
    print(f"Total calls to add: {add.call_count}")

    # ========================================================================
    # Class Decorator with Parameters
    # ========================================================================
    print("\n" + "=" * 70)
    print("4. CLASS DECORATOR WITH PARAMETERS (Timer)")
    print("=" * 70)

    print("\nCalling slow_function(10):")
    slow_function(10)

    print("\nCalling another_function(5):")
    another_function(5)

    # ========================================================================
    # Memoization
    # ========================================================================
    print("\n" + "=" * 70)
    print("5. MEMOIZATION WITH CLASS DECORATOR")
    print("=" * 70)

    print("\nCalculating fibonacci(5):")
    result = fibonacci(5)
    print(f"Result: {result}")

    print("\nCalculating fibonacci(5) again (cached):")
    result = fibonacci(5)
    print(f"Result: {result}")

    print("\nCalculating factorial(5):")
    result = factorial(5)
    print(f"Result: {result}")

    # ========================================================================
    # Type Validation
    # ========================================================================
    print("\n" + "=" * 70)
    print("6. TYPE VALIDATION")
    print("=" * 70)

    print("\nCalling process_user('Alice', 30):")
    result = process_user("Alice", 30)
    print(f"Result: {result}")

    print("\nCalling process_user('Bob', '25'):")
    try:
        result = process_user("Bob", "25")  # type: ignore
    except TypeError as e:
        print(f"Error: {e}")

    # ========================================================================
    # Adding Methods to Class
    # ========================================================================
    print("\n" + "=" * 70)
    print("7. ADDING METHODS TO CLASS")
    print("=" * 70)

    print("\nCreating User:")
    user = User("Alice", "alice@example.com")

    print("\nConverting to dict:")
    user_dict = user.to_dict()
    print(f"Dict: {user_dict}")

    print("\nCreating from dict:")
    new_user = User.from_dict({"name": "Bob", "email": "bob@example.com"})
    print(f"New user: {new_user.name}, {new_user.email}")

    # ========================================================================
    # Frozen Class
    # ========================================================================
    print("\n" + "=" * 70)
    print("8. FROZEN CLASS (IMMUTABLE)")
    print("=" * 70)

    print("\nCreating Point(3, 4):")
    point = Point(3.0, 4.0)
    print(f"Point: ({point.x}, {point.y})")

    print("\nTrying to modify point.x:")
    try:
        point.x = 5.0
    except AttributeError as e:
        print(f"Error: {e}")

    print("\n" + "=" * 70)

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Decorators can be applied to classes")
    print("2. Function decorators modify class definition")
    print("3. Classes can be used as decorators via __call__")
    print("4. Class decorators can add/modify methods and attributes")
    print("5. Singleton pattern: ensure only one instance exists")
    print("6. Class-based decorators maintain state")
    print("7. Use wraps() to preserve metadata")
    print("8. Class decorators with params: __init__ for params, __call__ for func")
    print("9. Can make classes immutable with decorators")
    print("10. Decorators enable powerful metaprogramming")
    print("=" * 70)

