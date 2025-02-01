/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       HUD.cs
 *  Purpose:    This script contains the DashAR HUD class.
 */

using UnityEngine;

public class HUD : MonoBehaviour
{

    private DashARStateMachine _dsm;

    // Start is called before the first frame update
    void Start()
    {
        // Initialize the DashAR State Machine.
        this._dsm = new DashARStateMachine();
    }

    // Update is called once per frame
    void Update()
    {
        if (Time.frameCount % 5 == 0)
        {
            this._dsm.PollForUpdate();
        }
    }
}
