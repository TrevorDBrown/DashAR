/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARConfiguration.cs
 *  Purpose:    This script contains configuration information for the DashAR HUD at runtime.
 */

using System;

public class DashARConfiguration
{
    private Guid _id;

    // General Configuration Settings
    private string _systemMode;
    private string _dasDeviceIP;

    public DashARConfiguration()
    {
        this._id = Guid.NewGuid();

        // Set the IP address of the ICS machine that is running the Data Aggregator and Server (DAS) API.
        // TODO: replace this with a dynamic host 
        this._dasDeviceIP = "192.168.3.1:3832";     // The IP address of the Raspberry Pi on its self-hosted network (DashAR-Network).
        //this._dasDeviceIP = "127.0.0.1:3832";     // The local loopback of the this machine.
        //this._dasDeviceIP = "192.168.2.99:3832";  // The IP address of my development machine, on my network.

        return;
    }

    public string DASDeviceIP { get { return this._dasDeviceIP; } }

}