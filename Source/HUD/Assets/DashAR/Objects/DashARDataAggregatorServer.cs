/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024 Trevor D. Brown. All rights reserved.
 * This project is distributed under the MIT license.
 *
 *  File:       DashARDataAggregatorServer.cs
 *  Purpose:    This script contains the DashAR HUD interface into the DAS API.
 */

using System;
using System.Net.Http;

public class DashARDataAggregatorServer
{
    private Guid _id;
    private readonly HttpClient _httpClient;

    public DashARDataAggregatorServer ()
    {
        this._id = Guid.NewGuid();
    }

    public string GetUpdateFromServer()
    {
        return "";
    }


}