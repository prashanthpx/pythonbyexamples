"""
Example: Encoding Handling
Demonstrates how to handle different character encodings.

Key Concepts:
- encoding parameter specifies character encoding
- Default encoding is locale-dependent (usually UTF-8)
- errors parameter controls error handling
- Common encodings: utf-8, ascii, latin-1, cp1252
- Encoding errors can cause UnicodeDecodeError

Why encoding matters:
- Different systems use different encodings
- Non-ASCII characters need proper encoding
- Prevents UnicodeDecodeError
- Ensures correct character display
"""

import subprocess
import sys
from typing import Optional


# ============================================================================
# DEFAULT ENCODING
# ============================================================================

def demonstrate_default_encoding() -> None:
    """
    Show the default encoding used by subprocess.
    
    Usually UTF-8 on modern systems.
    """
    print("Default encoding:")
    
    # Get system default encoding
    default_encoding = sys.getdefaultencoding()
    print(f"  System default: {default_encoding}")
    
    # subprocess uses locale encoding by default
    import locale
    locale_encoding = locale.getpreferredencoding()
    print(f"  Locale encoding: {locale_encoding}")
    
    # Run command with text=True (uses default encoding)
    result = subprocess.run(
        ["echo", "Hello"],
        capture_output=True,
        text=True  # ← Uses default encoding
    )
    
    print(f"\nOutput: {repr(result.stdout)}")


# ============================================================================
# SPECIFYING ENCODING
# ============================================================================

def specify_encoding() -> None:
    """
    Explicitly specify encoding.
    
    Recommended for portability.
    """
    print("\n" + "=" * 70)
    print("SPECIFYING ENCODING")
    print("=" * 70)
    
    # UTF-8 encoding (recommended)
    result = subprocess.run(
        ["echo", "Hello 世界"],  # Chinese characters
        capture_output=True,
        text=True,
        encoding='utf-8'  # ← Explicit UTF-8
    )
    
    print(f"\nUTF-8 output: {result.stdout.strip()}")
    
    # ASCII encoding (will fail with non-ASCII)
    try:
        result = subprocess.run(
            ["echo", "Hello"],
            capture_output=True,
            text=True,
            encoding='ascii'  # ← ASCII only
        )
        print(f"ASCII output: {result.stdout.strip()}")
    except UnicodeDecodeError as e:
        print(f"ASCII error: {e}")


# ============================================================================
# HANDLING ENCODING ERRORS
# ============================================================================

def handle_encoding_errors() -> None:
    """
    Handle encoding errors with errors parameter.
    
    Options: 'strict', 'ignore', 'replace', 'backslashreplace'
    """
    print("\n" + "=" * 70)
    print("HANDLING ENCODING ERRORS")
    print("=" * 70)
    
    # Create a command that outputs non-ASCII
    command = ["echo", "Café"]
    
    # Strict (default) - raises exception
    print("\n1. errors='strict' (default):")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding='ascii',
            errors='strict'  # ← Raise exception on error
        )
        print(f"   Output: {result.stdout}")
    except UnicodeDecodeError as e:
        print(f"   Error: {type(e).__name__}")
    
    # Ignore - skip invalid characters
    print("\n2. errors='ignore':")
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding='ascii',
        errors='ignore'  # ← Skip invalid characters
    )
    print(f"   Output: {repr(result.stdout)}")
    
    # Replace - replace with ?
    print("\n3. errors='replace':")
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding='ascii',
        errors='replace'  # ← Replace with ?
    )
    print(f"   Output: {repr(result.stdout)}")
    
    # Backslashreplace - use escape sequences
    print("\n4. errors='backslashreplace':")
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding='ascii',
        errors='backslashreplace'  # ← Use \\xNN
    )
    print(f"   Output: {repr(result.stdout)}")


# ============================================================================
# COMMON ENCODINGS
# ============================================================================

def demonstrate_common_encodings() -> None:
    """
    Demonstrate common character encodings.
    """
    print("\n" + "=" * 70)
    print("COMMON ENCODINGS")
    print("=" * 70)
    
    text = "Hello"
    command = ["echo", text]
    
    encodings = ['utf-8', 'ascii', 'latin-1', 'utf-16']
    
    for enc in encodings:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding=enc
            )
            print(f"\n{enc:12s}: {repr(result.stdout.strip())}")
        except (UnicodeDecodeError, UnicodeEncodeError) as e:
            print(f"\n{enc:12s}: Error - {type(e).__name__}")


# ============================================================================
# BYTES VS ENCODING
# ============================================================================

def bytes_vs_encoding() -> None:
    """
    Compare bytes mode vs encoding parameter.
    """
    print("\n" + "=" * 70)
    print("BYTES VS ENCODING")
    print("=" * 70)
    
    command = ["echo", "Hello"]
    
    # Bytes mode - no encoding
    print("\n1. Bytes mode (no encoding):")
    result = subprocess.run(command, capture_output=True)
    print(f"   Type: {type(result.stdout)}")
    print(f"   Value: {result.stdout}")
    
    # Text mode with encoding
    print("\n2. Text mode with UTF-8:")
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    print(f"   Type: {type(result.stdout)}")
    print(f"   Value: {repr(result.stdout)}")


# ============================================================================
# DEMONSTRATION: Encoding Handling
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ENCODING HANDLING")
    print("=" * 70)
    
    # Default encoding
    print("\n" + "=" * 70)
    print("1. DEFAULT ENCODING")
    print("=" * 70)
    demonstrate_default_encoding()
    
    # Specifying encoding
    specify_encoding()
    
    # Handling errors
    handle_encoding_errors()
    
    # Common encodings
    demonstrate_common_encodings()
    
    # Bytes vs encoding
    bytes_vs_encoding()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Default encoding is locale-dependent (usually UTF-8)")
    print("2. Use encoding='utf-8' for explicit UTF-8")
    print("3. errors parameter controls error handling")
    print("4. errors='strict': Raise exception (default)")
    print("5. errors='ignore': Skip invalid characters")
    print("6. errors='replace': Replace with ?")
    print("7. errors='backslashreplace': Use escape sequences")
    print("8. Common encodings: utf-8, ascii, latin-1")
    print("9. Always specify encoding for portability")
    print("10. Use bytes mode if encoding is unknown")
    print("=" * 70)

