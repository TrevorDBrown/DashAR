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
    private DashARDataAggregatorServer _dasAPI;

    // Gauge List
    private DashARGauge _gaugeSpeed;    // Speedometer (Test Gauge) - will eventually be included in _gauges list.
    //private List<DashARGauge> _gauges;

    public DashARStateMachine ()
    {
        this._id = Guid.NewGuid();
        this._origin = GameObject.Find("Origin");

        this._gaugeSpeed = new DashARGauge("Speedometer", "string", "mph", "current_speed");
        //this._gauges = new List<DashARGauge>();
        this._dasAPI = new DashARDataAggregatorServer();

        return;
    }

    public async void PollForUpdate()
    {
        DashARDataAggregatorServerResponse responseFromServer = await this._dasAPI.GetUpdateFromServerAsync();

        this.UpdateGauge(this._gaugeSpeed, responseFromServer.obdii_data.speed);

        return;
    }

    public void UpdateGauge (DashARGauge gaugeToUpdate, string newValue)
    {
        gaugeToUpdate.Value = newValue;
        gaugeToUpdate.SetGaugeDisplayValue();
        return;
    }

}