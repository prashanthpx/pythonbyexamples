"""
Example: Basic Piping
Demonstrates connecting processes with pipes.

Key Concepts:
- Pipe output from one process to another
- subprocess.PIPE constant
- Chaining commands
- Reading from previous process
- Building command pipelines

What is a pipe?
- Connects stdout of one process to stdin of another
- Allows data to flow between processes
- Similar to shell: command1 | command2
"""

import subprocess
from typing import Optional


# ============================================================================
# BASIC PIPE
# ============================================================================

def basic_pipe() -> None:
    """
    Basic pipe between two processes.
    
    Equivalent to: echo "Hello World" | wc -w
    """
    print("Basic pipe (echo | wc):")
    
    # First process: echo
    p1 = subprocess.Popen(
        ["echo", "Hello World"],
        stdout=subprocess.PIPE  # ← Capture output for piping
    )
    
    # Second process: wc (word count)
    p2 = subprocess.Popen(
        ["wc", "-w"],
        stdin=p1.stdout,  # ← Use p1's output as input
        stdout=subprocess.PIPE
    )
    
    # Close p1's stdout in parent
    if p1.stdout:
        p1.stdout.close()  # ← Allow p1 to receive SIGPIPE
    
    # Get final output
    output, _ = p2.communicate()
    
    print(f"Word count: {output.decode().strip()}")


# ============================================================================
# PIPE WITH TEXT MODE
# ============================================================================

def pipe_with_text_mode() -> None:
    """
    Pipe with text mode for easier handling.
    
    Equivalent to: echo "Line 1\nLine 2\nLine 3" | wc -l
    """
    print("\n" + "=" * 70)
    print("PIPE WITH TEXT MODE")
    print("=" * 70)
    
    # First process
    p1 = subprocess.Popen(
        ["echo", "Line 1\nLine 2\nLine 3"],
        stdout=subprocess.PIPE,
        text=True  # ← Text mode
    )
    
    # Second process
    p2 = subprocess.Popen(
        ["wc", "-l"],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        text=True  # ← Text mode
    )
    
    if p1.stdout:
        p1.stdout.close()
    
    output, _ = p2.communicate()
    
    print(f"Line count: {output.strip()}")


# ============================================================================
# MULTIPLE PIPES
# ============================================================================

def multiple_pipes() -> None:
    """
    Chain multiple processes together.
    
    Equivalent to: echo "apple\nbanana\napple" | sort | uniq
    """
    print("\n" + "=" * 70)
    print("MULTIPLE PIPES")
    print("=" * 70)
    
    # Process 1: echo
    p1 = subprocess.Popen(
        ["echo", "apple\nbanana\napple\ncherry\nbanana"],
        stdout=subprocess.PIPE
    )
    
    # Process 2: sort
    p2 = subprocess.Popen(
        ["sort"],
        stdin=p1.stdout,
        stdout=subprocess.PIPE
    )
    
    if p1.stdout:
        p1.stdout.close()
    
    # Process 3: uniq
    p3 = subprocess.Popen(
        ["uniq"],
        stdin=p2.stdout,
        stdout=subprocess.PIPE,
        text=True
    )
    
    if p2.stdout:
        p2.stdout.close()
    
    output, _ = p3.communicate()
    
    print("Unique sorted items:")
    print(output)


# ============================================================================
# PIPE WITH ERROR HANDLING
# ============================================================================

def pipe_with_error_handling() -> None:
    """
    Handle errors in piped processes.
    
    Check return codes of all processes.
    """
    print("\n" + "=" * 70)
    print("PIPE WITH ERROR HANDLING")
    print("=" * 70)
    
    # First process
    p1 = subprocess.Popen(
        ["echo", "test data"],
        stdout=subprocess.PIPE
    )
    
    # Second process
    p2 = subprocess.Popen(
        ["grep", "data"],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        text=True
    )
    
    if p1.stdout:
        p1.stdout.close()
    
    output, _ = p2.communicate()
    
    # Check return codes
    p1.wait()
    
    print(f"Process 1 return code: {p1.returncode}")
    print(f"Process 2 return code: {p2.returncode}")
    print(f"Output: {output.strip()}")


# ============================================================================
# READING PIPE OUTPUT
# ============================================================================

def reading_pipe_output() -> None:
    """
    Read output from piped processes.

    Process data as it flows through the pipe.
    """
    print("\n" + "=" * 70)
    print("READING PIPE OUTPUT")
    print("=" * 70)

    # Generate data
    p1 = subprocess.Popen(
        ["echo", "apple\nbanana\ncherry"],
        stdout=subprocess.PIPE
    )

    # Filter data
    p2 = subprocess.Popen(
        ["grep", "a"],  # Lines containing 'a'
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        text=True
    )

    if p1.stdout:
        p1.stdout.close()

    # Read output
    output, _ = p2.communicate()

    print("Lines containing 'a':")
    for line in output.strip().split('\n'):
        print(f"  - {line}")


# ============================================================================
# PIPE WITH CUSTOM DATA
# ============================================================================

def pipe_with_custom_data() -> None:
    """
    Pipe custom data through processes.

    Send your own data through a pipeline.
    """
    print("\n" + "=" * 70)
    print("PIPE WITH CUSTOM DATA")
    print("=" * 70)

    # Custom data
    data = "apple\nbanana\napple\ncherry\nbanana\napple\n"

    # Process 1: sort
    p1 = subprocess.Popen(
        ["sort"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    # Process 2: uniq -c (count occurrences)
    p2 = subprocess.Popen(
        ["uniq", "-c"],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        text=True
    )

    if p1.stdout:
        p1.stdout.close()

    # Send data to first process
    p1.stdin.write(data) if p1.stdin else None
    if p1.stdin:
        p1.stdin.close()

    # Get result
    output, _ = p2.communicate()

    print("Item counts:")
    print(output)


# ============================================================================
# DEMONSTRATION: Basic Piping
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("BASIC PIPING")
    print("=" * 70)

    # Basic pipe
    print("\n" + "=" * 70)
    print("1. BASIC PIPE")
    print("=" * 70)
    basic_pipe()

    # Text mode
    pipe_with_text_mode()

    # Multiple pipes
    multiple_pipes()

    # Error handling
    pipe_with_error_handling()

    # Reading output
    reading_pipe_output()

    # Custom data
    pipe_with_custom_data()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Use subprocess.PIPE to connect processes")
    print("2. Set stdin of p2 to stdout of p1")
    print("3. Close p1.stdout after connecting to p2")
    print("4. Use text=True for easier string handling")
    print("5. Chain multiple processes for complex pipelines")
    print("6. Check return codes of all processes")
    print("7. Use communicate() to get final output")
    print("8. Pipes work like shell: cmd1 | cmd2")
    print("9. Can send custom data through pipelines")
    print("10. Always handle errors in piped processes")
    print("=" * 70)

