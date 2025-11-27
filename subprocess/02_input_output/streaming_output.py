"""
Example: Real-time Output Streaming
Demonstrates how to process output line-by-line in real-time.

Key Concepts:
- subprocess.run() waits for completion (no streaming)
- subprocess.Popen() allows real-time processing
- Read from process.stdout line by line
- Useful for long-running commands
- Monitor progress in real-time

Why streaming:
- Process output as it's generated
- Show progress to user
- Handle large output efficiently
- Don't wait for completion
- Monitor long-running processes
"""

import subprocess
import time
from typing import Iterator, Optional


# ============================================================================
# NON-STREAMING (subprocess.run)
# ============================================================================

def non_streaming_example() -> None:
    """
    subprocess.run() waits for completion.
    
    All output comes at once, no streaming.
    """
    print("Non-streaming (subprocess.run):")
    print("Waiting for command to complete...")
    
    result = subprocess.run(
        ["python3", "-c", "import time; [print(i) or time.sleep(0.5) for i in range(5)]"],
        capture_output=True,
        text=True
    )
    
    print("Command completed!")
    print(f"Output:\n{result.stdout}")


# ============================================================================
# BASIC STREAMING (subprocess.Popen)
# ============================================================================

def basic_streaming() -> None:
    """
    Use Popen for real-time output streaming.
    
    Read output line by line as it's generated.
    """
    print("\n" + "=" * 70)
    print("BASIC STREAMING (subprocess.Popen)")
    print("=" * 70)
    
    print("\nStreaming output:")
    
    # Start process
    process = subprocess.Popen(
        ["python3", "-c", "import time; [print(f'Line {i}') or time.sleep(0.5) for i in range(5)]"],
        stdout=subprocess.PIPE,  # ← Capture stdout
        text=True                # ← Text mode
    )
    
    # Read line by line
    if process.stdout:
        for line in process.stdout:
            print(f"  Received: {line.strip()}")
    
    # Wait for completion
    process.wait()
    print("Streaming complete!")


# ============================================================================
# STREAMING WITH PROGRESS
# ============================================================================

def streaming_with_progress() -> None:
    """
    Show progress while streaming output.
    
    Useful for long-running commands.
    """
    print("\n" + "=" * 70)
    print("STREAMING WITH PROGRESS")
    print("=" * 70)
    
    print("\nProcessing with progress:")
    
    # Simulate a command that outputs progress
    command = [
        "python3", "-c",
        "import time; [print(f'Processing item {i}/10') or time.sleep(0.3) for i in range(1, 11)]"
    ]
    
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        text=True
    )
    
    # Stream and show progress
    if process.stdout:
        for line in process.stdout:
            print(f"  {line.strip()}")
    
    process.wait()
    print("✅ Processing complete!")


# ============================================================================
# STREAMING AND FILTERING
# ============================================================================

def streaming_and_filtering() -> None:
    """
    Filter output while streaming.
    
    Process only relevant lines.
    """
    print("\n" + "=" * 70)
    print("STREAMING AND FILTERING")
    print("=" * 70)
    
    print("\nFiltering output (only errors):")
    
    # Command that outputs mixed messages
    command = [
        "python3", "-c",
        """
import time
messages = [
    'INFO: Starting',
    'DEBUG: Step 1',
    'ERROR: Something failed',
    'INFO: Continuing',
    'ERROR: Another error',
    'INFO: Done'
]
for msg in messages:
    print(msg)
    time.sleep(0.2)
"""
    ]
    
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        text=True
    )
    
    # Filter for ERROR lines
    if process.stdout:
        for line in process.stdout:
            if 'ERROR' in line:
                print(f"  ⚠️  {line.strip()}")
    
    process.wait()


# ============================================================================
# STREAMING WITH TIMEOUT
# ============================================================================

def streaming_with_timeout() -> None:
    """
    Stream output with timeout.
    
    Stop if process takes too long.
    """
    print("\n" + "=" * 70)
    print("STREAMING WITH TIMEOUT")
    print("=" * 70)
    
    print("\nStreaming with 3-second timeout:")
    
    # Long-running command
    command = [
        "python3", "-c",
        "import time; [print(f'Line {i}') or time.sleep(1) for i in range(10)]"
    ]
    
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        text=True
    )
    
    try:
        # Read with timeout
        if process.stdout:
            for line in process.stdout:
                print(f"  {line.strip()}")
        
        # Wait with timeout
        process.wait(timeout=3)  # ← 3 second timeout
        
    except subprocess.TimeoutExpired:
        print("  ⏱️  Timeout! Killing process...")
        process.kill()
        process.wait()


# ============================================================================
# STREAMING BOTH STDOUT AND STDERR
# ============================================================================

def streaming_both_streams() -> None:
    """
    Stream both stdout and stderr.
    
    Note: This is simplified; real implementation needs threading.
    """
    print("\n" + "=" * 70)
    print("STREAMING STDOUT AND STDERR")
    print("=" * 70)
    
    print("\nStreaming both streams:")
    
    # Command that outputs to both
    command = [
        "python3", "-c",
        """
import sys, time
print('STDOUT: Line 1')
print('STDERR: Error 1', file=sys.stderr)
time.sleep(0.3)
print('STDOUT: Line 2')
print('STDERR: Error 2', file=sys.stderr)
"""
    ]
    
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Read stdout
    if process.stdout:
        for line in process.stdout:
            print(f"  OUT: {line.strip()}")
    
    process.wait()
    
    # Read stderr after completion
    if process.stderr:
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"  ERR: {stderr_output.strip()}")


# ============================================================================
# DEMONSTRATION: Streaming Output
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("REAL-TIME OUTPUT STREAMING")
    print("=" * 70)
    
    # Non-streaming
    print("\n" + "=" * 70)
    print("1. NON-STREAMING (subprocess.run)")
    print("=" * 70)
    non_streaming_example()
    
    # Basic streaming
    basic_streaming()
    
    # With progress
    streaming_with_progress()
    
    # With filtering
    streaming_and_filtering()
    
    # With timeout
    streaming_with_timeout()
    
    # Both streams
    streaming_both_streams()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. subprocess.run() waits for completion (no streaming)")
    print("2. subprocess.Popen() enables real-time streaming")
    print("3. Read from process.stdout line by line")
    print("4. Use for long-running commands")
    print("5. Show progress to users in real-time")
    print("6. Filter output while streaming")
    print("7. Use timeout to prevent hanging")
    print("8. process.wait() waits for completion")
    print("9. Streaming is more memory efficient")
    print("10. For both streams, consider threading")
    print("=" * 70)

