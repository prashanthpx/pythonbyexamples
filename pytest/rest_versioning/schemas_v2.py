"""Version ``v2`` schema information for the ``RestClient`` examples.

Compared to ``v1`` this adds a ``compression`` field and one extra
optional field. Tests will assert on these differences.
"""

from typing import List


REQUIRED_FIELDS: List[str] = ["name", "size_gb", "compression"]
OPTIONAL_FIELDS: List[str] = ["description", "replication"]

