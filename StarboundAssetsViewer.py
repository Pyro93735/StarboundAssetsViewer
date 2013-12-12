#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import DispSheet
import DispTree
try:
    from wx.lib import sheet
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"
    
import json

class MyFile():
    #def __init__(self):

    def Open(self, fileLocation):
        self.loc = fileLocation
        file = open(fileLocation, 'r') 
        toParse = file.read()
        file.close()
        self.data = json.loads(toParse)

    def HasAttr(self, key):
        return key in self.data
        
    def Save(self):
        data = json.dumps(self.data, indent=2, separators=(',', ": "))
        print data
     

            
class FileViewer(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.SetNumberRows(0)
        self.SetNumberCols(1)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.EnableCellEditControl(False)
        
    def populate(self, results):
        index = 0
        for root, dirs, files in results:
            for file in files:
                self.InsertRows(index)
                self.SetCellValue(index, 0, file)
                index = index + 1
                
	
		   

class MainApp(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = ( 800, 600))

        box = wx.GridBagSizer()

        self.SetSizer(box)

        self.sheet1 = DispSheet.DispSheet(self)
        self.sheet1.SetFocus()
        self.tree = DispTree.DispTree(self)
        self.fileSelector = FileViewer(self)
        button = wx.Button(self,-1,label="Select Directory...")		
        button.Bind(wx.EVT_BUTTON, self.onDir)
		
        box.Add(button, (0,0))
        box.Add(self.fileSelector, (1,0), (1,1), wx.EXPAND)
        box.Add(self.tree, (0,1), (2,1), wx.EXPAND)
        box.Add(self.sheet1, (0,2), (2,1) ,wx.EXPAND)

        self.CreateStatusBar()
        self.Centre()
        self.Show(True)

    def onDir(self, event): 
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self.fileSelector.populate(os.walk(dlg.GetPath()))
        dlg.Destroy()

def main():
    app = wx.App(0)
    newt = MainApp(None, -1, 'SpreadSheet')
    myfile = MyFile()
    myfile.Open("arid.surfacebiome") #arid.surfacebiome platinumdrill.miningtool
    #newt.sheet1.populate(myfile)
    newt.tree.populate(myfile.data)
    app.MainLoop()
    
if __name__ == "__main__":
    main()
