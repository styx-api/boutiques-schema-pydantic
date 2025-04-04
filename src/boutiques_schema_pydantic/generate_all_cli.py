"""Script to generate all available Boutiques JSON schemas
and save them to the public directory for GitHub Pages.
"""

import json
import os
import sys

# Add the project root to the path so we can import the CLI module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import from the CLI module
from .cli import ALL_NAMES, get_schema


def main():
    """Generate all schemas and save them to the public directory"""
    output_dir = "public"
    os.makedirs(output_dir, exist_ok=True)

    for schema_name in ALL_NAMES:
        output_path = os.path.join(output_dir, f"{schema_name}.json")
        try:
            schema = get_schema(schema_name)
            with open(output_path, "w") as f:
                json.dump(schema, f, indent=2)
            print(f"✅ Exported {schema_name} to {output_path}")
        except Exception as e:
            print(f"❌ Error exporting {schema_name}: {str(e)}", file=sys.stderr)
            sys.exit(1)

    print(f"\n📦 All schemas successfully generated in '{output_dir}' directory")


if __name__ == "__main__":
    main()
