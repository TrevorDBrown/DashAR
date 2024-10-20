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
using System.Threading.Tasks;

using UnityEngine;

public class DashARStateMachine : MonoBehaviour
{
    private Guid _id;
    private GameObject _origin;

    private DashARHUDDevice _hudDevice;
    private DashARDataAggregatorServer _dasAPI;

    // Gauge List
    private List<DashARGauge> _gauges;      // Built-in gauges include: Speedometer (N), Tachometer (N), Fuel Level (N), and Compass (Y).

    public DashARStateMachine ()
    {
        this._id = Guid.NewGuid();
        this._origin = GameObject.Find("HUD");

        this._gauges = new List<DashARGauge>();
        this._gauges.Add(new DashARGauge(gaugeName: "Speedometer", gaugeValueType: "string", gaugeUnitOfMeasure: "mph", dataSource: "DAS", dataSourceMappedValue: "current_speed"));
        this._gauges.Add(new DashARGauge(gaugeName: "Compass", gaugeValueType: "string", gaugeUnitOfMeasure: "cardinal", dataSource: "HUD Device", suppressUnitOfMeasureOnDisplay: true));

        this._hudDevice = new DashARHUDDevice();
        
        //string httpHost = "http://192.168.3.1:3000/";   // The IP address of the network self-hosted by the Raspberry Pi 5.
        string httpHost = "http://localhost:3000/";     // The local machine (testing on development machine only...)

        this._dasAPI = new DashARDataAggregatorServer(httpHost);

        return;
    }

    public async void PollForUpdate()
    {
        DashARDataAggregatorServerResponse responseFromServer = await this._dasAPI.GetUpdateFromServerAsync();

        foreach (DashARGauge currentGauge in this._gauges)
        {

            if (currentGauge.DataSource == "DAS")
            {
                if (currentGauge.Name == "Speedometer")
                {
                    Debug.Log("Updating speed...");
                    currentGauge.UpdateGauge(responseFromServer.obdii_data.speed);
                }
            } else if (currentGauge.DataSource == "HUD Device") {
                if (currentGauge.Name == "Compass")
                {
                    Debug.Log("Updating compass...");
                    currentGauge.UpdateGauge(this._hudDevice.GetCompassHeading());

                }
            }

        }

        return;
    }
}