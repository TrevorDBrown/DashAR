/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARHUD.cs
 *  Purpose:    This script contains the DashAR HUD class.
 */

using System;
using System.Collections.Generic;
using UnityEngine;

public class DashARHUD
{
    // General
    private Guid _id;

    // HUD Environment
    private GameObject _origin;
    private List<DashARHUDTray> _trays;
    private List<DashARHUDBaseWidget> _baseWidgets;
    private List<DashARHUDWidget> _widgets;

    public DashARHUD(DashARDataAggregatorServerHUDConfigurationResponse hudConfiguration)
    {
        this._id = Guid.NewGuid();

        // Initialize the lists.
        this._trays = new List<DashARHUDTray>();
        this._baseWidgets = new List<DashARHUDBaseWidget>();
        this._widgets = new List<DashARHUDWidget>();

        // Set up the camera.
        GameObject camera = GameObject.Find("NRCameraRig");
        camera.transform.localScale = new Vector3(1f, 1f, 1f);
        camera.transform.position = new Vector3(0f, 0f, 0f);

        // Set up the origin.
        this._origin = GameObject.Find(hudConfiguration.hud_configuration_base.origin);
        this._origin.transform.localScale = new Vector3(1f, 1f, 1f);
        this._origin.transform.localPosition = new Vector3(0f, 0f, 0.5f);

        // Set up the Trays.
        foreach (HUDConfigurationBaseTray trayConfiguration in hudConfiguration.hud_configuration_base.trays)
        {
            DashARHUDTray newTray = new DashARHUDTray(trayConfiguration, this._origin);
            this._trays.Add(newTray);
        }

        // Set up the Base Widgets.
        foreach (HUDConfigurationBaseWidgetConfiguration baseWidgetConfiguration in hudConfiguration.hud_configuration_base.widgetConfigurations)
        {
            this._baseWidgets.Add(new DashARHUDBaseWidget(baseWidgetConfiguration));
        }

        // Set up the Widgets.
        foreach (HUDConfigurationWidget widgetConfiguration in hudConfiguration.hud_configuration_widgets)
        {
            // TODO: implement the following:
            // - Check the widget's tray anchor position. If empty, use it. Otherwise, throw an error.
            // - Find the Base Widget type. If found, use its transform properties. Otherwise, throw an error.
            // - Create the widget instance, using the transform properties of the base widget.
        }

        // TODO: swap out for parsing of config files with gauge data.
        //this._widgets = new List<DashARHUDWidget>();
        //this._widgets.Add(new DashARHUDWidget(gaugeName: "Speedometer", gaugeValueType: "string", gaugeUnitOfMeasure: "mph", dataSource: "DAS", dataSourceMappedValue: "current_speed"));
        //this._widgets.Add(new DashARHUDWidget(gaugeName: "Tachometer", gaugeValueType: "string", gaugeUnitOfMeasure: "rpms", dataSource: "DAS", dataSourceMappedValue: "current_rpms"));
        //this._widgets.Add(new DashARHUDWidget(gaugeName: "Fuel_Level", gaugeValueType: "string", gaugeUnitOfMeasure: "fuel", dataSource: "DAS", dataSourceMappedValue: "current_fuel_level"));
        //this._widgets.Add(new DashARHUDWidget(gaugeName: "Compass", gaugeValueType: "string", gaugeUnitOfMeasure: "cardinal", dataSource: "HUD Device", suppressUnitOfMeasureOnDisplay: true));
        //this._widgets.Add(new DashARHUDWidget(gaugeName: "Clock", gaugeValueType: "string", gaugeUnitOfMeasure: "time", dataSource: "HUD Device", suppressUnitOfMeasureOnDisplay: true));

        return;
    }

    public List<DashARHUDWidget> Widgets { get { return this._widgets; } }
}