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
            // Check the Anchor Position's availability.
            foreach (DashARHUDTray currentTray in this._trays)
            {
                foreach (DashARHUDTrayAnchor currentAnchor in currentTray.TrayAnchors)
                {
                    if (currentAnchor.Name != widgetConfiguration.anchorPosition)
                    {
                        continue;
                    }

                    if (currentAnchor.AnchoredWidgetGameObject != null)
                    {
                        // The anchor is occupied.
                        // TODO: determine error handling strategy.
                        continue;
                    }

                    // The Tray Anchor is free. Widget is safe to make.
                    // Verify the Base Widget exists.
                    string newWidgetBaseWidgetType = widgetConfiguration.type;
                    // TODO: make object nullable.
                    string newWidgetBaseWidgetTemporaryName = Guid.NewGuid().ToString();

                    DashARHUDBaseWidget newWidgetBaseWidget = new DashARHUDBaseWidget(widgetName: newWidgetBaseWidgetType);

                    foreach (DashARHUDBaseWidget currentBaseWidget in this._baseWidgets)
                    {
                        if (currentBaseWidget.Name != newWidgetBaseWidgetType)
                        {
                            continue;
                        }

                        // Base Widget Found.
                        newWidgetBaseWidget = currentBaseWidget;

                        // Construct the Widget.
                        string newWidgetName = widgetConfiguration.name;
                        string newWidgetDescription = widgetConfiguration.description;
                        string newWidgetDataSource = widgetConfiguration.dataSource;
                        string newWidgetUnitOfMeasure = widgetConfiguration.unitOfMeasure;
                        string newWidgetTextAlignment = widgetConfiguration.textAlignment;

                        DashARHUDWidget newWidget = new DashARHUDWidget(
                            baseWidget: newWidgetBaseWidget,
                            widgetName: newWidgetName,
                            widgetDescription: newWidgetDescription,
                            widgetDataSource: newWidgetDataSource,
                            widgetUnitOfMeasure: newWidgetUnitOfMeasure,
                            widgetTextAlignment: newWidgetTextAlignment
                        );

                        this._widgets.Add(newWidget);

                        // TODO: implement searching methods within the respective lists without having to loop.
                        break;

                    }

                    if (newWidgetBaseWidget.Name == newWidgetBaseWidgetTemporaryName)
                    {
                        // TODO: Base Widget Not Found.
                        // Implement error handling.
                    }
                }
            }

            // TODO: implement the following:
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