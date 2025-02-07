/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARHUDTrayAnchor.cs
 *  Purpose:    This script contains the DashAR HUD Tray Anchor class.
 */

using System;
using UnityEngine;

public class DashARHUDTrayAnchor
{
    Guid _id;
    private GameObject _gameObject;
    private string _name;
    private Vector3 _scale;
    private Vector3 _position;
    private Vector3 _rotation;

    private DashARHUDWidget _anchoredWidget;

    public DashARHUDTrayAnchor(HUDConfigurationBaseTrayAnchor trayAnchorConfiguration, GameObject parent)
    {
        this._id = Guid.NewGuid();
        this._name = trayAnchorConfiguration.name;
        this._gameObject = new GameObject(this._name);

        this._gameObject.transform.parent = parent.transform;

        this._scale = new Vector3((float) trayAnchorConfiguration.scale[0], (float) trayAnchorConfiguration.scale[1], (float) trayAnchorConfiguration.scale[2]);
        this._position = new Vector3((float) trayAnchorConfiguration.position[0], (float) trayAnchorConfiguration.position[1], (float) trayAnchorConfiguration.position[2]);
        this._rotation = new Vector3((float) trayAnchorConfiguration.rotation[0], (float) trayAnchorConfiguration.rotation[1], (float) trayAnchorConfiguration.rotation[2]);

        this._gameObject.transform.localScale = this._scale;
        this._gameObject.transform.localPosition = this._position;
        this._gameObject.transform.Rotate(this._rotation);

        this._anchoredWidget = null;

        return;
    }

    public string Name {  get { return this._name; } }
    
    public GameObject TrayAnchorGameObject { get { return this._gameObject; } }
    
    public DashARHUDWidget AnchoredWidgetGameObject { 
        get { return this._anchoredWidget; } 
        set { this._anchoredWidget = value; }
    }
}