/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARHUD.cs
 *  Purpose:    This script contains the DashAR HUD class.
 */

using System;
using System.Collections.Generic;
using System.Linq;
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
            string anchorPrefix = widgetConfiguration.anchorPosition.Substring(0, 1);

            DashARHUDTray targetTray = this._trays.FirstOrDefault(t => t.AnchorPrefix == anchorPrefix);

            if (targetTray == null) {
                // Tray does not exist.
                // TODO: implement error handling.
            }

            DashARHUDTrayAnchor targetTrayAnchor = targetTray.TrayAnchors.FirstOrDefault(ta => ta.Name == widgetConfiguration.anchorPosition);

            if (targetTrayAnchor == null)
            {
                // Tray Anchor does not exist.
                // TODO: implement error handling.
            }

            if (targetTrayAnchor.AnchoredWidgetGameObject != null)
            {
                // Tray Anchor is occupied.
                // TODO: implement error handling.
            }

            DashARHUDBaseWidget baseWidget = this._baseWidgets.FirstOrDefault(bw => bw.Type == widgetConfiguration.type);

            if (baseWidget == null)
            {
                // Base Widget Not Found. 
                // TODO: implement error handling.
            }

            // Construct the Widget.
            string newWidgetName = widgetConfiguration.name;
            string newWidgetDescription = widgetConfiguration.description;
            string newWidgetDataSource = widgetConfiguration.dataSource;
            string newWidgetUnitOfMeasure = widgetConfiguration.unitOfMeasure;
            string newWidgetTextAlignment = widgetConfiguration.textAlignment;

            DashARHUDWidget newWidget = new DashARHUDWidget(
                baseWidget: baseWidget,
                trayAnchor: targetTrayAnchor,
                widgetName: newWidgetName,
                widgetDescription: newWidgetDescription,
                widgetDataSource: newWidgetDataSource,
                widgetUnitOfMeasure: newWidgetUnitOfMeasure,
                widgetTextAlignment: newWidgetTextAlignment
            );

            // Associate the Widget with the Tray Anchor.
            targetTrayAnchor.AnchoredWidgetGameObject = newWidget;

            // Add widget to list.
            this._widgets.Add(newWidget);

        }

        return;
    }

    public List<DashARHUDWidget> Widgets { get { return this._widgets; } }
}