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
using System.Threading.Tasks;

using Newtonsoft.Json;
using UnityEngine;

public class DashARDataAggregatorServer : MonoBehaviour
{
    private Guid _id;
    private HttpClient _httpClient;

    public DashARDataAggregatorServer ()
    {
        this._id = Guid.NewGuid();
        this._httpClient = new HttpClient();

        this._httpClient.BaseAddress = new Uri("http://localhost:3000/");
    }

    public async Task<DashARDataAggregatorServerResponse> GetUpdateFromServerAsync()
    {
        this._httpClient.DefaultRequestHeaders.Accept.Clear();
        this._httpClient.DefaultRequestHeaders.Accept.Add(
            new MediaTypeWithQualityHeaderValue("application/json")
        );
        this._httpClient.DefaultRequestHeaders.Add("User-Agent", "DashAR HUD");

        string responseInJson = await this.GetAsync("/data/obdii");

        Debug.Log("Response: " + responseInJson);
        
        DashARDataAggregatorServerResponse response = JsonConvert.DeserializeObject<DashARDataAggregatorServerResponse>(responseInJson);

        return response;
    }

    public async Task<string> GetAsync(string uri)
    {
        HttpResponseMessage response = await this._httpClient.GetAsync(uri);
        
        if (response.IsSuccessStatusCode)
        {
            return await response.Content.ReadAsStringAsync();
        }
        else
        {
            return "";
        }
    }

}