/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARHUDTray.cs
 *  Purpose:    This script contains the DashAR HUD Tray class.
 */

using System;
using System.Collections.Generic;
using System.Linq;
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
    private string _anchorPrefix;
    private List<DashARHUDTrayAnchor> _anchors;

    public DashARHUDTray(HUDConfigurationBaseTray trayConfiguration, GameObject parent)
    {
        this._id = Guid.NewGuid();
        this._name = "Tray_" + trayConfiguration.name;
        
        // Use the first letter in the tray name as the anchor prefix.
        this._anchorPrefix = trayConfiguration.name.Substring(0, 1);

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

        // GameObject formatting.
        Material trayMaterial = new Material(Shader.Find("Xreal/Instanced-Colored"));
        trayMaterial.color = new Color(0.78f, 0.78f, 0.78f); // 200/255, or C8C8C8.

        Renderer rendererComponent = this._gameObject.GetComponent<Renderer>();
        rendererComponent.receiveShadows = true;
        rendererComponent.material = trayMaterial;

        this._anchors = new List<DashARHUDTrayAnchor>();

        foreach (HUDConfigurationBaseTrayAnchor anchorConfiguration in trayConfiguration.anchors)
        {
            DashARHUDTrayAnchor newTrayAnchor = new DashARHUDTrayAnchor(anchorConfiguration, this._gameObject);
            
            this._anchors.Add(newTrayAnchor);
        }

        return;
    }

    public DashARHUDTrayAnchor getTrayAnchor(string trayAnchorName)
    {
        DashARHUDTrayAnchor targetTrayAnchor = this._anchors.FirstOrDefault(ta => ta.Name == trayAnchorName);

        if (targetTrayAnchor == null)
        {
            return null;
        }

        return targetTrayAnchor;
    }

    public string AnchorPrefix { get { return this._anchorPrefix; } }
    public GameObject TrayGameObject {  get { return this._gameObject; } }
    public List<DashARHUDTrayAnchor> TrayAnchors { get { return this._anchors; } }

}