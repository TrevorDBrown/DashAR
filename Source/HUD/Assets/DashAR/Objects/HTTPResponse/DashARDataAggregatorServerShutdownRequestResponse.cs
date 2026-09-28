/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARDataAggregatorServerOBDIIResponse.cs
 *  Purpose:    This script contains the response of an OBDII data request by the DashAR HUD to the DAS.
 */

public class DashARDataAggregatorServerShutdownRequestResponse
{
    public string current_timestamp { get; set; }
    public string message { get; set; }
    public OBDIIData obdii_data { get; set; }
}