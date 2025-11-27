"""
Example: Advanced Redirection
Demonstrates complex redirection patterns.

Key Concepts:
- Multiple file descriptors
- Bidirectional communication
- Tee-like behavior (split output)
- Dynamic redirection
- Context-based redirection

Advanced patterns:
- Read from multiple sources
- Write to multiple destinations
- Conditional redirection
- Logging and monitoring
"""

import subprocess
import tempfile
import os
from typing import Optional, TextIO


# ============================================================================
# BIDIRECTIONAL COMMUNICATION
# ============================================================================

def bidirectional_communication() -> None:
    """
    Two-way communication with a process.
    
    Send input and receive output interactively.
    """
    print("Bidirectional communication:")
    
    # Start interactive process
    process = subprocess.Popen(
        ["cat"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    
    # Send data
    if process.stdin:
        process.stdin.write("Hello\n")
        process.stdin.write("World\n")
        process.stdin.close()
    
    # Read response
    if process.stdout:
        output = process.stdout.read()
        print(f"Received: {output.strip()}")
    
    process.wait()


# ============================================================================
# TEE-LIKE BEHAVIOR
# ============================================================================

def tee_like_behavior() -> None:
    """
    Split output to multiple destinations.
    
    Like Unix 'tee' command: write to file AND stdout.
    """
    print("\n" + "=" * 70)
    print("TEE-LIKE BEHAVIOR")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        output_file = f.name
    
    try:
        # Run command and capture output
        result = subprocess.run(
            ["echo", "This goes to both file and stdout"],
            capture_output=True,
            text=True
        )
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write(result.stdout)
        
        # Also print to stdout
        print(f"To stdout: {result.stdout.strip()}")
        
        # Verify file
        with open(output_file, 'r') as f:
            file_content = f.read()
        print(f"To file: {file_content.strip()}")
    finally:
        os.unlink(output_file)


# ============================================================================
# CONDITIONAL REDIRECTION
# ============================================================================

def conditional_redirection() -> None:
    """
    Redirect based on conditions.
    
    Different redirection based on success/failure.
    """
    print("\n" + "=" * 70)
    print("CONDITIONAL REDIRECTION")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        success_file = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        error_file = f.name
    
    try:
        # Run command
        result = subprocess.run(
            ["echo", "Success!"],
            capture_output=True,
            text=True
        )
        
        # Redirect based on return code
        if result.returncode == 0:
            with open(success_file, 'w') as f:
                f.write(result.stdout)
            print("✅ Output written to success file")
        else:
            with open(error_file, 'w') as f:
                f.write(result.stderr)
            print("❌ Errors written to error file")
        
        # Show file content
        with open(success_file, 'r') as f:
            content = f.read()
        if content:
            print(f"Success file: {content.strip()}")
    finally:
        os.unlink(success_file)
        os.unlink(error_file)


# ============================================================================
# LOGGING WRAPPER
# ============================================================================

def logging_wrapper() -> None:
    """
    Wrap command execution with logging.
    
    Log all input/output to file.
    """
    print("\n" + "=" * 70)
    print("LOGGING WRAPPER")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        log_file = f.name
    
    try:
        # Open log file
        with open(log_file, 'w') as log:
            # Log command
            command = ["echo", "Test command"]
            log.write(f"Command: {' '.join(command)}\n")
            log.write("-" * 40 + "\n")
            
            # Run command
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )
            
            # Log output
            log.write(f"stdout:\n{result.stdout}")
            log.write(f"stderr:\n{result.stderr}")
            log.write(f"Return code: {result.returncode}\n")
        
        # Show log
        with open(log_file, 'r') as log:
            print("Log file content:")
            print(log.read())
    finally:
        os.unlink(log_file)


# ============================================================================
# MULTIPLE INPUT SOURCES
# ============================================================================

def multiple_input_sources() -> None:
    """
    Combine input from multiple sources.
    
    Merge data from different sources.
    """
    print("\n" + "=" * 70)
    print("MULTIPLE INPUT SOURCES")
    print("=" * 70)
    
    # Create temp files
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        file1 = f.name
        f.write("Data from file 1\n")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        file2 = f.name
        f.write("Data from file 2\n")
    
    try:
        # Combine files
        result = subprocess.run(
            ["cat", file1, file2],
            capture_output=True,
            text=True
        )
        
        print("Combined output:")
        print(result.stdout)
    finally:
        os.unlink(file1)
        os.unlink(file2)


# ============================================================================
# DYNAMIC REDIRECTION
# ============================================================================

def dynamic_redirection() -> None:
    """
    Choose redirection target dynamically.

    Redirect based on runtime conditions.
    """
    print("\n" + "=" * 70)
    print("DYNAMIC REDIRECTION")
    print("=" * 70)

    # Condition
    verbose = True

    # Choose redirection
    if verbose:
        stderr_target = None  # Show on console
    else:
        stderr_target = subprocess.DEVNULL  # Suppress

    # Run command
    result = subprocess.run(
        ["sh", "-c", "echo 'output' && echo 'error' >&2"],
        stdout=subprocess.PIPE,
        stderr=stderr_target,
        text=True
    )

    print(f"stdout: {result.stdout.strip()}")
    if verbose:
        print("(stderr shown on console)")
    else:
        print("(stderr suppressed)")


# ============================================================================
# PIPELINE WITH FILE CHECKPOINTS
# ============================================================================

def pipeline_with_checkpoints() -> None:
    """
    Save intermediate results in pipeline.

    Checkpoint data at each stage.
    """
    print("\n" + "=" * 70)
    print("PIPELINE WITH CHECKPOINTS")
    print("=" * 70)

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='_stage1.txt') as f:
        stage1_file = f.name

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='_stage2.txt') as f:
        stage2_file = f.name

    try:
        # Stage 1: Generate data
        p1 = subprocess.Popen(
            ["echo", "apple\nbanana\ncherry"],
            stdout=subprocess.PIPE,
            text=True
        )

        # Save stage 1 output
        if p1.stdout:
            stage1_output = p1.stdout.read()
            with open(stage1_file, 'w') as f:
                f.write(stage1_output)

        p1.wait()

        # Stage 2: Sort (read from checkpoint)
        with open(stage1_file, 'r') as f:
            p2 = subprocess.Popen(
                ["sort"],
                stdin=f,
                stdout=subprocess.PIPE,
                text=True
            )

            # Save stage 2 output
            if p2.stdout:
                stage2_output = p2.stdout.read()
                with open(stage2_file, 'w') as f2:
                    f2.write(stage2_output)

        p2.wait()

        # Show checkpoints
        print("Stage 1 checkpoint:")
        with open(stage1_file, 'r') as f:
            print(f.read())

        print("Stage 2 checkpoint:")
        with open(stage2_file, 'r') as f:
            print(f.read())
    finally:
        os.unlink(stage1_file)
        os.unlink(stage2_file)


# ============================================================================
# DEMONSTRATION: Advanced Redirection
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ADVANCED REDIRECTION")
    print("=" * 70)

    # Bidirectional
    print("\n" + "=" * 70)
    print("1. BIDIRECTIONAL COMMUNICATION")
    print("=" * 70)
    bidirectional_communication()

    # Tee-like
    tee_like_behavior()

    # Conditional
    conditional_redirection()

    # Logging
    logging_wrapper()

    # Multiple sources
    multiple_input_sources()

    # Dynamic
    dynamic_redirection()

    # Checkpoints
    pipeline_with_checkpoints()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Bidirectional communication with stdin/stdout")
    print("2. Split output to multiple destinations (tee)")
    print("3. Conditional redirection based on results")
    print("4. Wrap commands with logging")
    print("5. Combine input from multiple sources")
    print("6. Dynamic redirection based on conditions")
    print("7. Save pipeline checkpoints for debugging")
    print("8. Use file handles for flexible redirection")
    print("9. Context managers ensure proper cleanup")
    print("10. Advanced patterns enable complex workflows")
    print("=" * 70)

