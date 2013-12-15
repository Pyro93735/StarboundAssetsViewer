from wx.lib import sheet
import wx
import os
import Utility

__name__ = "DispSheet"

class DispSheet(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridCellChange)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnGridCellSelected)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnGridCellDClick)
        self.row = self.col = 0
        self.SetNumberRows(0)
        self.SetNumberCols(2)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.EnableEditing(True)
        #self.EnableCellEditControl(True)
        #self.EnableGridLines(False)

    def populate(self, node, tree):
        self.node = node
        self.tree = tree
        self.data = tree.GetItemData(node).GetData()[0]
        self.SetNumberRows(tree.GetChildrenCount(node, False))
        self.children = []
        self.Unbind(wx.grid.EVT_GRID_CELL_CHANGE)
        for child in tree.Children(node):
            self.children.append(child)   
        index = 0
        if type(self.data) is dict:
            for key in self.data.iterkeys():
                self.SetCellValue(index, 0, str(key))
                self.SetCellValue(index, 1, str(self.data[key][0]))
                index = index + 1
        else:   #assume type array
            for i in self.data:
                self.SetCellValue(index, 0, str(index))
                self.SetCellValue(index, 1, str(i[0]))
                index = index + 1
        self.AutoSize()
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridCellChange)

    def OnGridCellChange(self, event):
        key = self.GetCellValue(event.GetRow(), 0)
        try:
            key = int(key)
        except:
            pass
        modkey = None
        mod = None
        if event.GetCol() > 0: # changing a value
            self.data[key] = Utility.TryToParse(self.GetCellValue(event.GetRow(), event.GetCol()))
            mod = True
        else:                  # changing an attribute
            newkey = TryToParse(self.GetCellValue(event.GetRow(), event.GetCol()))
            self.data[newkey] = self.data.pop(key)
            modkey = True
        self.tree.Modified(self.children[event.GetRow()] ,modkey, mod)

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



