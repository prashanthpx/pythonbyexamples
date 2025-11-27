"""
Example: Return Codes and Exit Status
Demonstrates how to check if commands succeeded or failed.

Key Concepts:
- Return code 0 = success
- Non-zero return code = failure
- returncode attribute contains exit status
- check=True raises exception on failure
- Different commands have different error codes

Why return codes matter:
- Detect command failures
- Handle errors appropriately
- Build robust scripts
"""

import subprocess
from typing import Optional


# ============================================================================
# BASIC RETURN CODE CHECKING
# ============================================================================

def check_return_code_manual() -> None:
    """
    Manually check return code after command execution.
    
    Return code 0 means success, non-zero means failure.
    """
    print("Running: ls /tmp")
    result = subprocess.run(["ls", "/tmp"])
    
    print(f"\nReturn code: {result.returncode}")  # ← 0 = success
    
    if result.returncode == 0:
        print("✅ Command succeeded!")
    else:
        print("❌ Command failed!")


def check_failed_command() -> None:
    """
    Demonstrate a command that fails.
    
    Trying to list a non-existent directory.
    """
    print("\nRunning: ls /nonexistent_directory")
    result = subprocess.run(["ls", "/nonexistent_directory"])
    
    print(f"\nReturn code: {result.returncode}")  # ← Non-zero = failure
    
    if result.returncode == 0:
        print("✅ Command succeeded!")
    else:
        print(f"❌ Command failed with code {result.returncode}!")


# ============================================================================
# USING check=True
# ============================================================================

def use_check_parameter() -> None:
    """
    Use check=True to automatically raise exception on failure.
    
    This is the recommended way for most cases.
    """
    print("\n" + "=" * 70)
    print("USING check=True")
    print("=" * 70)
    
    # Success case
    print("\n1. Successful command:")
    try:
        subprocess.run(
            ["echo", "Hello"],
            check=True  # ← Raise CalledProcessError if returncode != 0
        )
        print("✅ Command succeeded!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
    
    # Failure case
    print("\n2. Failed command:")
    try:
        subprocess.run(
            ["ls", "/nonexistent"],
            check=True  # ← Will raise exception
        )
        print("✅ Command succeeded!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with return code {e.returncode}")


# ============================================================================
# DIFFERENT EXIT CODES
# ============================================================================

def demonstrate_exit_codes() -> None:
    """
    Different commands return different exit codes.
    
    Common conventions:
    - 0: Success
    - 1: General error
    - 2: Misuse of command
    - 126: Command cannot execute
    - 127: Command not found
    - 130: Terminated by Ctrl+C
    """
    print("\n" + "=" * 70)
    print("DIFFERENT EXIT CODES")
    print("=" * 70)
    
    test_cases = [
        (["echo", "success"], "Successful command"),
        (["ls", "/nonexistent"], "Non-existent file"),
        (["false"], "Command that always fails"),
        (["test", "1", "-eq", "2"], "Failed test condition"),
    ]
    
    for command, description in test_cases:
        print(f"\n{description}:")
        print(f"  Command: {' '.join(command)}")
        result = subprocess.run(command)
        print(f"  Return code: {result.returncode}")


# ============================================================================
# CUSTOM EXIT CODES
# ============================================================================

def run_python_with_exit_code(exit_code: int) -> int:
    """
    Run Python command that exits with specific code.
    
    Args:
        exit_code: Exit code to use
        
    Returns:
        The return code from the command
    """
    result = subprocess.run([
        "python3",
        "-c",
        f"import sys; sys.exit({exit_code})"
    ])
    return result.returncode


# ============================================================================
# HANDLING RETURN CODES
# ============================================================================

def handle_return_codes() -> None:
    """
    Demonstrate different ways to handle return codes.
    """
    print("\n" + "=" * 70)
    print("HANDLING RETURN CODES")
    print("=" * 70)
    
    # Method 1: Manual check
    print("\n1. Manual check:")
    result = subprocess.run(["ls", "/tmp"])
    if result.returncode != 0:
        print(f"  Error: Command failed with code {result.returncode}")
    else:
        print("  Success!")
    
    # Method 2: Using check=True with try/except
    print("\n2. Using check=True:")
    try:
        subprocess.run(["ls", "/tmp"], check=True)
        print("  Success!")
    except subprocess.CalledProcessError as e:
        print(f"  Error: {e}")
    
    # Method 3: Check specific return codes
    print("\n3. Check specific return codes:")
    result = subprocess.run(["grep", "pattern", "/dev/null"])
    if result.returncode == 0:
        print("  Pattern found")
    elif result.returncode == 1:
        print("  Pattern not found (normal)")
    else:
        print(f"  Error occurred: {result.returncode}")


# ============================================================================
# DEMONSTRATION: Return Codes
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("RETURN CODES AND EXIT STATUS")
    print("=" * 70)
    
    # Basic return code checking
    print("\n" + "=" * 70)
    print("1. BASIC RETURN CODE CHECKING")
    print("=" * 70)
    check_return_code_manual()
    check_failed_command()
    
    # Using check=True
    use_check_parameter()
    
    # Different exit codes
    demonstrate_exit_codes()

    # Handling return codes
    handle_return_codes()

    # Custom exit codes
    print("\n" + "=" * 70)
    print("4. CUSTOM EXIT CODES")
    print("=" * 70)

    for code in [0, 1, 42, 127]:
        returned = run_python_with_exit_code(code)
        print(f"  Requested exit code {code}, got: {returned}")

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Return code 0 = success, non-zero = failure")
    print("2. Access return code via result.returncode")
    print("3. Use check=True to auto-raise exception on failure")
    print("4. CalledProcessError contains returncode attribute")
    print("5. Different commands use different error codes")
    print("6. Always check return codes in production code")
    print("7. Common codes: 0=success, 1=error, 127=not found")
    print("8. Use try/except with check=True for robust error handling")
    print("=" * 70)

