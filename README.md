# DashAR: An Augmented Reality-based Heads Up Display for Automobiles

DashAR is an AR-based HUD for Automobiles. It is designed to work with any gasoline-powered automobile manufactured during or after 1996 (i.e. OBDII availability).

## Repository Structure

This repository is designed to act as a "monorepo" for all components of the system.

### Directories

#### Source

This directory contains all source code related to the DashAR system. This includes the Data Aggregator and Server (DAS) software, the HUD software, and the HUD Companion App source code.

#### Templates

This directory contains all templates related to the DashAR system. This includes data templates (e.g. database files), configuration templates (e.g. JSON configuration files for each component of the system), and other relevant templates and boilerplate information.

#### Testing

This directory contains data and configurations used for testing the source code. This includes a config for mypy, and copies of the SQLite database used.

## Documentation

The DashAR System Documentation can be found [here](https://github.com/TrevorDBrown/DashAR-Docs). The documentation is a work-in-progress.

## Issues and Enhancements

If you desire to see enhancements, additional functionality, and/or would like to report an issue with the system, please utilize the "Issues" section of this repository.

## Disclaimer

The DashAR System is a research-oriented, work-in-progress project. It is not to be considered a "production ready" system, as of 04/04/2025. Please use at your own discretion.

It is also highly advised to avoid use DashAR in low-visibility conditions. This includes, but is not limited to: nighttime, in adverse weather such as rain, snow, sleet, hail, etc., and in foggy conditions.

A good rule of thumb for determining if the system can be used safely is: "Would I wear sunglasses right now?"
