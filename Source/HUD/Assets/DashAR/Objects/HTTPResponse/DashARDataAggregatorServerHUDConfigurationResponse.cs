/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARDataAggregatorServerHUDConfigurationResponse.cs
 *  Purpose:    This script contains the response of a HUD configuration request by the DashAR HUD to the DAS.
 */

public class DashARDataAggregatorServerHUDConfigurationResponse
{
    public string current_timestamp { get; set; }
    public string message { get; set; }
}