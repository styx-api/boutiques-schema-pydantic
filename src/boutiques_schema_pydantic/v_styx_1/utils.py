"""Utility types."""

from typing import Annotated

from pydantic import StringConstraints

StringProperty = Annotated[
    str,
    StringConstraints(min_length=1),
]
"""Pydantic string property with min-length 1."""

IdStringProperty = Annotated[
    str,
    StringConstraints(pattern=r"^[0-9_a-zA-Z]+$", min_length=1),
]
"""Pydantic string property, alphanumeric only and min-length 1.
Used for various ID fields."""

ValueKeyStringProperty = Annotated[
    str,
    StringConstraints(pattern=r"^\[[0-9_A-Z]+\]$", min_length=1),
]
"""Pydantic string property, uppercase alphanumeric only and min-length 1
surrounded by square brackets. Used for value-key fields."""
