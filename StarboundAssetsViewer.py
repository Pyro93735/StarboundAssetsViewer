#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

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
        print self.data

    def HasAttr(self, key):
        return key in self.data
        
    def Save(self):
        data = json.dumps(self.data, indent=2, separators=(',', ": "))
        print data

    
class DispSheet(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridCellChange)
        self.row = self.col = 0
        self.SetNumberRows(100)-
        self.SetNumberCols(2)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.EnableCellEditControl(False)
        self.EnableGridLines(False)
    
    def populate(self, file):
        self.file = file
        self.Unbind(wx.grid.EVT_GRID_CELL_CHANGE)
        index = 0
        for key in file.data.iterkeys():
            self.SetCellValue(index, 0, str(key))
            self.SetCellValue(index, 1, str(file.data[key]))
            index = index + 1
        self.SetNumberRows(index-1)
        self.AutoSize()
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridCellChange)

    def OnGridCellChange(self, event):
        if hasattr(self, "file"):
            key = self.GetCellValue(event.GetRow(), 0)
            if event.GetCol() > 0: # changing a value
                self.file.data[key] = self.GetCellValue(event.GetRow(), event.GetCol())
            else:                  # changing an attribute
                newkey = self.GetCellValue(event.GetRow(), event.GetCol())
                self.file.data[newkey] = self.file.data.pop(key)
                
            self.file.Save()
        else:
            print "error editing something with no file"

class MainApp(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = ( 650, 600))

        box = wx.GridBagSizer()

        self.SetSizer(box)

        self.sheet1 = DispSheet(self)
        self.sheet1.SetFocus()
        panel2 = wx.Panel(self)
        button = wx.Button(self,-1,label="Select Directory...")		
        button.Bind(wx.EVT_BUTTON, self.onDir)
        panel2.SetBackgroundColour('Red')
		
        box.Add(button, (0,0))
        box.Add(panel2, (1,0), (1,1), wx.EXPAND)
        box.Add(self.sheet1, (0,1), (2,1) ,wx.EXPAND)

        self.CreateStatusBar()
        self.Centre()
        self.Show(True)
		
    def onDir(self, event): 
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           )
        if dlg.ShowModal() == wx.ID_OK:
            for root, dirs, files in os.walk(dlg.GetPath()):
                for file in files:
                    print file
        dlg.Destroy()

app = wx.App(0)
newt = MainApp(None, -1, 'SpreadSheet')
myfile = MyFile()
myfile.Open("platinumdrill.miningtool")
newt.sheet1.populate(myfile)
app.MainLoop()
