#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import FileViewer
import DispTree
import DispSheet
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

        self.sheet1 = DispSheet.DispSheet(self)
        self.sheet1.SetFocus()
        self.tree = DispTree.DispTree(self)
        self.fileSelector = FileViewer.FileViewer(self)
        self.fileSelector.SetMinSize((150,600))
        openButton = wx.Button(self,-1,label="Open", size=(50,20))
        saveButton = wx.Button(self,-1,label="Save", size=(50,20))
        clearButton = wx.Button(self,-1,label="Clear", size=(50,20))
        openButton.Bind(wx.EVT_BUTTON, self.onOpen)
        saveButton.Bind(wx.EVT_BUTTON, self.onSave)
        searchBox = wx.TextCtrl(self)
		
        
        box.Add(searchBox, (0,0), (1,3), wx.EXPAND)
        box.Add(openButton, (1,0), (1,1), wx.EXPAND)
        box.Add(saveButton, (1,1), (1,1), wx.EXPAND)
        box.Add(clearButton, (1,2), (1,1), wx.EXPAND)
        box.Add(self.fileSelector, (2,0), (1,3), wx.EXPAND)
        box.Add(self.tree, (0,3), (3,1), wx.EXPAND)
        box.Add(self.sheet1, (0,4), (3,1) ,wx.EXPAND)

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
    app.MainLoop()
    
if __name__ == "__main__":
    main()
