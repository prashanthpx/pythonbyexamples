"""
Example: communicate() Method
Demonstrates using communicate() for process I/O.

Key Concepts:
- communicate() sends input and reads output
- Waits for process to complete
- Returns (stdout, stderr) tuple
- Handles deadlocks automatically
- Preferred over manual read/write

Why communicate():
- Prevents deadlocks
- Handles buffering correctly
- Simpler than manual I/O
- Thread-safe
- Recommended by Python docs
"""

import subprocess
from typing import Tuple, Optional


# ============================================================================
# BASIC COMMUNICATE
# ============================================================================

def basic_communicate() -> None:
    """
    Basic communicate() usage.
    
    Waits for process and returns output.
    """
    print("Basic communicate():")
    
    process = subprocess.Popen(
        ["echo", "Hello World"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait and get output
    stdout, stderr = process.communicate()  # ← Returns (stdout, stderr)
    
    print(f"stdout: {repr(stdout)}")
    print(f"stderr: {repr(stderr)}")
    print(f"Return code: {process.returncode}")


# ============================================================================
# COMMUNICATE WITH INPUT
# ============================================================================

def communicate_with_input() -> None:
    """
    Send input to process with communicate().
    
    Pass input parameter to send data to stdin.
    """
    print("\n" + "=" * 70)
    print("COMMUNICATE WITH INPUT")
    print("=" * 70)
    
    process = subprocess.Popen(
        ["cat"],  # cat reads from stdin
        stdin=subprocess.PIPE,   # ← Enable stdin
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send input and get output
    input_data = "Hello from communicate!\n"
    stdout, stderr = process.communicate(input=input_data)  # ← Send input
    
    print(f"Input: {repr(input_data)}")
    print(f"Output: {repr(stdout)}")


# ============================================================================
# COMMUNICATE WITH GREP
# ============================================================================

def communicate_with_grep() -> None:
    """
    Use communicate() with grep.
    
    Common pattern for filtering data.
    """
    print("\n" + "=" * 70)
    print("COMMUNICATE WITH GREP")
    print("=" * 70)
    
    # Data to filter
    data = """apple
banana
cherry
date
elderberry
fig
grape
"""
    
    process = subprocess.Popen(
        ["grep", "e"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send data and get results
    stdout, stderr = process.communicate(input=data)
    
    print(f"Input:\n{data}")
    print(f"Lines containing 'e':\n{stdout}")


# ============================================================================
# COMMUNICATE WITH TIMEOUT
# ============================================================================

def communicate_with_timeout() -> None:
    """
    Use timeout with communicate().
    
    Prevents hanging on long-running processes.
    """
    print("\n" + "=" * 70)
    print("COMMUNICATE WITH TIMEOUT")
    print("=" * 70)
    
    # Quick command
    print("\n1. Quick command (within timeout):")
    process = subprocess.Popen(
        ["echo", "Hello"],
        stdout=subprocess.PIPE,
        text=True
    )
    
    try:
        stdout, stderr = process.communicate(timeout=5)  # ← 5 second timeout
        print(f"   Output: {repr(stdout)}")
    except subprocess.TimeoutExpired:
        print("   Timeout!")
        process.kill()
        process.communicate()
    
    # Slow command
    print("\n2. Slow command (exceeds timeout):")
    process = subprocess.Popen(
        ["sleep", "10"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        stdout, stderr = process.communicate(timeout=2)  # ← 2 second timeout
        print("   Completed")
    except subprocess.TimeoutExpired:
        print("   ⏱️  Timeout! Killing process...")
        process.kill()
        stdout, stderr = process.communicate()  # Clean up
        print("   Process killed")


# ============================================================================
# COMMUNICATE VS MANUAL READ
# ============================================================================

def communicate_vs_manual_read() -> None:
    """
    Compare communicate() vs manual read.
    
    Shows why communicate() is preferred.
    """
    print("\n" + "=" * 70)
    print("COMMUNICATE VS MANUAL READ")
    print("=" * 70)
    
    # Using communicate() (recommended)
    print("\n1. Using communicate() (recommended):")
    process = subprocess.Popen(
        ["echo", "Hello"],
        stdout=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate()  # ← Safe, handles deadlocks
    print(f"   Output: {repr(stdout)}")
    
    # Manual read (not recommended)
    print("\n2. Manual read (not recommended):")
    process = subprocess.Popen(
        ["echo", "Hello"],
        stdout=subprocess.PIPE,
        text=True
    )
    
    # This can deadlock with large output!
    if process.stdout:
        output = process.stdout.read()  # ← Can deadlock
        print(f"   Output: {repr(output)}")
    
    process.wait()


# ============================================================================
# COMMUNICATE RETURN VALUES
# ============================================================================

def communicate_return_values() -> None:
    """
    Understanding communicate() return values.
    
    Returns tuple of (stdout, stderr).
    """
    print("\n" + "=" * 70)
    print("COMMUNICATE RETURN VALUES")
    print("=" * 70)
    
    # Both stdout and stderr
    print("\n1. Capturing both:")
    process = subprocess.Popen(
        ["python3", "-c", "import sys; print('OUT'); print('ERR', file=sys.stderr)"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate()
    print(f"   stdout: {repr(stdout)}")
    print(f"   stderr: {repr(stderr)}")
    
    # Only stdout
    print("\n2. Only stdout:")
    process = subprocess.Popen(
        ["echo", "Hello"],
        stdout=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate()
    print(f"   stdout: {repr(stdout)}")
    print(f"   stderr: {stderr}")  # None
    
    # No capture
    print("\n3. No capture:")
    process = subprocess.Popen(["echo", "Hello"])
    
    stdout, stderr = process.communicate()
    print(f"   stdout: {stdout}")  # None
    print(f"   stderr: {stderr}")  # None


# ============================================================================
# DEMONSTRATION: communicate() Method
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("COMMUNICATE() METHOD")
    print("=" * 70)
    
    # Basic usage
    print("\n" + "=" * 70)
    print("1. BASIC COMMUNICATE")
    print("=" * 70)
    basic_communicate()
    
    # With input
    communicate_with_input()
    
    # With grep
    communicate_with_grep()
    
    # With timeout
    communicate_with_timeout()
    
    # Comparison
    communicate_vs_manual_read()
    
    # Return values
    communicate_return_values()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. communicate() sends input and reads output")
    print("2. Returns tuple: (stdout, stderr)")
    print("3. Waits for process to complete")
    print("4. Prevents deadlocks automatically")
    print("5. Use input parameter to send data to stdin")
    print("6. Use timeout parameter to prevent hanging")
    print("7. Preferred over manual read/write")
    print("8. Thread-safe and handles buffering")
    print("9. Can only be called once per process")
    print("10. Returns None for uncaptured streams")
    print("=" * 70)

