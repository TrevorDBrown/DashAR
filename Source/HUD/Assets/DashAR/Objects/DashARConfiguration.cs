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

        // TODO: replace this with a dynamic host.
        //this._dasDeviceIP = "127.0.0.1:3832";         // The local machine (testing on development machine only...)
        //this._dasDeviceIP = "192.168.2.1:3832";     // The IP address assigned by my MacBook Pro when sharing my loopback address.
        this._dasDeviceIP = "192.168.3.1:3832";     // The IP address of the network self-hosted by the Raspberry Pi 5.

        return;
    }

    public string DASDeviceIP { get { return this._dasDeviceIP;  } }

}