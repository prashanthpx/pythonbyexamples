"""
Example: File Redirection
Demonstrates redirecting input/output to/from files.

Key Concepts:
- Redirect stdout to file
- Redirect stderr to file
- Read stdin from file
- Append vs overwrite
- File handles and modes

Redirection types:
- stdout > file: Write output to file
- stderr > file: Write errors to file
- stdin < file: Read input from file
- stdout >> file: Append to file
"""

import subprocess
import os
import tempfile
from typing import Optional


# ============================================================================
# REDIRECT STDOUT TO FILE
# ============================================================================

def redirect_stdout_to_file() -> None:
    """
    Redirect stdout to a file.
    
    Equivalent to: echo "Hello" > output.txt
    """
    print("Redirect stdout to file:")
    
    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        output_file = f.name
    
    try:
        # Open file for writing
        with open(output_file, 'w') as f:
            subprocess.run(
                ["echo", "Hello World"],
                stdout=f  # ← Redirect stdout to file
            )
        
        # Read the file
        with open(output_file, 'r') as f:
            content = f.read()
        
        print(f"File content: {content.strip()}")
    finally:
        os.unlink(output_file)


# ============================================================================
# REDIRECT STDERR TO FILE
# ============================================================================

def redirect_stderr_to_file() -> None:
    """
    Redirect stderr to a file.
    
    Capture error messages separately.
    """
    print("\n" + "=" * 70)
    print("REDIRECT STDERR TO FILE")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        error_file = f.name
    
    try:
        # Command that produces error
        with open(error_file, 'w') as f:
            result = subprocess.run(
                ["ls", "/nonexistent"],
                stderr=f,  # ← Redirect stderr to file
                stdout=subprocess.PIPE
            )
        
        # Read error file
        with open(error_file, 'r') as f:
            errors = f.read()
        
        print(f"Return code: {result.returncode}")
        print(f"Errors written to file: {bool(errors)}")
        if errors:
            print(f"Error content: {errors.strip()}")
    finally:
        os.unlink(error_file)


# ============================================================================
# REDIRECT STDIN FROM FILE
# ============================================================================

def redirect_stdin_from_file() -> None:
    """
    Read stdin from a file.
    
    Equivalent to: wc -l < input.txt
    """
    print("\n" + "=" * 70)
    print("REDIRECT STDIN FROM FILE")
    print("=" * 70)
    
    # Create input file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        input_file = f.name
        f.write("Line 1\nLine 2\nLine 3\n")
    
    try:
        # Open file for reading
        with open(input_file, 'r') as f:
            result = subprocess.run(
                ["wc", "-l"],
                stdin=f,  # ← Read stdin from file
                capture_output=True,
                text=True
            )
        
        print(f"Line count: {result.stdout.strip()}")
    finally:
        os.unlink(input_file)


# ============================================================================
# APPEND TO FILE
# ============================================================================

def append_to_file() -> None:
    """
    Append output to a file.
    
    Equivalent to: echo "text" >> file.txt
    """
    print("\n" + "=" * 70)
    print("APPEND TO FILE")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        output_file = f.name
    
    try:
        # First write
        with open(output_file, 'w') as f:
            subprocess.run(["echo", "First line"], stdout=f)
        
        # Append
        with open(output_file, 'a') as f:  # ← 'a' for append
            subprocess.run(["echo", "Second line"], stdout=f)
            subprocess.run(["echo", "Third line"], stdout=f)
        
        # Read file
        with open(output_file, 'r') as f:
            content = f.read()
        
        print("File content:")
        print(content)
    finally:
        os.unlink(output_file)


# ============================================================================
# REDIRECT BOTH STDOUT AND STDERR
# ============================================================================

def redirect_both_streams() -> None:
    """
    Redirect both stdout and stderr to files.
    
    Separate output and errors.
    """
    print("\n" + "=" * 70)
    print("REDIRECT BOTH STREAMS")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        stdout_file = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        stderr_file = f.name
    
    try:
        # Run command with both redirections
        with open(stdout_file, 'w') as out_f, open(stderr_file, 'w') as err_f:
            subprocess.run(
                ["sh", "-c", "echo 'output' && echo 'error' >&2"],
                stdout=out_f,  # ← Redirect stdout
                stderr=err_f   # ← Redirect stderr
            )
        
        # Read both files
        with open(stdout_file, 'r') as f:
            stdout_content = f.read()
        
        with open(stderr_file, 'r') as f:
            stderr_content = f.read()
        
        print(f"Stdout: {stdout_content.strip()}")
        print(f"Stderr: {stderr_content.strip()}")
    finally:
        os.unlink(stdout_file)
        os.unlink(stderr_file)


# ============================================================================
# REDIRECT TO DEVNULL
# ============================================================================

def redirect_to_devnull() -> None:
    """
    Discard output by redirecting to /dev/null.

    Suppress unwanted output.
    """
    print("\n" + "=" * 70)
    print("REDIRECT TO DEVNULL")
    print("=" * 70)

    # Suppress stdout
    print("1. Suppress stdout:")
    result = subprocess.run(
        ["echo", "This will be discarded"],
        stdout=subprocess.DEVNULL  # ← Discard stdout
    )
    print(f"   Return code: {result.returncode}")

    # Suppress stderr
    print("\n2. Suppress stderr:")
    result = subprocess.run(
        ["ls", "/nonexistent"],
        stderr=subprocess.DEVNULL  # ← Discard stderr
    )
    print(f"   Return code: {result.returncode}")

    # Suppress both
    print("\n3. Suppress both:")
    result = subprocess.run(
        ["sh", "-c", "echo 'out' && echo 'err' >&2"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"   Return code: {result.returncode}")


# ============================================================================
# FILE REDIRECTION WITH POPEN
# ============================================================================

def file_redirection_with_popen() -> None:
    """
    Use file redirection with Popen.

    More control over file handling.
    """
    print("\n" + "=" * 70)
    print("FILE REDIRECTION WITH POPEN")
    print("=" * 70)

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        output_file = f.name

    try:
        # Open file
        with open(output_file, 'w') as f:
            # Start process with file redirection
            process = subprocess.Popen(
                ["echo", "Hello from Popen"],
                stdout=f
            )

            # Wait for completion
            process.wait()

        # Read result
        with open(output_file, 'r') as f:
            content = f.read()

        print(f"File content: {content.strip()}")
        print(f"Return code: {process.returncode}")
    finally:
        os.unlink(output_file)


# ============================================================================
# DEMONSTRATION: File Redirection
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("FILE REDIRECTION")
    print("=" * 70)

    # Redirect stdout
    print("\n" + "=" * 70)
    print("1. REDIRECT STDOUT TO FILE")
    print("=" * 70)
    redirect_stdout_to_file()

    # Redirect stderr
    redirect_stderr_to_file()

    # Redirect stdin
    redirect_stdin_from_file()

    # Append
    append_to_file()

    # Both streams
    redirect_both_streams()

    # Devnull
    redirect_to_devnull()

    # With Popen
    file_redirection_with_popen()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Use file handle for stdout/stderr/stdin")
    print("2. Open file with 'w' to write, 'a' to append")
    print("3. Open file with 'r' for stdin input")
    print("4. subprocess.DEVNULL discards output")
    print("5. Can redirect stdout and stderr separately")
    print("6. Use context managers for file handling")
    print("7. Works with both run() and Popen()")
    print("8. Always close files properly")
    print("9. Use tempfile for temporary files")
    print("10. Check return codes even with redirection")
    print("=" * 70)

