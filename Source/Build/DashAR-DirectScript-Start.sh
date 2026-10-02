#!/bin/sh
#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       DashAR-DirectScript-Start.sh
#   Purpose:    This script starts DAS API for the DashAR System, using Direct Script mode.
#

# Splash Message
echo "\nDashAR - an AR-based HUD for Automobiles"
echo "(c)2024-2026 Trevor D. Brown."
echo "Distributed under the MIT License."

echo "\nStarting the DashAR System (in Direct Script mode)...\n"

# Set up variables
SCRIPT_PATH=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
cd $SCRIPT_PATH
cd "../../"

# Path Variables
PROJECT_ROOT=$PWD
VENV_ROOT="$PROJECT_ROOT/.venv/"
SOURCE_ROOT="$PROJECT_ROOT/Source/"
DAS_ROOT="$SOURCE_ROOT/DAS/"

cd $DAS_ROOT
$VENV_ROOT/bin/python3 $DAS_ROOT/das_service.py
