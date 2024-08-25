# Generative AI API

This is an experimental python package to make it easier to work with generative AI GPT-based models in python and is faintly inspired by [aitextgen](https://github.com/minimaxir/aitextgen).

Uses the hatchling and build packages to create a python package that can be installed and used in other projects.

## Build

First open the root directory of the project in a terminal, then run the following command to build the package:

```bash
python -m build
```

## Installation

To install the package, run the following command from the root directory of the project:

```bash
pip install dist/generative_ai_library-0.0.1-py3-none-any.whl
```

or

```bash
pip install dist/generative_ai_library-0.0.1.tar.gz
```

## System Design

![System Design](system_design.png)

