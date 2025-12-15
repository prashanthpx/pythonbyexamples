"""Compare different places to put helper logic in a class.

- Inner function defined inside a method
- Private instance method (_make_api_url)
- @staticmethod helper
- @classmethod alternate constructor
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ApiClient:
    base_url: str

    # 1) Method that defines an inner helper function
    def fetch_users_with_inner_helper(self) -> None:
        """Use an inner function as a one-off helper inside a method."""

        def make_url(endpoint: str) -> str:
            # Inner function closes over `self`
            return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        url = make_url("/users")
        print(f"[inner] GET {url}")

    # 2) Private instance method helper
    def _make_api_url(self, endpoint: str) -> str:
        """Private instance method reused by multiple call sites."""
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def fetch_users_with_private_method(self) -> None:
        url = self._make_api_url("/users")
        print(f"[private] GET {url}")

    def fetch_orders_with_private_method(self) -> None:
        url = self._make_api_url("/orders")
        print(f"[private] GET {url}")

    # 3) Staticmethod helper: does not depend on self or cls
    @staticmethod
    def _join_url(base_url: str, endpoint: str) -> str:
        """Pure helper: does not touch self/cls, easy to unit-test."""
        return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def fetch_users_with_static_helper(self) -> None:
        url = self._join_url(self.base_url, "/users")
        print(f"[static] GET {url}")

    # 4) Classmethod option: build client from class-level configuration
    @classmethod
    def from_default(cls) -> "ApiClient":
        """Alternate constructor; pretend to load base_url from config."""
        default_base = "https://api.example.com"
        return cls(default_base)


def main() -> None:
    print("=== ApiClient helper placement demo ===")

    client = ApiClient("https://api.test")
    client.fetch_users_with_inner_helper()
    client.fetch_users_with_private_method()
    client.fetch_orders_with_private_method()
    client.fetch_users_with_static_helper()

    print("--- Using classmethod alternate constructor ---")
    default_client = ApiClient.from_default()
    default_client.fetch_users_with_private_method()


if __name__ == "__main__":
    main()

