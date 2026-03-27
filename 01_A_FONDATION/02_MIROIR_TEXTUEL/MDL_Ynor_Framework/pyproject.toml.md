# MIROIR TEXTUEL - pyproject.toml

Source : MDL_Ynor_Framework\pyproject.toml
Taille : 560 octets
SHA256 : 5dfa96dbdfda178fefd8283dc3945a89641c716e40b9f72355110e8f9f80b277

```text
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "mdl-ynor-framework"
version = "0.1.0"
description = "Operational packaging for the MDL Ynor core runtime and API surface."
readme = "README.md"
requires-python = ">=3.10"

[tool.setuptools]
include-package-data = true

[tool.setuptools.packages.find]
include = ["_04_DEPLOYMENT_AND_API*"]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I"]

```