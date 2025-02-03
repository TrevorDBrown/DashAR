/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARDevice.cs
 *  Purpose:    This script contains data and functions related to the DashAR AR/HUD device.
 */

using NRKernal;
using System;
using System.Globalization;
using UnityEngine;

public class DashARDevice : MonoBehaviour
{
    private Guid _id;
    private NRDeviceType _deviceType;
    private CultureInfo _deviceCulture;

    public DashARDevice()
    {
        // Define the device parameters.
        this._id = Guid.NewGuid();
        this._deviceType = NRDeviceType.XrealAIR2_PRO;

        // Enable the device's compass.
        Input.compass.enabled = true;
        Input.location.Start();

        // Determine the locale of the device.
        this._deviceCulture = CultureInfo.CurrentCulture;
    }

    public string GetCompassHeading(bool showDegrees = false)
    {
        float compassResult = Input.compass.trueHeading;
        string compassString = "";

        if (showDegrees)
        {
            compassString = "\n" + compassResult.ToString("0") + "�";
        }

        // Translate compass degree ranges into headings.
        if (compassResult >= 22 && compassResult < 67)
        {
            return "NE" + compassString;
        }
        else if (compassResult >= 67 && compassResult < 112){
            return "E" + compassString;
        }
        else if (compassResult >= 112 && compassResult < 157)
        {
            return "SE" + compassString;
        }
        else if (compassResult >= 157 && compassResult < 202)
        {
            return "S" + compassString;
        }
        else if (compassResult >= 202 && compassResult < 247)
        {
            return "SW" + compassString;
        }
        else if (compassResult >= 247 && compassResult < 292)
        {
            return "W" + compassString;
        }
        else if (compassResult >= 292 && compassResult < 315)
        {
            return "NW" + compassString;
        }
        else
        {
            return "N" + compassString;
        }

    }

    public string GetCurrentTime()
    {
        return DateTime.Now.ToLocalTime().ToString("h:mm tt");
    }
}
