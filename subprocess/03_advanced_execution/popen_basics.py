"""
Example: subprocess.Popen Basics
Demonstrates the low-level Popen interface.

Key Concepts:
- Popen is the low-level interface
- subprocess.run() is built on top of Popen
- Popen gives more control over process execution
- Returns immediately (non-blocking by default)
- Need to manage process lifecycle manually

Popen vs run():
- run(): High-level, waits for completion
- Popen: Low-level, returns immediately
- run(): Simpler for most cases
- Popen: More control and flexibility
"""

import subprocess
import time
from typing import Optional


# ============================================================================
# BASIC POPEN USAGE
# ============================================================================

def basic_popen() -> None:
    """
    Basic Popen usage.
    
    Popen returns immediately, process runs in background.
    """
    print("Starting process with Popen:")
    
    # Start process
    process = subprocess.Popen(
        ["echo", "Hello from Popen"]
    )
    
    print(f"Process started, PID: {process.pid}")
    print("Popen returned immediately!")
    
    # Wait for completion
    process.wait()
    print(f"Process finished with return code: {process.returncode}")


# ============================================================================
# POPEN WITH OUTPUT CAPTURE
# ============================================================================

def popen_with_capture() -> None:
    """
    Capture output with Popen.
    
    Use PIPE to capture stdout/stderr.
    """
    print("\n" + "=" * 70)
    print("POPEN WITH OUTPUT CAPTURE")
    print("=" * 70)
    
    # Start process with output capture
    process = subprocess.Popen(
        ["echo", "Hello World"],
        stdout=subprocess.PIPE,  # ← Capture stdout
        stderr=subprocess.PIPE,  # ← Capture stderr
        text=True                # ← Text mode
    )
    
    print(f"Process PID: {process.pid}")
    
    # Wait and get output
    process.wait()
    
    # Read output
    if process.stdout:
        output = process.stdout.read()
        print(f"Output: {repr(output)}")
    
    print(f"Return code: {process.returncode}")


# ============================================================================
# POPEN VS RUN
# ============================================================================

def compare_popen_vs_run() -> None:
    """
    Compare Popen vs run().
    
    Shows the difference in behavior.
    """
    print("\n" + "=" * 70)
    print("POPEN VS RUN COMPARISON")
    print("=" * 70)
    
    # Using run() - waits for completion
    print("\n1. Using subprocess.run():")
    print("   Starting...")
    start = time.time()
    
    result = subprocess.run(
        ["sleep", "1"],
        capture_output=True
    )
    
    elapsed = time.time() - start
    print(f"   Completed in {elapsed:.2f} seconds")
    print(f"   Return code: {result.returncode}")
    
    # Using Popen - returns immediately
    print("\n2. Using subprocess.Popen():")
    print("   Starting...")
    start = time.time()
    
    process = subprocess.Popen(
        ["sleep", "1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    elapsed = time.time() - start
    print(f"   Popen returned in {elapsed:.4f} seconds")
    print(f"   Process is running in background...")
    
    # Wait for completion
    process.wait()
    elapsed = time.time() - start
    print(f"   Process completed in {elapsed:.2f} seconds")
    print(f"   Return code: {process.returncode}")


# ============================================================================
# POPEN ATTRIBUTES
# ============================================================================

def popen_attributes() -> None:
    """
    Explore Popen object attributes.
    
    Shows available attributes and methods.
    """
    print("\n" + "=" * 70)
    print("POPEN ATTRIBUTES")
    print("=" * 70)
    
    process = subprocess.Popen(
        ["echo", "Hello"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print(f"\nProcess attributes:")
    print(f"  pid: {process.pid}")  # Process ID
    print(f"  args: {process.args}")  # Command arguments
    print(f"  returncode: {process.returncode}")  # None until finished
    
    # Wait for completion
    process.wait()
    
    print(f"\nAfter wait():")
    print(f"  returncode: {process.returncode}")  # Now has value
    
    # Read output
    if process.stdout:
        print(f"  stdout: {repr(process.stdout.read())}")


# ============================================================================
# WHEN TO USE POPEN
# ============================================================================

def when_to_use_popen() -> None:
    """
    When to use Popen vs run().
    """
    print("\n" + "=" * 70)
    print("WHEN TO USE POPEN")
    print("=" * 70)
    
    print("\n✅ Use subprocess.run() when:")
    print("   - Simple command execution")
    print("   - You can wait for completion")
    print("   - You want all output at once")
    print("   - Simpler code is preferred")
    
    print("\n✅ Use subprocess.Popen() when:")
    print("   - Need real-time output streaming")
    print("   - Running multiple processes concurrently")
    print("   - Need fine-grained control")
    print("   - Want to check status while running")
    print("   - Need to send input during execution")
    print("   - Building process pipelines")


# ============================================================================
# DEMONSTRATION: Popen Basics
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SUBPROCESS.POPEN BASICS")
    print("=" * 70)
    
    # Basic usage
    print("\n" + "=" * 70)
    print("1. BASIC POPEN USAGE")
    print("=" * 70)
    basic_popen()
    
    # With capture
    popen_with_capture()
    
    # Comparison
    compare_popen_vs_run()
    
    # Attributes
    popen_attributes()
    
    # When to use
    when_to_use_popen()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Popen is the low-level subprocess interface")
    print("2. subprocess.run() is built on top of Popen")
    print("3. Popen returns immediately (non-blocking)")
    print("4. Use wait() to wait for process completion")
    print("5. Access process.pid for process ID")
    print("6. process.returncode is None until finished")
    print("7. Use PIPE to capture stdout/stderr")
    print("8. Use run() for simple cases, Popen for control")
    print("9. Popen allows real-time streaming")
    print("10. Must manage process lifecycle manually")
    print("=" * 70)

