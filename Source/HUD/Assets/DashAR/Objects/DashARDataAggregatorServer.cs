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
using System.Net.NetworkInformation;
using System.Net.Sockets;
using System.Text.RegularExpressions;
using Newtonsoft.Json;
using UnityEngine;
using System.Linq;
using TMPro;

public class DashARDataAggregatorServer
{
    private Guid _id;
    private HttpClient _httpClient;
    private NetworkInterface _networkInterface;
    private string _httpHostIpAddress;
    private string _deviceIPAddress;
    private DateTime _lastSuccessfulPoll;

    public DashARDataAggregatorServer (string httpHost = "")
    {
        this._id = Guid.NewGuid();

        this._httpHostIpAddress = GetServerIPAddress(httpHost);

        //GameObject ipGO = GameObject.Find("Widget_IP");
        //TextMeshPro ipGOText = ipGO.GetComponent<TextMeshPro>();
        //ipTextToDisplay += "Device IP: " + this._deviceIPAddress + "\n" + "Server IP: " + this._httpHostIpAddress;
        //ipGOText.text = ipTextToDisplay;

        this._httpClient = new HttpClient();
        string httpBaseAddress = "http://" + this._httpHostIpAddress + "/";
        this._httpClient.BaseAddress = new Uri(httpBaseAddress);

        this._lastSuccessfulPoll = DateTime.Now;

        return;
    }

    private string GetServerIPAddress(string providedHttpHostIpAddress = "")
    {

        //string ipAddressRetrieved = "";

        if (providedHttpHostIpAddress == "" || providedHttpHostIpAddress == null)
        {
            // TODO: the following method does not work on XREAL. Find a different way! 
            // Infer the IP address of the server, using the IP address of the device.
            // (e.g. same subnet, host 1 - 192.168.3.128 -> 192.168.3.1)
            foreach (NetworkInterface netInterface in NetworkInterface.GetAllNetworkInterfaces())
            {

                // Get the IP Properties of the adapter.
                //IPInterfaceProperties ipProperties_Test = netInterface.GetIPProperties();
                //UnicastIPAddressInformation unicastIpAddressInformationResult_Test = ipProperties_Test.UnicastAddresses.FirstOrDefault(x => x.Address.AddressFamily == AddressFamily.InterNetwork);
                //ipAddressRetrieved += unicastIpAddressInformationResult_Test.Address.ToString() + "\n";

                // Since the target device only supports WiFi, no need to check other Network Interface types.
                if ((netInterface.NetworkInterfaceType == NetworkInterfaceType.Wireless80211) && (this._deviceIPAddress == "" || this._deviceIPAddress == null))
                {
                    // Get the IP Properties of the adapter.
                    IPInterfaceProperties ipProperties = netInterface.GetIPProperties();

                    UnicastIPAddressInformation unicastIpAddressInformationResult = ipProperties.UnicastAddresses.FirstOrDefault(x => x.Address.AddressFamily == AddressFamily.InterNetwork);

                    string potentialIpAddress = unicastIpAddressInformationResult.Address.ToString();

                    // Check for invalid IP Address (i.e. IP Address Prefixed with "169")
                    if (potentialIpAddress.StartsWith("169"))
                    {
                        // Invalid IP, ignore.
                        continue;
                    }
                    else
                    {
                        // Valid IP.
                        // Storing the network adapter, for future use.
                        this._networkInterface = netInterface;

                        // This is our current IP.
                        this._deviceIPAddress = potentialIpAddress;

                        // Infer the server IP.
                        Regex ipPrefixRegex = new Regex("^([0-9]+.[0-9]+.[0-9]+.)");
                        Match ipPrefixMatch = ipPrefixRegex.Match(potentialIpAddress);
                        string ipPrefix = ipPrefixMatch.Value;
                        string ipHostSegment = "1";
                        string ipPortSegment = "3832";

                        // Assume the first host in the subnet is the right host.
                        return ipPrefix + ipHostSegment + ":" + ipPortSegment;

                    }
                }
            }
        }
        else
        {
            // Manually provided IP address overrides inference process.
            return providedHttpHostIpAddress;
        }

        // No connections found, treat as localhost run.
        return "127.0.0.1:3832";

        //return ipAddressRetrieved;

    }

    public async Task<DashARDataAggregatorServerResponse> GetUpdateFromServerAsync()
    {
        this._httpClient.DefaultRequestHeaders.Accept.Clear();
        this._httpClient.DefaultRequestHeaders.Accept.Add(
            new MediaTypeWithQualityHeaderValue("application/json")
        );
        this._httpClient.DefaultRequestHeaders.Add("User-Agent", "DashAR HUD");

        string responseInJson = await this.GetAsync("/data/obdii");

        return JsonConvert.DeserializeObject<DashARDataAggregatorServerResponse>(responseInJson);
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
            // TODO: implement error handling.
            return "";
        }
    }

}