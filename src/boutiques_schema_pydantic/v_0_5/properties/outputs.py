"""Model for Boutiques descriptor outputs property."""

import typing
from typing import Annotated, Optional

import pydantic

from .. import StringProperty


class PathProperty(pydantic.BaseModel):
    """Model representing an path property."""

    propertyNames: Annotated[
        str, pydantic.StringConstraints(pattern=r"^[A-Za-z0-9_><=!)( ]*$")
    ] = pydantic.Field()


class BaseOutput(pydantic.BaseModel):
    """Model representing an output file."""

    id: Annotated[
        str, pydantic.StringConstraints(pattern=r"^[0-9_a-zA-Z]+$", min_length=1)
    ] = pydantic.Field(
        description="A short, unique, informative identifier "
        "containing only alphanumeric characters and underscores. "
        'Typically used to generate variable names. Example: "data_file".',
    )
    name: StringProperty = pydantic.Field(
        description="A human-readable name. Example: 'Data file'.",
    )
    description: Optional[str] = pydantic.Field(default=None)

    optional: bool = pydantic.Field(description="True if optional", default=False)

    path_template_stripped_extensions: Optional[list[str]] = pydantic.Field(
        alias="path-template-stripped-extensions",
        description="List of file extensions that will be stripped from the input "
        "values before being substituted in the path template. Example: "
        '[".nii",".nii.gz"].',
        default=None,
    )
    file_template: Optional[list[StringProperty]] = pydantic.Field(
        alias="file-template",
        description="An array of strings that may contain value keys. Each item will "
        "be a line in the configuration file.",
        default=None,
    )
    value_key: Optional[str] = pydantic.Field(
        alias="value-key",
        description="A string contained in command-line, substituted by the input "
        "value and/or flag at runtime.",
        default=None,
    )


class PathTemplateOutput(pydantic.BaseModel):
    """Output using a (basic) path template."""

    path_template: Optional[StringProperty] = pydantic.Field(
        alias="path-template",
        description="Describes the output file path relatively to the execution "
        "directory. May contain input value keys and wildcards. Example: "
        '"results/[INPUT1]_brain*.mnc".',
        default=None,
    )


class ConditionalPathTemplateOutput(pydantic.BaseModel):
    """Output using a conditional path template."""

    conditional_path_template: Optional[list[PathProperty]] = pydantic.Field(
        alias="conditional-path-template",
        description="List of objects containing boolean statement (Limited python "
        "syntax: ==, !=, <, >, <=, >=, and, or) and output file paths relative to "
        "the execution directory, assign path of first true boolean statement. May "
        'contain input value keys, "default" object required if "optional" set to '
        'True . Example list: "[{"[PARAM1] > 8": "outputs/[INPUT1].txt"}, {"default": '
        '"outputs/default.txt"}]".',
        min_length=1,
        default=None,
    )


Output = typing.Union[PathTemplateOutput, ConditionalPathTemplateOutput]


# TODO: I think outputs can also have a few additional properties like 'list'
