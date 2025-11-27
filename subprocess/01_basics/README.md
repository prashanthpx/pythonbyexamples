# 01. Subprocess Basics

[← Back to Subprocess](../subprocess.md) | [Next: Input/Output →](../02_input_output/)

> **Level**: 🟢 Beginner  
> **Estimated Time**: 2 hours  
> **Prerequisites**: Basic Python syntax, basic command-line knowledge

---

## 📚 Table of Contents

1. [Introduction](#1-introduction)
2. [subprocess.run() Basics](#2-subprocessrun-basics)
3. [Return Codes](#3-return-codes)
4. [CompletedProcess Object](#4-completedprocess-object)
5. [subprocess vs os.system](#5-subprocess-vs-ossystem)
6. [Summary](#6-summary)

---

## 1. Introduction

The `subprocess` module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. It's the modern, recommended way to execute external commands from Python.

### Why Use subprocess?

| Use Case | Example |
|----------|---------|
| **Run system commands** | Execute `ls`, `grep`, `git`, etc. |
| **Automate tasks** | Backup scripts, deployment automation |
| **Integrate tools** | Call external programs from Python |
| **Process data** | Pipe data through command-line tools |

### Key Concepts

- **subprocess.run()**: The recommended high-level interface (Python 3.5+)
- **Synchronous execution**: Waits for command to complete
- **Return codes**: 0 = success, non-zero = failure
- **CompletedProcess**: Object containing execution results

---

## 2. subprocess.run() Basics

**File**: [`basic_run.py`](basic_run.py)

### 2.1. Simple Command Execution

**File**: [`basic_run.py`](basic_run.py) - Line 27

```python
import subprocess

# Run a simple command
subprocess.run(["ls", "-l"])

# Key points:
# - Command as list of strings
# - First element is the command
# - Remaining elements are arguments
# - Waits for completion
```

### 🔑 Command Format

**Always use list format** (recommended):

```python
# ✅ Correct - list format
subprocess.run(["echo", "Hello World"])
subprocess.run(["ls", "-l", "-h", "/tmp"])
subprocess.run(["git", "status"])

# ❌ Avoid - string format (requires shell=True)
subprocess.run("echo Hello World", shell=True)  # Security risk!
```

### 2.2. Why List Format?

**File**: [`basic_run.py`](basic_run.py) - Line 70

```python
# List format handles special characters safely
command = ["echo", "Hello & Goodbye"]
subprocess.run(command)
# Output: Hello & Goodbye

# The & is treated as literal text, not a shell operator
```

### 2.3. Common Commands

**File**: [`basic_run.py`](basic_run.py) - Line 115

```python
# List files
subprocess.run(["ls", "-lh"])

# Print working directory
subprocess.run(["pwd"])

# Show date
subprocess.run(["date"])

# Echo message
subprocess.run(["echo", "Hello from Python!"])
```

### 💡 Best Practices

1. **Use list format** for commands (safer)
2. **Use full paths** when possible: `["/bin/echo", "hello"]`
3. **Avoid shell=True** unless absolutely necessary
4. **Check return codes** to detect failures
5. **Capture output** when you need to process it

---

## 3. Return Codes

**File**: [`return_codes.py`](return_codes.py)

### 3.1. What is a Return Code?

Every command returns an exit status:
- **0**: Success
- **Non-zero**: Failure (different codes mean different errors)

### 3.2. Manual Return Code Checking

**File**: [`return_codes.py`](return_codes.py) - Line 24

```python
result = subprocess.run(["ls", "/tmp"])

if result.returncode == 0:
    print("✅ Command succeeded!")
else:
    print(f"❌ Command failed with code {result.returncode}")
```

### 3.3. Using check=True

**File**: [`return_codes.py`](return_codes.py) - Line 56

```python
try:
    subprocess.run(
        ["ls", "/nonexistent"],
        check=True  # ← Raises CalledProcessError if returncode != 0
    )
except subprocess.CalledProcessError as e:
    print(f"Command failed with return code {e.returncode}")
```

### 🔑 check=True Benefits

1. **Automatic error detection** - No manual checking needed
2. **Exception-based flow** - Use try/except for error handling
3. **Cleaner code** - Less boilerplate
4. **Recommended** for most use cases

### 3.4. Common Return Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse of command |
| 126 | Command cannot execute |
| 127 | Command not found |
| 130 | Terminated by Ctrl+C |

### 💡 Return Code Best Practices

1. **Always check return codes** in production code
2. **Use check=True** for automatic error handling
3. **Handle CalledProcessError** with try/except
4. **Log failures** for debugging
5. **Different commands** may use different error codes

---

## 4. CompletedProcess Object

**File**: [`completed_process.py`](completed_process.py)

### 4.1. What is CompletedProcess?

`subprocess.run()` returns a `CompletedProcess` instance containing:

| Attribute | Description |
|-----------|-------------|
| `args` | The command that was run |
| `returncode` | Exit status (0 = success) |
| `stdout` | Captured standard output (if requested) |
| `stderr` | Captured standard error (if requested) |

### 4.2. Inspecting CompletedProcess

**File**: [`completed_process.py`](completed_process.py) - Line 24

```python
result = subprocess.run(["echo", "Hello"])

print(result.args)        # ['echo', 'Hello']
print(result.returncode)  # 0
print(result.stdout)      # None (not captured)
print(result.stderr)      # None (not captured)
```

### 4.3. Capturing Output

**File**: [`completed_process.py`](completed_process.py) - Line 44

```python
result = subprocess.run(
    ["echo", "Hello World"],
    capture_output=True,  # ← Capture stdout and stderr
    text=True             # ← Return as string (not bytes)
)

print(result.stdout)  # 'Hello World\n'
print(result.stderr)  # ''
```

### 🔑 capture_output vs text

```python
# Without capture_output
result = subprocess.run(["echo", "hello"])
# stdout/stderr: None (output goes to terminal)

# With capture_output=True
result = subprocess.run(["echo", "hello"], capture_output=True)
# stdout: b'hello\n' (bytes)

# With capture_output=True and text=True
result = subprocess.run(["echo", "hello"], capture_output=True, text=True)
# stdout: 'hello\n' (string)
```

### 4.4. Using CompletedProcess Attributes

**File**: [`completed_process.py`](completed_process.py) - Line 64

```python
result = subprocess.run(
    ["ls", "-lh", "/tmp"],
    capture_output=True,
    text=True
)

# Check success
if result.returncode == 0:
    print(f"Command: {' '.join(result.args)}")
    print(f"Output:\n{result.stdout}")
else:
    print(f"Error: {result.stderr}")
```

### 💡 CompletedProcess Best Practices

1. **Use capture_output=True** to get stdout/stderr
2. **Use text=True** for string output (easier to work with)
3. **Check returncode** before processing output
4. **Store results** for later processing
5. **Access stderr** for error messages

---

## 5. subprocess vs os.system

**File**: [`run_vs_os_system.py`](run_vs_os_system.py)

### 5.1. Why Not os.system()?

`os.system()` is the old way and has several problems:

| Issue | os.system() | subprocess.run() |
|-------|-------------|------------------|
| **Shell usage** | Always uses shell | No shell by default |
| **Security** | ⚠️ Shell injection risk | ✅ Safe |
| **Output capture** | ❌ Difficult | ✅ Easy |
| **Return value** | Encoded exit status | CompletedProcess object |
| **Error handling** | ❌ Limited | ✅ Comprehensive |
| **Recommended** | ❌ No | ✅ Yes |

### 5.2. Security Comparison

**File**: [`run_vs_os_system.py`](run_vs_os_system.py) - Line 103

```python
# ⚠️ DANGEROUS with os.system()
os.system("echo 'hello' && echo 'injected!'")
# Output: hello
#         injected!
# The && is interpreted as command separator!

# ✅ SAFE with subprocess.run()
subprocess.run(["echo", "hello && echo 'injected!'"])
# Output: hello && echo 'injected!'
# The && is treated as literal text
```

### 5.3. Output Capture Comparison

**File**: [`run_vs_os_system.py`](run_vs_os_system.py) - Line 127

```python
# ❌ os.system() - Difficult
os.system("ls /tmp > /tmp/output.txt")
with open("/tmp/output.txt") as f:
    output = f.read()
# Need temp file!

# ✅ subprocess.run() - Easy
result = subprocess.run(
    ["ls", "/tmp"],
    capture_output=True,
    text=True
)
output = result.stdout
# Direct access!
```

### 5.4. When to Use Each

**File**: [`run_vs_os_system.py`](run_vs_os_system.py) - Line 157

```python
# ✅ Use subprocess.run():
# - Almost always (it's the modern way)
# - When you need to capture output
# - When security matters
# - For production code

# ⚠️ Use os.system():
# - Quick one-off scripts (not recommended)
# - Legacy code compatibility
# - (But consider subprocess.run(shell=True) instead)

# ❌ Never use os.system():
# - With user input (security risk!)
# - In production code
# - When you need output
```

### 💡 Migration Guide

```python
# Old way (os.system)
import os
os.system("ls -l")

# New way (subprocess.run)
import subprocess
subprocess.run(["ls", "-l"])

# Old way with output
os.system("ls -l > output.txt")
with open("output.txt") as f:
    output = f.read()

# New way with output
result = subprocess.run(["ls", "-l"], capture_output=True, text=True)
output = result.stdout
```

---

## 6. Summary

### What You Learned

✅ **subprocess.run()** is the modern, recommended way
✅ **Command format**: Use list `["cmd", "arg1", "arg2"]`
✅ **Return codes**: 0 = success, non-zero = failure
✅ **check=True**: Auto-raise exception on failure
✅ **CompletedProcess**: Contains args, returncode, stdout, stderr
✅ **capture_output=True**: Capture stdout/stderr
✅ **text=True**: Get strings instead of bytes
✅ **subprocess > os.system**: Safer, more powerful

### Key Takeaways

1. **Always use subprocess.run()** for new code
2. **Pass commands as lists** for safety
3. **Check return codes** to detect failures
4. **Use check=True** for automatic error handling
5. **Capture output** with capture_output=True
6. **Avoid shell=True** unless necessary
7. **Never use os.system()** with user input

### Quick Reference

```python
import subprocess

# Basic execution
subprocess.run(["ls", "-l"])

# With error checking
subprocess.run(["ls", "-l"], check=True)

# Capture output
result = subprocess.run(
    ["ls", "-l"],
    capture_output=True,
    text=True,
    check=True
)
print(result.stdout)

# Handle errors
try:
    subprocess.run(["ls", "/nonexistent"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Failed with code {e.returncode}")
```

---

## 📝 Practice Exercises

### Exercise 1: Basic Execution
Write a script that runs `date` and `whoami` commands.

### Exercise 2: Return Code Checking
Write a function that checks if a directory exists using `ls` and return codes.

### Exercise 3: Output Capture
Write a script that captures the output of `ls -l` and counts the number of files.

### Exercise 4: Error Handling
Write a script that tries to list a non-existent directory and handles the error gracefully.

---

## ✅ Self-Assessment Checklist

Before moving to the next topic, make sure you can:

- [ ] Execute a simple command with subprocess.run()
- [ ] Pass arguments to commands correctly
- [ ] Check return codes manually
- [ ] Use check=True for automatic error handling
- [ ] Capture command output
- [ ] Access CompletedProcess attributes
- [ ] Explain why subprocess is better than os.system()
- [ ] Handle CalledProcessError exceptions
- [ ] Use text=True to get string output
- [ ] Write safe subprocess code

---

## 🔗 Navigation

- [← Back to Subprocess](../subprocess.md)
- [Next: Input/Output →](../02_input_output/)

---

## 📚 Additional Resources

- [Python subprocess Documentation](https://docs.python.org/3/library/subprocess.html)
- [PEP 324 - subprocess module](https://peps.python.org/pep-0324/)
- [subprocess.run() Documentation](https://docs.python.org/3/library/subprocess.html#subprocess.run)

---

**Files in this section**:
- [`basic_run.py`](basic_run.py) - Basic subprocess.run() usage
- [`return_codes.py`](return_codes.py) - Return code handling
- [`completed_process.py`](completed_process.py) - CompletedProcess object
- [`run_vs_os_system.py`](run_vs_os_system.py) - Comparison with os.system()

**Next**: [02. Input/Output →](../02_input_output/)
