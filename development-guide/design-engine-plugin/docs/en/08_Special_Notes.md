# 8. Special Notes

## 8.1. Notes

### Adding Required Packages for Plugins

You can add third-party Python packages as needed when implementing a plugin.

When adding packages, edit the Layout Design's `pyproject.toml` located at the path below:
- `layout-design-compose/layout-design/layout-design/pyproject.toml`

In `pyproject.toml`, add the required packages to `dependencies` in the `project` section.  
Ensure that your dependencies are consistent with the dependency packages defined on the Layout Design side, including their version constraints.

Below is an excerpt from the Layout Design's `pyproject.toml`:

```toml
[project]
name = "layoutdesign"
version = "0.1.0"
description = ""
authors = [
    {name = "NEC corporation."},
]
dependencies = [        # Add required packages here
    "jsonschema<5.0.0,>=4.23.0",
    "uvicorn<1.0.0,>=0.30.6",
    "fastapi<1.0.0,>=0.115.0",
    "requests>=2.32.3",
    "pyyaml",
    "tenacity>=9.0.0",
]
requires-python = "<4.0,>=3.14.0"
readme = "README.md"
license = {text = "LICENSE"}
```

After adding packages, rebuild the Layout Design container with the command below:

```shell
cd <any directory path>/layout-design-compose
docker compose up [-d] --build
```
