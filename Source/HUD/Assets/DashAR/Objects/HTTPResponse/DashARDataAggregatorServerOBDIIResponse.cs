/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARDataAggregatorServerOBDIIResponse.cs
 *  Purpose:    This script contains the response of an OBDII data request by the DashAR HUD to the DAS.
 */

using System.Net;
using System.Xml.Linq;

public class OBDIIData
{
    public string speed { get; set; }
    public string rpms { get; set; }
    public string fuel_level { get; set; }
}

public class DashARDataAggregatorServerOBDIIResponse
{
    public string current_timestamp { get; set; }
    public string message { get; set; }
    public OBDIIData obdii_data { get; set; }

    public override string ToString()
    {
        string output_string = $"Capture Time: {this.current_timestamp}\n";
        output_string += $"API Message: {this.message}\n";
        output_string += $"Speed: {this.obdii_data.speed}\n";
        output_string += $"RPMs: {this.obdii_data.rpms}\n";
        output_string += $"Fuel Level (%): {this.obdii_data.fuel_level}\n";
        return output_string;
    }
}