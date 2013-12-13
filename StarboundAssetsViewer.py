#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import CustomGui
import Utility
try:
    from wx.lib import sheet
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

class MainApp(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = ( 800, 600))

        box = wx.GridBagSizer()

        self.SetSizer(box)

        self.sheet1 = CustomGui.DispSheet(self)
        self.sheet1.SetFocus()
        self.tree = CustomGui.DispTree(self)
        self.fileSelector = CustomGui.FileViewer(self)
        openButton = wx.Button(self,-1,label="Open")
        saveButton = wx.Button(self,-1,label="Save")		
        openButton.Bind(wx.EVT_BUTTON, self.onOpen)
        saveButton.Bind(wx.EVT_BUTTON, self.onSave)
		
        box.Add(openButton, (0,0))
        box.Add(saveButton, (1,0))
        box.Add(self.fileSelector, (2,0), (1,1), wx.EXPAND)
        box.Add(self.tree, (0,1), (2,1), wx.EXPAND)
        box.Add(self.sheet1, (0,2), (2,1) ,wx.EXPAND)

        self.CreateStatusBar()
        self.Centre()
        self.Show(True)

    def onOpen(self, event): 
        dirText = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           )
        if dirText.ShowModal() == wx.ID_OK:
            self.fileSelector.populate(os.walk(dirText.GetPath()))
        dirText.Destroy()
        
    def onSave(self, event): 
        self.fileSelector.files[self.fileSelector.lastSelected].Save()

def main():
    app = wx.App(0)
    newt = MainApp(None, -1, 'StarBooundAssetEditor')
    myfile = Utility.MyFile("arid.surfacebiome")
    myfile.Open() #arid.surfacebiome platinumdrill.miningtool
    #newt.sheet1.populate(myfile)
    newt.tree.populate(myfile.data)
    app.MainLoop()
    
if __name__ == "__main__":
    main()
