/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARDataAggregatorServerResponse.cs
 *  Purpose:    This script contains the response of a request by the DashAR HUD interface into the DAS API.
 */

public class OBDIIData
{
    public string speed { get; set; }
    public string rpms { get; set; }
    public string fuel_level { get; set; }
}

public class DashARDataAggregatorServerResponse
{
    public string current_timestamp { get; set; }
    public string message { get; set; }
    public OBDIIData obdii_data { get; set; }
}