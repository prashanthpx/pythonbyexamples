"""
Example: Non-blocking Execution
Demonstrates running processes without waiting.

Key Concepts:
- Popen returns immediately (non-blocking)
- Can start multiple processes concurrently
- Do other work while process runs
- Check status with poll()
- Useful for parallel execution

Benefits:
- Better performance
- Concurrent execution
- Responsive applications
- Efficient resource usage
"""

import subprocess
import time
from typing import List


# ============================================================================
# BASIC NON-BLOCKING
# ============================================================================

def basic_non_blocking() -> None:
    """
    Basic non-blocking execution.
    
    Start process and continue immediately.
    """
    print("Non-blocking execution:")
    
    # Start process
    print("Starting process...")
    process = subprocess.Popen(
        ["sleep", "3"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"Process started (PID {process.pid})")
    print("Continuing immediately!")
    
    # Do other work
    for i in range(3):
        print(f"  Doing other work... {i+1}")
        time.sleep(1)
    
    # Wait for completion
    print("Now waiting for process...")
    process.wait()
    print("Process finished!")


# ============================================================================
# MULTIPLE CONCURRENT PROCESSES
# ============================================================================

def multiple_concurrent_processes() -> None:
    """
    Run multiple processes concurrently.
    
    Start all processes, then wait for all.
    """
    print("\n" + "=" * 70)
    print("MULTIPLE CONCURRENT PROCESSES")
    print("=" * 70)
    
    print("\nStarting 3 processes concurrently...")
    start_time = time.time()
    
    # Start all processes
    processes = [
        subprocess.Popen(["sleep", "2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE),
        subprocess.Popen(["sleep", "2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE),
        subprocess.Popen(["sleep", "2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE),
    ]
    
    print(f"All processes started in {time.time() - start_time:.4f}s")
    
    # Wait for all to complete
    print("Waiting for all processes...")
    for i, process in enumerate(processes):
        process.wait()
        print(f"  Process {i+1} finished")
    
    elapsed = time.time() - start_time
    print(f"\nAll processes completed in {elapsed:.2f}s")
    print("(Would take 6s if run sequentially!)")


# ============================================================================
# SEQUENTIAL VS CONCURRENT
# ============================================================================

def sequential_vs_concurrent() -> None:
    """
    Compare sequential vs concurrent execution.
    
    Shows performance difference.
    """
    print("\n" + "=" * 70)
    print("SEQUENTIAL VS CONCURRENT")
    print("=" * 70)
    
    # Sequential execution
    print("\n1. Sequential execution:")
    start = time.time()
    
    for i in range(3):
        result = subprocess.run(
            ["sleep", "1"],
            capture_output=True
        )
        print(f"   Process {i+1} finished")
    
    sequential_time = time.time() - start
    print(f"   Total time: {sequential_time:.2f}s")
    
    # Concurrent execution
    print("\n2. Concurrent execution:")
    start = time.time()
    
    # Start all
    processes = [
        subprocess.Popen(["sleep", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for _ in range(3)
    ]
    
    # Wait for all
    for i, process in enumerate(processes):
        process.wait()
        print(f"   Process {i+1} finished")
    
    concurrent_time = time.time() - start
    print(f"   Total time: {concurrent_time:.2f}s")
    
    print(f"\n   Speedup: {sequential_time/concurrent_time:.2f}x faster!")


# ============================================================================
# WORK WHILE WAITING
# ============================================================================

def work_while_waiting() -> None:
    """
    Do work while process runs.
    
    Demonstrates responsive execution.
    """
    print("\n" + "=" * 70)
    print("WORK WHILE WAITING")
    print("=" * 70)
    
    # Start long-running process
    print("\nStarting long-running process...")
    process = subprocess.Popen(
        ["sleep", "5"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Do work while it runs
    print("Doing work while process runs:")
    counter = 0
    while process.poll() is None:  # ← While still running
        counter += 1
        print(f"  Work iteration {counter}")
        time.sleep(1)
    
    print(f"\nProcess finished after {counter} iterations")


# ============================================================================
# PROCESS WITH RESULTS
# ============================================================================

def process_with_results() -> None:
    """
    Start processes and collect results.
    
    Non-blocking with result collection.
    """
    print("\n" + "=" * 70)
    print("PROCESS WITH RESULTS")
    print("=" * 70)
    
    # Commands to run
    commands = [
        ["echo", "Result 1"],
        ["echo", "Result 2"],
        ["echo", "Result 3"],
    ]
    
    print("\nStarting processes...")
    
    # Start all processes
    processes = [
        subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for cmd in commands
    ]
    
    print(f"Started {len(processes)} processes")
    
    # Collect results
    print("\nCollecting results:")
    results = []
    for i, process in enumerate(processes):
        stdout, stderr = process.communicate()
        results.append(stdout.strip())
        print(f"  Process {i+1}: {stdout.strip()}")
    
    print(f"\nCollected {len(results)} results")


# ============================================================================
# EARLY TERMINATION
# ============================================================================

def early_termination() -> None:
    """
    Start process and terminate early if needed.
    
    Demonstrates process control.
    """
    print("\n" + "=" * 70)
    print("EARLY TERMINATION")
    print("=" * 70)
    
    # Start long process
    print("\nStarting long process...")
    process = subprocess.Popen(
        ["sleep", "10"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Monitor and terminate early
    print("Monitoring process...")
    for i in range(3):
        if process.poll() is None:
            print(f"  Still running... ({i+1}s)")
            time.sleep(1)
    
    # Terminate early
    print("Terminating process early...")
    process.terminate()
    process.wait()
    print("Process terminated!")


# ============================================================================
# DEMONSTRATION: Non-blocking Execution
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("NON-BLOCKING EXECUTION")
    print("=" * 70)
    
    # Basic non-blocking
    print("\n" + "=" * 70)
    print("1. BASIC NON-BLOCKING")
    print("=" * 70)
    basic_non_blocking()
    
    # Multiple concurrent
    multiple_concurrent_processes()
    
    # Sequential vs concurrent
    sequential_vs_concurrent()
    
    # Work while waiting
    work_while_waiting()
    
    # With results
    process_with_results()
    
    # Early termination
    early_termination()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Popen returns immediately (non-blocking)")
    print("2. Can start multiple processes concurrently")
    print("3. Do other work while process runs")
    print("4. Use poll() to check if still running")
    print("5. Concurrent execution is much faster")
    print("6. Start all processes, then wait for all")
    print("7. Collect results with communicate()")
    print("8. Can terminate processes early")
    print("9. Great for parallel execution")
    print("10. Improves application responsiveness")
    print("=" * 70)

