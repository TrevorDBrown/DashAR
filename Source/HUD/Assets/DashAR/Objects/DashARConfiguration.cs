/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARConfiguration.cs
 *  Purpose:    This script contains configuration information for the DashAR HUD at runtime.
 */

using System;
using System.Collections.Generic;

class DashARConfiguration
{
    private Guid _id;

    // Configuration Settings
    private string _systemMode;
    private string _dasIP;
    private List<DashARGauge> _gauges;

    public DashARConfiguration()
    {
        this._id = Guid.NewGuid();

        // NOTE: use these to override the host IP inference process.
        //this._dasIP = "192.168.2.1:3832";     // The IP address assigned by my MacBook Pro when sharing my loopback address.
        //this._dasIP = "192.168.3.1:3832";     // The IP address of the network self-hosted by the Raspberry Pi 5.
        this._dasIP = "localhost:3832";         // The local machine (testing on development machine only...)

        // TODO: swap out for parsing of config files with gauge data.
        this._gauges = new List<DashARGauge>();
        this._gauges.Add(new DashARGauge(gaugeName: "Speedometer", gaugeValueType: "string", gaugeUnitOfMeasure: "mph", dataSource: "DAS", dataSourceMappedValue: "current_speed"));
        this._gauges.Add(new DashARGauge(gaugeName: "Tachometer", gaugeValueType: "string", gaugeUnitOfMeasure: "rpms", dataSource: "DAS", dataSourceMappedValue: "current_rpms"));
        this._gauges.Add(new DashARGauge(gaugeName: "Fuel_Level", gaugeValueType: "string", gaugeUnitOfMeasure: "fuel", dataSource: "DAS", dataSourceMappedValue: "current_fuel_level"));
        this._gauges.Add(new DashARGauge(gaugeName: "Compass", gaugeValueType: "string", gaugeUnitOfMeasure: "cardinal", dataSource: "HUD Device", suppressUnitOfMeasureOnDisplay: true));
        this._gauges.Add(new DashARGauge(gaugeName: "Clock", gaugeValueType: "string", gaugeUnitOfMeasure: "time", dataSource: "HUD Device", suppressUnitOfMeasureOnDisplay: true));

        return;
    }

    // Getters
    public List<DashARGauge> Gauges { get { return this._gauges; } }
    public string DasIp { get { return this._dasIP;  } }

}