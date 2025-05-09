"""Model for Boutiques descriptor suggested-ressources property."""

from typing import Optional

import pydantic


class SuggestedResources(pydantic.BaseModel):
    """Model for suggested computational resources."""

    cpu_cores: Optional[int] = pydantic.Field(
        alias="cpu-core",
        description="The requested number of cpu cores to run the described "
        "application",
        ge=1,
    )
    ram: Optional[float] = pydantic.Field(
        description="The requested number of GB RAM to run the described application",
        ge=0,
    )
    disk_space: Optional[float] = pydantic.Field(
        alias="disk-space",
        description="The requested number of GB of storage to run the described "
        "application",
        ge=0,
    )
    nodes: Optional[int] = pydantic.Field(
        description="The requested number of nodes to spread the described application "
        "across",
        ge=1,
    )
    walltime_estimate: Optional[float] = pydantic.Field(
        alias="walltime-estimate",
        description="Estimated wall time of a task in seconds.",
        ge=0,
    )
