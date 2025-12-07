"""Tiny fake REST client used to demonstrate pytest fixtures and versioning.

The goal of this module is not to model a real API, but to give the
fixtures something concrete to work with, similar in spirit to the
``rest1_client`` tests in the Purity ``clusterload`` suite.
"""

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class RestClient:
    """Very small fake REST client.

    Attributes
    ----------
    base_url:
        Base URL of the (fake) service, such as
        ``"https://storage.example.test"``.
    api_version:
        Version string like ``"v1"`` or ``"v2"`` used in the examples.
    """

    base_url: str
    api_version: str

    def list_volumes(self) -> Dict[str, Any]:
        """Return a tiny "response" payload that includes the API version.

        In a real client this would perform an HTTP GET. Here we just
        return a structure that tests can assert on without any network
        calls. Keeping the behaviour simple lets us focus on pytest
        fixtures and parametrization.
        """

        return {
            "api_version": self.api_version,
            "volumes": [],  # a real service would return real data here
        }

