#!/bin/sh
#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       DashAR-Buck2Build-Setup.sh
#   Purpose:    Builds the DashAR system, using the buck2 Build System.
#

# Splash Message
echo -e "\nDashAR: an AR-based HUD for Automobiles"
echo "(c)2025-2026 Trevor D. Brown"
echo "Distributed under the MIT License."

echo -e "\nBuilding the DashAR System (using buck2)..."

# Set up variables.
SCRIPT_PATH=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
cd $SCRIPT_PATH
cd "../../"
PROJECT_ROOT=$PWD

# Build DAS executable.
buck2 build //Source/DAS:DashAR-DAS --show-output
