#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from wx.lib import sheet
import wx

__name__ = "CustomGui"

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

class DispSheet(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridCellChange)
        self.row = self.col = 0
        self.SetNumberRows(100)
        self.SetNumberCols(2)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.EnableCellEditControl(True)
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
