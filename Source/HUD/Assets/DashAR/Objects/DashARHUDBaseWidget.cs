/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARHUDBaseWidget.cs
 *  Purpose:    This script contains the DashAR HUD Base Widget class.
 */

using System;
using UnityEngine;

public class DashARHUDBaseWidget
{
    Guid _id;

    private string _type;
    private PrimitiveType _shape;
    private Vector3 _scale;
    private Vector3 _position;
    private Vector3 _rotation;

    public DashARHUDBaseWidget(HUDConfigurationBaseWidgetConfiguration baseWidgetConfiguration)
    {
        this._id = Guid.NewGuid();
        this._type = baseWidgetConfiguration.name;
        this._shape = Enum.Parse<PrimitiveType>(baseWidgetConfiguration.primitiveType);

        this._scale = new Vector3((float) baseWidgetConfiguration.relativeTransform.scale[0], (float) baseWidgetConfiguration.relativeTransform.scale[1], (float) baseWidgetConfiguration.relativeTransform.scale[2]);
        this._position = new Vector3((float) baseWidgetConfiguration.relativeTransform.position[0], (float) baseWidgetConfiguration.relativeTransform.position[1], (float) baseWidgetConfiguration.relativeTransform.position[2]);
        this._rotation = new Vector3((float) baseWidgetConfiguration.relativeTransform.rotation[0], (float) baseWidgetConfiguration.relativeTransform.rotation[1], (float) baseWidgetConfiguration.relativeTransform.rotation[2]);

        return;
    }

    public DashARHUDBaseWidget(string baseWidgetType, PrimitiveType baseWidgetShape, Vector3 baseWidgetScale, Vector3 baseWidgetPosition, Vector3 baseWidgetRotation)
    {
        this._type = baseWidgetType;
        this._shape = baseWidgetShape;
        this._scale = baseWidgetScale;
        this._position = baseWidgetPosition;
        this._rotation = baseWidgetRotation;

        return;
    }

    public string Type { get { return _type; } }
    public PrimitiveType Shape { get { return _shape; } }
    public Vector3 Scale { get { return _scale; } }
    public Vector3 Position { get { return _position; } }
    public Vector3 Rotation { get { return _rotation; } }

}