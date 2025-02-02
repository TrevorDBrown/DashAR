/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARStateMachine.cs
 *  Purpose:    This script contains the DashAR HUD State Machine class.
 */

using System;
using System.Collections.Generic;
using UnityEngine;

public class DashARStateMachine : MonoBehaviour
{
    private Guid _id;
    private GameObject _origin;
    private DashARConfiguration _configuration;

    private DashARHUDDevice _hudDevice;
    private DashARDataAggregatorServer _dasAPI;

    private List<DashARGauge> _gauges;      // Built-in gauges include: Speedometer, Tachometer, Fuel Level, and Compass.

    public DashARStateMachine ()
    {
        this._id = Guid.NewGuid();

        // Load the configuration.
        this._configuration = new DashARConfiguration();

        // Contextualize the HUD Device.
        this._hudDevice = new DashARHUDDevice();

        // Establish the entry point for the HUD gauge objects,
        this._origin = GameObject.Find("HUD");

        // Initialize the gauges.
        this._gauges = this._configuration.Gauges;

        // Establish the server connection.
        this._dasAPI = new DashARDataAggregatorServer(this._configuration.DasIp);

        return;
    }

    public async void PollForUpdate()
    {
        // TODO: find way to dynamically handle data retrieval and processing.
        DashARDataAggregatorServerOBDIIResponse responseFromServer = await this._dasAPI.GetUpdateFromServerAsync();

        foreach (DashARGauge currentGauge in this._gauges)
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

            } else if (currentGauge.DataSource == "HUD Device") {
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