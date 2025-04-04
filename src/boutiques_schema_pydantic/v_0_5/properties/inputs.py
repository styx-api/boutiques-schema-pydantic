"""Model for Boutiques descriptor inputs property."""

import typing
from typing import Annotated, Any, Literal, Optional, Union

import pydantic

from .. import StringProperty


class BaseInput(pydantic.BaseModel):
    """Base input model."""

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

    requires_inputs: Optional[list[str]] = pydantic.Field(
        alias="requires-inputs",
        description="Ids of the inputs or ids of groups "
        "whose members must be active for this input to be available.",
        default=None,
    )
    disables_inputs: Optional[list[str]] = pydantic.Field(
        alias="disables-inputs",
        description="Ids of the inputs that are disabled when this input is active.",
        default=None,
    )
    value_key: str = pydantic.Field(
        alias="value-key",
        description="A string contained in command-line, "
        "substituted by the input value and/or flag at runtime.",
    )
    value_requires: Optional[Any] = pydantic.Field(
        description="Ids of the inputs that are required "
        "when the corresponding value choice is selected.",
        default=None,
        deprecated=True,
    )
    value_enables: Optional[Any] = pydantic.Field(
        description="Ids of the inputs that are enabled "
        "when the corresponding value choice is selected.",
        default=None,
        deprecated=True,
    )
    value_disables: Optional[Any] = pydantic.Field(
        description="Ids of the inputs that are disabled "
        "when the corresponding value choice is selected.",
        default=None,
        deprecated=True,
    )


class CommandLineFlagged(pydantic.BaseModel):
    """Input has a command line flag preceding it."""

    command_line_flag: str = pydantic.Field(
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

    type_: Union[Literal["String"]] = pydantic.Field(alias="type")

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

    type_: Union[Literal["File"]] = pydantic.Field(alias="type")

    uses_absolute_path: bool = pydantic.Field(
        alias="uses-absolute-path",
        description="Specifies value must be given as an absolute path.",
        default=False,
    )

    optional: bool = pydantic.Field(description="True if optional", default=False)


class IntegerInput(BaseInput):
    """Integer input."""

    type_: Union[Literal["Number"]] = pydantic.Field(alias="type")

    integer: Literal[True] = pydantic.Field(
        description="Specify whether the input should be an integer. "
        "May only be used with Number type inputs.",
        default=True,
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
    exclusive_minimum: bool = pydantic.Field(
        alias="exclusive-minimum",
        description="Specify whether the minimum is exclusive or not. "
        "May only be used with Number type inputs.",
        default=False,
    )
    exclusive_maximum: bool = pydantic.Field(
        alias="exclusive-maximum",
        description="Specify whether the maximum is exclusive or not. "
        "May only be used with Number type inputs.",
        default=False,
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

    type_: Union[Literal["Number"]] = pydantic.Field(alias="type")

    integer: Optional[Literal[False]] = pydantic.Field(
        description="Specify whether the input should be an integer. "
        "May only be used with Number type inputs.",
        default=False,
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

    type_: Union[Literal["Flag"]] = pydantic.Field(alias="type")

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


class IntegerListInput(IntegerInput, ListInput):
    """List of integers."""

    pass


class FloatListInput(IntegerInput, ListInput):
    """List of floats."""

    pass


class StringListInput(IntegerInput, ListInput):
    """List of strings."""

    pass


class FileListInput(FileInput, ListInput):
    """List of files."""

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
]
