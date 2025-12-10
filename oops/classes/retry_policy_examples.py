"""Examples comparing hard-coded __init__ defaults vs @classmethod presets.

Run from the repo root with:

    python3 oops/classes/retry_policy_examples.py
"""

from __future__ import annotations


class RetryPolicyRigid:
    """Rigid design: only one configuration baked into __init__.

    You *cannot* create a RetryPolicyRigid with different values.
    """

    def __init__(self) -> None:
        self.attempts: int = 3
        self.delay: float = 10.0


class RetryPolicy:
    """Flexible design: __init__ is general, classmethods provide presets."""

    def __init__(self, attempts: int, delay: float) -> None:
        self.attempts = attempts
        self.delay = delay

    @classmethod
    def default(cls) -> "RetryPolicy":
        """Common default policy used in most places."""

        return cls(attempts=3, delay=1.0)

    @classmethod
    def fast(cls) -> "RetryPolicy":
        """More aggressive: few attempts, short delay."""

        return cls(attempts=1, delay=0.1)

    @classmethod
    def slow(cls) -> "RetryPolicy":
        """Conservative: many attempts, long delay."""

        return cls(attempts=10, delay=5.0)


class CustomRetryPolicy(RetryPolicy):
    """Subclass to show that classmethods return the subclass when called there."""

    @classmethod
    def default(cls) -> "CustomRetryPolicy":  # type: ignore[override]
        # Start from the base default, then tweak if needed.
        base = super().default()
        return cls(attempts=base.attempts + 1, delay=base.delay)


if __name__ == "__main__":
    rigid = RetryPolicyRigid()
    print("[Rigid] attempts=", rigid.attempts, "delay=", rigid.delay)

    # Flexible patterns
    print("[Default]", vars(RetryPolicy.default()))
    print("[Fast]   ", vars(RetryPolicy.fast()))
    print("[Slow]   ", vars(RetryPolicy.slow()))
    print("[Custom] ", vars(RetryPolicy(attempts=7, delay=2.5)))

    # Subclass: classmethod uses CustomRetryPolicy as cls
    custom = CustomRetryPolicy.default()
    print("[CustomRetryPolicy.default] type=", type(custom).__name__, "values=", vars(custom))

