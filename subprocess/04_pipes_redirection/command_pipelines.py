"""
Example: Command Pipelines
Demonstrates building complex multi-stage pipelines.

Key Concepts:
- Multi-stage pipelines
- Data transformation chains
- Pipeline error handling
- Pipeline optimization
- Real-world pipeline examples

Pipeline pattern:
data → process1 → process2 → process3 → result

Benefits:
- Break complex tasks into simple steps
- Reusable components
- Easy to debug
- Efficient data processing
"""

import subprocess
from typing import List, Optional, Tuple


# ============================================================================
# THREE-STAGE PIPELINE
# ============================================================================

def three_stage_pipeline() -> None:
    """
    Build a three-stage pipeline.
    
    Equivalent to: echo "data" | sort | uniq | wc -l
    """
    print("Three-stage pipeline:")
    
    # Stage 1: Generate data
    p1 = subprocess.Popen(
        ["echo", "apple\nbanana\napple\ncherry\nbanana\napple"],
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
    
    print(f"Unique items count: {output.strip()}")


# ============================================================================
# PIPELINE WITH DATA PROCESSING
# ============================================================================

def pipeline_with_data_processing() -> None:
    """
    Pipeline that processes and transforms data.
    
    Equivalent to: cat file | grep pattern | sort | head -n 5
    """
    print("\n" + "=" * 70)
    print("PIPELINE WITH DATA PROCESSING")
    print("=" * 70)
    
    # Generate sample data
    data = "apple\nbanana\napricot\navocado\nblueberry\ncherry\n"
    
    # Stage 1: Input data
    p1 = subprocess.Popen(
        ["cat"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    
    # Stage 2: Filter (lines starting with 'a')
    p2 = subprocess.Popen(
        ["grep", "^a"],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        text=True
    )
    
    if p1.stdout:
        p1.stdout.close()
    
    # Stage 3: Sort
    p3 = subprocess.Popen(
        ["sort"],
        stdin=p2.stdout,
        stdout=subprocess.PIPE,
        text=True
    )
    
    if p2.stdout:
        p2.stdout.close()
    
    # Send data and get result
    if p1.stdin:
        p1.stdin.write(data)
        p1.stdin.close()
    
    output, _ = p3.communicate()
    
    print("Items starting with 'a' (sorted):")
    print(output)


# ============================================================================
# PIPELINE BUILDER
# ============================================================================

def build_pipeline(commands: List[List[str]], input_data: Optional[str] = None) -> str:
    """
    Build a pipeline from a list of commands.
    
    Args:
        commands: List of command lists
        input_data: Optional input data
    
    Returns:
        Pipeline output
    """
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


def use_pipeline_builder() -> None:
    """
    Use the pipeline builder function.

    Demonstrates reusable pipeline construction.
    """
    print("\n" + "=" * 70)
    print("PIPELINE BUILDER")
    print("=" * 70)

    # Example 1: Sort and count
    print("\n1. Sort and count unique items:")
    commands = [
        ["sort"],
        ["uniq"],
        ["wc", "-l"]
    ]
    data = "apple\nbanana\napple\ncherry\nbanana\n"
    result = build_pipeline(commands, data)
    print(f"   Unique count: {result.strip()}")

    # Example 2: Filter and sort
    print("\n2. Filter and sort:")
    commands = [
        ["grep", "a"],
        ["sort"]
    ]
    data = "apple\nbanana\ncherry\navocado\n"
    result = build_pipeline(commands, data)
    print("   Filtered and sorted:")
    for line in result.strip().split('\n'):
        print(f"     - {line}")


# ============================================================================
# PIPELINE WITH ERROR HANDLING
# ============================================================================

def pipeline_with_error_handling() -> None:
    """
    Handle errors in pipelines.

    Check each stage for errors.
    """
    print("\n" + "=" * 70)
    print("PIPELINE WITH ERROR HANDLING")
    print("=" * 70)

    # Stage 1
    p1 = subprocess.Popen(
        ["echo", "test data"],
        stdout=subprocess.PIPE
    )

    # Stage 2 (might fail)
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
    print(f"Stage 1 return code: {p1.returncode}")
    print(f"Stage 2 return code: {p2.returncode}")

    if p1.returncode == 0 and p2.returncode == 0:
        print(f"✅ Pipeline succeeded: {output.strip()}")
    else:
        print("❌ Pipeline failed!")


# ============================================================================
# COMPLEX PIPELINE EXAMPLE
# ============================================================================

def complex_pipeline_example() -> None:
    """
    Real-world complex pipeline.

    Process log data: filter → sort → count → format
    """
    print("\n" + "=" * 70)
    print("COMPLEX PIPELINE EXAMPLE")
    print("=" * 70)

    # Sample log data
    log_data = """ERROR: Connection failed
INFO: Starting service
ERROR: Timeout occurred
WARNING: Low memory
ERROR: Connection failed
INFO: Service started
ERROR: Timeout occurred
"""

    # Stage 1: Filter errors only
    p1 = subprocess.Popen(
        ["grep", "ERROR"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    # Stage 2: Sort
    p2 = subprocess.Popen(
        ["sort"],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        text=True
    )

    if p1.stdout:
        p1.stdout.close()

    # Stage 3: Count unique
    p3 = subprocess.Popen(
        ["uniq", "-c"],
        stdin=p2.stdout,
        stdout=subprocess.PIPE,
        text=True
    )

    if p2.stdout:
        p2.stdout.close()

    # Send data
    if p1.stdin:
        p1.stdin.write(log_data)
        p1.stdin.close()

    # Get result
    output, _ = p3.communicate()

    print("Error summary:")
    print(output)


# ============================================================================
# PARALLEL PIPELINES
# ============================================================================

def parallel_pipelines() -> None:
    """
    Run multiple pipelines in parallel.

    Process different data streams concurrently.
    """
    print("\n" + "=" * 70)
    print("PARALLEL PIPELINES")
    print("=" * 70)

    # Pipeline 1: Count words
    commands1 = [
        ["echo", "one two three"],
        ["wc", "-w"]
    ]

    # Pipeline 2: Count lines
    commands2 = [
        ["echo", "line1\nline2\nline3"],
        ["wc", "-l"]
    ]

    # Start both pipelines
    print("\nStarting parallel pipelines...")

    # Pipeline 1
    p1_1 = subprocess.Popen(commands1[0], stdout=subprocess.PIPE)
    p1_2 = subprocess.Popen(commands1[1], stdin=p1_1.stdout, stdout=subprocess.PIPE, text=True)
    if p1_1.stdout:
        p1_1.stdout.close()

    # Pipeline 2
    p2_1 = subprocess.Popen(commands2[0], stdout=subprocess.PIPE)
    p2_2 = subprocess.Popen(commands2[1], stdin=p2_1.stdout, stdout=subprocess.PIPE, text=True)
    if p2_1.stdout:
        p2_1.stdout.close()

    # Get results
    result1, _ = p1_2.communicate()
    result2, _ = p2_2.communicate()

    print(f"Pipeline 1 (word count): {result1.strip()}")
    print(f"Pipeline 2 (line count): {result2.strip()}")


# ============================================================================
# DEMONSTRATION: Command Pipelines
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("COMMAND PIPELINES")
    print("=" * 70)

    # Three-stage
    print("\n" + "=" * 70)
    print("1. THREE-STAGE PIPELINE")
    print("=" * 70)
    three_stage_pipeline()

    # Data processing
    pipeline_with_data_processing()

    # Pipeline builder
    use_pipeline_builder()

    # Error handling
    pipeline_with_error_handling()

    # Complex example
    complex_pipeline_example()

    # Parallel
    parallel_pipelines()

    print("\n" + "=" * 70)

    # Key takeaways
    print("\nKEY TAKEAWAYS:")
    print("-" * 70)
    print("1. Chain multiple processes for complex tasks")
    print("2. Close stdout after connecting to next process")
    print("3. Build reusable pipeline functions")
    print("4. Check return codes of all stages")
    print("5. Use text=True for string processing")
    print("6. Handle errors at each stage")
    print("7. Pipelines break complex tasks into simple steps")
    print("8. Can run multiple pipelines in parallel")
    print("9. Always wait for all processes to complete")
    print("10. Pipeline pattern: data → p1 → p2 → p3 → result")
    print("=" * 70)

