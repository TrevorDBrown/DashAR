/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARHUDWidget.cs
 *  Purpose:    This script contains the DashAR HUD Widget class.
 */

using System;
using TMPro;
using UnityEngine;

public class DashARHUDWidget
{
    Guid _id;
    private string _name;
    private string _description;
    private string _valueType;
    private string _unitOfMeasure;
    private string _valueString;
    private string _textAlignment;
    private string _dataSource;
    private string _dataSourceMappedValue;
    private bool _suppressUnitOfMeasureOnDisplay;

    private GameObject _gameObject;
    private string _gameObjectName;
    private Vector3 _gameObjectTransform;
    private Vector3 _gameObjectPosition;
    private Vector3 _gameObjectRotation;


    private GameObject _gameObjectText;
    private string _gameObjectTextName;


    // TODO: make extend DashARHUDBaseWidget.
    public DashARHUDWidget(DashARHUDBaseWidget baseWidget, string widgetName, string widgetDescription = "", string widgetDataSource = "", string widgetUnitOfMeasure = "", string widgetDataSourceMappedValue = "", string widgetTextAlignment = "", bool suppressUnitOfMeasureOnDisplay = false, string initializedValue = "-")
    {
        this._id = Guid.NewGuid();
        this._gameObjectName = "Widget_" + widgetName;
        this._gameObjectTextName = this._gameObjectName + "_Text";

        this._name = widgetName;
        this._description = widgetDescription;
        this._unitOfMeasure = widgetUnitOfMeasure;
        this._suppressUnitOfMeasureOnDisplay = suppressUnitOfMeasureOnDisplay;
        this._dataSourceMappedValue = widgetDataSourceMappedValue;
        this._dataSource = widgetDataSource;
        this._textAlignment = widgetTextAlignment;

        // TODO: implement widget construction.
        //this._gameObject = GameObject.Find(this._gameObjectName);
        //this._gameObjectText = GameObject.Find(this._gameObjectTextName);
        //this.UpdateGauge(initializedValue);

        return;
    }

    public string Name
    {
        get { return this._name; }
    }

    public string ValueType
    {
        get { return this._valueType; }
    }

    public string UnitOfMeasure
    {
        get { return this._unitOfMeasure; }
    }

    public string Value
    {
        get { return this._valueString; }
        set { this._valueString = value; }
    }

    public string DataSource
    {
        get { return this._dataSource; }
    }

    public string DataSourceMappedValue
    {
        get { return this._dataSourceMappedValue; }
    }

    public void UpdateGauge(string newValue)
    {
        this.Value = newValue;
        this.SetWidgetDisplayValue();
        return;
    }


    public string GetWidgetDisplayValue()
    {
        if (this._unitOfMeasure == "" || this._suppressUnitOfMeasureOnDisplay){
            return this.Value;
        }

        if (this._textAlignment == "Stacked")
        {
            return this.Value + "\n" + this._unitOfMeasure;
        }

        if (this._textAlignment == "Inline")
        {
            return this.Value + " " + this._unitOfMeasure;
        }

        // Unknown Text Alignment Mode, just return an empty string.
        // TODO: implement error handling, default text alignment mode.
        return "";

    }

    public void SetWidgetDisplayValue()
    {
        TextMeshPro textMeshProComponent = this._gameObjectText.GetComponent<TextMeshPro>();

        textMeshProComponent.text = this.GetWidgetDisplayValue();

        return;
    }

}