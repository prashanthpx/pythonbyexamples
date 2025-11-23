class Account:
    """A simple bank account with encapsulated balance.

    We keep the real value in a "private" attribute `_balance` and expose a
    `balance` property with validation. Code that uses this class works with
    `account.balance` like a normal attribute, but we can enforce rules in one
    place.
    """

    def __init__(self, owner: str, balance: int = 0) -> None:
        self.owner = owner
        # Store value through the property so validation always applies
        self._balance = 0
        self.balance = balance

    @property
    def balance(self) -> int:
        """Public attribute-like access to the current balance."""

        return self._balance

    @balance.setter
    def balance(self, value: int) -> None:
        """Validate and update the balance.

        This is where we enforce the rule: balance can never be negative.
        """

        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

    def deposit(self, amount: int) -> None:
        print(f"[DEPOSIT] +{amount}")
        self.balance = self.balance + amount

    def withdraw(self, amount: int) -> None:
        print(f"[WITHDRAW] -{amount}")
        self.balance = self.balance - amount


if __name__ == "__main__":  # pragma: no cover - manual run example
    account = Account("alice", balance=100)
    print("Owner:", account.owner)
    print("Initial balance:", account.balance)

    account.deposit(50)
    print("After deposit:", account.balance)

    try:
        # This would make the balance negative, so the property setter rejects it
        account.withdraw(200)
    except ValueError as e:
        print("Withdraw failed:", e)

    print("Balance after failed withdraw:", account.balance)

    account.withdraw(50)
    print("Final balance:", account.balance)


# Captured output from running: python3 encapsulation_property_example.py
output = """Owner: alice
Initial balance: 100
[DEPOSIT] +50
After deposit: 150
[WITHDRAW] -200
Withdraw failed: Balance cannot be negative
Balance after failed withdraw: 150
[WITHDRAW] -50
Final balance: 100
"""

