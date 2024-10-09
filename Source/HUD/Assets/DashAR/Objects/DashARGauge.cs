/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024 Trevor D. Brown. All rights reserved.
 * This project is distributed under the MIT license.
 *
 *  File:       DashARGauge.cs
 *  Purpose:    This script contains the DashAR HUD Gauge class.
 */

using System;

public class DashARGauge
{
    Guid _id;
    private string _name;
    private string _valueType;
    private string _unitOfMeasure;
    private string _valueString = "";
    private string _dasDataMappedValue;
    
    public DashARGauge(string gaugeName, string gaugeValueType, string gaugeUnitOfMeasure, string dasDataMappedValue)
    {
        this._id = Guid.NewGuid();
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

}