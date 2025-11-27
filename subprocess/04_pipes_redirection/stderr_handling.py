"""
Example: stderr Handling
Demonstrates handling stderr in various ways.

Key Concepts:
- Separate stdout and stderr
- Combine stdout and stderr
- Redirect stderr to stdout
- Suppress stderr
- Process errors separately

stderr uses:
- Error messages
- Warnings
- Diagnostic information
- Debug output
- Progress information
"""

import subprocess
from typing import Tuple


# ============================================================================
# SEPARATE STDOUT AND STDERR
# ============================================================================

def separate_stdout_stderr() -> None:
    """
    Capture stdout and stderr separately.
    
    Process output and errors independently.
    """
    print("Separate stdout and stderr:")
    
    result = subprocess.run(
        ["sh", "-c", "echo 'output' && echo 'error' >&2"],
        capture_output=True,  # ← Captures both
        text=True
    )
    
    print(f"stdout: {result.stdout.strip()}")
    print(f"stderr: {result.stderr.strip()}")
    print(f"Return code: {result.returncode}")


# ============================================================================
# COMBINE STDOUT AND STDERR
# ============================================================================

def combine_stdout_stderr() -> None:
    """
    Combine stderr into stdout.
    
    Equivalent to: command 2>&1
    """
    print("\n" + "=" * 70)
    print("COMBINE STDOUT AND STDERR")
    print("=" * 70)
    
    result = subprocess.run(
        ["sh", "-c", "echo 'output' && echo 'error' >&2"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # ← Redirect stderr to stdout
        text=True
    )
    
    print("Combined output:")
    print(result.stdout)


# ============================================================================
# REDIRECT STDERR TO STDOUT IN PIPE
# ============================================================================

def redirect_stderr_in_pipe() -> None:
    """
    Redirect stderr to stdout in a pipeline.
    
    Process both streams together.
    """
    print("\n" + "=" * 70)
    print("REDIRECT STDERR IN PIPE")
    print("=" * 70)
    
    # First process with combined output
    p1 = subprocess.Popen(
        ["sh", "-c", "echo 'out' && echo 'err' >&2"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # ← Combine streams
        text=True
    )
    
    # Second process receives both
    p2 = subprocess.Popen(
        ["cat"],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        text=True
    )
    
    if p1.stdout:
        p1.stdout.close()
    
    output, _ = p2.communicate()
    
    print("Combined output from pipeline:")
    print(output)


# ============================================================================
# SUPPRESS STDERR
# ============================================================================

def suppress_stderr() -> None:
    """
    Suppress stderr output.
    
    Discard error messages.
    """
    print("\n" + "=" * 70)
    print("SUPPRESS STDERR")
    print("=" * 70)
    
    # Command that produces error
    print("Running command that produces error...")
    result = subprocess.run(
        ["ls", "/nonexistent"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,  # ← Suppress stderr
        text=True
    )
    
    print(f"Return code: {result.returncode}")
    print(f"stdout: {result.stdout}")
    print("(stderr was suppressed)")


# ============================================================================
# PROCESS STDERR SEPARATELY
# ============================================================================

def process_stderr_separately() -> None:
    """
    Process stderr separately from stdout.
    
    Handle errors differently.
    """
    print("\n" + "=" * 70)
    print("PROCESS STDERR SEPARATELY")
    print("=" * 70)
    
    result = subprocess.run(
        ["sh", "-c", "echo 'Success' && echo 'Warning: low memory' >&2"],
        capture_output=True,
        text=True
    )
    
    # Process stdout
    if result.stdout:
        print("✅ Output:")
        print(f"   {result.stdout.strip()}")
    
    # Process stderr
    if result.stderr:
        print("⚠️  Warnings/Errors:")
        print(f"   {result.stderr.strip()}")


# ============================================================================
# STDERR IN PIPELINE
# ============================================================================

def stderr_in_pipeline() -> None:
    """
    Handle stderr in multi-stage pipeline.
    
    Each stage can have its own errors.
    """
    print("\n" + "=" * 70)
    print("STDERR IN PIPELINE")
    print("=" * 70)
    
    # Stage 1
    p1 = subprocess.Popen(
        ["sh", "-c", "echo 'data' && echo 'warning from p1' >&2"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Stage 2
    p2 = subprocess.Popen(
        ["cat"],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    if p1.stdout:
        p1.stdout.close()
    
    # Get outputs
    p2_out, p2_err = p2.communicate()
    p1.wait()
    
    # Get p1 stderr
    p1_err = p1.stderr.read() if p1.stderr else ""
    
    print(f"Stage 1 stderr: {p1_err.strip()}")
    print(f"Stage 2 stdout: {p2_out.strip()}")
    print(f"Stage 2 stderr: {p2_err.strip()}")


# ============================================================================
# CHECK STDERR FOR ERRORS
# ============================================================================

def check_stderr_for_errors() -> None:
    """
    Check stderr to detect errors.

    Use stderr content to determine success.
    """
    print("\n" + "=" * 70)
    print("CHECK STDERR FOR ERRORS")
    print("=" * 70)

    result = subprocess.run(
        ["sh", "-c", "echo 'output' && echo 'ERROR: failed' >&2"],
        capture_output=True,
        text=True
    )

    # Check for errors in stderr
    if "ERROR" in result.stderr:
        print("❌ Error detected in stderr:")
        print(f"   {result.stderr.strip()}")
    else:
        print("✅ No errors")

    print(f"stdout: {result.stdout.strip()}")


# ============================================================================
# FILTER STDERR
# ============================================================================

def filter_stderr() -> None:
    """
    Filter stderr output.

    Process only specific error messages.
    """
    print("\n" + "=" * 70)
    print("FILTER STDERR")
    print("=" * 70)

    result = subprocess.run(
        ["sh", "-c", "echo 'INFO: starting' >&2 && echo 'ERROR: failed' >&2 && echo 'WARNING: slow' >&2"],
        capture_output=True,
        text=True
    )

    # Filter stderr lines
    stderr_lines = result.stderr.strip().split('\n')

    errors = [line for line in stderr_lines if 'ERROR' in line]
    warnings = [line for line in stderr_lines if 'WARNING' in line]
    info = [line for line in stderr_lines if 'INFO' in line]

    print("Errors:")
    for err in errors:
        print(f"  ❌ {err}")

    print("\nWarnings:")
    for warn in warnings:
        print(f"  ⚠️  {warn}")

    print("\nInfo:")
    for inf in info:
        print(f"  ℹ️  {inf}")


# ============================================================================
# DEMONSTRATION: stderr Handling
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("STDERR HANDLING")
    print("=" * 70)

    # Separate
    print("\n" + "=" * 70)
    print("1. SEPARATE STDOUT AND STDERR")
    print("=" * 70)
    separate_stdout_stderr()

    # Combine
    combine_stdout_stderr()

    # Redirect in pipe
    redirect_stderr_in_pipe()

    # Suppress
    suppress_stderr()

    # Process separately
    process_stderr_separately()

    # Pipeline
    stderr_in_pipeline()

    # Check for errors
    check_stderr_for_errors()

    # Filter
    filter_stderr()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. capture_output=True captures both stdout and stderr")
    print("2. stderr=subprocess.STDOUT combines streams")
    print("3. stderr=subprocess.DEVNULL suppresses errors")
    print("4. Process stdout and stderr separately")
    print("5. Check stderr for error detection")
    print("6. Filter stderr by error level")
    print("7. Each pipeline stage has its own stderr")
    print("8. Use stderr for diagnostics and errors")
    print("9. Can redirect stderr to stdout in pipes")
    print("10. Always handle stderr appropriately")
    print("=" * 70)

