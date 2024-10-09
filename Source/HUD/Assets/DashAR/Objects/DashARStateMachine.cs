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
    private DashARDataAggregatorServer _dasAPI;

    // Gauge List
    private DashARGauge _gaugeSpeed;    // Test Gauge - will eventually be included in _gauges array.
    private List<DashARGauge> _gauges;

    public DashARStateMachine ()
    {
        this._id = Guid.NewGuid();
        this._gaugeSpeed = new DashARGauge("Speedometer", "string", "mph", "current_speed");
        this._gauges = new List<DashARGauge>();
        this._dasAPI = new DashARDataAggregatorServer();
        return;
    }

    public void PollForUpdate()
    {
        string resultFromServer = this._dasAPI.GetUpdateFromServer();
        string displayableValue = this.UpdateGauge(this._gaugeSpeed, resultFromServer);
        return; 
    }

    public string UpdateGauge (DashARGauge gaugeToUpdate, string newValue)
    {
        gaugeToUpdate.Value = newValue;
        return gaugeToUpdate.GetGaugeDisplayValue();
    }

}