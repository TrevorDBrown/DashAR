/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARHUDTray.cs
 *  Purpose:    This script contains the DashAR HUD Tray class.
 */

using System;
using System.Collections.Generic;
using UnityEngine;

public class DashARHUDTray
{
    Guid _id;
    private GameObject _gameObject;
    private string _name;
    private PrimitiveType _shape;
    private Vector3 _scale;
    private Vector3 _position;
    private Vector3 _rotation;
    private List<DashARHUDTrayAnchor> _anchors;

    public DashARHUDTray(HUDConfigurationBaseTray trayConfiguration, GameObject parent)
    {
        this._id = Guid.NewGuid();
        this._name = "Tray_" + trayConfiguration.name;
        this._shape = Enum.Parse<PrimitiveType>(trayConfiguration.shape);

        this._gameObject = GameObject.CreatePrimitive(this._shape);
        this._gameObject.name = this._name;

        this._gameObject.transform.parent = parent.transform;
        
        this._scale = new Vector3((float) trayConfiguration.scale[0], (float) trayConfiguration.scale[1], (float) trayConfiguration.scale[2]);
        this._position = new Vector3((float) trayConfiguration.position[0], (float) trayConfiguration.position[1], (float) trayConfiguration.position[2]);
        this._rotation = new Vector3((float) trayConfiguration.rotation[0], (float) trayConfiguration.rotation[1], (float) trayConfiguration.rotation[2]);

        this._gameObject.transform.localScale = this._scale;
        this._gameObject.transform.position = this._position;
        this._gameObject.transform.Rotate(this._rotation);
        
        this._anchors = new List<DashARHUDTrayAnchor>();

        foreach (HUDConfigurationBaseTrayAnchor anchorConfiguration in trayConfiguration.anchors)
        {
            DashARHUDTrayAnchor newTrayAnchor = new DashARHUDTrayAnchor(anchorConfiguration, this._gameObject);
            
            this._anchors.Add(newTrayAnchor);
        }

        return;
    }

    public GameObject TrayGameObject {  get { return this._gameObject; } }

}