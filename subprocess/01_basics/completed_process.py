"""
Example: CompletedProcess Object
Demonstrates the object returned by subprocess.run().

Key Concepts:
- subprocess.run() returns CompletedProcess instance
- Contains: args, returncode, stdout, stderr
- Provides information about completed process
- Can be inspected after execution

CompletedProcess attributes:
- args: The command that was run
- returncode: Exit status
- stdout: Captured standard output (if requested)
- stderr: Captured standard error (if requested)
"""

import subprocess
from subprocess import CompletedProcess


# ============================================================================
# BASIC CompletedProcess
# ============================================================================

def inspect_completed_process() -> None:
    """
    Inspect the CompletedProcess object returned by run().
    
    Shows all available attributes.
    """
    print("Running: echo 'Hello World'")
    
    result = subprocess.run(["echo", "Hello World"])  # ← Returns CompletedProcess
    
    print(f"\nType: {type(result)}")
    print(f"Class: {result.__class__.__name__}")
    
    print("\nAttributes:")
    print(f"  args: {result.args}")  # ← Command that was run
    print(f"  returncode: {result.returncode}")  # ← Exit status
    print(f"  stdout: {result.stdout}")  # ← None (not captured)
    print(f"  stderr: {result.stderr}")  # ← None (not captured)


# ============================================================================
# CAPTURING OUTPUT IN CompletedProcess
# ============================================================================

def capture_output_in_result() -> None:
    """
    Capture output and inspect in CompletedProcess.
    
    Use capture_output=True to get stdout/stderr.
    """
    print("\n" + "=" * 70)
    print("CAPTURING OUTPUT")
    print("=" * 70)
    
    result = subprocess.run(
        ["echo", "Hello World"],
        capture_output=True,  # ← Capture stdout and stderr
        text=True             # ← Return as string (not bytes)
    )
    
    print(f"\nargs: {result.args}")
    print(f"returncode: {result.returncode}")
    print(f"stdout: {repr(result.stdout)}")  # ← Now contains output
    print(f"stderr: {repr(result.stderr)}")  # ← Empty for this command


# ============================================================================
# USING CompletedProcess ATTRIBUTES
# ============================================================================

def use_completed_process_attributes() -> None:
    """
    Demonstrate using CompletedProcess attributes.
    
    Shows practical usage of the returned object.
    """
    print("\n" + "=" * 70)
    print("USING ATTRIBUTES")
    print("=" * 70)
    
    # Run command
    result = subprocess.run(
        ["ls", "-lh", "/tmp"],
        capture_output=True,
        text=True
    )
    
    # Check if successful
    if result.returncode == 0:
        print("✅ Command succeeded!")
        print(f"\nCommand was: {' '.join(result.args)}")
        print(f"\nOutput ({len(result.stdout)} characters):")
        print(result.stdout[:200])  # First 200 chars
        if len(result.stdout) > 200:
            print("...")
    else:
        print("❌ Command failed!")
        print(f"Error: {result.stderr}")


# ============================================================================
# COMPARING RESULTS
# ============================================================================

def compare_successful_and_failed() -> None:
    """
    Compare CompletedProcess for success vs failure.
    
    Shows difference in attributes.
    """
    print("\n" + "=" * 70)
    print("SUCCESS VS FAILURE")
    print("=" * 70)
    
    # Successful command
    print("\n1. Successful command:")
    success = subprocess.run(
        ["echo", "Success!"],
        capture_output=True,
        text=True
    )
    print(f"  returncode: {success.returncode}")
    print(f"  stdout: {repr(success.stdout)}")
    print(f"  stderr: {repr(success.stderr)}")
    
    # Failed command
    print("\n2. Failed command:")
    failure = subprocess.run(
        ["ls", "/nonexistent"],
        capture_output=True,
        text=True
    )
    print(f"  returncode: {failure.returncode}")
    print(f"  stdout: {repr(failure.stdout)}")
    print(f"  stderr: {repr(failure.stderr)}")  # ← Error message here


# ============================================================================
# STORING AND REUSING RESULTS
# ============================================================================

def store_and_reuse_results() -> None:
    """
    Store CompletedProcess objects for later use.
    
    Useful for comparing multiple command results.
    """
    print("\n" + "=" * 70)
    print("STORING RESULTS")
    print("=" * 70)
    
    # Run multiple commands and store results
    results = []
    
    commands = [
        ["echo", "First"],
        ["echo", "Second"],
        ["echo", "Third"]
    ]
    
    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True)
        results.append(result)
    
    # Process results later
    print("\nStored results:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {' '.join(result.args)}: {result.stdout.strip()}")


# ============================================================================
# CHECKING SPECIFIC ATTRIBUTES
# ============================================================================

def check_specific_attributes() -> None:
    """
    Check specific attributes for decision making.
    """
    print("\n" + "=" * 70)
    print("ATTRIBUTE-BASED DECISIONS")
    print("=" * 70)
    
    result = subprocess.run(
        ["python3", "--version"],
        capture_output=True,
        text=True
    )
    
    # Decision based on returncode
    if result.returncode == 0:
        print("✅ Python is installed")
        # Note: Python --version outputs to stderr
        version = result.stderr.strip() or result.stdout.strip()
        print(f"   Version: {version}")
    else:
        print("❌ Python not found")
    
    # Check if output contains specific text
    result2 = subprocess.run(
        ["echo", "Hello World"],
        capture_output=True,
        text=True
    )
    
    if "World" in result2.stdout:
        print("\n✅ Output contains 'World'")
    
    # Check output length
    if len(result2.stdout) > 0:
        print(f"✅ Output is not empty ({len(result2.stdout)} chars)")


# ============================================================================
# DEMONSTRATION: CompletedProcess
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("COMPLETEDPROCESS OBJECT")
    print("=" * 70)
    
    # Basic inspection
    print("\n" + "=" * 70)
    print("1. BASIC INSPECTION")
    print("=" * 70)
    inspect_completed_process()
    
    # Capturing output
    capture_output_in_result()
    
    # Using attributes
    use_completed_process_attributes()
    
    # Success vs failure
    compare_successful_and_failed()
    
    # Storing results
    store_and_reuse_results()
    
    # Attribute-based decisions
    check_specific_attributes()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. subprocess.run() returns CompletedProcess object")
    print("2. Attributes: args, returncode, stdout, stderr")
    print("3. args: The command that was executed")
    print("4. returncode: Exit status (0 = success)")
    print("5. stdout/stderr: None unless capture_output=True")
    print("6. Use text=True to get strings instead of bytes")
    print("7. Can store and reuse CompletedProcess objects")
    print("8. Inspect attributes for decision making")
    print("=" * 70)

