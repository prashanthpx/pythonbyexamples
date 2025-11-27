"""
Example: Sending Input to Processes (stdin)
Demonstrates how to send input to commands via stdin.

Key Concepts:
- input parameter sends data to stdin
- stdin=subprocess.PIPE for manual input
- input can be string (text mode) or bytes
- Useful for interactive commands
- Commands read from stdin instead of terminal

Common use cases:
- Send data to grep, sort, etc.
- Provide input to interactive programs
- Pipe data through filters
- Automate interactive commands
"""

import subprocess
from typing import Optional


# ============================================================================
# BASIC INPUT
# ============================================================================

def send_basic_input() -> None:
    """
    Send input to a command using input parameter.
    
    The simplest way to provide stdin data.
    """
    print("Sending input to 'cat' command:")
    
    result = subprocess.run(
        ["cat"],  # cat reads from stdin
        input="Hello from Python!\n",  # ← Send this to stdin
        capture_output=True,
        text=True
    )
    
    print(f"Output: {repr(result.stdout)}")


# ============================================================================
# INPUT WITH GREP
# ============================================================================

def input_with_grep() -> None:
    """
    Send input to grep for filtering.
    
    Common pattern for text processing.
    """
    print("\n" + "=" * 70)
    print("INPUT WITH GREP")
    print("=" * 70)
    
    # Data to search
    data = """apple
banana
cherry
date
elderberry
"""
    
    # Search for lines containing 'e'
    result = subprocess.run(
        ["grep", "e"],
        input=data,  # ← Send data to grep
        capture_output=True,
        text=True
    )
    
    print(f"\nInput data:\n{data}")
    print(f"Lines containing 'e':\n{result.stdout}")


# ============================================================================
# INPUT WITH SORT
# ============================================================================

def input_with_sort() -> None:
    """
    Send input to sort command.
    
    Demonstrates sorting data via stdin.
    """
    print("\n" + "=" * 70)
    print("INPUT WITH SORT")
    print("=" * 70)
    
    # Unsorted data
    data = """zebra
apple
mango
banana
cherry
"""
    
    # Sort the data
    result = subprocess.run(
        ["sort"],
        input=data,  # ← Send data to sort
        capture_output=True,
        text=True
    )
    
    print(f"\nUnsorted:\n{data}")
    print(f"Sorted:\n{result.stdout}")


# ============================================================================
# BYTES INPUT
# ============================================================================

def send_bytes_input() -> None:
    """
    Send bytes input instead of text.
    
    Use when working with binary data.
    """
    print("\n" + "=" * 70)
    print("BYTES INPUT")
    print("=" * 70)
    
    # Bytes input
    data = b"Hello from bytes!\n"
    
    result = subprocess.run(
        ["cat"],
        input=data,  # ← Bytes input
        capture_output=True
        # No text=True, so output is also bytes
    )
    
    print(f"\nInput type: {type(data)}")
    print(f"Input: {data}")
    print(f"Output type: {type(result.stdout)}")
    print(f"Output: {result.stdout}")


# ============================================================================
# MULTILINE INPUT
# ============================================================================

def send_multiline_input() -> None:
    """
    Send multiple lines of input.
    
    Useful for batch processing.
    """
    print("\n" + "=" * 70)
    print("MULTILINE INPUT")
    print("=" * 70)
    
    # Multiple lines
    data = """Line 1
Line 2
Line 3
Line 4
Line 5
"""
    
    # Count lines with wc
    result = subprocess.run(
        ["wc", "-l"],
        input=data,
        capture_output=True,
        text=True
    )
    
    print(f"\nInput:\n{data}")
    print(f"Line count: {result.stdout.strip()}")


# ============================================================================
# INPUT FROM FILE CONTENT
# ============================================================================

def input_from_file_content() -> None:
    """
    Read file content and send as input.
    
    Alternative to shell redirection.
    """
    print("\n" + "=" * 70)
    print("INPUT FROM FILE CONTENT")
    print("=" * 70)
    
    # Simulate file content
    file_content = """Python
Java
JavaScript
C++
Go
Rust
"""
    
    # Filter with grep
    result = subprocess.run(
        ["grep", "-i", "java"],  # -i for case-insensitive
        input=file_content,
        capture_output=True,
        text=True
    )
    
    print(f"\nFile content:\n{file_content}")
    print(f"Lines matching 'java' (case-insensitive):\n{result.stdout}")


# ============================================================================
# INPUT WITH PROCESSING
# ============================================================================

def input_with_processing() -> None:
    """
    Process data before sending as input.
    
    Shows common data preparation patterns.
    """
    print("\n" + "=" * 70)
    print("INPUT WITH PROCESSING")
    print("=" * 70)
    
    # Original data
    numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    
    # Convert to string format
    data = "\n".join(map(str, numbers)) + "\n"
    
    # Sort numerically
    result = subprocess.run(
        ["sort", "-n"],  # -n for numeric sort
        input=data,
        capture_output=True,
        text=True
    )
    
    print(f"\nOriginal: {numbers}")
    print(f"Sorted:\n{result.stdout}")


# ============================================================================
# DEMONSTRATION: stdin Input
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SENDING INPUT TO PROCESSES (stdin)")
    print("=" * 70)
    
    # Basic input
    print("\n" + "=" * 70)
    print("1. BASIC INPUT")
    print("=" * 70)
    send_basic_input()
    
    # With grep
    input_with_grep()
    
    # With sort
    input_with_sort()
    
    # Bytes input
    send_bytes_input()
    
    # Multiline input
    send_multiline_input()
    
    # From file content
    input_from_file_content()
    
    # With processing
    input_with_processing()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. input parameter sends data to stdin")
    print("2. input can be string (text mode) or bytes")
    print("3. Use with commands that read from stdin (cat, grep, sort)")
    print("4. Useful for filtering and processing data")
    print("5. Alternative to shell input redirection")
    print("6. Multiline input: use \\n to separate lines")
    print("7. Process data before sending (join, map, etc.)")
    print("8. Combine with capture_output to get results")
    print("9. Use text=True for string input/output")
    print("10. Great for automating interactive commands")
    print("=" * 70)

