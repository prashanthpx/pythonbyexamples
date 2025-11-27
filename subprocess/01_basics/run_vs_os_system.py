"""
Example: subprocess.run() vs os.system()
Compares subprocess.run() with the older os.system().

Key Concepts:
- os.system() is the old way (deprecated for most uses)
- subprocess.run() is the modern, recommended way
- subprocess provides more control and safety
- os.system() uses shell (security risk)

Why use subprocess instead of os.system():
- Better error handling
- Capture output easily
- No shell injection vulnerabilities
- More control over execution
- Returns structured data
"""

import subprocess
import os
from typing import Tuple


# ============================================================================
# os.system() - THE OLD WAY
# ============================================================================

def demonstrate_os_system() -> None:
    """
    Demonstrate os.system() - the old way.
    
    Problems with os.system():
    - Always uses shell (security risk)
    - Can't capture output easily
    - Returns encoded exit status
    - Less control
    """
    print("Using os.system():")
    print("-" * 70)
    
    # Run command
    exit_status = os.system("echo 'Hello from os.system()'")
    
    print(f"\nReturn value: {exit_status}")
    print("Note: Can't capture output, it goes directly to terminal")
    
    # Try to list files
    print("\nListing files:")
    exit_status = os.system("ls -l /tmp | head -5")
    print(f"Exit status: {exit_status}")


# ============================================================================
# subprocess.run() - THE MODERN WAY
# ============================================================================

def demonstrate_subprocess_run() -> None:
    """
    Demonstrate subprocess.run() - the modern way.
    
    Advantages:
    - No shell by default (safer)
    - Easy output capture
    - Returns CompletedProcess object
    - Better error handling
    """
    print("\n" + "=" * 70)
    print("Using subprocess.run():")
    print("-" * 70)
    
    # Run command
    result = subprocess.run(
        ["echo", "Hello from subprocess.run()"],
        capture_output=True,
        text=True
    )
    
    print(f"Return code: {result.returncode}")
    print(f"Captured output: {repr(result.stdout)}")
    print("Note: Output is captured and can be processed")
    
    # List files
    print("\nListing files:")
    result = subprocess.run(
        ["ls", "-l", "/tmp"],
        capture_output=True,
        text=True
    )
    
    lines = result.stdout.split('\n')[:5]
    for line in lines:
        print(f"  {line}")
    
    print(f"\nReturn code: {result.returncode}")


# ============================================================================
# SIDE-BY-SIDE COMPARISON
# ============================================================================

def compare_side_by_side() -> None:
    """
    Compare os.system() and subprocess.run() side by side.
    """
    print("\n" + "=" * 70)
    print("SIDE-BY-SIDE COMPARISON")
    print("=" * 70)
    
    command = "echo 'Test message'"
    
    # os.system()
    print("\n1. os.system():")
    print(f"   Code: os.system(\"{command}\")")
    exit_code = os.system(command)
    print(f"   Return: {exit_code}")
    print("   Output: (printed directly, can't capture)")
    
    # subprocess.run()
    print("\n2. subprocess.run():")
    print(f"   Code: subprocess.run({command.split()})")
    result = subprocess.run(
        command.split(),
        capture_output=True,
        text=True
    )
    print(f"   Return: {result.returncode}")
    print(f"   Output: {repr(result.stdout)}")


# ============================================================================
# SECURITY COMPARISON
# ============================================================================

def demonstrate_security_difference() -> None:
    """
    Show security difference between os.system() and subprocess.run().
    
    os.system() always uses shell - dangerous!
    subprocess.run() doesn't use shell by default - safe!
    """
    print("\n" + "=" * 70)
    print("SECURITY COMPARISON")
    print("=" * 70)
    
    # Dangerous with os.system()
    print("\n1. os.system() - DANGEROUS:")
    print("   Command: echo 'hello' && echo 'injected!'")
    print("   (Shell interprets && as command separator)")
    os.system("echo 'hello' && echo 'injected!'")
    
    # Safe with subprocess.run()
    print("\n2. subprocess.run() - SAFE:")
    print("   Command: ['echo', 'hello && echo injected!']")
    print("   (No shell, && treated as literal text)")
    result = subprocess.run(
        ["echo", "hello && echo 'injected!'"],
        capture_output=True,
        text=True
    )
    print(f"   Output: {result.stdout.strip()}")
    print("   (The && is printed literally, not executed)")


# ============================================================================
# OUTPUT CAPTURE COMPARISON
# ============================================================================

def compare_output_capture() -> None:
    """
    Compare how to capture output with both methods.
    """
    print("\n" + "=" * 70)
    print("OUTPUT CAPTURE COMPARISON")
    print("=" * 70)
    
    # os.system() - difficult
    print("\n1. os.system() - Difficult:")
    print("   Need to redirect to file and read it")
    print("   Code: os.system('ls /tmp > /tmp/output.txt')")
    os.system("ls /tmp > /tmp/os_system_output.txt 2>&1")
    with open("/tmp/os_system_output.txt") as f:
        output = f.read()
    print(f"   Lines captured: {len(output.splitlines())}")
    os.remove("/tmp/os_system_output.txt")
    
    # subprocess.run() - easy
    print("\n2. subprocess.run() - Easy:")
    print("   Code: subprocess.run(['ls', '/tmp'], capture_output=True)")
    result = subprocess.run(
        ["ls", "/tmp"],
        capture_output=True,
        text=True
    )
    print(f"   Lines captured: {len(result.stdout.splitlines())}")
    print("   (Direct access to output, no temp files needed)")


# ============================================================================
# WHEN TO USE EACH
# ============================================================================

def when_to_use_each() -> None:
    """
    Explain when to use each method.
    """
    print("\n" + "=" * 70)
    print("WHEN TO USE EACH")
    print("=" * 70)
    
    print("\n✅ Use subprocess.run():")
    print("   - Almost always (it's the modern way)")
    print("   - When you need to capture output")
    print("   - When security matters")
    print("   - When you need error handling")
    print("   - For production code")
    
    print("\n⚠️  Use os.system():")
    print("   - Quick one-off scripts (not recommended)")
    print("   - Legacy code compatibility")
    print("   - When you specifically need shell features")
    print("   - (But consider subprocess.run(shell=True) instead)")
    
    print("\n❌ Never use os.system():")
    print("   - With user input (security risk!)")
    print("   - In production code")
    print("   - When you need output")


# ============================================================================
# DEMONSTRATION: subprocess.run() vs os.system()
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("subprocess.run() vs os.system()")
    print("=" * 70)
    
    # os.system()
    print("\n" + "=" * 70)
    print("1. os.system() - THE OLD WAY")
    print("=" * 70)
    demonstrate_os_system()
    
    # subprocess.run()
    demonstrate_subprocess_run()
    
    # Side by side
    compare_side_by_side()
    
    # Security
    demonstrate_security_difference()
    
    # Output capture
    compare_output_capture()
    
    # When to use
    when_to_use_each()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. subprocess.run() is the modern, recommended way")
    print("2. os.system() is deprecated for most uses")
    print("3. subprocess.run() is safer (no shell by default)")
    print("4. subprocess.run() makes output capture easy")
    print("5. os.system() always uses shell (security risk)")
    print("6. subprocess.run() returns structured CompletedProcess")
    print("7. os.system() returns encoded exit status")
    print("8. Use subprocess.run() for all new code")
    print("9. Never use os.system() with user input")
    print("10. subprocess provides better error handling")
    print("=" * 70)

