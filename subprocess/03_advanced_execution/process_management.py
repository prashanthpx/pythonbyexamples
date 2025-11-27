"""
Example: Process Management
Demonstrates managing process lifecycle and resources.

Key Concepts:
- Process lifecycle: start, monitor, terminate
- Process attributes: pid, returncode, args
- Termination methods: terminate(), kill()
- Resource cleanup
- Process groups

Process states:
- Running: poll() returns None
- Finished: poll() returns returncode
- Terminated: returncode is negative
"""

import subprocess
import time
import signal
from typing import List, Optional


# ============================================================================
# PROCESS ATTRIBUTES
# ============================================================================

def process_attributes() -> None:
    """
    Explore process attributes.
    
    Shows available information about a process.
    """
    print("Process attributes:")
    
    process = subprocess.Popen(
        ["sleep", "5"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"\nWhile running:")
    print(f"  pid: {process.pid}")  # Process ID
    print(f"  args: {process.args}")  # Command arguments
    print(f"  returncode: {process.returncode}")  # None while running
    
    # Terminate and check again
    process.terminate()
    process.wait()
    
    print(f"\nAfter termination:")
    print(f"  pid: {process.pid}")  # Still available
    print(f"  returncode: {process.returncode}")  # Now has value


# ============================================================================
# TERMINATING PROCESSES
# ============================================================================

def terminating_processes() -> None:
    """
    Different ways to terminate processes.
    
    terminate() vs kill().
    """
    print("\n" + "=" * 70)
    print("TERMINATING PROCESSES")
    print("=" * 70)
    
    # Using terminate() (graceful)
    print("\n1. Using terminate() (graceful):")
    process = subprocess.Popen(
        ["sleep", "10"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"   Started process {process.pid}")
    time.sleep(1)
    
    process.terminate()  # ← Send SIGTERM (graceful)
    process.wait()
    print(f"   Terminated with code: {process.returncode}")
    
    # Using kill() (forceful)
    print("\n2. Using kill() (forceful):")
    process = subprocess.Popen(
        ["sleep", "10"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"   Started process {process.pid}")
    time.sleep(1)
    
    process.kill()  # ← Send SIGKILL (forceful)
    process.wait()
    print(f"   Killed with code: {process.returncode}")


# ============================================================================
# SENDING SIGNALS
# ============================================================================

def sending_signals() -> None:
    """
    Send custom signals to processes.
    
    Use send_signal() for specific signals.
    """
    print("\n" + "=" * 70)
    print("SENDING SIGNALS")
    print("=" * 70)
    
    process = subprocess.Popen(
        ["sleep", "10"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"\nStarted process {process.pid}")
    time.sleep(1)
    
    # Send SIGTERM
    print("Sending SIGTERM...")
    process.send_signal(signal.SIGTERM)  # ← Custom signal
    process.wait()
    
    print(f"Process terminated with code: {process.returncode}")


# ============================================================================
# PROCESS CLEANUP
# ============================================================================

def process_cleanup() -> None:
    """
    Proper process cleanup.
    
    Always clean up resources.
    """
    print("\n" + "=" * 70)
    print("PROCESS CLEANUP")
    print("=" * 70)
    
    # Using context manager (recommended)
    print("\n1. Using context manager (recommended):")
    
    with subprocess.Popen(
        ["sleep", "2"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ) as process:
        print(f"   Process started: {process.pid}")
        process.wait()
        print(f"   Process finished: {process.returncode}")
    
    print("   Resources automatically cleaned up!")
    
    # Manual cleanup
    print("\n2. Manual cleanup:")
    process = subprocess.Popen(
        ["sleep", "2"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        print(f"   Process started: {process.pid}")
        process.wait()
        print(f"   Process finished: {process.returncode}")
    finally:
        # Ensure cleanup
        if process.poll() is None:
            process.terminate()
            process.wait()
        print("   Cleanup complete!")


# ============================================================================
# MANAGING MULTIPLE PROCESSES
# ============================================================================

def managing_multiple_processes() -> None:
    """
    Manage multiple processes.
    
    Track and control several processes.
    """
    print("\n" + "=" * 70)
    print("MANAGING MULTIPLE PROCESSES")
    print("=" * 70)
    
    # Start multiple processes
    print("\nStarting processes...")
    processes = []
    for i in range(3):
        p = subprocess.Popen(
            ["sleep", str(i + 1)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(p)
        print(f"  Started process {i+1} (PID {p.pid})")
    
    # Monitor all
    print("\nMonitoring processes...")
    while any(p.poll() is None for p in processes):
        for i, p in enumerate(processes):
            if p.poll() is None:
                print(f"  Process {i+1}: running")
            else:
                print(f"  Process {i+1}: finished ({p.returncode})")
        time.sleep(1)
        print()
    
    print("All processes finished!")


# ============================================================================
# PROCESS TIMEOUT AND CLEANUP
# ============================================================================

def process_timeout_cleanup() -> None:
    """
    Handle timeout with proper cleanup.
    
    Ensure resources are freed on timeout.
    """
    print("\n" + "=" * 70)
    print("PROCESS TIMEOUT AND CLEANUP")
    print("=" * 70)
    
    process = subprocess.Popen(
        ["sleep", "10"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"\nStarted process {process.pid}")
    print("Waiting with 2-second timeout...")
    
    try:
        process.wait(timeout=2)
        print("Process completed")
    except subprocess.TimeoutExpired:
        print("⏱️  Timeout! Cleaning up...")
        process.kill()  # ← Force kill
        process.wait()  # ← Wait for cleanup
        print("Process killed and cleaned up")


# ============================================================================
# CHECKING PROCESS STATE
# ============================================================================

def checking_process_state() -> None:
    """
    Check various process states.
    
    Understand process lifecycle.
    """
    print("\n" + "=" * 70)
    print("CHECKING PROCESS STATE")
    print("=" * 70)
    
    process = subprocess.Popen(
        ["sleep", "2"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # State 1: Running
    print(f"\n1. Running:")
    print(f"   poll(): {process.poll()}")
    print(f"   returncode: {process.returncode}")
    
    # Wait for completion
    process.wait()
    
    # State 2: Finished normally
    print(f"\n2. Finished normally:")
    print(f"   poll(): {process.poll()}")
    print(f"   returncode: {process.returncode}")
    
    # State 3: Terminated
    process = subprocess.Popen(
        ["sleep", "10"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    process.terminate()
    process.wait()
    
    print(f"\n3. Terminated:")
    print(f"   poll(): {process.poll()}")
    print(f"   returncode: {process.returncode}")


# ============================================================================
# DEMONSTRATION: Process Management
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PROCESS MANAGEMENT")
    print("=" * 70)
    
    # Attributes
    print("\n" + "=" * 70)
    print("1. PROCESS ATTRIBUTES")
    print("=" * 70)
    process_attributes()
    
    # Terminating
    terminating_processes()
    
    # Signals
    sending_signals()
    
    # Cleanup
    process_cleanup()
    
    # Multiple processes
    managing_multiple_processes()
    
    # Timeout cleanup
    process_timeout_cleanup()
    
    # Process state
    checking_process_state()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Access process.pid for process ID")
    print("2. process.returncode is None while running")
    print("3. terminate() sends SIGTERM (graceful)")
    print("4. kill() sends SIGKILL (forceful)")
    print("5. send_signal() for custom signals")
    print("6. Use context manager for automatic cleanup")
    print("7. Always clean up resources (wait/terminate)")
    print("8. Handle timeouts with proper cleanup")
    print("9. Monitor multiple processes with poll()")
    print("10. Check process state with poll() and returncode")
    print("=" * 70)

