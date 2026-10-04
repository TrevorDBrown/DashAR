# DashAR: An Augmented Reality-based Heads Up Display for Automobiles

DashAR is an AR-based HUD system for automobiles. It is designed to work with any automobile equipped with and ODBII diagnostic port (i.e. all gasoline powered automobiles manufactured in 1996 and onwards).

This repository is designed to act as a monorepo for all components of the system.

## Repository Structure

### Build

This directory, generated on-the-fly, will, after a successful build, contain all compiled, consolidated executable code for each component of the system. The Data Aggregator and Server (DAS), the HUD, and the HUD Companion app.

### Resources

This directory contains all of the relevant configurations and data necessary for each component of the system to function correctly. These files are copied to the Build directory specific to each component.

### Source

This directory contains all source code related to the DashAR system. This includes the DAS source, the HUD source, and the HUD Companion App source (well... eventually.)

### Templates

This directory contains all templates related to the DashAR system. This includes data and configuration templates (e.g. SQLite files, configuration JSON schemas and examples, etc.), as well as code boilerplate templates (e.g templates for Python code, C# code, etc.).

### Testing

This directory contains data and configurations used for testing the source code. This includes a config for mypy, and copies of the SQLite database used.

### Tools

This directory contains build scripts and other resources needed to successfully build and deploy the DashAR system.

### LICENSES

This directory is strictly for the repository, to indicate additional licenses utilized by components outside of, but utilized by, the DashAR system.

## Documentation

The DashAR system documentation, powered by Docusaurus, is hosted [here](https://dashar.org/), with its source hosted [here](https://github.com/TrevorDBrown/DashAR-Docs). The documentation is a work-in-progress.

## Issues and Enhancements

If you desire to see enhancements, additional functionality, and/or would like to report an issue with the system, please utilize GitHub Issues.

## Disclaimer

The DashAR System is a research-oriented project. It should not be considered a "production ready" system. Please use at your own discretion.

Also, it is highly recommended to avoid use of the DashAR system in hazardous conditions. This includes, but is not limited to:

- Low visibility (i.e. nighttime, foggy)
- Adverse weather (i.e. rain, snow, sleet, hail, tornados, hurricanes, etc.)

A good rule of thumb for determining if the DashAR system can be used safely: would I wear sunglasses right now?

With all of that said... safe and happy driving to you! :)
