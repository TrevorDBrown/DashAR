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
using System.Net.Http.Headers;
using System.Text.Json;

public class DashARDataAggregatorServer
{
    private Guid _id;
    private readonly HttpClient _httpClient;

    public DashARDataAggregatorServer ()
    {
        this._id = Guid.NewGuid();
        this._httpClient = new HttpClient();
    }

    public DashARDataAggregatorServerResponse GetUpdateFromServer()
    {
        this._httpClient.DefaultRequestHeaders.Accept.Clear();
        this._httpClient.DefaultRequestHeaders.Accept.Add(
            new MediaTypeWithQualityHeaderValue("text/json")
        );
        this._httpClient.DefaultRequestHeaders.Add("User-Agent", "DashAR HUD");

        string responseJsonAsString = ""; //TODO: figure this out... -> await this.GetUpdateFromServerAsync(this._httpClient);

        return new DashARDataAggregatorServerResponse(responseJsonAsString);

    }

    // private async Task GetUpdateFromServerAsync(HttpClient client){
    //     string response = await client.GetStringAsync(
    //         "http://127.0.0.1:3000/data/obdii"
    //     );

    //     return response;
    // }




}