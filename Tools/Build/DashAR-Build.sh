#!/bin/sh
#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       DashAR-Build.sh
#   Purpose:    This script builds the DashAR Project according to the specified build mode flag.
#

# Splash Message
echo "\nDashAR - an AR-based HUD for Automobiles"
echo "(c)2024-2026 Trevor D. Brown"
echo "Distributed under the MIT License."

echo "Building DashAR..."

# Find our way to the project root directory.
SCRIPT_PATH=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
cd $SCRIPT_PATH
cd "../../"
PROJECT_ROOT=$PWD

# Set the Build directories variables.
BUILD_ROOT=$PROJECT_ROOT/Build/
COMPANION_BUILD_PATH=$BUILD_ROOT/Companion/
DAS_BUILD_PATH=$BUILD_ROOT/DAS/
HUD_BUILD_PATH=$BUILD_ROOT/HUD/

# Set the Source directories variables
SOURCE_ROOT=$PROJECT_ROOT/Source/
COMPANION_SOURCE_PATH=$SOURCE_ROOT/Companion/
DAS_SOURCE_PATH=$SOURCE_ROOT/DAS/
HUD_SOURCE_PATH=$SOURCE_ROOT/HUD/

# Set the Testing directories variables.
TESTING_ROOT=$PROJECT_ROOT/Testing/
PYLINT_PATH=$TESTING_ROOT/pylint/
MYPY_PATH=$TESTING_ROOT/mypy/

# Set the Templates directories variables.
TEMPLATES_ROOT=$PROJECT_ROOT/Templates/
DAS_TEMPLATES_PATH=$TEMPLATES_ROOT/DAS/

# Set up DAS-specific variables.
DATABASE_TEMPLATE_PATH=$DAS_TEMPLATES_PATH/dashar-data.sqlite3/dashar-data.sqlite3
DAS_DATA_PATH=$PROJECT_ROOT/Source/DAS/data/
PRIVATE_DATA_PATH=$PROJECT_ROOT/Source/DAS/private/

# Determine Build Mode: DirectScript or pyinstaller
# TODO: implement argv checks and determine which sub-build script to run. Pass in the variables set here too...

# If OS is Linux-based, create the Wi-Fi Access Point/Hotspot.
# TODO: add OS check.
# Create the Wi-Fi Access Point/Hotspot.
echo "\nSetting up persistent Wi-Fi Access Point..."
echo "SSID: DashAR-Network"
echo "Password: ConnectToDashAR"

nmcli device wifi hotspot ssid "DashAR-Network" password "ConnectToDashAR"

echo "\nDashAR Build Complete! Happy Driving!\n"
