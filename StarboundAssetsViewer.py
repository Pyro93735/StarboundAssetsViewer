#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

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
        self.SetNumberRows(100)
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
        wx.Frame.__init__(self, parent, -1, title, size = ( 550, 500))

        box = wx.GridBagSizer()

        self.SetSizer(box)

        self.sheet1 = DispSheet(self)
        self.sheet1.SetFocus()
        searchbox = wx.TextCtrl(self,-1,value=u"try1",size=(100,20))
        panel2 = wx.Panel(self)
        panel2.SetBackgroundColour('Red')

        box.Add(searchbox, (0,0), (1,1), wx.EXPAND)
        box.Add(panel2, (1,0), (1,1), wx.EXPAND)
        box.Add(self.sheet1, (0,1), (2,1) ,wx.EXPAND)

        self.CreateStatusBar()
        self.Centre()
        self.Show(True)

app = wx.App(0)
newt = MainApp(None, -1, 'SpreadSheet')
myfile = MyFile()
myfile.Open("platinumdrill.miningtool")
newt.sheet1.populate(myfile)
app.MainLoop()