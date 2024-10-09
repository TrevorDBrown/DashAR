/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024 Trevor D. Brown. All rights reserved.
 * This project is distributed under the MIT license.
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
        this._dsm = new DashARStateMachine();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
