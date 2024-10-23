/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024 Trevor D. Brown. All rights reserved.
 * This project is distributed under the MIT license.
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

    private DashARHUDDevice _hudDevice;
    private DashARDataAggregatorServer _dasAPI;

    private List<DashARGauge> _gauges;      // Built-in gauges include: Speedometer (N), Tachometer (N), Fuel Level (N), and Compass (Y).

    public DashARStateMachine ()
    {
        this._id = Guid.NewGuid();

        // Contextualize the HUD Device.
        this._hudDevice = new DashARHUDDevice();

        // Establish the entry point for the HUD gauge objects,
        this._origin = GameObject.Find("HUD");

        // Initialize the gauges.
        // TODO: swap out for parsing of config files with gauge data.
        this._gauges = new List<DashARGauge>();
        this._gauges.Add(new DashARGauge(gaugeName: "Speedometer", gaugeValueType: "string", gaugeUnitOfMeasure: "mph", dataSource: "DAS", dataSourceMappedValue: "current_speed"));
        this._gauges.Add(new DashARGauge(gaugeName: "Compass", gaugeValueType: "string", gaugeUnitOfMeasure: "cardinal", dataSource: "HUD Device", suppressUnitOfMeasureOnDisplay: true));
        this._gauges.Add(new DashARGauge(gaugeName: "Clock", gaugeValueType: "string", gaugeUnitOfMeasure: "time", dataSource: "HUD Device", suppressUnitOfMeasureOnDisplay: true));

        // NOTE: use these to override the host IP inference process.
        //string httpHost = "192.168.2.1:3832";   // The IP address assigned by my MacBook Pro when sharing my loopback address.
        string httpHost = "192.168.3.1:3832";   // The IP address of the network self-hosted by the Raspberry Pi 5.
        //string httpHost = "localhost:3832";     // The local machine (testing on development machine only...)
        //string httpHost = "";

        this._dasAPI = new DashARDataAggregatorServer(httpHost);

        return;
    }

    public async void PollForUpdate()
    {
        foreach (DashARGauge currentGauge in this._gauges)
        {
            if (currentGauge.DataSource == "DAS")
            {
                DashARDataAggregatorServerResponse responseFromServer = await this._dasAPI.GetUpdateFromServerAsync();

                if (currentGauge.Name == "Speedometer")
                {
                    currentGauge.UpdateGauge(responseFromServer.obdii_data.speed);
                }
            } else if (currentGauge.DataSource == "HUD Device") {
                if (currentGauge.Name == "Compass")
                {
                    currentGauge.UpdateGauge(this._hudDevice.GetCompassHeading());

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