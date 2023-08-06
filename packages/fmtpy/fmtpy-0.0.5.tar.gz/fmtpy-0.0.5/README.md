# fmtpy

Uses [yapf](https://github.com/google/yapf) and [autoflake](https://github.com/PyCQA/autoflake) to format python files, but with properly sorted import statements.

## Requirements

- [Python>=3.6](https://www.python.org/downloads/)

## Installation

```
pip install fmtpy
```

## Usage

```
usage: fmtpy [-h] [-s {pep8,google,yapf,facebook}] [-i] [-o] [-n] [-k]
             files [files ...]

positional arguments:
  files                 files to format

optional arguments:
  -h, --help            show this help message and exit
  -s {pep8,google,yapf,facebook}, --style {pep8,google,yapf,facebook}
                        Formatting style
  -i, --in-place        Make changes in-place
  -o, --only-imports    Only return sorted import statements
  -n, --show-line-numbers
                        Render a column for line numbers
  -k, --keep-external-unused-imports
                        Keep the import statement of external unused modules
```

## Examples

[![Examples](static/examples.gif)](https://asciinema.org/a/QwXWTTnU95Fw2YFihSWVVvR8F)
