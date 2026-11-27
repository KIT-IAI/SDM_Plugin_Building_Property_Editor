import BuildingPropertiesDialog
import BuildingProperties
import ifcdb
import wx

class BuildingPropertiesObserver(ifcdb.PopulationObserver):

    def __init__(self, dialog):
        super().__init__()
        self.dialog = dialog

    def select_entity(self, oid, selected):
        self.dialog.select_entity(oid, selected)

class BuildingPropertiesDialogImpl(BuildingPropertiesDialog.BuildingPropertiesDialog):

    def __init__(self, parent):

        self.CurrentBuilding = None

        BuildingPropertiesDialog.BuildingPropertiesDialog.__init__(self, parent)

        self.properties = BuildingProperties.BuildingProperties(self)

        self.observer = BuildingPropertiesObserver(self)

        ifcdb.register_population_observer(self.observer)

    def __del__(self):
        pass

    def Destroy(self):
        ifcdb.unregister_population_observer(self.observer)
        self.observer = None

        return super().Destroy()

    def select_entity(self, oid, selected):
        if selected:
            self.fillData()
        else:
            self.clearData()

    def OnGmlIdChanged(self, event):
        self.properties.mark_changed("gml:id")
        self.m_buttonUpdateData.Enable(True)

    def OnFunctionChanged(self, event):
        self.properties.mark_changed("bldg:function")
        self.m_buttonUpdateData.Enable(True) 

    def OnYearOfConstructionChanged(self, event):
        self.properties.mark_changed("bldg:yearOfConstruction")
        self.m_buttonUpdateData.Enable(True)

    def OnRoofTypeChanged(self, event):
        self.properties.mark_changed("bldg:roofType")
        self.m_buttonUpdateData.Enable(True)

    def OnBuildingHeightChanged(self, event):
        self.properties.mark_changed("bldg:measuredHeight")
        self.m_buttonUpdateData.Enable(True)

    def OnStoreyAboveGroundChanged(self, event):
        self.properties.mark_changed("bldg:storeysAboveGround")
        self.m_buttonUpdateData.Enable(True)

    def OnStoreyHeightsAboveGroundChanged(self, event):
        self.properties.mark_changed("bldg:storeyHeightsAboveGround")
        self.m_buttonUpdateData.Enable(True)

    def OnStoreyBelowGroundChanged(self, event):
        self.properties.mark_changed("bldg:storeysBelowGround")
        self.m_buttonUpdateData.Enable(True)

    def OnStoreyHeightsBelowGroundChanged(self, event):
        self.properties.mark_changed("bldg:storeyHeightsBelowGround")
        self.m_buttonUpdateData.Enable(True)

    def OnButtonUpdateData(self, event):
        self.storeData()

    def get_selected_building(self):
        document = ifcdb.get_document()
        selected_entities = document.get_selected_entities()

        if not selected_entities:
            return None

        if len(selected_entities) != 1:
            wx.MessageBox("Please select only one building or buildng part!", "Warning", wx.OK | wx.ICON_EXCLAMATION)
            return None

        entity = selected_entities[0]

        if entity.type not in ["bldg:Building", "bldg:BuildingPart"]:
            wx.MessageBox("Selected entity is not a building or building part!", "Warning", wx.OK | wx.ICON_EXCLAMATION)
            return None

        return entity

    def clearData(self):
        
        self.CurrentBuilding = None
        self.clear_text_controls(self)
        
    def clear_text_controls(self, parent):
        for child in parent.GetChildren():
            if isinstance(child, wx.TextCtrl):
                child.Clear()
            else:
                self.clear_text_controls(child)
                
    def fillData(self):
        
        building = self.get_selected_building()
        
        if building == None:
            
            self.clearData()
            
        else :

            self.m_elementType.SetValue(building.type)
            
            self.CurrentBuilding = building
            self.properties.fill(building)
                        
    def storeData(self):

        if self.CurrentBuilding is None:

            wx.MessageBox("No building data available!", "Warning", wx.OK | wx.ICON_EXCLAMATION)
            return

        if not self.properties.store(self.CurrentBuilding):

            wx.MessageBox("Invalid property value!", "Input Error", wx.OK | wx.ICON_ERROR)

        self.m_buttonUpdateData.Enable(False)