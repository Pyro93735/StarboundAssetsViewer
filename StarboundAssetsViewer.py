#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import FileViewer
import DispTree
import DispSheet
try:
    from wx.lib import sheet
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

class MainApp(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title)

        box = wx.GridBagSizer()

        dispSheet = DispSheet.DispSheet(self)
        dispTree = DispTree.DispTree(self, dispSheet)
        filePanel = FileViewer.FilePanel(self, dispTree)

        box.Add(filePanel, (0,0) , (1,1), wx.EXPAND)
        box.Add(dispTree, (0,1), (1,1), wx.EXPAND)
        box.Add(dispSheet, (0,2), (1,1) ,wx.EXPAND)

        box.AddGrowableCol(1)
        box.AddGrowableCol(2)
        box.AddGrowableRow(0)
        self.SetSizerAndFit(box)

        self.CreateStatusBar()
        self.Centre()
        self.Show(True)

        
def main():
    app = wx.App(0)
    MainApp(None, -1, 'StarBooundAssetEditor')
    app.MainLoop()
    
if __name__ == "__main__":
    main()
