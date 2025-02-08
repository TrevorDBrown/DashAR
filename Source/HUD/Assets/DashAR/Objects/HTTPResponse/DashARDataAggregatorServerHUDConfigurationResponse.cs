/*
 * DashAR - An AR-based HUD for Automobiles.
 * (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
 *
 *  File:       DashARDataAggregatorServerHUDConfigurationResponse.cs
 *  Purpose:    This script contains the response of a HUD configuration request 
 *              by the DashAR HUD application to the DAS.
 */

using System.Collections.Generic;

public class HUDConfigurationBaseTrayAnchor
{
    public string name { get; set; }
    public float[] scale { get; set; }
    public float[] position { get; set; }
    public float[] rotation { get; set; }
}

public class HUDConfigurationBaseTray
{
    public string name { get; set; }
    public string shape { get; set; }
    public float[] scale { get; set; }
    public float[] position { get; set; }
    public float[] rotation { get; set; }
    public List<HUDConfigurationBaseTrayAnchor> anchors { get; set; }
}

public class HUDConfigurationBaseWidgetConfigurationRelativeTransform
{
    public float[] scale { get; set; }
    public float[] position { get; set; }
    public float[] rotation { get; set; }
}

public class HUDConfigurationBaseWidgetConfigurationTextRelativeTransform
{
    public float fontSize { get; set; }
    public float[] box { get; set; }
    public float[] scale { get; set; }
}

public class HUDConfigurationBaseWidgetConfiguration
{
    public string name { get; set; }
    public string primitiveType { get; set; }
    public HUDConfigurationBaseWidgetConfigurationRelativeTransform relativeTransform { get; set; }
    public HUDConfigurationBaseWidgetConfigurationTextRelativeTransform textRelativeTransform { get; set; }
}

public class HUDConfigurationBase
{
    public string origin { get; set; }
    public string targetConfiguration { get; set; }
    public List<HUDConfigurationBaseTray> trays { get; set; }
    public List<HUDConfigurationBaseWidgetConfiguration> widgetConfigurations { get; set; }
}

public class HUDConfigurationWidget
{
    public string name { get; set;}
    public string description { get; set;}
    public string dataSource { get; set; }
    public string unitOfMeasure {  get; set; }
    public string textAlignment {  get; set; }
    public string type { get; set; }
    public string anchorPosition { get; set; }
}

public class DashARDataAggregatorServerHUDConfigurationResponse
{
    public string current_timestamp { get; set; }
    public HUDConfigurationBase hud_configuration_base { get; set; }
    public List<HUDConfigurationWidget> hud_configuration_widgets { get; set; }
}