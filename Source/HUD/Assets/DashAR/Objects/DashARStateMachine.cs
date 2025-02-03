/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARStateMachine.cs
 *  Purpose:    This script contains the DashAR HUD State Machine class.
 */

using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using UnityEngine;

public class DashARStateMachine
{
    // General
    private Guid _id;

    // System Configuration
    private DashARConfiguration _configuration;

    // System Devices
    private DashARDevice _hudDevice;
    private DashARDataAggregatorServer _dasDevice;

    // HUD
    private DashARDataAggregatorServerHUDConfigurationResponse _hudConfiguration;
    private DashARHUD _hud;

    public DashARStateMachine ()
    {
        this._id = Guid.NewGuid();

        // Load the system configuration.
        this._configuration = new DashARConfiguration();

        // Set up the DAS connection.
        this._dasDevice = new DashARDataAggregatorServer(this._configuration.DASDeviceIP);

        // Contextualize the HUD Device.
        this._hudDevice = new DashARDevice();

        return;
    }

    public async void GetHUDConfigurationFromServer()
    {
        DashARDataAggregatorServerHUDConfigurationResponse hudConfigurationResponse = await this._dasDevice.GetHUDConfigurationFromServerAsync();
        this._hudConfiguration = hudConfigurationResponse;
        this._hud = new DashARHUD(this._hudConfiguration);
        return;
    }

    public async void PollForDataUpdates()
    {
        // TODO: find way to dynamically handle data retrieval and processing.
        DashARDataAggregatorServerOBDIIResponse responseFromServer = await this._dasDevice.GetOBDIIDataFromServerAsync();

        foreach (DashARHUDWidget currentGauge in this._hud.Widgets)
        {
            if (currentGauge.DataSource == "DAS")
            {
                if (currentGauge.Name == "Speedometer")
                {
                    currentGauge.UpdateGauge(responseFromServer.obdii_data.speed);
                }

                if (currentGauge.Name == "Tachometer")
                {
                    currentGauge.UpdateGauge(responseFromServer.obdii_data.rpms);
                }

                if (currentGauge.Name == "Fuel_Level")
                {
                    if (responseFromServer.obdii_data.fuel_level != "-1%")
                    {
                        currentGauge.UpdateGauge(responseFromServer.obdii_data.fuel_level);
                    }
                }

            }
            else if (currentGauge.DataSource == "HUD Device")
            {
                if (currentGauge.Name == "Compass")
                {
                    currentGauge.UpdateGauge(this._hudDevice.GetCompassHeading(showDegrees: true));

                }
                else if (currentGauge.Name == "Clock")
                {
                    currentGauge.UpdateGauge(this._hudDevice.GetCurrentTime());
                }
            }

        }

        return;
    }
}