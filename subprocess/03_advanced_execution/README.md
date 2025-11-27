# 03. Advanced Execution

[← Back to Subprocess](../subprocess.md) | [Previous: Input/Output](../02_input_output/) | [Next: Pipes and Redirection →](../04_pipes_redirection/)

> **Level**: 🟡 Intermediate  
> **Estimated Time**: 2.5 hours  
> **Prerequisites**: 01. Basics, 02. Input/Output

---

## 📚 Table of Contents

1. [Introduction](#1-introduction)
2. [subprocess.Popen Basics](#2-subprocesspopen-basics)
3. [communicate() Method](#3-communicate-method)
4. [poll() and wait()](#4-poll-and-wait)
5. [Non-blocking Execution](#5-non-blocking-execution)
6. [Process Management](#6-process-management)
7. [Summary](#7-summary)

---

## 1. Introduction

Advanced execution techniques give you fine-grained control over processes. You'll learn:
- Low-level Popen interface
- Process communication
- Status checking
- Non-blocking execution
- Process lifecycle management

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Popen** | Low-level process interface |
| **communicate()** | Send input and read output |
| **poll()** | Check status without waiting |
| **wait()** | Wait for process completion |
| **Non-blocking** | Start process and continue immediately |
| **Process management** | Control process lifecycle |

---

## 2. subprocess.Popen Basics

**File**: [`popen_basics.py`](popen_basics.py)

### 2.1. Basic Popen Usage

**File**: [`popen_basics.py`](popen_basics.py) - Line 27

```python
import subprocess

# Start process
process = subprocess.Popen(
    ["echo", "Hello from Popen"]
)

print(f"Process started, PID: {process.pid}")
print("Popen returned immediately!")

# Wait for completion
process.wait()
print(f"Return code: {process.returncode}")
```

### 🔑 Popen vs run()

| Aspect | subprocess.run() | subprocess.Popen() |
|--------|------------------|-------------------|
| **Level** | High-level | Low-level |
| **Blocking** | Waits for completion | Returns immediately |
| **Control** | Less | More |
| **Complexity** | Simpler | More complex |
| **Use for** | Simple commands | Advanced control |

### 2.2. Popen with Output Capture

**File**: [`popen_basics.py`](popen_basics.py) - Line 51

```python
# Start process with output capture
process = subprocess.Popen(
    ["echo", "Hello World"],
    stdout=subprocess.PIPE,  # ← Capture stdout
    stderr=subprocess.PIPE,  # ← Capture stderr
    text=True                # ← Text mode
)

# Wait and get output
process.wait()

# Read output
if process.stdout:
    output = process.stdout.read()
    print(f"Output: {output}")
```

### 2.3. Popen Attributes

**File**: [`popen_basics.py`](popen_basics.py) - Line 135

```python
process = subprocess.Popen(
    ["echo", "Hello"],
    stdout=subprocess.PIPE,
    text=True
)

# Available attributes
print(f"pid: {process.pid}")          # Process ID
print(f"args: {process.args}")        # Command arguments
print(f"returncode: {process.returncode}")  # None until finished

process.wait()
print(f"returncode: {process.returncode}")  # Now has value
```

### 💡 When to Use Popen

**Use subprocess.run() when**:
- Simple command execution
- You can wait for completion
- You want all output at once
- Simpler code is preferred

**Use subprocess.Popen() when**:
- Need real-time output streaming
- Running multiple processes concurrently
- Need fine-grained control
- Want to check status while running
- Need to send input during execution

---

## 3. communicate() Method

**File**: [`communicate_method.py`](communicate_method.py)

### 3.1. Basic communicate()

**File**: [`communicate_method.py`](communicate_method.py) - Line 27

```python
process = subprocess.Popen(
    ["echo", "Hello World"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Wait and get output
stdout, stderr = process.communicate()  # ← Returns (stdout, stderr)

print(f"stdout: {stdout}")
print(f"stderr: {stderr}")
print(f"Return code: {process.returncode}")
```

### 3.2. communicate() with Input

**File**: [`communicate_method.py`](communicate_method.py) - Line 53

```python
process = subprocess.Popen(
    ["cat"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

# Send input and get output
input_data = "Hello from communicate!\n"
stdout, stderr = process.communicate(input=input_data)

print(f"Output: {stdout}")
```

### 3.3. communicate() with Timeout

**File**: [`communicate_method.py`](communicate_method.py) - Line 119

```python
process = subprocess.Popen(
    ["sleep", "10"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

try:
    stdout, stderr = process.communicate(timeout=2)
except subprocess.TimeoutExpired:
    print("Timeout! Killing process...")
    process.kill()
    process.communicate()  # Clean up
```

### 🔑 Why communicate()?

1. **Prevents deadlocks** - Handles buffering correctly
2. **Thread-safe** - Safe for concurrent use
3. **Simpler** - Easier than manual read/write
4. **Recommended** - Python docs recommend it
5. **One call** - Handles input and output together

### 💡 communicate() Best Practices

1. **Use communicate()** instead of manual read/write
2. **Always use timeout** for long-running processes
3. **Clean up on timeout** with kill() and communicate()
4. **Can only call once** per process
5. **Returns tuple** of (stdout, stderr)

---

## 4. poll() and wait()

**File**: [`poll_and_wait.py`](poll_and_wait.py)

### 4.1. poll() - Non-blocking Check

**File**: [`poll_and_wait.py`](poll_and_wait.py) - Line 27

```python
process = subprocess.Popen(
    ["sleep", "2"],
    stdout=subprocess.PIPE
)

# Check status without waiting
status = process.poll()  # ← Returns None if running

if status is None:
    print("Still running")
else:
    print(f"Finished with code: {status}")
```

### 4.2. wait() - Blocking Wait

**File**: [`poll_and_wait.py`](poll_and_wait.py) - Line 59

```python
process = subprocess.Popen(
    ["sleep", "2"],
    stdout=subprocess.PIPE
)

print("Waiting for completion...")
returncode = process.wait()  # ← Blocks until finished

print(f"Process finished with code: {returncode}")
```

### 4.3. Polling Loop

**File**: [`poll_and_wait.py`](poll_and_wait.py) - Line 81

```python
process = subprocess.Popen(
    ["sleep", "3"],
    stdout=subprocess.PIPE
)

# Poll in a loop
while process.poll() is None:  # ← While still running
    print("Still running...")
    time.sleep(1)

print(f"Finished with code: {process.returncode}")
```

### 4.4. wait() with Timeout

**File**: [`poll_and_wait.py`](poll_and_wait.py) - Line 107

```python
process = subprocess.Popen(
    ["sleep", "10"],
    stdout=subprocess.PIPE
)

try:
    returncode = process.wait(timeout=2)
    print(f"Completed: {returncode}")
except subprocess.TimeoutExpired:
    print("Timeout! Killing process...")
    process.kill()
    process.wait()
```

### 🔑 poll() vs wait()

| Method | Behavior | Returns | Use When |
|--------|----------|---------|----------|
| **poll()** | Non-blocking | None or returncode | Checking status |
| **wait()** | Blocking | returncode | Waiting for completion |
| **wait(timeout)** | Blocking with limit | returncode | Preventing hangs |

### 💡 poll() and wait() Best Practices

1. **Use poll()** to check status without waiting
2. **Use wait()** when you need to wait
3. **Always use timeout** with wait()
4. **Use poll() in loop** to monitor progress
5. **Check multiple processes** with poll()

---

## 5. Non-blocking Execution

**File**: [`non_blocking.py`](non_blocking.py)

### 5.1. Basic Non-blocking

**File**: [`non_blocking.py`](non_blocking.py) - Line 27

```python
# Start process
process = subprocess.Popen(
    ["sleep", "3"],
    stdout=subprocess.PIPE
)

print("Process started!")
print("Continuing immediately!")

# Do other work
for i in range(3):
    print(f"Doing work... {i+1}")
    time.sleep(1)

# Wait when ready
process.wait()
```

### 5.2. Multiple Concurrent Processes

**File**: [`non_blocking.py`](non_blocking.py) - Line 56

```python
# Start all processes
processes = [
    subprocess.Popen(["sleep", "2"], stdout=subprocess.PIPE)
    for _ in range(3)
]

print("All processes started!")

# Wait for all
for process in processes:
    process.wait()

print("All processes finished!")
```

### 5.3. Sequential vs Concurrent

**File**: [`non_blocking.py`](non_blocking.py) - Line 85

```python
# Sequential - takes 3 seconds
for i in range(3):
    subprocess.run(["sleep", "1"])

# Concurrent - takes 1 second
processes = [
    subprocess.Popen(["sleep", "1"])
    for _ in range(3)
]
for p in processes:
    p.wait()
```

### 🔑 Benefits of Non-blocking

1. **Better performance** - Run processes concurrently
2. **Responsive apps** - Don't freeze while waiting
3. **Parallel execution** - Multiple processes at once
4. **Efficient** - Better resource usage
5. **Flexible** - Do work while waiting

### 💡 Non-blocking Best Practices

1. **Start all processes first** - Then wait for all
2. **Use poll()** to check status
3. **Collect results** with communicate()
4. **Handle errors** for each process
5. **Clean up** all processes

---

## 6. Process Management

**File**: [`process_management.py`](process_management.py)

### 6.1. Process Attributes

**File**: [`process_management.py`](process_management.py) - Line 27

```python
process = subprocess.Popen(
    ["sleep", "5"],
    stdout=subprocess.PIPE
)

# Available attributes
print(f"pid: {process.pid}")              # Process ID
print(f"args: {process.args}")            # Command
print(f"returncode: {process.returncode}") # None while running
```

### 6.2. Terminating Processes

**File**: [`process_management.py`](process_management.py) - Line 57

```python
# Graceful termination
process.terminate()  # ← Sends SIGTERM
process.wait()

# Forceful termination
process.kill()  # ← Sends SIGKILL
process.wait()
```

### 6.3. Sending Signals

**File**: [`process_management.py`](process_management.py) - Line 95

```python
import signal

process = subprocess.Popen(["sleep", "10"])

# Send custom signal
process.send_signal(signal.SIGTERM)
process.wait()
```

### 6.4. Process Cleanup

**File**: [`process_management.py`](process_management.py) - Line 117

```python
# Using context manager (recommended)
with subprocess.Popen(
    ["sleep", "2"],
    stdout=subprocess.PIPE
) as process:
    process.wait()
# Resources automatically cleaned up!

# Manual cleanup
process = subprocess.Popen(["sleep", "2"])
try:
    process.wait()
finally:
    if process.poll() is None:
        process.terminate()
        process.wait()
```

### 🔑 Termination Methods

| Method | Signal | Behavior |
|--------|--------|----------|
| **terminate()** | SIGTERM | Graceful shutdown |
| **kill()** | SIGKILL | Immediate termination |
| **send_signal()** | Custom | Specific signal |

### 💡 Process Management Best Practices

1. **Use context manager** for automatic cleanup
2. **terminate() first** - Try graceful shutdown
3. **kill() if needed** - Force if terminate fails
4. **Always wait()** - Clean up resources
5. **Handle timeouts** - Don't let processes hang
6. **Track PIDs** - For monitoring and debugging

---

## 7. Summary

### What You Learned

✅ **Popen basics**: Low-level process interface
✅ **communicate()**: Send input and read output safely
✅ **poll()**: Check status without waiting
✅ **wait()**: Wait for process completion
✅ **Non-blocking**: Run processes concurrently
✅ **Process management**: Control lifecycle and resources
✅ **Termination**: terminate(), kill(), signals
✅ **Cleanup**: Proper resource management

### Key Takeaways

1. **Use Popen** for advanced control
2. **communicate()** prevents deadlocks
3. **poll()** for non-blocking status checks
4. **wait()** with timeout to prevent hanging
5. **Non-blocking** for better performance
6. **Start all, wait all** for concurrent execution
7. **terminate()** for graceful shutdown
8. **Always clean up** resources

### Quick Reference

```python
import subprocess
import time

# Basic Popen
process = subprocess.Popen(
    ["command"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# communicate()
stdout, stderr = process.communicate(input="data", timeout=10)

# poll() and wait()
if process.poll() is None:
    print("Still running")

process.wait(timeout=10)

# Non-blocking
processes = [
    subprocess.Popen(["cmd"]) for _ in range(3)
]
for p in processes:
    p.wait()

# Process management
process.terminate()  # Graceful
process.kill()       # Forceful
process.wait()       # Clean up
```

---

## 📝 Practice Exercises

### Exercise 1: Real-time Monitoring
Create a script that monitors a long-running process and shows progress.

### Exercise 2: Concurrent Execution
Run multiple commands concurrently and collect their results.

### Exercise 3: Timeout Handling
Implement a function that runs a command with timeout and proper cleanup.

### Exercise 4: Process Pool
Create a simple process pool that runs commands with a maximum concurrency limit.

---

## ✅ Self-Assessment Checklist

Before moving to the next topic, make sure you can:

- [ ] Use Popen to start processes
- [ ] Understand Popen vs run() differences
- [ ] Use communicate() for I/O
- [ ] Handle timeouts with communicate()
- [ ] Check process status with poll()
- [ ] Wait for processes with wait()
- [ ] Run processes concurrently
- [ ] Terminate processes gracefully
- [ ] Send custom signals
- [ ] Clean up process resources properly

---

## 🔗 Navigation

- [← Back to Subprocess](../subprocess.md)
- [Previous: Input/Output](../02_input_output/)
- [Next: Pipes and Redirection →](../04_pipes_redirection/)

---

## 📚 Additional Resources

- [subprocess.Popen Documentation](https://docs.python.org/3/library/subprocess.html#subprocess.Popen)
- [Process Management in Python](https://docs.python.org/3/library/subprocess.html#subprocess-replacements)
- [Signal Handling](https://docs.python.org/3/library/signal.html)

---

**Files in this section**:
- [`popen_basics.py`](popen_basics.py) - Popen interface basics
- [`communicate_method.py`](communicate_method.py) - Using communicate()
- [`poll_and_wait.py`](poll_and_wait.py) - Status checking and waiting
- [`non_blocking.py`](non_blocking.py) - Non-blocking execution
- [`process_management.py`](process_management.py) - Process lifecycle management

**Next**: [04. Pipes and Redirection →](../04_pipes_redirection/)
