"""Simple calculator module for pytest learning examples.

This module is intentionally small and simple so that you
don't have to think about the logic and can focus on tests.
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    """Divide a by b.

    For now we assume b is not zero. Later, we can extend
    this with error handling and tests for exceptions.
    """
    return a / b

