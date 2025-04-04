"""Model for Boutiques descriptor container-image property."""

import abc
import pathlib
import typing
from typing import Literal, Optional

import pydantic

from .. import StringProperty


class BaseContainerImage(pydantic.BaseModel, abc.ABC):
    """Model for container image configuration."""

    working_directory: Optional[pathlib.Path] = pydantic.Field(
        alias="working-directory",
        description="Location from which this task must be launched within the "
        "container.",
        default=None,
    )
    container_hash: Optional[StringProperty] = pydantic.Field(
        alias="container-hash",
        description="Hash for the given container.",
        default=None,
    )
    entrypoint: bool = pydantic.Field(
        description="Flag indicating whether or not the container uses an entrypoint.",
        default=False,
    )
    index: Optional[StringProperty] = pydantic.Field(
        description="Optional index where the image is available, if not the standard "
        "location. Example: docker.io",
        default=None,
    )
    container_opts: Optional[list[str]] = pydantic.Field(
        alias="container-opts",
        description="Container-level arguments for the application. Example: "
        "--privileged",
        default=None,
    )


class DockerContainerImage(BaseContainerImage):
    """Model for container image configuration."""

    type_: Literal["docker", "singularity"] = pydantic.Field(alias="type")
    image: StringProperty = pydantic.Field(
        description="Name of an image where the tool is installed and configured. "
        "Example: bids/mriqc.",
    )


class RootfsContainerImage(BaseContainerImage):
    """Model for container image configuration."""

    type_: Literal["rootfs"] = pydantic.Field(alias="type")
    url: pydantic.HttpUrl = pydantic.Field(
        description="URL where the image is available.",
    )


ContainerImage = typing.Union[DockerContainerImage, RootfsContainerImage]
