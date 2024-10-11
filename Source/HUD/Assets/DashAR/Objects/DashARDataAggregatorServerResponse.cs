/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024 Trevor D. Brown. All rights reserved.
 * This project is distributed under the MIT license.
 *
 *  File:       DashARDataAggregatorServerResponse.cs
 *  Purpose:    This script contains the response of a request by the DashAR HUD interface into the DAS API.
 */

using System;

public class DashARDataAggregatorServerResponse
{
    private Guid _responseId;
    private string _responseSpeed;

    public DashARDataAggregatorServerResponse (string responseJsonAsString){
        this._responseId = Guid.Parse("");
        this._responseSpeed = "";
    }

    public string getSpeed(){
        return this._responseSpeed;
    }

}