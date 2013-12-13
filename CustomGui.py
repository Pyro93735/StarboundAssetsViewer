#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from wx.lib import sheet
import wx
import os
import Utility

__name__ = "CustomGui"

class DispTree(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent, size=(400,600), style=wx.TR_EDIT_LABELS | wx.TR_DEFAULT_STYLE | wx.TR_TWIST_BUTTONS)
        self.parent = parent
        #root = self.AddRoot("Root")
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.ItemActivated)
        
    def ItemActivated(self, event):
        data = self.GetItemData(event.GetItem()).GetData()
        if type(data) is dict or list:
            self.parent.sheet1.populate(event.GetItem(), self)
        else:
            print "trying stuff"
            self.parent.sheet1.populate(self.GetItemParent(event.GetItem()), self)
            #select cell
        
    def populate(self, data):
        self.DeleteAllItems()
        root = self.AddRoot("Root ")
        self.AddToTree(root, data)
        
    def AddToTree(self, itemID, data):
        if type(data) is dict:
            self.SetItemData(itemID, wx.TreeItemData(data))
            self.AppendText(itemID, "{")
            for key, val in  data.iteritems():
                newnode = self.AppendItem(itemID, str(key) + " : ")
                self.AddToTree(newnode, val)
        elif type(data) is list:
            self.SetItemData(itemID, wx.TreeItemData(data))
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
        
    def Children(self,itemID):
        (node,cookie) = self.GetFirstChild(itemID)
        while node.IsOk():
            yield node
            (node, cookie) = self.GetNextChild(itemID, cookie)

class DispSheet(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridCellChange)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnGridCellSelected)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnGridCellDClick)
        self.row = self.col = 0
        self.SetNumberRows(1)
        self.SetNumberCols(2)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.EnableEditing(True)
        #self.EnableCellEditControl(True)
        #self.EnableGridLines(False)

    def populate(self, node, tree):
        self.node = node
        self.tree = tree
        self.data = tree.GetItemData(node).GetData()
        self.SetNumberRows(tree.GetChildrenCount(node, False))
        self.children = []
        self.Unbind(wx.grid.EVT_GRID_CELL_CHANGE)
        for child in tree.Children(node):
            self.children.append(child)   
        index = 0
        if type(self.data) is dict:
            for key in self.data.iterkeys():
                self.SetCellValue(index, 0, str(key))
                self.SetCellValue(index, 1, str(self.data[key]))
                index = index + 1
        else:   #assume type array
            for i in self.data:
                self.SetCellValue(index, 0, str(index))
                self.SetCellValue(index, 1, str(i))
                index = index + 1
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
            
    def OnGridCellSelected(self, event):
        #remove editor
        self.row = event.GetRow()
        self.col = event.GetCol()
        self.SetGridCursor(self.row, self.col)
        self.tree.EnsureVisible(self.children[event.GetRow()])
        self.tree.SelectItem(self.children[event.GetRow()])

    def OnGridCellDClick(self, event):
        self.row = event.GetRow()
        self.col = event.GetCol()
        self.SetGridCursor(self.row, self.col)
        child = self.children[event.GetRow()]
        if self.tree.ItemHasChildren(child):
            self.tree.Expand(child)
            self.populate(child, self.tree)
        else:
            self.EnableCellEditControl()
            self.ShowCellEditControl()
        

class FileViewer(sheet.CSheet):
    def __init__(self, parent):
        self.files = []
        self.parent = parent
        sheet.CSheet.__init__(self, parent)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnFileSelect)
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
                self.files.append(Utility.MyFile(os.path.join(root, file)))
                index = index + 1
                
    def OnFileSelect(self, event):
        self.files[event.GetRow()].Open()
        self.parent.tree.populate(self.files[event.GetRow()].data)
