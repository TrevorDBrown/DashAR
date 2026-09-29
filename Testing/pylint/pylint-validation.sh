#!/bin/sh
#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       pylint-validation.sh
#

# Splash Message
echo "\nDashAR: an AR-based HUD for Automobiles"
echo "(c)2025-2026 Trevor D. Brown"
echo "Distributed under the MIT License."

echo "\nRunning pylint...\n"

# Set up variables
SCRIPT_PATH=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
cd $SCRIPT_PATH
cd "../../"
PROJECT_ROOT=$PWD
VENV_ROOT="$PROJECT_ROOT/.venv/"
SOURCE_PATH="$PROJECT_ROOT/Source/"
DAS_PATH="$SOURCE_PATH/DAS/"
TESTING_PATH="$PROJECT_ROOT/Testing/"
PYLINTRC_FILE="$TESTING_PATH/pylint/.pylintrc"

"$VENV_ROOT/bin/python3" -m pylint $DAS_PATH --rcfile="$PYLINTRC_FILE"