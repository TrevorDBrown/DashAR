# Testing

This directory contains various scripts for system-wide testing and quabity assuance (I'm sorry.. "_quality assurance_"...) of the DashAR system.

## Python QA

For development of Python resources for DashAR, like the Data Aggregator and Server, we utilize two primary tools: [pylint](https://www.pylint.org/) and [mypy](https://mypy-lang.org/).

pylint is a linter. In the future, we would like to change over to using ruff, since it is built on Rust and is much faster.

mypy is a static type checker.

### pylint

For pylint, we utilize a modified version of Google's Python style guide (.pylintrc).

### mypy

For mypy, we utilize a custom configuration file (.mypy).

## BeamNG

In October 2026, we began experimenting with incorporating BeamNG.drive simulations into DashAR. This would allow users to utilize the HUD without having to leave their gaming chairs. Test and validation scripts are found here.
