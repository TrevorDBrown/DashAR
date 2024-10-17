/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024 Trevor D. Brown. All rights reserved.
 * This project is distributed under the MIT license.
 *
 *  File:       DashARDataAggregatorServerResponse.cs
 *  Purpose:    This script contains the response of a request by the DashAR HUD interface into the DAS API.
 */

using System;

public class OBDIIData
{
    public string speed { get; set; }    
}

public class DashARDataAggregatorServerResponse
{
    public string current_timestamp { get; set; }
    public OBDIIData obdii_data { get; set; }

}