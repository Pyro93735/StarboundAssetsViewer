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

SAVEFILE = "save.sae"
    
class MainApp(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = ( 800, 600))

        box = wx.GridBagSizer()
        self.baseDirs = []
        self.SetSizer(box)

        self.sheet1 = DispSheet.DispSheet(self)
        self.sheet1.SetFocus()
        self.tree = DispTree.DispTree(self)
        self.fileSelector = FileViewer.FileViewer(self)
        self.fileSelector.SetMinSize((150,600))
        #clearButton = wx.BitmapButton(self, -1, bitmap=wx.Image('clear.ico', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), size=(20,20))
        openButton = wx.Button(self,-1,label="Open", size=(37,20))
        saveButton = wx.Button(self,-1,label="Save", size=(37,20))
        clearButton = wx.Button(self,-1,label="Clear", size=(37,20))
        loadButton = wx.Button(self,-1,label="Load", size=(37,20))
        openButton.Bind(wx.EVT_BUTTON, self.onOpen)
        saveButton.Bind(wx.EVT_BUTTON, self.onSave)
        clearButton.Bind(wx.EVT_BUTTON, self.onClear)
        loadButton.Bind(wx.EVT_BUTTON, self.onLoad)
        searchBox = wx.TextCtrl(self)
		
        
        box.Add(searchBox, (0,0), (1,4), wx.EXPAND)
        box.Add(openButton, (1,0), (1,1), wx.EXPAND)
        box.Add(loadButton, (1,1), (1,1), wx.EXPAND)
        box.Add(saveButton, (1,2), (1,1), wx.EXPAND)
        box.Add(clearButton, (1,3), (1,1), wx.EXPAND)
        box.Add(self.fileSelector, (2,0), (1,4), wx.EXPAND)
        box.Add(self.tree, (0,4), (3,1), wx.EXPAND)
        box.Add(self.sheet1, (0,5), (3,1) ,wx.EXPAND)

        self.CreateStatusBar()
        self.Centre()
        self.Show(True)

    def onOpen(self, event): 
        dirText = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           )
        if dirText.ShowModal() == wx.ID_OK:
            self.baseDirs.append(dirText.GetPath())
            self.fileSelector.populate(os.walk(dirText.GetPath()))
        dirText.Destroy()
        
    def onLoad(self, file):
        savefile = Utility.MyFile(SAVEFILE)
        savefile.Open()
        self.baseDirs = savefile.data[:] #make a copy instead of reference
        for file in self.baseDirs:
            self.fileSelector.populate(os.walk(file))

    def onSave(self, event):
        savefile = Utility.MyFile(SAVEFILE)
        savefile.data = self.baseDirs[:]
        savefile.Save()

    def onClear(self, event):
        self.fileSelector.cleanUp()
        
def main():
    app = wx.App(0)
    newt = MainApp(None, -1, 'StarBooundAssetEditor')
    app.MainLoop()
    
if __name__ == "__main__":
    main()
