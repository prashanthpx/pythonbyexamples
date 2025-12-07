"""Version ``v1`` schema information for the ``RestClient`` examples.

We keep this deliberately tiny so that tests can easily see the
difference between versions.
"""

from typing import List


REQUIRED_FIELDS: List[str] = ["name", "size_gb"]
OPTIONAL_FIELDS: List[str] = ["description"]

