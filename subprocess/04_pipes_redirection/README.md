# 04. Pipes and Redirection

[← Back to Subprocess](../subprocess.md) | [Previous: Advanced Execution](../03_advanced_execution/) | [Next: Process Control →](../05_process_control/)

> **Level**: 🟡 Intermediate  
> **Estimated Time**: 2.5 hours  
> **Prerequisites**: 01. Basics, 02. Input/Output, 03. Advanced Execution

---

## 📚 Table of Contents

1. [Introduction](#1-introduction)
2. [Basic Piping](#2-basic-piping)
3. [File Redirection](#3-file-redirection)
4. [Command Pipelines](#4-command-pipelines)
5. [stderr Handling](#5-stderr-handling)
6. [Advanced Redirection](#6-advanced-redirection)
7. [Summary](#7-summary)

---

## 1. Introduction

Pipes and redirection are fundamental concepts for connecting processes and managing data flow. You'll learn:
- Connecting processes with pipes
- Redirecting input/output to files
- Building multi-stage pipelines
- Handling stdout and stderr
- Advanced redirection patterns

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Pipe** | Connect stdout of one process to stdin of another |
| **Redirection** | Send output to files or read input from files |
| **Pipeline** | Chain of processes connected by pipes |
| **stdout** | Standard output stream |
| **stderr** | Standard error stream |

---

## 2. Basic Piping

**File**: [`basic_piping.py`](basic_piping.py)

### 2.1. Simple Pipe

**File**: [`basic_piping.py`](basic_piping.py) - Line 27

```python
import subprocess

# First process: echo
p1 = subprocess.Popen(
    ["echo", "Hello World"],
    stdout=subprocess.PIPE  # ← Capture output for piping
)

# Second process: wc (word count)
p2 = subprocess.Popen(
    ["wc", "-w"],
    stdin=p1.stdout,  # ← Use p1's output as input
    stdout=subprocess.PIPE
)

# Close p1's stdout in parent
if p1.stdout:
    p1.stdout.close()  # ← Allow p1 to receive SIGPIPE

# Get final output
output, _ = p2.communicate()

print(f"Word count: {output.decode().strip()}")
```

**Equivalent shell command**: `echo "Hello World" | wc -w`

### 2.2. Why Close p1.stdout?

Closing `p1.stdout` in the parent process is important:
- Allows `p1` to receive SIGPIPE if `p2` exits
- Prevents deadlocks
- Proper resource management
- Follows Unix pipe semantics

### 2.3. Multiple Pipes

**File**: [`basic_piping.py`](basic_piping.py) - Line 97

```python
# Process 1: echo
p1 = subprocess.Popen(
    ["echo", "apple\nbanana\napple\ncherry\nbanana"],
    stdout=subprocess.PIPE
)

# Process 2: sort
p2 = subprocess.Popen(
    ["sort"],
    stdin=p1.stdout,
    stdout=subprocess.PIPE
)

if p1.stdout:
    p1.stdout.close()

# Process 3: uniq
p3 = subprocess.Popen(
    ["uniq"],
    stdin=p2.stdout,
    stdout=subprocess.PIPE,
    text=True
)

if p2.stdout:
    p2.stdout.close()

output, _ = p3.communicate()
```

**Equivalent shell command**: `echo "..." | sort | uniq`

### 💡 Piping Best Practices

1. **Use subprocess.PIPE** for stdout of source process
2. **Connect stdin** of destination to stdout of source
3. **Close stdout** after connecting to next process
4. **Use text=True** for string processing
5. **Check return codes** of all processes
6. **Handle errors** at each stage

---

## 3. File Redirection

**File**: [`file_redirection.py`](file_redirection.py)

### 3.1. Redirect stdout to File

**File**: [`file_redirection.py`](file_redirection.py) - Line 27

```python
# Open file for writing
with open('output.txt', 'w') as f:
    subprocess.run(
        ["echo", "Hello World"],
        stdout=f  # ← Redirect stdout to file
    )

# Read the file
with open('output.txt', 'r') as f:
    content = f.read()
```

**Equivalent shell command**: `echo "Hello World" > output.txt`

### 3.2. Redirect stderr to File

**File**: [`file_redirection.py`](file_redirection.py) - Line 59

```python
# Command that produces error
with open('error.txt', 'w') as f:
    result = subprocess.run(
        ["ls", "/nonexistent"],
        stderr=f,  # ← Redirect stderr to file
        stdout=subprocess.PIPE
    )
```

### 3.3. Redirect stdin from File

**File**: [`file_redirection.py`](file_redirection.py) - Line 93

```python
# Open file for reading
with open('input.txt', 'r') as f:
    result = subprocess.run(
        ["wc", "-l"],
        stdin=f,  # ← Read stdin from file
        capture_output=True,
        text=True
    )
```

**Equivalent shell command**: `wc -l < input.txt`

### 3.4. Append to File

**File**: [`file_redirection.py`](file_redirection.py) - Line 125

```python
# First write
with open('output.txt', 'w') as f:
    subprocess.run(["echo", "First line"], stdout=f)

# Append
with open('output.txt', 'a') as f:  # ← 'a' for append
    subprocess.run(["echo", "Second line"], stdout=f)
```

**Equivalent shell command**: `echo "Second line" >> output.txt`

### 3.5. Redirect to /dev/null

**File**: [`file_redirection.py`](file_redirection.py) - Line 219

```python
# Suppress stdout
result = subprocess.run(
    ["echo", "This will be discarded"],
    stdout=subprocess.DEVNULL  # ← Discard stdout
)

# Suppress stderr
result = subprocess.run(
    ["ls", "/nonexistent"],
    stderr=subprocess.DEVNULL  # ← Discard stderr
)
```

### 🔑 File Redirection Modes

| Mode | Description | Shell Equivalent |
|------|-------------|------------------|
| `'w'` | Write (overwrite) | `>` |
| `'a'` | Append | `>>` |
| `'r'` | Read | `<` |
| `subprocess.DEVNULL` | Discard | `> /dev/null` |

---

## 4. Command Pipelines

**File**: [`command_pipelines.py`](command_pipelines.py)

### 4.1. Three-Stage Pipeline

**File**: [`command_pipelines.py`](command_pipelines.py) - Line 29

```python
# Stage 1: Generate data
p1 = subprocess.Popen(
    ["echo", "apple\nbanana\napple\ncherry"],
    stdout=subprocess.PIPE
)

# Stage 2: Sort
p2 = subprocess.Popen(
    ["sort"],
    stdin=p1.stdout,
    stdout=subprocess.PIPE
)

if p1.stdout:
    p1.stdout.close()

# Stage 3: Get unique items
p3 = subprocess.Popen(
    ["uniq"],
    stdin=p2.stdout,
    stdout=subprocess.PIPE
)

if p2.stdout:
    p2.stdout.close()

# Stage 4: Count lines
p4 = subprocess.Popen(
    ["wc", "-l"],
    stdin=p3.stdout,
    stdout=subprocess.PIPE,
    text=True
)

if p3.stdout:
    p3.stdout.close()

# Get result
output, _ = p4.communicate()
```

**Equivalent shell command**: `echo "..." | sort | uniq | wc -l`

### 4.2. Pipeline Builder Function

**File**: [`command_pipelines.py`](command_pipelines.py) - Line 135

```python
def build_pipeline(commands: List[List[str]], input_data: Optional[str] = None) -> str:
    """Build a pipeline from a list of commands."""
    processes = []

    # Create first process
    first_process = subprocess.Popen(
        commands[0],
        stdin=subprocess.PIPE if input_data else None,
        stdout=subprocess.PIPE,
        text=True
    )
    processes.append(first_process)

    # Create middle processes
    for cmd in commands[1:]:
        prev_process = processes[-1]
        process = subprocess.Popen(
            cmd,
            stdin=prev_process.stdout,
            stdout=subprocess.PIPE,
            text=True
        )
        processes.append(process)

        # Close previous stdout
        if prev_process.stdout:
            prev_process.stdout.close()

    # Send input data if provided
    if input_data and first_process.stdin:
        first_process.stdin.write(input_data)
        first_process.stdin.close()

    # Get output from last process
    output, _ = processes[-1].communicate()

    return output

# Usage
commands = [
    ["sort"],
    ["uniq"],
    ["wc", "-l"]
]
data = "apple\nbanana\napple\ncherry\n"
result = build_pipeline(commands, data)
```

### 4.3. Pipeline Error Handling

**File**: [`command_pipelines.py`](command_pipelines.py) - Line 223

```python
# Stage 1
p1 = subprocess.Popen(
    ["echo", "test data"],
    stdout=subprocess.PIPE
)

# Stage 2
p2 = subprocess.Popen(
    ["grep", "data"],
    stdin=p1.stdout,
    stdout=subprocess.PIPE,
    text=True
)

if p1.stdout:
    p1.stdout.close()

# Get output
output, _ = p2.communicate()

# Wait for all processes
p1.wait()

# Check return codes
if p1.returncode == 0 and p2.returncode == 0:
    print(f"✅ Pipeline succeeded: {output.strip()}")
else:
    print("❌ Pipeline failed!")
```

### 💡 Pipeline Best Practices

1. **Close stdout** after connecting to next process
2. **Check return codes** of all stages
3. **Build reusable** pipeline functions
4. **Handle errors** at each stage
5. **Use text=True** for string processing
6. **Wait for all processes** to complete

---

## 5. stderr Handling

**File**: [`stderr_handling.py`](stderr_handling.py)

### 5.1. Separate stdout and stderr

**File**: [`stderr_handling.py`](stderr_handling.py) - Line 27

```python
result = subprocess.run(
    ["sh", "-c", "echo 'output' && echo 'error' >&2"],
    capture_output=True,  # ← Captures both
    text=True
)

print(f"stdout: {result.stdout.strip()}")
print(f"stderr: {result.stderr.strip()}")
```

### 5.2. Combine stdout and stderr

**File**: [`stderr_handling.py`](stderr_handling.py) - Line 51

```python
result = subprocess.run(
    ["sh", "-c", "echo 'output' && echo 'error' >&2"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,  # ← Redirect stderr to stdout
    text=True
)

print("Combined output:")
print(result.stdout)
```

**Equivalent shell command**: `command 2>&1`

### 5.3. Suppress stderr

**File**: [`stderr_handling.py`](stderr_handling.py) - Line 103

```python
# Command that produces error
result = subprocess.run(
    ["ls", "/nonexistent"],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,  # ← Suppress stderr
    text=True
)
```

**Equivalent shell command**: `command 2>/dev/null`

### 5.4. Process stderr Separately

**File**: [`stderr_handling.py`](stderr_handling.py) - Line 129

```python
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
```

### 5.5. Filter stderr by Level

**File**: [`stderr_handling.py`](stderr_handling.py) - Line 253

```python
result = subprocess.run(
    ["sh", "-c", "echo 'INFO: starting' >&2 && echo 'ERROR: failed' >&2"],
    capture_output=True,
    text=True
)

# Filter stderr lines
stderr_lines = result.stderr.strip().split('\n')

errors = [line for line in stderr_lines if 'ERROR' in line]
warnings = [line for line in stderr_lines if 'WARNING' in line]
info = [line for line in stderr_lines if 'INFO' in line]
```

### 🔑 stderr Redirection Options

| Option | Description | Shell Equivalent |
|--------|-------------|------------------|
| `capture_output=True` | Capture both stdout and stderr | N/A |
| `stderr=subprocess.STDOUT` | Combine stderr into stdout | `2>&1` |
| `stderr=subprocess.DEVNULL` | Suppress stderr | `2>/dev/null` |
| `stderr=subprocess.PIPE` | Capture stderr separately | N/A |
| `stderr=file_handle` | Redirect to file | `2> file` |

---

## 6. Advanced Redirection

**File**: [`advanced_redirection.py`](advanced_redirection.py)

### 6.1. Bidirectional Communication

**File**: [`advanced_redirection.py`](advanced_redirection.py) - Line 27

```python
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
```

### 6.2. Tee-like Behavior

**File**: [`advanced_redirection.py`](advanced_redirection.py) - Line 59

```python
# Run command and capture output
result = subprocess.run(
    ["echo", "This goes to both file and stdout"],
    capture_output=True,
    text=True
)

# Write to file
with open('output.txt', 'w') as f:
    f.write(result.stdout)

# Also print to stdout
print(f"To stdout: {result.stdout.strip()}")
```

**Like Unix `tee` command**: Write to file AND stdout

### 6.3. Conditional Redirection

**File**: [`advanced_redirection.py`](advanced_redirection.py) - Line 95

```python
# Run command
result = subprocess.run(
    ["echo", "Success!"],
    capture_output=True,
    text=True
)

# Redirect based on return code
if result.returncode == 0:
    with open('success.txt', 'w') as f:
        f.write(result.stdout)
else:
    with open('error.txt', 'w') as f:
        f.write(result.stderr)
```

### 6.4. Pipeline with Checkpoints

**File**: [`advanced_redirection.py`](advanced_redirection.py) - Line 253

```python
# Stage 1: Generate data
p1 = subprocess.Popen(
    ["echo", "apple\nbanana\ncherry"],
    stdout=subprocess.PIPE,
    text=True
)

# Save stage 1 output
if p1.stdout:
    stage1_output = p1.stdout.read()
    with open('stage1.txt', 'w') as f:
        f.write(stage1_output)

p1.wait()

# Stage 2: Sort (read from checkpoint)
with open('stage1.txt', 'r') as f:
    p2 = subprocess.Popen(
        ["sort"],
        stdin=f,
        stdout=subprocess.PIPE,
        text=True
    )

    # Save stage 2 output
    if p2.stdout:
        stage2_output = p2.stdout.read()
        with open('stage2.txt', 'w') as f2:
            f2.write(stage2_output)

p2.wait()
```

### 💡 Advanced Redirection Patterns

1. **Bidirectional** - Two-way communication with processes
2. **Tee** - Split output to multiple destinations
3. **Conditional** - Redirect based on results
4. **Logging** - Wrap commands with logging
5. **Checkpoints** - Save intermediate pipeline results
6. **Dynamic** - Choose redirection at runtime

---

## 7. Summary

### What You Learned

✅ **Basic piping**: Connect processes with pipes
✅ **File redirection**: Redirect stdin/stdout/stderr to files
✅ **Command pipelines**: Build multi-stage data processing
✅ **stderr handling**: Separate, combine, or suppress errors
✅ **Advanced patterns**: Bidirectional, tee, conditional, checkpoints
✅ **Best practices**: Close stdout, check return codes, handle errors

### Key Takeaways

1. **Use subprocess.PIPE** to connect processes
2. **Close stdout** after connecting to next process
3. **File handles** for flexible redirection
4. **subprocess.DEVNULL** to discard output
5. **stderr=subprocess.STDOUT** to combine streams
6. **Check return codes** of all pipeline stages
7. **Build reusable** pipeline functions
8. **Handle errors** at each stage

### Quick Reference

```python
import subprocess

# Basic pipe
p1 = subprocess.Popen(["echo", "data"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["wc", "-w"], stdin=p1.stdout, stdout=subprocess.PIPE)
if p1.stdout:
    p1.stdout.close()
output, _ = p2.communicate()

# File redirection
with open('output.txt', 'w') as f:
    subprocess.run(["echo", "Hello"], stdout=f)

with open('input.txt', 'r') as f:
    subprocess.run(["cat"], stdin=f)

# stderr handling
result = subprocess.run(
    ["command"],
    capture_output=True,  # Both stdout and stderr
    text=True
)

# Combine stderr into stdout
result = subprocess.run(
    ["command"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)

# Suppress stderr
result = subprocess.run(
    ["command"],
    stderr=subprocess.DEVNULL
)
```

---

## 📝 Practice Exercises

### Exercise 1: Log Processor
Create a pipeline that processes log files: filter errors → sort → count unique.

### Exercise 2: Data Pipeline
Build a reusable pipeline function that accepts a list of commands and processes data.

### Exercise 3: Tee Implementation
Implement a function that writes output to both a file and stdout (like `tee`).

### Exercise 4: Error Handler
Create a wrapper that redirects output based on success/failure.

---

## ✅ Self-Assessment Checklist

Before moving to the next topic, make sure you can:

- [ ] Connect two processes with a pipe
- [ ] Build multi-stage pipelines
- [ ] Redirect stdout to a file
- [ ] Redirect stderr to a file
- [ ] Read stdin from a file
- [ ] Append to files
- [ ] Combine stdout and stderr
- [ ] Suppress unwanted output
- [ ] Check return codes in pipelines
- [ ] Build reusable pipeline functions

---

## 🔗 Navigation

- [← Back to Subprocess](../subprocess.md)
- [Previous: Advanced Execution](../03_advanced_execution/)
- [Next: Process Control →](../05_process_control/)

---

## 📚 Additional Resources

- [Unix Pipes and Filters](https://en.wikipedia.org/wiki/Pipeline_(Unix))
- [I/O Redirection](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)
- [subprocess Documentation](https://docs.python.org/3/library/subprocess.html)

---

**Files in this section**:
- [`basic_piping.py`](basic_piping.py) - Connecting processes with pipes
- [`file_redirection.py`](file_redirection.py) - Redirecting to/from files
- [`command_pipelines.py`](command_pipelines.py) - Multi-stage pipelines
- [`stderr_handling.py`](stderr_handling.py) - Managing stderr
- [`advanced_redirection.py`](advanced_redirection.py) - Advanced patterns

**Next**: [05. Process Control →](../05_process_control/)
