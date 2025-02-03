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
    private GameObject _gameObject;
    private GameObject _gameObjectText;
    private string _gameObjectName;
    private string _gameObjectTextName;
    private string _name;
    private string _valueType;
    private string _unitOfMeasure = "";
    private string _valueString = "";
    private string _dataSource = "";
    private string _dataSourceMappedValue;
    private bool _suppressUnitOfMeasureOnDisplay;

    public DashARHUDWidget(string gaugeName, string gaugeValueType, string gaugeUnitOfMeasure = "", string dataSource = "", string dataSourceMappedValue = "", bool suppressUnitOfMeasureOnDisplay = false, string initializedValue = "-")
    {
        this._id = Guid.NewGuid();
        this._gameObjectName = "Widget_" + gaugeName;
        this._gameObjectTextName = this._gameObjectName + "_Text";
        this._gameObject = GameObject.Find(this._gameObjectName);
        this._gameObjectText = GameObject.Find(this._gameObjectTextName);

        this._name = gaugeName;
        this._valueType = gaugeValueType;
        this._unitOfMeasure = gaugeUnitOfMeasure;
        this._suppressUnitOfMeasureOnDisplay = suppressUnitOfMeasureOnDisplay;
        this._dataSourceMappedValue = dataSourceMappedValue;
        this._dataSource = dataSource;

        this.UpdateGauge(initializedValue);

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
        else {
            return this.Value + "\n" + this._unitOfMeasure;
        }

    }

    public void SetWidgetDisplayValue()
    {
        TextMeshPro textMeshProComponent = this._gameObjectText.GetComponent<TextMeshPro>();

        textMeshProComponent.text = this.GetWidgetDisplayValue();

        return;
    }

}