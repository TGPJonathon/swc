# swc

[![Tests](https://github.com/TGPJonathon/swc/workflows/Test/badge.svg)](https://github.com/TGPJonathon/swc/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/TGPJonathon/swc/blob/master/LICENSE)

Reimplementing the wc linux command for a challenge

## Installation

Install this tool using `pip`:

    pip install swc

## Usage

For help, run:

    swc --help

You can also use:

    python -m swc --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd swc
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
