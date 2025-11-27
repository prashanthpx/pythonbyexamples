"""
Example: Text Mode vs Bytes Mode
Demonstrates the difference between text and bytes output.

Key Concepts:
- By default, subprocess returns bytes (binary data)
- text=True converts output to strings
- universal_newlines=True is an alias for text=True
- Bytes mode: result.stdout is bytes object
- Text mode: result.stdout is string object
- Text mode handles encoding automatically

When to use each:
- Text mode: For text output (most common)
- Bytes mode: For binary data, when you need raw bytes
"""

import subprocess
from typing import Union


# ============================================================================
# BYTES MODE (DEFAULT)
# ============================================================================

def demonstrate_bytes_mode() -> None:
    """
    By default, subprocess returns bytes.
    
    Output is a bytes object (b'...')
    """
    print("Running: echo 'Hello World'")
    
    result = subprocess.run(
        ["echo", "Hello World"],
        capture_output=True
        # No text=True, so returns bytes
    )
    
    print(f"\nType of stdout: {type(result.stdout)}")
    print(f"stdout: {result.stdout}")  # ← bytes object: b'Hello World\n'
    print(f"Is bytes: {isinstance(result.stdout, bytes)}")
    print(f"Is string: {isinstance(result.stdout, str)}")


# ============================================================================
# TEXT MODE
# ============================================================================

def demonstrate_text_mode() -> None:
    """
    Use text=True to get strings.
    
    Output is automatically decoded to string.
    """
    print("\n" + "=" * 70)
    print("TEXT MODE")
    print("=" * 70)
    
    result = subprocess.run(
        ["echo", "Hello World"],
        capture_output=True,
        text=True  # ← Convert to string
    )
    
    print(f"\nType of stdout: {type(result.stdout)}")
    print(f"stdout: {result.stdout}")  # ← string: 'Hello World\n'
    print(f"Is bytes: {isinstance(result.stdout, bytes)}")
    print(f"Is string: {isinstance(result.stdout, str)}")


# ============================================================================
# WORKING WITH BYTES
# ============================================================================

def work_with_bytes() -> None:
    """
    Working with bytes output.
    
    Need to decode manually to get string.
    """
    print("\n" + "=" * 70)
    print("WORKING WITH BYTES")
    print("=" * 70)
    
    result = subprocess.run(
        ["echo", "Hello World"],
        capture_output=True
    )
    
    # Output is bytes
    bytes_output = result.stdout
    print(f"\nBytes: {bytes_output}")
    
    # Decode to string
    string_output = bytes_output.decode('utf-8')  # ← Manual decode
    print(f"Decoded: {repr(string_output)}")
    
    # Can also use different encoding
    string_output2 = bytes_output.decode('ascii')
    print(f"ASCII decode: {repr(string_output2)}")


# ============================================================================
# WORKING WITH TEXT
# ============================================================================

def work_with_text() -> None:
    """
    Working with text output.
    
    Already a string, ready to use.
    """
    print("\n" + "=" * 70)
    print("WORKING WITH TEXT")
    print("=" * 70)
    
    result = subprocess.run(
        ["echo", "Hello World"],
        capture_output=True,
        text=True
    )
    
    # Output is already string
    output = result.stdout
    print(f"\nString: {repr(output)}")
    
    # Can use string methods directly
    print(f"Upper: {output.upper()}")
    print(f"Stripped: {repr(output.strip())}")
    print(f"Split: {output.split()}")


# ============================================================================
# COMPARISON
# ============================================================================

def compare_bytes_vs_text() -> None:
    """
    Side-by-side comparison of bytes vs text mode.
    """
    print("\n" + "=" * 70)
    print("BYTES VS TEXT COMPARISON")
    print("=" * 70)
    
    command = ["echo", "Hello World"]
    
    # Bytes mode
    bytes_result = subprocess.run(command, capture_output=True)
    print("\n1. Bytes mode:")
    print(f"   Type: {type(bytes_result.stdout)}")
    print(f"   Value: {bytes_result.stdout}")
    print(f"   Length: {len(bytes_result.stdout)} bytes")
    
    # Text mode
    text_result = subprocess.run(command, capture_output=True, text=True)
    print("\n2. Text mode:")
    print(f"   Type: {type(text_result.stdout)}")
    print(f"   Value: {repr(text_result.stdout)}")
    print(f"   Length: {len(text_result.stdout)} characters")


# ============================================================================
# WHEN TO USE EACH
# ============================================================================

def when_to_use_each() -> None:
    """
    Demonstrate when to use bytes vs text mode.
    """
    print("\n" + "=" * 70)
    print("WHEN TO USE EACH")
    print("=" * 70)
    
    print("\n✅ Use text=True (text mode):")
    print("   - Reading text output (most common)")
    print("   - Processing log files")
    print("   - Parsing command output")
    print("   - When you need string operations")
    print("   - For human-readable output")
    
    print("\n✅ Use bytes mode (default):")
    print("   - Reading binary files")
    print("   - Processing images, videos, etc.")
    print("   - When encoding is unknown")
    print("   - When you need exact byte values")
    print("   - For binary protocols")


# ============================================================================
# UNIVERSAL_NEWLINES ALIAS
# ============================================================================

def demonstrate_universal_newlines() -> None:
    """
    universal_newlines is an alias for text=True.
    
    Older code may use this parameter.
    """
    print("\n" + "=" * 70)
    print("UNIVERSAL_NEWLINES (ALIAS)")
    print("=" * 70)
    
    # These are equivalent:
    result1 = subprocess.run(
        ["echo", "Hello"],
        capture_output=True,
        text=True  # ← Modern way
    )
    
    result2 = subprocess.run(
        ["echo", "Hello"],
        capture_output=True,
        universal_newlines=True  # ← Old way (still works)
    )
    
    print(f"\ntext=True: {repr(result1.stdout)}")
    print(f"universal_newlines=True: {repr(result2.stdout)}")
    print(f"Are equal: {result1.stdout == result2.stdout}")


# ============================================================================
# DEMONSTRATION: Text vs Bytes
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TEXT MODE VS BYTES MODE")
    print("=" * 70)
    
    # Bytes mode
    print("\n" + "=" * 70)
    print("1. BYTES MODE (DEFAULT)")
    print("=" * 70)
    demonstrate_bytes_mode()
    
    # Text mode
    demonstrate_text_mode()
    
    # Working with bytes
    work_with_bytes()
    
    # Working with text
    work_with_text()
    
    # Comparison
    compare_bytes_vs_text()
    
    # When to use
    when_to_use_each()
    
    # Universal newlines
    demonstrate_universal_newlines()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Default mode returns bytes (binary data)")
    print("2. text=True converts output to strings")
    print("3. Bytes: b'Hello\\n', String: 'Hello\\n'")
    print("4. Text mode handles encoding automatically")
    print("5. Bytes need manual decode: bytes.decode('utf-8')")
    print("6. Use text=True for most text processing")
    print("7. Use bytes mode for binary data")
    print("8. universal_newlines=True is old alias for text=True")
    print("9. String methods work only in text mode")
    print("10. Check type with isinstance(output, bytes/str)")
    print("=" * 70)

