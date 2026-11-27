import ifcdb
import wx
import BuildingPropertiesDialogImpl
import ctypes
from ctypes import wintypes

def set_mfc_owner(wx_dialog, mfc_hwnd):
    user32 = ctypes.windll.user32
    user32.SetWindowLongPtrW(wintypes.HWND(wx_dialog.GetHandle()), -8, ctypes.c_ssize_t(mfc_hwnd))
    
def start_building_properties_dialog():

    app = wx.App(False)

    document = ifcdb.get_document()
    document.log_message("CityGML Building Properties Editor")

    dlg = BuildingPropertiesDialogImpl.BuildingPropertiesDialogImpl(None)
    set_mfc_owner(dlg, document.get_parent_window())
    dlg.fillData()
    dlg.ShowModal()
    dlg.Destroy()

start_building_properties_dialog()