# 02. Input/Output

[← Back to Subprocess](../subprocess.md) | [Previous: Basics](../01_basics/) | [Next: Advanced Execution →](../03_advanced_execution/)

> **Level**: 🟢 Beginner  
> **Estimated Time**: 2.5 hours  
> **Prerequisites**: 01. Basics

---

## 📚 Table of Contents

1. [Introduction](#1-introduction)
2. [Capturing Output](#2-capturing-output)
3. [Text vs Bytes Mode](#3-text-vs-bytes-mode)
4. [Encoding Handling](#4-encoding-handling)
5. [Sending Input (stdin)](#5-sending-input-stdin)
6. [Real-time Streaming](#6-real-time-streaming)
7. [Summary](#7-summary)

---

## 1. Introduction

Input/output handling is crucial for working with subprocess. You need to:
- Capture command output for processing
- Send input to commands
- Handle different encodings
- Process output in real-time

### Key Concepts

| Concept | Description |
|---------|-------------|
| **stdout** | Standard output stream (normal output) |
| **stderr** | Standard error stream (error messages) |
| **stdin** | Standard input stream (input to command) |
| **capture_output** | Capture both stdout and stderr |
| **text mode** | Convert bytes to strings |
| **encoding** | Character encoding (UTF-8, ASCII, etc.) |

---

## 2. Capturing Output

**File**: [`capturing_output.py`](capturing_output.py)

### 2.1. Basic Output Capture

**File**: [`capturing_output.py`](capturing_output.py) - Line 27

```python
import subprocess

result = subprocess.run(
    ["echo", "Hello World"],
    capture_output=True,  # ← Capture both stdout and stderr
    text=True             # ← Return as string
)

print(result.stdout)  # 'Hello World\n'
print(result.stderr)  # ''
```

### 🔑 Capture Methods

```python
# Method 1: capture_output=True (recommended)
result = subprocess.run(
    ["ls", "-l"],
    capture_output=True,
    text=True
)

# Method 2: stdout and stderr separately
result = subprocess.run(
    ["ls", "-l"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Method 3: stdout only
result = subprocess.run(
    ["ls", "-l"],
    stdout=subprocess.PIPE,
    text=True
)
```

### 2.2. Without Capture

**File**: [`capturing_output.py`](capturing_output.py) - Line 47

```python
# Without capture_output, output goes to terminal
result = subprocess.run(["echo", "Hello"])

print(result.stdout)  # None
print(result.stderr)  # None
```

### 2.3. Processing Captured Output

**File**: [`capturing_output.py`](capturing_output.py) - Line 135

```python
result = subprocess.run(
    ["ls", "-l", "/tmp"],
    capture_output=True,
    text=True
)

# Split into lines
lines = result.stdout.splitlines()

# Filter lines
py_files = [line for line in lines if '.py' in line]

# Strip whitespace
clean = result.stdout.strip()

# Check patterns
if "total" in result.stdout:
    print("Found 'total'")
```

### 💡 Output Capture Best Practices

1. **Use capture_output=True** for simplicity
2. **Always use text=True** for text output
3. **Check returncode** before processing output
4. **Use splitlines()** to process line by line
5. **Strip whitespace** with strip()

---

## 3. Text vs Bytes Mode

**File**: [`text_vs_bytes.py`](text_vs_bytes.py)

### 3.1. Bytes Mode (Default)

**File**: [`text_vs_bytes.py`](text_vs_bytes.py) - Line 24

```python
# Default: returns bytes
result = subprocess.run(
    ["echo", "Hello"],
    capture_output=True
)

print(type(result.stdout))  # <class 'bytes'>
print(result.stdout)        # b'Hello\n'
```

### 3.2. Text Mode

**File**: [`text_vs_bytes.py`](text_vs_bytes.py) - Line 44

```python
# text=True: returns string
result = subprocess.run(
    ["echo", "Hello"],
    capture_output=True,
    text=True  # ← Convert to string
)

print(type(result.stdout))  # <class 'str'>
print(result.stdout)        # 'Hello\n'
```

### 🔑 Bytes vs Text Comparison

| Aspect | Bytes Mode | Text Mode |
|--------|------------|-----------|
| **Parameter** | (default) | `text=True` |
| **Type** | `bytes` | `str` |
| **Example** | `b'Hello\n'` | `'Hello\n'` |
| **Encoding** | Manual | Automatic |
| **Use for** | Binary data | Text output |

### 3.3. Converting Between Bytes and Text

**File**: [`text_vs_bytes.py`](text_vs_bytes.py) - Line 64

```python
# Bytes to string
bytes_output = b'Hello\n'
string_output = bytes_output.decode('utf-8')

# String to bytes
string_output = 'Hello\n'
bytes_output = string_output.encode('utf-8')
```

### 💡 When to Use Each

**Use text=True (text mode)**:
- Reading text output (most common)
- Processing log files
- Parsing command output
- When you need string operations

**Use bytes mode (default)**:
- Reading binary files
- Processing images, videos
- When encoding is unknown
- For binary protocols

---

## 4. Encoding Handling

**File**: [`encoding_handling.py`](encoding_handling.py)

### 4.1. Specifying Encoding

**File**: [`encoding_handling.py`](encoding_handling.py) - Line 48

```python
result = subprocess.run(
    ["echo", "Hello 世界"],
    capture_output=True,
    text=True,
    encoding='utf-8'  # ← Explicit UTF-8
)

print(result.stdout)  # 'Hello 世界\n'
```

### 4.2. Handling Encoding Errors

**File**: [`encoding_handling.py`](encoding_handling.py) - Line 72

```python
# errors='strict' (default) - raises exception
result = subprocess.run(
    ["echo", "Café"],
    capture_output=True,
    text=True,
    encoding='ascii',
    errors='strict'  # ← Raise on error
)

# errors='ignore' - skip invalid characters
result = subprocess.run(
    ["echo", "Café"],
    capture_output=True,
    text=True,
    encoding='ascii',
    errors='ignore'  # ← Skip invalid chars
)

# errors='replace' - replace with ?
result = subprocess.run(
    ["echo", "Café"],
    capture_output=True,
    text=True,
    encoding='ascii',
    errors='replace'  # ← Replace with ?
)
```

### 🔑 Error Handling Options

| Option | Behavior | Example |
|--------|----------|---------|
| `'strict'` | Raise exception | UnicodeDecodeError |
| `'ignore'` | Skip invalid chars | `'Caf'` |
| `'replace'` | Replace with ? | `'Caf?'` |
| `'backslashreplace'` | Use escape sequences | `'Caf\\xe9'` |

### 4.3. Common Encodings

```python
# UTF-8 (recommended for most cases)
encoding='utf-8'

# ASCII (English only)
encoding='ascii'

# Latin-1 (Western European)
encoding='latin-1'

# Windows encoding
encoding='cp1252'
```

### 💡 Encoding Best Practices

1. **Always specify encoding** explicitly
2. **Use UTF-8** for most cases
3. **Handle encoding errors** with errors parameter
4. **Test with non-ASCII** characters
5. **Use bytes mode** if encoding is unknown

---

## 5. Sending Input (stdin)

**File**: [`stdin_input.py`](stdin_input.py)

### 5.1. Basic Input

**File**: [`stdin_input.py`](stdin_input.py) - Line 27

```python
result = subprocess.run(
    ["cat"],
    input="Hello from Python!\n",  # ← Send to stdin
    capture_output=True,
    text=True
)

print(result.stdout)  # 'Hello from Python!\n'
```

### 5.2. Input with grep

**File**: [`stdin_input.py`](stdin_input.py) - Line 43

```python
data = """apple
banana
cherry
date
elderberry
"""

result = subprocess.run(
    ["grep", "e"],
    input=data,  # ← Send data to grep
    capture_output=True,
    text=True
)

print(result.stdout)  # Lines containing 'e'
```

### 5.3. Input with sort

**File**: [`stdin_input.py`](stdin_input.py) - Line 73

```python
data = """zebra
apple
mango
banana
"""

result = subprocess.run(
    ["sort"],
    input=data,
    capture_output=True,
    text=True
)

print(result.stdout)  # Sorted output
```

### 🔑 Input Patterns

```python
# String input (text mode)
subprocess.run(["cat"], input="text", text=True)

# Bytes input
subprocess.run(["cat"], input=b"bytes")

# Multiline input
subprocess.run(["wc", "-l"], input="line1\nline2\nline3\n", text=True)

# From list
data = "\n".join(["item1", "item2", "item3"]) + "\n"
subprocess.run(["sort"], input=data, text=True)
```

### 💡 stdin Best Practices

1. **Use input parameter** for simple cases
2. **Match mode**: string input with text=True
3. **Add newlines** for line-based commands
4. **Process data** before sending
5. **Combine with capture_output** to get results

---

## 6. Real-time Streaming

**File**: [`streaming_output.py`](streaming_output.py)

### 6.1. Non-streaming (subprocess.run)

**File**: [`streaming_output.py`](streaming_output.py) - Line 27

```python
# subprocess.run() waits for completion
result = subprocess.run(
    ["long_running_command"],
    capture_output=True,
    text=True
)

# All output comes at once
print(result.stdout)
```

### 6.2. Basic Streaming (subprocess.Popen)

**File**: [`streaming_output.py`](streaming_output.py) - Line 45

```python
# Use Popen for real-time streaming
process = subprocess.Popen(
    ["long_running_command"],
    stdout=subprocess.PIPE,
    text=True
)

# Read line by line
if process.stdout:
    for line in process.stdout:
        print(f"Received: {line.strip()}")

process.wait()
```

### 6.3. Streaming with Progress

**File**: [`streaming_output.py`](streaming_output.py) - Line 71

```python
process = subprocess.Popen(
    ["command_with_progress"],
    stdout=subprocess.PIPE,
    text=True
)

if process.stdout:
    for line in process.stdout:
        print(f"Progress: {line.strip()}")

process.wait()
```

### 6.4. Streaming and Filtering

**File**: [`streaming_output.py`](streaming_output.py) - Line 97

```python
process = subprocess.Popen(
    ["command"],
    stdout=subprocess.PIPE,
    text=True
)

# Filter for ERROR lines
if process.stdout:
    for line in process.stdout:
        if 'ERROR' in line:
            print(f"⚠️  {line.strip()}")

process.wait()
```

### 🔑 Streaming vs Non-streaming

| Aspect | subprocess.run() | subprocess.Popen() |
|--------|------------------|-------------------|
| **Execution** | Waits for completion | Can stream |
| **Output** | All at once | Line by line |
| **Use for** | Short commands | Long-running |
| **Progress** | No | Yes |
| **Memory** | Stores all output | Processes incrementally |

### 💡 Streaming Best Practices

1. **Use Popen** for long-running commands
2. **Read line by line** for efficiency
3. **Show progress** to users
4. **Filter output** while streaming
5. **Use timeout** to prevent hanging
6. **Call wait()** to ensure completion

---

## 7. Summary

### What You Learned

✅ **Capturing output**: capture_output=True, stdout/stderr
✅ **Text vs bytes**: text=True for strings, default for bytes
✅ **Encoding**: encoding parameter, errors handling
✅ **Sending input**: input parameter for stdin
✅ **Real-time streaming**: Popen for line-by-line processing
✅ **Processing output**: splitlines(), strip(), filtering
✅ **Error handling**: errors parameter for encoding issues

### Key Takeaways

1. **Use capture_output=True** to capture stdout/stderr
2. **Use text=True** for text output (most common)
3. **Specify encoding** explicitly for portability
4. **Use input parameter** to send data to stdin
5. **Use Popen** for real-time streaming
6. **Process output** with string methods
7. **Handle encoding errors** with errors parameter
8. **Filter output** while streaming for efficiency

### Quick Reference

```python
import subprocess

# Capture output
result = subprocess.run(
    ["command"],
    capture_output=True,
    text=True
)
print(result.stdout)

# With encoding
result = subprocess.run(
    ["command"],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='replace'
)

# Send input
result = subprocess.run(
    ["grep", "pattern"],
    input="data\nto\nsearch\n",
    capture_output=True,
    text=True
)

# Real-time streaming
process = subprocess.Popen(
    ["command"],
    stdout=subprocess.PIPE,
    text=True
)
if process.stdout:
    for line in process.stdout:
        print(line.strip())
process.wait()
```

---

## 📝 Practice Exercises

### Exercise 1: Output Capture
Write a script that captures the output of `ls -l` and counts the number of files.

### Exercise 2: Text Processing
Use grep with input parameter to filter a list of words.

### Exercise 3: Encoding
Write a script that handles non-ASCII characters with different encodings.

### Exercise 4: Streaming
Create a progress monitor for a long-running command using Popen.

---

## ✅ Self-Assessment Checklist

Before moving to the next topic, make sure you can:

- [ ] Capture stdout and stderr separately
- [ ] Use text=True for string output
- [ ] Understand bytes vs text mode
- [ ] Specify character encoding
- [ ] Handle encoding errors
- [ ] Send input to commands via stdin
- [ ] Process multiline input
- [ ] Stream output in real-time with Popen
- [ ] Filter output while streaming
- [ ] Process captured output (split, strip, filter)

---

## 🔗 Navigation

- [← Back to Subprocess](../subprocess.md)
- [Previous: Basics](../01_basics/)
- [Next: Advanced Execution →](../03_advanced_execution/)

---

## 📚 Additional Resources

- [subprocess - Capturing Output](https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess)
- [Text Encoding in Python](https://docs.python.org/3/howto/unicode.html)
- [subprocess.Popen Documentation](https://docs.python.org/3/library/subprocess.html#subprocess.Popen)

---

**Files in this section**:
- [`capturing_output.py`](capturing_output.py) - Capturing stdout/stderr
- [`text_vs_bytes.py`](text_vs_bytes.py) - Text mode vs bytes mode
- [`encoding_handling.py`](encoding_handling.py) - Character encoding
- [`stdin_input.py`](stdin_input.py) - Sending input to processes
- [`streaming_output.py`](streaming_output.py) - Real-time output streaming

**Next**: [03. Advanced Execution →](../03_advanced_execution/)
