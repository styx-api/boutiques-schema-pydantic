# boutiques-schema-pydantic

A Python package providing Pydantic models for the Boutiques descriptor standard, with automatic JSON Schema generation for VS Code and other integrations.

[![Build](https://github.com/childmindresearch/boutiques-schema-pydantic/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/childmindresearch/boutiques-schema-pydantic/actions/workflows/test.yaml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/childmindresearch/boutiques-schema-pydantic/branch/main/graph/badge.svg?token=22HWWFWPW5)](https://codecov.io/gh/childmindresearch/boutiques-schema-pydantic)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![stability-stable](https://img.shields.io/badge/stability-stable-green.svg)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/childmindresearch/boutiques-schema-pydantic/blob/main/LICENSE)
[![pages](https://img.shields.io/badge/online-schemas-blue)](https://childmindresearch.github.io/boutiques-schema-pydantic)

## Overview

This package provides:

1. Fully typed Pydantic models representing the Boutiques descriptor specification
2. Automatic JSON Schema generation published to GitHub Pages
3. Validation and serialization utilities for Boutiques descriptors
4. VS Code integration for real-time validation and autocompletion

## Installation

```bash
pip install boutiques-schema-pydantic
```

## Usage

### Basic Usage

```python
from boutiques_schema_pydantic.v_0_5 import Descriptor

# Create a descriptor from scratch
descriptor = Descriptor(
    name="my-tool",
    tool_version="0.1.0",
    description="My amazing tool",
    command_line="command [INPUT] [OUTPUT]",
    inputs=[...],
    output_files=[...],
    # other required fields
)

# Validate and export to JSON
descriptor_json = descriptor.model_dump_json(indent=2)
with open("descriptor.json", "w") as f:
    f.write(descriptor_json)

# Load and validate an existing descriptor
with open("existing_descriptor.json", "r") as f:
    loaded_descriptor = Descriptor.model_validate_json(f.read())
```

### Schema Integration with VS Code

This repository automatically publishes JSON Schema files to GitHub Pages, allowing for real-time validation and autocompletion in VS Code.

To use this in VS Code:

1. Add the following to your VS Code `settings.json`:

```json
{
    "json.schemas": [
        {
            "fileMatch": ["descriptors/**/*.json"],
            "url": "https://styx-api.github.io/boutiques-schema-pydantic/boutiques-0.5.json"
        }
    ]
}
```

2. Now when editing any file matching the patterns above, you'll get:
   - Real-time validation
   - Property autocompletion
   - Documentation on hover
   - IntelliSense suggestions

## Development

### Generate Schema Files


```bash
boutiques-schema-generator --help
```

Generate all schemas:

```bash
boutiques-schema-generator-all
```

This will create updated schema files in the `public/` directory.

### Run Tests

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Boutiques](https://boutiques.github.io/) for the descriptor standard
- [Pydantic](https://docs.pydantic.dev/) for the data validation framework