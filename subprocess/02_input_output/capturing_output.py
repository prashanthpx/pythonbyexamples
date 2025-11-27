"""
Example: Capturing Output
Demonstrates how to capture stdout and stderr from commands.

Key Concepts:
- capture_output=True captures both stdout and stderr
- stdout=subprocess.PIPE captures only stdout
- stderr=subprocess.PIPE captures only stderr
- By default, output goes to terminal (not captured)
- Captured output is available in CompletedProcess object

Why capture output:
- Process command results in Python
- Parse command output
- Log command output
- Check for specific patterns
- Suppress output from user
"""

import subprocess
from typing import Optional


# ============================================================================
# BASIC OUTPUT CAPTURE
# ============================================================================

def capture_basic_output() -> None:
    """
    Capture output using capture_output=True.
    
    This is the simplest way to capture both stdout and stderr.
    """
    print("Running: echo 'Hello World'")
    
    result = subprocess.run(
        ["echo", "Hello World"],
        capture_output=True,  # ← Capture both stdout and stderr
        text=True             # ← Return as string
    )
    
    print(f"\nReturn code: {result.returncode}")
    print(f"Stdout: {repr(result.stdout)}")
    print(f"Stderr: {repr(result.stderr)}")


def without_capture() -> None:
    """
    Without capture_output, output goes to terminal.
    
    stdout and stderr will be None.
    """
    print("\n" + "=" * 70)
    print("WITHOUT CAPTURE")
    print("=" * 70)
    
    print("\nRunning: echo 'This goes to terminal'")
    result = subprocess.run(["echo", "This goes to terminal"])
    
    print(f"\nstdout: {result.stdout}")  # ← None
    print(f"stderr: {result.stderr}")    # ← None


# ============================================================================
# CAPTURING STDOUT ONLY
# ============================================================================

def capture_stdout_only() -> None:
    """
    Capture only stdout, let stderr go to terminal.
    
    Use stdout=subprocess.PIPE for more control.
    """
    print("\n" + "=" * 70)
    print("CAPTURE STDOUT ONLY")
    print("=" * 70)
    
    result = subprocess.run(
        ["ls", "-lh", "/tmp"],
        stdout=subprocess.PIPE,  # ← Capture stdout only
        text=True
    )
    
    print(f"\nCaptured {len(result.stdout)} characters")
    print(f"First 100 chars: {result.stdout[:100]}")
    print(f"stderr: {result.stderr}")  # ← None (not captured)


# ============================================================================
# CAPTURING STDERR ONLY
# ============================================================================

def capture_stderr_only() -> None:
    """
    Capture only stderr, let stdout go to terminal.
    
    Useful for capturing error messages.
    """
    print("\n" + "=" * 70)
    print("CAPTURE STDERR ONLY")
    print("=" * 70)
    
    # This command outputs to stderr
    result = subprocess.run(
        ["ls", "/nonexistent_directory"],
        stderr=subprocess.PIPE,  # ← Capture stderr only
        text=True
    )
    
    print(f"\nstdout: {result.stdout}")  # ← None (not captured)
    print(f"stderr: {repr(result.stderr)}")  # ← Error message


# ============================================================================
# CAPTURING BOTH SEPARATELY
# ============================================================================

def capture_both_separately() -> None:
    """
    Capture stdout and stderr separately.
    
    More control than capture_output=True.
    """
    print("\n" + "=" * 70)
    print("CAPTURE BOTH SEPARATELY")
    print("=" * 70)
    
    result = subprocess.run(
        ["python3", "--version"],
        stdout=subprocess.PIPE,  # ← Capture stdout
        stderr=subprocess.PIPE,  # ← Capture stderr
        text=True
    )
    
    print(f"stdout: {repr(result.stdout)}")
    print(f"stderr: {repr(result.stderr)}")
    # Note: Python --version outputs to stderr!


# ============================================================================
# PROCESSING CAPTURED OUTPUT
# ============================================================================

def process_captured_output() -> None:
    """
    Process captured output in various ways.
    
    Shows common patterns for working with output.
    """
    print("\n" + "=" * 70)
    print("PROCESSING CAPTURED OUTPUT")
    print("=" * 70)
    
    # Capture directory listing
    result = subprocess.run(
        ["ls", "-l", "/tmp"],
        capture_output=True,
        text=True
    )
    
    # Split into lines
    lines = result.stdout.splitlines()
    print(f"\n1. Total lines: {len(lines)}")
    
    # Filter lines
    py_files = [line for line in lines if '.py' in line]
    print(f"2. Python files: {len(py_files)}")
    
    # Strip whitespace
    clean_output = result.stdout.strip()
    print(f"3. Output length (stripped): {len(clean_output)}")
    
    # Check for patterns
    if "total" in result.stdout:
        print("4. Output contains 'total'")
    
    # Get first/last lines
    if lines:
        print(f"5. First line: {lines[0][:50]}...")


# ============================================================================
# DEMONSTRATION: Capturing Output
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CAPTURING OUTPUT")
    print("=" * 70)
    
    # Basic capture
    print("\n" + "=" * 70)
    print("1. BASIC OUTPUT CAPTURE")
    print("=" * 70)
    capture_basic_output()
    
    # Without capture
    without_capture()
    
    # Stdout only
    capture_stdout_only()
    
    # Stderr only
    capture_stderr_only()
    
    # Both separately
    capture_both_separately()
    
    # Processing output
    process_captured_output()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. capture_output=True captures both stdout and stderr")
    print("2. stdout=subprocess.PIPE captures only stdout")
    print("3. stderr=subprocess.PIPE captures only stderr")
    print("4. Without capture, output goes to terminal")
    print("5. Use text=True to get strings instead of bytes")
    print("6. Captured output is in result.stdout and result.stderr")
    print("7. Process output with splitlines(), strip(), etc.")
    print("8. Check patterns with 'in' operator")
    print("9. Filter lines with list comprehensions")
    print("10. Always check returncode before processing output")
    print("=" * 70)

