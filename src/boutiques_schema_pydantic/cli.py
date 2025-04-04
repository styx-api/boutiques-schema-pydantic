"""CLI used to."""

import argparse
import json
from typing import Any

NAME_BOUTIQUES_0_5 = "boutiques-0.5"
NAME_BOUTIQUES_STYX_DESCRIPTOR_1 = "boutiques-styx-descriptor-1"

ALL_NAMES = [
    NAME_BOUTIQUES_0_5,
    # NAME_BOUTIQUES_STYX_DESCRIPTOR_1,
]


def export_boutiques_0_5() -> dict[str, Any]:
    """Export the Boutiques 0.5 JSON Schema."""
    from boutiques_schema_pydantic.v_0_5.schema import Descriptor

    return Descriptor.model_json_schema()


def get_schema(schema_name: str) -> dict[str, Any]:
    """Get a schema by name."""
    if schema_name == NAME_BOUTIQUES_0_5:
        return export_boutiques_0_5()
    # elif schema_name == NAME_BOUTIQUES_STYX_DESCRIPTOR_1:
    #    return export_boutiques_styx_descriptor_1()
    else:
        raise ValueError(f"Unknown schema: {schema_name}")


def main() -> None:
    """Main."""
    all_names_human = " or ".join([f"'{name}'" for name in ALL_NAMES])

    parser = argparse.ArgumentParser(description="Export Boutiques JSON Schema")
    parser.add_argument(
        "schema",
        choices=ALL_NAMES,
        help=f"Schema to export as JSON Schema ({all_names_human})",
    )
    parser.add_argument(
        "-o", "--output", help="Output file path (if not specified, prints to stdout)"
    )
    args = parser.parse_args()

    result = get_schema(args.schema)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Results written to {args.output}")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
