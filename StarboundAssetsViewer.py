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
                
	
		   
class DispTree(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent, size=(400,600), style=wx.TR_EDIT_LABELS | wx.TR_DEFAULT_STYLE | wx.TR_TWIST_BUTTONS)
        #root = self.AddRoot("Root")
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.Try1)
        
    def Try1(self, event):
        self.EditLabel(self.GetSelection())
        
    def populate(self, data):
        #clear
        root = self.AddRoot("Root")
        self.AddToTree(root, data)
        
    def AddToTree(self, itemID, data):
        if type(data) is dict:
            self.AppendText(itemID, "{")
            for key, val in  data.iteritems():
                newnode = self.AppendItem(itemID, str(key) + " : ")
                self.AddToTree(newnode, val)
        elif type(data) is list:
            self.AppendText(itemID, "[")
            index = 0
            for item in data:
                if type(item) is dict or type(item) is list:
                    newnode = self.AppendItem(itemID, str(index) + " ")
                    self.AddToTree(newnode, item)
                else:
                    newnode = self.AppendItem(itemID, str(item))
                index = index + 1
        else:
            self.AppendText(itemID, str(data))
            
    def AppendText(self, itemID, text):
        self.SetItemText(itemID, self.GetItemText(itemID) + text)

class MainApp(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = ( 800, 600))

        box = wx.GridBagSizer()

        self.SetSizer(box)

        self.sheet1 = DispSheet(self)
        self.sheet1.SetFocus()
        self.tree = DispTree(self)
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

app = wx.App(0)
newt = MainApp(None, -1, 'SpreadSheet')
myfile = MyFile()
myfile.Open("arid.surfacebiome") #arid.surfacebiome platinumdrill.miningtool
newt.sheet1.populate(myfile)
newt.tree.populate(newt.sheet1.file.data)
app.MainLoop()
