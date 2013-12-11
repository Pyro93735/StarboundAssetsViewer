#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

try:
    from wx.lib import sheet
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

class MyFile():
    #def __init__(self):
        
        
    def Open(self, value):
        self.file = open(value, 'r+') 
        toParse = self.file.read()
        toParse = toParse.replace("true","\"true\"")
        toParse = toParse.replace("false","\"false\"")
        self.data = eval(toParse)

    def HasAttr(self, key):
        return key in self.data
        
    #def Save(self):
        

    
class DispSheet(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridCellChange)
        self.row = self.col = 0
        self.SetNumberRows(100)-
        self.SetNumberCols(2)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
    
    def associate(self, file):
        self.file = file
        self.populate(file.data)
    
    def populate(self, data):
        index = 0
        for i in data.iterkeys():
            self.SetCellValue(index, 0, i)
            self.SetCellValue(index, 1, str(data[i]))
            index = index + 1
        self.SetNumberRows(index-1)
        self.AutoSize()

    def OnGridCellChange(self, event):
        print "you lose"
       # if hasattr(self, file)
        
    
    # def OnGridSelectCell(self, event):
        # self.row, self.col = event.GetRow(), event.GetCol()
        # value =  self.GetColLabelValue(self.col) + self.GetRowLabelValue(self.row)
        # self.SetCellValue(self.row, self.col, value)
        # super(MySheet, self).OnGridSelectCell(event)


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
newt.sheet1.associate(myfile)
app.MainLoop()
