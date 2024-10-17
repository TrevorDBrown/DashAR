/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024 Trevor D. Brown. All rights reserved.
 * This project is distributed under the MIT license.
 *
 *  File:       DashARGauge.cs
 *  Purpose:    This script contains the DashAR HUD Gauge class.
 */

using System;
using TMPro;
using UnityEngine;

public class DashARGauge
{
    Guid _id;
    private GameObject _gameObject;
    private string _gameObjectName;
    private string _name;
    private string _valueType;
    private string _unitOfMeasure;
    private string _valueString = "";
    private string _dasDataMappedValue;
    
    public DashARGauge(string gaugeName, string gaugeValueType, string gaugeUnitOfMeasure, string dasDataMappedValue)
    {
        this._id = Guid.NewGuid();
        this._gameObjectName = "Widget_" + gaugeName;
        this._gameObject = GameObject.Find(this._gameObjectName);

        this._name = gaugeName;
        this._valueType = gaugeValueType;
        this._unitOfMeasure = gaugeUnitOfMeasure;
        this._dasDataMappedValue = dasDataMappedValue;
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

    public string GetGaugeDisplayValue()
    {
        return this._valueString + "\n" + this._unitOfMeasure;
    }

    public void SetGaugeDisplayValue()
    {
        string textGameObjectName = this._gameObjectName + "_Text";
        GameObject textObject = GameObject.Find(textGameObjectName);

        TextMeshPro textMeshProComponent = textObject.GetComponent<TextMeshPro>();

        Debug.Log("Current Text: " + textMeshProComponent.text);

        textMeshProComponent.text = this.GetGaugeDisplayValue();

        Debug.Log("New Text: " + textMeshProComponent.text);
        
        return;
    }

}