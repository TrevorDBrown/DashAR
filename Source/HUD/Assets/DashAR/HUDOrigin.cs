/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       HUDOrigin.cs
 *  Purpose:    This script is the entry point for the application.
 */

using System.Collections;
using UnityEngine;

public class HUDOrigin : MonoBehaviour
{
    private DashARStateMachine _dsm;

    // Start is called before the first frame update.
    void Start()
    {
        // Initialize the DashAR State Machine.
        this._dsm = new DashARStateMachine();

        // Set up the HUD.
        this._dsm.GetHUDConfigurationFromServer();

        StartCoroutine(UpdateHUDRepeatedly());
    }

    // Polls for data updates every n seconds.
    IEnumerator UpdateHUDRepeatedly()
    {
        while (true)
        {
            UpdateHUD();
            yield return new WaitForSeconds(0.1f);
        }
    }

    // Polls for data updates.
    void UpdateHUD()
    {
        this._dsm.PollForDataUpdates();
    }

    // When the HUD application is closed.
    private void OnApplicationQuit()
    {
        // Application is quitting, so shut down the DAS server connection.
        this._dsm.SignalServerShutdown();
        return;
    }
}
