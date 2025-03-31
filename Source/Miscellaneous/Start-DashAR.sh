#!/bin/bash

#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       Start-DashAR.sh
#   Purpose:    This script starts DAS API for the DashAR System.
#

# Set up variables
SCRIPT_PATH=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
cd $SCRIPT_PATH
cd "../../"
PROJECT_ROOT=$PWD

# Replace the following with the path to the DashAR Project.
cd $PROJECT_ROOT/DashAR/Source/DAS/

# Replace the following with the path to your Python virtual environment and the path to the DashAR project, respectively.
"[REPLACE ME WITH PATH TO VENV]/bin/python3" $PROJECT_ROOT/Source/DAS/das_service.py
