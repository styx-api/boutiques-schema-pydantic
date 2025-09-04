"""Pydantic model for Styx frontend."""

from __future__ import annotations

import typing
from typing import Literal, Optional

import pydantic

from .utils import IdStringProperty, StringProperty, ValueKeyStringProperty


class BaseInput(pydantic.BaseModel):
    """Base input model."""

    model_config = pydantic.ConfigDict(extra="forbid")

    id: IdStringProperty = pydantic.Field(
        description="A short, unique, informative identifier "
        "containing only alphanumeric characters and underscores. "
        'Typically used to generate variable names. Example: "data_file".',
    )
    name: Optional[StringProperty] = pydantic.Field(
        description="A human-readable name. Example: 'Data file'.",
        default=None,
    )
    description: Optional[StringProperty] = pydantic.Field(default=None)

    value_key: ValueKeyStringProperty = pydantic.Field(
        alias="value-key",
        description="A string contained in command-line, "
        "substituted by the input value and/or flag at runtime.",
    )


class CommandLineFlagged(pydantic.BaseModel):
    """Input has a command line flag preceding it."""

    model_config = pydantic.ConfigDict(extra="forbid")

    command_line_flag: StringProperty = pydantic.Field(
        alias="command-line-flag",
        description="Option flag, involved in the value-key substitution. "
        'Inputs of type "Flag" have to have a command-line flag. '
        "Examples: -v, --force.",
    )
    command_line_flag_separator: Optional[str] = pydantic.Field(
        alias="command-line-flag-separator",
        description="Separator used between flags and their arguments. "
        "Defaults to a single space.",
        default=None,
    )


class ListInput(pydantic.BaseModel):
    """Input is a list of objects."""

    model_config = pydantic.ConfigDict(extra="forbid")

    list_: Literal[True] = pydantic.Field(
        alias="list",
        description="True if list of values. "
        'If value is of type "Flag" cannot be a list.',
    )
    list_separator: Optional[str] = pydantic.Field(
        alias="list-separator",
        description="Separator used between list items. Defaults to a single space.",
        default=None,
    )
    min_list_entries: Optional[float] = pydantic.Field(
        alias="min-list-entries",
        description="Specify the minimum number of entries in the list. "
        "May only be used with List type inputs.",
        default=None,
    )
    max_list_entries: Optional[float] = pydantic.Field(
        alias="max-list-entries",
        description="Specify the maximum number of entries in the list. "
        "May only be used with List type inputs.",
        default=None,
    )


class StringInput(BaseInput):
    """String input."""

    type_: Literal["String"] = pydantic.Field(alias="type")

    value_choices: Optional[list[str]] = pydantic.Field(
        alias="value-choices",
        description="Permitted choices for input value. "
        "May not be used with the Flag type.",
        default=None,
    )

    default_value: Optional[str] = pydantic.Field(
        alias="default-value",
        description="Default value of the input. "
        "The default value is set when no value is specified, "
        "even when the input is optional. "
        "If the desired behavior is to omit the input from the command line "
        "when no value is specified, "
        "then no default value should be used. "
        "In this case, the tool might still use a default value internally, "
        "but this will remain undocumented in the Boutiques interface.",
        default=None,
    )

    optional: bool = pydantic.Field(description="True if optional", default=False)


class FileInput(BaseInput):
    """File input."""

    type_: Literal["File"] = pydantic.Field(alias="type")

    mutable: bool = pydantic.Field(
        description="Specifies that the tool may modify the input file. "
        "Only specifiable for File type inputs.",
        default=False,
    )
    resolve_parent: bool = pydantic.Field(
        alias="resolve-parent",
        description="Specifies that the full parent directory of this file "
        "needs to be visible to the tool. "
        "Only specifiable for File type inputs.",
        default=False,
    )

    optional: bool = pydantic.Field(description="True if optional", default=False)


class IntegerInput(BaseInput):
    """Integer input."""

    type_: Literal["Number"] = pydantic.Field(alias="type")

    integer: Literal[True] = pydantic.Field(
        description="Specify whether the input should be an integer. "
        "May only be used with Number type inputs.",
        default=True,
    )

    minimum: Optional[int] = pydantic.Field(
        description="Specify the minimum value of the input (inclusive). "
        "May only be used with Number type inputs.",
        default=None,
    )
    maximum: Optional[int] = pydantic.Field(
        description="Specify the maximum value of the input (inclusive). "
        "May only be used with Number type inputs.",
        default=None,
    )

    value_choices: Optional[list[int]] = pydantic.Field(
        alias="value-choices",
        description="Permitted choices for input value. "
        "May not be used with the Flag type.",
        default=None,
    )

    default_value: Optional[int] = pydantic.Field(
        alias="default-value",
        description="Default value of the input. "
        "The default value is set when no value is specified, "
        "even when the input is optional. "
        "If the desired behavior is to omit the input from the command line "
        "when no value is specified, "
        "then no default value should be used. "
        "In this case, the tool might still use a default value internally, "
        "but this will remain undocumented in the Boutiques interface.",
        default=None,
    )

    optional: bool = pydantic.Field(description="True if optional", default=False)


class FloatInput(BaseInput):
    """Float input."""

    type_: Literal["Number"] = pydantic.Field(alias="type")

    integer: Optional[Literal[False]] = pydantic.Field(
        description="Specify whether the input should be an integer. "
        "May only be used with Number type inputs.",
        default=False,
    )

    minimum: Optional[float] = pydantic.Field(
        description="Specify the minimum value of the input (inclusive). "
        "May only be used with Number type inputs.",
        default=None,
    )
    maximum: Optional[float] = pydantic.Field(
        description="Specify the maximum value of the input (inclusive). "
        "May only be used with Number type inputs.",
        default=None,
    )

    default_value: Optional[float] = pydantic.Field(
        alias="default-value",
        description="Default value of the input. "
        "The default value is set when no value is specified, "
        "even when the input is optional. "
        "If the desired behavior is to omit the input from the command line "
        "when no value is specified, "
        "then no default value should be used. "
        "In this case, the tool might still use a default value internally, "
        "but this will remain undocumented in the Boutiques interface.",
        default=None,
    )

    optional: bool = pydantic.Field(description="True if optional", default=False)


class FlagInput(BaseInput):
    """Flag input."""

    type_: Literal["Flag"] = pydantic.Field(alias="type")

    default_value: Optional[bool] = pydantic.Field(
        alias="default-value",
        description="Default value of the input. "
        "The default value is set when no value is specified, "
        "even when the input is optional. "
        "If the desired behavior is to omit the input from the "
        "command line when no value is specified, "
        "then no default value should be used. "
        "In this case, the tool might still use a default value internally, "
        "but this will remain undocumented in the Boutiques interface.",
        default=None,
    )

    command_line_flag: str = pydantic.Field(
        alias="command-line-flag",
        description="Option flag, involved in the value-key substitution. "
        'Inputs of type "Flag" have to have a command-line flag. '
        "Examples: -v, --force.",
    )

    optional: bool = pydantic.Field(
        description="Optional has no meaning for Flag type inputs",
        default=False,
        deprecated=True,
    )


class SubCommand(pydantic.BaseModel):
    """Sub-command attriblutes shared between base descriptor and sub-commands."""

    model_config = pydantic.ConfigDict(extra="forbid")

    command_line: StringProperty = pydantic.Field(
        alias="command-line",
        description="A string that describes the tool command line, where input and "
        'output values are identified by "keys". At runtime, command-line keys are '
        "substituted with flags and values.",
    )

    inputs: Optional[list[Input]] = pydantic.Field(
        description="An array of input objects",
        default=None,
    )
    output_files: Optional[list[Output]] = pydantic.Field(
        alias="output-files",
        default=None,
    )


class SubCommandType(SubCommand):
    """Sub-command specification."""

    id: IdStringProperty = pydantic.Field(
        description="A short, unique, informative identifier "
        "containing only alphanumeric characters and underscores. "
        'Typically used to generate variable names. Example: "data_file".',
    )
    name: Optional[StringProperty] = pydantic.Field(
        description="A human-readable name. Example: 'Data file'.",
        default=None,
    )
    description: Optional[str] = pydantic.Field(default=None)


class SubCommandInput(BaseInput):
    """Sub command."""

    type_: SubCommandType = pydantic.Field(
        description="Sub-command type.", alias="type"
    )

    optional: bool = pydantic.Field(description="True if optional", default=False)


class SubCommandUnionInput(BaseInput):
    """Choice out of a list of possible sub-commands."""

    type_: list[SubCommandType] = pydantic.Field(
        description="Sub-command type union.", alias="type"
    )

    optional: bool = pydantic.Field(description="True if optional", default=False)


class IntegerListInput(IntegerInput, ListInput):
    """List of integers."""

    pass


class FloatListInput(FloatInput, ListInput):
    """List of floats."""

    pass


class StringListInput(StringInput, ListInput):
    """List of strings."""

    pass


class FileListInput(FileInput, ListInput):
    """List of files."""

    pass


class SubCommandListInput(SubCommandInput, ListInput):
    """List of sub-commands."""

    pass


class SubCommandUnionListInput(SubCommandUnionInput, ListInput):
    """List of sub-command unions."""

    pass


class CommandLineFlaggedIntegerInput(IntegerInput, CommandLineFlagged):
    """Integer with a command line flag before it."""

    pass


class CommandLineFlaggedFloatInput(FloatInput, CommandLineFlagged):
    """Float with a command line flag before it."""

    pass


class CommandLineFlaggedStringInput(StringInput, CommandLineFlagged):
    """String with a command line flag before it."""

    pass


class CommandLineFlaggedFileInput(FileInput, CommandLineFlagged):
    """File with a command line flag before it."""

    pass


class CommandLineFlaggedIntegerListInput(IntegerListInput, CommandLineFlagged):
    """List of integers with a command line flag before them."""

    pass


class CommandLineFlaggedFloatListInput(FloatListInput, CommandLineFlagged):
    """List of floats with a command line flag before them."""

    pass


class CommandLineFlaggedStringListInput(StringListInput, CommandLineFlagged):
    """List of strings with a command line flag before them."""

    pass


class CommandLineFlaggedFileListInput(FileListInput, CommandLineFlagged):
    """List of files with a command line flag before them."""

    pass


class CommandLineFlaggedSubCommandInput(SubCommandInput, CommandLineFlagged):
    """Sub-command with a command line flag before it."""

    pass


class CommandLineFlaggedSubCommandListInput(SubCommandListInput, CommandLineFlagged):
    """List of sub-commands with a command line flag before them."""

    pass


class CommandLineFlaggedSubCommandUnionInput(SubCommandUnionInput, CommandLineFlagged):
    """Sub-commands union with a command line flag before it."""

    pass


class CommandLineFlaggedSubCommandUnionListInput(
    SubCommandUnionListInput, CommandLineFlagged
):
    """List of sub-command unions with a command line flag before them."""

    pass


Input = typing.Union[
    FlagInput,
    StringInput,
    FileInput,
    IntegerInput,
    FloatInput,
    StringListInput,
    FileListInput,
    IntegerListInput,
    FloatListInput,
    CommandLineFlaggedStringInput,
    CommandLineFlaggedFileInput,
    CommandLineFlaggedIntegerInput,
    CommandLineFlaggedFloatInput,
    CommandLineFlaggedStringListInput,
    CommandLineFlaggedFileListInput,
    CommandLineFlaggedIntegerListInput,
    CommandLineFlaggedFloatListInput,
    SubCommandInput,
    SubCommandUnionInput,
    SubCommandListInput,
    SubCommandUnionListInput,
    CommandLineFlaggedSubCommandInput,
    CommandLineFlaggedSubCommandListInput,
    CommandLineFlaggedSubCommandUnionInput,
    CommandLineFlaggedSubCommandUnionListInput,
]


class Output(pydantic.BaseModel):
    """Model representing an output file."""

    model_config = pydantic.ConfigDict(extra="forbid")

    id: IdStringProperty = pydantic.Field(
        description="A short, unique, informative identifier "
        "containing only alphanumeric characters and underscores. "
        'Typically used to generate variable names. Example: "data_file".',
    )
    name: Optional[StringProperty] = pydantic.Field(
        description="A human-readable name. Example: 'Data file'.",
        default=None,
    )
    description: Optional[StringProperty] = pydantic.Field(default=None)

    path_template: StringProperty = pydantic.Field(
        alias="path-template",
        description="Describes the output file path relatively to the execution "
        "directory. May contain input value keys and wildcards. Example: "
        '"results/[INPUT1]_brain.mnc".',
    )
    path_template_stripped_extensions: Optional[list[StringProperty]] = pydantic.Field(
        alias="path-template-stripped-extensions",
        description="List of file extensions that will be stripped from the input "
        "values before being substituted in the path template. Example: "
        '[".nii",".nii.gz"].',
        default=None,
    )
    path_template_fallback: Optional[str] = pydantic.Field(
        alias="path-template-fallback",
        description="Fall back to this value if the referenced input is optional and set to None.",
        default=None,
    )


class ContainerImage(pydantic.BaseModel):
    """Model for container image configuration."""

    model_config = pydantic.ConfigDict(extra="forbid")

    type_: Literal["docker"] = pydantic.Field(alias="type")
    image: StringProperty = pydantic.Field(
        description="Name of an image where the tool is installed and configured. "
        "Example: bids/mriqc.",
    )


class StdoutOutput(pydantic.BaseModel):
    """Model for stdout output configuration."""

    model_config = pydantic.ConfigDict(extra="forbid")

    id: IdStringProperty = pydantic.Field(
        description="A short, unique, informative identifier containing "
        "only alphanumeric characters and underscores. "
        'Typically used to generate variable names. Example: "my_output"',
    )
    name: Optional[str] = pydantic.Field(
        description="A human-readable output name. Example: 'My output'",
        min_length=1,
        default=None,
    )
    description: Optional[str] = pydantic.Field(
        description="Output description.",
        default=None,
    )


class StderrOutput(StdoutOutput):
    """Model for stderr output configuration."""

    pass


class Descriptor(SubCommand):
    """Complete Descriptor JSON schema model."""

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
        extra="forbid",
        validate_assignment=True,
    )

    name: StringProperty = pydantic.Field(description="Tool name.")
    description: Optional[StringProperty] = pydantic.Field(
        description="Tool description.",
        default=None,
    )

    # Required fields
    schema_version: Literal["0.5+styx"] = pydantic.Field(alias="schema-version")

    # Optional fields
    author: Optional[StringProperty] = pydantic.Field(
        description="Tool author name(s).",
        default=None,
    )
    url: Optional[pydantic.HttpUrl] = pydantic.Field(
        description="Tool URL.",
        default=None,
    )
    stdout_output: Optional[StdoutOutput] = pydantic.Field(
        alias="stdout-output",
        description="If present the stdout will be treated as a "
        "(string) output itself.",
        default=None,
    )
    stderr_output: Optional[StderrOutput] = pydantic.Field(
        alias="stderr-output",
        description="If present the stderr will be treated as a "
        "(string) output itself.",
        default=None,
    )


SubCommandType.model_rebuild()
SubCommandInput.model_rebuild()
SubCommandUnionInput.model_rebuild()
Descriptor.model_rebuild()
