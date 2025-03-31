#!/bin/bash

#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       Setup-DashAR.sh
#   Purpose:    This script sets up the DashAR System for use on the ICS device.
#

# Splash Message
echo -e "\nDashAR: an AR-based HUD for Automobiles"
echo "(c)2025 Trevor D. Brown"
echo "Distrbuted under the MIT License."

echo -e "\nRunning setup..."

# Set up Path Variables
SCRIPT_PATH=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
cd $SCRIPT_PATH
cd "../../"
PROJECT_ROOT=$PWD

echo -e "\nDashAR's root directory is: $PROJECT_ROOT"

TEMPLATE_DATABASE_PATH=$PROJECT_ROOT/Templates/DAS/dashar-data.sqlite3/dashar-data.sqlite3
DATA_PATH=$PROJECT_ROOT/Source/DAS/data/
PRIVATE_DATA_PATH=$PROJECT_ROOT/Source/DAS/privates/

# Check template files.
# dashar-data.sqlite3
if ! [ -f $TEMPLATE_DATABASE_PATH ]; then
    echo -e "\nError: dashar-data.sqlite3 template does not exist. Exiting."
    exit 2
fi

# Check data directories and files.
# data
if ! [ -d $DATA_PATH ]; then
    mkdir $DATA_PATH
    echo -e "\nWARNING: $DATA_PATH did not exist. It has been created, but it is empty. Please populate this directory with the config.json file, hud/base.json file, and hud/default.json file."
fi

# private
if ! [ -d $PRIVATE_DATA_PATH ]; then
    mkdir $PRIVATE_DATA_PATH
    echo -e "\nINFO: $PRIVATE_DATA_PATH has been created."
fi

# dashar-data.sqlite3 (private)
if ! [ -f $PRIVATE_DATA_PATH/dashar-data.sqlite3 ]; then
    cp $TEMPLATE_DATABASE_PATH $PRIVATE_DATA_PATH/dashar-data.sqlite3
    echo -e "\nINFO: $TEMPLATE_DATABASE_PATH has been copied to $PRIVATE_DATA_PATH."
fi

# Create the Wi-Fi Access Point/Hotspot.
echo -e "\nSetting up persistent Wi-Fi Access Point..."
echo "SSID: DashAR-Network"
echo "Password: ConnectToDashAR"

nmcli device wifi hotspot ssid "DashAR-Network" password "ConnectToDashAR"

echo -e "\nDashAR Setup Complete! Happy Driving!\n"
