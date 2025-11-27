"""
Example: Basic subprocess.run()
Demonstrates the fundamental way to execute commands using subprocess.

Key Concepts:
- subprocess.run() is the recommended way (Python 3.5+)
- Executes command and waits for completion
- Returns CompletedProcess object
- Simple, high-level interface

When to use subprocess.run():
- When you need to run a command and wait for it to finish
- When you want a simple, synchronous execution
- For most common subprocess use cases
"""

import subprocess
from typing import List


# ============================================================================
# BASIC COMMAND EXECUTION
# ============================================================================

def run_simple_command() -> None:
    """
    Execute a simple command with subprocess.run().
    
    The most basic usage - just run a command.
    """
    print("Running: ls -l")
    
    # Run command - waits for completion
    subprocess.run(["ls", "-l"])  # ← Command as list of strings
    
    print("\nCommand completed!")


def run_with_arguments() -> None:
    """
    Execute command with multiple arguments.
    
    Important: Pass command and arguments as a list.
    """
    print("Running: echo with multiple arguments")
    
    # Each argument is a separate list element
    subprocess.run([
        "echo",      # ← Command
        "Hello",     # ← Argument 1
        "World",     # ← Argument 2
        "from",      # ← Argument 3
        "Python!"    # ← Argument 4
    ])


def run_command_with_path() -> None:
    """
    Execute command with full path.
    
    Using full path is more explicit and secure.
    """
    print("\nRunning: /bin/echo with full path")
    
    # Use full path to executable
    subprocess.run(["/bin/echo", "Using full path"])  # ← Full path


# ============================================================================
# COMMAND AS LIST VS STRING
# ============================================================================

def demonstrate_list_format() -> None:
    """
    Demonstrate why command should be a list.
    
    List format is safer and more explicit.
    """
    print("\n" + "=" * 70)
    print("COMMAND AS LIST (RECOMMENDED)")
    print("=" * 70)
    
    # Correct way: command as list
    command = ["echo", "Hello World"]
    print(f"Command: {command}")
    subprocess.run(command)
    
    # With special characters
    command_with_special = ["echo", "Hello & Goodbye"]
    print(f"\nCommand with special chars: {command_with_special}")
    subprocess.run(command_with_special)  # ← Handles special chars safely


# ============================================================================
# CHECKING IF COMMAND EXISTS
# ============================================================================

def check_command_exists(command: str) -> bool:
    """
    Check if a command exists on the system.
    
    Args:
        command: Command name to check
        
    Returns:
        True if command exists
    """
    try:
        # Try to run with --version or --help
        subprocess.run(
            [command, "--version"],
            capture_output=True,  # ← Don't show output
            check=False           # ← Don't raise exception
        )
        return True
    except FileNotFoundError:
        return False


# ============================================================================
# COMMON COMMANDS
# ============================================================================

def run_common_commands() -> None:
    """Demonstrate running common system commands."""
    
    print("\n" + "=" * 70)
    print("COMMON COMMANDS")
    print("=" * 70)
    
    # List files
    print("\n1. List files (ls):")
    subprocess.run(["ls", "-lh"])
    
    # Print working directory
    print("\n2. Print working directory (pwd):")
    subprocess.run(["pwd"])
    
    # Date and time
    print("\n3. Current date (date):")
    subprocess.run(["date"])
    
    # Echo
    print("\n4. Echo message:")
    subprocess.run(["echo", "subprocess.run() is easy!"])


# ============================================================================
# DEMONSTRATION: Basic subprocess.run()
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("BASIC SUBPROCESS.RUN()")
    print("=" * 70)
    
    # Basic execution
    print("\n" + "=" * 70)
    print("1. SIMPLE COMMAND EXECUTION")
    print("=" * 70)
    run_simple_command()
    
    # With arguments
    print("\n" + "=" * 70)
    print("2. COMMAND WITH ARGUMENTS")
    print("=" * 70)
    run_with_arguments()
    
    # With full path
    run_command_with_path()
    
    # List format
    demonstrate_list_format()
    
    # Common commands
    run_common_commands()

    # Check command exists
    print("\n" + "=" * 70)
    print("5. CHECK IF COMMAND EXISTS")
    print("=" * 70)

    commands_to_check = ["python3", "git", "nonexistent_command"]
    for cmd in commands_to_check:
        exists = check_command_exists(cmd)
        status = "✅ Found" if exists else "❌ Not found"
        print(f"  {cmd}: {status}")

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. subprocess.run() is the recommended way (Python 3.5+)")
    print("2. Pass command as list: ['command', 'arg1', 'arg2']")
    print("3. subprocess.run() waits for command to complete")
    print("4. Returns CompletedProcess object")
    print("5. Use full paths for security: ['/bin/echo', 'hello']")
    print("6. List format handles special characters safely")
    print("7. Simple and synchronous - good for most use cases")
    print("=" * 70)

