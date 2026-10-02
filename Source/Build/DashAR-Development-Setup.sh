#!/bin/sh
#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       DashAR-Development-Setup.sh
#   Purpose:    Sets up development tools for DashAR.
#

# Splash Message
echo "\nDashAR - an AR-based HUD for Automobiles"
echo "(c)2024-2026 Trevor D. Brown"
echo "Distributed under the MIT License."

echo "\nSetting up development tools..."

# Set up variables.
SCRIPT_PATH=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
cd $SCRIPT_PATH
cd "../../"
PROJECT_ROOT=$PWD

VENV_ROOT=$PROJECT_ROOT/.venv/

PYTHON_REQUIREMENTS_FILE=$PROJECT_ROOT/Source/Build/requirements.txt

# Create the virtual environment.
python3 -m venv $VENV_ROOT

echo "\nPython Virtual Environment created at: $VENV_ROOT"

# Install requirements.
$VENV_ROOT/bin/python3 -m pip install -r $PYTHON_REQUIREMENTS_FILE

echo "\nModules installed from requirements define at: $PYTHON_REQUIREMENTS_FILE"

echo "\nDevelopment tools set up for DashAR System development. Happy coding!\n"