# Build

This directory contains various scripts, configurations, and other files needed for the DashAR system build process.

## Build Modes

There are two primary build modes available for the project: Direct Script and pyinstaller Build.

### Direct Script

Direct Script mode is how the DashAR system was originally designed to be deployed and utilized: simply call the scripts in-place to run everything.

While this is effective for rapid development, it definitely has its costs and difficulties for long-term maintenance. The scripts associated with Direct Script mode are prefixed with "DashAR-DirectScript-". This method is not recommended, and will be most likely removed from a future version of the project.

### Bundled Build

In an effort to make the build process more robust, this build mode produces executables rather than a set of scripts. For the Data Aggregator and Server, pyinstaller is utilized.

The scripts associated with the pyinstaller Build mode are prefixed with "DashAR-Bundled-". This is currently the preferred build method.

### buck2 Build

I'd eventually like to get to a place where we would utilize the [buck2 Build System by Meta](https://buck2.build/). The scripts associated with the buck2 Build mode are prefixed with "DashAR-buck2Build-".
