# Build

This directory contains various scripts, configurations, and other files needed for the DashAR system setup.

## Build Modes

### Direct Script

Direct Script mode is how the DashAR system was originally designed to be deployed and utilized: simply call the scripts in-place to run everything. While this is effective for rapid development, it definitely has its costs and difficulties for long-term maintenance. The scripts associated with Direct Script mode are prefixed with "DashAR-DirectScript-".

### buck2 Build

In an effort to make the build process more robust, the [buck2 Build System (from Meta)](https://buck2.build/) is utilized. The scripts associated with buck2 Build mode are prefixed with "DashAR-Buck2Build-".
