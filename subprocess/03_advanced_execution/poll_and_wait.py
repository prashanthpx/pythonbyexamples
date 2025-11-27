"""
Example: poll() and wait() Methods
Demonstrates checking process status and waiting for completion.

Key Concepts:
- poll() checks if process has finished (non-blocking)
- wait() waits for process to finish (blocking)
- returncode is None while running
- returncode is set after completion
- Use timeout to prevent hanging

Methods:
- poll(): Check status without waiting
- wait(): Wait for completion
- wait(timeout): Wait with timeout
"""

import subprocess
import time
from typing import Optional


# ============================================================================
# BASIC POLL
# ============================================================================

def basic_poll() -> None:
    """
    Use poll() to check process status.
    
    poll() returns None if still running, returncode if finished.
    """
    print("Basic poll():")
    
    # Start long-running process
    process = subprocess.Popen(
        ["sleep", "2"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"Process started, PID: {process.pid}")
    
    # Check status immediately
    status = process.poll()  # ← Returns None if running
    print(f"Status immediately: {status}")
    
    # Wait a bit and check again
    time.sleep(1)
    status = process.poll()
    print(f"Status after 1 second: {status}")
    
    # Wait for completion
    time.sleep(2)
    status = process.poll()
    print(f"Status after 3 seconds: {status}")  # Should be 0


# ============================================================================
# BASIC WAIT
# ============================================================================

def basic_wait() -> None:
    """
    Use wait() to wait for process completion.
    
    wait() blocks until process finishes.
    """
    print("\n" + "=" * 70)
    print("BASIC WAIT")
    print("=" * 70)
    
    print("\nStarting process...")
    process = subprocess.Popen(
        ["sleep", "2"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print("Waiting for completion...")
    returncode = process.wait()  # ← Blocks until finished
    
    print(f"Process finished!")
    print(f"Return code: {returncode}")


# ============================================================================
# POLLING LOOP
# ============================================================================

def polling_loop() -> None:
    """
    Use poll() in a loop to monitor progress.
    
    Allows doing other work while process runs.
    """
    print("\n" + "=" * 70)
    print("POLLING LOOP")
    print("=" * 70)
    
    process = subprocess.Popen(
        ["sleep", "3"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"\nMonitoring process {process.pid}...")
    
    # Poll in a loop
    elapsed = 0
    while process.poll() is None:  # ← While still running
        print(f"  Still running... ({elapsed}s)")
        time.sleep(1)
        elapsed += 1
    
    print(f"Process finished after {elapsed} seconds")
    print(f"Return code: {process.returncode}")


# ============================================================================
# WAIT WITH TIMEOUT
# ============================================================================

def wait_with_timeout() -> None:
    """
    Use wait() with timeout.
    
    Prevents hanging on long-running processes.
    """
    print("\n" + "=" * 70)
    print("WAIT WITH TIMEOUT")
    print("=" * 70)
    
    # Quick process (within timeout)
    print("\n1. Quick process (within timeout):")
    process = subprocess.Popen(
        ["sleep", "1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        returncode = process.wait(timeout=5)  # ← 5 second timeout
        print(f"   Completed with code: {returncode}")
    except subprocess.TimeoutExpired:
        print("   Timeout!")
        process.kill()
    
    # Slow process (exceeds timeout)
    print("\n2. Slow process (exceeds timeout):")
    process = subprocess.Popen(
        ["sleep", "10"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        returncode = process.wait(timeout=2)  # ← 2 second timeout
        print(f"   Completed with code: {returncode}")
    except subprocess.TimeoutExpired:
        print("   ⏱️  Timeout! Killing process...")
        process.kill()
        process.wait()  # Clean up
        print("   Process killed")


# ============================================================================
# POLL VS WAIT
# ============================================================================

def poll_vs_wait() -> None:
    """
    Compare poll() vs wait().
    
    Shows the difference in behavior.
    """
    print("\n" + "=" * 70)
    print("POLL VS WAIT COMPARISON")
    print("=" * 70)
    
    # poll() - non-blocking
    print("\n1. poll() - non-blocking:")
    process = subprocess.Popen(
        ["sleep", "2"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print("   Calling poll()...")
    status = process.poll()  # ← Returns immediately
    print(f"   Returned immediately: {status}")
    print("   Can do other work here!")
    
    # Clean up
    process.wait()
    
    # wait() - blocking
    print("\n2. wait() - blocking:")
    process = subprocess.Popen(
        ["sleep", "2"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print("   Calling wait()...")
    returncode = process.wait()  # ← Blocks until finished
    print(f"   Returned after process finished: {returncode}")


# ============================================================================
# CHECKING MULTIPLE PROCESSES
# ============================================================================

def check_multiple_processes() -> None:
    """
    Use poll() to check multiple processes.
    
    Monitor several processes concurrently.
    """
    print("\n" + "=" * 70)
    print("CHECKING MULTIPLE PROCESSES")
    print("=" * 70)
    
    # Start multiple processes
    processes = [
        subprocess.Popen(["sleep", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE),
        subprocess.Popen(["sleep", "2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE),
        subprocess.Popen(["sleep", "3"], stdout=subprocess.PIPE, stderr=subprocess.PIPE),
    ]
    
    print(f"\nStarted {len(processes)} processes")
    
    # Monitor all processes
    while any(p.poll() is None for p in processes):  # ← While any running
        for i, p in enumerate(processes):
            status = p.poll()
            if status is None:
                print(f"  Process {i+1} (PID {p.pid}): running")
            else:
                print(f"  Process {i+1} (PID {p.pid}): finished ({status})")
        print()
        time.sleep(1)
    
    print("All processes finished!")


# ============================================================================
# DEMONSTRATION: poll() and wait()
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("POLL() AND WAIT() METHODS")
    print("=" * 70)
    
    # Basic poll
    print("\n" + "=" * 70)
    print("1. BASIC POLL")
    print("=" * 70)
    basic_poll()
    
    # Basic wait
    basic_wait()
    
    # Polling loop
    polling_loop()
    
    # Wait with timeout
    wait_with_timeout()
    
    # Comparison
    poll_vs_wait()
    
    # Multiple processes
    check_multiple_processes()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. poll() checks status without waiting (non-blocking)")
    print("2. wait() waits for completion (blocking)")
    print("3. poll() returns None if running, returncode if finished")
    print("4. wait() returns returncode after completion")
    print("5. Use wait(timeout=N) to prevent hanging")
    print("6. TimeoutExpired raised if timeout exceeded")
    print("7. Use poll() in loop to monitor progress")
    print("8. poll() allows doing other work while waiting")
    print("9. Use poll() to check multiple processes")
    print("10. Always call wait() or poll() to clean up")
    print("=" * 70)

