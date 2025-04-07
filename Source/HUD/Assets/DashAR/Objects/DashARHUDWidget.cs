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

public class DashARHUDWidget : DashARHUDBaseWidget
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
    private GameObject _gameObjectText;


    public DashARHUDWidget(DashARHUDBaseWidget baseWidget, DashARHUDTrayAnchor trayAnchor, string widgetName, string widgetDescription = "", string widgetDataSource = "", string widgetUnitOfMeasure = "", string widgetDataSourceMappedValue = "", string widgetTextAlignment = "", bool suppressUnitOfMeasureOnDisplay = false, string initializedValue = "-") : base(baseWidgetType: baseWidget.Type, baseWidgetShape: baseWidget.Shape, baseWidgetScale: baseWidget.Scale, baseWidgetPosition: baseWidget.Position, baseWidgetRotation: baseWidget.Position, baseWidgetTextFontSize: baseWidget.TextFontSize, baseWidgetTextBox: baseWidget.TextBox, baseWidgetTextScale: baseWidget.TextScale)
    {
        this._id = Guid.NewGuid();

        this._name = widgetName;
        this._description = widgetDescription;
        this._suppressUnitOfMeasureOnDisplay = suppressUnitOfMeasureOnDisplay;
        this._dataSourceMappedValue = widgetDataSourceMappedValue;
        this._dataSource = widgetDataSource;
        this._textAlignment = widgetTextAlignment;

        if (widgetUnitOfMeasure == "Degrees")
        {
            // Replace with Degrees Symbol.
            this._unitOfMeasure = "°";
        }
        else
        {
            this._unitOfMeasure = widgetUnitOfMeasure;
        }


        // Create the GameObjects needed for the widget.
        CreateGameObject(this._name, base.Shape, base.Scale, base.Position, base.Rotation, trayAnchor);

        // Initialize the widget's value.
        this.UpdateGauge(initializedValue);

        return;
    }

    private void CreateGameObject(string gameObjectName, PrimitiveType gameObjectPrimitiveType, Vector3 gameObjectScale, Vector3 gameObjectPosition, Vector3 gameObjectRotation, DashARHUDTrayAnchor trayAnchor)
    {
        string gameObjectWidgetName = "Widget_" + gameObjectName;
        string gameObjectWidgetTextName = gameObjectWidgetName + "_Text";

        // Create the Widget GameObject.
        GameObject newGameObject = GameObject.CreatePrimitive(gameObjectPrimitiveType);

        // Set the Tray the Tray Anchor is in as the parent.
        // (NOTE: there were some issues with transforms when the anchor was set as the parent.)
        newGameObject.transform.parent = trayAnchor.TrayAnchorGameObject.transform.parent;

        // Set Widget GameObject properties.
        newGameObject.name = gameObjectWidgetName;
        newGameObject.transform.localScale = base.Scale;
        newGameObject.transform.position = trayAnchor.TrayAnchorGameObject.transform.position;
        newGameObject.transform.rotation = Quaternion.Euler(gameObjectRotation);

        // Disable shadow casting.
        newGameObject.GetComponent<MeshRenderer>().shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;

        // Create the Textbox GameObject.
        GameObject newGameObjectText = new GameObject(gameObjectWidgetTextName);
        TextMeshPro tmpComponent = newGameObjectText.AddComponent<TextMeshPro>();

        newGameObjectText.transform.parent = newGameObject.transform;

        // Textbox GameObject formatting.
        tmpComponent.transform.localPosition = new Vector3(0f, 0f, -1f);
        tmpComponent.transform.rotation = Quaternion.Euler(new Vector3(0f, 0f, 0f));
        tmpComponent.transform.localScale = base.TextScale;

        tmpComponent.GetComponent<RectTransform>().sizeDelta = base.TextBox;
        tmpComponent.fontSize = base.TextFontSize;

        // GameObject formatting.
        Material widgetMaterial = new Material(Shader.Find("Xreal/Instanced-Colored"));
        widgetMaterial.color = new Color(0.9f, 0.9f, 0.9f); // 230/255, or E6E6E6.

        Renderer rendererComponent = newGameObject.GetComponent<Renderer>();
        rendererComponent.receiveShadows = true;
        rendererComponent.material = widgetMaterial;

        this._gameObject = newGameObject;
        this._gameObjectText = newGameObjectText;

        return;
    }

    public string GetWidgetDisplayValue()
    {
        if (this._unitOfMeasure == "" || this._suppressUnitOfMeasureOnDisplay){
            return this.Value;
        }

        if (this._textAlignment == "Stacked")
        {
            return "<align=\"center\"><color=\"black\"><b>" + this.Value + "\n" + this._unitOfMeasure + "</b></color></align>";
        }

        if (this._textAlignment == "Inline")
        {
            return "<align=\"center\"><color=\"black\"><b>" + this.Value + " " + this._unitOfMeasure + "</b></color></align>";
        }

        // Unknown Text Alignment Mode.
        // TODO: implement error handling.
        return "N/A";

    }

    public void SetWidgetDisplayValue()
    {
        TextMeshPro textMeshProComponent = this._gameObjectText.GetComponent<TextMeshPro>();

        textMeshProComponent.text = this.GetWidgetDisplayValue();

        return;
    }

    public void UpdateGauge(string newValue)
    {
        this._valueString = newValue;
        this.SetWidgetDisplayValue();
        return;
    }

    public string Name { get {  return this._name; } }
    public string ValueType { get { return this._valueType; } }
    public string UnitOfMeasure { get { return this._unitOfMeasure; } }
    public string Value { get { return this._valueString; } }
    public string DataSource { get {  return this._dataSource; } }
    public string DataSourceMappedValue { get {  return this._dataSourceMappedValue; } }

}