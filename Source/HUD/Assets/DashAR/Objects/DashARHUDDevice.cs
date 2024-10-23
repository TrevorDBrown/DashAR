using NRKernal;
using System;
using System.Globalization;
using UnityEngine;

public class DashARHUDDevice : MonoBehaviour
{
    private string _name;
    private NRDeviceType _deviceType;
    private CultureInfo _deviceCulture;

    public DashARHUDDevice()
    {
        this._name = "My HUD Device";
        this._deviceType = NRDeviceType.XrealAIR2_PRO;

        // Enable the device's compass.
        Input.compass.enabled = true;
        Input.location.Start();

        // Determine the locale of the device.
        this._deviceCulture = CultureInfo.CurrentCulture;
    }

    public string GetCompassHeading()
    {
        float compassResult = Input.compass.trueHeading;

        if (compassResult >= 22 && compassResult < 67)
        {
            return "NE";
        }
        else if (compassResult >= 67 && compassResult < 112){
            return "E";
        }
        else if (compassResult >= 112 && compassResult < 157)
        {
            return "SE";
        }
        else if (compassResult >= 157 && compassResult < 202)
        {
            return "S";
        }
        else if (compassResult >= 202 && compassResult < 247)
        {
            return "SW";
        }
        else if (compassResult >= 247 && compassResult < 292)
        {
            return "W";
        }
        else if (compassResult >= 292 && compassResult < 315)
        {
            return "NW";
        }
        else
        {
            return "N";
        }

    }

    public string GetCurrentTime()
    {
        return DateTime.Now.ToLocalTime().ToString("h:mm tt");
    }
}
